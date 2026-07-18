#!/usr/bin/env python3
"""Materialize successful command evidence from one root Codex run and its descendants."""

from __future__ import annotations

import argparse
import json
import re
import shlex
from pathlib import Path
from typing import Any, Iterable


class AllAgentCommandEvidenceError(Exception):
    pass


SCHEMA_VERSION = "the-caption-prompt.all-agent-command-evidence/v4"
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


def root_completed_commands(events_file: Path, root_thread_id: str) -> list[dict[str, Any]]:
    observed_thread_id: str | None = None
    commands: list[dict[str, Any]] = []
    for item in jsonl_items(events_file):
        if item.get("type") == "thread.started" and isinstance(item.get("thread_id"), str):
            observed_thread_id = item["thread_id"]
        if item.get("type") != "item.completed" or not isinstance(item.get("item"), dict):
            continue
        event = item["item"]
        if event.get("type") != "command_execution" or event.get("exit_code") != 0:
            continue
        command = event.get("command")
        if isinstance(command, str) and command:
            commands.append(
                {
                    "thread_id": root_thread_id,
                    "parent_thread_id": None,
                    "source": "root_codex_events",
                    "command": command,
                    "exit_code": 0,
                }
            )
    if observed_thread_id != root_thread_id:
        raise AllAgentCommandEvidenceError(
            "root Codex events thread.started differs from all-agent usage"
        )
    return commands


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


def successful_result_objects(value: Any, source: str = "") -> Iterable[dict[str, Any]]:
    for candidate in decoded_values(value):
        if isinstance(candidate, dict) and candidate.get("exit_code") == 0:
            yield candidate
        elif isinstance(candidate, str) and "${r.exit_code}" in source:
            for match in re.finditer(r"\bCHECK\s+(\d+)\s+exit=0\b", candidate):
                yield {"command_index": int(match.group(1)), "exit_code": 0}
            if "${r.name}" in source or "${r.label}" in source:
                for match in re.finditer(
                    r"(?:^|\n)([A-Za-z0-9_.-]+):\s*exit=0(?=\n|$)",
                    candidate,
                ):
                    yield {"name": match.group(1), "exit_code": 0}
                for match in re.finditer(
                    r"(?:^|\n)###\s+([A-Za-z0-9_.-]+)\s*\n"
                    r"exit_code=0(?=\n|$)",
                    candidate,
                ):
                    yield {"name": match.group(1), "exit_code": 0}
            if re.search(r"(?:^|\n)exit_code=0(?:\n|$)", candidate):
                yield {"exit_code": 0}


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
    commands = [
        decode_js_string(match.group(1))
        for match in re.finditer(rf"\bcmd\s*:\s*{literal}", source, re.DOTALL)
    ]
    commands = [command for command in commands if command]
    by_name: dict[str, str] = {}
    object_pattern = re.compile(
        rf"\bname\s*:\s*{literal}\s*,\s*\bcmd\s*:\s*{literal}",
        re.DOTALL,
    )
    for match in object_pattern.finditer(source):
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
    for assignment in assignment_pattern.finditer(source):
        variable = assignment.group(1)
        if re.search(rf"\b{re.escape(variable)}\.(?:map|forEach)\b", source) is None:
            continue
        body = assignment.group(2)
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
        assigned_commands = [
            decode_js_string(match.group(1))
            for match in re.finditer(literal, body, re.DOTALL)
        ]
        commands.extend(command for command in assigned_commands if command)
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
    name = result.get("name") or result.get("label")
    if isinstance(name, str) and name in by_name:
        return by_name[name]
    for value in result.values():
        if isinstance(value, str) and value in commands:
            return value
    for key in ("command_index", "check"):
        index = result.get(key)
        if isinstance(index, int) and not isinstance(index, bool) and 1 <= index <= len(commands):
            return commands[index - 1]
    index = result.get("index")
    if isinstance(index, int) and not isinstance(index, bool) and 0 <= index < len(commands):
        return commands[index]
    if len(commands) == 1:
        return commands[0]
    return None


def descendant_completed_commands(
    rollout_file: Path,
    thread_id: str,
    parent_thread_id: str,
) -> list[dict[str, Any]]:
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
    commands: list[dict[str, Any]] = []
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
            if any(successful_result_objects(payload.get("output"), continuation_source)):
                command = pending_sessions.get(session_id)
                if command is not None:
                    commands.append(
                        {
                            "thread_id": thread_id,
                            "parent_thread_id": parent_thread_id,
                            "source": "descendant_rollout_tool_output",
                            "command": command,
                            "exit_code": 0,
                        }
                    )
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
        successful_results = list(successful_result_objects(payload.get("output"), source))
        indexes = [
            result.get("index")
            for result in successful_results
            if isinstance(result.get("index"), int)
            and not isinstance(result.get("index"), bool)
        ]
        one_based_indexes = (
            len(indexes) == len(parsed_commands)
            and set(indexes) == set(range(1, len(parsed_commands) + 1))
        )
        for result_index, result in enumerate(successful_results):
            if one_based_indexes and "index" in result:
                result = {**result, "command_index": result["index"]}
                del result["index"]
            command = command_for_result(result, source, parsed_commands, by_name)
            if command is None and len(successful_results) == len(parsed_commands):
                command = parsed_commands[result_index]
            if command is None or command in seen_for_call:
                continue
            seen_for_call.add(command)
            commands.append(
                {
                    "thread_id": thread_id,
                    "parent_thread_id": parent_thread_id,
                    "source": "descendant_rollout_tool_output",
                    "command": command,
                    "exit_code": 0,
                }
            )
    return commands


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


def collect(usage_path: Path, root_events: Path) -> dict[str, Any]:
    usage = load_json(usage_path)
    if usage.get("schema_version") != USAGE_SCHEMA_VERSION:
        raise AllAgentCommandEvidenceError("all-agent usage uses an unsupported schema_version")
    run_id = usage.get("run_id")
    if not isinstance(run_id, str) or not run_id:
        raise AllAgentCommandEvidenceError("all-agent usage has no run_id")
    root_thread_id, sessions = validate_session_graph(usage)
    commands = root_completed_commands(root_events, root_thread_id)
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
        commands.extend(
            descendant_completed_commands(Path(rollout_file), thread_id, parent_thread_id)
        )
    return {
        "schema_version": SCHEMA_VERSION,
        "run_id": run_id,
        "root_thread_id": root_thread_id,
        "session_count": len(sessions),
        "session_sources": session_sources,
        "successful_command_count": len(commands),
        "successful_commands": commands,
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
