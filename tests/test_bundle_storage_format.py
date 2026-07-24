from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import (
    BundleError,
    INSTRUCTION_BASENAMES,
    STORAGE_FORMAT_LEGACY,
    STORAGE_FORMAT_SUFFIXED,
    STORE_SUFFIX,
    bundle_sha256,
    stored_link_target,
    stored_relpath,
    target_from_stored,
    verify_bundle,
)

REPO_ROOT = Path(__file__).resolve().parent.parent


def bundle_dirs() -> list[Path]:
    return sorted(p.parent for p in REPO_ROOT.glob("prompts/**/manifest.json"))


class StorageHelperTest(unittest.TestCase):
    def test_suffixed_roundtrip_for_instruction_paths(self) -> None:
        for target in ("AGENTS.md", "CLAUDE.md", "docs/AGENTS.md", "src/CLAUDE.md"):
            stored = stored_relpath(target, STORAGE_FORMAT_SUFFIXED)
            self.assertTrue(stored.endswith(STORE_SUFFIX))
            self.assertEqual(target_from_stored(stored, STORAGE_FORMAT_SUFFIXED), target)

    def test_non_instruction_paths_are_untouched(self) -> None:
        for target in ("docs/prompt-guide.md", "prompts/plan.md", "src/main.py"):
            self.assertEqual(stored_relpath(target, STORAGE_FORMAT_SUFFIXED), target)
            self.assertEqual(target_from_stored(target, STORAGE_FORMAT_SUFFIXED), target)

    def test_legacy_format_is_identity_mapping(self) -> None:
        for target in ("AGENTS.md", "docs/CLAUDE.md", "src/main.py"):
            self.assertEqual(stored_relpath(target, STORAGE_FORMAT_LEGACY), target)
            self.assertEqual(target_from_stored(target, STORAGE_FORMAT_LEGACY), target)

    def test_symlink_target_mapping(self) -> None:
        self.assertEqual(
            stored_link_target("AGENTS.md", STORAGE_FORMAT_SUFFIXED), "AGENTS.md" + STORE_SUFFIX
        )
        self.assertEqual(stored_link_target("AGENTS.md", STORAGE_FORMAT_LEGACY), "AGENTS.md")


class LegacyBundleCompatTest(unittest.TestCase):
    def test_legacy_layout_still_verifies(self) -> None:
        # storage_format 未指定の従来レイアウト（files/AGENTS.md を実体名で格納）が
        # 引き続き検証できること（後方互換）。
        with tempfile.TemporaryDirectory() as tmp:
            bundle = Path(tmp)
            files_root = bundle / "files"
            files_root.mkdir()
            content = b"legacy root\n"
            (files_root / "AGENTS.md").write_bytes(content)
            entry = {
                "git_blob_sha1": "0" * 40,
                "mode": "100644",
                "sha256": __import__("hashlib").sha256(content).hexdigest(),
                "target": "AGENTS.md",
                "type": "file",
            }
            manifest = {
                "bundle_sha256": bundle_sha256([entry]),
                "files": [entry],
                "prompt_identity": "legacy-r1",
                "schema_version": "the-caption-prompt.bundle/v1",
            }
            (bundle / "manifest.json").write_text(
                json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )
            verified = verify_bundle(bundle)
            self.assertNotIn("storage_format", verified)


class RepositoryBundleStorageTest(unittest.TestCase):
    def setUp(self) -> None:
        self.bundles = bundle_dirs()

    def test_repository_has_bundles(self) -> None:
        self.assertGreater(len(self.bundles), 0)

    def test_no_instruction_named_files_at_rest(self) -> None:
        # working tree: prompts/**/files 配下に自動読込対象名(AGENTS.md/CLAUDE.md)を
        # 実体名で置かない。
        offenders = [
            path.relative_to(REPO_ROOT).as_posix()
            for path in (REPO_ROOT / "prompts").rglob("*")
            if "/files/" in (path.as_posix() + "/")
            and path.name in INSTRUCTION_BASENAMES
            and (path.is_file() or path.is_symlink())
        ]
        self.assertEqual(offenders, [], f"instruction-named files stored at rest: {offenders}")

    def test_no_instruction_named_files_tracked(self) -> None:
        # git index 側でも回帰しないこと。
        tracked = subprocess.run(
            ["git", "ls-files", "--", "prompts/**/files/**/AGENTS.md",
             "prompts/**/files/AGENTS.md", "prompts/**/files/**/CLAUDE.md",
             "prompts/**/files/CLAUDE.md"],
            cwd=REPO_ROOT, capture_output=True, text=True, check=True,
        ).stdout.split()
        self.assertEqual(tracked, [])

    def test_all_bundles_suffixed_verify_and_hash_invariant(self) -> None:
        for bundle in self.bundles:
            with self.subTest(bundle=bundle.relative_to(REPO_ROOT).as_posix()):
                manifest = verify_bundle(bundle)
                self.assertEqual(manifest.get("storage_format"), STORAGE_FORMAT_SUFFIXED)
                # bundle_sha256 は files 由来。verify を通過した時点で
                # 保存 hash == files 由来 hash が成立している。
                recomputed = bundle_sha256(
                    [{k: v for k, v in e.items() if isinstance(v, str)} for e in manifest["files"]]
                )
                self.assertEqual(manifest["bundle_sha256"], recomputed)


if __name__ == "__main__":
    unittest.main()
