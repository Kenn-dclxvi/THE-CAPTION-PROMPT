#!/usr/bin/env python3
"""Expand one A/B capsule pair per case into a wave-isolated parallel plan."""

from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path
from typing import Any

try:
    from .parallel_runner import (
        ParallelRunError,
        binding_from_capsule,
        require_positive_integer,
        write_json_once,
    )
except ImportError:  # Direct script execution.
    from parallel_runner import (
        ParallelRunError,
        binding_from_capsule,
        require_positive_integer,
        write_json_once,
    )


def load_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        raise ParallelRunError(f"invalid capsule template: {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ParallelRunError(f"capsule template root must be an object: {path}")
    return value


def collect_templates(paths: list[Path]) -> list[tuple[str, dict[str, dict[str, Any]]]]:
    cases: dict[str, dict[str, dict[str, Any]]] = {}
    order: list[str] = []
    for path in paths:
        resolved = path.resolve()
        binding = binding_from_capsule(resolved)
        case_id = binding["case_id"]
        condition = binding["condition"]
        if case_id not in cases:
            cases[case_id] = {}
            order.append(case_id)
        if condition in cases[case_id]:
            raise ParallelRunError(f"duplicate template for {case_id} condition {condition}")
        cases[case_id][condition] = load_object(resolved)
    for case_id, templates in cases.items():
        if set(templates) != {"a", "b"}:
            raise ParallelRunError(f"case needs one a and one b template: {case_id}")
    return [(case_id, cases[case_id]) for case_id in order]


def prepare_plan(
    templates: list[Path],
    repetitions: int,
    cycle: Path,
    evaluator: Path,
    output: Path,
    max_workers: int = 2,
    max_attempts: int = 3,
    monitor_interval_seconds: int = 15,
) -> dict[str, Any]:
    repetitions = require_positive_integer(repetitions, "repetitions")
    max_workers = require_positive_integer(max_workers, "max_workers")
    max_attempts = require_positive_integer(max_attempts, "max_attempts")
    monitor_interval_seconds = require_positive_integer(
        monitor_interval_seconds, "monitor_interval_seconds"
    )
    if max_workers < 2:
        raise ParallelRunError("A/B wave execution requires max_workers >= 2")
    cycle = cycle.resolve()
    evaluator = evaluator.resolve()
    output = output.resolve()
    if not (cycle / "layer1" / "set.json").is_file():
        raise ParallelRunError(f"cycle is not frozen: {cycle}")
    if not evaluator.is_file():
        raise ParallelRunError(f"evaluation loop does not exist: {evaluator}")
    if output.exists():
        raise ParallelRunError(f"refusing to overwrite output: {output}")
    pairs = collect_templates(templates)
    output.mkdir(parents=True)
    capsule_dir = output / "capsules"
    capsule_dir.mkdir()
    jobs: list[dict[str, Any]] = []
    wave = 0
    for repetition in range(1, repetitions + 1):
        for case_index, (case_id, pair) in enumerate(pairs, start=1):
            wave += 1
            condition_order = ("a", "b") if (repetition + case_index) % 2 == 0 else ("b", "a")
            for condition in condition_order:
                capsule = copy.deepcopy(pair[condition])
                binding = capsule.get("binding")
                if not isinstance(binding, dict):
                    raise ParallelRunError(f"capsule template has no binding: {case_id} {condition}")
                binding["repetition"] = repetition
                filename = f"{case_id}-{condition}-r{repetition}.json"
                destination = capsule_dir / filename
                write_json_once(destination, capsule)
                jobs.append({"wave": wave, "capsule": str(destination)})
    plan = {
        "schema_version": "the-caption-prompt.parallel-execution-plan/v1",
        "cycle": str(cycle),
        "evaluation_loop": str(evaluator),
        "max_workers": max_workers,
        "max_attempts": max_attempts,
        "monitor_interval_seconds": monitor_interval_seconds,
        "jobs": jobs,
    }
    plan_path = output / "parallel-plan.json"
    write_json_once(plan_path, plan)
    return {
        "plan": str(plan_path),
        "case_count": len(pairs),
        "repetitions": repetitions,
        "slot_count": len(jobs),
        "wave_count": wave,
    }


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--template", action="append", required=True)
    result.add_argument("--repetitions", type=int, required=True)
    result.add_argument("--cycle", required=True)
    result.add_argument("--evaluation-loop", required=True)
    result.add_argument("--output", required=True)
    result.add_argument("--max-workers", type=int, default=2)
    result.add_argument("--max-attempts", type=int, default=3)
    result.add_argument("--monitor-interval-seconds", type=int, default=15)
    return result


def main() -> int:
    args = parser().parse_args()
    try:
        result = prepare_plan(
            [Path(path) for path in args.template],
            args.repetitions,
            Path(args.cycle),
            Path(args.evaluation_loop),
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
