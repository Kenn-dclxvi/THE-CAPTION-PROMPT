#!/usr/bin/env python3
"""Prepare one self-contained seeded repository fixture from a case revision."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import stat
import subprocess
import sys
from pathlib import Path
from typing import Any


class FixtureError(Exception):
    pass


def run(
    command: list[str],
    cwd: Path | None = None,
    binary: bool = False,
    env: dict[str, str] | None = None,
) -> str | bytes:
    completed = subprocess.run(command, cwd=cwd, env=env, capture_output=True, check=False)
    if completed.returncode != 0:
        detail = completed.stderr.decode("utf-8", errors="replace").strip()
        raise FixtureError(f"command failed ({completed.returncode}): {' '.join(command)}: {detail}")
    if binary:
        return completed.stdout
    return completed.stdout.decode("utf-8", errors="strict")


def load_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise FixtureError(f"missing case data: {path}") from exc
    except json.JSONDecodeError as exc:
        raise FixtureError(f"invalid case data JSON: {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise FixtureError("case data root must be an object")
    return value


def require_object(value: Any, name: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise FixtureError(f"{name} must be an object")
    return value


def require_string(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value:
        raise FixtureError(f"{name} must be a non-empty string")
    return value


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def resolve_case_path(case_root: Path, relative: str) -> Path:
    path = (case_root / relative).resolve()
    if not path.is_relative_to(case_root):
        raise FixtureError(f"case path escapes revision root: {relative}")
    return path


def read_tree_entry(workspace: Path, revision: str, path: str) -> tuple[str, str, str]:
    output = run(["git", "ls-tree", revision, "--", path], cwd=workspace)
    assert isinstance(output, str)
    line = output.strip()
    if not line:
        raise FixtureError(f"missing tracked path at {revision}: {path}")
    try:
        metadata, listed_path = line.split("\t", 1)
        mode, object_type, object_id = metadata.split(" ")
    except ValueError as exc:
        raise FixtureError(f"unexpected ls-tree output for {path}: {line}") from exc
    if listed_path != path:
        raise FixtureError(f"ls-tree path mismatch: expected {path}, got {listed_path}")
    return mode, object_type, object_id


def verify_preimages(workspace: Path, files: Any) -> None:
    if not isinstance(files, list) or not files:
        raise FixtureError("seed.application_contract.preimage_files must be a non-empty array")
    for index, raw_entry in enumerate(files):
        entry = require_object(raw_entry, f"preimage_files[{index}]")
        path = require_string(entry.get("path"), f"preimage_files[{index}].path")
        expected_mode = require_string(entry.get("mode"), f"preimage_files[{index}].mode")
        expected_blob = require_string(entry.get("git_blob_sha1"), f"preimage_files[{index}].git_blob_sha1")
        expected_sha256 = require_string(entry.get("raw_sha256"), f"preimage_files[{index}].raw_sha256")
        mode, object_type, blob = read_tree_entry(workspace, "HEAD", path)
        if object_type != "blob" or mode != expected_mode or blob != expected_blob:
            raise FixtureError(f"preimage Git identity mismatch: {path}")
        content = run(["git", "cat-file", "blob", blob], cwd=workspace, binary=True)
        assert isinstance(content, bytes)
        if sha256_bytes(content) != expected_sha256:
            raise FixtureError(f"preimage SHA-256 mismatch: {path}")


def working_tree_mode(path: Path) -> str:
    if not path.is_file():
        raise FixtureError(f"expected regular post-seed file: {path}")
    return "100755" if path.stat().st_mode & stat.S_IXUSR else "100644"


def verify_postimages(workspace: Path, files: Any) -> set[str]:
    if not isinstance(files, list) or not files:
        raise FixtureError("seed.expected_post_seed_files must be a non-empty array")
    expected_paths: set[str] = set()
    for index, raw_entry in enumerate(files):
        entry = require_object(raw_entry, f"expected_post_seed_files[{index}]")
        relative = require_string(entry.get("path"), f"expected_post_seed_files[{index}].path")
        expected_mode = require_string(entry.get("mode"), f"expected_post_seed_files[{index}].mode")
        expected_blob = require_string(entry.get("git_blob_sha1"), f"expected_post_seed_files[{index}].git_blob_sha1")
        expected_sha256 = require_string(entry.get("raw_sha256"), f"expected_post_seed_files[{index}].raw_sha256")
        path = (workspace / relative).resolve()
        if not path.is_relative_to(workspace):
            raise FixtureError(f"post-seed path escapes fixture: {relative}")
        if working_tree_mode(path) != expected_mode:
            raise FixtureError(f"post-seed mode mismatch: {relative}")
        blob = run(["git", "hash-object", "--", relative], cwd=workspace)
        assert isinstance(blob, str)
        if blob.strip() != expected_blob:
            raise FixtureError(f"post-seed Git blob mismatch: {relative}")
        if sha256_bytes(path.read_bytes()) != expected_sha256:
            raise FixtureError(f"post-seed SHA-256 mismatch: {relative}")
        expected_paths.add(relative)
    return expected_paths


def changed_paths(workspace: Path) -> set[str]:
    commands = [
        ["git", "diff", "--name-only", "--no-ext-diff"],
        ["git", "diff", "--cached", "--name-only", "--no-ext-diff"],
        ["git", "ls-files", "--others", "--exclude-standard"],
    ]
    paths: set[str] = set()
    for command in commands:
        output = run(command, cwd=workspace)
        assert isinstance(output, str)
        paths.update(line for line in output.splitlines() if line)
    return paths


def materialize_seed_state(
    workspace: Path,
    seed: dict[str, Any],
    seeded_paths: set[str],
    target_commit: str,
) -> tuple[str, str, set[str]]:
    raw_contract = seed.get("fixture_materialization")
    if raw_contract is None:
        head = run(["git", "rev-parse", "HEAD^{commit}"], cwd=workspace)
        tree = run(["git", "rev-parse", "HEAD^{tree}"], cwd=workspace)
        assert isinstance(head, str) and isinstance(tree, str)
        return head.strip(), tree.strip(), changed_paths(workspace)

    contract = require_object(raw_contract, "seed.fixture_materialization")
    mode = require_string(contract.get("mode"), "seed.fixture_materialization.mode")
    if mode != "committed_seed":
        raise FixtureError(f"unsupported seed fixture materialization mode: {mode}")
    commit = require_object(contract.get("commit"), "seed.fixture_materialization.commit")
    message = require_string(commit.get("message"), "seed.fixture_materialization.commit.message")
    timestamp = require_string(commit.get("timestamp"), "seed.fixture_materialization.commit.timestamp")
    author_name = require_string(commit.get("author_name"), "seed.fixture_materialization.commit.author_name")
    author_email = require_string(commit.get("author_email"), "seed.fixture_materialization.commit.author_email")

    run(["git", "add", "--", *sorted(seeded_paths)], cwd=workspace)
    staged = run(["git", "diff", "--cached", "--name-only", "--no-ext-diff"], cwd=workspace)
    assert isinstance(staged, str)
    if set(staged.splitlines()) != seeded_paths:
        raise FixtureError("seed commit staged paths do not match expected post-seed paths")
    env = os.environ.copy()
    env.update(
        {
            "GIT_AUTHOR_DATE": timestamp,
            "GIT_AUTHOR_EMAIL": author_email,
            "GIT_AUTHOR_NAME": author_name,
            "GIT_COMMITTER_DATE": timestamp,
            "GIT_COMMITTER_EMAIL": author_email,
            "GIT_COMMITTER_NAME": author_name,
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
            message,
        ],
        cwd=workspace,
        env=env,
    )
    head = run(["git", "rev-parse", "HEAD^{commit}"], cwd=workspace)
    tree = run(["git", "rev-parse", "HEAD^{tree}"], cwd=workspace)
    parent = run(["git", "rev-parse", "HEAD^1"], cwd=workspace)
    assert isinstance(head, str) and isinstance(tree, str) and isinstance(parent, str)
    if parent.strip() != target_commit:
        raise FixtureError("seed commit parent does not match target commit")
    expected_commit = commit.get("expected_commit")
    expected_tree = commit.get("expected_tree")
    if expected_commit is not None and head.strip() != require_string(expected_commit, "expected_commit"):
        raise FixtureError("seed commit identity mismatch")
    if expected_tree is not None and tree.strip() != require_string(expected_tree, "expected_tree"):
        raise FixtureError("seed tree identity mismatch")
    remaining = changed_paths(workspace)
    if remaining:
        raise FixtureError(f"committed seed fixture is not clean: {sorted(remaining)}")
    return head.strip(), tree.strip(), remaining


def prepare_fixture(case_root: Path, source_repo: Path, output: Path) -> dict[str, Any]:
    case_root = case_root.resolve()
    source_repo = source_repo.resolve()
    output = output.resolve()
    data = load_object(case_root / "private" / "case-data.json")
    seed = require_object(data.get("seed"), "seed")
    artifact = require_object(seed.get("artifact"), "seed.artifact")
    application = require_object(seed.get("application_contract"), "seed.application_contract")
    patch_relative = require_string(artifact.get("path"), "seed.artifact.path")
    patch = resolve_case_path(case_root, patch_relative)
    if artifact.get("format") != "git_diff":
        raise FixtureError("seed.artifact.format must be git_diff")
    if sha256_bytes(patch.read_bytes()) != require_string(artifact.get("raw_sha256"), "seed.artifact.raw_sha256"):
        raise FixtureError("seed patch SHA-256 mismatch")
    target_commit = require_string(application.get("target_commit"), "seed.application_contract.target_commit")
    target_tree = require_string(application.get("target_tree"), "seed.application_contract.target_tree")

    if output == source_repo or output.is_relative_to(source_repo):
        raise FixtureError("output must not be inside the source repository")
    if output == case_root or output.is_relative_to(case_root):
        raise FixtureError("output must not be inside the case revision")
    if output.exists():
        raise FixtureError(f"refusing to overwrite output: {output}")
    output.parent.mkdir(parents=True, exist_ok=True)
    try:
        run(["git", "-C", str(source_repo), "cat-file", "-e", f"{target_commit}^{{commit}}"])
        run(["git", "clone", "--no-local", "--no-checkout", "--", str(source_repo), str(output)])
        run(["git", "checkout", "--detach", target_commit], cwd=output)
        run(["git", "remote", "remove", "origin"], cwd=output)
        head = run(["git", "rev-parse", "HEAD^{commit}"], cwd=output)
        tree = run(["git", "rev-parse", "HEAD^{tree}"], cwd=output)
        assert isinstance(head, str) and isinstance(tree, str)
        if head.strip() != target_commit or tree.strip() != target_tree:
            raise FixtureError("cloned target identity mismatch")
        verify_preimages(output, application.get("preimage_files"))
        run(["git", "apply", "--check", str(patch)], cwd=output)
        run(["git", "apply", str(patch)], cwd=output)
        expected_paths = verify_postimages(output, seed.get("expected_post_seed_files"))
        actual_paths = changed_paths(output)
        if actual_paths != expected_paths:
            raise FixtureError(
                f"fixture drift mismatch: expected {sorted(expected_paths)}, got {sorted(actual_paths)}"
            )
        fixture_head, fixture_tree, final_changed_paths = materialize_seed_state(
            output,
            seed,
            expected_paths,
            target_commit,
        )
        remotes = run(["git", "remote"], cwd=output)
        assert isinstance(remotes, str)
        if remotes.strip():
            raise FixtureError("fixture must not retain Git remotes")
        alternates = output / ".git" / "objects" / "info" / "alternates"
        if alternates.exists() and alternates.read_text(encoding="utf-8").strip():
            raise FixtureError("fixture must not depend on an alternate object database")
    except Exception:
        if output.exists():
            shutil.rmtree(output)
        raise

    return {
        "case_id": require_string(data.get("case_id"), "case_id"),
        "case_revision": require_string(data.get("case_revision"), "case_revision"),
        "fixture": str(output),
        "target_commit": target_commit,
        "target_tree": target_tree,
        "seeded_paths": sorted(actual_paths),
        "changed_paths": sorted(final_changed_paths),
        "fixture_head_commit": fixture_head,
        "fixture_head_tree": fixture_tree,
    }


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--case", required=True, help="Case revision directory")
    result.add_argument("--source-repo", required=True, help="Local source Git repository")
    result.add_argument("--output", required=True, help="New fixture directory")
    return result


def main() -> int:
    args = parser().parse_args()
    try:
        result = prepare_fixture(Path(args.case), Path(args.source_repo), Path(args.output))
    except (FixtureError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
