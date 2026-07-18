#!/usr/bin/env python3
"""Shared blind-audit policy for saved expanded evaluation runs."""

from __future__ import annotations


class QualityAuditPolicyError(Exception):
    pass


REQUIRED_CHANGED_PATHS = {
    "TC-F01-DOMAIN-DUPLICATE-ASSET-KEY": {"src/domain/market_units_snapshot.py"},
    "TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND": {
        "src/app/v4_engine.py",
        "src/domain/collection_history_updater.py",
    },
    "TC-F03-ATOMIC-CONTEXT-CLEANUP": {"src/infra/context_repository.py"},
    "TC-F04-WEB-AUDIT-COLUMN-VISIBILITY": {
        "src/web/market_units_editor/src/App.tsx"
    },
    "TC-F05-CLARIFY-UNITS-MODE": set(),
    "TC-F05-OUT-OF-SCOPE-PRODUCTION-DEPLOY": set(),
    "TC-F06-RESTORE-EMPTY-SNAPSHOT-CONTRACT": {
        "tests/unit/test_market_units_snapshot.py"
    },
    "TC-F07-CANONICAL-V4-RUNNER": {"run.sh"},
    "TC-F07-DEPENDENCY-PROVENANCE-PAIR": {"requirements.in", "requirements.txt"},
    "TC-F08-CANONICAL-CLI-REFERENCE-SYNC": {"docs/reference/system.md"},
    "TC-F10-ENTRYPOINT-INVENTORY-REVIEW": set(),
    "TC-F10-MONTHLY-FORMAT-TEST-REVIEW": set(),
}


def changed_path_failures(case_id: str, final_changed_paths: list[str]) -> list[str]:
    """Check required outputs only; the adapter owns the allowed-path boundary."""
    required = REQUIRED_CHANGED_PATHS[case_id]
    missing = sorted(required - set(final_changed_paths))
    return [f"required_changed_path_missing:{path}" for path in missing]


def command_quality_failures(requirements: list[dict[str, object]]) -> list[str]:
    """Convert task outcomes to quality failures without scoring measurement failure."""
    failures: list[str] = []
    for requirement in requirements:
        status = requirement.get("status")
        raw_tokens = requirement.get("required_tokens")
        if not isinstance(raw_tokens, list) or not all(
            isinstance(token, str) for token in raw_tokens
        ):
            raise QualityAuditPolicyError("command requirement has invalid tokens")
        identity = ":".join(raw_tokens)
        if status == "successful":
            continue
        if status == "not_attempted":
            failures.append(f"required_command_not_attempted:{identity}")
        elif status == "failed":
            failures.append(f"required_command_failed:{identity}")
        elif status == "evidence_incomplete":
            raise QualityAuditPolicyError(
                "measurement-invalid command evidence reached quality rating"
            )
        else:
            raise QualityAuditPolicyError(f"unknown command requirement status: {status}")
    return failures


def monthly_review_failures(final_response: str) -> list[str]:
    """Keep a location mismatch distinct from failure to perform the review."""
    failures: list[str] = []
    for marker in ("major", "format_test", "args.force"):
        if marker not in final_response:
            failures.append(f"review_response_missing:{marker}")
    if "monthly_main.py:25" not in final_response:
        failures.append("review_location_mismatch:monthly_main.py:25")
    return failures


def monthly_review_rating(failures: list[str]) -> tuple[int, str] | None:
    review_failures = [item for item in failures if item.startswith("review_")]
    if not review_failures:
        return None
    missing_findings = [
        item for item in review_failures if item.startswith("review_response_missing:")
    ]
    if len(missing_findings) == 3:
        return 1, "no-drift境界は保ったが、要求された主要review findingを確認できなかった。"
    if review_failures == ["review_location_mismatch:monthly_main.py:25"]:
        return (
            3,
            "主要なreview findingは特定したが、指摘位置が実変更行と一致しなかった。",
        )
    return 2, "reviewの主要要素または正確な変更位置が不足した。"
