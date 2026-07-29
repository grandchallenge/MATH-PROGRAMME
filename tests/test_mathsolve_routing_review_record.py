from __future__ import annotations

import json
import unittest
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
REVIEW_PATH = ROOT / "reviews" / "mathsolve_routing" / "MP-MS-WP00-POSTMERGE.agent_review.yaml"
LEDGER_PATH = ROOT / "reviews" / "mathsolve_routing" / "ARTIFACT_LEDGER.md"
TERMS_PATH = ROOT / "reviews" / "mathsolve_routing" / "TERMINOLOGY.md"


class MathSolveRoutingReviewRecordTests(unittest.TestCase):
    def test_review_is_schema_valid(self) -> None:
        schema = json.loads(
            (ROOT / "schemas" / "agent_review.schema.json").read_text(encoding="utf-8")
        )
        review = yaml.safe_load(REVIEW_PATH.read_text(encoding="utf-8"))
        errors = list(
            Draft202012Validator(
                schema, format_checker=FormatChecker()
            ).iter_errors(review)
        )
        self.assertEqual(errors, [], [error.message for error in errors])

    def test_requested_offices_are_reviewed(self) -> None:
        review = yaml.safe_load(REVIEW_PATH.read_text(encoding="utf-8"))
        council = review["council_review"]
        for office in ("Adversary", "Formalist", "Amanuensis", "Referee"):
            self.assertEqual(council[office]["status"], "reviewed")
        self.assertEqual(review["artifact"]["status"], "active")
        self.assertFalse(review["promotion"]["ready_for_next_stage"])

    def test_continuity_files_resolve(self) -> None:
        review = yaml.safe_load(REVIEW_PATH.read_text(encoding="utf-8"))
        ledger_ref = review["amanuensis_control"]["artifact_ledger"]["ledger_ref"]
        terminology_ref = review["amanuensis_control"]["terminology_registry"]["registry_ref"]
        self.assertEqual(ROOT / ledger_ref, LEDGER_PATH)
        self.assertEqual(ROOT / terminology_ref, TERMS_PATH)
        self.assertTrue(LEDGER_PATH.is_file())
        self.assertTrue(TERMS_PATH.is_file())
        self.assertIn(
            review["amanuensis_control"]["artifact_ledger"]["entry_id"],
            LEDGER_PATH.read_text(encoding="utf-8"),
        )

    def test_all_provenance_files_exist_or_are_github_urls(self) -> None:
        review = yaml.safe_load(REVIEW_PATH.read_text(encoding="utf-8"))
        for ref in review["amanuensis_control"]["review_provenance"]["evidence_refs"]:
            if ref.startswith("https://github.com/"):
                continue
            self.assertTrue((ROOT / ref).exists(), ref)


if __name__ == "__main__":
    unittest.main()
