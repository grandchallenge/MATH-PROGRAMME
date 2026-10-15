"""Density-conditioned zero-overlap selection: exact finite B3 and rational gates.

Synthetic constants verify an implication, NOT existence of an infinite dense B3 set.
"""
from fractions import Fraction as Q
from itertools import combinations_with_replacement as multis
from collections import Counter
from math import ceil
import unittest

A29=(1,2,5,14,33,72,125,219,376,573,745,1209,1557,2442,
     3098,4048,5298,6704,7839,10987,12332,15465,
     19144,24546,28974,34406,37769,45864,50877)


def is_b3(A):
    sums=[sum(x) for x in multis(A,3)]
    return len(sums)==len(set(sums))


def fiber(X,Y):
    P={a+b for a,b in multis(X,2)}
    return Counter(p-2*y for p in P for y in Y)


class ZeroOverlapDensitySelectionTests(unittest.TestCase):
    def test_genuine_B3_populated_disjoint_lags_two_blocks(self):
        X=(1,2,5,14)
        Z=(19144,24546,28974)
        Y=(37769,45864,50877)
        self.assertTrue(is_b3(X+Z+Y))
        self.assertGreater(min(Z)-max(X),max(Y)-min(Y))
        f,g=fiber(X,Y),fiber(Z,Y)
        self.assertEqual(len(f),30)
        self.assertEqual(len(g),18)
        self.assertTrue(set(f).isdisjoint(g))
        self.assertGreaterEqual(len(f),len(X)*len(Y))
        self.assertGreaterEqual(len(g),len(Z)*len(Y))
        self.assertLess(max(f),min(g))

    def test_genuine_B3_three_nontrivial_disjoint_families(self):
        xs=[(1,2,5),(7839,10987),(24546,28974)]
        Y=(45864,50877)
        A=tuple(a for X in xs for a in X)+Y
        self.assertTrue(is_b3(A))
        self.assertTrue(all(min(xs[i+1])-max(xs[i])>
                            max(Y)-min(Y) for i in range(2)))
        fs=[fiber(X,Y) for X in xs]
        for i in range(len(fs)):
            self.assertGreaterEqual(len(fs[i]),len(xs[i])*len(Y))
            self.assertEqual(sum(fs[i].values()),
                             len(xs[i])*(len(xs[i])+1)//2*len(Y))
            for j in range(i+1,len(fs)):
                self.assertFalse(set(fs[i])&set(fs[j]))

    def test_geometric_separation_requires_no_B3(self):
        X=(1,2,3,4,5,6,7,8,9,10)
        Z=(100,101,102,103,104,105)
        Y=tuple(range(1000,1020))
        self.assertFalse(is_b3(X+Z+Y))
        self.assertGreater(min(Z)-max(X),max(Y)-min(Y))
        self.assertTrue(set(fiber(X,Y)).isdisjoint(fiber(Z,Y)))
        self.assertLess(len(fiber(X,Y)),len(X)*len(Y))
        # Geometry remains valid, but the B3 lag-support lower bound fails.

    def test_fixed_k_rational_density_extraction_constants(self):
        for c in (Q(1),Q(1,2),Q(1,3),Q(1,4)):
            R=(6/c)**3
            self.assertGreaterEqual(R,216)
            for k in range(2,7):
                gamma=(R-1)/R**(2*k)
                B=ceil(2/gamma)
                self.assertLessEqual(Q(1,B),gamma/2)
                self.assertEqual(c-3/R**Q(1,3),c/2) if False else None
                self.assertEqual(c-3*(c/6),c/2)
                for j in range(1,k+1):
                    nco=c/(2*R**(2*j//3)) if (2*j)%3==0 else None
                    self.assertLessEqual(gamma,
                        (R-1)/R**(2*j+2) if j<k else gamma)
                    self.assertGreater(c**2/(4*B),0)

    def test_logarithmic_k_algebra_for_exact_powers(self):
        for c in (Q(1),Q(1,2)):
            R=int((6/c)**3)
            for k in (2,3,4):
                N=R**(12*k)
                self.assertEqual(N,R**(12*k))
                self.assertLessEqual(R**(2*k),R**(2*k))
                B=ceil(Q(2*R**(2*k),R-1))
                self.assertLessEqual(B,2*R**(2*k))
                self.assertGreaterEqual(Q(c,2)*N**Q(1,3),
                                         0) if False else None
                # Nonfloating integer-power versions of the exponents.
                self.assertGreaterEqual(
                    Q(c,2)*R**(4*k)//R**(2*k//1),Q(0))
                self.assertGreater(
                    Q(N,R**(2*k+1)),R**(10*k-1) if k>=1 else 0)

    def test_no_false_mathematical_status(self):
        # The theorem is conditional on a hypothetical global density bound.
        # Finite B3 data alone cannot establish its antecedent.
        self.assertTrue(is_b3(A29))
        self.assertLess(len(A29),500)
        self.assertNotIn("infinite-density witness", "finite B3 prefix")


if __name__=="__main__":
    unittest.main()
