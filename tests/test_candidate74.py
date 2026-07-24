from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C71 = ROOT / "prompts/candidates/the-caption-3ce91a4-validation-closure-r1"
C74 = ROOT / "prompts/candidates/the-caption-3ce91a4-typed-execution-state-machine-r1"
C71_PROFILE = ROOT / "evaluations/profiles/candidate71-validation-closure-v12-standard14-global-m24-n5-r1.json"
C74_PROFILE = ROOT / "evaluations/profiles/candidate74-typed-execution-state-machine-v12-standard14-global-m24-n5-r1.json"


class Candidate74Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source = verify_bundle(C71)
        cls.candidate = verify_bundle(C74)
        cls.prompt = (C74 / "files/AGENTS.md.txt").read_text(encoding="utf-8")

    def test_is_single_target_direct_child_of_candidate71(self) -> None:
        self.assertEqual(
            self.candidate["prompt_identity"],
            "the-caption-3ce91a4-typed-execution-state-machine-r1",
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

    def test_has_six_common_definition_sections_and_legacy_references(self) -> None:
        for heading in (
            "AUTHORITY_AND_TASKSPEC",
            "IDENTITY_AND_LINEAGE",
            "EXECUTION_STATE",
            "PRODUCER_AND_DELEGATION",
            "SCHEDULING_AND_VALIDATION",
            "METHOD_AND_RECOVERY",
        ):
            self.assertEqual(self.prompt.count(f"## {heading}\n"), 1)
        for label in (
            "SPEC",
            "PRODUCER",
            "TERMINAL",
            "CONTEXT",
            "OWNER_ROLE",
            "ROOT",
            "INDEPENDENCE",
            "DECISION_BOUNDARY",
            "VALIDATION_CLOSURE",
            "METHOD",
            "RECOVERY",
        ):
            self.assertIn(f"`{label}", self.prompt)

    def test_keeps_typed_authority_and_requested_value_boundary(self) -> None:
        for marker in (
            "`outcome_authority`",
            "`policy_authority`",
            "`runtime_authority`",
            "`method_authority`",
            "`method_control_authority`",
            "`dependency_authority`",
            "current value、option set、complement、test expectation、implementation convenience",
            "authorityも有限defaultもなければ実行を開始しない",
        ):
            self.assertIn(marker, self.prompt)

    def test_separates_identity_revision_and_result_validity(self) -> None:
        for marker in (
            "`operation_lineage_identity`",
            "`operation_execution_identity`",
            "`TaskSpec_revision`",
            "`predicate_contract_version`",
            "result_validity_key := operation_execution_identity",
            "target_or_artifact_version",
            "producer_execution_identity",
            "`TaskSpec_revision`を更新し、新しいoperation execution identityとproducer bindingを発行",
            "独立predicateを含めcurrent resultまたはterminal集約に使用しない",
        ):
            self.assertIn(marker, self.prompt)

    def test_separates_invocation_process_predicate_and_terminal_axes(self) -> None:
        for marker in (
            "terminal set := success | failed | unavailable",
            "nonterminal set := pending | running",
            "process_exit := zero | nonzero | signal | timeout | not_observed",
            "predicate_evaluation := pending | evaluated | unavailable",
            "predicate_value := true | false",
            "operation_evaluation_outcome := satisfied | unsatisfied | unavailable",
            "operation_stop_reason := none | prohibited",
            "process exitがnonzeroでも",
            "predicateを`false`へ自動変換しない",
            "`unsatisfied + prohibited`",
        ):
            self.assertIn(marker, self.prompt)

    def test_closes_delegation_root_and_context_boundaries(self) -> None:
        for marker in (
            "runtime_spawn_result.task_name == canonical task_identity",
            "FINAL_ANSWER.Sender == canonical task_identity",
            "`delegated_result_ready`はworker起動条件ではない",
            "missing result補完をしない",
            "`enforced_context_constraint`",
            "`advisory_context_constraint`",
            "`criterion_owner=none`",
        ):
            self.assertIn(marker, self.prompt)

    def test_closes_validation_method_and_recovery(self) -> None:
        for marker in (
            "dependency DAGがacyclic",
            "同一waveの全invocationを同一model stepから発行",
            "一部resultだけを見て次waveを発行しない",
            "`unexpected state`としてoperationをnonterminalへ戻し",
            "method_stop_condition := permitted candidate exhaustion | method budget exhaustion | explicit prohibition | permission denial",
            "一回のenvironment-only repair適用 + その直後のsame required command identityの一回のrerun",
            "command failureだけをpredicate`false`へ変換しない",
        ):
            self.assertIn(marker, self.prompt)

    def test_manifest_records_standard14_evaluated_revision_scope(self) -> None:
        artifact = self.candidate["artifact"]
        self.assertEqual(artifact["baseline_identity"], self.source["prompt_identity"])
        self.assertEqual(artifact["evaluation_status"], "standard14_evaluated")
        self.assertEqual(artifact["state"], "standard14_evaluated")
        self.assertIn("R-01からR-11", artifact["change_reason"])
        manifest = json.loads((C74 / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["provenance"]["runtime_projection_status"], "not_projected")

    def test_standard14_profile_changes_only_prompt_identity(self) -> None:
        source = json.loads(C71_PROFILE.read_text(encoding="utf-8"))
        candidate = json.loads(C74_PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(len(candidate["cases"]), 14)
        self.assertEqual(candidate["comparison_conditions"], source["comparison_conditions"])
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
