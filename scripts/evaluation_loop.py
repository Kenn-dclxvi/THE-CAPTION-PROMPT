#!/usr/bin/env python3
"""Minimal four-layer KPI evidence loop for two THE-CAPTION prompt sets."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import statistics
import subprocess
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class EvaluationError(Exception):
    pass


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise EvaluationError(f"missing file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise EvaluationError(f"invalid JSON: {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise EvaluationError(f"JSON root must be an object: {path}")
    return value


def write_json_once(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("x", encoding="utf-8", newline="\n") as handle:
            json.dump(value, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
    except FileExistsError as exc:
        raise EvaluationError(f"refusing to overwrite: {path}") from exc


def require_positive(value: int, name: str) -> None:
    if value < 1:
        raise EvaluationError(f"{name} must be a positive integer")


def frozen_set(cycle: Path) -> dict[str, Any]:
    return load_json(cycle / "layer1" / "set.json")


def find_case(cycle: Path, case_id: str) -> dict[str, Any]:
    manifest = frozen_set(cycle)
    for case in manifest["cases"]:
        if case["id"] == case_id:
            return case
    raise EvaluationError(f"unknown case: {case_id}")


def validate_set(source: Path, manifest: dict[str, Any]) -> list[dict[str, Any]]:
    if not isinstance(manifest.get("set_id"), str) or not manifest["set_id"].strip():
        raise EvaluationError("set_id must be a non-empty string")
    cases = manifest.get("cases")
    if not isinstance(cases, list) or not cases:
        raise EvaluationError("cases must be a non-empty array")
    seen: set[str] = set()
    validated: list[dict[str, Any]] = []
    for case in cases:
        if not isinstance(case, dict):
            raise EvaluationError("each case must be an object")
        for key in ("id", "fixture"):
            if not isinstance(case.get(key), str) or not case[key].strip():
                raise EvaluationError(f"case {key} must be a non-empty string")
        if case["id"] in seen:
            raise EvaluationError(f"duplicate case id: {case['id']}")
        seen.add(case["id"])
        fixture = (source.parent / case["fixture"]).resolve()
        if not fixture.is_dir():
            raise EvaluationError(f"fixture must be a directory: {fixture}")
        validated.append({**case, "_source_fixture": str(fixture)})
    return validated


def layer1_freeze(args: argparse.Namespace) -> dict[str, Any]:
    source = Path(args.set).resolve()
    cycle = Path(args.cycle).resolve()
    manifest = load_json(source)
    cases = validate_set(source, manifest)
    if cycle.exists() and any(cycle.iterdir()):
        raise EvaluationError(f"cycle directory is not empty: {cycle}")

    frozen_cases: list[dict[str, Any]] = []
    fixture_root = cycle / "layer1" / "fixtures"
    for case in cases:
        destination = fixture_root / case["id"]
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(case["_source_fixture"], destination, symlinks=True)
        frozen_case = {key: value for key, value in case.items() if key != "_source_fixture"}
        frozen_case["fixture"] = f"fixtures/{case['id']}"
        frozen_cases.append(frozen_case)

    frozen = {
        "schema_version": "the-caption-prompt.evaluation-set/v1",
        "set_id": manifest["set_id"],
        "frozen_at": utc_now(),
        "cases": frozen_cases,
    }
    write_json_once(cycle / "layer1" / "set.json", frozen)
    return {"layer": 1, "set_id": frozen["set_id"], "case_count": len(frozen_cases)}


def parse_usage(path: Path) -> int | None:
    if not path.exists():
        return None
    usage = load_json(path)
    total = usage.get("total_tokens")
    if not isinstance(total, int) or total < 0:
        raise EvaluationError("usage must contain a non-negative integer total_tokens")
    return total


def parse_run_status(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    status = load_json(path)
    if status.get("schema_version") != "the-caption-prompt.run-status/v1":
        raise EvaluationError("run status has an unsupported schema_version")
    if status.get("status") != "excluded" or status.get("category") != "external_failure":
        raise EvaluationError("run status may only report an excluded external_failure")
    reason_code = status.get("reason_code")
    if not isinstance(reason_code, str) or not reason_code.strip():
        raise EvaluationError("run status reason_code must be a non-empty string")
    return status


def binding_is_excluded(binding: dict[str, Any]) -> bool:
    return binding.get("status", "valid") == "excluded"


def existing_binding(cycle: Path, condition: str, case_id: str, repetition: int) -> bool:
    for path in (cycle / "layer2" / "bindings").glob("*.json"):
        binding = load_json(path)
        if (
            not binding_is_excluded(binding)
            and binding["condition"] == condition
            and binding["case_id"] == case_id
            and binding["repetition"] == repetition
        ):
            return True
    return False


def validate_run_capsule(capsule: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    binding = capsule.get("binding")
    adapter = capsule.get("adapter")
    if not isinstance(binding, dict) or not isinstance(adapter, dict):
        raise EvaluationError("run capsule needs binding and adapter objects")
    condition = binding.get("condition")
    if condition not in ("a", "b"):
        raise EvaluationError("binding.condition must be a or b")
    for key in ("prompt_identity", "case_id"):
        if not isinstance(binding.get(key), str) or not binding[key].strip():
            raise EvaluationError(f"binding.{key} must be a non-empty string")
    repetition = binding.get("repetition")
    if not isinstance(repetition, int):
        raise EvaluationError("binding.repetition must be an integer")
    require_positive(repetition, "binding.repetition")
    argv = adapter.get("argv")
    if not isinstance(argv, list) or not argv or not all(isinstance(item, str) and item for item in argv):
        raise EvaluationError("adapter.argv must be a non-empty string array")
    return binding, argv


def layer2_run(args: argparse.Namespace) -> dict[str, Any]:
    cycle = Path(args.cycle).resolve()
    capsule_source = Path(args.capsule).resolve()
    capsule = load_json(capsule_source)
    binding_input, command = validate_run_capsule(capsule)
    condition = binding_input["condition"]
    case_id = binding_input["case_id"]
    repetition = binding_input["repetition"]
    case = find_case(cycle, case_id)
    if existing_binding(cycle, condition, case_id, repetition):
        raise EvaluationError("run already exists for condition/case/repetition")

    run_id = uuid.uuid4().hex
    evidence = cycle / "layer2" / "evidence" / run_id
    workspace = evidence / "workspace"
    source_fixture = cycle / "layer1" / case["fixture"]
    evidence.mkdir(parents=True, exist_ok=False)
    shutil.copytree(source_fixture, workspace, symlinks=True)
    case_path = evidence / "case.json"
    capsule_path = cycle / "layer2" / "capsules" / f"{run_id}.json"
    write_json_once(case_path, case)
    write_json_once(capsule_path, capsule)
    usage_report_path = evidence / ".usage-report.json"
    status_report_path = evidence / ".run-status-report.json"
    extension_dir = cycle / "layer2" / "extensions" / run_id
    extension_dir.mkdir(parents=True)

    env = os.environ.copy()
    env["EVAL_CASE_FILE"] = str(case_path)
    env["EVAL_RUN_CAPSULE_FILE"] = str(capsule_path)
    env["EVAL_USAGE_FILE"] = str(usage_report_path)
    env["EVAL_RUN_STATUS_FILE"] = str(status_report_path)
    env["EVAL_EXTENSION_DIR"] = str(extension_dir)
    started_at = utc_now()
    started = time.perf_counter()
    completed = subprocess.run(command, cwd=workspace, env=env, capture_output=True, check=False)
    elapsed = time.perf_counter() - started
    ended_at = utc_now()
    (evidence / "stdout.bin").write_bytes(completed.stdout)
    (evidence / "stderr.bin").write_bytes(completed.stderr)

    exclusion = parse_run_status(status_report_path)
    if status_report_path.exists():
        status_report_path.unlink()
    try:
        total_tokens = parse_usage(usage_report_path)
    except EvaluationError:
        if exclusion is None:
            raise
        total_tokens = None
    if usage_report_path.exists():
        usage_report_path.unlink()
    status = "excluded" if exclusion is not None else "valid"
    if total_tokens is not None:
        write_json_once(evidence / "usage.json", {"total_tokens": total_tokens})
    if exclusion is not None:
        write_json_once(evidence / "exclusion.json", exclusion)

    execution = {
        "schema_version": "the-caption-prompt.execution/v1",
        "run_id": run_id,
        "case_id": case_id,
        "repetition": repetition,
        "started_at": started_at,
        "ended_at": ended_at,
        "exit_code": completed.returncode,
        "elapsed_seconds": elapsed,
        "total_tokens": total_tokens,
        "status": status,
    }
    binding = {
        "schema_version": "the-caption-prompt.execution-binding/v1",
        "run_id": run_id,
        "case_id": case_id,
        "repetition": repetition,
        "condition": condition,
        "prompt_identity": binding_input["prompt_identity"],
        "status": status,
    }
    write_json_once(evidence / "execution.json", execution)
    write_json_once(cycle / "layer2" / "bindings" / f"{run_id}.json", binding)
    result = {"layer": 2, "run_id": run_id, "evidence": str(evidence), "status": status}
    if exclusion is not None:
        result["exclusion"] = exclusion
    return result


def layer3_rate(args: argparse.Namespace) -> dict[str, Any]:
    cycle = Path(args.cycle).resolve()
    execution_path = cycle / "layer2" / "evidence" / args.run_id / "execution.json"
    execution = load_json(execution_path)
    if execution.get("status", "valid") == "excluded":
        raise EvaluationError("excluded run cannot be quality-rated")
    if args.score < 0 or args.score > 4:
        raise EvaluationError("score must be between 0 and 4")
    if not args.reason.strip():
        raise EvaluationError("reason must be non-empty")
    rating = {
        "schema_version": "the-caption-prompt.quality-rating/v1",
        "run_id": args.run_id,
        "score": args.score,
        "reason": args.reason.strip(),
        "rated_at": utc_now(),
    }
    write_json_once(cycle / "layer3" / "ratings" / f"{args.run_id}.json", rating)
    return {"layer": 3, "run_id": args.run_id, "score": args.score}


def collect_runs(cycle: Path) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    manifest = frozen_set(cycle)
    runs: list[dict[str, Any]] = []
    excluded_attempts: list[dict[str, Any]] = []
    for binding_path in sorted((cycle / "layer2" / "bindings").glob("*.json")):
        binding = load_json(binding_path)
        if binding_is_excluded(binding):
            exclusion = load_json(
                cycle / "layer2" / "evidence" / binding["run_id"] / "exclusion.json"
            )
            excluded_attempts.append(
                {
                    "run_id": binding["run_id"],
                    "condition": binding["condition"],
                    "case_id": binding["case_id"],
                    "repetition": binding["repetition"],
                    "category": exclusion["category"],
                    "reason_code": exclusion["reason_code"],
                }
            )
            continue
        run_id = binding["run_id"]
        execution = load_json(cycle / "layer2" / "evidence" / run_id / "execution.json")
        rating = load_json(cycle / "layer3" / "ratings" / f"{run_id}.json")
        runs.append({**binding, "execution": execution, "rating": rating})
    if not runs:
        raise EvaluationError("no rated runs found")
    return manifest, runs, excluded_attempts


def aggregate_condition(
    condition: str,
    cases: list[str],
    repetitions: list[int],
    index: dict[tuple[str, str, int], dict[str, Any]],
) -> dict[str, Any]:
    per_repetition: list[dict[str, Any]] = []
    for repetition in repetitions:
        selected = [index[(condition, case_id, repetition)] for case_id in cases]
        tokens = [item["execution"]["total_tokens"] for item in selected]
        if any(value is None for value in tokens):
            raise EvaluationError("all runs need token usage before KPI comparison")
        quality = sum(item["rating"]["score"] for item in selected) / (4 * len(cases)) * 100
        per_repetition.append(
            {
                "repetition": repetition,
                "quality_score": quality,
                "total_tokens": sum(tokens),
                "elapsed_seconds": sum(item["execution"]["elapsed_seconds"] for item in selected),
            }
        )
    return {
        "repetitions": per_repetition,
        "median": {
            "quality_score": statistics.median(item["quality_score"] for item in per_repetition),
            "total_tokens": statistics.median(item["total_tokens"] for item in per_repetition),
            "elapsed_seconds": statistics.median(item["elapsed_seconds"] for item in per_repetition),
        },
    }


def kpi_difference_b_minus_a(a: dict[str, Any], b: dict[str, Any]) -> dict[str, Any]:
    return {
        "quality_score": b["quality_score"] - a["quality_score"],
        "total_tokens": b["total_tokens"] - a["total_tokens"],
        "elapsed_seconds": b["elapsed_seconds"] - a["elapsed_seconds"],
    }


def layer4_compare(args: argparse.Namespace) -> dict[str, Any]:
    cycle = Path(args.cycle).resolve()
    manifest, runs, excluded_attempts = collect_runs(cycle)
    cases = sorted(case["id"] for case in manifest["cases"])
    index: dict[tuple[str, str, int], dict[str, Any]] = {}
    identities: dict[str, set[str]] = {"a": set(), "b": set()}
    for run in runs:
        condition = run["condition"]
        if condition not in identities:
            raise EvaluationError(f"unexpected condition: {condition}")
        key = (condition, run["case_id"], run["repetition"])
        if key in index:
            raise EvaluationError(f"duplicate run key: {key}")
        index[key] = run
        identities[condition].add(run["prompt_identity"])
    if any(len(values) != 1 for values in identities.values()):
        raise EvaluationError("each condition must use exactly one prompt identity")

    repetitions_by_condition = {
        condition: sorted({key[2] for key in index if key[0] == condition})
        for condition in identities
    }
    if repetitions_by_condition["a"] != repetitions_by_condition["b"]:
        raise EvaluationError("prompt sets a and b repetitions must match")
    repetitions = repetitions_by_condition["a"]
    if not repetitions or repetitions != list(range(1, max(repetitions) + 1)):
        raise EvaluationError("repetitions must be contiguous and start at 1")
    expected = {
        (condition, case_id, repetition)
        for condition in identities
        for case_id in cases
        for repetition in repetitions
    }
    if set(index) != expected:
        raise EvaluationError("prompt sets a and b must cover every frozen case and repetition")

    set_a = aggregate_condition("a", cases, repetitions, index)
    set_b = aggregate_condition("b", cases, repetitions, index)
    comparison = {
        "schema_version": "the-caption-prompt.kpi-comparison/v2",
        "set_id": manifest["set_id"],
        "repetition_count": len(repetitions),
        "a": {
            "prompt_identity": next(iter(identities["a"])),
            **set_a,
        },
        "b": {
            "prompt_identity": next(iter(identities["b"])),
            **set_b,
        },
        "difference_b_minus_a": kpi_difference_b_minus_a(set_a["median"], set_b["median"]),
        "excluded_attempts": excluded_attempts,
        "compared_at": utc_now(),
    }
    artifact = cycle / "layer4" / "comparison.json"
    write_json_once(artifact, comparison)
    return {
        "layer": 4,
        "artifact": str(artifact),
        "repetition_count": len(repetitions),
        "excluded_attempt_count": len(excluded_attempts),
    }


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    commands = root.add_subparsers(dest="subcommand", required=True)

    freeze = commands.add_parser("freeze-set", help="Layer 1: freeze an evaluation set")
    freeze.add_argument("--set", required=True)
    freeze.add_argument("--cycle", required=True)
    freeze.set_defaults(handler=layer1_freeze)

    run = commands.add_parser("run", help="Layer 2: execute one case")
    run.add_argument("--cycle", required=True)
    run.add_argument("--capsule", required=True)
    run.set_defaults(handler=layer2_run)

    rate = commands.add_parser("rate", help="Layer 3: record one blind quality score")
    rate.add_argument("--cycle", required=True)
    rate.add_argument("--run-id", required=True)
    rate.add_argument("--score", type=int, required=True)
    rate.add_argument("--reason", required=True)
    rate.set_defaults(handler=layer3_rate)

    compare = commands.add_parser("compare", help="Layer 4: record KPI comparison evidence")
    compare.add_argument("--cycle", required=True)
    compare.set_defaults(handler=layer4_compare)

    return root


def main() -> int:
    args = parser().parse_args()
    try:
        result = args.handler(args)
    except EvaluationError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
