from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C43 = ROOT / "prompts/candidates/the-caption-3ce91a4-outcome-authority-boundary-r1"
C65 = ROOT / "prompts/candidates/the-caption-3ce91a4-shared-operation-core-r1"
PROFILES = ROOT / "evaluations/profiles"
PROFILE_PAIRS = (
    (
        PROFILES
        / "candidate43-outcome-authority-boundary-outcome-quality-owner-diagnostic-v9-targeted2-global-m10-n5-catalog-fixed-r1.json",
        PROFILES
        / "candidate65-shared-operation-core-outcome-quality-owner-diagnostic-v9-targeted2-global-m10-n5-catalog-fixed-r1.json",
    ),
    (
        PROFILES
        / "candidate43-outcome-authority-boundary-ambiguity-targeted2-v10-global-m10-n5-catalog-fixed-r1.json",
        PROFILES
        / "candidate65-shared-operation-core-ambiguity-targeted2-v10-global-m10-n5-catalog-fixed-r1.json",
    ),
    (
        PROFILES
        / "candidate43-outcome-authority-boundary-explicit-producer-d01-v9-global-m5-n5-catalog-fixed-r1.json",
        PROFILES
        / "candidate65-shared-operation-core-explicit-producer-d01-v9-global-m5-n5-catalog-fixed-r1.json",
    ),
)


CLAUSE_COVERAGE = {
    "SPEC1": ("READINESS", "実行前にrequired outcomeをoperation identityへ分け"),
    "SPEC2": ("READINESS", "`spec_ready := 必要な全値が"),
    "SPEC3": (
        "READINESS",
        "current value / option set / complement / test expectation / implementation convenience",
    ),
    "SPEC4": (
        "READINESS",
        "`spec_ready=false`ならproducer binding / predicate実行 / artifact変更 / testを開始せず",
    ),
    "SPEC5": ("READINESS", "未固定値だけをclarification resultにする"),
    "SPEC6": ("SCOPE", "別operation / task全体へ伝播させない"),
    "PRODUCER1": ("PRODUCER", "producer execution identityを一つbind"),
    "PRODUCER2": ("PRODUCER", "他producerへ順次・並行に再割当てしない"),
    "PRODUCER3": ("ENTRY", "TaskSpecが独立producer executionを明示した場合だけ"),
    "PRODUCER4": ("ENTRY", "worker指定には使わない"),
    "PRODUCER5": ("PRODUCER", "producer変更は旧bindingを失効し、新identityのTaskSpecで行う"),
    "TERMINAL1": ("TERMINAL", "terminal resultがある場合だけoperationをterminalにする"),
    "TERMINAL2": ("TERMINAL", "result欠落ならoperationもnonterminal"),
    "CONTEXT1": ("CONTEXT", "worker packetへ`criterion / owner / pass condition"),
    "CONTEXT2": ("CONTEXT", "`fork_turns=none`、不足時だけ意味保持に必要な最小turn数"),
    "CONTEXT3": ("CONTEXT", "全履歴継承の理由にしない"),
    "OWNER_ROLE1": ("ENTRY", "criterion owner語列はnon-machine riskの担当情報"),
    "OWNER_ROLE2": ("ENTRY", "predicate前に対応workerを起動する"),
    "OWNER_ROLE3": ("RESULT", "`delegated_result_ready := runtime_spawn_result.task_name"),
    "OWNER_ROLE4": ("RESULT", "`wait`は同期専用でidentity証跡にしない"),
    "OWNER_ROLE5": ("RESULT", "producer terminal後もfalseなら`unavailable`にする"),
    "OWNER_ROLE6": ("TERMINAL", "bind済みcriterionの`false / failed`"),
    "OWNER_ROLE7": ("RESULT", "異Sender message / root再構成で補完しない"),
    "ROOT1": ("ROOT", "predicate実行 / result再生成をしない"),
    "INDEPENDENCE1": ("INDEPENDENCE", "先行result / artifactを対象とする別operation"),
    "INDEPENDENCE2": ("PRODUCER", "同一predicateを他producerへ順次・並行に再割当てしない"),
    "METHOD1": ("METHOD", "TaskSpec明示手段だけを固定"),
    "METHOD2": ("METHOD", "未固定手段はpredicateを変えずpermission内でexecutorが選ぶ"),
    "METHOD3": ("METHOD", "failed / unavailableをpermission否定 / terminalにせず"),
    "METHOD4": ("METHOD", "明示禁止 / permission否定は停止し、回避しない"),
    "RECOVERY1": ("RECOVERY", "environment-only repair + same required command rerun"),
    "RECOVERY2": ("RECOVERY", "`environment_recovery_max`を消費し、未固定手段の選択は数えない"),
}


