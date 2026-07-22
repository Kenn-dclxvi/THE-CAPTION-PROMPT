from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C57 = ROOT / "prompts/candidates/the-caption-3ce91a4-task-enumerated-read-boundary-r1"
C58 = ROOT / "prompts/candidates/the-caption-3ce91a4-purpose-bound-read-route-r1"
PROFILES = ROOT / "evaluations/profiles"


class Candidate58Test(unittest.TestCase):
    def test_bundle_replaces_only_read_route(self) -> None:
        source = verify_bundle(C57)
        candidate = verify_bundle(C58)
        self.assertEqual(
            candidate["content_relation"],
            {
                "changed_targets": ["AGENTS.md"],
                "kind": "direct_child_full_bundle",
                "source_prompt_identity": source["prompt_identity"],
            },
        )
        source_lines = (C57 / "files/AGENTS.md").read_text(encoding="utf-8").splitlines()
        candidate_lines = (C58 / "files/AGENTS.md").read_text(encoding="utf-8").splitlines()
        removed = [line for line in source_lines if line not in candidate_lines]
        added = [line for line in candidate_lines if line not in source_lines]
        self.assertEqual(len(removed), 1)
        self.assertTrue(removed[0].startswith("- FIXED_READ:"))
        self.assertEqual(len(added), 1)
        self.assertTrue(added[0].startswith("- READ_ROUTE:"))
        for required in (
            "read pathまたはcommandを有限列挙",
            "各result後に次のreadを一つ決め",
            "複数readを同一model stepへ置かない",
        ):
            self.assertIn(required, added[0])

    def test_profiles_change_only_prompt_identity(self) -> None:
        manifest = verify_bundle(C58)
        names = (
            "ambiguity-targeted2-v10-global-m10-n5-catalog-fixed-r1",
            "outcome-quality-owner-diagnostic-v9-targeted2-global-m10-n5-catalog-fixed-r1",
        )
        for suffix in names:
            source = json.loads((PROFILES / f"candidate57-task-enumerated-read-boundary-{suffix}.json").read_text())
            candidate = json.loads((PROFILES / f"candidate58-purpose-bound-read-route-{suffix}.json").read_text())
            self.assertEqual(candidate["prompt_set_identity"]["name"], manifest["prompt_identity"])
            self.assertEqual(candidate["prompt_set_identity"]["bundle_sha256"], manifest["bundle_sha256"])
            for profile in (source, candidate):
                profile.pop("profile_id")
                profile.pop("prompt_set_identity")
            self.assertEqual(candidate, source)


if __name__ == "__main__":
    unittest.main()
