from __future__ import annotations

import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C43 = ROOT / "prompts/candidates/the-caption-3ce91a4-outcome-authority-boundary-r1"
C50 = ROOT / "prompts/candidates/the-caption-3ce91a4-root-read-batch-r1"


def control_lines(path: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("- ") or ":" not in line:
            continue
        label = line[2:].split(":", 1)[0]
        result[label] = line
    return result


class Candidate50PromptTest(unittest.TestCase):
    def test_candidate_is_a_single_target_direct_child_of_candidate43(self) -> None:
        source = verify_bundle(C43)
        candidate = verify_bundle(C50)

        self.assertEqual(
            candidate["prompt_identity"],
            "the-caption-3ce91a4-root-read-batch-r1",
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

    def test_existing_candidate43_control_lines_are_identical(self) -> None:
        source = control_lines(C43 / "files/AGENTS.md")
        candidate = control_lines(C50 / "files/AGENTS.md")

        self.assertEqual(set(candidate) - set(source), {"ROOT_BATCH"})
        for label, line in source.items():
            self.assertEqual(candidate[label], line)

    def test_root_batch_preserves_command_evidence_and_dependency_boundary(self) -> None:
        root_batch = control_lines(C50 / "files/AGENTS.md")["ROOT_BATCH"]

        for required in (
            "spec_ready=true",
            "rootがproducer",
            "read-only predicate",
            "commandとexitを分離",
            "同一model step",
            "TaskSpec、repository authority、既読sourceを再探索しない",
            "write / test / dependency操作",
            "前段resultで対象かcommandが変わる確認",
        ):
            self.assertIn(required, root_batch)


if __name__ == "__main__":
    unittest.main()