def labelled_blocks(text: str) -> dict[str, str]:
    blocks = {}
    for line in text.splitlines():
        if not line.startswith("- "):
            continue
        label, body = line[2:].split(": ", 1)
        blocks[label] = body
    return blocks


class Candidate65Test(unittest.TestCase):
    def test_is_a_single_target_direct_child_of_candidate43(self) -> None:
        source = verify_bundle(C43)
        candidate = verify_bundle(C65)
        self.assertEqual(
            candidate["prompt_identity"],
            "the-caption-3ce91a4-shared-operation-core-r1",
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
            (C65 / "manifest.json").read_text(encoding="utf-8")
        )
        self.assertEqual(
            [entry for entry in candidate_manifest["files"] if entry["target"] != "AGENTS.md"],
            [entry for entry in source_manifest["files"] if entry["target"] != "AGENTS.md"],
        )

    def test_maps_all_32_source_clauses_to_compact_labels(self) -> None:
        text = (C65 / "files/AGENTS.md").read_text(encoding="utf-8")
        blocks = labelled_blocks(text)
        self.assertEqual(len(CLAUSE_COVERAGE), 32)
        self.assertEqual(
            set(blocks),
            {
                "READINESS",
                "SCOPE",
                "PRODUCER",
                "TERMINAL",
                "INDEPENDENCE",
                "ENTRY",
                "CONTEXT",
                "RESULT",
                "ROOT",
                "METHOD",
                "RECOVERY",
            },
        )
        for clause_id, (label, required) in CLAUSE_COVERAGE.items():
            with self.subTest(clause_id=clause_id, label=label):
                self.assertIn(required, blocks[label])

    def test_duplicate_predicates_have_one_compact_occurrence(self) -> None:
        text = (C65 / "files/AGENTS.md").read_text(encoding="utf-8")
        self.assertEqual(
            text.count("TaskSpecが独立producer executionを明示した場合だけ"),
            1,
        )
        self.assertEqual(text.count("同一predicateを他producerへ"), 1)
        self.assertEqual(text.count("bind済みcriterionの`false / failed`"), 1)
        self.assertNotIn("root producer operation", text)
        self.assertNotIn("delegated producer operationへ進む", text)

    def test_has_three_ordered_purpose_regions(self) -> None:
        text = (C65 / "files/AGENTS.md").read_text(encoding="utf-8")
        headings = [
            "## Common operation",
            "## Explicit delegation extension",
            "## Failure and recovery",
        ]
        positions = [text.index(heading) for heading in headings]
        self.assertEqual(positions, sorted(positions))
        self.assertEqual(text.count("\n## "), 3)

    def test_reduces_static_bytes_without_duplicating_full_bundle(self) -> None:
        source_size = (C43 / "files/AGENTS.md").stat().st_size
        candidate_size = (C65 / "files/AGENTS.md").stat().st_size
        self.assertEqual(source_size, 3980)
        self.assertEqual(candidate_size, 3701)
        self.assertLess(candidate_size, source_size)
        self.assertGreater(candidate_size, 3000)

    def test_n5_profiles_change_only_prompt_identity(self) -> None:
        manifest = verify_bundle(C65)
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
