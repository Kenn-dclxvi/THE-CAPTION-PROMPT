from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROFILES = ROOT / "evaluations/profiles"
C43_ORIGINAL = PROFILES / "candidate43-outcome-authority-boundary-outcome-quality-owner-diagnostic-v9-targeted2-global-m10-n5-r1.json"
C43_FIXED = PROFILES / "candidate43-outcome-authority-boundary-outcome-quality-owner-diagnostic-v9-targeted2-global-m10-n5-catalog-fixed-r1.json"
C51_FIXED = PROFILES / "candidate51-root-operation-completion-boundary-outcome-quality-owner-diagnostic-v9-targeted2-global-m10-n5-catalog-fixed-r1.json"


class CatalogFixedProfileTest(unittest.TestCase):
    def load(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    def test_c43_and_c51_change_only_prompt_identity(self) -> None:
        c43 = self.load(C43_FIXED)
        c51 = self.load(C51_FIXED)
        for profile in (c43, c51):
            profile.pop("profile_id")
            profile.pop("prompt_set_identity")
        self.assertEqual(c51, c43)

    def test_fixed_profile_adds_only_catalog_condition(self) -> None:
        original = self.load(C43_ORIGINAL)
        fixed = self.load(C43_FIXED)
        original.pop("profile_id")
        fixed.pop("profile_id")
        policy = fixed["comparison_conditions"]["agent_environment"].pop(
            "model_visible_capability_catalog"
        )
        self.assertEqual(fixed, original)
        self.assertEqual(
            policy,
            {
                "apps_enabled": False,
                "expected_sha256": "e755bd6f50049d0a3a96b01a450dea46a31cd1842fd434f4ecef421b059a077e",
                "plugin_sharing_enabled": False,
                "plugins_enabled": False,
                "schema_version": "the-caption-prompt.model-visible-capability-catalog/v1",
            },
        )


if __name__ == "__main__":
    unittest.main()
