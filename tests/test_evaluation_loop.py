from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.evaluation_loop import kpi_difference_b_minus_a


ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "evaluation_loop.py"


class EvaluationLoopTest(unittest.TestCase):
    def test_kpi_difference_reports_b_minus_a_without_a_winner(self) -> None:
        self.assertEqual(
            kpi_difference_b_minus_a(
                {"quality_score": 75, "total_tokens": 200, "elapsed_seconds": 20},
                {"quality_score": 50, "total_tokens": 100, "elapsed_seconds": 10},
            ),
            {"quality_score": -25, "total_tokens": -100, "elapsed_seconds": -10},
        )

    def cli(self, *args: str) -> dict:
        completed = subprocess.run(
            [sys.executable, str(CLI), *args],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        return json.loads(completed.stdout)

    def make_set(self, root: Path) -> Path:
        fixture = root / "fixture"
        fixture.mkdir(parents=True)
        (fixture / "input.txt").write_text("input\n", encoding="utf-8")
        (fixture / "input-link.txt").symlink_to("input.txt")
        manifest = root / "set.json"
        manifest.write_text(
            json.dumps(
                {
                    "set_id": "test-set",
                    "cases": [
                        {
                            "id": "TEST-CASE",
                            "fixture": "fixture",
                            "payload": {"task": "test task", "future_parameter": "opaque"},
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        return manifest

    def execute(self, cycle: Path, condition: str, identity: str, repetition: int, tokens: int) -> str:
        command = (
            "import json,os,pathlib; "
            "case=json.loads(pathlib.Path(os.environ['EVAL_CASE_FILE']).read_text()); "
            "capsule=json.loads(pathlib.Path(os.environ['EVAL_RUN_CAPSULE_FILE']).read_text()); "
            "assert case['payload']['future_parameter']=='opaque'; "
            "assert capsule['parameters']['future_parameter']==42; "
            "pathlib.Path('result.txt').write_text('result\\n', encoding='utf-8'); "
            "extension=pathlib.Path(os.environ['EVAL_EXTENSION_DIR'])/'token-analysis'; "
            "extension.mkdir(); "
            "(extension/'provider-usage.json').write_text(json.dumps({'future_detail': 42})); "
            f"pathlib.Path(os.environ['EVAL_USAGE_FILE']).write_text(json.dumps({{'total_tokens': {tokens}}}))"
        )
        capsule = cycle.parent / f"{condition}-{repetition}.json"
        capsule.write_text(
            json.dumps(
                {
                    "schema_version": "the-caption-prompt.execution-capsule/v1",
                    "binding": {
                        "condition": condition,
                        "prompt_identity": identity,
                        "case_id": "TEST-CASE",
                        "repetition": repetition,
                    },
                    "adapter": {"argv": [sys.executable, "-c", command]},
                    "parameters": {"future_parameter": 42},
                }
            ),
            encoding="utf-8",
        )
        result = self.cli(
            "run",
            "--cycle",
            str(cycle),
            "--capsule",
            str(capsule),
        )
        return result["run_id"]

    def test_four_layer_kpi_comparison_without_scenario_or_prompt(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cycle = root / "cycle"
            manifest = self.make_set(root)
            frozen = self.cli("freeze-set", "--set", str(manifest), "--cycle", str(cycle))
            self.assertEqual(frozen["case_count"], 1)
            self.assertTrue((cycle / "layer1" / "fixtures" / "TEST-CASE" / "input-link.txt").is_symlink())

            set_a_ids = [self.execute(cycle, "a", "prompt-set-a", n, 120) for n in (1, 2)]
            set_b_ids = [self.execute(cycle, "b", "prompt-set-b", n, 100) for n in (1, 2)]
            for run_id in set_a_ids + set_b_ids:
                evidence = cycle / "layer2" / "evidence" / run_id
                self.assertTrue((evidence / "workspace" / "input-link.txt").is_symlink())
                execution = json.loads((evidence / "execution.json").read_text())
                self.assertNotIn("condition", execution)
                self.assertFalse((evidence / "run-capsule.json").exists())
                self.assertEqual(
                    json.loads((evidence / "usage.json").read_text()),
                    {"total_tokens": execution["total_tokens"]},
                )
                self.assertFalse((evidence / "extensions").exists())
                self.assertTrue(
                    (cycle / "layer2" / "extensions" / run_id / "token-analysis" / "provider-usage.json").exists()
                )
                self.assertTrue((cycle / "layer2" / "capsules" / f"{run_id}.json").exists())
                self.assertTrue((cycle / "layer2" / "bindings" / f"{run_id}.json").exists())
            for run_id in set_a_ids:
                self.cli("rate", "--cycle", str(cycle), "--run-id", run_id, "--score", "3", "--reason", "test rating")
            for run_id in set_b_ids:
                self.cli("rate", "--cycle", str(cycle), "--run-id", run_id, "--score", "4", "--reason", "test rating")

            result = self.cli("compare", "--cycle", str(cycle))
            self.assertEqual(result["repetition_count"], 2)
            comparison = json.loads((cycle / "layer4" / "comparison.json").read_text())
            self.assertNotIn("winner", comparison)
            self.assertEqual(comparison["schema_version"], "the-caption-prompt.kpi-comparison/v2")
            self.assertEqual(comparison["b"]["prompt_identity"], "prompt-set-b")
            self.assertEqual(comparison["difference_b_minus_a"]["quality_score"], 25.0)
            self.assertEqual(comparison["difference_b_minus_a"]["total_tokens"], -20.0)
            self.assertIsInstance(comparison["difference_b_minus_a"]["elapsed_seconds"], float)
            self.assertEqual(comparison["excluded_attempts"], [])
            self.assertFalse((cycle / "prompts").exists())
            self.assertFalse((cycle / "layer5").exists())

    def test_layer_outputs_are_not_overwritten(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cycle = root / "cycle"
            manifest = self.make_set(root)
            self.cli("freeze-set", "--set", str(manifest), "--cycle", str(cycle))
            completed = subprocess.run(
                [sys.executable, str(CLI), "freeze-set", "--set", str(manifest), "--cycle", str(cycle)],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            self.assertEqual(completed.returncode, 2)
            self.assertIn("cycle directory is not empty", completed.stderr)

    def test_excluded_external_failure_is_preserved_and_does_not_occupy_repetition(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cycle = root / "cycle"
            manifest = self.make_set(root)
            self.cli("freeze-set", "--set", str(manifest), "--cycle", str(cycle))

            excluded_command = (
                "import json,os,pathlib,sys; "
                "pathlib.Path(os.environ['EVAL_RUN_STATUS_FILE']).write_text(json.dumps({"
                "'schema_version':'the-caption-prompt.run-status/v1',"
                "'status':'excluded','category':'external_failure',"
                "'reason_code':'codex_collab_parent_thread_missing'})); "
                "sys.exit(75)"
            )
            capsule = root / "excluded.json"
            capsule.write_text(
                json.dumps(
                    {
                        "binding": {
                            "condition": "a",
                            "prompt_identity": "prompt-set-a",
                            "case_id": "TEST-CASE",
                            "repetition": 1,
                        },
                        "adapter": {"argv": [sys.executable, "-c", excluded_command]},
                    }
                ),
                encoding="utf-8",
            )
            excluded = self.cli("run", "--cycle", str(cycle), "--capsule", str(capsule))
            self.assertEqual(excluded["status"], "excluded")
            excluded_id = excluded["run_id"]
            excluded_evidence = cycle / "layer2" / "evidence" / excluded_id
            self.assertTrue((excluded_evidence / "exclusion.json").is_file())
            excluded_execution = json.loads((excluded_evidence / "execution.json").read_text())
            self.assertEqual(excluded_execution["status"], "excluded")
            self.assertIsNone(excluded_execution["total_tokens"])

            rate = subprocess.run(
                [
                    sys.executable,
                    str(CLI),
                    "rate",
                    "--cycle",
                    str(cycle),
                    "--run-id",
                    excluded_id,
                    "--score",
                    "4",
                    "--reason",
                    "must not be accepted",
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            self.assertEqual(rate.returncode, 2)
            self.assertIn("excluded run cannot be quality-rated", rate.stderr)

            valid_a = self.execute(cycle, "a", "prompt-set-a", 1, 120)
            valid_b = self.execute(cycle, "b", "prompt-set-b", 1, 120)
            for run_id in (valid_a, valid_b):
                self.cli("rate", "--cycle", str(cycle), "--run-id", run_id, "--score", "4", "--reason", "valid")
            self.cli("compare", "--cycle", str(cycle))
            comparison = json.loads((cycle / "layer4" / "comparison.json").read_text())
            self.assertEqual(comparison["repetition_count"], 1)
            self.assertEqual(comparison["a"]["median"]["total_tokens"], 120)
            self.assertEqual(comparison["b"]["median"]["total_tokens"], 120)
            self.assertEqual(len(comparison["excluded_attempts"]), 1)
            self.assertEqual(
                comparison["excluded_attempts"][0]["reason_code"],
                "codex_collab_parent_thread_missing",
            )
            self.assertEqual(len(list((cycle / "layer2" / "bindings").glob("*.json"))), 3)


if __name__ == "__main__":
    unittest.main()
