#!/usr/bin/env python3
"""Backfill all-agent token evidence for append-only v3 root-only results."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from all_agent_usage import AllAgentUsageError, index_sessions, summarize_workspace_usage
except ModuleNotFoundError:
    from scripts.all_agent_usage import AllAgentUsageError, index_sessions, summarize_workspace_usage


class BackfillError(Exception):
    pass


def load_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        raise BackfillError(f"invalid JSON: {path}") from exc
    if not isinstance(value, dict):
        raise BackfillError(f"JSON root must be an object: {path}")
    return value


def write_once(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("x", encoding="utf-8", newline="\n") as handle:
            json.dump(value, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
    except FileExistsError as exc:
        raise BackfillError(f"refusing to overwrite: {path}") from exc


def workspace_run_id(cwd: str) -> str | None:
    path = Path(cwd)
    if path.name != "workspace" or path.parent.parent.name != "evidence":
        return None
    return path.parent.name


def backfill(registry: Path, session_root: Path, output: Path) -> dict[str, Any]:
    source_results = []
    run_tokens: dict[str, int] = {}
    for path in sorted((registry / "results").glob("*.json")):
        result = load_object(path)
        if result.get("schema_version") != "the-caption-prompt.prompt-set-result/v1":
            continue
        source_results.append(result["result_id"])
        for item in result["case_results"]:
            run_id = item["run_id"]
            root_total = item["total_tokens"]
            if run_id in run_tokens and run_tokens[run_id] != root_total:
                raise BackfillError(f"inconsistent root total_tokens for run: {run_id}")
            run_tokens[run_id] = root_total
    indexed = index_sessions(session_root)
    by_run: dict[str, list[dict[str, Any]]] = {}
    for cwd, records in indexed.items():
        run_id = workspace_run_id(cwd)
        if run_id is not None:
            by_run[run_id] = records
    for run_id, root_total in sorted(run_tokens.items()):
        try:
            usage = summarize_workspace_usage(by_run.get(run_id, []), root_total)
        except AllAgentUsageError as exc:
            raise BackfillError(f"cannot backfill run {run_id}: {exc}") from exc
        usage["run_id"] = run_id
        usage["generated_at"] = datetime.now(timezone.utc).isoformat()
        usage["source"] = "historical Codex rollout final usage grouped by exact workspace"
        write_once(output / "layer2" / "extensions" / run_id / "all-agent-usage" / "usage.json", usage)
    manifest = {
        "schema_version": "the-caption-prompt.all-agent-usage-backfill/v1",
        "source_registry": str(registry),
        "session_root": str(session_root),
        "source_result_ids": sorted(source_results),
        "source_result_count": len(source_results),
        "run_count": len(run_tokens),
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
    write_once(output / "manifest.json", manifest)
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", required=True)
    parser.add_argument("--session-root", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    try:
        result = backfill(
            Path(args.registry).resolve(),
            Path(args.session_root).resolve(),
            Path(args.output).resolve(),
        )
    except (BackfillError, AllAgentUsageError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
