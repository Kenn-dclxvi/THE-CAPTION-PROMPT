from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C55 = ROOT / "prompts/candidates/the-caption-3ce91a4-prebound-operation-graph-r1"
C60 = ROOT / "prompts/candidates/the-caption-3ce91a4-operation-method-capsule-r1"
PROFILES = ROOT / "evaluations/profiles"
C55_PROFILE = PROFILES / (
    "candidate55-prebound-operation-graph-v10-operation-method-capsule-"
    "boundary-targeted2-global-m2-n1-catalog-fixed-r1.json"
)
C60_PROFILE = PROFILES / (
    "candidate60-operation-method-capsule-v10-operation-method-capsule-"
    "boundary-targeted2-global-m2-n1-catalog-fixed-r1.json"
)


class Candidate60Test(unittest.TestCase):
    def test_bundle_replaces_only_operation_boundary(self) -> None:
        source = verify_bundle(C55)
        candidate = verify_bundle(C60)
        self.assertEqual(
            candidate["content_relation"],
            {
                "changed_targets": ["AGENTS.md"],
                "kind": "direct_child_full_bundle",
                "source_prompt_identity": source["prompt_identity"],
            },
        )

        source_manifest = json.loads((C55 / "manifest.json").read_text(encoding="utf-8"))
        candidate_manifest = json.loads((C60 / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(len(candidate_manifest["files"]), 19)
        self.assertEqual(
            [entry for entry in candidate_manifest["files"] if entry["target"] != "AGENTS.md"],
            [entry for entry in source_manifest["files"] if entry["target"] != "AGENTS.md"],
        )

        source_lines = (C55 / "files/AGENTS.md").read_text(encoding="utf-8").splitlines()
        candidate_lines = (C60 / "files/AGENTS.md").read_text(encoding="utf-8").splitlines()
        removed = [line for line in source_lines if line not in candidate_lines]
        added = [line for line in candidate_lines if line not in source_lines]
        self.assertEqual(len(removed), 1)
        self.assertEqual(len(added), 1)
        self.assertTrue(removed[0].startswith("- OPERATION:"))
        self.assertTrue(added[0].startswith("- OPERATION:"))
        for required in (
            "method / result / constraint / failure / terminal",
            "TaskSpecが明示したterminal result",
            "tool grouping",
            "invocation状態",
            "raw output",
            "伝播させない",
        ):
            self.assertIn(required, added[0])

    def test_probe_profiles_change_only_prompt_identity(self) -> None:
        manifest = verify_bundle(C60)
        source = json.loads(C55_PROFILE.read_text(encoding="utf-8"))
        candidate = json.loads(C60_PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(candidate["prompt_set_identity"]["name"], manifest["prompt_identity"])
        self.assertEqual(candidate["prompt_set_identity"]["bundle_sha256"], manifest["bundle_sha256"])

        source_condition = copy.deepcopy(source)
        candidate_condition = copy.deepcopy(candidate)
        for profile in (source_condition, candidate_condition):
            profile.pop("profile_id")
            profile.pop("prompt_set_identity")
        self.assertEqual(candidate_condition, source_condition)

        self.assertEqual(candidate["cases"], [
            {
                "id": "TC-F10-MONTHLY-FORMAT-TEST-REVIEW",
                "revision": "r3-method-capsule-probe1",
            },
            {
                "id": "TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING",
                "revision": "r2-start-identity-method-capsule-probe1",
            },
        ])
        self.assertEqual(candidate["comparison_conditions"]["repetition_condition"]["iterations"], 1)
        self.assertEqual(candidate["execution"]["max_workers"], 2)
        self.assertEqual(
            candidate["comparison_conditions"]["agent_environment"]["model_visible_capability_catalog"]["expected_sha256"],
            "e755bd6f50049d0a3a96b01a450dea46a31cd1842fd434f4ecef421b059a077e",
        )

        f10 = json.loads((
            ROOT
            / "evaluations/cases/TC-F10-MONTHLY-FORMAT-TEST-REVIEW/"
            "r3-method-capsule-probe1/trial-prompt-input.json"
        ).read_text(encoding="utf-8"))
        a02 = json.loads((
            ROOT
            / "evaluations/cases/TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING/"
            "r2-start-identity-method-capsule-probe1/trial-prompt-input.json"
        ).read_text(encoding="utf-8"))
        self.assertEqual(f10["operation_method_capsule"]["operation_id"], "fixed-seed-diff-review")
        self.assertEqual(a02["operation_method_capsule"]["operation_id"], "start-identity")
        self.assertIn("canonical-target-resolutionのmethodは未指定", a02["operation_method_capsule"]["expires"])


if __name__ == "__main__":
    unittest.main()
