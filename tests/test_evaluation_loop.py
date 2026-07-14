from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.evaluation_loop import compare_sets


ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "evaluation_loop.py"


class EvaluationLoopTest(unittest.TestCase):
    def test_winner_uses_only_the_three_kpis(self) -> None:
        self.assertEqual(
            compare_sets(
                {"quality_score": 75, "total_tokens": 200, "elapsed_seconds": 20},
                {"quality_score": 50, "total_tokens": 100, "elapsed_seconds": 10},
            ),
            "a",
        )
        self.assertEqual(
            compare_sets(
                {"quality_score": 75, "total_tokens": 100, "elapsed_seconds": 20},
                {"quality_score": 75, "total_tokens": 200, "elapsed_seconds": 10},
            ),
            "a",
        )
        self.assertEqual(
            compare_sets(
                {"quality_score": 75, "total_tokens": 100, "elapsed_seconds": 10},
                {"quality_score": 75, "total_tokens": 100, "elapsed_seconds": 20},
            ),
            "a",
        )
        self.assertEqual(
            compare_sets(
                {"quality_score": 75, "total_tokens": 100, "elapsed_seconds": 10},
                {"quality_score": 75, "total_tokens": 100, "elapsed_seconds": 10},
            ),
            "tie",
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

            set_a_ids = [self.execute(cycle, "a", "prompt-set-a", n, 120) for n in (1, 2)]
            set_b_ids = [self.execute(cycle, "b", "prompt-set-b", n, 100) for n in (1, 2)]
            for run_id in set_a_ids + set_b_ids:
                evidence = cycle / "layer2" / "evidence" / run_id
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

            decision = self.cli("decide", "--cycle", str(cycle))
            self.assertEqual(decision["winner"], "b")
            decision_file = json.loads((cycle / "layer4" / "decision.json").read_text())
            self.assertEqual(decision_file["winner"], "b")
            self.assertEqual(decision_file["b"]["prompt_identity"], "prompt-set-b")
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


if __name__ == "__main__":
    unittest.main()
