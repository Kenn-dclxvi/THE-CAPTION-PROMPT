from __future__ import annotations

import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C43 = ROOT / "prompts/candidates/the-caption-3ce91a4-outcome-authority-boundary-r1"
C55 = ROOT / "prompts/candidates/the-caption-3ce91a4-prebound-operation-graph-r1"


class Candidate55PromptTest(unittest.TestCase):
    def test_candidate_is_a_single_target_direct_child_of_candidate43(self) -> None:
        source = verify_bundle(C43)
        candidate = verify_bundle(C55)

        self.assertEqual(
            candidate["prompt_identity"],
            "the-caption-3ce91a4-prebound-operation-graph-r1",
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

    def test_prebinds_fixed_operation_input_before_first_predicate(self) -> None:
        text = (C55 / "files/AGENTS.md.txt").read_text(encoding="utf-8")

        self.assertIn("初回predicate前に", text)
        self.assertIn(
            "TaskSpecで確定済みの`required outcome / predicate / permission / constraint`を同一operationへbindする",
            text,
        )
        self.assertLess(text.index("- READINESS:"), text.index("- OPERATION:"))
        self.assertLess(text.index("- OPERATION:"), text.index("- PRODUCER:"))

    def test_keeps_conditional_delegation_without_phase_sections(self) -> None:
        text = (C55 / "files/AGENTS.md.txt").read_text(encoding="utf-8")

        for required in (
            "同じoperationのpredicate実行またはresult生成を別producerへ再割当てしない",
            "required predicateすべてにbind済みproducerのterminal result",
            "final responseで補完しない",
            "TaskSpecが独立producer executionを明示した場合だけ",
            "runtime_spawn_result.task_name",
            "FINAL_ANSWER.Sender",
            "fork_turns=none",
        ):
            self.assertIn(required, text)
        for forbidden in (
            "## Readiness",
            "## Fixed operation",
            "## Explicit delegation",
            "environment recovery",
            "environment_recovery_max",
        ):
            self.assertNotIn(forbidden, text)

    def test_reduces_root_bytes_while_restoring_the_missing_relation(self) -> None:
        source_size = (C43 / "files/AGENTS.md.txt").stat().st_size
        candidate_size = (C55 / "files/AGENTS.md.txt").stat().st_size

        self.assertLess(candidate_size, source_size)
        self.assertGreater(candidate_size, 2500)


if __name__ == "__main__":
    unittest.main()
