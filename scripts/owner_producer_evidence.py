#!/usr/bin/env python3
"""Build blind owner/producer evidence used by quality rating revision v1."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "the-caption-prompt.owner-producer-evidence/v1"
OWNER_PATTERN = re.compile(r"owner\s*=\s*([^\u3002\n;,]+)", re.IGNORECASE)
CRITERION_PATTERN = re.compile(r"\bF\d{2}(?:-[A-Z]+)?-C\d+\b")
GENERIC_OWNER_WORDS = {"independent", "check", "review", "audit", "owner"}


class EvidenceError(Exception):
    pass


def load_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        raise EvidenceError(f"invalid JSON object: {path}") from exc
    if not isinstance(value, dict):
        raise EvidenceError(f"JSON root must be an object: {path}")
    return value


def trial_input_text(case: dict[str, Any]) -> str:
    payload = case.get("payload")
    if not isinstance(payload, dict):
        raise EvidenceError("case payload is missing")
    trial = payload.get("trial_prompt_input")
    if not isinstance(trial, dict):
        raise EvidenceError("case trial_prompt_input is missing")
    return "\n".join(value for value in trial.values() if isinstance(value, str))


def owner_domain(owner: str) -> list[str]:
    words = re.findall(r"[a-z0-9]+", owner.lower())
    return [word for word in words if word not in GENERIC_OWNER_WORDS]


def final_result(rollout: Path) -> tuple[bool, str]:
    completed = False
    final = ""
    try:
        lines = rollout.read_text(encoding="utf-8", errors="replace").splitlines()
    except FileNotFoundError:
        return False, ""
    for raw in lines:
        try:
            event = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if event.get("type") != "event_msg":
            continue
        payload = event.get("payload")
        if not isinstance(payload, dict) or payload.get("type") != "task_complete":
            continue
        completed = True
        message = payload.get("last_agent_message")
        if isinstance(message, str):
            final = message
    return completed, final


def role_matches(owner: str, agent_path: str) -> bool:
    domain = owner_domain(owner)
    normalized_path = re.sub(r"[^a-z0-9]+", "_", agent_path.lower())
    return bool(domain) and any(word in normalized_path for word in domain)


def collect_run(cycle: Path, binding: dict[str, Any]) -> dict[str, Any]:
    run_id = binding.get("run_id")
    if not isinstance(run_id, str) or not run_id:
        raise EvidenceError("valid binding has no run_id")
    case_path = cycle / "layer2" / "evidence" / run_id / "case.json"
    case = load_object(case_path)
    text = trial_input_text(case)
    owner_match = OWNER_PATTERN.search(text)
    criteria = sorted(set(CRITERION_PATTERN.findall(text)))
    if owner_match is None:
        return {
            "case_id": binding.get("case_id", case.get("id")),
            "criterion_ids": criteria,
            "criterion_owner": None,
            "iteration": binding.get("iteration"),
            "run_id": run_id,
            "score_4_owner_evidence_eligible": True,
            "status": "not_applicable",
        }

    owner = owner_match.group(1).strip()
    usage_path = cycle / "layer2" / "extensions" / run_id / "all-agent-usage" / "usage.json"
    try:
        usage = load_object(usage_path)
    except EvidenceError:
        return {
            "case_id": binding.get("case_id", case.get("id")),
            "criterion_ids": criteria,
            "criterion_owner": owner,
            "iteration": binding.get("iteration"),
            "run_id": run_id,
            "score_4_owner_evidence_eligible": False,
            "status": "unavailable",
            "reason": "all-agent usage evidence is missing",
        }

    root_thread_id = usage.get("root_thread_id")
    sessions = usage.get("sessions")
    if not isinstance(root_thread_id, str) or not isinstance(sessions, list):
        raise EvidenceError(f"invalid all-agent usage evidence: {usage_path}")

    producers: list[dict[str, Any]] = []
    for raw_session in sessions:
        if not isinstance(raw_session, dict):
            continue
        thread_id = raw_session.get("thread_id")
        parent_thread_id = raw_session.get("parent_thread_id")
        source = raw_session.get("source")
        rollout_file = raw_session.get("rollout_file")
        agent_path = None
        if isinstance(source, dict):
            try:
                agent_path = source["subagent"]["thread_spawn"]["agent_path"]
            except (KeyError, TypeError):
                agent_path = None
        if not all(isinstance(value, str) and value for value in (thread_id, agent_path, rollout_file)):
            continue
        if not role_matches(owner, agent_path):
            continue
        completed, result = final_result(Path(rollout_file))
        distinct = thread_id != root_thread_id and parent_thread_id == root_thread_id
        mentioned = sorted(set(CRITERION_PATTERN.findall(result)))
        producers.append(
            {
                "agent_path": agent_path,
                "completed": completed,
                "criterion_ids_mentioned_in_result": mentioned,
                "distinct_from_active_executor": distinct,
                "parent_thread_id": parent_thread_id,
                "result_sha256": hashlib.sha256(result.encode("utf-8")).hexdigest() if result else None,
                "result_text": result,
                "thread_id": thread_id,
            }
        )

    independent = "independent" in owner.lower()
    admissible = [
        item
        for item in producers
        if item["completed"] and item["result_text"] and (not independent or item["distinct_from_active_executor"])
    ]
    eligible = bool(admissible)
    return {
        "admissible_producer_count": len(admissible),
        "case_id": binding.get("case_id", case.get("id")),
        "criterion_ids": criteria,
        "criterion_owner": owner,
        "independent_owner": independent,
        "iteration": binding.get("iteration"),
        "producer_candidates": producers,
        "run_id": run_id,
        "score_4_owner_evidence_eligible": eligible,
        "status": "available" if eligible else "failed",
    }


def collect(cycle: Path) -> dict[str, Any]:
    bindings_dir = cycle / "layer2" / "bindings"
    runs = []
    for path in sorted(bindings_dir.glob("*.json")):
        binding = load_object(path)
        if binding.get("status") != "valid":
            continue
        runs.append(collect_run(cycle, binding))
    if not runs:
        raise EvidenceError("no valid runs found")
    return {
        "eligible_run_count": sum(item["score_4_owner_evidence_eligible"] for item in runs),
        "ineligible_run_count": sum(not item["score_4_owner_evidence_eligible"] for item in runs),
        "run_count": len(runs),
        "runs": runs,
        "schema_version": SCHEMA_VERSION,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cycle", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = collect(args.cycle.resolve())
    rendered = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output is None:
        print(rendered, end="")
    else:
        output = args.output.resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        try:
            with output.open("x", encoding="utf-8") as handle:
                handle.write(rendered)
        except FileExistsError as exc:
            raise EvidenceError(f"refusing to overwrite owner-producer evidence: {output}") from exc
    return 0 if report["ineligible_run_count"] == 0 else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except EvidenceError as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc
