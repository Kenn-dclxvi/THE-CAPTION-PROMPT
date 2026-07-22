from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
PROFILES = ROOT / "evaluations/profiles"
BUNDLE = ROOT / "prompts/candidates/the-caption-3ce91a4-task-enumerated-read-boundary-r1"
PAIRS = (
    (
        PROFILES / "candidate56-resolved-fixed-read-boundary-ambiguity-targeted2-v10-global-m10-n5-catalog-fixed-r1.json",
        PROFILES / "candidate57-task-enumerated-read-boundary-ambiguity-targeted2-v10-global-m10-n5-catalog-fixed-r1.json",
    ),
    (
        PROFILES / "candidate56-resolved-fixed-read-boundary-outcome-quality-owner-diagnostic-v9-targeted2-global-m10-n5-catalog-fixed-r1.json",
        PROFILES / "candidate57-task-enumerated-read-boundary-outcome-quality-owner-diagnostic-v9-targeted2-global-m10-n5-catalog-fixed-r1.json",
    ),
)


class Candidate57ProfileTest(unittest.TestCase):
    def load(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    def test_profiles_change_only_prompt_identity(self) -> None:
        manifest = verify_bundle(BUNDLE)
        for source_path, candidate_path in PAIRS:
            source = self.load(source_path)
            candidate = self.load(candidate_path)
            self.assertEqual(candidate["prompt_set_identity"]["name"], manifest["prompt_identity"])
            self.assertEqual(candidate["prompt_set_identity"]["bundle_sha256"], manifest["bundle_sha256"])
            for profile in (source, candidate):
                profile.pop("profile_id")
                profile.pop("prompt_set_identity")
            self.assertEqual(candidate, source)


if __name__ == "__main__":
    unittest.main()
