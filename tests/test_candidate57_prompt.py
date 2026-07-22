from __future__ import annotations

import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C56 = ROOT / "prompts/candidates/the-caption-3ce91a4-resolved-fixed-read-boundary-r1"
C57 = ROOT / "prompts/candidates/the-caption-3ce91a4-task-enumerated-read-boundary-r1"


class Candidate57PromptTest(unittest.TestCase):
    def test_candidate_replaces_one_target_from_candidate56(self) -> None:
        source = verify_bundle(C56)
        candidate = verify_bundle(C57)
        self.assertEqual(candidate["prompt_identity"], "the-caption-3ce91a4-task-enumerated-read-boundary-r1")
        self.assertEqual(
            candidate["content_relation"],
            {
                "changed_targets": ["AGENTS.md"],
                "kind": "direct_child_full_bundle",
                "source_prompt_identity": source["prompt_identity"],
            },
        )
        source_files = {entry["target"]: entry for entry in source["files"]}
        candidate_files = {entry["target"]: entry for entry in candidate["files"]}
        self.assertEqual(
            [target for target in sorted(source_files) if source_files[target] != candidate_files[target]],
            ["AGENTS.md"],
        )

    def test_fixed_read_requires_task_enumeration_and_excludes_authority_discovery(self) -> None:
        source = (C56 / "files/AGENTS.md").read_text(encoding="utf-8")
        candidate = (C57 / "files/AGENTS.md").read_text(encoding="utf-8")
        source_fixed = next(line for line in source.splitlines() if line.startswith("- FIXED_READ:"))
        candidate_fixed = next(line for line in candidate.splitlines() if line.startswith("- FIXED_READ:"))
        self.assertNotEqual(candidate_fixed, source_fixed)
        for required in (
            "実行前TaskSpec",
            "read pathまたはcommandを有限列挙",
            "列挙済みreadだけ",
            "repository authority / stateから対象を決めるread",
            "列挙を補完・拡張しない",
        ):
            self.assertIn(required, candidate_fixed)

    def test_changes_only_fixed_read_line(self) -> None:
        source = (C56 / "files/AGENTS.md").read_text(encoding="utf-8").splitlines()
        candidate = (C57 / "files/AGENTS.md").read_text(encoding="utf-8").splitlines()
        removed = [line for line in source if line not in candidate]
        added = [line for line in candidate if line not in source]
        self.assertEqual(len(removed), 1)
        self.assertEqual(len(added), 1)
        self.assertTrue(removed[0].startswith("- FIXED_READ:"))
        self.assertTrue(added[0].startswith("- FIXED_READ:"))


if __name__ == "__main__":
    unittest.main()
