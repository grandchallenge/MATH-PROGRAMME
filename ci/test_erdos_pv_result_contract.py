#!/usr/bin/env python3
"""End-to-end canary contract regression: source -> stage A -> scoped return -> B eligibility.

This suite is an OFFLINE contract replay. Actual GitHub ref conflict,
RESULT/1 comment readback, protected merge, and Project field observation
must be tested against the live services separately.
"""
from __future__ import annotations
import copy
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import erdos_pv_result_contract as rc
import erdos_pv_queue as queue

COHORT = "governance/erdos_proof_verification/coverage/cohorts/0001-0100.json"
RECEIPT = "governance/erdos_proof_verification/evidence/0001/SOURCE_SCOPE_RECONCILIATION_001.json"


class E2ELifecycleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cohort = queue.read(COHORT)
        cls.row = cls.cohort["items"][0]
        cls.review = queue.read(RECEIPT)
        assert cls.row["problem_id"] == 1

    def receipt_text(self):
        return (
            "RESULT/1\n"
            "ASSIGNMENT_ID: ERDOS-PV-0001-A\n"
            "PROBLEM_ID: 1\n"
            "PHASE: A\n"
            "COHORT_ISSUE: 3212\n"
            "SOURCE_ISSUE: 1270\n"
            "SOURCE_BODY_SHA256: "
            + self.row["source_issue_body_sha256"] + "\n"
            "DISPOSITION: SOURCE_SCOPE_RECONCILED_CANDIDATE\n"
            "EVIDENCE_REF: " + RECEIPT + "\n"
            "CLAIM_REF: refs/heads/gcl-pv-claims/ERDOS-PV-0001-A\n"
            "\n## Review\n"
            "Historical source review reused, no source-proof kernel certification."
        )

    def test_main_census_unmodified(self):
        result = queue.validate()
        self.assertEqual(result["individual_problems"], 1221)
        self.assertEqual(result["substantive_terminal_count"], 0)

    def test_protected_source_identity_and_review_reuse(self):
        r = self.row
        self.assertEqual(r["source_audit_issue"], 1270)
        self.assertEqual(r["source_issue_live_state"], "CLOSED")
        self.assertEqual(r["triage_decision"], "SELECTED_WITH_MANIFEST")
        self.assertEqual(r["stage_work_items"]["A"]["work_status"], "REUSED_SCOPE_VERIFIED")
        self.assertEqual(r["stage_work_items"]["A"]["review_status"],
                         "PASS_PRIOR_SOURCE_REVIEW_REUSED")
        self.assertEqual(self.review["assignment_id"], "ERDOS-PV-0001-A")
        self.assertFalse(self.review["nonclaims"]["full_source_proof_replayed"])
        self.assertFalse(self.review["nonclaims"]["autonomous_agent_dispatch_proven"])

    def test_exact_bound_result_passes(self):
        d = rc.validate_return(self.row, "A", self.receipt_text())
        self.assertEqual(d["COHORT_ISSUE"], "3212")
        self.assertEqual(d["ASSIGNMENT_ID"], "ERDOS-PV-0001-A")

    def test_duplicate_return_rejected(self):
        with self.assertRaisesRegex(ValueError, "duplicate"):
            rc.validate_return(self.row, "A", self.receipt_text(),
                               ["EVIDENCE_REVIEW/1\nold", self.receipt_text()])

    def test_wrong_source_hash_rejected(self):
        with self.assertRaisesRegex(ValueError, "mismatch"):
            rc.validate_return(self.row, "A", self.receipt_text().replace(
                self.row["source_issue_body_sha256"], "f" * 64))

    def test_wrong_source_issue_rejected(self):
        with self.assertRaisesRegex(ValueError, "mismatch"):
            rc.validate_return(self.row, "A", self.receipt_text().replace(
                "SOURCE_ISSUE: 1270", "SOURCE_ISSUE: 1271"))

    def test_wrong_phase_rejected(self):
        with self.assertRaises(ValueError):
            rc.validate_return(self.row, "A", self.receipt_text().replace(
                "PHASE: A", "PHASE: B"))

    def test_false_proof_certification_rejected(self):
        with self.assertRaises(ValueError):
            rc.validate_return(self.row, "A", self.receipt_text().replace(
                "SOURCE_SCOPE_RECONCILED_CANDIDATE", "MATHCERT_CERTIFIED"))

    def test_claim_ref_misrouting_rejected(self):
        with self.assertRaisesRegex(ValueError, "claim-ref"):
            rc.validate_return(self.row, "A", self.receipt_text().replace(
                "gcl-pv-claims/ERDOS-PV-0001-A", "gcl-pv-claims/ERDOS-PV-0002-A"))

    def test_unbound_protected_state_cannot_release(self):
        self.assertFalse(rc.can_release_after_readback(
            self.row, "A", "grandchallenge/MATH-PROGRAMME@" + "1" * 40))

    def test_one_stage_A_enables_only_same_problem_B(self):
        b = queue.candidates("B", limit=20)
        self.assertEqual([(x["problem_id"], x["queue_issue"]) for x in b], [(1, 3225)])
        self.assertEqual(queue.candidates("C", limit=20), [])
        self.assertEqual(queue.candidates("D", limit=20), [])
        self.assertEqual(self.cohort["items"][1]["stage_work_items"]["A"]["work_status"],
                         "UNEXECUTED")
        self.assertEqual(self.cohort["items"][1]["stage_work_items"]["B"]["work_status"],
                         "UNEXECUTED")

    def test_cohort_issue_not_complete_after_one_child(self):
        self.assertFalse(self.cohort["fully_verified"])
        self.assertEqual(len(self.cohort["items"]), 100)
        self.assertEqual(sum(x["stage_work_items"]["A"]["work_status"] != "UNEXECUTED"
                             for x in self.cohort["items"]), 1)

if __name__ == "__main__":
    unittest.main()
