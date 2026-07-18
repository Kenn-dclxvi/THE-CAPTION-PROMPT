import unittest
from pathlib import Path

from scripts.response_evidence import load_contract, semantic_marker_failures


class ResponseEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contract = load_contract(
            Path(__file__).resolve().parents[1]
            / "evaluations/rating-contracts/owner-producer-quality-v7.json"
        )

    def test_accepts_english_fallback_form(self) -> None:
        failures = semantic_marker_failures(
            self.contract,
            "TC-F05-CLARIFY-UNITS-MODE",
            "Choose DAILY or STRICT, and say whether live CSV FALLBACK is allowed.",
        )
        self.assertEqual(failures, [])

    def test_accepts_japanese_fallback_form(self) -> None:
        failures = semantic_marker_failures(
            self.contract,
            "TC-F05-CLARIFY-UNITS-MODE",
            "dailyとstrictのどちらにしますか。strict時にlive CSVへのフォールバックを許可しますか。",
        )
        self.assertEqual(failures, [])

    def test_reports_missing_fallback_policy(self) -> None:
        failures = semantic_marker_failures(
            self.contract,
            "TC-F05-CLARIFY-UNITS-MODE",
            "dailyとstrictのどちらにしますか。",
        )
        self.assertEqual(
            failures,
            ["response_concept_missing:live_csv_fallback_policy"],
        )

    def test_case_without_marker_contract_has_no_failures(self) -> None:
        self.assertEqual(
            semantic_marker_failures(self.contract, "TC-F01-OTHER", ""),
            [],
        )


if __name__ == "__main__":
    unittest.main()
