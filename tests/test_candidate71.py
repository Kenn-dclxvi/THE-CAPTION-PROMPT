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
C71 = ROOT / "prompts/candidates/the-caption-3ce91a4-validation-closure-r1"
C69_PROFILE = (
    ROOT
    / "evaluations/profiles/candidate69-model-reentry-decision-boundary-v11-machine-boundary-targeted4-global-m24-n5-r1.json"
)
C71_PROFILE = (
    ROOT
    / "evaluations/profiles/candidate71-validation-closure-v11-machine-boundary-targeted4-global-m24-n5-r1.json"
)
C69_STANDARD_PROFILE = (
    ROOT
    / "evaluations/profiles/candidate69-model-reentry-decision-boundary-v10-standard14-global-m24-n5-r1.json"
)
C71_STANDARD_PROFILE = (
    ROOT
    / "evaluations/profiles/candidate71-validation-closure-v10-standard14-global-m24-n5-r1.json"
)

VALIDATION_CLOSURE = (
    "- VALIDATION_CLOSURE: `validation_set_ready := artifact変更完了 ∧ "
    "TaskSpec-required validationのidentity / command / individual pass condition / "
    "stop conditionが全件bind済み`。`validation_set_ready=true`の場合だけ、全required "
    "validationを個別invocationとして同一model stepから発行し、全resultを一度だけmodelへ返す。"
    "全件successかつ全result bind済みなら、TaskSpec追加要求またはresult失効がない限りread / "
    "validationを追加せずterminalを判断する。欠落 / non-success / unexpected stateはoperationを"
    "nonterminalにする。target探索 / 変更前 / review finding / 未固定methodまたはrecoveryへ適用しない。\n"
)


def labelled_lines(text: str) -> dict[str, str]:
    blocks = {}
    for line in text.splitlines():
        if not line.startswith("- "):
            continue
        label, body = line[2:].split(": ", 1)
        blocks[label] = body
    return blocks


class Candidate71Test(unittest.TestCase):
    def test_is_a_single_target_direct_child_of_candidate69(self) -> None:
        source = verify_bundle(C69)
        candidate = verify_bundle(C71)
        self.assertEqual(
            candidate["prompt_identity"],
            "the-caption-3ce91a4-validation-closure-r1",
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
            (C71 / "manifest.json").read_text(encoding="utf-8")
        )
        self.assertEqual(
            [entry for entry in candidate_manifest["files"] if entry["target"] != "AGENTS.md"],
            [entry for entry in source_manifest["files"] if entry["target"] != "AGENTS.md"],
        )

    def test_adds_only_validation_closure(self) -> None:
        source_text = (C69 / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        candidate_text = (C71 / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        expected = source_text.replace("- METHOD:", VALIDATION_CLOSURE + "- METHOD:")
        self.assertEqual(candidate_text, expected)

    def test_preserves_candidate69_labels_and_adds_one_invariant(self) -> None:
        source = labelled_lines((C69 / "files/AGENTS.md.txt").read_text(encoding="utf-8"))
        candidate = labelled_lines((C71 / "files/AGENTS.md.txt").read_text(encoding="utf-8"))
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
                "METHOD",
                "RECOVERY",
            ],
        )
        self.assertEqual({label: candidate[label] for label in source}, source)
        invariant = candidate["VALIDATION_CLOSURE"]
        self.assertIn("artifact変更完了", invariant)
        self.assertIn("individual pass condition / stop conditionが全件bind済み", invariant)
        self.assertIn("個別invocationとして同一model stepから発行", invariant)
        self.assertIn("全resultを一度だけmodelへ返す", invariant)
        self.assertIn("read / validationを追加せずterminalを判断", invariant)
        self.assertIn("欠落 / non-success / unexpected stateはoperationをnonterminal", invariant)
        self.assertIn("target探索 / 変更前 / review finding / 未固定methodまたはrecoveryへ適用しない", invariant)
        self.assertNotIn("MACHINE_BOUNDARY", candidate)
        for case_specific_term in ("F04", "F06", "F07", "A02"):
            self.assertNotIn(case_specific_term, invariant)

    def test_targeted_profiles_change_only_prompt_identity(self) -> None:
        manifest = verify_bundle(C71)
        source = json.loads(C69_PROFILE.read_text(encoding="utf-8"))
        candidate = json.loads(C71_PROFILE.read_text(encoding="utf-8"))
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

    def test_standard14_profiles_change_only_prompt_identity(self) -> None:
        manifest = verify_bundle(C71)
        source = json.loads(C69_STANDARD_PROFILE.read_text(encoding="utf-8"))
        candidate = json.loads(C71_STANDARD_PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(len(candidate["cases"]), 14)
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
