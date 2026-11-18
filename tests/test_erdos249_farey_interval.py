"""Exact Farey certificate adversarial tests; no inferred irrationality."""
import hashlib
import itertools
import json
import math
import unittest
from fractions import Fraction
from pathlib import Path

from experiments.erdos249_full_series_phase.farey_interval import (phi_sieve, prefix_integer, interval_neighbors, compute, validate_receipt)


class FareyExclusionTests(unittest.TestCase):
    def test_phi_sieve_against_gcd(self):
        phi=phi_sieve(512)
        for n in range(1,513):
            self.assertEqual(phi[n],sum(math.gcd(n,j)==1 for j in range(1,n+1)))
        self.assertEqual(phi[1:11],[1,1,2,2,4,2,6,4,6,4])

    def test_prefix_exact_independent_direct_sum(self):
        phi=phi_sieve(72)
        for N in (8,16,31,48,64):
            A=prefix_integer(phi,N)
            naive=sum(phi[n]<<(N-n) for n in range(1,N+1))
            self.assertEqual(A,naive)

    def test_simplest_fraction_bruteforce(self):
        # Brute scan exact rational p/q, 1<=q<q_min, at low depths.
        for N in (8,9,10,12,16,20,24):
            z=compute(N)
            A=int(z["numerator_prefix"])
            Q=1<<N
            D=N+2
            qstar=int(z["minimal_denominator"])
            for q in range(1,qstar):
                lo=A*q//Q+1
                hi=((A+D)*q-1)//Q
                self.assertGreater(lo,hi,(N,q,lo,hi))
            p=int(z["first_interior_fraction"][0])
            self.assertLess(A*qstar,p*Q)
            self.assertLess(p*Q,(A+D)*qstar)

    def test_farey_adjacency_exact_and_mutation_rejection(self):
        for N in (240,4096,65536):
            r=json.loads((Path(__file__).resolve().parents[1]/"experiments"/"erdos249_full_series_phase"/f"K{N}.json").read_text())
            validate_receipt(r)
            left=list(r["farey_left"])
            r["farey_left"][1]=str(int(left[1])+1)
            with self.assertRaises(AssertionError):
                validate_receipt(r)

    def test_large_receipts_recompute_original_totient_prefix(self):
        for N in (240,4096,65536):
            r=json.loads((Path(__file__).resolve().parents[1]/"experiments"/"erdos249_full_series_phase"/f"K{N}.json").read_text())
            validate_receipt(r)
            assert r["N"]==N
            phi=phi_sieve(N)
            A=prefix_integer(phi,N)
            self.assertEqual(int(r["numerator_prefix"]),A)
            self.assertEqual(hashlib.sha256(str(A).encode()).hexdigest(),r["prefix_sha256"])
            self.assertEqual(r["minimal_denominator_digits"],len(r["minimal_denominator"]))
            self.assertGreaterEqual(int(r["minimal_denominator"]),10**(r["minimal_denominator_digits"]-1))

    def test_monotone_interval_refinements(self):
        # The exact enclosures are nested; minimal compatible denominator cannot decrease.
        xs=[compute(N) for N in (8,16,32,48,64,96,128,240)]
        denominators=[int(r["minimal_denominator"]) for r in xs]
        self.assertEqual(denominators,sorted(denominators))
        self.assertEqual(len(str(denominators[-1])),35)

    def test_rational_comparator_falsifies_irrationality_inference(self):
        # a_n=2*floor(n/2), sum a_n 2^-n=4/3 exactly.
        for N in (24,48,96):
            prefix=sum((2*(n//2))<<(N-n) for n in range(1,N+1))
            lo=Fraction(prefix,1<<N)
            upper=lo+Fraction(N+2,1<<N)
            self.assertLess(lo,Fraction(4,3))
            self.assertLess(Fraction(4,3),upper)
            self.assertEqual(Fraction(4,3).denominator,3)

    def test_result_scope_and_hashes(self):
        p=Path(__file__).resolve().parents[1]/"experiments"/"erdos249_full_series_phase"
        r=json.loads((p/"K65536.json").read_text())
        self.assertEqual(r["status"],"FINITE_EXCLUSION_ONLY_S_IRRATIONALITY_OPEN")
        self.assertEqual(r["minimal_denominator_digits"],9862)
        self.assertEqual(r["stern_brocot_steps"],19184)
        self.assertGreater(int(r["minimal_denominator"]),10**9861)
