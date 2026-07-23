from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C75 = ROOT / "prompts/candidates/the-caption-3ce91a4-authority-bound-validation-fast-path-r1"
C76 = ROOT / "prompts/candidates/the-caption-3ce91a4-final-state-validation-wave-r1"
C75_PROFILE = ROOT / "evaluations/profiles/candidate75-authority-bound-validation-fast-path-v12-validation-fast-path-f06-global-m5-n5-r1.json"
C76_PROFILE = ROOT / "evaluations/profiles/candidate76-final-state-validation-wave-v12-validation-fast-path-f06-global-m5-n5-r1.json"
C74_STANDARD_PROFILE = ROOT / "evaluations/profiles/candidate74-typed-execution-state-machine-v12-standard14-global-m24-n5-r1.json"
C76_STANDARD_PROFILE = ROOT / "evaluations/profiles/candidate76-final-state-validation-wave-v12-standard14-global-m24-n5-r1.json"


class Candidate76Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source = verify_bundle(C75)
        cls.candidate = verify_bundle(C76)
        cls.source_prompt = (C75 / "files/AGENTS.md").read_text(encoding="utf-8")
        cls.prompt = (C76 / "files/AGENTS.md").read_text(encoding="utf-8")

    def test_is_single_target_direct_child_of_candidate75(self) -> None:
        self.assertEqual(
            self.candidate["prompt_identity"],
            "the-caption-3ce91a4-final-state-validation-wave-r1",
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

    def test_adds_only_final_state_observer_rule(self) -> None:
        addition = (
            "`final_state_observer := 他required invocation完了後のtarget / artifact / worktree versionをpass conditionが観測するvalidation`。"
            "test、lint、buildその他のrequired invocationが観測対象pathを生成・変更・削除し得る場合、pass conditionとtarget versionをpolicy authorityとして各potential mutatorからfinal-state observerへdependency edgeをbindする。"
            "diff、status、path-scope、生成物確認など複数のfinal-state observerは、全potential mutator完了後の同一waveへまとめる。"
            "このedgeは最終versionを観測する順序だけを固定し、先行resultによるearly-stopまたは後続省略を許可しない。\n\n"
        )
        expected = self.source_prompt.replace(
            "`validation_fast_path_ready := validation_set_ready ∧ 全required validationがindependent ∧ decision boundaryなし`。",
            "`validation_fast_path_ready := validation_set_ready ∧ 全required validationがindependent ∧ final-state observerなし ∧ decision boundaryなし`。",
        ).replace(
            "### Validation wave\n",
            addition + "### Validation wave\n",
        )
        self.assertEqual(self.prompt, expected)

    def test_preserves_fast_path_and_typed_state_markers(self) -> None:
        for marker in (
            "`operation_execution_identity`",
            "`result_validity_key",
            "invocation_status := pending | running | success | failed | unavailable",
            "predicate_evaluation := pending | evaluated | unavailable",
            "`validation_independence_policy`",
            "全required validationを個別invocationとして同一model stepから一つのwaveで発行",
            "status再確認、line再読、根拠再取得を含むread / validationを追加せず",
            "method_stop_condition := permitted candidate exhaustion",
        ):
            self.assertIn(marker, self.prompt)

    def test_targeted_profile_changes_only_prompt_identity(self) -> None:
        source = json.loads(C75_PROFILE.read_text(encoding="utf-8"))
        candidate = json.loads(C76_PROFILE.read_text(encoding="utf-8"))
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

    def test_standard14_profile_changes_only_prompt_identity(self) -> None:
        source = json.loads(C74_STANDARD_PROFILE.read_text(encoding="utf-8"))
        candidate = json.loads(C76_STANDARD_PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(len(candidate["cases"]), 14)
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
