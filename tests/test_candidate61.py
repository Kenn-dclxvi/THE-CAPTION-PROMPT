from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C43 = ROOT / "prompts/candidates/the-caption-3ce91a4-outcome-authority-boundary-r1"
C55 = ROOT / "prompts/candidates/the-caption-3ce91a4-prebound-operation-graph-r1"
C61 = ROOT / "prompts/candidates/the-caption-3ce91a4-atomic-spec-operation-gate-r1"
PROFILES = ROOT / "evaluations/profiles"
C55_PROFILE = PROFILES / (
    "candidate55-prebound-operation-graph-outcome-quality-owner-diagnostic-v9-"
    "targeted2-global-m10-n5-catalog-fixed-r1.json"
)
C61_PROFILE = PROFILES / (
    "candidate61-atomic-spec-operation-gate-outcome-quality-owner-diagnostic-v9-"
    "targeted2-global-m10-n5-catalog-fixed-r1.json"
)
C43_A_PROFILE = PROFILES / (
    "candidate43-outcome-authority-boundary-ambiguity-targeted2-v10-global-m10-n5-"
    "catalog-fixed-r1.json"
)
C61_A_PROFILE = PROFILES / (
    "candidate61-atomic-spec-operation-gate-ambiguity-targeted2-v10-global-m10-n5-"
    "catalog-fixed-r1.json"
)


class Candidate61Test(unittest.TestCase):
    def test_restores_exact_candidate43_spec_as_one_change(self) -> None:
        source = verify_bundle(C55)
        candidate = verify_bundle(C61)
        self.assertEqual(
            candidate["content_relation"],
            {
                "changed_targets": ["AGENTS.md"],
                "kind": "direct_child_full_bundle",
                "source_prompt_identity": source["prompt_identity"],
            },
        )

        source_manifest = json.loads((C55 / "manifest.json").read_text(encoding="utf-8"))
        candidate_manifest = json.loads((C61 / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(
            [entry for entry in candidate_manifest["files"] if entry["target"] != "AGENTS.md"],
            [entry for entry in source_manifest["files"] if entry["target"] != "AGENTS.md"],
        )

        c43_spec = next(
            line
            for line in (C43 / "files/AGENTS.md.txt").read_text(encoding="utf-8").splitlines()
            if line.startswith("- SPEC:")
        )
        source_lines = (C55 / "files/AGENTS.md.txt").read_text(encoding="utf-8").splitlines()
        candidate_lines = (C61 / "files/AGENTS.md.txt").read_text(encoding="utf-8").splitlines()
        removed = [line for line in source_lines if line not in candidate_lines]
        added = [line for line in candidate_lines if line not in source_lines]
        self.assertEqual([line.split(":", 1)[0] for line in removed], ["- READINESS", "- OPERATION"])
        self.assertEqual(added, [c43_spec])
        self.assertNotIn("FIXED_READ", "\n".join(candidate_lines))
        self.assertNotIn("operation_method_capsule", "\n".join(candidate_lines))
        self.assertLess((C61 / "files/AGENTS.md.txt").stat().st_size, (C43 / "files/AGENTS.md.txt").stat().st_size)

    def test_profile_changes_only_prompt_identity(self) -> None:
        manifest = verify_bundle(C61)
        source = json.loads(C55_PROFILE.read_text(encoding="utf-8"))
        candidate = json.loads(C61_PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(candidate["prompt_set_identity"]["name"], manifest["prompt_identity"])
        self.assertEqual(candidate["prompt_set_identity"]["bundle_sha256"], manifest["bundle_sha256"])

        source_condition = copy.deepcopy(source)
        candidate_condition = copy.deepcopy(candidate)
        for profile in (source_condition, candidate_condition):
            profile.pop("profile_id")
            profile.pop("prompt_set_identity")
        self.assertEqual(candidate_condition, source_condition)

    def test_ambiguity_profile_changes_only_prompt_identity(self) -> None:
        manifest = verify_bundle(C61)
        source = json.loads(C43_A_PROFILE.read_text(encoding="utf-8"))
        candidate = json.loads(C61_A_PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(candidate["prompt_set_identity"]["name"], manifest["prompt_identity"])
        self.assertEqual(
            candidate["prompt_set_identity"]["bundle_sha256"], manifest["bundle_sha256"]
        )

        source_condition = copy.deepcopy(source)
        candidate_condition = copy.deepcopy(candidate)
        for profile in (source_condition, candidate_condition):
            profile.pop("profile_id")
            profile.pop("prompt_set_identity")
        self.assertEqual(candidate_condition, source_condition)


if __name__ == "__main__":
    unittest.main()
