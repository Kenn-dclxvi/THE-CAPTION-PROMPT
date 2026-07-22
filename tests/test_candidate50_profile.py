from __future__ import annotations

import json
import unittest
from copy import deepcopy
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C43_AMBIGUITY = ROOT / "evaluations/profiles/candidate43-outcome-authority-boundary-ambiguity-targeted2-v10-global-m10-n5-r1.json"
C50_AMBIGUITY = ROOT / "evaluations/profiles/candidate50-root-read-batch-ambiguity-targeted2-v10-global-m10-n5-r1.json"
C43_OUTCOME = ROOT / "evaluations/profiles/candidate43-outcome-authority-boundary-outcome-quality-owner-diagnostic-v9-targeted2-global-m10-n5-r1.json"
C50_OUTCOME = ROOT / "evaluations/profiles/candidate50-root-read-batch-outcome-quality-owner-diagnostic-v9-targeted2-global-m10-n5-r1.json"
C50_BUNDLE = ROOT / "prompts/candidates/the-caption-3ce91a4-root-read-batch-r1"


class Candidate50ProfileTest(unittest.TestCase):
    def load(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    def assert_changes_only_prompt_identity(self, source_path: Path, candidate_path: Path) -> None:
        source = self.load(source_path)
        candidate = self.load(candidate_path)
        source_comparable = deepcopy(source)
        candidate_comparable = deepcopy(candidate)
        source_comparable.pop("profile_id")
        candidate_comparable.pop("profile_id")
        source_comparable.pop("prompt_set_identity")
        candidate_comparable.pop("prompt_set_identity")
        self.assertEqual(candidate_comparable, source_comparable)

    def assert_binds_candidate50(self, profile_path: Path) -> None:
        profile = self.load(profile_path)
        manifest = verify_bundle(C50_BUNDLE)
        self.assertEqual(profile["prompt_set_identity"]["name"], manifest["prompt_identity"])
        self.assertEqual(
            profile["prompt_set_identity"]["bundle_sha256"],
            manifest["bundle_sha256"],
        )
        self.assertEqual(
            profile["comparison_conditions"]["repetition_condition"]["iterations"],
            5,
        )

    def test_ambiguity_profile_changes_only_prompt_identity(self) -> None:
        self.assert_changes_only_prompt_identity(C43_AMBIGUITY, C50_AMBIGUITY)
        self.assert_binds_candidate50(C50_AMBIGUITY)

    def test_outcome_profile_changes_only_prompt_identity(self) -> None:
        self.assert_changes_only_prompt_identity(C43_OUTCOME, C50_OUTCOME)
        self.assert_binds_candidate50(C50_OUTCOME)


if __name__ == "__main__":
    unittest.main()
