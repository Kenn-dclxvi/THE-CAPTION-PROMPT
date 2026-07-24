from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C43 = ROOT / "prompts/candidates/the-caption-3ce91a4-outcome-authority-boundary-r1"
C69 = (
    ROOT
    / "prompts/candidates/the-caption-3ce91a4-model-reentry-decision-boundary-r1"
)
SOURCE_PROFILE = (
    ROOT
    / "evaluations/profiles/candidate43-outcome-authority-boundary-v10-standard14-global-m24-n5-r1.json"
)
CANDIDATE_PROFILE = (
    ROOT
    / "evaluations/profiles/candidate69-model-reentry-decision-boundary-v10-standard14-global-m24-n5-r1.json"
)

DECISION_BOUNDARY = (
    "- DECISION_BOUNDARY: `decision_boundary := 受領resultが未発行invocationの"
    "target / permission / method / stop conditionを変え得る`。"
    "decision boundaryを持たない既知の相互非依存invocationは分割せず"
    "同一model stepで発行し、全result受領後に一度だけ次を判断する。\n"
)


def labelled_lines(text: str) -> dict[str, str]:
    blocks = {}
    for line in text.splitlines():
        if not line.startswith("- "):
            continue
        label, body = line[2:].split(": ", 1)
        blocks[label] = body
    return blocks


class Candidate69Test(unittest.TestCase):
    def test_is_a_single_target_direct_child_of_candidate43(self) -> None:
        source = verify_bundle(C43)
        candidate = verify_bundle(C69)
        self.assertEqual(
            candidate["prompt_identity"],
            "the-caption-3ce91a4-model-reentry-decision-boundary-r1",
        )
        self.assertEqual(
            candidate["content_relation"],
            {
                "changed_targets": ["AGENTS.md"],
                "kind": "direct_child_full_bundle",
                "source_prompt_identity": source["prompt_identity"],
            },
        )

        source_manifest = json.loads((C43 / "manifest.json").read_text(encoding="utf-8"))
        candidate_manifest = json.loads(
            (C69 / "manifest.json").read_text(encoding="utf-8")
        )
        self.assertEqual(
            [entry for entry in candidate_manifest["files"] if entry["target"] != "AGENTS.md"],
            [entry for entry in source_manifest["files"] if entry["target"] != "AGENTS.md"],
        )

    def test_adds_only_decision_boundary(self) -> None:
        source_text = (C43 / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        candidate_text = (C69 / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        anchor = "- METHOD:"
        expected = source_text.replace(anchor, DECISION_BOUNDARY + anchor)
        self.assertEqual(candidate_text, expected)

    def test_preserves_candidate43_labels_and_adds_one_invariant(self) -> None:
        source = labelled_lines((C43 / "files/AGENTS.md.txt").read_text(encoding="utf-8"))
        candidate = labelled_lines((C69 / "files/AGENTS.md.txt").read_text(encoding="utf-8"))
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
                "METHOD",
                "RECOVERY",
            ],
        )
        self.assertEqual(
            {label: candidate[label] for label in source},
            source,
        )
        self.assertIn("未発行invocationのtarget / permission / method / stop condition", candidate["DECISION_BOUNDARY"])
        self.assertNotIn("read-only", candidate["DECISION_BOUNDARY"])
        self.assertNotIn("F10", candidate["DECISION_BOUNDARY"])
        self.assertNotIn("A02", candidate["DECISION_BOUNDARY"])

    def test_standard14_profile_changes_only_prompt_identity(self) -> None:
        manifest = verify_bundle(C69)
        source = json.loads(SOURCE_PROFILE.read_text(encoding="utf-8"))
        candidate = json.loads(CANDIDATE_PROFILE.read_text(encoding="utf-8"))
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
