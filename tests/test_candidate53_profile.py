from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C43_PROFILE = ROOT / "evaluations/profiles/candidate43-outcome-authority-boundary-outcome-quality-owner-diagnostic-v9-targeted2-global-m10-n5-catalog-fixed-r1.json"
C53_PROFILE = ROOT / "evaluations/profiles/candidate53-purpose-separated-operation-graph-outcome-quality-owner-diagnostic-v9-targeted2-global-m10-n5-catalog-fixed-r1.json"
C53_BUNDLE = ROOT / "prompts/candidates/the-caption-3ce91a4-purpose-separated-operation-graph-r1"


class Candidate53ProfileTest(unittest.TestCase):
    def load(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    def test_profile_changes_only_prompt_identity(self) -> None:
        source = self.load(C43_PROFILE)
        candidate = self.load(C53_PROFILE)
        for profile in (source, candidate):
            profile.pop("profile_id")
            profile.pop("prompt_set_identity")
        self.assertEqual(candidate, source)

    def test_profile_binds_bundle_and_catalog_gate(self) -> None:
        profile = self.load(C53_PROFILE)
        manifest = verify_bundle(C53_BUNDLE)

        self.assertEqual(profile["prompt_set_identity"]["name"], manifest["prompt_identity"])
        self.assertEqual(
            profile["prompt_set_identity"]["bundle_sha256"], manifest["bundle_sha256"]
        )
        policy = profile["comparison_conditions"]["agent_environment"]["model_visible_capability_catalog"]
        self.assertEqual(
            policy["expected_sha256"],
            "e755bd6f50049d0a3a96b01a450dea46a31cd1842fd434f4ecef421b059a077e",
        )
        self.assertFalse(policy["apps_enabled"])
        self.assertFalse(policy["plugins_enabled"])
        self.assertFalse(policy["plugin_sharing_enabled"])


if __name__ == "__main__":
    unittest.main()
