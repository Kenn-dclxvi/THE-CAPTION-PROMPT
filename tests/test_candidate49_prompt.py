from __future__ import annotations

import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C43 = ROOT / "prompts/candidates/the-caption-3ce91a4-outcome-authority-boundary-r1"
C49 = ROOT / "prompts/candidates/the-caption-3ce91a4-explicit-delegation-control-boundary-r1"


def control_lines(path: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("- ") or ":" not in line:
            continue
        label = line[2:].split(":", 1)[0]
        result[label] = line
    return result


class Candidate49PromptTest(unittest.TestCase):
    def test_candidate_is_a_single_target_direct_child_of_candidate43(self) -> None:
        source = verify_bundle(C43)
        candidate = verify_bundle(C49)

        self.assertEqual(
            candidate["prompt_identity"],
            "the-caption-3ce91a4-explicit-delegation-control-boundary-r1",
        )
        self.assertEqual(
            candidate["content_relation"],
            {
                "changed_targets": ["AGENTS.md"],
                "kind": "direct_child_full_bundle",
                "source_prompt_identity": source["prompt_identity"],
            },
        )

        source_files = {entry["target"]: entry for entry in source["files"]}
        candidate_files = {entry["target"]: entry for entry in candidate["files"]}
        changed = [
            target
            for target in sorted(source_files)
            if source_files[target] != candidate_files[target]
        ]
        self.assertEqual(changed, ["AGENTS.md"])

    def test_spec_method_and_recovery_are_identical_to_candidate43(self) -> None:
        source = control_lines(C43 / "files/AGENTS.md.txt")
        candidate = control_lines(C49 / "files/AGENTS.md.txt")

        for label in ("SPEC", "METHOD", "RECOVERY"):
            self.assertEqual(candidate[label], source[label])

    def test_worker_control_graph_is_replaced_by_three_direct_labels(self) -> None:
        candidate_path = C49 / "files/AGENTS.md.txt"
        candidate = control_lines(candidate_path)

        self.assertEqual(
            list(candidate),
            ["SPEC", "DELEGATION", "CONTEXT", "COMPLETION", "METHOD", "RECOVERY"],
        )
        for removed in ("PRODUCER", "TERMINAL", "OWNER_ROLE", "ROOT", "INDEPENDENCE"):
            self.assertNotIn(removed, candidate)

        text = candidate_path.read_text(encoding="utf-8")
        for added_abstraction in ("admission", "premise", "applicability", "dependency"):
            self.assertNotIn(added_abstraction, text)

    def test_root_control_is_materially_smaller(self) -> None:
        source_size = (C43 / "files/AGENTS.md.txt").stat().st_size
        candidate_size = (C49 / "files/AGENTS.md.txt").stat().st_size

        self.assertLess(candidate_size, source_size * 0.65)


if __name__ == "__main__":
    unittest.main()
