from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C71 = ROOT / "prompts/candidates/the-caption-3ce91a4-validation-closure-r1"
C73 = ROOT / "prompts/candidates/the-caption-3ce91a4-terminal-closure-preserving-compression-r1"
C71_PROFILE = ROOT / "evaluations/profiles/candidate71-validation-closure-v12-closure-abstraction-targeted4-global-m24-n5-r1.json"
C73_PROFILE = ROOT / "evaluations/profiles/candidate73-terminal-closure-preserving-compression-v12-closure-abstraction-targeted4-global-m24-n5-r1.json"


def labelled_lines(text: str) -> dict[str, str]:
    blocks = {}
    for line in text.splitlines():
        if not line.startswith("- "):
            continue
        label, body = line[2:].split(": ", 1)
        blocks[label] = body
    return blocks


class Candidate73Test(unittest.TestCase):
    def test_is_single_target_direct_child_of_candidate71(self) -> None:
        source = verify_bundle(C71)
        candidate = verify_bundle(C73)
        self.assertEqual(
            candidate["prompt_identity"],
            "the-caption-3ce91a4-terminal-closure-preserving-compression-r1",
        )
        self.assertEqual(
            candidate["content_relation"],
            {
                "changed_targets": ["AGENTS.md"],
                "kind": "direct_child_full_bundle",
                "source_prompt_identity": source["prompt_identity"],
            },
        )
        self.assertEqual(
            [entry for entry in candidate["files"] if entry["target"] != "AGENTS.md"],
            [entry for entry in source["files"] if entry["target"] != "AGENTS.md"],
        )

    def test_preserves_terminal_closure_while_shortening_one_label(self) -> None:
        source = labelled_lines((C71 / "files/AGENTS.md.txt").read_text(encoding="utf-8"))
        candidate = labelled_lines((C73 / "files/AGENTS.md.txt").read_text(encoding="utf-8"))
        self.assertEqual(list(candidate), list(source))
        self.assertEqual(
            {label: body for label, body in candidate.items() if label != "VALIDATION_CLOSURE"},
            {label: body for label, body in source.items() if label != "VALIDATION_CLOSURE"},
        )
        closure = candidate["VALIDATION_CLOSURE"]
        self.assertLess(len(closure.encode("utf-8")), len(source["VALIDATION_CLOSURE"].encode("utf-8")))
        for marker in (
            "identity / command / pass / stop conditionが全件確定",
            "個別invocationとして同一model stepで発行",
            "全resultを一度だけ受領",
            "全件successかつresult有効で追加要求がなければ",
            "追加read / validationなしでterminalを判断",
            "欠落 / non-success / unexpected stateはnonterminal",
            "探索 / 変更前 / review / 未固定method / recoveryには適用しない",
        ):
            self.assertIn(marker, closure)

    def test_targeted_profiles_change_only_prompt_identity(self) -> None:
        manifest = verify_bundle(C73)
        source = json.loads(C71_PROFILE.read_text(encoding="utf-8"))
        candidate = json.loads(C73_PROFILE.read_text(encoding="utf-8"))
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
