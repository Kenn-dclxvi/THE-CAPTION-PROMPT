from __future__ import annotations

import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C43 = ROOT / "prompts/candidates/the-caption-3ce91a4-outcome-authority-boundary-r1"
C49 = ROOT / "prompts/candidates/the-caption-3ce91a4-explicit-delegation-control-boundary-r1"
C51 = ROOT / "prompts/candidates/the-caption-3ce91a4-root-operation-completion-boundary-r1"


def control_lines(path: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("- ") or ":" not in line:
            continue
        label = line[2:].split(":", 1)[0]
        result[label] = line
    return result


class Candidate51PromptTest(unittest.TestCase):
    def test_candidate_is_a_single_target_direct_child_of_candidate49(self) -> None:
        source = verify_bundle(C49)
        candidate = verify_bundle(C51)

        self.assertEqual(
            candidate["prompt_identity"],
            "the-caption-3ce91a4-root-operation-completion-boundary-r1",
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

    def test_only_delegation_and_completion_change_from_candidate49(self) -> None:
        source = control_lines(C49 / "files/AGENTS.md")
        candidate = control_lines(C51 / "files/AGENTS.md")

        self.assertEqual(set(candidate), set(source))
        for label in ("SPEC", "CONTEXT", "METHOD", "RECOVERY"):
            self.assertEqual(candidate[label], source[label])
        self.assertNotEqual(candidate["DELEGATION"], source["DELEGATION"])
        self.assertNotEqual(candidate["COMPLETION"], source["COMPLETION"])

    def test_root_producer_and_all_predicate_completion_are_restored(self) -> None:
        candidate = control_lines(C51 / "files/AGENTS.md")

        for required in (
            "それ以外はrootをproducerとする",
            "各operationへproducer execution identityを一つbind",
        ):
            self.assertIn(required, candidate["DELEGATION"])
        for required in (
            "開始したoperation",
            "全predicate",
            "bind済みproducerのterminal resultが揃うまで完了にしない",
        ):
            self.assertIn(required, candidate["COMPLETION"])

        text = (C51 / "files/AGENTS.md").read_text(encoding="utf-8")
        self.assertNotIn("ROOT_BATCH", text)
        self.assertNotIn("INDEPENDENCE", text)
        self.assertNotIn("同一model step", text)

    def test_root_control_remains_materially_smaller_than_candidate43(self) -> None:
        source_size = (C43 / "files/AGENTS.md").stat().st_size
        candidate_size = (C51 / "files/AGENTS.md").stat().st_size

        self.assertLess(candidate_size, source_size * 0.65)


if __name__ == "__main__":
    unittest.main()
