#!/usr/bin/env python3
"""Expand A/B capsule templates into a longest-first global execution queue."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

try:
    from .parallel_runner import ParallelRunError, require_positive_integer, write_json_once
    from .prepare_plan import collect_templates, load_object
except ImportError:  # Direct script execution.
    from parallel_runner import ParallelRunError, require_positive_integer, write_json_once
    from prepare_plan import collect_templates, load_object


def load_duration_hints(path: Path) -> dict[str, dict[str, float]]:
    document = load_object(path.resolve())
    execution = document.get("execution")
    raw_hints = (
        execution.get("duration_hints_seconds")
        if isinstance(execution, dict)
        else document.get("duration_hints_seconds")
    )
    if not isinstance(raw_hints, dict) or not raw_hints:
        raise ParallelRunError("duration hints must be a non-empty object")
    hints: dict[str, dict[str, float]] = {}
    for case_id, raw_conditions in raw_hints.items():
        if not isinstance(case_id, str) or not case_id or not isinstance(raw_conditions, dict):
            raise ParallelRunError("duration hints need case objects")
        conditions: dict[str, float] = {}
        for condition in ("a", "b"):
            value = raw_conditions.get(condition)
            if not isinstance(value, (int, float)) or isinstance(value, bool) or value <= 0:
                raise ParallelRunError(f"duration hint must be positive: {case_id} {condition}")
            conditions[condition] = float(value)
        hints[case_id] = conditions
    return hints


def prepare_global_plan(
    templates: list[Path],
    repetitions: list[int],
    cycle: Path,
    evaluator: Path,
    duration_hints_path: Path,
    output: Path,
    max_workers: int = 4,
    max_attempts: int = 3,
    monitor_interval_seconds: int = 15,
) -> dict[str, Any]:
    normalized_repetitions = sorted(
        {require_positive_integer(value, "repetition") for value in repetitions}
    )
    if len(normalized_repetitions) != len(repetitions):
        raise ParallelRunError("repetitions must not contain duplicates")
    max_workers = require_positive_integer(max_workers, "max_workers")
    max_attempts = require_positive_integer(max_attempts, "max_attempts")
    monitor_interval_seconds = require_positive_integer(
        monitor_interval_seconds, "monitor_interval_seconds"
    )
    cycle = cycle.resolve()
    evaluator = evaluator.resolve()
    duration_hints_path = duration_hints_path.resolve()
    output = output.resolve()
    if not (cycle / "layer1" / "set.json").is_file():
        raise ParallelRunError(f"cycle is not frozen: {cycle}")
    if not evaluator.is_file():
        raise ParallelRunError(f"evaluation loop does not exist: {evaluator}")
    if output.exists():
        raise ParallelRunError(f"refusing to overwrite output: {output}")

    pairs = collect_templates(templates)
    hints = load_duration_hints(duration_hints_path)
    missing = [case_id for case_id, _ in pairs if case_id not in hints]
    if missing:
        raise ParallelRunError(f"duration hint missing for case: {missing[0]}")

    output.mkdir(parents=True)
    capsule_dir = output / "capsules"
    capsule_dir.mkdir()
    pending: list[dict[str, Any]] = []
    for repetition in normalized_repetitions:
        for case_id, pair in pairs:
            for condition in ("a", "b"):
                capsule = copy.deepcopy(pair[condition])
                binding = capsule.get("binding")
                if not isinstance(binding, dict):
                    raise ParallelRunError(f"capsule template has no binding: {case_id} {condition}")
                binding["repetition"] = repetition
                filename = f"{case_id}-{condition}-r{repetition}.json"
                destination = capsule_dir / filename
                write_json_once(destination, capsule)
                pending.append(
                    {
                        "capsule": str(destination),
                        "estimated_seconds": hints[case_id][condition],
                        "case_id": case_id,
                        "condition": condition,
                        "repetition": repetition,
                    }
                )

    pending.sort(
        key=lambda item: (
            -item["estimated_seconds"],
            item["case_id"],
            item["condition"],
            item["repetition"],
        )
    )
    jobs = [
        {
            "sequence": sequence,
            "estimated_seconds": item["estimated_seconds"],
            "capsule": item["capsule"],
        }
        for sequence, item in enumerate(pending, start=1)
    ]
    hints_sha256 = hashlib.sha256(duration_hints_path.read_bytes()).hexdigest()
    plan = {
        "schema_version": "the-caption-prompt.parallel-execution-plan/v2",
        "schedule_policy": "global_queue",
        "ordering": "estimated_seconds_descending",
        "duration_hints": str(duration_hints_path),
        "duration_hints_sha256": hints_sha256,
        "cycle": str(cycle),
        "evaluation_loop": str(evaluator),
        "max_workers": max_workers,
        "max_attempts": max_attempts,
        "monitor_interval_seconds": monitor_interval_seconds,
        "jobs": jobs,
    }
    plan_path = output / "global-plan.json"
    write_json_once(plan_path, plan)
    return {
        "plan": str(plan_path),
        "case_count": len(pairs),
        "repetitions": normalized_repetitions,
        "slot_count": len(jobs),
        "max_workers": max_workers,
    }


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--template", action="append", required=True)
    result.add_argument("--repetition", action="append", type=int, required=True)
    result.add_argument("--cycle", required=True)
    result.add_argument("--evaluation-loop", required=True)
    result.add_argument("--duration-hints", required=True)
    result.add_argument("--output", required=True)
    result.add_argument("--max-workers", type=int, default=4)
    result.add_argument("--max-attempts", type=int, default=3)
    result.add_argument("--monitor-interval-seconds", type=int, default=15)
    return result


def main() -> int:
    args = parser().parse_args()
    try:
        result = prepare_global_plan(
            [Path(path) for path in args.template],
            args.repetition,
            Path(args.cycle),
            Path(args.evaluation_loop),
            Path(args.duration_hints),
            Path(args.output),
            args.max_workers,
            args.max_attempts,
            args.monitor_interval_seconds,
        )
    except (ParallelRunError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
