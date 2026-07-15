#!/usr/bin/env python3
"""Audit verification storage and remove only expired, unreferenced scratch runs."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import stat
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPORT_SCHEMA = "the-caption-prompt.storage-audit/v1"
MANIFEST_SCHEMA = "the-caption-prompt.storage-gc-manifest/v1"
RECEIPT_SCHEMA = "the-caption-prompt.storage-gc-receipt/v1"
PACK_MANIFEST_SCHEMA = "the-caption-prompt.storage-pack-dedup-manifest/v1"
PACK_RECEIPT_SCHEMA = "the-caption-prompt.storage-pack-dedup-receipt/v1"
TEXT_SUFFIXES = {
    ".json",
    ".md",
    ".py",
    ".sh",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}


class StorageError(Exception):
    pass


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def canonical_json(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, separators=(",", ":"), sort_keys=True
    ).encode("utf-8")


def identity_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_json(value)).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise StorageError(f"missing file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise StorageError(f"invalid JSON: {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise StorageError(f"JSON root must be an object: {path}")
    return value


def write_json_once(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("x", encoding="utf-8", newline="\n") as handle:
            json.dump(value, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
    except FileExistsError as exc:
        raise StorageError(f"refusing to overwrite: {path}") from exc


def allocated_bytes(path: Path) -> int:
    completed = subprocess.run(
        ["du", "-sk", str(path)], capture_output=True, check=False, text=True
    )
    if completed.returncode != 0:
        raise StorageError(completed.stderr.strip() or f"du failed: {path}")
    try:
        return int(completed.stdout.split()[0]) * 1024
    except (IndexError, ValueError) as exc:
        raise StorageError(f"unexpected du output for {path}") from exc


def repository_text(repository: Path) -> list[tuple[str, str]]:
    result: list[tuple[str, str]] = []
    for directory, names, files in os.walk(repository, followlinks=False):
        names[:] = [name for name in names if name != ".git"]
        base = Path(directory)
        for name in files:
            path = base / name
            if path.suffix.lower() not in TEXT_SUFFIXES:
                continue
            try:
                if path.stat().st_size > 4 * 1024 * 1024:
                    continue
                result.append(
                    (path.relative_to(repository).as_posix(), path.read_text(encoding="utf-8"))
                )
            except (OSError, UnicodeDecodeError):
                continue
    return result


def path_within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


def inbound_symlinks(root: Path, runs: list[Path]) -> dict[Path, list[str]]:
    result = {run: [] for run in runs}
    for directory, names, files in os.walk(root, followlinks=False):
        base = Path(directory)
        entries = [base / name for name in (*names, *files)]
        names[:] = [name for name in names if not (base / name).is_symlink()]
        for link in entries:
            if not link.is_symlink():
                continue
            try:
                target = (link.parent / os.readlink(link)).resolve(strict=False)
            except OSError:
                continue
            for run in runs:
                if path_within(target, run) and not path_within(link, run):
                    result[run].append(link.relative_to(root).as_posix())
    return result


def scan_run(run: Path) -> dict[str, Any]:
    newest = run.lstat().st_mtime
    file_count = 0
    pack_files: list[tuple[str, int]] = []
    registrations: list[str] = []
    for directory, names, files in os.walk(run, followlinks=False):
        base = Path(directory)
        for name in (*names, *files):
            path = base / name
            try:
                metadata = path.lstat()
            except FileNotFoundError:
                continue
            if stat.S_ISREG(metadata.st_mode):
                newest = max(newest, metadata.st_mtime)
                file_count += 1
                relative = path.relative_to(run)
                if (
                    name.startswith("pack-")
                    and name.endswith(".pack")
                    and ".git" in relative.parts
                    and "objects" in relative.parts
                    and "pack" in relative.parts
                ):
                    pack_files.append((name, metadata.st_size))
                if name == "result-registration.json" and path.parent.name == "layer4":
                    registrations.append(relative.as_posix())
            elif stat.S_ISLNK(metadata.st_mode):
                newest = max(newest, metadata.st_mtime)
    return {
        "allocated_bytes": allocated_bytes(run),
        "file_count": file_count,
        "newest_mtime": newest,
        "pack_files": pack_files,
        "registrations": sorted(registrations),
    }


def audit_storage(
    root: Path, repository: Path, scratch_days: int, soft_limit_gib: float, hard_limit_gib: float
) -> dict[str, Any]:
    root = root.resolve()
    repository = repository.resolve()
    runs_root = root / "runs"
    if not root.is_dir() or not runs_root.is_dir():
        raise StorageError(f"storage root must contain runs/: {root}")
    if not repository.is_dir():
        raise StorageError(f"repository must be a directory: {repository}")
    if scratch_days < 0:
        raise StorageError("scratch-days must be zero or greater")
    if soft_limit_gib <= 0 or hard_limit_gib < soft_limit_gib:
        raise StorageError("limits must satisfy 0 < soft-limit-gib <= hard-limit-gib")

    runs = sorted(
        path for path in runs_root.iterdir() if path.is_dir() and not path.is_symlink()
    )
    text_files = repository_text(repository)
    links = inbound_symlinks(root, runs)
    now = datetime.now(timezone.utc).timestamp()
    all_packs: list[tuple[str, int]] = []
    run_reports: list[dict[str, Any]] = []
    candidates: list[str] = []
    for run in runs:
        scanned = scan_run(run)
        references = [name for name, content in text_files if str(run) in content]
        age_days = max(0.0, (now - scanned["newest_mtime"]) / 86400)
        protected_by: list[str] = []
        if references:
            protected_by.append("repository_reference")
        if links[run]:
            protected_by.append("inbound_symlink")
        if scanned["registrations"]:
            protected_by.append("result_registration")
        eligible = not protected_by and age_days >= scratch_days
        relative = run.relative_to(root).as_posix()
        if eligible:
            candidates.append(relative)
        all_packs.extend(scanned["pack_files"])
        run_reports.append(
            {
                "path": relative,
                "allocated_bytes": scanned["allocated_bytes"],
                "file_count": scanned["file_count"],
                "age_days": round(age_days, 3),
                "repository_references": references,
                "inbound_symlinks": links[run],
                "result_registrations": scanned["registrations"],
                "protected_by": protected_by,
                "gc_eligible": eligible,
            }
        )

    pack_total = sum(size for _, size in all_packs)
    unique_packs: dict[str, int] = {}
    for name, size in all_packs:
        unique_packs[name] = max(size, unique_packs.get(name, 0))
    pack_unique = sum(unique_packs.values())
    total = allocated_bytes(root)
    soft = int(soft_limit_gib * 1024**3)
    hard = int(hard_limit_gib * 1024**3)
    usage_state = (
        "above_hard_limit" if total > hard else "above_soft_limit" if total > soft else "within_soft_limit"
    )
    disk = shutil.disk_usage(root)
    return {
        "schema_version": REPORT_SCHEMA,
        "generated_at": utc_now(),
        "root": str(root),
        "repository": str(repository),
        "policy": {
            "scratch_days": scratch_days,
            "soft_limit_bytes": soft,
            "hard_limit_bytes": hard,
            "registered_or_referenced_runs_are_automatic_gc_ineligible": True,
        },
        "storage": {
            "allocated_bytes": total,
            "usage_state": usage_state,
            "filesystem_total_bytes": disk.total,
            "filesystem_free_bytes": disk.free,
        },
        "git_pack_duplication": {
            "file_count": len(all_packs),
            "total_bytes": pack_total,
            "unique_name_count": len(unique_packs),
            "unique_name_bytes": pack_unique,
            "duplicate_name_bytes": max(0, pack_total - pack_unique),
        },
        "runs": run_reports,
        "gc_candidates": candidates,
        "gc_candidate_bytes": sum(
            item["allocated_bytes"] for item in run_reports if item["gc_eligible"]
        ),
    }


def tree_fingerprint(root: Path) -> str:
    digest = hashlib.sha256()
    for directory, names, files in os.walk(root, followlinks=False):
        names.sort()
        files.sort()
        base = Path(directory)
        for name in (*names, *files):
            path = base / name
            relative = path.relative_to(root).as_posix()
            metadata = path.lstat()
            mode = metadata.st_mode & 0o777
            if path.is_symlink():
                header = [relative, "symlink", str(mode), os.readlink(path)]
                digest.update(canonical_json(header))
            elif path.is_dir():
                digest.update(canonical_json([relative, "directory", str(mode)]))
            elif path.is_file():
                digest.update(canonical_json([relative, "file", str(mode), metadata.st_size]))
                with path.open("rb") as handle:
                    for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                        digest.update(chunk)
            else:
                raise StorageError(f"unsupported entry while fingerprinting: {path}")
    return digest.hexdigest()


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(4 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def discover_pack_groups(root: Path) -> list[list[Path]]:
    groups: dict[tuple[str, int], list[Path]] = {}
    for path in (root / "runs").rglob("pack-*.pack"):
        if path.is_symlink() or not path.is_file():
            continue
        relative = path.relative_to(root)
        if ".git" not in relative.parts or "objects" not in relative.parts:
            continue
        groups.setdefault((path.name, path.stat().st_size), []).append(path)
    return [sorted(paths) for paths in groups.values() if len(paths) > 1]


def pack_dedup_manifest(args: argparse.Namespace) -> dict[str, Any]:
    root = Path(args.root).resolve()
    if not (root / "runs").is_dir():
        raise StorageError(f"storage root must contain runs/: {root}")
    entries: list[dict[str, Any]] = []
    for paths in discover_pack_groups(root):
        source = paths[0]
        source_sha256 = file_sha256(source)
        for target in paths[1:]:
            if file_sha256(target) != source_sha256:
                continue
            entries.append(
                {
                    "source_path": source.relative_to(root).as_posix(),
                    "target_path": target.relative_to(root).as_posix(),
                    "size_bytes": source.stat().st_size,
                    "content_sha256": source_sha256,
                }
            )
    document = {
        "schema_version": PACK_MANIFEST_SCHEMA,
        "generated_at": utc_now(),
        "root": str(root),
        "entries": entries,
        "reclaimable_logical_bytes": sum(item["size_bytes"] for item in entries),
    }
    manifest = {**document, "manifest_sha256": identity_sha256(document)}
    manifest_path = Path(args.manifest).resolve()
    write_json_once(manifest_path, manifest)
    return {
        "mode": "dry_run",
        "manifest": str(manifest_path),
        "entry_count": len(entries),
        "reclaimable_logical_bytes": manifest["reclaimable_logical_bytes"],
    }


def verify_pack_manifest(manifest: dict[str, Any]) -> None:
    if manifest.get("schema_version") != PACK_MANIFEST_SCHEMA:
        raise StorageError("unsupported pack dedup manifest schema")
    content = {key: value for key, value in manifest.items() if key != "manifest_sha256"}
    if manifest.get("manifest_sha256") != identity_sha256(content):
        raise StorageError("pack dedup manifest content hash does not match")


def clone_pack(source: Path, target: Path) -> None:
    if sys.platform != "darwin":
        raise StorageError("pack deduplication requires macOS clonefile support")
    metadata = target.stat()
    temporary = target.with_name(f".{target.name}.clonefile-{os.getpid()}")
    if temporary.exists() or temporary.is_symlink():
        raise StorageError(f"temporary pack path already exists: {temporary}")
    completed = subprocess.run(
        ["/bin/cp", "-c", str(source), str(temporary)],
        capture_output=True,
        check=False,
        text=True,
    )
    if completed.returncode != 0:
        if temporary.exists():
            temporary.unlink()
        raise StorageError(completed.stderr.strip() or f"clonefile failed: {target}")
    try:
        os.chmod(temporary, stat.S_IMODE(metadata.st_mode))
        os.utime(temporary, ns=(metadata.st_atime_ns, metadata.st_mtime_ns))
        os.replace(temporary, target)
    finally:
        if temporary.exists():
            temporary.unlink()


def apply_pack_dedup(args: argparse.Namespace) -> dict[str, Any]:
    manifest_path = Path(args.manifest).resolve()
    receipt_path = Path(args.receipt).resolve()
    if receipt_path.exists():
        raise StorageError(f"refusing to overwrite: {receipt_path}")
    manifest = load_json(manifest_path)
    verify_pack_manifest(manifest)
    root = Path(manifest["root"]).resolve()
    if root != Path(args.root).resolve():
        raise StorageError("pack dedup manifest root does not match arguments")
    locks = list((root / "runs").rglob(".git/objects/pack/*.lock"))
    if locks:
        raise StorageError(f"Git pack lock exists: {locks[0]}")
    entries = manifest.get("entries")
    if not isinstance(entries, list):
        raise StorageError("pack dedup manifest entries must be an array")

    validated: list[tuple[Path, Path, dict[str, Any]]] = []
    for entry in entries:
        if not isinstance(entry, dict):
            raise StorageError("pack dedup manifest entry is invalid")
        source = (root / entry["source_path"]).resolve()
        target = (root / entry["target_path"]).resolve()
        if (
            not path_within(source, root / "runs")
            or not path_within(target, root / "runs")
            or source.is_symlink()
            or target.is_symlink()
            or not source.is_file()
            or not target.is_file()
        ):
            raise StorageError(f"invalid pack dedup path: {entry}")
        expected_size = entry.get("size_bytes")
        if source.stat().st_size != expected_size or target.stat().st_size != expected_size:
            raise StorageError(f"pack size changed: {entry['target_path']}")
        expected_hash = entry.get("content_sha256")
        if file_sha256(source) != expected_hash or file_sha256(target) != expected_hash:
            raise StorageError(f"pack content changed: {entry['target_path']}")
        validated.append((source, target, entry))

    free_before = shutil.disk_usage(root).free
    for source, target, _ in validated:
        clone_pack(source, target)
    free_after = shutil.disk_usage(root).free
    receipt = {
        "schema_version": PACK_RECEIPT_SCHEMA,
        "applied_at": utc_now(),
        "manifest": str(manifest_path),
        "manifest_sha256": manifest["manifest_sha256"],
        "rematerialized_count": len(validated),
        "logical_bytes": sum(entry["size_bytes"] for _, _, entry in validated),
        "filesystem_free_bytes_before": free_before,
        "filesystem_free_bytes_after": free_after,
        "filesystem_free_bytes_delta": free_after - free_before,
    }
    write_json_once(receipt_path, receipt)
    return {
        "mode": "apply",
        "receipt": str(receipt_path),
        "rematerialized_count": len(validated),
        "logical_bytes": receipt["logical_bytes"],
        "filesystem_free_bytes_delta": receipt["filesystem_free_bytes_delta"],
    }


def gc_manifest(args: argparse.Namespace) -> dict[str, Any]:
    root = Path(args.root).resolve()
    repository = Path(args.repository).resolve()
    report = audit_storage(
        root, repository, args.scratch_days, args.soft_limit_gib, args.hard_limit_gib
    )
    run_index = {item["path"]: item for item in report["runs"]}
    entries = []
    for relative in report["gc_candidates"]:
        path = root / relative
        entries.append(
            {
                "path": relative,
                "reason": "expired_unreferenced_scratch_run",
                "allocated_bytes": run_index[relative]["allocated_bytes"],
                "file_count": run_index[relative]["file_count"],
                "tree_sha256": tree_fingerprint(path),
            }
        )
    document = {
        "schema_version": MANIFEST_SCHEMA,
        "generated_at": utc_now(),
        "root": str(root),
        "repository": str(repository),
        "policy": report["policy"],
        "entries": entries,
        "total_allocated_bytes": sum(item["allocated_bytes"] for item in entries),
    }
    manifest = {**document, "manifest_sha256": identity_sha256(document)}
    write_json_once(Path(args.manifest).resolve(), manifest)
    return {
        "mode": "dry_run",
        "manifest": str(Path(args.manifest).resolve()),
        "entry_count": len(entries),
        "total_allocated_bytes": manifest["total_allocated_bytes"],
    }


def verify_manifest(manifest: dict[str, Any]) -> dict[str, Any]:
    if manifest.get("schema_version") != MANIFEST_SCHEMA:
        raise StorageError("unsupported GC manifest schema")
    content = {key: value for key, value in manifest.items() if key != "manifest_sha256"}
    if manifest.get("manifest_sha256") != identity_sha256(content):
        raise StorageError("GC manifest content hash does not match")
    return content


def apply_gc(args: argparse.Namespace) -> dict[str, Any]:
    manifest_path = Path(args.manifest).resolve()
    receipt_path = Path(args.receipt).resolve()
    if receipt_path.exists():
        raise StorageError(f"refusing to overwrite: {receipt_path}")
    manifest = load_json(manifest_path)
    verify_manifest(manifest)
    root = Path(manifest["root"]).resolve()
    repository = Path(manifest["repository"]).resolve()
    if root != Path(args.root).resolve() or repository != Path(args.repository).resolve():
        raise StorageError("GC manifest root or repository does not match arguments")
    policy = manifest.get("policy")
    if not isinstance(policy, dict) or not isinstance(policy.get("scratch_days"), int):
        raise StorageError("GC manifest has invalid policy")
    report = audit_storage(
        root,
        repository,
        policy["scratch_days"],
        policy["soft_limit_bytes"] / 1024**3,
        policy["hard_limit_bytes"] / 1024**3,
    )
    eligible = set(report["gc_candidates"])
    entries = manifest.get("entries")
    if not isinstance(entries, list):
        raise StorageError("GC manifest entries must be an array")

    validated: list[tuple[Path, dict[str, Any]]] = []
    runs_root = (root / "runs").resolve()
    for entry in entries:
        if not isinstance(entry, dict) or not isinstance(entry.get("path"), str):
            raise StorageError("GC manifest entry is invalid")
        relative = Path(entry["path"])
        path = (root / relative).resolve()
        if relative.is_absolute() or path.parent != runs_root or path.is_symlink():
            raise StorageError(f"GC target must be a direct runs/ child: {relative}")
        if entry["path"] not in eligible:
            raise StorageError(f"GC target is no longer eligible: {relative}")
        if allocated_bytes(path) != entry.get("allocated_bytes"):
            raise StorageError(f"GC target allocated size changed: {relative}")
        if tree_fingerprint(path) != entry.get("tree_sha256"):
            raise StorageError(f"GC target content changed: {relative}")
        validated.append((path, entry))

    for path, _ in validated:
        shutil.rmtree(path)
    receipt = {
        "schema_version": RECEIPT_SCHEMA,
        "applied_at": utc_now(),
        "manifest": str(manifest_path),
        "manifest_sha256": manifest["manifest_sha256"],
        "deleted": [entry for _, entry in validated],
        "total_allocated_bytes": sum(entry["allocated_bytes"] for _, entry in validated),
    }
    write_json_once(receipt_path, receipt)
    return {
        "mode": "apply",
        "receipt": str(receipt_path),
        "deleted_count": len(validated),
        "total_allocated_bytes": receipt["total_allocated_bytes"],
    }


def audit_command(args: argparse.Namespace) -> dict[str, Any]:
    return audit_storage(
        Path(args.root),
        Path(args.repository),
        args.scratch_days,
        args.soft_limit_gib,
        args.hard_limit_gib,
    )


def add_common_arguments(command: argparse.ArgumentParser) -> None:
    command.add_argument("--root", required=True)
    command.add_argument("--repository", required=True)
    command.add_argument("--scratch-days", type=int, default=3)
    command.add_argument("--soft-limit-gib", type=float, default=3.0)
    command.add_argument("--hard-limit-gib", type=float, default=5.0)


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    commands = result.add_subparsers(dest="subcommand", required=True)
    audit = commands.add_parser("audit", help="report allocation and retention state")
    add_common_arguments(audit)
    audit.set_defaults(handler=audit_command)

    gc = commands.add_parser("gc", help="create or apply a verified GC manifest")
    add_common_arguments(gc)
    gc.add_argument("--manifest", required=True)
    gc.add_argument("--apply", action="store_true")
    gc.add_argument("--receipt")
    gc.set_defaults(handler=lambda args: apply_gc(args) if args.apply else gc_manifest(args))

    packs = commands.add_parser(
        "deduplicate-packs", help="rematerialize identical Git packs with clonefile"
    )
    packs.add_argument("--root", required=True)
    packs.add_argument("--manifest", required=True)
    packs.add_argument("--apply", action="store_true")
    packs.add_argument("--receipt")
    packs.set_defaults(
        handler=lambda args: apply_pack_dedup(args) if args.apply else pack_dedup_manifest(args)
    )
    return result


def main() -> int:
    args = parser().parse_args()
    if getattr(args, "apply", False) and not args.receipt:
        print("error: --apply requires --receipt", file=sys.stderr)
        return 2
    if not getattr(args, "apply", False) and getattr(args, "receipt", None):
        print("error: --receipt requires --apply", file=sys.stderr)
        return 2
    try:
        value = args.handler(args)
    except (StorageError, OSError, KeyError, TypeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(value, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
