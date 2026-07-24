from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C43 = ROOT / "prompts/candidates/the-caption-3ce91a4-outcome-authority-boundary-r1"
C66 = ROOT / "prompts/candidates/the-caption-3ce91a4-topology-preserving-compression-r1"
PROFILES = ROOT / "evaluations/profiles"
PROFILE_PAIRS = (
    (
        PROFILES
        / "candidate43-outcome-authority-boundary-fixed-evidence-review-f10-v9-global-m10-n5-catalog-fixed-r1.json",
        PROFILES
        / "candidate66-topology-preserving-compression-fixed-evidence-review-f10-v9-global-m10-n5-catalog-fixed-r1.json",
    ),
    (
        PROFILES
        / "candidate43-outcome-authority-boundary-outcome-quality-owner-diagnostic-v9-targeted2-global-m10-n5-catalog-fixed-r1.json",
        PROFILES
        / "candidate66-topology-preserving-compression-outcome-quality-owner-diagnostic-v9-targeted2-global-m10-n5-catalog-fixed-r1.json",
    ),
    (
        PROFILES
        / "candidate43-outcome-authority-boundary-ambiguity-targeted2-v10-global-m10-n5-catalog-fixed-r1.json",
        PROFILES
        / "candidate66-topology-preserving-compression-ambiguity-targeted2-v10-global-m10-n5-catalog-fixed-r1.json",
    ),
    (
        PROFILES
        / "candidate43-outcome-authority-boundary-explicit-producer-d01-v9-global-m5-n5-catalog-fixed-r1.json",
        PROFILES
        / "candidate66-topology-preserving-compression-explicit-producer-d01-v9-global-m5-n5-catalog-fixed-r1.json",
    ),
)


CLAUSE_COVERAGE = {
    "SPEC1": ("SPEC", "実行前にrequired outcomeをoperation identityへ分け"),
    "SPEC2": ("SPEC", "`spec_ready := TaskSpecへ固定する全値が"),
    "SPEC3": (
        "SPEC",
        "current value / option set / complement / test expectation / implementation convenience",
    ),
    "SPEC4": (
        "SPEC",
        "`spec_ready=false`の間はproducer binding / predicate実行 / artifact変更 / testを開始せず",
    ),
    "SPEC5": ("SPEC", "未固定値だけをclarification resultにする"),
    "SPEC6": ("SPEC", "別operation / task全体へ伝播させない"),
    "PRODUCER1": ("PRODUCER", "producer execution identityを一つbind"),
    "PRODUCER2": ("PRODUCER", "他producerへ順次・並行に割り当てない"),
    "PRODUCER3": ("PRODUCER", "TaskSpecが独立producer executionを明示した場合だけ"),
    "PRODUCER4": ("PRODUCER", "criterion owner語列だけでproducerを選ばない"),
    "PRODUCER5": (
        "PRODUCER",
        "producer変更は理由を問わず旧bindingを失効し、新identityのTaskSpecで行う",
    ),
    "TERMINAL1": ("TERMINAL", "terminal resultがある場合だけoperationをterminalにする"),
    "TERMINAL2": ("TERMINAL", "result欠落ならoperationもnonterminal"),
    "CONTEXT1": ("CONTEXT", "worker packetへ`criterion / owner / pass condition"),
    "CONTEXT2": ("CONTEXT", "`fork_turns=none`、不足時だけ意味保持に必要な最小turn数"),
    "CONTEXT3": ("CONTEXT", "全履歴継承の理由にしない"),
    "OWNER_ROLE1": ("OWNER_ROLE", "criterion owner語列をnon-machine riskの担当情報として保持"),
    "OWNER_ROLE2": ("OWNER_ROLE", "predicate前に対応workerを起動する"),
    "OWNER_ROLE3": ("OWNER_ROLE", "`delegated_result_ready := runtime_spawn_result.task_name"),
    "OWNER_ROLE4": ("OWNER_ROLE", "`wait`は同期専用でidentity証跡にしない"),
    "OWNER_ROLE5": (
        "OWNER_ROLE",
        "producer terminal後も`delegated_result_ready=false`ならcriterionを`unavailable`にする",
    ),
    "OWNER_ROLE6": ("OWNER_ROLE", "bind済みcriterionの`false / failed`"),
    "OWNER_ROLE7": ("OWNER_ROLE", "異Sender message / root再構成による補完は禁止する"),
    "ROOT1": ("ROOT", "predicate実行 / result再生成をしない"),
    "INDEPENDENCE1": ("INDEPENDENCE", "先行result / artifactを対象とする別operation"),
    "INDEPENDENCE2": ("INDEPENDENCE", "同一predicateを別producerへ再割当てしない"),
    "METHOD1": ("METHOD", "TaskSpec明示手段だけを固定"),
    "METHOD2": ("METHOD", "未固定手段はpredicateを変えずpermission内でexecutorが選ぶ"),
    "METHOD3": ("METHOD", "failed / unavailableをpermission否定 / terminalにせず"),
    "METHOD4": ("METHOD", "明示禁止 / permission否定は停止し、回避しない"),
    "RECOVERY1": ("RECOVERY", "environment-only repair + same required command rerun"),
    "RECOVERY2": (
        "RECOVERY",
        "`environment_recovery_max`を消費し、未固定手段の選択は数えない",
    ),
}


