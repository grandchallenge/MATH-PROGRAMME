#!/usr/bin/env python3
"""Hostile and two-oracle regression for ERDOS-PV-0560-B."""
import json
import unittest
from fractions import Fraction
from pathlib import Path

from ci import erdos_pv_bipartite_count_0560 as p

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "governance/erdos_proof_verification/evidence/0560/B_FINITE_COUNTING_001.json"


class CopyCount0560Tests(unittest.TestCase):
    def test_empty_edgeless_and_small_hosts(self):
        for n in (0, 1, 4, 6, 8):
            adj = p.neighbors(n, 0)
            self.assertEqual(p.graph_edges(adj), 0)
            self.assertEqual(p.producer(adj, 2, 4)[0], 0)
            self.assertEqual(p.oracle(adj, 2, 4), 0)

    def test_complete_graph_count_and_unique_side_orientation(self):
        for n, s, t in ((6, 2, 4), (7, 2, 4),
                         (8, 3, 5), (9, 3, 6)):
            adj = p.neighbors(n, 2 ** (n*(n-1)//2) - 1)
            expected = p.comb(n, s)*p.comb(n-s, t)
            self.assertEqual(p.producer(adj, s, t)[0], expected)
            self.assertEqual(p.oracle(adj, s, t), expected)

    def test_last_index_bucket_assignment(self):
        adj = p.neighbors(7, 2**21-1)
        count, buckets, bound = p.producer(adj, 2, 4)
        self.assertEqual(count, 105)
        self.assertEqual(sum(buckets), count)
        self.assertEqual(buckets[-1], 30)
        # Deleting the s-side multiplicity factor is a concrete false bound.
        self.assertGreater(buckets[-1], p.comb(6,4))
        self.assertTrue(all(a<=b for a,b in zip(buckets,bound)))

    def test_orientation_and_hypothesis_exclusions(self):
        for args in ((0,2),(1,3),(2,2),(2,3),(3,4),(4,5),(-2,0)):
            with self.subTest(args=args), self.assertRaises(ValueError):
                p.parameters(*args)
        for args in ((True,4),(2,4.0)):
            with self.assertRaises(ValueError):
                p.parameters(*args)

    def test_invalid_graphs_fail_closed(self):
        for adj in ((1,), (2,0), (-1,0), (4,0), (0,1)):
            with self.subTest(adj=adj), self.assertRaises(ValueError):
                p.graph_edges(adj)
        with self.assertRaises(ValueError):
            p.neighbors(7,2**21)
        with self.assertRaises(ValueError):
            p.neighbors(10,0)

    def test_power_sum_factor_exact_fraction(self):
        self.assertEqual(p.integral_factor(2,4),Fraction(4,1))
        self.assertEqual(p.integral_factor(3,5),Fraction(9,2))
        for s in range(2,25):
            for t in range(s+2,65):
                self.assertLessEqual(p.integral_factor(s,t),2**t)

    def test_strict_first_moment_and_threshold(self):
        self.assertEqual(p.first_moment(1,2,4),Fraction(1,128))
        self.assertLess(2*(Fraction(18,25)**4),1)
        self.assertGreaterEqual(p.first_moment(420,2,4),1)
        with self.assertRaises(ValueError):
            p.first_moment(-1,2,4)
        with self.assertRaises(ValueError):
            p.first_moment(0.5,2,4)

    def test_exact_claim_and_result_comment_binding(self):
        name='governance/erdos_proof_verification/evidence/0560/B_RETURN_BINDING_001.json'
        doc=json.loads((ROOT/name).read_text())
        self.assertEqual(doc['assignment_id'],p.TASK)
        self.assertEqual(doc['return_comment_id'],6944746101)
        self.assertEqual(doc['return_body_sha256'],
                         'f5c282e50bef75522ba306f10126c5ff7763f8dd92076eb7e69b3162e60258b3')
        self.assertEqual(doc['source_issue_body_sha256'],p.SOURCE_SHA256)
        self.assertEqual(doc['claim_commit'],
                         '321bcc27a63b0732b7154cc7dd0aa6d1fe3549f5')
        self.assertEqual(doc['return_disposition'],'BOUNDED_RESULT_RETURNED')
        self.assertIs(doc['mathematical_certification'],False)

    def test_reproducible_exhaustive_and_seeded_certificate(self):
        actual = p.regenerate()
        pinned = json.loads(FIXTURE.read_text(encoding="utf-8"))
        self.assertEqual(actual,pinned)
        self.assertEqual(actual["exhaustive"]["graph_cases"],32768)
        self.assertGreater(actual["exhaustive"]["positive_cases"],0)
        self.assertGreater(actual["sampled"][-1]["positive_cases"],0)
        self.assertGreater(actual["total_graph_oracle_checks"],36000)

    def test_protected_stage_source_binding(self):
        packet=json.loads((ROOT/"governance/erdos_proof_verification/coverage/cohorts/0501-0600.json").read_text())
        row=packet["items"][560-501]
        self.assertEqual(row["source_issue_body_sha256"],p.SOURCE_SHA256)
        self.assertEqual(row["triage_decision"],"SELECTED_WITH_MANIFEST")
        self.assertEqual(row["stage_work_items"]["B"]["task_id"],p.TASK)


if __name__ == "__main__":
    unittest.main()
