from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C74 = ROOT / "prompts/candidates/the-caption-3ce91a4-typed-execution-state-machine-r1"
C75 = ROOT / "prompts/candidates/the-caption-3ce91a4-authority-bound-validation-fast-path-r1"
C74_PROFILE = ROOT / "evaluations/profiles/candidate74-typed-execution-state-machine-v12-validation-fast-path-f06-global-m5-n5-r1.json"
C75_PROFILE = ROOT / "evaluations/profiles/candidate75-authority-bound-validation-fast-path-v12-validation-fast-path-f06-global-m5-n5-r1.json"


class Candidate75Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source = verify_bundle(C74)
        cls.candidate = verify_bundle(C75)
        cls.source_prompt = (C74 / "files/AGENTS.md").read_text(encoding="utf-8")
        cls.prompt = (C75 / "files/AGENTS.md").read_text(encoding="utf-8")

    def test_is_single_target_direct_child_of_candidate74(self) -> None:
        self.assertEqual(
            self.candidate["prompt_identity"],
            "the-caption-3ce91a4-authority-bound-validation-fast-path-r1",
        )
        self.assertEqual(
            self.candidate["content_relation"],
            {
                "changed_targets": ["AGENTS.md"],
                "kind": "direct_child_full_bundle",
                "source_prompt_identity": self.source["prompt_identity"],
            },
        )
        self.assertEqual(
            [entry for entry in self.candidate["files"] if entry["target"] != "AGENTS.md"],
            [entry for entry in self.source["files"] if entry["target"] != "AGENTS.md"],
        )

    def test_changes_only_scheduling_and_validation_section(self) -> None:
        source_before, source_tail = self.source_prompt.split(
            "## SCHEDULING_AND_VALIDATION\n", 1
        )
        candidate_before, candidate_tail = self.prompt.split(
            "## SCHEDULING_AND_VALIDATION\n", 1
        )
        source_after = source_tail.split("## METHOD_AND_RECOVERY\n", 1)[1]
        candidate_after = candidate_tail.split("## METHOD_AND_RECOVERY\n", 1)[1]
        self.assertEqual(candidate_before, source_before)
        self.assertEqual(candidate_after, source_after)

    def test_preserves_candidate74_typed_state_structure(self) -> None:
        for marker in (
            "`outcome_authority`",
            "`dependency_authority`",
            "`operation_execution_identity`",
            "`result_validity_key",
            "invocation_status := pending | running | success | failed | unavailable",
            "predicate_evaluation := pending | evaluated | unavailable",
            "operation_lifecycle := spec_pending | ready | running | terminal | invalidated",
            "`delegated_result_ready",
            "method_stop_condition := permitted candidate exhaustion",
            "environment_recovery_attempt",
        ):
            self.assertIn(marker, self.prompt)

    def test_defines_authority_bound_independent_fast_path(self) -> None:
        for marker in (
            "dependencyは`dependency_authority`が直接固定したedgeだけ",
            "focused / full、coverage包含、command cost、慣例的なfail-fast",
            "`validation_independence_policy`",
            "validation_fast_path_ready := validation_set_ready ∧ 全required validationがindependent ∧ decision boundaryなし",
            "全required validationを個別invocationとして同一model stepから一つのwaveで発行",
            "一部resultだけを見て次を判断しない",
            "`validation_fast_path_ready=false`の場合だけ",
            "明示edgeのないnodeを、既存waveのresultを見たという理由だけで後続waveへ移さない",
        ):
            self.assertIn(marker, self.prompt)

    def test_closes_success_without_additional_read(self) -> None:
        self.assertIn(
            "status再確認、line再読、根拠再取得を含むread / validationを追加せず、bind済みresultからterminalとfinal responseを一度で確定",
            self.prompt,
        )

    def test_targeted_profiles_change_only_prompt_identity(self) -> None:
        source = json.loads(C74_PROFILE.read_text(encoding="utf-8"))
        candidate = json.loads(C75_PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(candidate["cases"], [{"id": "TC-F06-RESTORE-EMPTY-SNAPSHOT-CONTRACT", "revision": "r2"}])
        self.assertEqual(
            candidate["prompt_set_identity"],
            {
                "bundle_sha256": self.candidate["bundle_sha256"],
                "name": self.candidate["prompt_identity"],
                "revision": "r1",
            },
        )
        comparable_source = copy.deepcopy(source)
        comparable_candidate = copy.deepcopy(candidate)
        for profile in (comparable_source, comparable_candidate):
            profile.pop("profile_id")
            profile.pop("prompt_set_identity")
        self.assertEqual(comparable_candidate, comparable_source)


if __name__ == "__main__":
    unittest.main()
