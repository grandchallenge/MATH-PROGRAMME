from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "governance" / "administrative_pilot_reviews" / "MP-ADMIN-PILOT-REVIEW-2026-08-10-001.json"
SCHEMA = ROOT / "schemas" / "administrative_pilot_review_completion.schema.json"
ADJUDICATION = ROOT / "governance" / "administrative_pilot_adjudication_2026_08_10.json"


class AdministrativePilotReviewCompletionTests(unittest.TestCase):
    def load_record(self):
        return json.loads(RECORD.read_text(encoding="utf-8"))

    def load_schema(self):
        return json.loads(SCHEMA.read_text(encoding="utf-8"))

    def validate(self, value):
        jsonschema.Draft202012Validator(self.load_schema()).validate(value)

    def test_record_binds_protected_adjudication(self):
        record = self.load_record()
        adjudication = json.loads(ADJUDICATION.read_text(encoding="utf-8"))
        self.validate(record)
        self.assertEqual(record["procedure_id"], "pilot_review")
        self.assertEqual(record["scheduled_due_at"], "2026-08-10T01:21:00Z")
        self.assertEqual(record["adjudication"]["docket"], adjudication["docket"])
        self.assertEqual(record["adjudication"]["adjudication_id"], adjudication["adjudication_id"])
        self.assertEqual(record["adjudication"]["decision"], adjudication["decision"]["disposition"])
        self.assertEqual(record["adjudication"]["residual_hardening_issue"], adjudication["hardening"]["residual_open_issue"])

    def test_receipt_contract_is_fail_closed(self):
        record = self.load_record()
        self.assertTrue(record["receipt_contract"]["separate_protected_receipt_required"])
        self.assertTrue(record["receipt_contract"]["binds_actual_adjudication_merge"])
        self.assertTrue(record["receipt_contract"]["premerge_candidate_head_is_not_completion_authority"])
        self.assertTrue(record["historical_evidence_policy"]["preserve_lateness"])
        self.assertTrue(all(value is False for value in record["claim_boundaries"].values()))

    def test_critical_mutations_fail_schema(self):
        mutations = (
            ("adjudication", "protected_merge", "0" * 40),
            ("adjudication", "reviewed_head", "0" * 40),
            ("adjudication", "decision", "REVERT_TO_1_0"),
            ("receipt_contract", "binds_actual_adjudication_merge", False),
            ("receipt_contract", "premerge_candidate_head_is_not_completion_authority", False),
            ("historical_evidence_policy", "preserve_lateness", False),
            ("authority_boundary", "future_control_plane_change_authorized", True),
            ("authority_boundary", "hardening_issue_407_is_implementation_authority", True),
            ("claim_boundaries", "external_claim_authorized", True),
        )
        for section, field, value in mutations:
            record = copy.deepcopy(self.load_record())
            record[section][field] = value
            with self.subTest(section=section, field=field):
                with self.assertRaises(jsonschema.ValidationError):
                    self.validate(record)


if __name__ == "__main__":
    unittest.main()
