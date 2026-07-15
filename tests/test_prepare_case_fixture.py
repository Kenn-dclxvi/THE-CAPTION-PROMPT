from __future__ import annotations

import hashlib
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.prepare_case_fixture import FixtureError, prepare_fixture
from scripts.prepare_evaluation_set import prepare_evaluation_set


def git(root: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class PrepareCaseFixtureTest(unittest.TestCase):
    def make_source_and_case(self, root: Path) -> tuple[Path, Path]:
        source = root / "source"
        source.mkdir()
        git(source, "init", "-q")
        git(source, "config", "user.name", "Fixture Test")
        git(source, "config", "user.email", "fixture@example.invalid")
        target = source / "target.txt"
        target.write_text("keep\nremove\n", encoding="utf-8")
        git(source, "add", "target.txt")
        git(source, "commit", "-qm", "fixture source")
        commit = git(source, "rev-parse", "HEAD^{commit}")
        tree = git(source, "rev-parse", "HEAD^{tree}")
        preimage_blob = git(source, "rev-parse", "HEAD:target.txt")

        case = root / "case"
        private = case / "private"
        private.mkdir(parents=True)
        patch = private / "seed.patch"
        patch.write_text(
            "diff --git a/target.txt b/target.txt\n"
            "--- a/target.txt\n"
            "+++ b/target.txt\n"
            "@@ -1,2 +1 @@\n"
            " keep\n"
            "-remove\n",
            encoding="utf-8",
        )
        postimage = root / "postimage.txt"
        postimage.write_text("keep\n", encoding="utf-8")
        postimage_blob = git(source, "hash-object", str(postimage))
        data = {
            "case_id": "TEST-CASE",
            "case_revision": "r1",
            "seed": {
                "artifact": {
                    "path": "private/seed.patch",
                    "format": "git_diff",
                    "raw_sha256": sha256(patch),
                },
                "application_contract": {
                    "target_commit": commit,
                    "target_tree": tree,
                    "preimage_files": [
                        {
                            "path": "target.txt",
                            "mode": "100644",
                            "git_blob_sha1": preimage_blob,
                            "raw_sha256": sha256(target),
                        }
                    ],
                },
                "expected_post_seed_files": [
                    {
                        "path": "target.txt",
                        "mode": "100644",
                        "git_blob_sha1": postimage_blob,
                        "raw_sha256": sha256(postimage),
                    }
                ],
            },
        }
        (private / "case-data.json").write_text(json.dumps(data), encoding="utf-8")
        (case / "trial-prompt-input.json").write_text(
            json.dumps({"task_kind_goal_and_done_condition": "restore target behavior"}),
            encoding="utf-8",
        )
        return source, case

    def test_prepares_self_contained_seeded_clone(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source, case = self.make_source_and_case(root)
            output = root / "fixture"

            result = prepare_fixture(case, source, output)

            self.assertEqual(result["changed_paths"], ["target.txt"])
            self.assertEqual((output / "target.txt").read_text(encoding="utf-8"), "keep\n")
            self.assertEqual(git(output, "remote"), "")
            self.assertEqual(git(output, "status", "--short"), "M target.txt")
            self.assertFalse((output / ".git" / "objects" / "info" / "alternates").exists())
            self.assertTrue((output / "logs").is_dir())
            self.assertEqual(git(source, "status", "--short"), "")

    def test_removes_partial_output_when_postimage_check_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source, case = self.make_source_and_case(root)
            data_path = case / "private" / "case-data.json"
            data = json.loads(data_path.read_text(encoding="utf-8"))
            data["seed"]["expected_post_seed_files"][0]["raw_sha256"] = "0" * 64
            data_path.write_text(json.dumps(data), encoding="utf-8")
            output = root / "fixture"

            with self.assertRaisesRegex(FixtureError, "post-seed SHA-256 mismatch"):
                prepare_fixture(case, source, output)

            self.assertFalse(output.exists())

    def test_can_commit_seed_for_a_clean_agent_start(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source, case = self.make_source_and_case(root)
            data_path = case / "private" / "case-data.json"
            data = json.loads(data_path.read_text(encoding="utf-8"))
            data["seed"]["fixture_materialization"] = {
                "mode": "committed_seed",
                "commit": {
                    "message": "evaluation fixture seed",
                    "timestamp": "2000-01-01T00:00:00Z",
                    "author_name": "Fixture Evaluation",
                    "author_email": "fixture@example.invalid",
                },
            }
            data_path.write_text(json.dumps(data), encoding="utf-8")
            output = root / "fixture"
            source_head = git(source, "rev-parse", "HEAD")

            result = prepare_fixture(case, source, output)

            self.assertEqual(result["seeded_paths"], ["target.txt"])
            self.assertEqual(result["changed_paths"], [])
            self.assertEqual(git(output, "status", "--short"), "")
            self.assertEqual(git(output, "rev-parse", "HEAD^1"), source_head)
            self.assertEqual((output / "target.txt").read_text(encoding="utf-8"), "keep\n")
            self.assertEqual(result["runtime_directories"], ["logs"])
            self.assertTrue((output / "logs").is_dir())

    def test_prepares_clean_checkout_without_a_seed_patch(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source, case = self.make_source_and_case(root)
            data_path = case / "private" / "case-data.json"
            data = json.loads(data_path.read_text(encoding="utf-8"))
            commit = git(source, "rev-parse", "HEAD^{commit}")
            tree = git(source, "rev-parse", "HEAD^{tree}")
            blob = git(source, "rev-parse", "HEAD:target.txt")
            data["fixture"] = {
                "target_identity": {"commit": commit, "tree": tree},
                "source_files": [
                    {
                        "path": "target.txt",
                        "mode": "100644",
                        "git_blob_sha1": blob,
                        "raw_sha256": sha256(source / "target.txt"),
                    }
                ],
                "absent_paths": ["missing.txt"],
            }
            data["seed"] = {
                "status": "clean_checkout",
                "operations": [],
                "fixture_materialization": {"mode": "clean_checkout"},
            }
            data_path.write_text(json.dumps(data), encoding="utf-8")
            output = root / "fixture"

            result = prepare_fixture(case, source, output)

            self.assertEqual(result["seeded_paths"], [])
            self.assertEqual(result["changed_paths"], [])
            self.assertEqual(result["fixture_head_commit"], commit)
            self.assertEqual(result["fixture_head_tree"], tree)
            self.assertEqual(git(output, "status", "--short"), "")
            self.assertEqual(git(output, "remote"), "")
            self.assertTrue((output / "logs").is_dir())

    def test_refuses_output_inside_source_repository(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source, case = self.make_source_and_case(root)
            output = source / "fixture"

            with self.assertRaisesRegex(FixtureError, "output must not be inside the source repository"):
                prepare_fixture(case, source, output)

            self.assertFalse(output.exists())

    def test_prepares_evaluation_set_without_private_case_data(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source, case = self.make_source_and_case(root)
            output = root / "evaluation-set"

            result = prepare_evaluation_set(case, source, output)

            capsule = json.loads((output / "set.json").read_text(encoding="utf-8"))
            self.assertEqual(result["set_id"], "test-case-r1")
            self.assertEqual(capsule["cases"][0]["fixture"], "fixture")
            self.assertEqual(capsule["cases"][0]["fixture_condition_paths"], ["target.txt"])
            self.assertEqual(
                capsule["cases"][0]["payload"]["trial_prompt_input"],
                {"task_kind_goal_and_done_condition": "restore target behavior"},
            )
            serialized = json.dumps(capsule)
            self.assertNotIn("expected_post_seed_files", serialized)
            self.assertNotIn("git_blob_sha1", serialized)
            self.assertTrue((output / "fixture" / ".git").is_dir())


if __name__ == "__main__":
    unittest.main()
