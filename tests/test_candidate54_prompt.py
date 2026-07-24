from __future__ import annotations

import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C43 = ROOT / "prompts/candidates/the-caption-3ce91a4-outcome-authority-boundary-r1"
C54 = ROOT / "prompts/candidates/the-caption-3ce91a4-evidence-backed-control-core-r1"


class Candidate54PromptTest(unittest.TestCase):
    def test_candidate_is_a_single_target_direct_child_of_candidate43(self) -> None:
        source = verify_bundle(C43)
        candidate = verify_bundle(C54)

        self.assertEqual(
            candidate["prompt_identity"],
            "the-caption-3ce91a4-evidence-backed-control-core-r1",
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

    def test_keeps_readiness_fixed_operation_and_conditional_delegation(self) -> None:
        text = (C54 / "files/AGENTS.md.txt").read_text(encoding="utf-8")

        readiness = text.index("## Readiness")
        operation = text.index("## Fixed operation")
        delegation = text.index("## Explicit delegation")
        self.assertLess(readiness, operation)
        self.assertLess(operation, delegation)
        for required in (
            "未確定値があれば、その値だけを質問して停止する",
            "同じoperationのpredicate実行またはresult生成を別producerへ再割当てしない",
            "required predicateすべてにbind済みproducerのterminal result",
            "final responseで補完しない",
            "criterion owner語列は担当情報であり、worker指定ではない",
            "TaskSpecが独立producer executionを明示した場合だけ",
            "runtime_spawn_result.task_name",
            "FINAL_ANSWER.Sender",
            "fork_turns=none",
        ):
            self.assertIn(required, text)

    def test_omits_unproven_always_visible_controls(self) -> None:
        text = (C54 / "files/AGENTS.md.txt").read_text(encoding="utf-8")

        for forbidden in (
            "environment recovery",
            "environment_recovery_max",
            "producer変更は理由を問わず旧bindingを失効",
            "TaskSpec該当範囲",
            "scoped diffまたはresult",
            "owner / pass condition",
        ):
            self.assertNotIn(forbidden, text)

    def test_reduces_root_bytes_beyond_candidate53(self) -> None:
        source_size = (C43 / "files/AGENTS.md.txt").stat().st_size
        candidate_size = (C54 / "files/AGENTS.md.txt").stat().st_size

        self.assertLessEqual(candidate_size, int(source_size * 0.65))
        self.assertGreater(candidate_size, 2200)


if __name__ == "__main__":
    unittest.main()
