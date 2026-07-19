import json
import tempfile
import unittest
from pathlib import Path

from scripts.response_claim_trace import collect


def completed(item: dict) -> dict:
    return {"type": "item.completed", "item": item}


class ResponseClaimTraceTests(unittest.TestCase):
    def collect_events(self, events: list[dict]) -> dict:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "events.jsonl"
            path.write_text(
                "".join(json.dumps(event) + "\n" for event in events),
                encoding="utf-8",
            )
            return collect(
                path,
                run_id="run-1",
                case_id="TC-F10-REVIEW",
                iteration=1,
            )

    def test_marks_unnumbered_adjacent_terminal_claim(self) -> None:
        diff = """diff --git a/src/app/main.py b/src/app/main.py
--- a/src/app/main.py
+++ b/src/app/main.py
@@ -24,1 +25,1 @@
-old_call()
+new_call()
"""
        result = self.collect_events(
            [
                completed(
                    {
                        "id": "item_1",
                        "type": "command_execution",
                        "command": "git show commit:src/app/main.py",
                        "aggregated_output": "old_call()\nnew_call()\n",
                    }
                ),
                completed(
                    {
                        "id": "item_2",
                        "type": "command_execution",
                        "command": "git diff commit^ commit -- src/app/main.py",
                        "aggregated_output": diff,
                    }
                ),
                completed(
                    {
                        "id": "item_3",
                        "type": "agent_message",
                        "text": "finding is ready without a coordinate",
                    }
                ),
                completed(
                    {
                        "id": "item_4",
                        "type": "agent_message",
                        "text": "location: src/app/main.py:24",
                    }
                ),
            ]
        )

        claim = result["response_claims"][0]
        self.assertEqual(claim["message_kind"], "terminal")
        self.assertEqual(claim["first_seen_sequence"], 4)
        self.assertEqual(claim["direct_coordinate_observation_sequences"], [])
        self.assertEqual(
            result["claim_alignment"][0],
            {
                "claim_sequence": 4,
                "delta": -1,
                "observed_changed_line": 25,
                "path": "src/app/main.py",
                "status": "adjacent",
            },
        )

    def test_binds_numbered_source_to_exact_claim(self) -> None:
        result = self.collect_events(
            [
                completed(
                    {
                        "id": "item_1",
                        "type": "command_execution",
                        "command": "git diff commit^ commit -- src/app/main.py",
                        "aggregated_output": (
                            "diff --git a/src/app/main.py b/src/app/main.py\n"
                            "--- a/src/app/main.py\n"
                            "+++ b/src/app/main.py\n"
                            "@@ -24,1 +25,1 @@\n"
                            "-old_call()\n"
                            "+new_call()\n"
                        ),
                    }
                ),
                completed(
                    {
                        "id": "item_2",
                        "type": "command_execution",
                        "command": "nl -ba src/app/main.py",
                        "aggregated_output": "    25\tnew_call()\n",
                    }
                ),
                completed(
                    {
                        "id": "item_3",
                        "type": "agent_message",
                        "text": "location: src/app/main.py:25",
                    }
                ),
            ]
        )

        claim = result["response_claims"][0]
        self.assertEqual(claim["direct_coordinate_observation_sequences"], [2])
        self.assertEqual(result["claim_alignment"][0]["status"], "exact")
        self.assertEqual(result["claim_alignment"][0]["delta"], 0)

    def test_binds_revision_prefixed_git_grep_output(self) -> None:
        result = self.collect_events(
            [
                completed(
                    {
                        "id": "item_1",
                        "type": "command_execution",
                        "command": (
                            "git grep -n format_test seed -- "
                            "src/app/main.py src/app/engine.py"
                        ),
                        "aggregated_output": (
                            "seed:src/app/main.py:25:    format_test=args.force\n"
                        ),
                    }
                ),
                completed(
                    {
                        "id": "item_2",
                        "type": "agent_message",
                        "text": "location: src/app/main.py:25",
                    }
                ),
            ]
        )

        claim = result["response_claims"][0]
        self.assertEqual(claim["direct_coordinate_observation_sequences"], [1])

    def test_tracks_first_seen_across_intermediate_and_terminal_messages(self) -> None:
        result = self.collect_events(
            [
                completed(
                    {
                        "id": "item_1",
                        "type": "agent_message",
                        "text": "candidate location src/app/main.py:25",
                    }
                ),
                completed(
                    {
                        "id": "item_2",
                        "type": "agent_message",
                        "text": "final location src/app/main.py:25",
                    }
                ),
            ]
        )

        self.assertEqual(len(result["response_claims"]), 2)
        self.assertEqual(result["response_claims"][0]["message_kind"], "intermediate")
        self.assertEqual(result["response_claims"][1]["message_kind"], "terminal")
        self.assertEqual(result["response_claims"][1]["first_seen_sequence"], 1)

    def test_trace_excludes_raw_command_output_message_and_rating_fields(self) -> None:
        secret = "sensitive-value"
        result = self.collect_events(
            [
                completed(
                    {
                        "id": "item_1",
                        "type": "command_execution",
                        "command": f"cat src/app/main.py # {secret}",
                        "aggregated_output": secret,
                    }
                ),
                completed(
                    {
                        "id": "item_2",
                        "type": "agent_message",
                        "text": f"{secret} src/app/main.py:25",
                    }
                ),
            ]
        )

        serialized = json.dumps(result)
        self.assertNotIn(secret, serialized)
        self.assertNotIn("rating", result)
        self.assertNotIn("score", result)
        self.assertNotIn("oracle", result)
        self.assertNotIn("expected_location", result)


if __name__ == "__main__":
    unittest.main()
