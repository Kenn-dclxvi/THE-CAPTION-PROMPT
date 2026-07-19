#!/usr/bin/env python3
"""Build a diagnostic-only provenance view for path:line response claims."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any, Iterable


SCHEMA_VERSION = "the-caption-prompt.response-claim-trace/v1"
COLLECTOR_REVISION = "response-claim-trace/v2"

PATH_LINE_PATTERN = re.compile(
    r"(?P<path>(?:[A-Za-z0-9_.-]+/)+[A-Za-z0-9_.-]+\.[A-Za-z0-9_.-]+)"
    r":(?P<line>[1-9][0-9]*)(?:-(?P<end>[1-9][0-9]*))?"
)
FILE_PATH_PATTERN = re.compile(
    r"(?P<path>(?:[A-Za-z0-9_.-]+/)+[A-Za-z0-9_.-]+\.[A-Za-z0-9_.-]+)"
)
HUNK_PATTERN = re.compile(
    r"^@@ -(?P<old>[0-9]+)(?:,[0-9]+)? \+(?P<new>[0-9]+)(?:,[0-9]+)? @@"
)
NUMBERED_LINE_PATTERN = re.compile(r"^\s*(?P<line>[1-9][0-9]*)\s+(?P<text>.*)$")
GREP_LINE_PATTERN = re.compile(
    r"^(?:[^:\n]+:)?"
    r"(?P<path>(?:[A-Za-z0-9_.-]+/)+[A-Za-z0-9_.-]+\.[A-Za-z0-9_.-]+)"
    r":(?P<line>[1-9][0-9]*):(?P<text>.*)$"
)
REPOSITORY_PREFIXES = (
    ".github/",
    "automation/",
    "configs/",
    "docs/",
    "evaluations/",
    "scripts/",
    "src/",
    "tests/",
)


class ResponseClaimTraceError(Exception):
    pass


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def text_descriptor(value: str) -> dict[str, Any]:
    encoded = value.encode("utf-8")
    return {"bytes": len(encoded), "sha256": sha256_bytes(encoded)}


def normalize_path(value: str) -> str:
    normalized = value.replace("\\", "/").lstrip("./")
    for prefix in REPOSITORY_PREFIXES:
        marker = f"/{prefix}"
        if marker in normalized:
            return prefix + normalized.rsplit(marker, 1)[1]
        if normalized.startswith(prefix):
            return normalized
    return normalized


def extract_paths(value: str) -> list[str]:
    return sorted(
        {
            normalize_path(match.group("path"))
            for match in FILE_PATH_PATTERN.finditer(value)
        }
    )


def jsonl_objects(path: Path) -> Iterable[tuple[int, dict[str, Any]]]:
    try:
        with path.open(encoding="utf-8") as handle:
            for sequence, raw in enumerate(handle, start=1):
                try:
                    value = json.loads(raw)
                except json.JSONDecodeError:
                    continue
                if isinstance(value, dict):
                    yield sequence, value
    except OSError as exc:
        raise ResponseClaimTraceError(f"cannot read events: {path}") from exc


def command_representation(command: str, output: str, paths: list[str]) -> str:
    if "git diff " in command and "diff --git " in output:
        return "unified_diff"
    if any(marker in command for marker in ("nl -ba", "git grep -n", "rg -n", "grep -n")):
        return "numbered_source"
    if paths and any(marker in command for marker in ("git show", "sed -n", "cat ")):
        return "unnumbered_source"
    return "other"


def diff_anchors(output: str) -> list[dict[str, Any]]:
    anchors: list[dict[str, Any]] = []
    current_path: str | None = None
    new_line: int | None = None
    for raw in output.splitlines():
        if raw.startswith("+++ b/"):
            current_path = normalize_path(raw[6:])
            continue
        hunk = HUNK_PATTERN.match(raw)
        if hunk is not None:
            new_line = int(hunk.group("new"))
            continue
        if current_path is None or new_line is None:
            continue
        if raw.startswith("+") and not raw.startswith("+++"):
            anchors.append(
                {
                    "kind": "changed_line",
                    "line": new_line,
                    "path": current_path,
                    "text_sha256": sha256_bytes(raw[1:].encode("utf-8")),
                }
            )
            new_line += 1
        elif raw.startswith("-") and not raw.startswith("---"):
            continue
        elif raw.startswith(" "):
            new_line += 1
        elif raw.startswith("\\"):
            continue
        else:
            new_line = None
    return anchors


def numbered_anchors(
    command: str, output: str, target_paths: list[str]
) -> list[dict[str, Any]]:
    anchors: list[dict[str, Any]] = []
    for raw in output.splitlines():
        grep_match = GREP_LINE_PATTERN.match(raw)
        if grep_match is not None:
            anchors.append(
                {
                    "kind": "numbered_line",
                    "line": int(grep_match.group("line")),
                    "path": normalize_path(grep_match.group("path")),
                    "text_sha256": sha256_bytes(
                        grep_match.group("text").encode("utf-8")
                    ),
                }
            )
            continue
        numbered_match = NUMBERED_LINE_PATTERN.match(raw)
        if numbered_match is None or len(target_paths) != 1:
            continue
        anchors.append(
            {
                "kind": "numbered_line",
                "line": int(numbered_match.group("line")),
                "path": target_paths[0],
                "text_sha256": sha256_bytes(
                    numbered_match.group("text").encode("utf-8")
                ),
            }
        )
    return anchors


def response_claims(text: str) -> list[dict[str, Any]]:
    claims: list[dict[str, Any]] = []
    seen: set[tuple[str, int, int | None]] = set()
    for match in PATH_LINE_PATTERN.finditer(text):
        end = int(match.group("end")) if match.group("end") else None
        key = (normalize_path(match.group("path")), int(match.group("line")), end)
        if key in seen:
            continue
        seen.add(key)
        claims.append({"end_line": end, "line": key[1], "path": key[0]})
    return claims


def alignment_for_claim(
    claim: dict[str, Any], observations: list[dict[str, Any]]
) -> dict[str, Any]:
    changed_lines = sorted(
        {
            anchor["line"]
            for observation in observations
            if observation["sequence"] < claim["message_sequence"]
            and observation.get("representation") == "unified_diff"
            for anchor in observation.get("line_anchors", [])
            if anchor.get("kind") == "changed_line"
            and anchor.get("path") == claim["path"]
            and isinstance(anchor.get("line"), int)
        }
    )
    if not changed_lines:
        return {
            "claim_sequence": claim["message_sequence"],
            "delta": None,
            "observed_changed_line": None,
            "path": claim["path"],
            "status": "none",
        }
    closest = min(changed_lines, key=lambda line: (abs(claim["line"] - line), line))
    delta = claim["line"] - closest
    return {
        "claim_sequence": claim["message_sequence"],
        "delta": delta,
        "observed_changed_line": closest,
        "path": claim["path"],
        "status": "exact" if delta == 0 else ("adjacent" if abs(delta) == 1 else "none"),
    }


def collect(
    events_path: Path,
    *,
    run_id: str,
    case_id: str,
    iteration: int,
) -> dict[str, Any]:
    raw_events = events_path.read_bytes()
    completed: list[tuple[int, dict[str, Any]]] = []
    for sequence, event in jsonl_objects(events_path):
        item = event.get("item")
        if event.get("type") == "item.completed" and isinstance(item, dict):
            completed.append((sequence, item))

    message_sequences = [
        sequence
        for sequence, item in completed
        if item.get("type") == "agent_message" and isinstance(item.get("text"), str)
    ]
    final_message_sequence = message_sequences[-1] if message_sequences else None

    observations: list[dict[str, Any]] = []
    claims: list[dict[str, Any]] = []
    first_seen: dict[tuple[str, int, int | None], int] = {}
    for sequence, item in completed:
        item_type = item.get("type")
        item_id = item.get("id") if isinstance(item.get("id"), str) else None
        if item_type == "command_execution":
            command = item.get("command") if isinstance(item.get("command"), str) else ""
            output = (
                item.get("aggregated_output")
                if isinstance(item.get("aggregated_output"), str)
                else ""
            )
            paths = extract_paths(command)
            representation = command_representation(command, output, paths)
            anchors = (
                diff_anchors(output)
                if representation == "unified_diff"
                else numbered_anchors(command, output, paths)
                if representation == "numbered_source"
                else []
            )
            observations.append(
                {
                    "command_sha256": sha256_bytes(command.encode("utf-8")),
                    "item_id": item_id,
                    "kind": "command",
                    "line_anchors": anchors,
                    "output_bytes": len(output.encode("utf-8")),
                    "output_sha256": sha256_bytes(output.encode("utf-8")),
                    "representation": representation,
                    "sequence": sequence,
                    "target_paths": paths,
                }
            )
        elif item_type == "agent_message" and isinstance(item.get("text"), str):
            text = item["text"]
            message_kind = (
                "terminal" if sequence == final_message_sequence else "intermediate"
            )
            parsed = response_claims(text)
            observations.append(
                {
                    "item_id": item_id,
                    "kind": "agent_message",
                    "line_anchors": [],
                    "message_kind": message_kind,
                    "output_bytes": len(text.encode("utf-8")),
                    "output_sha256": sha256_bytes(text.encode("utf-8")),
                    "representation": message_kind,
                    "sequence": sequence,
                    "target_paths": sorted({claim["path"] for claim in parsed}),
                }
            )
            for parsed_claim in parsed:
                key = (
                    parsed_claim["path"],
                    parsed_claim["line"],
                    parsed_claim["end_line"],
                )
                first_seen.setdefault(key, sequence)
                direct_sequences = sorted(
                    {
                        observation["sequence"]
                        for observation in observations
                        if observation["sequence"] < sequence
                        and observation.get("representation") == "numbered_source"
                        for anchor in observation.get("line_anchors", [])
                        if anchor.get("path") == parsed_claim["path"]
                        and anchor.get("line") == parsed_claim["line"]
                    }
                )
                claims.append(
                    {
                        **parsed_claim,
                        "direct_coordinate_observation_sequences": direct_sequences,
                        "first_seen_sequence": first_seen[key],
                        "item_id": item_id,
                        "message_kind": message_kind,
                        "message_sequence": sequence,
                        "message_sha256": sha256_bytes(text.encode("utf-8")),
                    }
                )

    return {
        "case_id": case_id,
        "claim_alignment": [alignment_for_claim(claim, observations) for claim in claims],
        "collector_revision": COLLECTOR_REVISION,
        "iteration": iteration,
        "observations": observations,
        "response_claims": claims,
        "run_id": run_id,
        "schema_version": SCHEMA_VERSION,
        "source_artifacts": [
            {
                "bytes": len(raw_events),
                "kind": "root_codex_events",
                "sha256": sha256_bytes(raw_events),
            }
        ],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--events", required=True, type=Path)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--case-id", required=True)
    parser.add_argument("--iteration", required=True, type=int)
    parser.add_argument("--output", required=True, type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.run_id or not args.case_id or args.iteration < 1:
        raise ResponseClaimTraceError("run binding is invalid")
    result = collect(
        args.events,
        run_id=args.run_id,
        case_id=args.case_id,
        iteration=args.iteration,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
