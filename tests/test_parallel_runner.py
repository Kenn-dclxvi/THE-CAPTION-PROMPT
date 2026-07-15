from __future__ import annotations

import json
import tempfile
import textwrap
import unittest
from pathlib import Path

from layer2.extensions.parallel_execution.parallel_runner import ParallelRunError, run_plan
from layer2.extensions.parallel_execution.prepare_plan import prepare_plan


class ParallelRunnerTest(unittest.TestCase):
    def make_capsule(
        self,
        root: Path,
        condition: str,
        case_id: str,
        repetition: int,
        fail_first: bool = False,
    ) -> Path:
        path = root / f"{condition}-{case_id}-{repetition}.json"
        path.write_text(
            json.dumps(
                {
                    "binding": {
                        "condition": condition,
                        "prompt_identity": f"prompt-{condition}",
                        "case_id": case_id,
                        "repetition": repetition,
                    },
                    "parameters": {"fail_first": fail_first},
                }
            ),
            encoding="utf-8",
        )
        return path

    def make_controller(self, root: Path) -> Path:
        path = root / "fake_evaluation_loop.py"
        path.write_text(
            textwrap.dedent(
                """
                import argparse
                import fcntl
                import json
                import time
                from pathlib import Path

                parser = argparse.ArgumentParser()
                parser.add_argument("subcommand")
                parser.add_argument("--cycle")
                parser.add_argument("--capsule")
                args = parser.parse_args()
                capsule = json.loads(Path(args.capsule).read_text())
                binding = capsule["binding"]
                root = Path(args.cycle).parent
                state_path = root / "state.json"
                lock_path = root / "state.lock"
                key = f"{binding['condition']}-{binding['case_id']}-{binding['repetition']}"

                def update(mutator):
                    with lock_path.open("a+") as lock:
                        fcntl.flock(lock, fcntl.LOCK_EX)
                        state = json.loads(state_path.read_text())
                        mutator(state)
                        state_path.write_text(json.dumps(state))
                        fcntl.flock(lock, fcntl.LOCK_UN)

                attempt = [0]
                def started(state):
                    state["active"] += 1
                    state["max_active"] = max(state["max_active"], state["active"])
                    state["attempts"][key] = state["attempts"].get(key, 0) + 1
                    attempt[0] = state["attempts"][key]
                update(started)
                time.sleep(0.1)
                update(lambda state: state.__setitem__("active", state["active"] - 1))
                status = "excluded" if capsule["parameters"]["fail_first"] and attempt[0] == 1 else "valid"
                print(json.dumps({"layer": 2, "run_id": key + f"-{attempt[0]}", "status": status}))
                """
            ),
            encoding="utf-8",
        )
        return path

    def make_plan(
        self,
        root: Path,
        capsules: list[Path],
        max_workers: int = 2,
        waves: list[int] | None = None,
    ) -> Path:
        cycle = root / "cycle"
        (cycle / "layer1").mkdir(parents=True)
        (cycle / "layer1" / "set.json").write_text("{}\n", encoding="utf-8")
        (root / "state.json").write_text(
            json.dumps({"active": 0, "max_active": 0, "attempts": {}}), encoding="utf-8"
        )
        plan = root / "plan.json"
        plan.write_text(
            json.dumps(
                {
                    "schema_version": "the-caption-prompt.parallel-execution-plan/v1",
                    "cycle": str(cycle),
                    "evaluation_loop": str(self.make_controller(root)),
                    "max_workers": max_workers,
                    "max_attempts": 3,
                    "monitor_interval_seconds": 0.05,
                    "jobs": [
                        {"wave": wave, "capsule": str(path)}
                        for wave, path in zip(waves or range(1, len(capsules) + 1), capsules)
                    ],
                }
            ),
            encoding="utf-8",
        )
        return plan

    def test_runs_two_slots_concurrently_and_retries_excluded_attempt(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            capsules = [
                self.make_capsule(root, "a", "CASE-1", 1, fail_first=True),
                self.make_capsule(root, "b", "CASE-1", 1),
                self.make_capsule(root, "a", "CASE-2", 1),
            ]
            summary = run_plan(
                self.make_plan(root, capsules, waves=[1, 1, 2]), root / "runner-output"
            )
            self.assertEqual(summary["status"], "complete")
            self.assertEqual(summary["valid_slots"], 3)
            self.assertEqual(summary["attempt_count"], 4)
            self.assertEqual(summary["excluded_attempt_count"], 1)
            state = json.loads((root / "state.json").read_text())
            self.assertEqual(state["max_active"], 2)
            self.assertEqual(state["attempts"]["a-CASE-1-1"], 2)
            self.assertTrue((root / "runner-output" / "os-samples.jsonl").is_file())

    def test_rejects_duplicate_execution_slot_before_start(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            capsule = self.make_capsule(root, "a", "CASE-1", 1)
            plan = self.make_plan(root, [capsule, capsule], waves=[1, 1])
            with self.assertRaisesRegex(ParallelRunError, "duplicate execution slot"):
                run_plan(plan, root / "runner-output")

    def test_prepares_alternating_ab_waves_without_changing_template_parameters(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cycle = root / "cycle"
            (cycle / "layer1").mkdir(parents=True)
            (cycle / "layer1" / "set.json").write_text("{}\n", encoding="utf-8")
            evaluator = root / "evaluation_loop.py"
            evaluator.write_text("# test\n", encoding="utf-8")
            templates = [
                self.make_capsule(root, "a", "CASE-1", 99),
                self.make_capsule(root, "b", "CASE-1", 99),
                self.make_capsule(root, "a", "CASE-2", 99),
                self.make_capsule(root, "b", "CASE-2", 99),
            ]
            result = prepare_plan(
                templates,
                repetitions=2,
                cycle=cycle,
                evaluator=evaluator,
                output=root / "parallel-inputs",
            )
            self.assertEqual(result["slot_count"], 8)
            self.assertEqual(result["wave_count"], 4)
            plan = json.loads(Path(result["plan"]).read_text())
            self.assertEqual([job["wave"] for job in plan["jobs"]], [1, 1, 2, 2, 3, 3, 4, 4])
            bindings = [
                json.loads(Path(job["capsule"]).read_text())["binding"] for job in plan["jobs"]
            ]
            self.assertEqual(
                [(item["condition"], item["case_id"], item["repetition"]) for item in bindings],
                [
                    ("a", "CASE-1", 1),
                    ("b", "CASE-1", 1),
                    ("b", "CASE-2", 1),
                    ("a", "CASE-2", 1),
                    ("b", "CASE-1", 2),
                    ("a", "CASE-1", 2),
                    ("a", "CASE-2", 2),
                    ("b", "CASE-2", 2),
                ],
            )
            generated = json.loads(Path(plan["jobs"][0]["capsule"]).read_text())
            self.assertEqual(generated["parameters"], {"fail_first": False})


if __name__ == "__main__":
    unittest.main()
