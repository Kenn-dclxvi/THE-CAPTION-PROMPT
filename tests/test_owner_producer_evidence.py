import hashlib
import json
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path

from scripts.evaluation_loop import (
    QUALITY_RATING,
    QUALITY_RATING_V2,
    EvaluationError,
    layer3_rate,
)
from scripts.owner_producer_evidence import collect


class OwnerProducerEvidenceTests(unittest.TestCase):
    def test_rating_contract_hash_matches_current_configuration(self) -> None:
        contract = (
            Path(__file__).resolve().parents[1]
            / "evaluations"
            / "rating-contracts"
            / "owner-producer-quality-v3.json"
        )
        self.assertEqual(
            hashlib.sha256(contract.read_bytes()).hexdigest(),
            QUALITY_RATING["contract_sha256"],
        )

    def test_rating_v2_contract_hash_remains_supported(self) -> None:
        contract = (
            Path(__file__).resolve().parents[1]
            / "evaluations"
            / "rating-contracts"
            / "owner-producer-quality-v2.json"
        )
        self.assertEqual(
            hashlib.sha256(contract.read_bytes()).hexdigest(),
            QUALITY_RATING_V2["contract_sha256"],
        )

    def make_cycle(self, root: Path, with_child: bool) -> Path:
        cycle = root / "cycle"
        run_id = "run-1"
        binding = cycle / "layer2" / "bindings" / "binding.json"
        binding.parent.mkdir(parents=True)
        binding.write_text(
            json.dumps(
                {
                    "case_id": "TC-F10-TEST",
                    "comparison_conditions": {"quality_rating": QUALITY_RATING},
                    "iteration": 1,
                    "run_id": run_id,
                    "status": "valid",
                }
            ),
            encoding="utf-8",
        )
        case = cycle / "layer2" / "evidence" / run_id / "case.json"
        case.parent.mkdir(parents=True)
        case.write_text(
            json.dumps(
                {
                    "id": "TC-F10-TEST",
                    "payload": {
                        "trial_prompt_input": {
                            "task_kind_goal_and_done_condition": "[F10-C1] report result. [F10-C2] keep clean.",
                            "validation_conditions_and_non_machine_risk": "non_machine_risk=response-quality, owner=independent response check."
                        }
                    }
                }
            ),
            encoding="utf-8",
        )
        sessions = [
            {
                "parent_thread_id": None,
                "rollout_file": str(root / "root.jsonl"),
                "source": "exec",
                "thread_id": "root-thread",
            }
        ]
        if with_child:
            rollout = root / "child.jsonl"
            rollout.write_text(
                json.dumps(
                    {
                        "type": "event_msg",
                        "payload": {
                            "type": "task_complete",
                            "last_agent_message": "F10-C1 and F10-C2 passed from the supplied evidence."
                        },
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            sessions.append(
                {
                    "parent_thread_id": "root-thread",
                    "rollout_file": str(rollout),
                    "source": {
                        "subagent": {
                            "thread_spawn": {"agent_path": "/root/independent_response_check"}
                        }
                    },
                    "thread_id": "child-thread",
                }
            )
        usage = cycle / "layer2" / "extensions" / run_id / "all-agent-usage" / "usage.json"
        usage.parent.mkdir(parents=True)
        usage.write_text(
            json.dumps({"root_thread_id": "root-thread", "sessions": sessions}),
            encoding="utf-8",
        )
        return cycle

    def test_distinct_matching_producer_is_score_4_eligible(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            report = collect(self.make_cycle(Path(temp), with_child=True))
            self.assertEqual(report["ineligible_run_count"], 0)
            self.assertTrue(report["runs"][0]["score_4_owner_evidence_eligible"])
            self.assertEqual(report["runs"][0]["admissible_producer_count"], 1)

    def test_missing_producer_prohibits_score_4(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            report = collect(self.make_cycle(Path(temp), with_child=False))
            self.assertEqual(report["ineligible_run_count"], 1)
            self.assertFalse(report["runs"][0]["score_4_owner_evidence_eligible"])
            self.assertEqual(report["runs"][0]["status"], "failed")

    def test_rating_layer_rejects_score_4_without_admissible_producer(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            cycle = self.make_cycle(Path(temp), with_child=False)
            evidence = cycle / "layer2" / "evidence" / "run-1"
            (evidence / "execution.json").write_text(
                json.dumps({"status": "valid"}), encoding="utf-8"
            )
            report_path = cycle / "layer3" / "owner-producer-evidence.json"
            report_path.parent.mkdir(parents=True)
            report_path.write_text(
                json.dumps(collect(cycle)), encoding="utf-8"
            )
            with self.assertRaisesRegex(
                EvaluationError, "score 4 requires an admissible owner-producer result"
            ):
                layer3_rate(
                    Namespace(
                        cycle=str(cycle),
                        reason="outcome text is otherwise correct",
                        run_id="run-1",
                        score=4,
                    )
                )

    def test_rating_v3_requires_bound_command_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            cycle = self.make_cycle(Path(temp), with_child=True)
            evidence = cycle / "layer2" / "evidence" / "run-1"
            (evidence / "execution.json").write_text(
                json.dumps({"status": "valid"}), encoding="utf-8"
            )
            report_path = cycle / "layer3" / "owner-producer-evidence.json"
            report_path.parent.mkdir(parents=True)
            report_path.write_text(json.dumps(collect(cycle)), encoding="utf-8")
            args = Namespace(
                cycle=str(cycle),
                reason="outcome and validation are correct",
                run_id="run-1",
                score=4,
            )

            with self.assertRaisesRegex(EvaluationError, "missing file"):
                layer3_rate(args)

            command_path = (
                cycle
                / "layer2"
                / "extensions"
                / "run-1"
                / "all-agent-command-evidence"
                / "evidence.json"
            )
            command_path.parent.mkdir(parents=True)
            command_path.write_text(
                json.dumps(
                    {
                        "schema_version": QUALITY_RATING["command_evidence_schema_version"],
                        "run_id": "run-1",
                        "successful_commands": [],
                    }
                ),
                encoding="utf-8",
            )

            layer3_rate(args)
            rating = json.loads(
                (cycle / "layer3" / "ratings" / "run-1.json").read_text()
            )
            self.assertEqual(rating["quality_rating_contract"], "owner-producer-quality-v3")
            self.assertEqual(rating["command_evidence_status"], "available")


if __name__ == "__main__":
    unittest.main()
