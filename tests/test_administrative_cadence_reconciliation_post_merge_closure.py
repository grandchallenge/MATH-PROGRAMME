from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "governance" / "administrative_cadence_reconciliation_post_merge_closure.json"
SCHEMA = ROOT / "schemas" / "administrative_cadence_reconciliation_post_merge_closure.schema.json"


class AdministrativeCadenceReconciliationPostMergeClosureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        cls.validator = Draft202012Validator(cls.schema)

    def fresh_record(self) -> dict:
        return json.loads(RECORD.read_text(encoding="utf-8"))

    def errors_for(self, record: dict) -> list[str]:
        return [error.message for error in self.validator.iter_errors(record)]

    def test_record_is_schema_valid(self) -> None:
        self.assertEqual(self.errors_for(self.fresh_record()), [])

    def test_merge_binds_reviewed_head(self) -> None:
        record = self.fresh_record()
        self.assertEqual(
            record["source_pull_request"]["reviewed_head"],
            "55acabde79b03f04a06d0c21c6b50c04e47da14b",
        )
        self.assertTrue(record["protected_merge"]["merged_head_matches_reviewed_head"])

    def test_historical_candidate_is_preserved_non_cyclically(self) -> None:
        record = self.fresh_record()
        self.assertEqual(record["predecessor"]["historical_status"], "IMPLEMENTED_PENDING_PROTECTED_REVIEW")
        self.assertTrue(record["predecessor"]["preserved_without_rewrite"])
        self.assertTrue(record["predecessor"]["successor_closure_is_non_cyclic"])

    def test_documentary_defect_does_not_erase_p2_findings(self) -> None:
        record = self.fresh_record()
        self.assertEqual(record["closure_disposition"]["original_p2_findings_preserved"], 5)
        self.assertFalse(record["closure_disposition"]["substantive_reexecution_required"])
        self.assertTrue(record["closure_disposition"]["pilot_level_escalation_remains_required"])

    def test_mutation_rejects_wrong_merge_commit(self) -> None:
        record = self.fresh_record()
        record["protected_merge"]["merge_commit"] = "0" * 40
        self.assertTrue(self.errors_for(record))

    def test_mutation_rejects_review_head_drift(self) -> None:
        record = self.fresh_record()
        record["source_pull_request"]["reviewed_head"] = "f" * 40
        self.assertTrue(self.errors_for(record))

    def test_mutation_rejects_missing_independent_approval(self) -> None:
        record = self.fresh_record()
        record["source_pull_request"]["review_state"] = "COMMENTED"
        self.assertTrue(self.errors_for(record))

    def test_mutation_rejects_false_github_comment_claim(self) -> None:
        record = self.fresh_record()
        record["human_steward_disposition"]["github_exact_head_comment_present"] = True
        self.assertTrue(self.errors_for(record))

    def test_mutation_rejects_p2_erasure(self) -> None:
        record = self.fresh_record()
        record["closure_disposition"]["original_p2_findings_preserved"] = 0
        self.assertTrue(self.errors_for(record))

    def test_mutation_rejects_waiver_or_anchor_reset(self) -> None:
        record = self.fresh_record()
        record["closure_disposition"]["waiver_used"] = True
        record["closure_disposition"]["cadence_anchor_reset"] = True
        self.assertTrue(self.errors_for(record))

    def test_mutation_rejects_deadline_reset(self) -> None:
        record = self.fresh_record()
        record["retained_deadlines"]["next_structural_sweep"] = "2026-08-05T15:57:00-07:00"
        self.assertTrue(self.errors_for(record))

    def test_mutation_rejects_claim_inflation(self) -> None:
        record = copy.deepcopy(self.fresh_record())
        record["claim_boundaries"]["cert_output_issued"] = True
        self.assertTrue(self.errors_for(record))


if __name__ == "__main__":
    unittest.main()
