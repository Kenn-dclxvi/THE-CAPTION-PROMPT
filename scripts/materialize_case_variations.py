#!/usr/bin/env python3
"""Materialize prompt-evaluation case designs as pinned file-bundle fixtures."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import stat
import subprocess
import tempfile
from pathlib import Path
from typing import Any


SEED_TIMESTAMP = "2000-01-01T00:00:00Z"
SEED_AUTHOR_NAME = "THE-CAPTION Prompt Evaluation"
SEED_AUTHOR_EMAIL = "evaluation@example.invalid"


class MaterializationError(Exception):
    pass


def run(
    command: list[str],
    *,
    cwd: Path,
    binary: bool = False,
    env: dict[str, str] | None = None,
) -> str | bytes:
    completed = subprocess.run(command, cwd=cwd, env=env, capture_output=True, check=False)
    if completed.returncode != 0:
        stderr = completed.stderr.decode("utf-8", errors="replace").strip()
        raise MaterializationError(
            f"command failed ({completed.returncode}): {' '.join(command)}: {stderr}"
        )
    if binary:
        return completed.stdout
    return completed.stdout.decode("utf-8", errors="strict")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def git_show(repo: Path, revision: str, path: str) -> bytes:
    value = run(["git", "show", f"{revision}:{path}"], cwd=repo, binary=True)
    assert isinstance(value, bytes)
    return value


def require_object(value: Any, name: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise MaterializationError(f"{name} must be an object")
    return value


def require_string(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value:
        raise MaterializationError(f"{name} must be a non-empty string")
    return value


def tree_entry(repo: Path, revision: str, path: str) -> tuple[str, str, str]:
    output = run(["git", "ls-tree", revision, "--", path], cwd=repo)
    assert isinstance(output, str)
    line = output.strip()
    if not line:
        raise MaterializationError(f"missing target path: {path}")
    metadata, listed_path = line.split("\t", 1)
    mode, kind, object_id = metadata.split(" ")
    if listed_path != path or kind != "blob":
        raise MaterializationError(f"unexpected target tree entry: {path}")
    return mode, kind, object_id


def complete_source_identities(data: dict[str, Any], target_repo: Path, commit: str) -> None:
    fixture = require_object(data.get("fixture"), "fixture")
    source_files = fixture.get("source_files")
    if not isinstance(source_files, list) or not source_files:
        raise MaterializationError("fixture.source_files must be a non-empty array")
    for index, raw_entry in enumerate(source_files):
        entry = require_object(raw_entry, f"fixture.source_files[{index}]")
        path = require_string(entry.get("path"), f"fixture.source_files[{index}].path")
        mode, _, blob = tree_entry(target_repo, commit, path)
        if entry.get("mode") != mode or entry.get("git_blob_sha1") != blob:
            raise MaterializationError(f"source identity differs from target commit: {path}")
        content = run(["git", "cat-file", "blob", blob], cwd=target_repo, binary=True)
        assert isinstance(content, bytes)
        digest = sha256_bytes(content)
        if entry.get("raw_sha256") not in {None, digest}:
            raise MaterializationError(f"source SHA-256 differs from target commit: {path}")
        entry["raw_sha256"] = digest


def apply_operations(workspace: Path, operations: list[Any], commit: str) -> list[str]:
    paths: list[str] = []
    verified_paths: set[str] = set()
    for index, raw_operation in enumerate(operations):
        operation = require_object(raw_operation, f"seed.operations[{index}]")
        if operation.get("operation") != "replace_exact_text":
            raise MaterializationError(f"unsupported seed operation: {operation.get('operation')}")
        relative = require_string(operation.get("path"), f"seed.operations[{index}].path")
        expected_blob = require_string(
            operation.get("expected_preimage_blob"),
            f"seed.operations[{index}].expected_preimage_blob",
        )
        if relative not in verified_paths:
            actual_blob = run(["git", "rev-parse", f"{commit}:{relative}"], cwd=workspace)
            assert isinstance(actual_blob, str)
            if actual_blob.strip() != expected_blob:
                raise MaterializationError(f"operation preimage differs from target commit: {relative}")
            verified_paths.add(relative)
        expected_occurrences = operation.get("expected_occurrences")
        if not isinstance(expected_occurrences, int) or expected_occurrences < 1:
            raise MaterializationError(f"invalid expected occurrence count: {relative}")
        before = require_string(operation.get("before_text"), f"seed.operations[{index}].before_text")
        after = operation.get("after_text")
        if not isinstance(after, str):
            raise MaterializationError(f"seed.operations[{index}].after_text must be a string")
        path = workspace / relative
        content = path.read_text(encoding="utf-8")
        if content.count(before) != expected_occurrences:
            raise MaterializationError(f"operation occurrence count differs: {relative}")
        path.write_text(content.replace(before, after), encoding="utf-8")
        if relative not in paths:
            paths.append(relative)
    return paths


def file_identity(workspace: Path, path: str) -> dict[str, str]:
    resolved = workspace / path
    mode = "100755" if resolved.stat().st_mode & stat.S_IXUSR else "100644"
    blob = run(["git", "hash-object", "--", path], cwd=workspace)
    assert isinstance(blob, str)
    return {
        "path": path,
        "mode": mode,
        "git_blob_sha1": blob.strip(),
        "raw_sha256": sha256_bytes(resolved.read_bytes()),
    }


def source_identity_by_path(data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    fixture = require_object(data.get("fixture"), "fixture")
    source_files = fixture.get("source_files")
    assert isinstance(source_files, list)
    return {
        require_string(entry.get("path"), "fixture.source_files.path"): entry
        for entry in source_files
        if isinstance(entry, dict)
    }


def deterministic_seed_commit(workspace: Path, paths: list[str]) -> tuple[str, str]:
    run(["git", "add", "--", *paths], cwd=workspace)
    env = os.environ.copy()
    env.update(
        {
            "GIT_AUTHOR_DATE": SEED_TIMESTAMP,
            "GIT_AUTHOR_EMAIL": SEED_AUTHOR_EMAIL,
            "GIT_AUTHOR_NAME": SEED_AUTHOR_NAME,
            "GIT_COMMITTER_DATE": SEED_TIMESTAMP,
            "GIT_COMMITTER_EMAIL": SEED_AUTHOR_EMAIL,
            "GIT_COMMITTER_NAME": SEED_AUTHOR_NAME,
        }
    )
    run(
        [
            "git",
            "-c",
            "commit.gpgsign=false",
            "commit",
            "--no-verify",
            "-qm",
            "evaluation fixture seed",
        ],
        cwd=workspace,
        env=env,
    )
    commit = run(["git", "rev-parse", "HEAD^{commit}"], cwd=workspace)
    tree = run(["git", "rev-parse", "HEAD^{tree}"], cwd=workspace)
    assert isinstance(commit, str) and isinstance(tree, str)
    return commit.strip(), tree.strip()


def materialize_case(
    source_repo: Path,
    source_ref: str,
    source_root: str,
    target_repo: Path,
    output_root: Path,
    case_id: str,
) -> dict[str, Any]:
    case_source = f"{source_root}/cases/{case_id}/r1"
    trial_path = f"{case_source}/trial-prompt-input.json"
    private_path = f"{case_source}/private/case-data.json"
    trial_bytes = git_show(source_repo, source_ref, trial_path)
    private_bytes = git_show(source_repo, source_ref, private_path)
    try:
        data = json.loads(private_bytes)
    except json.JSONDecodeError as exc:
        raise MaterializationError(f"invalid upstream case JSON: {case_id}: {exc}") from exc
    if not isinstance(data, dict) or data.get("case_id") != case_id:
        raise MaterializationError(f"upstream case identity mismatch: {case_id}")

    fixture = require_object(data.get("fixture"), "fixture")
    target = require_object(fixture.get("target_identity"), "fixture.target_identity")
    target_commit = require_string(target.get("commit"), "fixture.target_identity.commit")
    target_tree = require_string(target.get("tree"), "fixture.target_identity.tree")
    actual_tree = run(["git", "rev-parse", f"{target_commit}^{{tree}}"], cwd=target_repo)
    assert isinstance(actual_tree, str)
    if actual_tree.strip() != target_tree:
        raise MaterializationError(f"target tree mismatch: {case_id}")
    complete_source_identities(data, target_repo, target_commit)

    source_commit = run(["git", "rev-parse", f"{source_ref}^{{commit}}"], cwd=source_repo)
    assert isinstance(source_commit, str)
    data["materialization_source"] = {
        "repository": "Kenn-dclxvi/ai-development-research",
        "commit": source_commit.strip(),
        "case_data_path": private_path,
        "case_data_raw_sha256": sha256_bytes(private_bytes),
        "trial_prompt_input_path": trial_path,
        "trial_prompt_input_raw_sha256": sha256_bytes(trial_bytes),
    }

    seed = require_object(data.get("seed"), "seed")
    operations = seed.get("operations")
    if not isinstance(operations, list):
        raise MaterializationError("seed.operations must be an array")
    seed["design_operations"] = operations
    del seed["operations"]

    output = output_root / case_id / "r1"
    if output.exists():
        raise MaterializationError(f"refusing to overwrite case revision: {output}")
    private_output = output / "private"
    private_output.mkdir(parents=True)
    try:
        if operations:
            with tempfile.TemporaryDirectory(prefix=f"{case_id}-") as temporary:
                workspace = Path(temporary) / "fixture"
                run(
                    [
                        "git",
                        "clone",
                        "--no-local",
                        "--no-checkout",
                        "--",
                        str(target_repo),
                        str(workspace),
                    ],
                    cwd=target_repo.parent,
                )
                run(["git", "checkout", "--detach", target_commit], cwd=workspace)
                changed_paths = apply_operations(workspace, operations, target_commit)
                diff = run(
                    ["git", "diff", "--binary", "--full-index", "--no-ext-diff", "--", *changed_paths],
                    cwd=workspace,
                    binary=True,
                )
                assert isinstance(diff, bytes)
                if not diff:
                    raise MaterializationError(f"seed operations produced no diff: {case_id}")
                patch_path = private_output / "seed.patch"
                patch_path.write_bytes(diff)
                identities = source_identity_by_path(data)
                preimages = []
                for path in changed_paths:
                    if path not in identities:
                        raise MaterializationError(f"changed path missing from source_files: {path}")
                    entry = identities[path]
                    preimages.append(
                        {
                            key: entry[key]
                            for key in ("path", "mode", "git_blob_sha1", "raw_sha256")
                        }
                    )
                postimages = [file_identity(workspace, path) for path in changed_paths]
                seed_commit, seed_tree = deterministic_seed_commit(workspace, changed_paths)
            seed["status"] = "materialized_not_applied"
            seed["artifact"] = {
                "path": "private/seed.patch",
                "format": "git_diff",
                "raw_sha256": sha256_bytes(diff),
            }
            seed["application_contract"] = {
                "target_commit": target_commit,
                "target_tree": target_tree,
                "preimage_files": preimages,
                "check": "resolve artifact.path from the case revision root and run git apply --check before applying",
                "apply": "apply the same resolved patch only after every identity and preimage check passes",
                "failure_mode": "fail_closed_no_partial_fixture",
            }
            seed["expected_post_seed_files"] = postimages
            seed["fixture_materialization"] = {
                "mode": "committed_seed",
                "commit": {
                    "message": "evaluation fixture seed",
                    "timestamp": SEED_TIMESTAMP,
                    "author_name": SEED_AUTHOR_NAME,
                    "author_email": SEED_AUTHOR_EMAIL,
                    "expected_commit": seed_commit,
                    "expected_tree": seed_tree,
                },
            }
        else:
            seed["status"] = "clean_checkout"
            seed["fixture_materialization"] = {"mode": "clean_checkout"}

        (output / "trial-prompt-input.json").write_bytes(trial_bytes)
        (private_output / "case-data.json").write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    except Exception:
        if output.exists():
            shutil.rmtree(output)
        raise

    return {
        "case_id": case_id,
        "output": str(output),
        "trial_prompt_input_raw_sha256": sha256_bytes(trial_bytes),
        "seed_mode": seed["fixture_materialization"]["mode"],
        "seed_patch_raw_sha256": seed.get("artifact", {}).get("raw_sha256"),
    }


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--source-repo", required=True)
    result.add_argument("--source-ref", default="origin/main")
    result.add_argument(
        "--source-root",
        default="packages/the-caption/prompt-evaluation",
    )
    result.add_argument("--target-repo", required=True)
    result.add_argument("--output-root", required=True)
    result.add_argument("case_ids", nargs="+")
    return result


def main() -> int:
    args = parser().parse_args()
    try:
        results = [
            materialize_case(
                Path(args.source_repo).resolve(),
                args.source_ref,
                args.source_root,
                Path(args.target_repo).resolve(),
                Path(args.output_root).resolve(),
                case_id,
            )
            for case_id in args.case_ids
        ]
    except (MaterializationError, OSError) as exc:
        print(f"error: {exc}")
        return 2
    print(json.dumps(results, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
