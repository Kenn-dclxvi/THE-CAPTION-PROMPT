from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C43 = ROOT / "prompts/candidates/the-caption-3ce91a4-outcome-authority-boundary-r1"
C67 = (
    ROOT
    / "prompts/candidates/the-caption-3ce91a4-cross-label-predicate-deduplication-r1"
)
PROFILES = ROOT / "evaluations/profiles"
PROFILE_PAIRS = (
    (
        PROFILES
        / "candidate43-outcome-authority-boundary-fixed-evidence-review-f10-v9-global-m10-n5-catalog-fixed-r1.json",
        PROFILES
        / "candidate67-cross-label-predicate-deduplication-fixed-evidence-review-f10-v9-global-m10-n5-catalog-fixed-r1.json",
    ),
    (
        PROFILES
        / "candidate43-outcome-authority-boundary-outcome-quality-owner-diagnostic-v9-targeted2-global-m10-n5-catalog-fixed-r1.json",
        PROFILES
        / "candidate67-cross-label-predicate-deduplication-outcome-quality-owner-diagnostic-v9-targeted2-global-m10-n5-catalog-fixed-r1.json",
    ),
    (
        PROFILES
        / "candidate43-outcome-authority-boundary-ambiguity-targeted2-v10-global-m10-n5-catalog-fixed-r1.json",
        PROFILES
        / "candidate67-cross-label-predicate-deduplication-ambiguity-targeted2-v10-global-m10-n5-catalog-fixed-r1.json",
    ),
    (
        PROFILES
        / "candidate43-outcome-authority-boundary-explicit-producer-d01-v9-global-m5-n5-catalog-fixed-r1.json",
        PROFILES
        / "candidate67-cross-label-predicate-deduplication-explicit-producer-d01-v9-global-m5-n5-catalog-fixed-r1.json",
    ),
    (
        PROFILES
        / "candidate43-outcome-authority-boundary-v10-standard14-global-m24-n5-r1.json",
        PROFILES
        / "candidate67-cross-label-predicate-deduplication-v10-standard14-global-m24-n5-r1.json",
    ),
)

EXPLICIT_DELEGATION_DUPLICATE = (
    "TaskSpecが独立したproducer executionを明示した場合だけ、"
    "その指定identityをproducer role identityへbindする。"
)
PRODUCER_REASSIGNMENT_DUPLICATE = "同一predicateを別producerへ再割当てしない。"


def labelled_blocks(text: str) -> dict[str, str]:
    blocks = {}
    for line in text.splitlines():
        if not line.startswith("- "):
            continue
        label, body = line[2:].split(": ", 1)
        blocks[label] = body
    return blocks


class Candidate67Test(unittest.TestCase):
    def test_is_a_single_target_direct_child_of_candidate43(self) -> None:
        source = verify_bundle(C43)
        candidate = verify_bundle(C67)
        self.assertEqual(
            candidate["prompt_identity"],
            "the-caption-3ce91a4-cross-label-predicate-deduplication-r1",
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
            (C67 / "manifest.json").read_text(encoding="utf-8")
        )
        self.assertEqual(
            [entry for entry in candidate_manifest["files"] if entry["target"] != "AGENTS.md"],
            [entry for entry in source_manifest["files"] if entry["target"] != "AGENTS.md"],
        )

    def test_removes_only_the_two_cross_label_duplicate_sentences(self) -> None:
        source_text = (C43 / "files/AGENTS.md").read_text(encoding="utf-8")
        candidate_text = (C67 / "files/AGENTS.md").read_text(encoding="utf-8")
        expected = source_text.replace(EXPLICIT_DELEGATION_DUPLICATE, "").replace(
            PRODUCER_REASSIGNMENT_DUPLICATE,
            "",
        )
        self.assertEqual(candidate_text, expected)

    def test_preserves_nine_labels_order_and_changes_only_canonicalized_labels(self) -> None:
        source = labelled_blocks((C43 / "files/AGENTS.md").read_text(encoding="utf-8"))
        candidate = labelled_blocks((C67 / "files/AGENTS.md").read_text(encoding="utf-8"))
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
            {"PRODUCER", "INDEPENDENCE"},
        )

    def test_retains_each_canonical_predicate_once(self) -> None:
        text = (C67 / "files/AGENTS.md").read_text(encoding="utf-8")
        blocks = labelled_blocks(text)
        self.assertEqual(
            text.count("TaskSpecが独立したproducer executionを明示した場合だけ"),
            1,
        )
        self.assertIn(
            "起動前にそのexecution identityをtask identityとしてproducerへbindし、"
            "predicate前に対応workerを起動する",
            blocks["OWNER_ROLE"],
        )
        self.assertNotIn(EXPLICIT_DELEGATION_DUPLICATE, blocks["PRODUCER"])
        self.assertIn(
            "同一operationのpredicate実行 / result生成を他producerへ順次・並行に割り当てない",
            blocks["PRODUCER"],
        )
        self.assertNotIn(PRODUCER_REASSIGNMENT_DUPLICATE, blocks["INDEPENDENCE"])
        self.assertIn(
            "先行result / artifactを対象とする別operationへ固有predicate / owner / producerを実行前に固定する",
            blocks["INDEPENDENCE"],
        )

    def test_reduces_only_the_duplicate_bytes(self) -> None:
        source_size = (C43 / "files/AGENTS.md").stat().st_size
        candidate_size = (C67 / "files/AGENTS.md").stat().st_size
        self.assertEqual(source_size, 3980)
        self.assertEqual(candidate_size, 3792)
        self.assertEqual(source_size - candidate_size, 188)

    def test_profiles_change_only_prompt_identity(self) -> None:
        manifest = verify_bundle(C67)
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
