from __future__ import annotations

import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C43 = ROOT / "prompts/candidates/the-caption-3ce91a4-outcome-authority-boundary-r1"
C53 = ROOT / "prompts/candidates/the-caption-3ce91a4-purpose-separated-operation-graph-r1"


class Candidate53PromptTest(unittest.TestCase):
    def test_candidate_is_a_single_target_direct_child_of_candidate43(self) -> None:
        source = verify_bundle(C43)
        candidate = verify_bundle(C53)

        self.assertEqual(
            candidate["prompt_identity"],
            "the-caption-3ce91a4-purpose-separated-operation-graph-r1",
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

    def test_separates_readiness_fixed_operation_and_explicit_delegation(self) -> None:
        text = (C53 / "files/AGENTS.md.txt").read_text(encoding="utf-8")

        readiness = text.index("## Outcome readiness")
        operation = text.index("## Fixed operation")
        delegation = text.index("## Explicit delegation")
        self.assertLess(readiness, operation)
        self.assertLess(operation, delegation)
        self.assertIn("spec_ready=false", text[readiness:operation])
        self.assertNotIn("delegated_result_ready", text[readiness:operation])
        self.assertIn("- OPERATION:", text[operation:delegation])
        self.assertIn("- PRODUCER:", text[operation:delegation])
        self.assertIn("- COMPLETION:", text[operation:delegation])
        self.assertIn("- INDEPENDENCE:", text[operation:delegation])
        self.assertIn("TaskSpecが独立producer executionを明示した場合だけ", text[delegation:])

    def test_preserves_operation_graph_without_method_control(self) -> None:
        text = (C53 / "files/AGENTS.md.txt").read_text(encoding="utf-8")

        for required in (
            "`DELEGATION`がなければroot",
            "全predicateにbind済みproducerのterminal result",
            "同一predicateを別producerへ再割当てしない",
            "result欠落ならoperationもnonterminal",
            "criterion owner語列は担当情報でありworker指定ではない",
            "`fork_turns=none`",
            "rootがproducerでないoperation",
        ):
            self.assertIn(required, text)
        for forbidden in ("ROOT_BATCH", "同一model step", "commandを結合", "read順序"):
            self.assertNotIn(forbidden, text)

    def test_reduces_root_bytes_without_candidate49_level_collapse(self) -> None:
        source_size = (C43 / "files/AGENTS.md.txt").stat().st_size
        candidate_size = (C53 / "files/AGENTS.md.txt").stat().st_size

        self.assertLessEqual(candidate_size, int(source_size * 0.85))
        self.assertGreater(candidate_size, 3000)


if __name__ == "__main__":
    unittest.main()
