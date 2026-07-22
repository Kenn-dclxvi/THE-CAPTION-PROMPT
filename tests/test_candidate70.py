from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C69 = (
    ROOT
    / "prompts/candidates/the-caption-3ce91a4-model-reentry-decision-boundary-r1"
)
C70 = ROOT / "prompts/candidates/the-caption-3ce91a4-machine-decision-boundary-r1"
C69_PROFILE = (
    ROOT
    / "evaluations/profiles/candidate69-model-reentry-decision-boundary-v11-machine-boundary-targeted4-global-m24-n5-r1.json"
)
C70_PROFILE = (
    ROOT
    / "evaluations/profiles/candidate70-machine-decision-boundary-v11-machine-boundary-targeted4-global-m24-n5-r1.json"
)
STANDARD_PROFILE = (
    ROOT
    / "evaluations/profiles/candidate69-model-reentry-decision-boundary-v10-standard14-global-m24-n5-r1.json"
)
V11_STANDARD_PROFILE = (
    ROOT
    / "evaluations/profiles/candidate69-model-reentry-decision-boundary-v11-standard14-global-m24-n5-r1.json"
)
C70_STANDARD_PROFILE = (
    ROOT
    / "evaluations/profiles/candidate70-machine-decision-boundary-v10-standard14-global-m24-n5-r1.json"
)

MACHINE_BOUNDARY = (
    "- MACHINE_BOUNDARY: `machine_result := structured exit code / status / boolean`。"
    "`machine_boundary := decision_boundary ∧ bind済みmachine_resultだけで後続"
    "invocationの発行またはstopが一意 ∧ 後続のidentity / "
    "command / permission / stop conditionが発行前にbind済み`。machine boundaryでは"
    "modelへ戻らず、同一tool call内で各commandを個別invocationとして順に発行し、"
    "最初のnon-successまたは全success後に全resultを一度だけmodelへ返す。target / "
    "method / recoveryの意味判断が残るresultは含めない。\n"
)


def labelled_lines(text: str) -> dict[str, str]:
    blocks = {}
    for line in text.splitlines():
        if not line.startswith("- "):
            continue
        label, body = line[2:].split(": ", 1)
        blocks[label] = body
    return blocks


class Candidate70Test(unittest.TestCase):
    def test_is_a_single_target_direct_child_of_candidate69(self) -> None:
        source = verify_bundle(C69)
        candidate = verify_bundle(C70)
        self.assertEqual(
            candidate["prompt_identity"],
            "the-caption-3ce91a4-machine-decision-boundary-r1",
        )
        self.assertEqual(
            candidate["content_relation"],
            {
                "changed_targets": ["AGENTS.md"],
                "kind": "direct_child_full_bundle",
                "source_prompt_identity": source["prompt_identity"],
            },
        )

        source_manifest = json.loads((C69 / "manifest.json").read_text(encoding="utf-8"))
        candidate_manifest = json.loads(
            (C70 / "manifest.json").read_text(encoding="utf-8")
        )
        self.assertEqual(
            [entry for entry in candidate_manifest["files"] if entry["target"] != "AGENTS.md"],
            [entry for entry in source_manifest["files"] if entry["target"] != "AGENTS.md"],
        )

    def test_adds_only_machine_boundary(self) -> None:
        source_text = (C69 / "files/AGENTS.md").read_text(encoding="utf-8")
        candidate_text = (C70 / "files/AGENTS.md").read_text(encoding="utf-8")
        anchor = "- METHOD:"
        expected = source_text.replace(anchor, MACHINE_BOUNDARY + anchor)
        self.assertEqual(candidate_text, expected)

    def test_preserves_candidate69_labels_and_adds_one_invariant(self) -> None:
        source = labelled_lines((C69 / "files/AGENTS.md").read_text(encoding="utf-8"))
        candidate = labelled_lines((C70 / "files/AGENTS.md").read_text(encoding="utf-8"))
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
                "MACHINE_BOUNDARY",
                "METHOD",
                "RECOVERY",
            ],
        )
        self.assertEqual({label: candidate[label] for label in source}, source)
        invariant = candidate["MACHINE_BOUNDARY"]
        self.assertIn("machine_result := structured exit code / status / boolean", invariant)
        self.assertIn("bind済みmachine_resultだけで後続invocationの発行またはstopが一意", invariant)
        self.assertIn("同一tool call内で各commandを個別invocation", invariant)
        self.assertIn("全resultを一度だけmodelへ返す", invariant)
        self.assertIn("target / method / recoveryの意味判断が残るresultは含めない", invariant)
        for case_specific_term in ("read-only", "F04", "F06", "F07", "A02"):
            self.assertNotIn(case_specific_term, invariant)

    def test_targeted_profiles_change_only_prompt_identity(self) -> None:
        manifest = verify_bundle(C70)
        source = json.loads(C69_PROFILE.read_text(encoding="utf-8"))
        candidate = json.loads(C70_PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(
            candidate["prompt_set_identity"],
            {
                "bundle_sha256": manifest["bundle_sha256"],
                "name": manifest["prompt_identity"],
                "revision": "r1",
            },
        )
        comparable_source = copy.deepcopy(source)
        comparable_candidate = copy.deepcopy(candidate)
        for profile in (comparable_source, comparable_candidate):
            profile.pop("profile_id")
            profile.pop("prompt_set_identity")
        self.assertEqual(comparable_candidate, comparable_source)

    def test_targeted_profile_keeps_standard_executor_conditions(self) -> None:
        standard = json.loads(V11_STANDARD_PROFILE.read_text(encoding="utf-8"))
        targeted = json.loads(C69_PROFILE.read_text(encoding="utf-8"))
        for field in (
            "agent_environment",
            "model",
            "permission",
            "quality_rating",
            "repetition_condition",
            "target_repository_ref",
        ):
            self.assertEqual(
                targeted["comparison_conditions"][field],
                standard["comparison_conditions"][field],
            )
        for field in (
            "duration_hint_method",
            "environment_adjustment",
            "max_attempts",
            "max_workers",
            "monitor_interval_seconds",
            "reasoning_effort",
            "schedule_policy",
            "token_accounting",
        ):
            self.assertEqual(
                targeted["comparison_conditions"]["executor_parameters"][field],
                standard["comparison_conditions"]["executor_parameters"][field],
            )
        self.assertEqual(targeted["execution"]["max_workers"], 24)

    def test_standard14_profiles_change_only_prompt_identity(self) -> None:
        manifest = verify_bundle(C70)
        source = json.loads(STANDARD_PROFILE.read_text(encoding="utf-8"))
        candidate = json.loads(C70_STANDARD_PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(len(source["cases"]), 14)
        self.assertEqual(
            candidate["prompt_set_identity"],
            {
                "bundle_sha256": manifest["bundle_sha256"],
                "name": manifest["prompt_identity"],
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
