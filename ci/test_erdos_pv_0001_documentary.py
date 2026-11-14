#!/usr/bin/env python3
"""Fail-closed documentary/source-claim review for the Erdős #1 bounded verifier."""
import hashlib
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTICLE = ROOT / "governance/erdos_compendium/editorial/0001.md"
REVIEW = ROOT / "governance/erdos_proof_verification/evidence/0001/DOCUMENTARY_SOURCE_AND_CRITIC_001.md"
REPLAY = ROOT / "governance/erdos_proof_verification/evidence/0001/LEAN_REPLAY_43541084973"
COHORT = ROOT / "governance/erdos_proof_verification/coverage/cohorts/0001-0100.json"
SHA256 = "64026cab37a6ba0bbe18d154ad64b38fe311d933dd0804e2c1a3414a9802cf78"

class DocumentaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.article = ARTICLE.read_text()
        cls.review = REVIEW.read_text()
        cls.receipt = json.loads((REPLAY/"RECEIPT.json").read_text())
        cls.critic = json.loads((REPLAY/"INDEPENDENT_GCL_REVIEW.json").read_text())
        cls.row = json.loads(COHORT.read_text())["items"][0]

    def test_article_bytes_bound_to_review(self):
        h = hashlib.sha256(self.article.strip().encode()).hexdigest()
        self.assertEqual(h, SHA256)
        self.assertIn(SHA256, self.review)

    def test_six_reader_sections(self):
        self.assertEqual(re.findall(r"(?m)^## (.+)$", self.article),
            ["The question in plain language", "A small example",
             "What is known", "GCL's current state", "What remains",
             "Sources and claim boundaries"])

    def test_no_obsolete_delimiters(self):
        self.assertNotIn(chr(92)+"(", self.article)
        self.assertNotIn(chr(92)+")", self.article)

    def test_example_is_actually_distinct(self):
        weights = (3,5,6,7)
        sums = {sum(w for i,w in enumerate(weights) if mask & (1<<i))
                for mask in range(16)}
        self.assertEqual(len(sums),16)

    def test_historical_status_not_promoted(self):
        self.assertIn("**The original conjecture is disproved.**", self.article)
        self.assertIn("does *not* say", self.article)

    def test_source_locked_kernel_receipt(self):
        self.assertEqual(self.receipt["result"],"LEAN_KERNEL_REPLAY_PASS_UNADJUDICATED")
        self.assertEqual((self.receipt["build_exit"],self.receipt["readback_exit"],
                          self.receipt["negative_exit"]),(0,0,1))
        self.assertIn("43541084973",self.article)
        self.assertEqual(self.receipt["source"]["toolchain"],"leanprover/lean4:v4.28.0")

    def test_allowed_kernel_axioms(self):
        self.assertEqual(len(self.receipt["axioms"]),2)
        for axioms in self.receipt["axioms"].values():
            self.assertEqual(set(axioms),{"propext","Classical.choice","Quot.sound"})

    def test_required_hypothesis_negative(self):
        self.assertTrue(self.critic["compiler"]["negative_test_rejected_missing_RelationFree"])
        self.assertIn("relation-freedom hypothesis",self.article)

    def test_full_source_not_independently_adjudicated(self):
        self.assertFalse(self.critic["full_disproof_independent_mathematical_verification"])
        self.assertFalse(self.critic["mathcert_certified"])
        self.assertIn("not independently reconstructed",self.article)
        self.assertIn("MATHCERT certification",self.article)

    def test_stage_D_only_for_problem_1(self):
        self.assertEqual(self.row["problem_id"],1)
        self.assertEqual(self.row["stage_work_items"]["B"]["work_status"],"PROTECTED_ADMITTED")
        self.assertEqual(self.row["stage_work_items"]["C"]["work_status"],"PROTECTED_ADMITTED")
        self.assertIn(self.row["stage_work_items"]["D"]["work_status"],
                      {"UNEXECUTED","IN_PROGRESS","VERIFIED_BOUNDED","PROTECTED_ADMITTED"})
        self.assertEqual(self.row["mathcert_status"],"NOT_SUBMITTED")

    def test_legacy_editorial_requires_separate_admission(self):
        self.assertIn("legacy explanatory exemplar",self.review)
        self.assertIn("editorial admission",self.review)
        self.assertIn("https://grandchallenge.github.io/MATH-PROGRAMME/erdos/problems/0001/",self.review)

if __name__=="__main__":
    unittest.main()
