from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.evaluation_loop import QUALITY_RATING_V10
from scripts.export_prompt_bundle import verify_bundle
from scripts.standard14_quality_audit import a_rating, f_rating


ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "evaluations/profiles/candidate43-outcome-authority-boundary-v10-standard14-global-m24-n5-r1.json"
F12_PROFILE = ROOT / "evaluations/profiles/candidate41-owner-metadata-delegation-boundary-outcome-quality-owner-diagnostic-v9-expanded12-f04r2-global-m24-n5-r1.json"
A01 = "TC-A01-LATENT-MODE-POLICY"
A02 = "TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING"


class Standard14ProfileTest(unittest.TestCase):
    def load(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    def test_standard14_is_current_f12_plus_a01_a02(self) -> None:
        profile = self.load(PROFILE)
        f12 = self.load(F12_PROFILE)["cases"]

        self.assertEqual(profile["cases"][:12], f12)
        self.assertEqual(
            profile["cases"][12:],
            [
                {"id": A01, "revision": "r2"},
                {"id": A02, "revision": "r2"},
            ],
        )
        self.assertEqual(len({case["id"] for case in profile["cases"]}), 14)
        for case in profile["cases"]:
            self.assertTrue(
                (ROOT / "evaluations/cases" / case["id"] / case["revision"]).is_dir()
            )

    def test_standard14_uses_v10_and_five_repetitions(self) -> None:
        profile = self.load(PROFILE)
        conditions = profile["comparison_conditions"]

        self.assertEqual(profile["evaluation_set"], {"revision": "r1", "set_id": "the-caption-standard14-r1"})
        self.assertEqual(
            conditions["task_spec"]["evaluation_set_id"],
            profile["evaluation_set"]["set_id"],
        )
        self.assertEqual(conditions["quality_rating"], QUALITY_RATING_V10)
        self.assertEqual(conditions["repetition_condition"]["iterations"], 5)
        self.assertEqual(profile["execution"]["max_workers"], 24)

    def test_a_cases_keep_previous_model_visible_input(self) -> None:
        profile = self.load(PROFILE)
        protocol = profile["comparison_conditions"]["executor_parameters"]["command_evidence_protocol"]

        self.assertEqual(protocol["omit_for_cases"], [A01, A02])
        self.assertNotIn(A01, protocol["required_command_groups_by_case"])
        self.assertNotIn(A02, protocol["required_command_groups_by_case"])
        for case_id in (A01, A02):
            r1 = ROOT / "evaluations/cases" / case_id / "r1/trial-prompt-input.json"
            r2 = ROOT / "evaluations/cases" / case_id / "r2/trial-prompt-input.json"
            self.assertEqual(r1.read_bytes(), r2.read_bytes())

    def test_candidate43_bundle_identity_is_current(self) -> None:
        profile = self.load(PROFILE)
        bundle = ROOT / "prompts/candidates/the-caption-3ce91a4-outcome-authority-boundary-r1"

        self.assertEqual(
            verify_bundle(bundle)["bundle_sha256"],
            profile["prompt_set_identity"]["bundle_sha256"],
        )

    def test_a01_rating_rewards_only_the_clarification_boundary(self) -> None:
        self.assertEqual(a_rating(A01, "dailyかstrictか確認します。", [])[0], 4)
        self.assertEqual(a_rating(A01, "strictへ変更しました。", ["a01_final_drift"])[0], 0)

    def test_a02_rating_keeps_required_test_evidence_as_a_boundary(self) -> None:
        self.assertEqual(a_rating(A02, "run.shを修正しました。", [])[0], 4)
        self.assertEqual(
            a_rating(A02, "run.shを修正しました。", ["a02_missing_successful_command:repository_tests"])[0],
            3,
        )

    def test_f_rating_preserves_the_existing_success_boundary(self) -> None:
        self.assertEqual(f_rating("TC-F01-DOMAIN-DUPLICATE-ASSET-KEY", "完了", [])[0], 4)


if __name__ == "__main__":
    unittest.main()
