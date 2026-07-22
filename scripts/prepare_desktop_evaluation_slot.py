#!/usr/bin/env python3
"""Prepare one reusable Codex Desktop evaluation workspace slot."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any

if __package__:
    from .export_prompt_bundle import BundleError, verify_bundle
    from .run_codex_evaluation import (
        AdapterError,
        changed_paths,
        overlay_bundle,
        prepare_runtime_links,
        prompt_overlay_commit,
    )
else:
    from export_prompt_bundle import BundleError, verify_bundle
    from run_codex_evaluation import (
        AdapterError,
        changed_paths,
        overlay_bundle,
        prepare_runtime_links,
        prompt_overlay_commit,
    )


SCHEMA_VERSION = "the-caption-prompt.desktop-evaluation-slot/v1"
MARKER_NAME = "the-caption-prompt-desktop-evaluation-slot.json"


class DesktopSlotError(ValueError):
    """Raised when a Desktop evaluation slot cannot be prepared safely."""


def git(workspace: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=workspace,
        capture_output=True,
        check=False,
        text=True,
    )
    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip()
        raise DesktopSlotError(f"git {' '.join(args)} failed: {detail}")
    return completed.stdout.strip()


def git_dir(workspace: Path) -> Path:
    raw = git(workspace, "rev-parse", "--git-dir")
    path = Path(raw)
    if not path.is_absolute():
        path = workspace / path
    return path.resolve()


def marker_path(workspace: Path) -> Path:
    return git_dir(workspace) / "info" / MARKER_NAME


def load_marker(workspace: Path) -> dict[str, Any]:
    path = marker_path(workspace)
    try:
        marker = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        raise DesktopSlotError(
            f"refusing to reuse an unmanaged workspace: {workspace}"
        ) from exc
    if not isinstance(marker, dict) or marker.get("schema_version") != SCHEMA_VERSION:
        raise DesktopSlotError(f"unsupported Desktop slot marker: {path}")
    if marker.get("workspace") != str(workspace):
        raise DesktopSlotError("Desktop slot marker workspace does not match its location")
    return marker


def write_marker(workspace: Path, marker: dict[str, Any]) -> None:
    path = marker_path(workspace)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp")
    temporary.write_text(
        json.dumps(marker, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def safe_target(raw_target: Any) -> PurePosixPath:
    if not isinstance(raw_target, str) or not raw_target:
        raise DesktopSlotError("runtime receipt target must be a non-empty string")
    target = PurePosixPath(raw_target)
    if target.is_absolute() or target.as_posix() != raw_target or ".." in target.parts:
        raise DesktopSlotError(f"unsafe runtime receipt target: {raw_target}")
    return target


def remove_owned_runtime_links(workspace: Path, marker: dict[str, Any]) -> None:
    receipts = marker.get("runtime_links", [])
    if not isinstance(receipts, list):
        raise DesktopSlotError("Desktop slot runtime_links marker must be an array")
    for receipt in receipts:
        if not isinstance(receipt, dict):
            raise DesktopSlotError("Desktop slot runtime receipt must be an object")
        relative = safe_target(receipt.get("target"))
        destination = workspace.joinpath(*relative.parts)
        if not destination.is_relative_to(workspace):
            raise DesktopSlotError("runtime receipt escapes the Desktop slot")
        if destination.is_symlink() or destination.is_file():
            destination.unlink()
        elif destination.is_dir():
            shutil.rmtree(destination)


def ensure_commit(workspace: Path, source_repo: Path, commit: str) -> None:
    present = subprocess.run(
        ["git", "cat-file", "-e", f"{commit}^{{commit}}"],
        cwd=workspace,
        capture_output=True,
        check=False,
    )
    if present.returncode == 0:
        return
    git(workspace, "fetch", "--no-tags", "--quiet", str(source_repo), commit)


def initialize_workspace(source_repo: Path, workspace: Path) -> None:
    if workspace.exists():
        raise DesktopSlotError(f"refusing to initialize over an existing path: {workspace}")
    workspace.parent.mkdir(parents=True, exist_ok=True)
    completed = subprocess.run(
        ["git", "clone", "--no-local", "--no-checkout", str(source_repo), str(workspace)],
        capture_output=True,
        check=False,
        text=True,
    )
    if completed.returncode != 0:
        if workspace.exists():
            shutil.rmtree(workspace)
        detail = completed.stderr.strip() or completed.stdout.strip()
        raise DesktopSlotError(f"failed to initialize Desktop slot: {detail}")


def prepare_desktop_slot(
    *,
    source_repo: Path,
    workspace: Path,
    target_commit: str,
    target_tree: str,
    prompt_bundle: Path,
    bundle_sha256: str,
    runtime_links: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    source_repo = source_repo.resolve()
    workspace = workspace.resolve()
    prompt_bundle = prompt_bundle.resolve()
    if not (source_repo / ".git").exists():
        raise DesktopSlotError(f"source repository is not a Git checkout: {source_repo}")
    if workspace == source_repo or workspace.is_relative_to(source_repo):
        raise DesktopSlotError("Desktop slot must be outside the source repository")

    previous_marker: dict[str, Any] | None = None
    if workspace.exists():
        previous_marker = load_marker(workspace)
        if changed_paths(workspace):
            raise DesktopSlotError("refusing to reuse a dirty Desktop slot")
        remove_owned_runtime_links(workspace, previous_marker)
    else:
        initialize_workspace(source_repo, workspace)

    ensure_commit(workspace, source_repo, target_commit)
    git(workspace, "checkout", "--detach", "--quiet", target_commit)
    actual_target_commit = git(workspace, "rev-parse", "HEAD^{commit}")
    actual_target_tree = git(workspace, "rev-parse", "HEAD^{tree}")
    if actual_target_commit != target_commit or actual_target_tree != target_tree:
        raise DesktopSlotError("Desktop slot target identity does not match the requested ref")
    if changed_paths(workspace):
        raise DesktopSlotError("Desktop slot is dirty after target checkout")

    manifest = verify_bundle(prompt_bundle)
    if manifest.get("bundle_sha256") != bundle_sha256:
        raise DesktopSlotError("prompt bundle identity does not match bundle_sha256")
    targets = overlay_bundle(workspace, prompt_bundle, manifest)
    overlay_commit, overlay_tree = prompt_overlay_commit(workspace, targets)
    prepared_runtime_links = prepare_runtime_links(workspace, runtime_links or [])
    if changed_paths(workspace):
        raise DesktopSlotError("prepared Desktop slot is not clean")

    receipt = {
        "schema_version": SCHEMA_VERSION,
        "workspace": str(workspace),
        "source_repository": str(source_repo),
        "target_commit": actual_target_commit,
        "target_tree": actual_target_tree,
        "prompt_set_identity": {
            "name": manifest.get("prompt_identity"),
            "bundle_sha256": bundle_sha256,
        },
        "prompt_overlay_commit": overlay_commit,
        "prompt_overlay_tree": overlay_tree,
        "runtime_links": prepared_runtime_links,
        "prepared_at": datetime.now(timezone.utc).isoformat(),
        "model_context_gate": {
            "required_user_config": {"features.memories": False},
            "required_memory_instructions": "absent",
        },
        "codex_app_command": [
            "codex",
            "app",
            str(workspace),
        ],
    }
    write_marker(workspace, receipt)
    return receipt


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--source-repo", required=True)
    result.add_argument("--workspace", required=True)
    result.add_argument("--target-commit", required=True)
    result.add_argument("--target-tree", required=True)
    result.add_argument("--prompt-bundle", required=True)
    result.add_argument("--bundle-sha256", required=True)
    result.add_argument("--runtime-source")
    result.add_argument("--runtime-target", default=".venv")
    result.add_argument("--runtime-identity-file")
    result.add_argument("--runtime-identity-sha256")
    result.add_argument(
        "--runtime-materialization",
        choices=("symlink", "copy", "venv_shim"),
        default="venv_shim",
    )
    result.add_argument("--runtime-python-version")
    return result


def runtime_links_from_args(args: argparse.Namespace) -> list[dict[str, Any]]:
    values = [
        args.runtime_source,
        args.runtime_identity_file,
        args.runtime_identity_sha256,
    ]
    if not any(values):
        return []
    if not all(values):
        raise DesktopSlotError(
            "runtime source, identity file, and identity SHA-256 must be specified together"
        )
    link: dict[str, Any] = {
        "source": args.runtime_source,
        "target": args.runtime_target,
        "identity_file": args.runtime_identity_file,
        "identity_sha256": args.runtime_identity_sha256,
        "materialization": args.runtime_materialization,
    }
    if args.runtime_python_version is not None:
        link["python_version"] = args.runtime_python_version
    return [link]


def main() -> int:
    args = parser().parse_args()
    try:
        receipt = prepare_desktop_slot(
            source_repo=Path(args.source_repo),
            workspace=Path(args.workspace),
            target_commit=args.target_commit,
            target_tree=args.target_tree,
            prompt_bundle=Path(args.prompt_bundle),
            bundle_sha256=args.bundle_sha256,
            runtime_links=runtime_links_from_args(args),
        )
    except (AdapterError, BundleError, DesktopSlotError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(receipt, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
