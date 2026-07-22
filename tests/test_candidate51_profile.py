from __future__ import annotations

import json
import unittest
from copy import deepcopy
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C49_PROFILE = ROOT / "evaluations/profiles/candidate49-explicit-delegation-control-boundary-outcome-quality-owner-diagnostic-v9-targeted2-global-m10-n5-r1.json"
C51_PROFILE = ROOT / "evaluations/profiles/candidate51-root-operation-completion-boundary-outcome-quality-owner-diagnostic-v9-targeted2-global-m10-n5-r1.json"
C51_BUNDLE = ROOT / "prompts/candidates/the-caption-3ce91a4-root-operation-completion-boundary-r1"


class Candidate51ProfileTest(unittest.TestCase):
    def load(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    def test_profile_changes_only_prompt_identity(self) -> None:
        source = self.load(C49_PROFILE)
        candidate = self.load(C51_PROFILE)
        source_comparable = deepcopy(source)
        candidate_comparable = deepcopy(candidate)
        source_comparable.pop("profile_id")
        candidate_comparable.pop("profile_id")
        source_comparable.pop("prompt_set_identity")
        candidate_comparable.pop("prompt_set_identity")
        self.assertEqual(candidate_comparable, source_comparable)

    def test_profile_binds_candidate51_bundle(self) -> None:
        profile = self.load(C51_PROFILE)
        manifest = verify_bundle(C51_BUNDLE)

        self.assertEqual(profile["prompt_set_identity"]["name"], manifest["prompt_identity"])
        self.assertEqual(
            profile["prompt_set_identity"]["bundle_sha256"],
            manifest["bundle_sha256"],
        )
        self.assertEqual(
            profile["cases"],
            [
                {"id": "TC-F05-CLARIFY-UNITS-MODE", "revision": "r1"},
                {"id": "TC-F10-MONTHLY-FORMAT-TEST-REVIEW", "revision": "r3"},
            ],
        )
        self.assertEqual(profile["comparison_conditions"]["repetition_condition"]["iterations"], 5)


if __name__ == "__main__":
    unittest.main()
