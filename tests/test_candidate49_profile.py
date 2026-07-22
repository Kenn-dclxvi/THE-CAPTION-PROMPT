from __future__ import annotations

import json
import unittest
from copy import deepcopy
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C43_PROFILE = ROOT / "evaluations/profiles/candidate43-outcome-authority-boundary-ambiguity-targeted2-v10-global-m10-n5-r1.json"
C49_PROFILE = ROOT / "evaluations/profiles/candidate49-explicit-delegation-control-boundary-ambiguity-targeted2-v10-global-m10-n5-r1.json"
C43_OUTCOME_PROFILE = ROOT / "evaluations/profiles/candidate43-outcome-authority-boundary-outcome-quality-owner-diagnostic-v9-targeted2-global-m10-n5-r1.json"
C49_OUTCOME_PROFILE = ROOT / "evaluations/profiles/candidate49-explicit-delegation-control-boundary-outcome-quality-owner-diagnostic-v9-targeted2-global-m10-n5-r1.json"
C49_BUNDLE = ROOT / "prompts/candidates/the-caption-3ce91a4-explicit-delegation-control-boundary-r1"


class Candidate49ProfileTest(unittest.TestCase):
    def load(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    def test_targeted_profile_changes_only_prompt_identity(self) -> None:
        source = self.load(C43_PROFILE)
        candidate = self.load(C49_PROFILE)

        source_comparable = deepcopy(source)
        candidate_comparable = deepcopy(candidate)
        source_comparable.pop("profile_id")
        candidate_comparable.pop("profile_id")
        source_comparable.pop("prompt_set_identity")
        candidate_comparable.pop("prompt_set_identity")
        self.assertEqual(candidate_comparable, source_comparable)

    def test_targeted_profile_binds_candidate49_bundle(self) -> None:
        profile = self.load(C49_PROFILE)
        manifest = verify_bundle(C49_BUNDLE)

        self.assertEqual(profile["prompt_set_identity"]["name"], manifest["prompt_identity"])
        self.assertEqual(
            profile["prompt_set_identity"]["bundle_sha256"],
            manifest["bundle_sha256"],
        )
        self.assertEqual(profile["comparison_conditions"]["repetition_condition"]["iterations"], 5)
        self.assertEqual(
            profile["cases"],
            [
                {"id": "TC-A01-LATENT-MODE-POLICY", "revision": "r2"},
                {"id": "TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING", "revision": "r2"},
            ],
        )

    def test_outcome_profile_changes_only_prompt_identity(self) -> None:
        source = self.load(C43_OUTCOME_PROFILE)
        candidate = self.load(C49_OUTCOME_PROFILE)

        source_comparable = deepcopy(source)
        candidate_comparable = deepcopy(candidate)
        source_comparable.pop("profile_id")
        candidate_comparable.pop("profile_id")
        source_comparable.pop("prompt_set_identity")
        candidate_comparable.pop("prompt_set_identity")
        self.assertEqual(candidate_comparable, source_comparable)

    def test_outcome_profile_binds_candidate49_bundle(self) -> None:
        profile = self.load(C49_OUTCOME_PROFILE)
        manifest = verify_bundle(C49_BUNDLE)

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


if __name__ == "__main__":
    unittest.main()
