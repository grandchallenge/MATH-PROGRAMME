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
        # Terminal count grows with protected bounded closure, not certification.
        rows = [r for c in queue.read(queue.REG)["cohorts"] for r in queue.read(c["packet"])["items"]]
        terminals = [r for r in rows if r["closure_status"] == "ADMITTED_BOUNDED_COMPLETE"]
        self.assertEqual(result["substantive_terminal_count"], len(terminals))
        self.assertTrue({1, 27, 560}.issubset({r["problem_id"] for r in terminals}))
        for r in terminals:
            stage = r["stage_work_items"]["D"]
            self.assertEqual(stage["work_status"], "PROTECTED_ADMITTED")
            self.assertRegex(stage["protected_admission_ref"], r"^grandchallenge/MATH-PROGRAMME@[0-9a-f]{40}$")
            self.assertTrue(r["closure_evidence_refs"])
        self.assertEqual(self.row["closure_status"], "ADMITTED_BOUNDED_COMPLETE")
        self.assertEqual(self.row["stage_work_items"]["D"]["protected_admission_ref"], "grandchallenge/MATH-PROGRAMME@bcad3e1b206674fbe090d29496fab75876629241")

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

    def test_per_problem_dependency_eligibility_not_whole_cohort(self):
        first = self.cohort["items"][0]
        second = self.cohort["items"][1]
        self.assertFalse(queue.permitted(first,"B"))
        self.assertFalse(queue.permitted(first,"C"))
        self.assertFalse(queue.permitted(first,"D"))
        # The selected second problem may advance to B only after its A
        # is source reviewed; C/D are always separately dependent.
        # Source completion is necessary, but a returned B task must not
        # become claimable again merely because A remains ready.
        expected=(second["stage_work_items"]["A"]["work_status"] in queue.READY
                  and second["stage_work_items"]["B"]["work_status"]
                      in ("UNEXECUTED","EVIDENCE_BLOCKED")
                  and second["existing_proof_issue"] is None)
        self.assertEqual(queue.permitted(second,"B"),expected)
        # C can become manifest-eligible only after B is critically verified;
        # separate live issue-label and exact protected-blob gates still apply.
        expected_C=(second["stage_work_items"]["B"]["work_status"] in queue.READY
                    and second["stage_work_items"]["C"]["work_status"]
                        in ("UNEXECUTED","EVIDENCE_BLOCKED")
                    and second["triage_decision"]!="PENDING")
        self.assertEqual(queue.permitted(second,"C"),expected_C)
        expected_D = (second["stage_work_items"]["C"]["work_status"] == "PROTECTED_ADMITTED"
                      and bool((second["stage_work_items"]["C"].get("protected_admission_ref") or "").startswith("grandchallenge/MATH-PROGRAMME@"))
                      and second["stage_work_items"]["D"]["work_status"] in ("UNEXECUTED","EVIDENCE_BLOCKED")
                      and second["triage_decision"] != "PENDING")
        self.assertEqual(queue.permitted(second,"D"),expected_D)
        # A later source receipt must not make all 100 items globally ready.
        self.assertFalse(queue.permitted(self.cohort["items"][2],"B"))

    def test_cohort_issue_remains_open_until_every_child(self):
        self.assertFalse(self.cohort["fully_verified"])
        self.assertEqual(len(self.cohort["items"]),100)
        completed_A=sum(row["stage_work_items"]["A"]["work_status"]!="UNEXECUTED"
                        for row in self.cohort["items"])
        self.assertGreaterEqual(completed_A,1)
        self.assertLess(completed_A,100)
        self.assertEqual(self.cohort["items"][2]["stage_work_items"]["A"]["work_status"],
                         "UNEXECUTED")


if __name__ == "__main__":
    unittest.main()
