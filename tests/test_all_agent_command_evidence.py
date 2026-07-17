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

    def test_collects_named_argv_commands_from_bound_descendant(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            usage, root_events = self.fixture(root)
            write_jsonl(
                root / "child.jsonl",
                [
                    {
                        "type": "session_meta",
                        "payload": {"id": "child", "parent_thread_id": "root"},
                    },
                    {
                        "type": "response_item",
                        "payload": {
                            "type": "custom_tool_call",
                            "name": "exec",
                            "call_id": "named-argv-call",
                            "input": (
                                "const cmds = [[\"static_validation\", "
                                "[\"python3\", \"-c\", \"assert True\"]], "
                                "[\"diff_check\", [\"git\", \"diff\", \"--check\"]]];"
                                "const results = await Promise.all(cmds.map(async "
                                "([label, argv]) => { const r = await tools.exec_command({"
                                "cmd: argv.join(\" \"), workdir: \"/tmp\"}); "
                                "return {label, exit_code: r.exit_code}; }));"
                                "results.forEach(r => text(JSON.stringify(r)));"
                            ),
                        },
                    },
                    {
                        "type": "response_item",
                        "payload": {
                            "type": "custom_tool_call_output",
                            "call_id": "named-argv-call",
                            "output": [
                                {
                                    "type": "input_text",
                                    "text": json.dumps(
                                        {"label": "static_validation", "exit_code": 0}
                                    ),
                                },
                                {
                                    "type": "input_text",
                                    "text": json.dumps(
                                        {"label": "diff_check", "exit_code": 1}
                                    ),
                                },
                            ],
                        },
                    },
                ],
            )

            report = collect(usage, root_events)
            commands = [item["command"] for item in report["successful_commands"]]

            self.assertIn("python3 -c 'assert True'", commands)
            self.assertNotIn("git diff --check", commands)

    def test_binds_named_plain_text_results_from_parallel_exec_wrapper(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            usage, root_events = self.fixture(root)
            write_jsonl(
                root / "child.jsonl",
                [
                    {
                        "type": "session_meta",
                        "payload": {"id": "child", "parent_thread_id": "root"},
                    },
                    {
                        "type": "response_item",
                        "payload": {
                            "type": "custom_tool_call",
                            "name": "exec",
                            "call_id": "plain-text-results-call",
                            "input": (
                                "const commands = [[\"static_validation\", \"python3 validation\"], "
                                "[\"diff_check\", \"git diff --check\"], "
                                "[\"diff_name_only\", \"git diff --name-only\"]];"
                                "const results = await Promise.all(commands.map(async ([name, cmd]) => {"
                                "const r = await tools.exec_command({cmd});"
                                "return {name, exit_code: r.exit_code, output: r.output}; }));"
                                "for (const r of results) {"
                                "text(`${r.name}: exit=${r.exit_code}\\n${r.output}`); }"
                            ),
                        },
                    },
                    {
                        "type": "response_item",
                        "payload": {
                            "type": "custom_tool_call_output",
                            "call_id": "plain-text-results-call",
                            "output": [
                                {
                                    "type": "input_text",
                                    "text": (
                                        "Script completed\nWall time 0.2 seconds\nOutput:\n"
                                        "static_validation: exit=0\n"
                                        "diff_check: exit=0\n"
                                        "diff_name_only: exit=1\nrequirements.in\n"
                                    ),
                                }
                            ],
                        },
                    },
                ],
            )

            report = collect(usage, root_events)
            commands = [item["command"] for item in report["successful_commands"]]

            self.assertIn("python3 validation", commands)
            self.assertIn("git diff --check", commands)
            self.assertNotIn("git diff --name-only", commands)

    def test_binds_completed_continuation_to_original_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            usage, root_events = self.fixture(root)
            write_jsonl(
                root / "child.jsonl",
                [
                    {
                        "type": "session_meta",
                        "payload": {"id": "child", "parent_thread_id": "root"},
                    },
                    {
                        "type": "response_item",
                        "payload": {
                            "type": "custom_tool_call",
                            "call_id": "start-call",
                            "input": (
                                "const r = await tools.exec_command({"
                                "cmd: \"bash scripts/dev/main_verify.sh\"});"
                                "text(JSON.stringify(r));"
                            ),
                        },
                    },
                    {
                        "type": "response_item",
                        "payload": {
                            "type": "custom_tool_call_output",
                            "call_id": "start-call",
                            "output": json.dumps({"session_id": 65481}),
                        },
                    },
                    {
                        "type": "response_item",
                        "payload": {
                            "type": "custom_tool_call",
                            "call_id": "wait-call",
                            "input": (
                                "const r = await tools.write_stdin({"
                                "session_id: 65481, chars: \"\"});"
                                "text(JSON.stringify(r));"
                            ),
                        },
                    },
                    {
                        "type": "response_item",
                        "payload": {
                            "type": "custom_tool_call_output",
                            "call_id": "wait-call",
                            "output": json.dumps({"exit_code": 0}),
                        },
                    },
                ],
            )

            report = collect(usage, root_events)
            commands = [item["command"] for item in report["successful_commands"]]

            self.assertIn("bash scripts/dev/main_verify.sh", commands)

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

    def test_binds_one_based_output_index_to_ordered_commands(self) -> None:
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
                            "call_id": "one-based-call",
                            "input": (
                                "const results = await Promise.all(["
                                "tools.exec_command({cmd: \"python3 validation\"}),"
                                "tools.exec_command({cmd: \"git diff --check\"})]);"
                            ),
                        },
                    },
                    {
                        "type": "response_item",
                        "payload": {
                            "type": "custom_tool_call_output",
                            "call_id": "one-based-call",
                            "output": [
                                {
                                    "type": "input_text",
                                    "text": json.dumps({"index": 1, "exit_code": 0}),
                                },
                                {
                                    "type": "input_text",
                                    "text": json.dumps({"index": 2, "exit_code": 0}),
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

    def test_accepts_runtime_command_returned_by_same_tool_result(self) -> None:
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
                            "call_id": "runtime-command-call",
                            "input": (
                                "const cmd = `python3 -c ${JSON.stringify(code)}`;"
                                "const r = await tools.exec_command({cmd});"
                                "text({command: cmd, exit_code: r.exit_code});"
                            ),
                        },
                    },
                    {
                        "type": "response_item",
                        "payload": {
                            "type": "custom_tool_call_output",
                            "call_id": "runtime-command-call",
                            "output": json.dumps(
                                {"command": "python3 -c \"assert True\"", "exit_code": 0}
                            ),
                        },
                    },
                ],
            )

            report = collect(usage, root_events)
            commands = [item["command"] for item in report["successful_commands"]]
            self.assertIn('python3 -c "assert True"', commands)


if __name__ == "__main__":
    unittest.main()
