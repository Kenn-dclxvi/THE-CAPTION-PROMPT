from __future__ import annotations

import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C55 = ROOT / "prompts/candidates/the-caption-3ce91a4-prebound-operation-graph-r1"
C56 = ROOT / "prompts/candidates/the-caption-3ce91a4-resolved-fixed-read-boundary-r1"


class Candidate56PromptTest(unittest.TestCase):
    def test_candidate_is_a_single_target_direct_child_of_candidate55(self) -> None:
        source = verify_bundle(C55)
        candidate = verify_bundle(C56)

        self.assertEqual(
            candidate["prompt_identity"],
            "the-caption-3ce91a4-resolved-fixed-read-boundary-r1",
        )
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

    def test_fixed_read_is_f_only_and_requires_resolved_finite_input(self) -> None:
        text = (C56 / "files/AGENTS.md.txt").read_text(encoding="utf-8")

        operation = text.index("- OPERATION:")
        fixed_read = text.index("- FIXED_READ:")
        producer = text.index("- PRODUCER:")
        self.assertLess(operation, fixed_read)
        self.assertLess(fixed_read, producer)
        for required in (
            "readiness解決後",
            "rootがproducer",
            "有限の相互非依存read-only入力を確定済み",
            "個別tool callとexitを保って同一model step",
            "authority探索中",
            "先行resultで次のtargetが変わるread",
            "read集合を広げない",
        ):
            self.assertIn(required, text)

    def test_changes_only_the_fixed_read_predicate(self) -> None:
        source_lines = (C55 / "files/AGENTS.md.txt").read_text(encoding="utf-8").splitlines()
        candidate_lines = (C56 / "files/AGENTS.md.txt").read_text(encoding="utf-8").splitlines()

        added = [line for line in candidate_lines if line not in source_lines]
        self.assertEqual(len(added), 1)
        self.assertTrue(added[0].startswith("- FIXED_READ:"))
        self.assertEqual(
            [line for line in source_lines if line not in candidate_lines],
            [],
        )


if __name__ == "__main__":
    unittest.main()
