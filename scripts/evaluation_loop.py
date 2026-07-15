#!/usr/bin/env python3
"""Four-layer KPI evidence loop with append-only prompt-set results."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import statistics
import subprocess
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

if __package__:
    from .storage_copy import StorageCopyError, materialize_tree
else:
    from storage_copy import StorageCopyError, materialize_tree


class EvaluationError(Exception):
    pass


REQUIRED_COMPARISON_CONDITIONS = (
    "target_repository_ref",
    "model",
    "agent_environment",
    "task_spec",
    "permission",
    "executor_parameters",
    "repetition_condition",
)


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


def canonical_json(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def identity_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_json(value)).hexdigest()


def require_non_empty_string(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise EvaluationError(f"{name} must be a non-empty string")
    return value


def require_positive(value: Any, name: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        raise EvaluationError(f"{name} must be a positive integer")
    return value


def frozen_set(cycle: Path) -> dict[str, Any]:
    return load_json(cycle / "layer1" / "set.json")


def find_case(cycle: Path, case_id: str) -> dict[str, Any]:
    manifest = frozen_set(cycle)
    for case in manifest["cases"]:
        if case["id"] == case_id:
            return case
    raise EvaluationError(f"unknown case: {case_id}")


def fixture_identity(root: Path) -> dict[str, str]:
    entries: list[dict[str, Any]] = []
    for path in sorted(root.rglob("*"), key=lambda item: item.relative_to(root).as_posix()):
        relative = path.relative_to(root)
        if ".git" in relative.parts:
            continue
        name = relative.as_posix()
        mode = path.lstat().st_mode & 0o777
        if path.is_symlink():
            entries.append({"path": name, "type": "symlink", "mode": mode, "target": os.readlink(path)})
        elif path.is_dir():
            entries.append({"path": name, "type": "directory", "mode": mode})
        elif path.is_file():
            entries.append(
                {
                    "path": name,
                    "type": "file",
                    "mode": mode,
                    "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                }
            )
        else:
            raise EvaluationError(f"unsupported fixture entry: {path}")
    return {
        "algorithm": "sha256(canonical-json(path,type,mode,content); excludes .git)",
        "digest": identity_sha256(entries),
    }


def validate_set(source: Path, manifest: dict[str, Any]) -> list[dict[str, Any]]:
    require_non_empty_string(manifest.get("set_id"), "set_id")
    require_non_empty_string(manifest.get("revision"), "revision")
    cases = manifest.get("cases")
    if not isinstance(cases, list) or not cases:
        raise EvaluationError("cases must be a non-empty array")
    seen: set[str] = set()
    validated: list[dict[str, Any]] = []
    for case in cases:
        if not isinstance(case, dict):
            raise EvaluationError("each case must be an object")
        case_id = require_non_empty_string(case.get("id"), "case id")
        fixture_value = require_non_empty_string(case.get("fixture"), "case fixture")
        if case_id in seen:
            raise EvaluationError(f"duplicate case id: {case_id}")
        seen.add(case_id)
        fixture = (source.parent / fixture_value).resolve()
        if not fixture.is_dir():
            raise EvaluationError(f"fixture must be a directory: {fixture}")
        validated.append(
            {
                **case,
                "_source_fixture": str(fixture),
                "_fixture_identity": fixture_identity(fixture),
            }
        )
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
        try:
            materialize_tree(case["_source_fixture"], destination)
        except StorageCopyError as exc:
            raise EvaluationError(f"failed to materialize fixture: {exc}") from exc
        frozen_case = {
            key: value
            for key, value in case.items()
            if key not in {"_source_fixture", "_fixture_identity"}
        }
        frozen_case["fixture"] = f"fixtures/{case['id']}"
        frozen_case["fixture_identity"] = case["_fixture_identity"]
        frozen_cases.append(frozen_case)

    identity_document = {
        "schema_version": "the-caption-prompt.evaluation-set/v2",
        "set_id": manifest["set_id"],
        "revision": manifest["revision"],
        "cases": frozen_cases,
    }
    frozen = {
        **identity_document,
        "identity_sha256": identity_sha256(identity_document),
        "frozen_at": utc_now(),
    }
    write_json_once(cycle / "layer1" / "set.json", frozen)
    return {
        "layer": 1,
        "set_id": frozen["set_id"],
        "revision": frozen["revision"],
        "identity_sha256": frozen["identity_sha256"],
        "case_count": len(frozen_cases),
    }


def parse_usage(path: Path) -> int | None:
    if not path.exists():
        return None
    usage = load_json(path)
    total = usage.get("total_tokens")
    if not isinstance(total, int) or isinstance(total, bool) or total < 0:
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
    require_non_empty_string(status.get("reason_code"), "run status reason_code")
    return status


def validate_prompt_set_identity(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise EvaluationError("binding.prompt_set_identity must be an object")
    identity = dict(value)
    require_non_empty_string(identity.get("name"), "binding.prompt_set_identity.name")
    revision = identity.get("revision")
    bundle_sha256 = identity.get("bundle_sha256")
    if revision is None and bundle_sha256 is None:
        raise EvaluationError("prompt_set_identity needs revision or bundle_sha256")
    if revision is not None:
        require_non_empty_string(revision, "binding.prompt_set_identity.revision")
    if bundle_sha256 is not None:
        digest = require_non_empty_string(
            bundle_sha256, "binding.prompt_set_identity.bundle_sha256"
        )
        if len(digest) != 64 or any(character not in "0123456789abcdef" for character in digest):
            raise EvaluationError("binding.prompt_set_identity.bundle_sha256 must be lowercase SHA-256")
    return identity


def validate_comparison_conditions(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise EvaluationError("comparison_conditions must be an object")
    conditions = dict(value)
    reserved = {"evaluation_set", "fixtures", "coverage"}.intersection(conditions)
    if reserved:
        raise EvaluationError(
            f"comparison_conditions uses reserved key: {sorted(reserved)[0]}"
        )
    for key in REQUIRED_COMPARISON_CONDITIONS:
        if key not in conditions or conditions[key] is None:
            raise EvaluationError(f"comparison_conditions.{key} is required")
        if isinstance(conditions[key], str) and not conditions[key].strip():
            raise EvaluationError(f"comparison_conditions.{key} must not be empty")
    repetition = conditions["repetition_condition"]
    if not isinstance(repetition, dict):
        raise EvaluationError("comparison_conditions.repetition_condition must be an object")
    require_positive(
        repetition.get("iterations"),
        "comparison_conditions.repetition_condition.iterations",
    )
    return conditions


def validate_run_capsule(
    capsule: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], list[str]]:
    if capsule.get("schema_version") != "the-caption-prompt.execution-capsule/v2":
        raise EvaluationError("run capsule has an unsupported schema_version")
    binding = capsule.get("binding")
    adapter = capsule.get("adapter")
    if not isinstance(binding, dict) or not isinstance(adapter, dict):
        raise EvaluationError("run capsule needs binding and adapter objects")
    identity = validate_prompt_set_identity(binding.get("prompt_set_identity"))
    case_id = require_non_empty_string(binding.get("case_id"), "binding.case_id")
    iteration = require_positive(binding.get("iteration"), "binding.iteration")
    conditions = validate_comparison_conditions(capsule.get("comparison_conditions"))
    argv = adapter.get("argv")
    if not isinstance(argv, list) or not argv or not all(
        isinstance(item, str) and item for item in argv
    ):
        raise EvaluationError("adapter.argv must be a non-empty string array")
    return {
        "prompt_set_identity": identity,
        "prompt_set_identity_sha256": identity_sha256(identity),
        "case_id": case_id,
        "iteration": iteration,
    }, conditions, argv


def binding_is_excluded(binding: dict[str, Any]) -> bool:
    return binding.get("status", "valid") == "excluded"


def existing_bindings(cycle: Path) -> list[dict[str, Any]]:
    return [
        load_json(path)
        for path in sorted((cycle / "layer2" / "bindings").glob("*.json"))
    ]


def validate_cycle_binding(
    bindings: list[dict[str, Any]],
    binding: dict[str, Any],
    conditions: dict[str, Any],
) -> None:
    for existing in bindings:
        if existing["prompt_set_identity"] != binding["prompt_set_identity"]:
            raise EvaluationError("one cycle may contain only one prompt_set_identity")
        if existing["comparison_conditions"] != conditions:
            raise EvaluationError("one cycle may contain only one comparison_conditions value")
        if (
            not binding_is_excluded(existing)
            and existing["case_id"] == binding["case_id"]
            and existing["iteration"] == binding["iteration"]
        ):
            raise EvaluationError("run already exists for case/iteration")


def layer2_run(args: argparse.Namespace) -> dict[str, Any]:
    cycle = Path(args.cycle).resolve()
    capsule_source = Path(args.capsule).resolve()
    capsule = load_json(capsule_source)
    binding_input, conditions, command = validate_run_capsule(capsule)
    case_id = binding_input["case_id"]
    iteration = binding_input["iteration"]
    case = find_case(cycle, case_id)
    validate_cycle_binding(existing_bindings(cycle), binding_input, conditions)

    run_id = uuid.uuid4().hex
    evidence = cycle / "layer2" / "evidence" / run_id
    workspace = evidence / "workspace"
    source_fixture = cycle / "layer1" / case["fixture"]
    evidence.mkdir(parents=True, exist_ok=False)
    try:
        materialize_tree(source_fixture, workspace)
    except StorageCopyError as exc:
        raise EvaluationError(f"failed to materialize workspace: {exc}") from exc
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
        "schema_version": "the-caption-prompt.execution/v2",
        "run_id": run_id,
        "case_id": case_id,
        "iteration": iteration,
        "started_at": started_at,
        "ended_at": ended_at,
        "exit_code": completed.returncode,
        "elapsed_seconds": elapsed,
        "total_tokens": total_tokens,
        "status": status,
    }
    binding = {
        "schema_version": "the-caption-prompt.execution-binding/v2",
        "run_id": run_id,
        "case_id": case_id,
        "iteration": iteration,
        "prompt_set_identity": binding_input["prompt_set_identity"],
        "prompt_set_identity_sha256": binding_input["prompt_set_identity_sha256"],
        "comparison_conditions": conditions,
        "comparison_conditions_sha256": identity_sha256(conditions),
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


def collect_runs(
    cycle: Path,
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    manifest = frozen_set(cycle)
    runs: list[dict[str, Any]] = []
    excluded_attempts: list[dict[str, Any]] = []
    for binding in existing_bindings(cycle):
        if binding_is_excluded(binding):
            exclusion = load_json(
                cycle / "layer2" / "evidence" / binding["run_id"] / "exclusion.json"
            )
            excluded_attempts.append(
                {
                    "run_id": binding["run_id"],
                    "case_id": binding["case_id"],
                    "iteration": binding["iteration"],
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


def aggregate_prompt_set(
    cases: list[str],
    iterations: list[int],
    index: dict[tuple[str, int], dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    case_results: list[dict[str, Any]] = []
    per_iteration: list[dict[str, Any]] = []
    for iteration in iterations:
        selected = [index[(case_id, iteration)] for case_id in cases]
        tokens = [item["execution"]["total_tokens"] for item in selected]
        if any(value is None for value in tokens):
            raise EvaluationError("all runs need token usage before result registration")
        for item in selected:
            case_results.append(
                {
                    "run_id": item["run_id"],
                    "case_id": item["case_id"],
                    "iteration": item["iteration"],
                    "quality_score": item["rating"]["score"],
                    "total_tokens": item["execution"]["total_tokens"],
                    "elapsed_seconds": item["execution"]["elapsed_seconds"],
                }
            )
        quality = sum(item["rating"]["score"] for item in selected) / (4 * len(cases)) * 100
        per_iteration.append(
            {
                "iteration": iteration,
                "quality_score": quality,
                "total_tokens": sum(tokens),
                "elapsed_seconds": sum(
                    item["execution"]["elapsed_seconds"] for item in selected
                ),
            }
        )
    median = {
        "quality_score": statistics.median(item["quality_score"] for item in per_iteration),
        "total_tokens": statistics.median(item["total_tokens"] for item in per_iteration),
        "elapsed_seconds": statistics.median(
            item["elapsed_seconds"] for item in per_iteration
        ),
    }
    return case_results, per_iteration, median


def build_compatibility(
    manifest: dict[str, Any],
    conditions: dict[str, Any],
    cases: list[str],
    iterations: list[int],
) -> dict[str, Any]:
    fixtures = {
        case["id"]: case["fixture_identity"]
        for case in manifest["cases"]
    }
    return {
        "evaluation_set": {
            "set_id": manifest["set_id"],
            "revision": manifest["revision"],
            "identity_sha256": manifest["identity_sha256"],
        },
        "fixtures": fixtures,
        **conditions,
        "coverage": {"case_ids": cases, "iterations": iterations},
    }


def layer4_record_result(args: argparse.Namespace) -> dict[str, Any]:
    cycle = Path(args.cycle).resolve()
    registry = Path(args.registry).resolve()
    receipt_path = cycle / "layer4" / "result-registration.json"
    if receipt_path.exists():
        raise EvaluationError(f"cycle result is already registered: {receipt_path}")
    manifest, runs, excluded_attempts = collect_runs(cycle)
    cases = sorted(case["id"] for case in manifest["cases"])
    identities = {canonical_json(run["prompt_set_identity"]) for run in runs}
    conditions_values = {canonical_json(run["comparison_conditions"]) for run in runs}
    if len(identities) != 1:
        raise EvaluationError("one result must use exactly one prompt_set_identity")
    if len(conditions_values) != 1:
        raise EvaluationError("one result must use exactly one comparison_conditions value")
    prompt_set_identity = runs[0]["prompt_set_identity"]
    conditions = runs[0]["comparison_conditions"]

    index: dict[tuple[str, int], dict[str, Any]] = {}
    for run in runs:
        key = (run["case_id"], run["iteration"])
        if key in index:
            raise EvaluationError(f"duplicate run key: {key}")
        index[key] = run
    iterations = sorted({key[1] for key in index})
    if not iterations or iterations != list(range(1, max(iterations) + 1)):
        raise EvaluationError("iterations must be contiguous and start at 1")
    expected = {(case_id, iteration) for case_id in cases for iteration in iterations}
    if set(index) != expected:
        raise EvaluationError("prompt set must cover every frozen case and iteration")
    expected_iterations = conditions["repetition_condition"]["iterations"]
    if len(iterations) != expected_iterations:
        raise EvaluationError("observed iterations do not match repetition_condition.iterations")

    case_results, per_iteration, median = aggregate_prompt_set(cases, iterations, index)
    compatibility = build_compatibility(manifest, conditions, cases, iterations)
    compatibility_key = identity_sha256(compatibility)
    result_id = uuid.uuid4().hex
    result = {
        "schema_version": "the-caption-prompt.prompt-set-result/v1",
        "result_id": result_id,
        "prompt_set_identity": prompt_set_identity,
        "prompt_set_identity_sha256": identity_sha256(prompt_set_identity),
        "compatibility": compatibility,
        "compatibility_key": compatibility_key,
        "case_results": case_results,
        "iterations": per_iteration,
        "median": median,
        "excluded_attempts": excluded_attempts,
        "created_at": utc_now(),
    }
    result["result_content_sha256"] = identity_sha256(result)
    artifact = registry / "results" / f"{result_id}.json"
    write_json_once(artifact, result)
    write_json_once(
        receipt_path,
        {
            "schema_version": "the-caption-prompt.result-registration/v1",
            "result_id": result_id,
            "result_path": str(artifact),
            "compatibility_key": compatibility_key,
            "result_content_sha256": result["result_content_sha256"],
            "registered_at": utc_now(),
        },
    )
    return {
        "layer": 4,
        "result_id": result_id,
        "artifact": str(artifact),
        "compatibility_key": compatibility_key,
        "iteration_count": len(iterations),
        "excluded_attempt_count": len(excluded_attempts),
    }


def registry_results(registry: Path) -> list[tuple[Path, dict[str, Any]]]:
    results: list[tuple[Path, dict[str, Any]]] = []
    for path in sorted((registry / "results").glob("*.json")):
        result = load_json(path)
        if result.get("schema_version") != "the-caption-prompt.prompt-set-result/v1":
            raise EvaluationError(f"unsupported registry result schema: {path}")
        if result.get("result_id") != path.stem:
            raise EvaluationError(f"registry result id does not match filename: {path}")
        prompt_set_identity = result.get("prompt_set_identity")
        if result.get("prompt_set_identity_sha256") != identity_sha256(prompt_set_identity):
            raise EvaluationError(f"registry prompt_set_identity hash mismatch: {path}")
        compatibility = result.get("compatibility")
        if result.get("compatibility_key") != identity_sha256(compatibility):
            raise EvaluationError(f"registry compatibility hash mismatch: {path}")
        content = {key: value for key, value in result.items() if key != "result_content_sha256"}
        if result.get("result_content_sha256") != identity_sha256(content):
            raise EvaluationError(f"registry result content hash mismatch: {path}")
        results.append((path, result))
    return results


def query_results(args: argparse.Namespace) -> dict[str, Any]:
    registry = Path(args.registry).resolve()
    selected: list[dict[str, Any]] = []
    for path, result in registry_results(registry):
        identity = result["prompt_set_identity"]
        if args.prompt_name is not None and identity.get("name") != args.prompt_name:
            continue
        if args.prompt_revision is not None and identity.get("revision") != args.prompt_revision:
            continue
        if args.bundle_sha256 is not None and identity.get("bundle_sha256") != args.bundle_sha256:
            continue
        if args.compatibility_key is not None and result["compatibility_key"] != args.compatibility_key:
            continue
        selected.append(
            {
                "result_id": result["result_id"],
                "path": str(path),
                "prompt_set_identity": identity,
                "compatibility_key": result["compatibility_key"],
                "median": result["median"],
                "created_at": result["created_at"],
            }
        )
    return {
        "schema_version": "the-caption-prompt.result-query/v1",
        "count": len(selected),
        "results": selected,
    }


def kpi_difference(minuend: dict[str, Any], subtrahend: dict[str, Any]) -> dict[str, Any]:
    return {
        "quality_score": minuend["quality_score"] - subtrahend["quality_score"],
        "total_tokens": minuend["total_tokens"] - subtrahend["total_tokens"],
        "elapsed_seconds": minuend["elapsed_seconds"] - subtrahend["elapsed_seconds"],
    }


def compare_results(args: argparse.Namespace) -> dict[str, Any]:
    registry = Path(args.registry).resolve()
    output = Path(args.output).resolve()
    result_ids = args.result_id
    if len(result_ids) < 2:
        raise EvaluationError("compare requires at least two --result-id values")
    if len(set(result_ids)) != len(result_ids):
        raise EvaluationError("compare result ids must be unique")
    if args.reference_result_id not in result_ids:
        raise EvaluationError("reference result id must be included in --result-id")
    available = {result["result_id"]: result for _, result in registry_results(registry)}
    missing = [result_id for result_id in result_ids if result_id not in available]
    if missing:
        raise EvaluationError(f"unknown result id: {missing[0]}")
    selected = [available[result_id] for result_id in result_ids]
    reference = available[args.reference_result_id]
    for result in selected:
        if result["compatibility_key"] != reference["compatibility_key"]:
            raise EvaluationError("result compatibility keys do not match")
        if result["compatibility"] != reference["compatibility"]:
            raise EvaluationError("result compatibility conditions do not match")

    view = {
        "schema_version": "the-caption-prompt.prompt-set-comparison-view/v1",
        "compatibility_key": reference["compatibility_key"],
        "reference_result_id": reference["result_id"],
        "prompt_sets": [
            {
                "result_id": result["result_id"],
                "prompt_set_identity": result["prompt_set_identity"],
                "iterations": result["iterations"],
                "median": result["median"],
                "excluded_attempts": result["excluded_attempts"],
            }
            for result in selected
        ],
        "differences": [
            {
                "minuend_result_id": result["result_id"],
                "subtrahend_result_id": reference["result_id"],
                "kpis": kpi_difference(result["median"], reference["median"]),
            }
            for result in selected
            if result["result_id"] != reference["result_id"]
        ],
        "generated_at": utc_now(),
    }
    write_json_once(output, view)
    return {
        "layer": 4,
        "artifact": str(output),
        "prompt_set_count": len(selected),
        "difference_count": len(view["differences"]),
    }


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    commands = root.add_subparsers(dest="subcommand", required=True)

    freeze = commands.add_parser("freeze-set", help="Layer 1: freeze an evaluation set")
    freeze.add_argument("--set", required=True)
    freeze.add_argument("--cycle", required=True)
    freeze.set_defaults(handler=layer1_freeze)

    run = commands.add_parser("run", help="Layer 2: execute one case and iteration")
    run.add_argument("--cycle", required=True)
    run.add_argument("--capsule", required=True)
    run.set_defaults(handler=layer2_run)

    rate = commands.add_parser("rate", help="Layer 3: record one blind quality score")
    rate.add_argument("--cycle", required=True)
    rate.add_argument("--run-id", required=True)
    rate.add_argument("--score", type=int, required=True)
    rate.add_argument("--reason", required=True)
    rate.set_defaults(handler=layer3_rate)

    record = commands.add_parser(
        "record-result", help="Layer 4: append one prompt-set result to a registry"
    )
    record.add_argument("--cycle", required=True)
    record.add_argument("--registry", required=True)
    record.set_defaults(handler=layer4_record_result)

    query = commands.add_parser("query-results", help="List stored prompt-set results")
    query.add_argument("--registry", required=True)
    query.add_argument("--prompt-name")
    query.add_argument("--prompt-revision")
    query.add_argument("--bundle-sha256")
    query.add_argument("--compatibility-key")
    query.set_defaults(handler=query_results)

    compare = commands.add_parser(
        "compare", help="Layer 4: create a view from compatible stored results"
    )
    compare.add_argument("--registry", required=True)
    compare.add_argument("--result-id", action="append", required=True)
    compare.add_argument("--reference-result-id", required=True)
    compare.add_argument("--output", required=True)
    compare.set_defaults(handler=compare_results)

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
