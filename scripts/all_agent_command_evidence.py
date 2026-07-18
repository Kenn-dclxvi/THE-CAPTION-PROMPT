#!/usr/bin/env python3
"""Materialize attempted and completed command evidence for one all-agent run."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shlex
from pathlib import Path
from typing import Any, Iterable


class AllAgentCommandEvidenceError(Exception):
    pass


SCHEMA_VERSION = "the-caption-prompt.all-agent-command-evidence/v5"
USAGE_SCHEMA_VERSION = "the-caption-prompt.all-agent-usage/v1"


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise AllAgentCommandEvidenceError(f"invalid JSON: {path}") from exc
    if not isinstance(value, dict):
        raise AllAgentCommandEvidenceError(f"JSON root must be an object: {path}")
    return value


def jsonl_items(path: Path) -> Iterable[dict[str, Any]]:
    try:
        with path.open(encoding="utf-8") as handle:
            for line in handle:
                try:
                    item = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if isinstance(item, dict):
                    yield item
    except OSError as exc:
        raise AllAgentCommandEvidenceError(f"cannot read rollout: {path}") from exc


def first_session_meta(path: Path) -> dict[str, Any]:
    for item in jsonl_items(path):
        if item.get("type") == "session_meta" and isinstance(item.get("payload"), dict):
            return item["payload"]
    raise AllAgentCommandEvidenceError(f"rollout has no session_meta: {path}")


def thread_id_from_meta(meta: dict[str, Any]) -> str | None:
    value = meta.get("id") or meta.get("session_id")
    return value if isinstance(value, str) and value else None


def root_command_evidence(events_file: Path, root_thread_id: str) -> dict[str, list[dict[str, Any]]]:
    observed_thread_id: str | None = None
    attempted: list[dict[str, Any]] = []
    successful: list[dict[str, Any]] = []
    failed: list[dict[str, Any]] = []
    protocol_violations: list[dict[str, Any]] = []
    for item in jsonl_items(events_file):
        if item.get("type") == "thread.started" and isinstance(item.get("thread_id"), str):
            observed_thread_id = item["thread_id"]
        if item.get("type") != "item.completed" or not isinstance(item.get("item"), dict):
            continue
        event = item["item"]
        if event.get("type") != "command_execution":
            continue
        command = event.get("command")
        if isinstance(command, str) and command:
            base = {
                "thread_id": root_thread_id,
                "parent_thread_id": None,
                "source": "root_codex_events",
                "command": command,
            }
            attempted.append(base)
            exit_code = event.get("exit_code")
            if isinstance(exit_code, int) and not isinstance(exit_code, bool):
                completed = {**base, "exit_code": exit_code}
                (successful if exit_code == 0 else failed).append(completed)
            else:
                protocol_violations.append(
                    {**base, "reason_code": "missing_machine_bound_exit_code"}
                )
    if observed_thread_id != root_thread_id:
        raise AllAgentCommandEvidenceError(
            "root Codex events thread.started differs from all-agent usage"
        )
    return {
        "attempted_commands": attempted,
        "successful_commands": successful,
        "failed_commands": failed,
        "protocol_violations": protocol_violations,
    }


def root_completed_commands(events_file: Path, root_thread_id: str) -> list[dict[str, Any]]:
    return root_command_evidence(events_file, root_thread_id)["successful_commands"]


def decoded_values(value: Any) -> Iterable[Any]:
    yield value
    if isinstance(value, dict):
        for child in value.values():
            yield from decoded_values(child)
    elif isinstance(value, list):
        for child in value:
            yield from decoded_values(child)
    elif isinstance(value, str):
        try:
            decoded = json.loads(value)
        except json.JSONDecodeError:
            for line in value.splitlines():
                try:
                    decoded_line = json.loads(line)
                except json.JSONDecodeError:
                    continue
                yield from decoded_values(decoded_line)
        else:
            if decoded != value:
                yield from decoded_values(decoded)


def command_result_objects(value: Any, source: str = "") -> Iterable[dict[str, Any]]:
    for candidate in decoded_values(value):
        if isinstance(candidate, dict):
            for name, nested in candidate.items():
                if isinstance(nested, dict):
                    exit_code = nested.get("exit_code", nested.get("exit_status"))
                    if isinstance(exit_code, int) and not isinstance(exit_code, bool):
                        yield {**nested, "name": name, "exit_code": exit_code}
        if isinstance(candidate, dict):
            exit_code = candidate.get("exit_code", candidate.get("exit_status"))
            if isinstance(exit_code, int) and not isinstance(exit_code, bool):
                yield {**candidate, "exit_code": exit_code}
        elif isinstance(candidate, str) and "${r.exit_code}" in source:
            for match in re.finditer(r"\bCHECK\s+(\d+)\s+exit=(-?\d+)\b", candidate):
                yield {
                    "command_index": int(match.group(1)),
                    "exit_code": int(match.group(2)),
                }
            if any(
                marker in source
                for marker in ("${r.name}", "${r.label}", "${name}", "${label}")
            ):
                for match in re.finditer(
                    r"(?:^|\n)([A-Za-z0-9_.-]+):\s*exit=(-?\d+)(?=\n|$)",
                    candidate,
                ):
                    yield {"name": match.group(1), "exit_code": int(match.group(2))}
                for match in re.finditer(
                    r"(?:^|\n)###\s+([A-Za-z0-9_.-]+)\s*\n"
                    r"exit_code=(-?\d+)(?=\n|$)",
                    candidate,
                ):
                    yield {"name": match.group(1), "exit_code": int(match.group(2))}
            exit_match = re.search(r"(?:^|\n)exit_code=(-?\d+)(?:\n|$)", candidate)
            if exit_match is not None:
                yield {"exit_code": int(exit_match.group(1))}
        if isinstance(candidate, str) and re.search(
            r"\$\{[^}]+\.exit_code\}", source
        ):
            for match in re.finditer(
                r"(?:^|\n)COMMAND:\s*(.+?)\nEXIT:\s*(-?\d+)(?=\n|$)",
                candidate,
            ):
                yield {"cmd": match.group(1), "exit_code": int(match.group(2))}


def successful_result_objects(value: Any, source: str = "") -> Iterable[dict[str, Any]]:
    for result in command_result_objects(value, source):
        if result["exit_code"] == 0:
            yield result


def decode_js_string(value: str) -> str:
    if value.startswith('"'):
        try:
            decoded = json.loads(value)
        except json.JSONDecodeError:
            return ""
        return decoded if isinstance(decoded, str) else ""
    if value.startswith("`") and value.endswith("`"):
        return value[1:-1]
    return ""


def command_spec(source: str) -> tuple[list[str], dict[str, str]]:
    literal = r'("(?:\\.|[^"\\])*"|`[^`]*`)'
    cmd_key = r'(?:"cmd"|cmd)'
    name_key = r'(?:"name"|name)'
    commands = [
        decode_js_string(match.group(1))
        for match in re.finditer(rf"{cmd_key}\s*:\s*{literal}", source, re.DOTALL)
    ]
    commands = [command for command in commands if command]
    scalar_command_pattern = re.compile(
        rf"\b(?:const|let|var)\s+cmd\s*=\s*{literal}\s*;",
        re.DOTALL,
    )
    if re.search(r"tools\.exec_command\(\{\s*cmd\b", source):
        commands.extend(
            command
            for command in (
                decode_js_string(match.group(1))
                for match in scalar_command_pattern.finditer(source)
            )
            if command
        )
    by_name: dict[str, str] = {}
    object_pattern = re.compile(
        rf"{name_key}\s*:\s*{literal}\s*,\s*{cmd_key}\s*:\s*{literal}",
        re.DOTALL,
    )
    for match in object_pattern.finditer(source):
        name = decode_js_string(match.group(1))
        command = decode_js_string(match.group(2))
        if name and command:
            by_name[name] = command
    keyed_command_pattern = re.compile(
        rf"\bkey\s*:\s*{literal}.*?{cmd_key}\s*:\s*{literal}",
        re.DOTALL,
    )
    for match in keyed_command_pattern.finditer(source):
        name = decode_js_string(match.group(1))
        command = decode_js_string(match.group(2))
        if name and command:
            by_name[name] = command
    pair_pattern = re.compile(rf"\[\s*{literal}\s*,\s*{literal}\s*\]", re.DOTALL)
    for match in pair_pattern.finditer(source):
        name = decode_js_string(match.group(1))
        command = decode_js_string(match.group(2))
        if name and command:
            by_name[name] = command
    indexed_names = re.search(
        r"\bname\s*:\s*\[(.*?)\]\s*\[\s*i\s*\]",
        source,
        re.DOTALL,
    )
    if indexed_names is not None:
        names = [
            decode_js_string(match.group(1))
            for match in re.finditer(literal, indexed_names.group(1), re.DOTALL)
        ]
        names = [name for name in names if name]
        if len(names) == len(commands):
            by_name.update(zip(names, commands, strict=True))
    assignment_pattern = re.compile(
        r"\b(?:const|let|var)\s+(\w+)\s*=\s*\[(.*?)\]\s*;",
        re.DOTALL,
    )
    argv_entry_pattern = re.compile(
        rf"\[\s*{literal}\s*,\s*\[((?:\s*{literal}\s*,?)+)\]\s*\]",
        re.DOTALL,
    )
    string_pair_entry_pattern = re.compile(
        rf"\[\s*{literal}\s*,\s*{literal}\s*\]",
        re.DOTALL,
    )
    for assignment in assignment_pattern.finditer(source):
        variable = assignment.group(1)
        if re.search(
            rf"(?:\b{re.escape(variable)}\.(?:map|forEach|length)\b|"
            rf"\bof\s+{re.escape(variable)}\b)",
            source,
        ) is None:
            continue
        body = assignment.group(2)
        if commands and "tools.exec_command" in body:
            continue
        argv_entries = list(argv_entry_pattern.finditer(body))
        if argv_entries:
            for entry in argv_entries:
                name = decode_js_string(entry.group(1))
                argv = [
                    decode_js_string(match.group(1))
                    for match in re.finditer(literal, entry.group(2), re.DOTALL)
                ]
                argv = [item for item in argv if item]
                if name and argv:
                    command = shlex.join(argv)
                    by_name[name] = command
                    commands.append(command)
            continue
        string_pair_entries = list(string_pair_entry_pattern.finditer(body))
        if string_pair_entries:
            for entry in string_pair_entries:
                name = decode_js_string(entry.group(1))
                command = decode_js_string(entry.group(2))
                if name and command:
                    by_name[name] = command
                    commands.append(command)
            continue
        assigned_commands = [
            decode_js_string(match.group(1))
            for match in re.finditer(literal, body, re.DOTALL)
        ]
        commands.extend(command for command in assigned_commands if command)
    inline_array_loop = re.compile(
        r"\bfor\s*\([^)]*\bof\s*\[(.*?)\]\s*\)",
        re.DOTALL,
    )
    for loop in inline_array_loop.finditer(source):
        commands.extend(
            command
            for command in (
                decode_js_string(match.group(1))
                for match in re.finditer(literal, loop.group(1), re.DOTALL)
            )
            if command
        )
    commands = list(dict.fromkeys(commands))
    return commands, by_name


def command_for_result(
    result: dict[str, Any],
    source: str,
    commands: list[str],
    by_name: dict[str, str],
) -> str | None:
    explicit = result.get("cmd") or result.get("command")
    if isinstance(explicit, str) and explicit:
        normalized_source = source
        normalized_explicit = explicit
        while "\\\\" in normalized_source:
            normalized_source = normalized_source.replace("\\\\", "\\")
        while "\\\\" in normalized_explicit:
            normalized_explicit = normalized_explicit.replace("\\\\", "\\")
        if normalized_explicit in normalized_source:
            return explicit
        if re.search(r"\b(?:cmd|command)\s*:\s*cmd\b", source):
            return explicit
    name = result.get("name") or result.get("label") or result.get("key")
    if isinstance(name, str) and name in by_name:
        return by_name[name]
    for value in result.values():
        if isinstance(value, str) and value in commands:
            return value
    for key in ("command_index", "check"):
        index = result.get(key)
        if isinstance(index, int) and not isinstance(index, bool) and 1 <= index <= len(commands):
            return commands[index - 1]
    numeric_command = result.get("command")
    if (
        isinstance(numeric_command, int)
        and not isinstance(numeric_command, bool)
        and 1 <= numeric_command <= len(commands)
    ):
        return commands[numeric_command - 1]
    command_number = result.get("command_number")
    if (
        isinstance(command_number, int)
        and not isinstance(command_number, bool)
        and 1 <= command_number <= len(commands)
    ):
        return commands[command_number - 1]
    index = result.get("index")
    if isinstance(index, int) and not isinstance(index, bool) and 0 <= index < len(commands):
        return commands[index]
    if len(commands) == 1:
        return commands[0]
    return None


def output_text(value: Any) -> str:
    return "\n".join(item for item in decoded_values(value) if isinstance(item, str))


def compound_status_commands(command: str, value: Any) -> list[str]:
    """Bind shell subcommands only when the wrapper prints their explicit zero status."""
    bindings: dict[str, str] = {}
    section_bindings: dict[str, str] = {}
    pending_section: str | None = None
    last_command: str | None = None
    for raw_line in command.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        section = re.search(r"\[([A-Za-z0-9_.-]+)\]", line)
        if line.startswith(("printf ", "echo ")) and section is not None:
            pending_section = section.group(1)
            continue
        status_assignment = re.fullmatch(r"([A-Za-z_][A-Za-z0-9_]*)=\$\?", line)
        if status_assignment is not None and last_command is not None:
            name = status_assignment.group(1)
            bindings[name] = last_command
            if name.startswith("status_"):
                bindings[name.removeprefix("status_")] = last_command
            continue
        if line.startswith(("printf ", "echo ")):
            if last_command is not None:
                for marker in re.findall(
                    r"([A-Za-z][A-Za-z0-9_.-]*(?:status|exit|rc))\s*=",
                    line,
                    re.IGNORECASE,
                ):
                    bindings[marker] = last_command
            continue
        if re.match(r"(?:[A-Za-z_][A-Za-z0-9_]*=|set\b|exit\b)", line):
            continue
        last_command = line
        if pending_section is not None:
            section_bindings[pending_section] = line
            pending_section = None
        if "bash -n run.sh" in line:
            for marker in re.findall(
                r"([A-Za-z][A-Za-z0-9_.-]*(?:status|exit|rc))\s*=",
                line,
                re.IGNORECASE,
            ):
                bindings[marker] = "bash -n run.sh"

    observed = output_text(value)
    for marker in re.finditer(
        r"\b([A-Za-z][A-Za-z0-9_.-]*(?:status|exit|rc))\s*=",
        command,
        re.IGNORECASE,
    ):
        for candidate in reversed(command[: marker.start()].splitlines()):
            candidate = candidate.strip()
            if re.match(r"(?:python\d*|git|bash|npm|pytest)\b", candidate):
                bindings[marker.group(1)] = candidate
                if re.match(r"n[A-Z]", marker.group(1)):
                    bindings[marker.group(1)[1:]] = candidate
                break
    successful: list[str] = []
    for marker in re.finditer(r"\b([A-Za-z][A-Za-z0-9_.-]*)=0\b", observed):
        command_for_marker = bindings.get(marker.group(1))
        if command_for_marker is not None:
            successful.append(command_for_marker)
    section_matches = list(re.finditer(r"\[([A-Za-z0-9_.-]+)\]", observed))
    for index, section in enumerate(section_matches):
        end = section_matches[index + 1].start() if index + 1 < len(section_matches) else len(observed)
        block = observed[section.end() : end]
        if re.search(r"(?:^|\n)exit=0(?=\n|$)", block) is None:
            continue
        command_for_section = section_bindings.get(section.group(1))
        if command_for_section is not None:
            successful.append(command_for_section)
    return list(dict.fromkeys(successful))


def descendant_command_evidence(
    rollout_file: Path,
    thread_id: str,
    parent_thread_id: str,
) -> dict[str, list[dict[str, Any]]]:
    meta = first_session_meta(rollout_file)
    if thread_id_from_meta(meta) != thread_id or meta.get("parent_thread_id") != parent_thread_id:
        raise AllAgentCommandEvidenceError(
            f"descendant rollout metadata differs from all-agent usage: {thread_id}"
        )
    rollout = list(jsonl_items(rollout_file))
    calls: dict[str, tuple[str, list[str], dict[str, str]]] = {}
    continuations: dict[str, tuple[int, str]] = {}
    for item in rollout:
        if item.get("type") != "response_item" or not isinstance(item.get("payload"), dict):
            continue
        payload = item["payload"]
        if payload.get("type") not in {"custom_tool_call", "function_call"}:
            continue
        call_id = payload.get("call_id")
        source = payload.get("input") or payload.get("arguments")
        if not isinstance(call_id, str) or not call_id or not isinstance(source, str):
            continue
        if "tools.write_stdin" in source:
            session_match = re.search(r"\bsession_id\s*:\s*(\d+)", source)
            if session_match is not None:
                continuations[call_id] = (int(session_match.group(1)), source)
            continue
        parsed_commands, by_name = command_spec(source)
        if parsed_commands or by_name or "tools.exec_command" in source:
            calls[call_id] = (source, parsed_commands, by_name)
    attempted: list[dict[str, Any]] = []
    successful: list[dict[str, Any]] = []
    failed: list[dict[str, Any]] = []
    unparsed_calls: list[dict[str, Any]] = []
    for call_id, (source, parsed_commands, _) in calls.items():
        if not parsed_commands:
            unparsed_calls.append(
                {
                    "thread_id": thread_id,
                    "parent_thread_id": parent_thread_id,
                    "source": "descendant_rollout_tool_call",
                    "call_id": call_id,
                    "reason_code": "unparsed_exec_command_call",
                }
            )
            continue
        attempted.extend(
            {
                "thread_id": thread_id,
                "parent_thread_id": parent_thread_id,
                "source": "descendant_rollout_tool_call",
                "command": command,
            }
            for command in parsed_commands
        )
    pending_sessions: dict[int, str] = {}
    for item in rollout:
        if item.get("type") != "response_item" or not isinstance(item.get("payload"), dict):
            continue
        payload = item["payload"]
        if payload.get("type") not in {"custom_tool_call_output", "function_call_output"}:
            continue
        call_id = payload.get("call_id")
        if not isinstance(call_id, str):
            continue
        if call_id in continuations:
            session_id, continuation_source = continuations[call_id]
            command = pending_sessions.get(session_id)
            if command is not None:
                for result in command_result_objects(payload.get("output"), continuation_source):
                    completed = {
                        "thread_id": thread_id,
                        "parent_thread_id": parent_thread_id,
                        "source": "descendant_rollout_tool_output",
                        "command": command,
                        "exit_code": result["exit_code"],
                    }
                    (successful if result["exit_code"] == 0 else failed).append(completed)
            continue
        if call_id not in calls:
            continue
        source, parsed_commands, by_name = calls[call_id]
        if len(parsed_commands) == 1:
            for candidate in decoded_values(payload.get("output")):
                if (
                    isinstance(candidate, dict)
                    and isinstance(candidate.get("session_id"), int)
                    and not isinstance(candidate.get("session_id"), bool)
                ):
                    pending_sessions[candidate["session_id"]] = parsed_commands[0]
        seen_for_call: set[str] = set()
        for parsed_command in parsed_commands:
            if "\n" not in parsed_command and ";" not in parsed_command:
                continue
            for command in compound_status_commands(parsed_command, payload.get("output")):
                if command in seen_for_call:
                    continue
                seen_for_call.add(command)
                successful.append(
                    {
                        "thread_id": thread_id,
                        "parent_thread_id": parent_thread_id,
                        "source": "descendant_rollout_tool_output",
                        "command": command,
                        "exit_code": 0,
                    }
                )
        results = list(command_result_objects(payload.get("output"), source))
        indexes = [
            result.get("index")
            for result in results
            if isinstance(result.get("index"), int)
            and not isinstance(result.get("index"), bool)
        ]
        ordered_indexes = (
            len(indexes) == len(parsed_commands)
            and indexes == list(range(indexes[0], indexes[0] + len(indexes)))
        ) if indexes else False
        for result_index, result in enumerate(results):
            command = None
            if ordered_indexes and len(results) == len(parsed_commands):
                command = parsed_commands[result_index]
            if command is None:
                command = command_for_result(result, source, parsed_commands, by_name)
            if command is None and len(results) == len(parsed_commands):
                command = parsed_commands[result_index]
            if command is None or command in seen_for_call:
                continue
            seen_for_call.add(command)
            completed = {
                "thread_id": thread_id,
                "parent_thread_id": parent_thread_id,
                "source": "descendant_rollout_tool_output",
                "command": command,
                "exit_code": result["exit_code"],
            }
            (successful if result["exit_code"] == 0 else failed).append(completed)
    bound = {item["command"] for item in successful + failed}
    protocol_violations = unparsed_calls + [
        {**item, "reason_code": "missing_machine_bound_exit_code"}
        for item in attempted
        if item["command"] not in bound
    ]
    return {
        "attempted_commands": attempted,
        "successful_commands": successful,
        "failed_commands": failed,
        "protocol_violations": protocol_violations,
    }


def descendant_completed_commands(
    rollout_file: Path,
    thread_id: str,
    parent_thread_id: str,
) -> list[dict[str, Any]]:
    return descendant_command_evidence(rollout_file, thread_id, parent_thread_id)[
        "successful_commands"
    ]


def validate_session_graph(usage: dict[str, Any]) -> tuple[str, list[dict[str, Any]]]:
    root_thread_id = usage.get("root_thread_id")
    sessions = usage.get("sessions")
    if not isinstance(root_thread_id, str) or not root_thread_id:
        raise AllAgentCommandEvidenceError("all-agent usage has no root_thread_id")
    if not isinstance(sessions, list) or not sessions or not all(
        isinstance(item, dict) for item in sessions
    ):
        raise AllAgentCommandEvidenceError("all-agent usage has invalid sessions")
    if usage.get("session_count") != len(sessions):
        raise AllAgentCommandEvidenceError("all-agent usage session_count differs from sessions")
    by_thread: dict[str, dict[str, Any]] = {}
    for session in sessions:
        thread_id = session.get("thread_id")
        if not isinstance(thread_id, str) or not thread_id or thread_id in by_thread:
            raise AllAgentCommandEvidenceError("all-agent usage has invalid or duplicate thread_id")
        by_thread[thread_id] = session
    root = by_thread.get(root_thread_id)
    if root is None or root.get("parent_thread_id") is not None:
        raise AllAgentCommandEvidenceError("all-agent usage root session is invalid")
    reachable = {root_thread_id}
    changed = True
    while changed:
        changed = False
        for thread_id, session in by_thread.items():
            if thread_id not in reachable and session.get("parent_thread_id") in reachable:
                reachable.add(thread_id)
                changed = True
    if reachable != set(by_thread):
        raise AllAgentCommandEvidenceError("all-agent usage contains a session outside root descendants")
    return root_thread_id, sessions


def deduplicate(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    unique: list[dict[str, Any]] = []
    for item in items:
        identity = json.dumps(item, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        if identity in seen:
            continue
        seen.add(identity)
        unique.append(item)
    return unique


def command_requirement_statuses(
    report: dict[str, Any], required_groups: list[list[str]]
) -> list[dict[str, Any]]:
    for group in required_groups:
        if not group or not all(isinstance(token, str) and token for token in group):
            raise AllAgentCommandEvidenceError("required command groups must contain strings")
    categories = {
        "attempted": report.get("attempted_commands"),
        "successful": report.get("successful_commands"),
        "failed": report.get("failed_commands"),
    }
    if not all(isinstance(items, list) for items in categories.values()):
        raise AllAgentCommandEvidenceError("command evidence lacks observation arrays")

    def matching_commands(items: list[Any], group: list[str]) -> list[dict[str, Any]]:
        return [
            item
            for item in items
            if isinstance(item, dict)
            and isinstance(item.get("command"), str)
            and all(token in item["command"] for token in group)
        ]

    statuses: list[dict[str, Any]] = []
    for group in required_groups:
        successful = matching_commands(categories["successful"], group)
        failed = matching_commands(categories["failed"], group)
        attempted = matching_commands(categories["attempted"], group)
        if successful:
            status = "successful"
        elif failed:
            status = "failed"
        elif attempted:
            status = "evidence_incomplete"
        else:
            status = "not_attempted"
        statuses.append(
            {
                "required_tokens": group,
                "status": status,
                "attempted_count": len(attempted),
                "successful_count": len(successful),
                "failed_count": len(failed),
                "matching_commands": sorted(
                    {
                        item["command"]
                        for item in attempted + successful + failed
                    }
                ),
            }
        )
    return statuses


def adapter_owned_cleanup_attempts(
    report: dict[str, Any], adapter_owned_paths: list[str]
) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    deletion = re.compile(
        r"(?:^|[\s;&|])(?:sudo\s+)?(?:rm|rmdir)\s|"
        r"(?:unlink|remove|rmtree)\s*\(",
        re.IGNORECASE,
    )
    for item in report.get("attempted_commands", []):
        if not isinstance(item, dict) or not isinstance(item.get("command"), str):
            continue
        matching_paths = [
            path
            for path in adapter_owned_paths
            if path in item["command"]
            or re.search(
                rf"(?:^|[\s'\"]){re.escape(path.rsplit('/', 1)[-1])}(?:$|[\s/'\"])",
                item["command"],
            )
        ]
        if matching_paths and deletion.search(item["command"]):
            attempts.append({**item, "matching_adapter_owned_paths": matching_paths})
    return attempts


def model_reported_adapter_owned_cleanup_attempts(
    events_file: Path, adapter_owned_paths: list[str]
) -> list[dict[str, Any]]:
    """Record model-reported cleanup attempts that may be rejected before tool start."""
    reports: list[dict[str, Any]] = []
    action = re.compile(r"削除|cleanup|remove|delet|rm\s+-", re.IGNORECASE)
    for event in jsonl_items(events_file):
        item = event.get("item")
        if event.get("type") != "item.completed" or not isinstance(item, dict):
            continue
        text = item.get("text")
        if item.get("type") != "agent_message" or not isinstance(text, str):
            continue
        matching_paths = [
            path
            for path in adapter_owned_paths
            if path in text or path.rsplit("/", 1)[-1] in text
        ]
        if not matching_paths or action.search(text) is None:
            continue
        reports.append(
            {
                "source": "root_agent_message",
                "matching_adapter_owned_paths": matching_paths,
                "text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
            }
        )
    return reports


def collect(usage_path: Path, root_events: Path) -> dict[str, Any]:
    usage = load_json(usage_path)
    if usage.get("schema_version") != USAGE_SCHEMA_VERSION:
        raise AllAgentCommandEvidenceError("all-agent usage uses an unsupported schema_version")
    run_id = usage.get("run_id")
    if not isinstance(run_id, str) or not run_id:
        raise AllAgentCommandEvidenceError("all-agent usage has no run_id")
    root_thread_id, sessions = validate_session_graph(usage)
    evidence = root_command_evidence(root_events, root_thread_id)
    session_sources: list[dict[str, Any]] = []
    for session in sessions:
        thread_id = session["thread_id"]
        parent_thread_id = session.get("parent_thread_id")
        rollout_file = session.get("rollout_file")
        if not isinstance(rollout_file, str) or not rollout_file:
            raise AllAgentCommandEvidenceError(f"session has no rollout_file: {thread_id}")
        session_sources.append(
            {
                "thread_id": thread_id,
                "parent_thread_id": parent_thread_id,
                "rollout_file": rollout_file,
            }
        )
        if thread_id == root_thread_id:
            continue
        if not isinstance(parent_thread_id, str) or not parent_thread_id:
            raise AllAgentCommandEvidenceError(f"descendant has no parent_thread_id: {thread_id}")
        descendant = descendant_command_evidence(
            Path(rollout_file), thread_id, parent_thread_id
        )
        for key in (
            "attempted_commands",
            "successful_commands",
            "failed_commands",
            "protocol_violations",
        ):
            evidence[key].extend(descendant[key])
    for key in (
        "attempted_commands",
        "successful_commands",
        "failed_commands",
        "protocol_violations",
    ):
        evidence[key] = deduplicate(evidence[key])
    return {
        "schema_version": SCHEMA_VERSION,
        "run_id": run_id,
        "root_thread_id": root_thread_id,
        "session_count": len(sessions),
        "session_sources": session_sources,
        "attempted_command_count": len(evidence["attempted_commands"]),
        "attempted_commands": evidence["attempted_commands"],
        "successful_command_count": len(evidence["successful_commands"]),
        "successful_commands": evidence["successful_commands"],
        "failed_command_count": len(evidence["failed_commands"]),
        "failed_commands": evidence["failed_commands"],
        "protocol_violation_count": len(evidence["protocol_violations"]),
        "protocol_violations": evidence["protocol_violations"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--usage", type=Path, required=True)
    parser.add_argument("--root-events", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        report = collect(args.usage.resolve(), args.root_events.resolve())
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("x", encoding="utf-8") as handle:
            json.dump(report, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
    except (AllAgentCommandEvidenceError, FileExistsError) as exc:
        print(f"error: {exc}")
        return 2
    print(json.dumps({"artifact": str(args.output), "run_id": report["run_id"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
