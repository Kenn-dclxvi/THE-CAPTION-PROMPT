from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.all_agent_command_evidence import (
    AllAgentCommandEvidenceError,
    collect,
)


def write_jsonl(path: Path, items: list[dict]) -> None:
    path.write_text("".join(json.dumps(item) + "\n" for item in items), encoding="utf-8")


class AllAgentCommandEvidenceTest(unittest.TestCase):
    def fixture(self, root: Path) -> tuple[Path, Path]:
        root_rollout = root / "root.jsonl"
        child_rollout = root / "child.jsonl"
        unrelated_rollout = root / "unrelated.jsonl"
        write_jsonl(
            root_rollout,
            [{"type": "session_meta", "payload": {"id": "root", "parent_thread_id": None}}],
        )
        write_jsonl(
            child_rollout,
            [
                {
                    "type": "session_meta",
                    "payload": {"id": "child", "parent_thread_id": "root"},
                },
                {
                    "type": "response_item",
                    "payload": {
                        "type": "custom_tool_call",
                        "call_id": "child-call",
                        "input": "const jobs = [{name:\"diff\", cmd:\"git diff --check\"}, {name:\"test\", cmd:\"pytest tests\"}];",
                    },
                },
                {
                    "type": "response_item",
                    "payload": {
                        "type": "custom_tool_call_output",
                        "call_id": "child-call",
                        "output": [
                            {
                                "type": "input_text",
                                "text": json.dumps(
                                    {"name": "diff", "exit_code": 0, "output": ""}
                                ),
                            },
                            {
                                "type": "input_text",
                                "text": json.dumps(
                                    {"name": "test", "exit_code": 1, "output": "failed"}
                                ),
                            },
                        ],
                    },
                },
            ],
        )
        write_jsonl(
            unrelated_rollout,
            [
                {
                    "type": "session_meta",
                    "payload": {"id": "unrelated", "parent_thread_id": None},
                },
                {
                    "type": "response_item",
                    "payload": {
                        "type": "custom_tool_call_output",
                        "output": json.dumps({"cmd": "must-not-appear", "exit_code": 0}),
                    },
                },
            ],
        )
        usage = root / "usage.json"
        usage.write_text(
            json.dumps(
                {
                    "schema_version": "the-caption-prompt.all-agent-usage/v1",
                    "run_id": "run-1",
                    "root_thread_id": "root",
                    "session_count": 2,
                    "sessions": [
                        {
                            "thread_id": "root",
                            "parent_thread_id": None,
                            "rollout_file": str(root_rollout),
                        },
                        {
                            "thread_id": "child",
                            "parent_thread_id": "root",
                            "rollout_file": str(child_rollout),
                        },
                    ],
                }
            ),
            encoding="utf-8",
        )
        root_events = root / "codex-events.jsonl"
        write_jsonl(
            root_events,
            [
                {"type": "thread.started", "thread_id": "root"},
                {
                    "type": "item.completed",
                    "item": {
                        "type": "command_execution",
                        "command": "bash -n run.sh",
                        "exit_code": 0,
                    },
                },
                {
                    "type": "item.completed",
                    "item": {
                        "type": "command_execution",
                        "command": "false",
                        "exit_code": 1,
                    },
                },
            ],
        )
        return usage, root_events

    def test_collects_successful_root_and_bound_descendant_commands_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            usage, root_events = self.fixture(Path(tmp))
            report = collect(usage, root_events)
            commands = [item["command"] for item in report["successful_commands"]]

            self.assertEqual(report["run_id"], "run-1")
            self.assertEqual(report["session_count"], 2)
            self.assertEqual(commands, ["bash -n run.sh", "git diff --check"])
            self.assertNotIn("pytest tests", commands)
            self.assertNotIn("must-not-appear", commands)

    def test_rejects_descendant_metadata_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            usage, root_events = self.fixture(Path(tmp))
            data = json.loads(usage.read_text())
            data["sessions"][1]["parent_thread_id"] = "different-parent"
            usage.write_text(json.dumps(data), encoding="utf-8")

            with self.assertRaisesRegex(
                AllAgentCommandEvidenceError,
                "outside root descendants",
            ):
                collect(usage, root_events)

    def test_rejects_root_event_thread_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            usage, root_events = self.fixture(Path(tmp))
            write_jsonl(root_events, [{"type": "thread.started", "thread_id": "other"}])

            with self.assertRaisesRegex(
                AllAgentCommandEvidenceError,
                "thread.started differs",
            ):
                collect(usage, root_events)

    def test_binds_indexed_output_names_to_ordered_commands(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            usage, root_events = self.fixture(root)
            child = root / "child.jsonl"
            write_jsonl(
                child,
                [
                    {
                        "type": "session_meta",
                        "payload": {"id": "child", "parent_thread_id": "root"},
                    },
                    {
                        "type": "response_item",
                        "payload": {
                            "type": "custom_tool_call",
                            "call_id": "indexed-call",
                            "input": (
                                "const results = await Promise.all(["
                                "tools.exec_command({cmd: `python3 validation`}),"
                                "tools.exec_command({cmd: `git diff --check`})]);"
                                "results.forEach((r, i) => text(JSON.stringify({"
                                "name: [\"static_validation\", \"diff_check\"][i],"
                                "exit_code: r.exit_code})));"
                            ),
                        },
                    },
                    {
                        "type": "response_item",
                        "payload": {
                            "type": "custom_tool_call_output",
                            "call_id": "indexed-call",
                            "output": [
                                {
                                    "type": "input_text",
                                    "text": json.dumps(
                                        {"name": "static_validation", "exit_code": 0}
                                    ),
                                },
                                {
                                    "type": "input_text",
                                    "text": json.dumps({"name": "diff_check", "exit_code": 0}),
                                },
                            ],
                        },
                    },
                ],
            )

            report = collect(usage, root_events)
            commands = [item["command"] for item in report["successful_commands"]]
            self.assertIn("python3 validation", commands)
            self.assertIn("git diff --check", commands)

    def test_binds_zero_based_output_index_to_ordered_commands(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            usage, root_events = self.fixture(root)
            child = root / "child.jsonl"
            write_jsonl(
                child,
                [
                    {
                        "type": "session_meta",
                        "payload": {"id": "child", "parent_thread_id": "root"},
                    },
                    {
                        "type": "response_item",
                        "payload": {
                            "type": "custom_tool_call",
                            "call_id": "zero-based-call",
                            "input": (
                                "const results = await Promise.all(["
                                "tools.exec_command({cmd: \"git diff --check\"}),"
                                "tools.exec_command({cmd: \"git diff --name-only\"})]);"
                            ),
                        },
                    },
                    {
                        "type": "response_item",
                        "payload": {
                            "type": "custom_tool_call_output",
                            "call_id": "zero-based-call",
                            "output": [
                                {
                                    "type": "input_text",
                                    "text": json.dumps({"index": 0, "exit_code": 0}),
                                },
                                {
                                    "type": "input_text",
                                    "text": json.dumps({"index": 1, "exit_code": 0}),
                                },
                            ],
                        },
                    },
                ],
            )

            report = collect(usage, root_events)
            commands = [item["command"] for item in report["successful_commands"]]
            self.assertIn("git diff --check", commands)
            self.assertIn("git diff --name-only", commands)


if __name__ == "__main__":
    unittest.main()
