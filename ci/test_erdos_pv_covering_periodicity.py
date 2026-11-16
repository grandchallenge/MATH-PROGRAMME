#!/usr/bin/env python3
"""Adversarial tests for Erdős #2's bounded periodicity implementation."""
from __future__ import annotations
import copy
import json
from math import lcm
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from erdos_pv_covering_periodicity import (
    HOUGH_SIX, direct_covered, finite_certificate, fixture_payload,
    verify_certificate,
)

FIXTURE = (Path(__file__).resolve().parents[1] /
           "governance/erdos_proof_verification/evidence/0002/"
           "B_COVERING_PERIODICITY_FINITE_FIXTURES_001.json")


class PeriodicityTests(unittest.TestCase):
    def test_positive_hough_six(self):
        cert = finite_certificate(HOUGH_SIX)
        self.assertEqual((cert["period"],cert["uncovered_residues"]),(24,[]))
        self.assertTrue(cert["covers_all_integers"])
        self.assertTrue(cert["distinct_moduli"])
        self.assertTrue(verify_certificate(HOUGH_SIX,cert))

    def test_strict_last_class_mutation(self):
        bad = HOUGH_SIX[:-1] + ((24,24),)
        c = finite_certificate(bad)
        self.assertEqual(c["uncovered_residues"],[23])
        self.assertFalse(c["covers_all_integers"])
        self.assertTrue(verify_certificate(bad,c))

    def test_duplicate_modulus_is_not_a_distinct_cover(self):
        x=((0,2),(1,2))
        c=finite_certificate(x)
        self.assertTrue(c["covers_all_integers"])
        self.assertFalse(c["distinct_moduli"])
        self.assertTrue(verify_certificate(x,c))

    def test_empty_list_does_not_cover(self):
        c=finite_certificate(())
        self.assertEqual((c["period"],c["uncovered_residues"]),(1,[0]))
        self.assertFalse(c["covers_all_integers"])
        self.assertTrue(verify_certificate((),c))

    def test_single_even_class_does_not_cover(self):
        c=finite_certificate(((0,2),))
        self.assertEqual(c["uncovered_residues"],[1])

    def test_integer_shifts_and_negative_residues(self):
        one=finite_certificate(((23,24),))
        self.assertEqual(one,finite_certificate(((-1,24),)))
        self.assertEqual(one,finite_certificate(((23+7*24,24),)))

    def test_periodicity_for_negative_and_positive_integers(self):
        L=lcm(*(m for _,m in HOUGH_SIX))
        for n in range(-7*L,7*L+1):
            self.assertEqual(direct_covered(HOUGH_SIX,n),
                             direct_covered(HOUGH_SIX,n+L))
            c=finite_certificate(HOUGH_SIX)
            self.assertEqual(direct_covered(HOUGH_SIX,n),
                             c["first_witness_index_by_residue"][n%L]>=0)

    def test_wrong_witness_fails_independent_check(self):
        c=finite_certificate(HOUGH_SIX)
        c["first_witness_index_by_residue"][23]=0
        with self.assertRaisesRegex(ValueError,"witness"):
            verify_certificate(HOUGH_SIX,c)

    def test_forged_coverage_metadata_fails(self):
        c=finite_certificate(((0,2),))
        c["covers_all_integers"]=True
        with self.assertRaisesRegex(ValueError,"coverage"):
            verify_certificate(((0,2),),c)

    def test_false_distinctness_fails(self):
        rows=((0,2),(1,2))
        c=finite_certificate(rows)
        c["distinct_moduli"]=True
        with self.assertRaisesRegex(ValueError,"distinct"):
            verify_certificate(rows,c)

    def test_wrong_period_fails(self):
        c=finite_certificate(((0,2),))
        c["period"]=3
        with self.assertRaisesRegex(ValueError,"period"):
            verify_certificate(((0,2),),c)

    def test_resource_cap_means_unchecked_not_false(self):
        with self.assertRaisesRegex(ValueError,"RESOURCE_CAP"):
            finite_certificate(((0,101),(0,103)),max_period=1000)

    def test_nonpositive_and_noninteger_moduli_rejected(self):
        for row in ((0,0),(0,1),(0,-2),(0,2.5),(0,True),
                    (False,2),("0",2)):
            with self.subTest(row=row),self.assertRaises(ValueError):
                finite_certificate((row,))

    def test_nonnumeric_capacity_rejected(self):
        for cap in (0,-1,False,1.1):
            with self.subTest(cap=cap),self.assertRaises(ValueError):
                finite_certificate(HOUGH_SIX,max_period=cap)

    def test_exhaustive_144_small_assignments(self):
        record=fixture_payload()
        self.assertEqual(record["exhaustive_small_distinct_assignments_checked"],144)
        self.assertFalse(record["lean_kernel_replayed"])

    def test_frozen_evidence_equals_regenerated(self):
        saved=json.loads(FIXTURE.read_text())
        self.assertEqual(saved,fixture_payload())


if __name__ == "__main__":
    unittest.main()
