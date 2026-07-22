from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C43 = ROOT / "prompts/candidates/the-caption-3ce91a4-outcome-authority-boundary-r1"
C64 = ROOT / "prompts/candidates/the-caption-3ce91a4-self-contained-execution-paths-r1"
PROFILES = ROOT / "evaluations/profiles"
C43_F_PROFILE = PROFILES / (
    "candidate43-outcome-authority-boundary-outcome-quality-owner-diagnostic-v9-"
    "targeted2-global-m10-n5-catalog-fixed-r1.json"
)
C64_F_PROFILE = PROFILES / (
    "candidate64-self-contained-execution-paths-outcome-quality-owner-diagnostic-v9-"
    "targeted2-global-m10-n5-catalog-fixed-r1.json"
)
C43_A_PROFILE = PROFILES / (
    "candidate43-outcome-authority-boundary-ambiguity-targeted2-v10-global-m10-n5-"
    "catalog-fixed-r1.json"
)
C64_A_PROFILE = PROFILES / (
    "candidate64-self-contained-execution-paths-ambiguity-targeted2-v10-global-m10-"
    "n5-catalog-fixed-r1.json"
)
C43_D_PROFILE = PROFILES / (
    "candidate43-outcome-authority-boundary-explicit-producer-d01-v9-global-m5-n5-"
    "catalog-fixed-r1.json"
)
C64_D_PROFILE = PROFILES / (
    "candidate64-self-contained-execution-paths-explicit-producer-d01-v9-global-m5-"
    "n5-catalog-fixed-r1.json"
)
F10_CASE = ROOT / "evaluations/cases/TC-F10-MONTHLY-FORMAT-TEST-REVIEW/r3"
D01_CASE = ROOT / "evaluations/cases/TC-D01-EXPLICIT-PRODUCER-MONTHLY-REVIEW/r1"


def source_clauses() -> dict[str, str]:
    clauses: dict[str, str] = {}
    text = (C43 / "files/AGENTS.md").read_text(encoding="utf-8")
    for line in text.splitlines():
        if not line.startswith("- "):
            continue
        label, body = line[2:].split(": ", 1)
        for index, part in enumerate((part for part in body.split("。") if part), 1):
            clauses[f"{label}{index}"] = f"{part}。"
    return clauses


EXPECTED_COUNTS = {
    **{f"SPEC{index}": 1 for index in range(1, 6)},
    "SPEC6": 2,
    "PRODUCER1": 2,
    "PRODUCER2": 2,
    "PRODUCER3": 2,
    "PRODUCER4": 2,
    "PRODUCER5": 2,
    "TERMINAL1": 2,
    "TERMINAL2": 2,
    "CONTEXT1": 1,
    "CONTEXT2": 1,
    "CONTEXT3": 1,
    "OWNER_ROLE1": 2,
    "OWNER_ROLE2": 1,
    "OWNER_ROLE3": 1,
    "OWNER_ROLE4": 1,
    "OWNER_ROLE5": 1,
    "OWNER_ROLE6": 2,
    "OWNER_ROLE7": 1,
    "ROOT1": 1,
    "INDEPENDENCE1": 1,
    "INDEPENDENCE2": 2,
    "METHOD1": 1,
    "METHOD2": 1,
    "METHOD3": 1,
    "METHOD4": 1,
    "RECOVERY1": 1,
    "RECOVERY2": 1,
}


