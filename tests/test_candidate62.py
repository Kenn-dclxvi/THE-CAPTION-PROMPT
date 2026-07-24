from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C43 = ROOT / "prompts/candidates/the-caption-3ce91a4-outcome-authority-boundary-r1"
C62 = ROOT / "prompts/candidates/the-caption-3ce91a4-task-closed-read-route-r1"
PROFILES = ROOT / "evaluations/profiles"
C43_F_PROFILE = PROFILES / (
    "candidate43-outcome-authority-boundary-outcome-quality-owner-diagnostic-v9-"
    "targeted2-global-m10-n5-catalog-fixed-r1.json"
)
C62_F_PROFILE = PROFILES / (
    "candidate62-task-closed-read-route-outcome-quality-owner-diagnostic-v9-"
    "targeted2-global-m10-n5-catalog-fixed-r1.json"
)
C43_A_PROFILE = PROFILES / (
    "candidate43-outcome-authority-boundary-ambiguity-targeted2-v10-global-m10-n5-"
    "catalog-fixed-r1.json"
)
C62_A02_PROFILE = PROFILES / (
    "candidate62-task-closed-read-route-ambiguity-a02-v10-global-m1-n1-catalog-fixed-r1.json"
)
C62_A_PROFILE = PROFILES / (
    "candidate62-task-closed-read-route-ambiguity-targeted2-v10-global-m10-n5-"
    "catalog-fixed-r1.json"
)


class Candidate62Test(unittest.TestCase):
    def test_adds_only_task_closed_read_to_candidate43(self) -> None:
        source = verify_bundle(C43)
        candidate = verify_bundle(C62)
        self.assertEqual(
            candidate["content_relation"],
            {
                "changed_targets": ["AGENTS.md"],
                "kind": "direct_child_full_bundle",
                "source_prompt_identity": source["prompt_identity"],
            },
        )

        source_manifest = json.loads((C43 / "manifest.json").read_text(encoding="utf-8"))
        candidate_manifest = json.loads((C62 / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(
            [entry for entry in candidate_manifest["files"] if entry["target"] != "AGENTS.md"],
            [entry for entry in source_manifest["files"] if entry["target"] != "AGENTS.md"],
        )

        source_lines = (C43 / "files/AGENTS.md.txt").read_text(encoding="utf-8").splitlines()
        candidate_lines = (C62 / "files/AGENTS.md.txt").read_text(encoding="utf-8").splitlines()
        added = [line for line in candidate_lines if line not in source_lines]
        self.assertEqual(len(added), 1)
        self.assertTrue(added[0].startswith("- TASK_CLOSED_READ:"))
        self.assertIn("required outcome全体がread-only", added[0])
        self.assertIn("taskの一部operationへの適用", added[0])
        self.assertIn("write / test / dependency操作を伴うtask", added[0])
        self.assertNotIn("FIXED_READ", "\n".join(candidate_lines))
        self.assertEqual(
            [line for line in candidate_lines if line != added[0]],
            source_lines,
        )

    def test_f_profile_changes_only_prompt_identity(self) -> None:
        manifest = verify_bundle(C62)
        source = json.loads(C43_F_PROFILE.read_text(encoding="utf-8"))
        candidate = json.loads(C62_F_PROFILE.read_text(encoding="utf-8"))
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

    def test_a02_probe_is_c43_a_profile_reduced_to_one_slot(self) -> None:
        manifest = verify_bundle(C62)
        source = json.loads(C43_A_PROFILE.read_text(encoding="utf-8"))
        candidate = json.loads(C62_A02_PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(candidate["prompt_set_identity"]["name"], manifest["prompt_identity"])
        self.assertEqual(
            candidate["prompt_set_identity"]["bundle_sha256"], manifest["bundle_sha256"]
        )

        source["cases"] = [
            item
            for item in source["cases"]
            if item["id"] == "TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING"
        ]
        source["comparison_conditions"]["executor_parameters"]["max_workers"] = 1
        source["comparison_conditions"]["repetition_condition"]["iterations"] = 1
        source["execution"]["duration_hints_seconds"] = {
            "TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING": 750.0
        }
        source["execution"]["max_workers"] = 1
        for profile in (source, candidate):
            profile.pop("profile_id")
            profile.pop("prompt_set_identity")
        self.assertEqual(candidate, source)

    def test_a_profile_changes_only_prompt_identity(self) -> None:
        manifest = verify_bundle(C62)
        source = json.loads(C43_A_PROFILE.read_text(encoding="utf-8"))
        candidate = json.loads(C62_A_PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(candidate["prompt_set_identity"]["name"], manifest["prompt_identity"])
        self.assertEqual(
            candidate["prompt_set_identity"]["bundle_sha256"], manifest["bundle_sha256"]
        )

        for profile in (source, candidate):
            profile.pop("profile_id")
            profile.pop("prompt_set_identity")
        self.assertEqual(candidate, source)


if __name__ == "__main__":
    unittest.main()
