from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle
from scripts.materialize_prompt_route import (
    RouteMaterializationError,
    load_route_delta,
    materialize_route,
    route_matches,
    select_prompt_identity,
)


ROOT = Path(__file__).resolve().parents[1]
C43 = ROOT / "prompts/candidates/the-caption-3ce91a4-outcome-authority-boundary-r1"
C63 = ROOT / "prompts/candidates/the-caption-3ce91a4-fixed-evidence-route-projection-r1"
DELTA_PATH = ROOT / "prompts/routes/fixed-evidence-review-r1.json"
C63_IDENTITY = "the-caption-3ce91a4-fixed-evidence-route-projection-r1"
PROFILES = ROOT / "evaluations/profiles"
C43_PROFILE = PROFILES / (
    "candidate43-outcome-authority-boundary-fixed-evidence-review-f10-v9-"
    "global-m10-n5-catalog-fixed-r1.json"
)
C63_PROFILE = PROFILES / (
    "candidate63-fixed-evidence-route-projection-fixed-evidence-review-f10-v9-"
    "global-m10-n5-catalog-fixed-r1.json"
)


FIXED_EVIDENCE_FACTS = {
    "dependency_allowed": False,
    "edit_allowed": False,
    "evidence_set": "finite_enumerated",
    "scope_expansion_allowed": False,
    "target_identity": "fixed",
    "task_outcome": "terminal_evidence_review",
    "test_allowed": False,
}


class Candidate63Test(unittest.TestCase):
    def test_route_accepts_only_fixed_evidence_review_shape(self) -> None:
        delta = load_route_delta(DELTA_PATH)
        self.assertTrue(route_matches(delta, FIXED_EVIDENCE_FACTS))

        f05 = {**FIXED_EVIDENCE_FACTS, "task_outcome": "clarification"}
        a02 = {**FIXED_EVIDENCE_FACTS, "edit_allowed": True, "test_allowed": True}
        a06 = {
            **FIXED_EVIDENCE_FACTS,
            "evidence_set": "open_discovery",
            "test_allowed": True,
        }
        self.assertFalse(route_matches(delta, f05))
        self.assertFalse(route_matches(delta, a02))
        self.assertFalse(route_matches(delta, a06))
        self.assertEqual(
            select_prompt_identity(delta, FIXED_EVIDENCE_FACTS, C63_IDENTITY),
            C63_IDENTITY,
        )
        for non_matching_facts in (f05, a02, a06):
            self.assertEqual(
                select_prompt_identity(delta, non_matching_facts, C63_IDENTITY),
                "the-caption-3ce91a4-outcome-authority-boundary-r1",
            )

    def test_materialized_bundle_is_base_plus_one_route_line(self) -> None:
        base = verify_bundle(C43)
        candidate = verify_bundle(C63)
        self.assertEqual(
            candidate["content_relation"],
            {
                "changed_targets": ["AGENTS.md"],
                "kind": "materialized_route_projection",
                "route_identity": "fixed-evidence-review-r1",
                "source_prompt_identity": base["prompt_identity"],
            },
        )
        self.assertEqual(
            candidate["route_projection"]["base_bundle_sha256"],
            base["bundle_sha256"],
        )

        base_manifest = json.loads((C43 / "manifest.json").read_text(encoding="utf-8"))
        candidate_manifest = json.loads(
            (C63 / "manifest.json").read_text(encoding="utf-8")
        )
        self.assertEqual(
            [entry for entry in candidate_manifest["files"] if entry["target"] != "AGENTS.md"],
            [entry for entry in base_manifest["files"] if entry["target"] != "AGENTS.md"],
        )

        base_lines = (C43 / "files/AGENTS.md").read_text(encoding="utf-8").splitlines()
        candidate_lines = (C63 / "files/AGENTS.md").read_text(encoding="utf-8").splitlines()
        added = [line for line in candidate_lines if line not in base_lines]
        self.assertEqual(len(added), 1)
        self.assertTrue(added[0].startswith("- FIXED_EVIDENCE_READ:"))
        self.assertEqual(
            [line for line in candidate_lines if line != added[0]],
            base_lines,
        )
        spec_index = next(
            index for index, line in enumerate(candidate_lines) if line.startswith("- SPEC:")
        )
        self.assertEqual(candidate_lines[spec_index + 1], added[0])

    def test_repository_candidate_is_reproducible_from_base_and_delta(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "candidate63"
            generated = materialize_route(
                C43,
                DELTA_PATH,
                output,
                C63_IDENTITY,
                FIXED_EVIDENCE_FACTS,
            )
            repository = verify_bundle(C63)
            self.assertEqual(generated["bundle_sha256"], repository["bundle_sha256"])
            self.assertEqual(
                (output / "files/AGENTS.md").read_bytes(),
                (C63 / "files/AGENTS.md").read_bytes(),
            )

    def test_non_matching_route_is_not_materialized(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "candidate63"
            with self.assertRaisesRegex(
                RouteMaterializationError,
                "route facts do not satisfy",
            ):
                materialize_route(
                    C43,
                    DELTA_PATH,
                    output,
                    C63_IDENTITY,
                    {**FIXED_EVIDENCE_FACTS, "edit_allowed": True},
                )
            self.assertFalse(output.exists())

    def test_f10_profiles_change_only_prompt_identity(self) -> None:
        candidate_manifest = verify_bundle(C63)
        base = json.loads(C43_PROFILE.read_text(encoding="utf-8"))
        candidate = json.loads(C63_PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(candidate["prompt_set_identity"]["name"], C63_IDENTITY)
        self.assertEqual(
            candidate["prompt_set_identity"]["bundle_sha256"],
            candidate_manifest["bundle_sha256"],
        )
        self.assertEqual(
            candidate["cases"],
            [{"id": "TC-F10-MONTHLY-FORMAT-TEST-REVIEW", "revision": "r3"}],
        )

        comparable_base = copy.deepcopy(base)
        comparable_candidate = copy.deepcopy(candidate)
        for profile in (comparable_base, comparable_candidate):
            profile.pop("profile_id")
            profile.pop("prompt_set_identity")
        self.assertEqual(comparable_candidate, comparable_base)


if __name__ == "__main__":
    unittest.main()
