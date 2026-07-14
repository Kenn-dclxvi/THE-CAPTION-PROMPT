from __future__ import annotations

import hashlib
import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import duplicate_candidate, export_baseline, verify_bundle
from scripts.run_codex_evaluation import parse_usage, prepare_runtime_links, render_task


def git(root: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


class ExportPromptBundleTest(unittest.TestCase):
    def test_exports_baseline_and_bit_identical_candidate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source"
            source.mkdir()
            git(source, "init", "-q")
            git(source, "config", "user.name", "Bundle Test")
            git(source, "config", "user.email", "bundle@example.invalid")
            (source / "docs").mkdir()
            (source / "AGENTS.md").write_text("root instructions\n", encoding="utf-8")
            (source / "docs" / "AGENTS.md").write_text("docs instructions\n", encoding="utf-8")
            (source / "CLAUDE.md").symlink_to("AGENTS.md")
            git(source, "add", "AGENTS.md", "CLAUDE.md", "docs/AGENTS.md")
            git(source, "commit", "-qm", "prompt source")
            commit = git(source, "rev-parse", "HEAD")

            baseline_path = root / "baseline"
            candidate_path = root / "candidate"
            baseline = export_baseline(
                source,
                commit,
                "https://example.invalid/source.git",
                baseline_path,
                "baseline-r1",
                ["docs/AGENTS.md", "CLAUDE.md", "AGENTS.md"],
            )
            candidate = duplicate_candidate(baseline_path, candidate_path, "candidate-r1")

            self.assertEqual(baseline["artifact"]["artifact_role"], "baseline")
            self.assertEqual(candidate["artifact"]["artifact_role"], "candidate")
            self.assertEqual(candidate["artifact"]["baseline_identity"], "baseline-r1")
            self.assertEqual(candidate["content_relation"]["kind"], "bit_identical_copy")
            self.assertEqual(candidate["bundle_sha256"], baseline["bundle_sha256"])
            self.assertEqual(candidate["files"], baseline["files"])
            self.assertEqual((candidate_path / "files" / "AGENTS.md").read_bytes(), b"root instructions\n")
            self.assertTrue((candidate_path / "files" / "CLAUDE.md").is_symlink())
            self.assertEqual((candidate_path / "files" / "CLAUDE.md").readlink(), Path("AGENTS.md"))
            self.assertEqual(verify_bundle(candidate_path)["prompt_identity"], "candidate-r1")

    def test_renders_case_task_and_parses_codex_usage(self) -> None:
        task = render_task({"payload": {"trial_prompt_input": {"goal": "restore behavior"}}})
        total, usage = parse_usage(
            b'{"type":"turn.completed","usage":{"input_tokens":120,"output_tokens":30}}\n'
        )

        self.assertIn('"goal": "restore behavior"', task)
        self.assertEqual(total, 150)
        self.assertEqual(usage["input_tokens"], 120)

    def test_prepares_identity_checked_ignored_runtime_link(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            workspace = root / "workspace"
            runtime = root / "runtime"
            workspace.mkdir()
            runtime.mkdir()
            git(workspace, "init", "-q")
            git(workspace, "config", "user.name", "Runtime Test")
            git(workspace, "config", "user.email", "runtime@example.invalid")
            (workspace / ".gitignore").write_text(".venv/\n", encoding="utf-8")
            git(workspace, "add", ".gitignore")
            git(workspace, "commit", "-qm", "workspace")
            identity = runtime / "pyvenv.cfg"
            identity.write_text("runtime identity\n", encoding="utf-8")
            expected = hashlib.sha256(identity.read_bytes()).hexdigest()
            result = prepare_runtime_links(
                workspace,
                [
                    {
                        "target": ".venv",
                        "source": str(runtime),
                        "identity_file": "pyvenv.cfg",
                        "identity_sha256": expected,
                    }
                ],
            )

            self.assertTrue((workspace / ".venv").is_symlink())
            self.assertEqual(result[0]["identity_sha256"], expected)
            self.assertEqual(git(workspace, "status", "--short"), "")

    def test_can_copy_runtime_inside_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            workspace = root / "workspace"
            runtime = root / "runtime"
            workspace.mkdir()
            runtime.mkdir()
            git(workspace, "init", "-q")
            git(workspace, "config", "user.name", "Runtime Test")
            git(workspace, "config", "user.email", "runtime@example.invalid")
            (workspace / ".gitignore").write_text(".venv/\n", encoding="utf-8")
            git(workspace, "add", ".gitignore")
            git(workspace, "commit", "-qm", "workspace")
            identity = runtime / "pyvenv.cfg"
            identity.write_text("runtime identity\n", encoding="utf-8")
            expected = hashlib.sha256(identity.read_bytes()).hexdigest()

            result = prepare_runtime_links(
                workspace,
                [
                    {
                        "target": ".venv",
                        "source": str(runtime),
                        "identity_file": "pyvenv.cfg",
                        "identity_sha256": expected,
                        "materialization": "copy",
                    }
                ],
            )

            self.assertFalse((workspace / ".venv").is_symlink())
            self.assertEqual((workspace / ".venv" / "pyvenv.cfg").read_bytes(), identity.read_bytes())
            self.assertEqual(result[0]["materialization"], "copy")
            self.assertEqual(git(workspace, "status", "--short"), "")


if __name__ == "__main__":
    unittest.main()
