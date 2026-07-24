from __future__ import annotations

import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C43 = ROOT / "prompts/candidates/the-caption-3ce91a4-outcome-authority-boundary-r1"
C51 = ROOT / "prompts/candidates/the-caption-3ce91a4-root-operation-completion-boundary-r1"
C52 = ROOT / "prompts/candidates/the-caption-3ce91a4-root-independence-boundary-r1"


def control_lines(path: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("- ") or ":" not in line:
            continue
        label = line[2:].split(":", 1)[0]
        result[label] = line
    return result


class Candidate52PromptTest(unittest.TestCase):
    def test_candidate_is_a_single_target_direct_child_of_candidate51(self) -> None:
        source = verify_bundle(C51)
        candidate = verify_bundle(C52)

        self.assertEqual(
            candidate["prompt_identity"],
            "the-caption-3ce91a4-root-independence-boundary-r1",
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
        self.assertEqual(
            [target for target in sorted(source_files) if source_files[target] != candidate_files[target]],
            ["AGENTS.md"],
        )

    def test_adds_only_exact_candidate43_independence_line(self) -> None:
        c43 = control_lines(C43 / "files/AGENTS.md.txt")
        c51 = control_lines(C51 / "files/AGENTS.md.txt")
        c52 = control_lines(C52 / "files/AGENTS.md.txt")

        self.assertEqual(set(c52), set(c51) | {"INDEPENDENCE"})
        for label in c51:
            self.assertEqual(c52[label], c51[label])
        self.assertEqual(c52["INDEPENDENCE"], c43["INDEPENDENCE"])

    def test_does_not_add_method_or_worker_controls(self) -> None:
        text = (C52 / "files/AGENTS.md.txt").read_text(encoding="utf-8")

        for forbidden in (
            "ROOT_BATCH",
            "同一model step",
            "OWNER_ROLE:",
            "- ROOT:",
            "- PRODUCER:",
            "- TERMINAL:",
        ):
            self.assertNotIn(forbidden, text)


if __name__ == "__main__":
    unittest.main()
