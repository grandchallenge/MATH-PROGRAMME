"""Exact fourth-order additive-energy identity on genuine finite M3 carriers.

Mathematical source: OFF_SPECTRUM_FOURTH_MOMENT.md.
"""
from collections import Counter
from fractions import Fraction
from random import Random
import unittest
from tests import test_erdos41_shadow_correlation as pairlib
pair_sums = pairlib.pair_sums
autocorrelations = pairlib.autocorrelations
difference = pairlib.difference
is_b3 = pairlib.is_b3


def energy_from_pairset(P):
    r=Counter(p-q for p in P for q in P)
    return sum(c*c for c in r.values())


class OffSpectrumEnergyTests(unittest.TestCase):
    A=pairlib.CorrelationSpectrumTests.A

    def test_exact_off_spectrum_decomposition_on_genuine_b3(self):
        self.assertTrue(is_b3(self.A))
        rng=Random(41)
        cases=[self.A[:n] for n in (1,2,3,4,6,8,12,18,29)]
        cases.extend(tuple(rng.sample(self.A,n)) for n in (1,3,7,14,20))
        for X in cases:
            n=len(X);P=pair_sums(X);R=autocorrelations(X)
            q=n*(n+1)//2
            self.assertEqual(len(P),q)
            total=energy_from_pairset(P)
            D= difference(self.A)
            on=sum(R[d]**2 for d in D)
            off=sum(cnt*cnt for d,cnt in R.items() if d not in D)
            self.assertEqual(on,q*q+n**3*(n-1))
            self.assertEqual(total,on+off)
            self.assertGreaterEqual(off,0)

    def test_cauchy_and_rational_lower_bounds(self):
        rng=Random(593)
        for X in (self.A[:n] for n in (1,2,3,6,10,15,24,29)):
            n=len(X);q=n*(n+1)//2;diam=max(X)-min(X)
            r=autocorrelations(X)
            e=sum(c*c for c in r.values())
            dA=difference(self.A)
            off=sum(c*c for d,c in r.items() if d not in dA)
            lower=Fraction(q**4,4*diam+1)-q*q-n**3*(n-1)
            self.assertGreaterEqual(off,lower)
            self.assertGreaterEqual(off,0)
            if diam:
                self.assertGreaterEqual(
                    off,Fraction(n**8,80*diam)-2*n**4)
            self.assertGreaterEqual((4*diam+1)*e,q**4)

    def test_critical_scale_algebra_conditional_not_a_b3_fixture(self):
        # D=n^3 is a hypothetical critical-scale arithmetic model.
        # No assertion of B3 realizability is made.
        for n in (321,400,800,2000):
            D=n**3
            lower=Fraction(n**8,80*D)-2*n**4
            self.assertGreaterEqual(lower,Fraction(n**5,160))

    def test_actual_zero_difference_energy_and_outer_carrier_dependence(self):
        X=self.A[:6]
        R=autocorrelations(X)
        q=len(pair_sums(X))
        self.assertEqual(R[0]**2,q*q)
        for A in (X,self.A[:10],self.A):
            dA=difference(A)
            known=sum(R[d]**2 for d in dA)
            self.assertEqual(known,q*q+len(X)**3*(len(X)-1))
            self.assertEqual(sum(c*c for c in R.values())-known,
                             sum(c*c for d,c in R.items() if d not in dA))

    def test_non_b3_cluster_invalidates_exact_selector_identity(self):
        X=(1,2,3)
        self.assertFalse(is_b3(X))
        R=autocorrelations(X)
        q=len(pair_sums(X))
        r_on=sum(R[d]**2 for d in difference(X))
        self.assertNotEqual(r_on,q*q+len(X)**3*(len(X)-1))


if __name__=='__main__':
    unittest.main()
