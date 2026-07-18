#!/usr/bin/env python3
"""Match contract-defined semantic response evidence without prompt-specific scoring."""

from __future__ import annotations

import json
import unicodedata
from pathlib import Path
from typing import Any


def load_contract(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"contract root must be an object: {path}")
    return value


def normalize(text: str) -> str:
    return unicodedata.normalize("NFKC", text).casefold()


def semantic_marker_failures(
    contract: dict[str, Any], case_id: str, final_response: str
) -> list[str]:
    response_evidence = contract.get("response_evidence", {})
    groups_by_case = response_evidence.get("semantic_marker_groups", {})
    groups = groups_by_case.get(case_id, {})
    if not isinstance(groups, dict):
        raise ValueError(f"semantic marker groups must be an object: {case_id}")

    normalized_response = normalize(final_response)
    failures: list[str] = []
    for concept, forms in groups.items():
        if not isinstance(forms, list) or not forms or not all(
            isinstance(form, str) and form for form in forms
        ):
            raise ValueError(f"semantic marker forms are invalid: {case_id}:{concept}")
        if not any(normalize(form) in normalized_response for form in forms):
            failures.append(f"response_concept_missing:{concept}")
    return failures
