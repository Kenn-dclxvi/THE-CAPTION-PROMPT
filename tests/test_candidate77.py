from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C71 = ROOT / "prompts/candidates/the-caption-3ce91a4-validation-closure-r1"
C77 = ROOT / "prompts/candidates/the-caption-3ce91a4-triggered-exception-transition-r1"
C76_PROFILE = ROOT / "evaluations/profiles/candidate76-final-state-validation-wave-v12-standard14-global-m24-n5-r1.json"
C77_PROFILE = ROOT / "evaluations/profiles/candidate77-triggered-exception-transition-v12-standard14-global-m24-n5-r1.json"


def labelled_lines(text: str) -> dict[str, str]:
    blocks = {}
    for line in text.splitlines():
        if not line.startswith("- "):
            continue
        label, body = line[2:].split(": ", 1)
        blocks[label] = body
    return blocks


class Candidate77Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source = verify_bundle(C71)
        cls.candidate = verify_bundle(C77)
        cls.source_root = (C71 / "files/AGENTS.md").read_text(encoding="utf-8")
        cls.root_prompt = (C77 / "files/AGENTS.md").read_text(encoding="utf-8")
        cls.exception_spec = (C77 / "files/docs/prompt-guide.md").read_text(
            encoding="utf-8"
        )

    def test_is_two_target_direct_child_of_candidate71(self) -> None:
        self.assertEqual(
            self.candidate["prompt_identity"],
            "the-caption-3ce91a4-triggered-exception-transition-r1",
        )
        self.assertEqual(
            self.candidate["content_relation"],
            {
                "changed_targets": ["AGENTS.md", "docs/prompt-guide.md"],
                "kind": "direct_child_full_bundle",
                "source_prompt_identity": self.source["prompt_identity"],
            },
        )
        changed = {"AGENTS.md", "docs/prompt-guide.md"}
        self.assertEqual(
            [entry for entry in self.candidate["files"] if entry["target"] not in changed],
            [entry for entry in self.source["files"] if entry["target"] not in changed],
        )

    def test_preserves_candidate71_core_verbatim(self) -> None:
        source = labelled_lines(self.source_root)
        candidate = labelled_lines(self.root_prompt)
        self.assertEqual(
            list(candidate),
            [
                "SPEC",
                "PRODUCER",
                "TERMINAL",
                "CONTEXT",
                "OWNER_ROLE",
                "ROOT",
                "INDEPENDENCE",
                "DECISION_BOUNDARY",
                "VALIDATION_CLOSURE",
                "EXCEPTION_TRANSITION",
                "METHOD",
                "RECOVERY",
            ],
        )
        self.assertEqual({label: candidate[label] for label in source}, source)

    def test_root_contains_only_trigger_gate_not_typed_state_body(self) -> None:
        self.assertLessEqual(len(self.root_prompt.encode("utf-8")), 7_500)
        gate = labelled_lines(self.root_prompt)["EXCEPTION_TRANSITION"]
        for heading in (
            "AUTHORITY_AND_TASKSPEC",
            "IDENTITY_AND_LINEAGE",
            "EXECUTION_STATE",
            "PRODUCER_AND_DELEGATION",
            "SCHEDULING_AND_VALIDATION",
            "METHOD_AND_RECOVERY",
        ):
            self.assertIn(heading, gate)
        self.assertIn("triggerがなければ同fileを読まず", gate)
        self.assertIn("requested outcome valueをuserまたは直接要求するrepository authority", gate)
        self.assertIn("permission / constraintをpolicy", gate)
        self.assertIn("runtime identityをruntime evidence", gate)
        self.assertIn("未指定methodをpermission内のexecutor choice", gate)
        self.assertIn("current operation / producer / predicate / target versionへbind", gate)
        self.assertIn("追加のidentity / version / DAG / budgetをmaterializeしない", gate)
        self.assertIn("対応しない節を読まず", gate)
        self.assertIn("例外解決後はC71 coreのterminal closureへ戻る", gate)
        for marker in (
            "result_validity_key :=",
            "invocation_status :=",
            "method_stop_condition :=",
            "environment_recovery_attempt :=",
        ):
            self.assertNotIn(marker, self.root_prompt)

    def test_exception_spec_has_six_sections_and_all_revisions(self) -> None:
        for heading in (
            "AUTHORITY_AND_TASKSPEC",
            "IDENTITY_AND_LINEAGE",
            "EXECUTION_STATE",
            "PRODUCER_AND_DELEGATION",
            "SCHEDULING_AND_VALIDATION",
            "METHOD_AND_RECOVERY",
        ):
            self.assertEqual(self.exception_spec.count(f"## {heading}\n"), 1)
        for revision in range(1, 15):
            self.assertEqual(self.exception_spec.count(f"### R-{revision:02d} "), 1)

    def test_exception_spec_preserves_required_state_semantics(self) -> None:
        for marker in (
            "`outcome_authority`",
            "`policy_authority`",
            "`runtime_authority`",
            "`method_authority`",
            "`method_control_authority`",
            "`dependency_authority`",
            "`operation_lineage_identity`",
            "`operation_execution_identity`",
            "`TaskSpec_revision`",
            "`predicate_contract_version`",
            "result_validity_key := operation_execution_identity",
            "terminal := success | failed | unavailable",
            "nonterminal := pending | running",
            "process_exit := zero | nonzero | signal | timeout | not_observed",
            "predicate_evaluation := pending | evaluated | unavailable",
            "operation_evaluation_outcome := satisfied | unsatisfied | unavailable",
            "operation_stop_reason := none | prohibited",
            "predicateを`false`へ自動変換しない",
            "`unsatisfied + prohibited`",
            "runtime_spawn_result.task_name == canonical task_identity",
            "FINAL_ANSWER.Sender == canonical task_identity",
            "missing result補完を行わない",
            "`enforced_context_constraint`",
            "`advisory_context_constraint`",
            "dependency DAGがacyclic",
            "一部resultだけを見て次waveを発行しない",
            "`final_state_observer :=",
            "`unexpected state`としてnonterminalへ戻す",
            "method_stop_condition := permitted candidate exhaustion | method budget exhaustion | explicit prohibition | permission denial",
            "一回のenvironment-only repair + 直後のsame required command identityの一回rerun",
            "command failureだけをpredicate falseへ変換しない",
            "`criterion_owner=none`",
        ):
            self.assertIn(marker, self.exception_spec)

    def test_acceptance_mapping_covers_a_through_q(self) -> None:
        mapping = self.exception_spec.split("## Acceptance mapping\n", 1)[1]
        for scenario in "ABCDEFGHIJKLMNOPQ":
            self.assertIn(f"| {scenario} ", mapping)

    def test_manifest_records_standard14_evaluated_stopped_state(self) -> None:
        manifest = json.loads((C77 / "manifest.json").read_text(encoding="utf-8"))
        artifact = manifest["artifact"]
        self.assertEqual(artifact["baseline_identity"], self.source["prompt_identity"])
        self.assertEqual(artifact["evaluation_status"], "standard14_evaluated")
        self.assertEqual(artifact["state"], "stopped")
        self.assertEqual(
            manifest["provenance"]["evaluation_status"],
            "standard14_evaluated_stopped",
        )
        self.assertEqual(manifest["provenance"]["runtime_projection_status"], "not_projected")

    def test_standard14_profile_changes_only_prompt_identity(self) -> None:
        source = json.loads(C76_PROFILE.read_text(encoding="utf-8"))
        candidate = json.loads(C77_PROFILE.read_text(encoding="utf-8"))
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