def labelled_blocks(text: str) -> list[tuple[str, str]]:
    blocks = []
    for line in text.splitlines():
        if not line.startswith("- "):
            continue
        label, body = line[2:].split(": ", 1)
        blocks.append((label, body))
    return blocks


class Candidate66Test(unittest.TestCase):
    def test_is_a_single_target_direct_child_of_candidate43(self) -> None:
        source = verify_bundle(C43)
        candidate = verify_bundle(C66)
        self.assertEqual(
            candidate["prompt_identity"],
            "the-caption-3ce91a4-topology-preserving-compression-r1",
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
        candidate_manifest = json.loads((C66 / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(
            [entry for entry in candidate_manifest["files"] if entry["target"] != "AGENTS.md"],
            [entry for entry in source_manifest["files"] if entry["target"] != "AGENTS.md"],
        )

    def test_preserves_nine_labels_order_and_single_layer(self) -> None:
        source_text = (C43 / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        candidate_text = (C66 / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        source_labels = [label for label, _ in labelled_blocks(source_text)]
        candidate_labels = [label for label, _ in labelled_blocks(candidate_text)]
        self.assertEqual(
            candidate_labels,
            [
                "SPEC",
                "PRODUCER",
                "TERMINAL",
                "CONTEXT",
                "OWNER_ROLE",
                "ROOT",
                "INDEPENDENCE",
                "METHOD",
                "RECOVERY",
            ],
        )
        self.assertEqual(candidate_labels, source_labels)
        self.assertNotIn("\n## ", candidate_text)
        self.assertEqual(len(candidate_text.splitlines()), 11)

    def test_keeps_all_32_clauses_in_their_source_labels(self) -> None:
        text = (C66 / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        blocks = dict(labelled_blocks(text))
        self.assertEqual(len(CLAUSE_COVERAGE), 32)
        for clause_id, (label, required) in CLAUSE_COVERAGE.items():
            with self.subTest(clause_id=clause_id, label=label):
                self.assertIn(required, blocks[label])

    def test_keeps_cross_label_duplicates(self) -> None:
        text = (C66 / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        self.assertEqual(
            text.count("TaskSpecが独立producer executionを明示した場合だけ"),
            2,
        )
        self.assertIn("他producerへ順次・並行に割り当てない", text)
        self.assertIn("同一predicateを別producerへ再割当てしない", text)

    def test_only_shortens_bodies_without_changing_label_membership(self) -> None:
        source = dict(
            labelled_blocks((C43 / "files/AGENTS.md.txt").read_text(encoding="utf-8"))
        )
        candidate = dict(
            labelled_blocks((C66 / "files/AGENTS.md.txt").read_text(encoding="utf-8"))
        )
        changed = {label for label in source if source[label] != candidate[label]}
        self.assertEqual(
            changed,
            {"SPEC", "PRODUCER", "TERMINAL", "CONTEXT", "OWNER_ROLE", "METHOD"},
        )
        for label in changed:
            with self.subTest(label=label):
                self.assertLess(len(candidate[label].encode()), len(source[label].encode()))

    def test_reduces_static_bytes(self) -> None:
        source_size = (C43 / "files/AGENTS.md.txt").stat().st_size
        candidate_size = (C66 / "files/AGENTS.md.txt").stat().st_size
        self.assertEqual(source_size, 3980)
        self.assertEqual(candidate_size, 3923)
        self.assertLess(candidate_size, source_size)

    def test_profiles_change_only_prompt_identity(self) -> None:
        manifest = verify_bundle(C66)
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