class Candidate64Test(unittest.TestCase):
    def test_candidate_is_a_single_target_direct_child_of_candidate43(self) -> None:
        source = verify_bundle(C43)
        candidate = verify_bundle(C64)

        self.assertEqual(
            candidate["prompt_identity"],
            "the-caption-3ce91a4-self-contained-execution-paths-r1",
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
            [
                target
                for target in sorted(source_files)
                if source_files[target] != candidate_files[target]
            ],
            ["AGENTS.md"],
        )

    def test_preserves_every_candidate43_atomic_clause(self) -> None:
        clauses = source_clauses()
        self.assertEqual(set(clauses), set(EXPECTED_COUNTS))
        text = (C64 / "files/AGENTS.md").read_text(encoding="utf-8")

        for clause_id, expected_count in EXPECTED_COUNTS.items():
            with self.subTest(clause_id=clause_id):
                self.assertEqual(text.count(clauses[clause_id]), expected_count)

    def test_has_four_ordered_execution_blocks(self) -> None:
        text = (C64 / "files/AGENTS.md").read_text(encoding="utf-8")
        headings = [
            "## 1. Start and path selection",
            "## 2. Root producer operation",
            "## 3. Delegated producer operation",
            "## 4. Failure and recovery",
        ]
        positions = [text.index(heading) for heading in headings]
        self.assertEqual(positions, sorted(positions))
        self.assertEqual(text.count("\n## "), 4)
        self.assertIn(
            "TaskSpecが独立したproducer executionを明示した場合だけdelegated "
            "producer operationへ進み、それ以外はroot producer operationへ進む。",
            text,
        )

    def test_root_and_delegated_paths_are_self_contained(self) -> None:
        text = (C64 / "files/AGENTS.md").read_text(encoding="utf-8")
        root_start = text.index("## 2. Root producer operation")
        delegated_start = text.index("## 3. Delegated producer operation")
        failure_start = text.index("## 4. Failure and recovery")
        root = text[root_start:delegated_start]
        delegated = text[delegated_start:failure_start]

        for block in (root, delegated):
            for required in (
                "`result / constraint / terminal`は同一operation identity内だけへbind",
                "producer execution identityを一つbindする",
                "全predicateにbind済みproducerのterminal result",
                "result欠落ならoperationもnonterminal",
                "bind済みcriterionの`false / failed`",
            ):
                self.assertIn(required, block)

        for delegated_only in (
            "worker packetへ",
            "`fork_turns=none`",
            "runtime_spawn_result.task_name",
            "FINAL_ANSWER.Sender",
            "rootがproducerでないoperation",
        ):
            self.assertNotIn(delegated_only, root)
            self.assertIn(delegated_only, delegated)

    def test_initial_structure_intentionally_increases_static_bytes(self) -> None:
        source_size = (C43 / "files/AGENTS.md").stat().st_size
        candidate_size = (C64 / "files/AGENTS.md").stat().st_size

        self.assertEqual(source_size, 3980)
        self.assertEqual(candidate_size, 5594)
        self.assertGreater(candidate_size, source_size)
        self.assertLess(candidate_size, int(source_size * 1.5))

    def test_n5_profiles_change_only_prompt_identity(self) -> None:
        manifest = verify_bundle(C64)
        for source_path, candidate_path in (
            (C43_F_PROFILE, C64_F_PROFILE),
            (C43_A_PROFILE, C64_A_PROFILE),
            (C43_D_PROFILE, C64_D_PROFILE),
        ):
            with self.subTest(candidate_profile=candidate_path.name):
                source = json.loads(source_path.read_text(encoding="utf-8"))
                candidate = json.loads(candidate_path.read_text(encoding="utf-8"))
                self.assertEqual(
                    candidate["prompt_set_identity"]["name"],
                    manifest["prompt_identity"],
                )
                self.assertEqual(
                    candidate["prompt_set_identity"]["bundle_sha256"],
                    manifest["bundle_sha256"],
                )

                comparable_source = copy.deepcopy(source)
                comparable_candidate = copy.deepcopy(candidate)
                for profile in (comparable_source, comparable_candidate):
                    profile.pop("profile_id")
                    profile.pop("prompt_set_identity")
                self.assertEqual(comparable_candidate, comparable_source)

    def test_d01_changes_only_model_visible_producer_binding(self) -> None:
        source_trial = json.loads(
            (F10_CASE / "trial-prompt-input.json").read_text(encoding="utf-8")
        )
        delegated_trial = json.loads(
            (D01_CASE / "trial-prompt-input.json").read_text(encoding="utf-8")
        )
        source_goal = source_trial.pop("task_kind_goal_and_done_condition")
        delegated_goal = delegated_trial.pop("task_kind_goal_and_done_condition")
        self.assertEqual(delegated_trial, source_trial)
        self.assertIn(source_goal.split("。", 1)[0], delegated_goal)
        self.assertIn("operation identity=monthly-format-review", delegated_goal)
        self.assertIn("local task_name=monthly_format_review_producer", delegated_goal)
        self.assertIn(
            "canonical producer identity=/root/monthly_format_review_producer",
            delegated_goal,
        )

        source_private = json.loads(
            (F10_CASE / "private/case-data.json").read_text(encoding="utf-8")
        )
        delegated_private = json.loads(
            (D01_CASE / "private/case-data.json").read_text(encoding="utf-8")
        )
        source_fixture = copy.deepcopy(source_private["fixture"])
        delegated_fixture = copy.deepcopy(delegated_private["fixture"])
        source_fixture.pop("case_spec")
        delegated_fixture.pop("case_spec")
        self.assertEqual(delegated_fixture, source_fixture)
        for key in ("seed", "oracle", "grader"):
            with self.subTest(private_section=key):
                self.assertEqual(delegated_private[key], source_private[key])
        self.assertEqual(
            (D01_CASE / "private/seed.patch").read_bytes(),
            (F10_CASE / "private/seed.patch").read_bytes(),
        )


if __name__ == "__main__":
    unittest.main()
