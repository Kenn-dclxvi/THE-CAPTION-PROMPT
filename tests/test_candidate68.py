from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C43 = ROOT / "prompts/candidates/the-caption-3ce91a4-outcome-authority-boundary-r1"
C68 = (
    ROOT
    / "prompts/candidates/the-caption-3ce91a4-independent-review-operation-removal-r1"
)
PROFILES = ROOT / "evaluations/profiles"
PROFILE_PAIRS = (
    (
        PROFILES
        / "candidate43-outcome-authority-boundary-fixed-evidence-review-f10-v9-global-m10-n5-catalog-fixed-r1.json",
        PROFILES
        / "candidate68-independent-review-operation-removal-fixed-evidence-review-f10-v9-global-m10-n5-catalog-fixed-r1.json",
    ),
    (
        PROFILES
        / "candidate43-outcome-authority-boundary-outcome-quality-owner-diagnostic-v9-targeted2-global-m10-n5-catalog-fixed-r1.json",
        PROFILES
        / "candidate68-independent-review-operation-removal-outcome-quality-owner-diagnostic-v9-targeted2-global-m10-n5-catalog-fixed-r1.json",
    ),
    (
        PROFILES
        / "candidate43-outcome-authority-boundary-ambiguity-targeted2-v10-global-m10-n5-catalog-fixed-r1.json",
        PROFILES
        / "candidate68-independent-review-operation-removal-ambiguity-targeted2-v10-global-m10-n5-catalog-fixed-r1.json",
    ),
    (
        PROFILES
        / "candidate43-outcome-authority-boundary-explicit-producer-d01-v9-global-m5-n5-catalog-fixed-r1.json",
        PROFILES
        / "candidate68-independent-review-operation-removal-explicit-producer-d01-v9-global-m5-n5-catalog-fixed-r1.json",
    ),
)

F9 = (
    "先行result / artifactを対象とする別operationへ"
    "固有predicate / owner / producerを実行前に固定する。"
)


def labelled_blocks(text: str) -> dict[str, str]:
    blocks = {}
    for line in text.splitlines():
        if not line.startswith("- "):
            continue
        label, body = line[2:].split(": ", 1)
        blocks[label] = body
    return blocks


class Candidate68Test(unittest.TestCase):
    def test_is_a_single_target_direct_child_of_candidate43(self) -> None:
        source = verify_bundle(C43)
        candidate = verify_bundle(C68)
        self.assertEqual(
            candidate["prompt_identity"],
            "the-caption-3ce91a4-independent-review-operation-removal-r1",
        )
        self.assertEqual(
            candidate["content_relation"],
            {
                "changed_targets": ["AGENTS.md"],
                "kind": "direct_child_full_bundle",
                "source_prompt_identity": source["prompt_identity"],
            },
        )

        source_manifest = json.loads((C43 / "manifest.json").read_text(encoding="utf-8"))
        candidate_manifest = json.loads(
            (C68 / "manifest.json").read_text(encoding="utf-8")
        )
        self.assertEqual(
            [entry for entry in candidate_manifest["files"] if entry["target"] != "AGENTS.md"],
            [entry for entry in source_manifest["files"] if entry["target"] != "AGENTS.md"],
        )

    def test_removes_only_f9(self) -> None:
        source_text = (C43 / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        candidate_text = (C68 / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        self.assertEqual(candidate_text, source_text.replace(F9, ""))

    def test_preserves_topology_and_adjacent_exclusivity(self) -> None:
        source = labelled_blocks((C43 / "files/AGENTS.md.txt").read_text(encoding="utf-8"))
        candidate = labelled_blocks((C68 / "files/AGENTS.md.txt").read_text(encoding="utf-8"))
        expected_labels = [
            "SPEC",
            "PRODUCER",
            "TERMINAL",
            "CONTEXT",
            "OWNER_ROLE",
            "ROOT",
            "INDEPENDENCE",
            "METHOD",
            "RECOVERY",
        ]
        self.assertEqual(list(candidate), expected_labels)
        self.assertEqual(list(candidate), list(source))
        self.assertEqual(
            {label for label in source if source[label] != candidate[label]},
            {"INDEPENDENCE"},
        )
        self.assertEqual(
            candidate["INDEPENDENCE"],
            "同一predicateを別producerへ再割当てしない。",
        )

    def test_retains_other_candidate43_targets(self) -> None:
        text = (C68 / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        self.assertNotIn(F9, text)
        self.assertIn(
            "TaskSpecが独立したproducer executionを明示した場合だけ、"
            "その指定identityをproducer role identityへbindする。",
            text,
        )
        self.assertIn(
            "同一operationのpredicate実行 / result生成を他producerへ順次・並行に割り当てない",
            text,
        )
        self.assertIn("criterion owner語列だけでproducerを選ばない。", text)
        self.assertIn("worker packetへ`criterion / owner / pass condition", text)
        self.assertIn("- RECOVERY:", text)

    def test_reduces_only_f9_bytes(self) -> None:
        source_size = (C43 / "files/AGENTS.md.txt").stat().st_size
        candidate_size = (C68 / "files/AGENTS.md.txt").stat().st_size
        self.assertEqual(source_size, 3980)
        self.assertEqual(candidate_size, 3860)
        self.assertEqual(source_size - candidate_size, 120)

    def test_profiles_change_only_prompt_identity(self) -> None:
        manifest = verify_bundle(C68)
        for source_path, candidate_path in PROFILE_PAIRS:
            with self.subTest(candidate_profile=candidate_path.name):
                source = json.loads(source_path.read_text(encoding="utf-8"))
                candidate = json.loads(candidate_path.read_text(encoding="utf-8"))
                self.assertEqual(
                    candidate["prompt_set_identity"],
                    {
                        "bundle_sha256": manifest["bundle_sha256"],
                        "name": manifest["prompt_identity"],
                        "revision": "r1",
                    },
                )
                comparable_source = copy.deepcopy(source)
                comparable_candidate = copy.deepcopy(candidate)
                for profile in (comparable_source, comparable_candidate):
                    profile.pop("profile_id")
                    profile.pop("prompt_set_identity")
                self.assertEqual(comparable_candidate, comparable_source)


if __name__ == "__main__":
    unittest.main()
