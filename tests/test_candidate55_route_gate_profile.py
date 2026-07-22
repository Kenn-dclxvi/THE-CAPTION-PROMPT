from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
R1 = ROOT / "evaluations/profiles/candidate55-prebound-operation-graph-outcome-quality-owner-diagnostic-v9-targeted2-global-m10-n5-catalog-fixed-r1.json"
R2 = ROOT / "evaluations/profiles/candidate55-prebound-operation-graph-outcome-quality-owner-diagnostic-v9-targeted2-global-m10-n5-catalog-fixed-route-gate-r2.json"
GATE = ROOT / "docs/candidate55-route-efficiency-gate-r2.md"


class Candidate55RouteGateProfileTest(unittest.TestCase):
    def load(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    def test_profile_revision_changes_only_profile_id(self) -> None:
        r1 = self.load(R1)
        r2 = self.load(R2)

        self.assertNotEqual(r1.pop("profile_id"), r2.pop("profile_id"))
        self.assertEqual(r2, r1)

    def test_gate_separates_shell_commands_from_context_rounds(self) -> None:
        text = GATE.read_text(encoding="utf-8")

        self.assertIn("shell command総数を停止条件から外し", text)
        self.assertIn("TaskSpec外read", text)
        self.assertIn("top-level tool call", text)
        self.assertIn("model step", text)
        self.assertIn("新しいprofileと新しい`N=5` result", text)


if __name__ == "__main__":
    unittest.main()
