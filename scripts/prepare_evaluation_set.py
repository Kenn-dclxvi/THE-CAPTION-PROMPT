#!/usr/bin/env python3
"""Prepare one Evaluation set capsule and its self-contained repository fixture."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path
from typing import Any

if __package__:
    from .prepare_case_fixture import FixtureError, load_object, prepare_fixture, require_string
else:
    from prepare_case_fixture import FixtureError, load_object, prepare_fixture, require_string


def write_json_once(path: Path, value: dict[str, Any]) -> None:
    try:
        with path.open("x", encoding="utf-8", newline="\n") as handle:
            json.dump(value, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
    except FileExistsError as exc:
        raise FixtureError(f"refusing to overwrite: {path}") from exc


def prepare_evaluation_set(case_root: Path, source_repo: Path, output: Path) -> dict[str, Any]:
    case_root = case_root.resolve()
    source_repo = source_repo.resolve()
    output = output.resolve()
    if output == source_repo or output.is_relative_to(source_repo):
        raise FixtureError("output must not be inside the source repository")
    if output == case_root or output.is_relative_to(case_root):
        raise FixtureError("output must not be inside the case revision")
    if output.exists():
        raise FixtureError(f"refusing to overwrite output: {output}")

    private_data = load_object(case_root / "private" / "case-data.json")
    trial_input = load_object(case_root / "trial-prompt-input.json")
    case_id = require_string(private_data.get("case_id"), "case_id")
    case_revision = require_string(private_data.get("case_revision"), "case_revision")
    set_id = f"{case_id.lower()}-{case_revision}"
    fixture = output / "fixture"
    set_file = output / "set.json"

    output.mkdir(parents=True)
    try:
        fixture_result = prepare_fixture(case_root, source_repo, fixture)
        capsule = {
            "schema_version": "the-caption-prompt.evaluation-set-source/v2",
            "set_id": set_id,
            "revision": case_revision,
            "cases": [
                {
                    "id": case_id,
                    "fixture": "fixture",
                    "case_revision": case_revision,
                    "fixture_condition_paths": fixture_result["seeded_paths"],
                    "payload": {"trial_prompt_input": trial_input},
                }
            ],
        }
        write_json_once(set_file, capsule)
    except Exception:
        if output.exists():
            shutil.rmtree(output)
        raise

    return {
        "set_id": set_id,
        "set_file": str(set_file),
        "fixture": fixture_result["fixture"],
        "case_id": case_id,
        "case_revision": case_revision,
    }


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--case", required=True, help="Case revision directory")
    result.add_argument("--source-repo", required=True, help="Local source Git repository")
    result.add_argument("--output", required=True, help="New Evaluation set directory")
    return result


def main() -> int:
    args = parser().parse_args()
    try:
        result = prepare_evaluation_set(Path(args.case), Path(args.source_repo), Path(args.output))
    except (FixtureError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
