#!/usr/bin/env python3
"""Expand one capsule template per case into a wave-isolated parallel plan."""

from __future__ import annotations

import argparse
import copy
import json
import math
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


def collect_templates(paths: list[Path]) -> list[tuple[str, dict[str, Any]]]:
    templates: list[tuple[str, dict[str, Any]]] = []
    seen_cases: set[str] = set()
    signature: tuple[str, str] | None = None
    for path in paths:
        resolved = path.resolve()
        binding = binding_from_capsule(resolved)
        case_id = binding["case_id"]
        if case_id in seen_cases:
            raise ParallelRunError(f"duplicate template for case: {case_id}")
        seen_cases.add(case_id)
        current_signature = (
            binding["prompt_set_identity_sha256"],
            binding["comparison_conditions_sha256"],
        )
        if signature is None:
            signature = current_signature
        elif current_signature != signature:
            raise ParallelRunError("templates must use one prompt identity and comparison conditions")
        templates.append((case_id, load_object(resolved)))
    if not templates:
        raise ParallelRunError("at least one template is required")
    return templates


def prepare_plan(
    templates: list[Path],
    iterations: int,
    cycle: Path,
    evaluator: Path,
    output: Path,
    max_workers: int = 2,
    max_attempts: int = 3,
    monitor_interval_seconds: int = 15,
) -> dict[str, Any]:
    iterations = require_positive_integer(iterations, "iterations")
    max_workers = require_positive_integer(max_workers, "max_workers")
    max_attempts = require_positive_integer(max_attempts, "max_attempts")
    monitor_interval_seconds = require_positive_integer(
        monitor_interval_seconds, "monitor_interval_seconds"
    )
    cycle = cycle.resolve()
    evaluator = evaluator.resolve()
    output = output.resolve()
    if not (cycle / "layer1" / "set.json").is_file():
        raise ParallelRunError(f"cycle is not frozen: {cycle}")
    if not evaluator.is_file():
        raise ParallelRunError(f"evaluation loop does not exist: {evaluator}")
    if output.exists():
        raise ParallelRunError(f"refusing to overwrite output: {output}")
    case_templates = collect_templates(templates)
    for case_id, template in case_templates:
        conditions = template.get("comparison_conditions")
        repetition = conditions.get("repetition_condition") if isinstance(conditions, dict) else None
        if not isinstance(repetition, dict) or repetition.get("iterations") != iterations:
            raise ParallelRunError(
                f"template repetition_condition.iterations must equal {iterations}: {case_id}"
            )
    output.mkdir(parents=True)
    capsule_dir = output / "capsules"
    capsule_dir.mkdir()
    jobs: list[dict[str, Any]] = []
    waves_per_iteration = math.ceil(len(case_templates) / max_workers)
    for iteration in range(1, iterations + 1):
        for case_index, (case_id, template) in enumerate(case_templates):
            capsule = copy.deepcopy(template)
            binding = capsule.get("binding")
            if not isinstance(binding, dict):
                raise ParallelRunError(f"capsule template has no binding: {case_id}")
            binding["iteration"] = iteration
            filename = f"{case_id}-i{iteration}.json"
            destination = capsule_dir / filename
            write_json_once(destination, capsule)
            wave = (iteration - 1) * waves_per_iteration + case_index // max_workers + 1
            jobs.append({"wave": wave, "capsule": str(destination)})
    plan = {
        "schema_version": "the-caption-prompt.parallel-execution-plan/v3",
        "schedule_policy": "wave_barrier",
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
        "case_count": len(case_templates),
        "iterations": iterations,
        "slot_count": len(jobs),
        "wave_count": waves_per_iteration * iterations,
    }


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--template", action="append", required=True)
    result.add_argument("--iterations", type=int, required=True)
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
            args.iterations,
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
