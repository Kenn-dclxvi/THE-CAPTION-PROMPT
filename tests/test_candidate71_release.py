from __future__ import annotations

import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / "prompts/candidates/the-caption-3ce91a4-validation-closure-r1"
RELEASE = ROOT / "prompts/releases/the-caption-3ce91a4-validation-closure-release-r1"
C43_RELEASE = ROOT / "prompts/releases/the-caption-3ce91a4-outcome-authority-boundary-release-r1"


class Candidate71ReleaseTest(unittest.TestCase):
    def test_release_is_content_identical_to_candidate(self) -> None:
        candidate = verify_bundle(CANDIDATE)
        release = verify_bundle(RELEASE)

        self.assertEqual(release["bundle_sha256"], candidate["bundle_sha256"])
        self.assertEqual(release["files"], candidate["files"])
        self.assertEqual(release["artifact"]["release_status"], "approved_for_projection")
        self.assertEqual(release["artifact"]["approval_status"], "approved")
        self.assertEqual(
            release["provenance"]["candidate_source_commit"],
            "bcfce844bbed28269429322a24545032cc64bf14",
        )
        self.assertEqual(release["provenance"]["runtime_projection_status"], "not_projected")
        self.assertEqual(release["content_relation"]["changed_targets"], [])

    def test_only_root_agents_differs_from_projected_candidate43(self) -> None:
        current = verify_bundle(C43_RELEASE)
        release = verify_bundle(RELEASE)
        current_files = {entry["target"]: entry for entry in current["files"]}
        release_files = {entry["target"]: entry for entry in release["files"]}

        changed = [
            target
            for target in sorted(current_files)
            if current_files[target] != release_files[target]
        ]
        self.assertEqual(changed, ["AGENTS.md"])


if __name__ == "__main__":
    unittest.main()
