from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C56 = ROOT / "prompts/candidates/the-caption-3ce91a4-resolved-fixed-read-boundary-r1"
C59 = ROOT / "prompts/candidates/the-caption-3ce91a4-read-only-operation-batch-r1"
PROFILES = ROOT / "evaluations/profiles"


class Candidate59Test(unittest.TestCase):
    def test_bundle_replaces_only_fixed_read(self) -> None:
        source = verify_bundle(C56)
        candidate = verify_bundle(C59)
        self.assertEqual(
            candidate["content_relation"],
            {
                "changed_targets": ["AGENTS.md"],
                "kind": "direct_child_full_bundle",
                "source_prompt_identity": source["prompt_identity"],
            },
        )
        source_lines = (C56 / "files/AGENTS.md.txt").read_text(encoding="utf-8").splitlines()
        candidate_lines = (C59 / "files/AGENTS.md.txt").read_text(encoding="utf-8").splitlines()
        removed = [line for line in source_lines if line not in candidate_lines]
        added = [line for line in candidate_lines if line not in source_lines]
        self.assertEqual(len(removed), 1)
        self.assertEqual(len(added), 1)
        self.assertTrue(removed[0].startswith("- FIXED_READ:"))
        self.assertTrue(added[0].startswith("- FIXED_READ:"))
        for required in (
            "operation全体",
            "edit=false",
            "test=false",
            "dependency=false",
            "read-only validationを有限列挙",
            "一条件でも未明示なら非適用",
        ):
            self.assertIn(required, added[0])

    def test_profiles_change_only_prompt_identity(self) -> None:
        manifest = verify_bundle(C59)
        names = (
            "ambiguity-targeted2-v10-global-m10-n5-catalog-fixed-r1",
            "outcome-quality-owner-diagnostic-v9-targeted2-global-m10-n5-catalog-fixed-r1",
        )
        for suffix in names:
            source = json.loads((PROFILES / f"candidate56-resolved-fixed-read-boundary-{suffix}.json").read_text())
            candidate = json.loads((PROFILES / f"candidate59-read-only-operation-batch-{suffix}.json").read_text())
            self.assertEqual(candidate["prompt_set_identity"]["name"], manifest["prompt_identity"])
            self.assertEqual(candidate["prompt_set_identity"]["bundle_sha256"], manifest["bundle_sha256"])
            for profile in (source, candidate):
                profile.pop("profile_id")
                profile.pop("prompt_set_identity")
            self.assertEqual(candidate, source)


if __name__ == "__main__":
    unittest.main()
