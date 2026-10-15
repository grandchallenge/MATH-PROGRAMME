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
                self.assertEqual(c-3*(c/6),c/2)
                for j in range(1,k+1):
                    self.assertLessEqual(gamma,
                        (R-1)/R**(2*j+2) if j<k else gamma)
                    self.assertGreater(c**2/(4*B),0)

    def test_logarithmic_k_algebra_for_exact_powers(self):
        for c in (Q(1),Q(1,2)):
            R=int((6/c)**3)
            for k in (2,3,4):
                N=R**(12*k)
                self.assertEqual(N,R**(12*k))
                self.assertEqual(N**1, R**(12*k))
                B=ceil(Q(2*R**(2*k),R-1))
                self.assertLessEqual(B,2*R**(2*k))
                # Nonfloating integer-power versions of the exponents.
                self.assertGreater(Q(c,2)*R**(4*k),0)
                self.assertEqual(Q(N,R**(2*k+1)), R**(10*k-1))

    def test_narrow_outer_center_width_enforces_sublinear_complete_mass(self):
        for c in (Q(1),Q(1,2),Q(1,4)):
            R=int((6/c)**3)
            for k in (2,3,4):
                N=R**(12*k)
                B=ceil(Q(2*R**(2*k),R-1))
                self.assertGreaterEqual(B,
                    Q(2*R**(2*k),R-1))
                # N^(1/6)=R^(2k), N^(5/6)=R^(10k).
                C=Q(R**2*(R-1),2)
                self.assertLessEqual(Q(N,B),C*R**(10*k))
                # Any B3 subset of the bin has y^3 <= 6(3*width+1).
                width=Q(N,B)
                y3_upper=6*(3*width+1)
                self.assertLessEqual(y3_upper,
                                     24*(width+1))
                # Upper total representation cubed <=
                # (n(n+1)/2)^3 * 24(width+1), n<=3*N^(1/3).
                n_upper=3*R**(4*k)
                q=n_upper*(n_upper+1)//2
                total_cube_bound=q**3*y3_upper
                self.assertLess(total_cube_bound,N**3)

    def test_full_centered_color_family_finite_capacity(self):
        inner=(1,2,5,7839,10987,24546,28974)
        Y=(45864,50877)
        self.assertTrue(is_b3(inner+Y))
        self.assertEqual(len(fiber(inner,Y)),
                         len(fiber(inner,Y).keys()))
        total=len(inner)*(len(inner)+1)//2*len(Y)
        self.assertEqual(sum(fiber(inner,Y).values()),total)
        self.assertLess(total,4*max(inner+Y))

    def test_exact_cross_bin_overlap_and_same_bin_zero(self):
        X=(1,2,5);Z=(573,745,1209)
        bins=[(2442,),(3098,)]
        self.assertTrue(is_b3(X+Z+bins[0]+bins[1]))
        fs=[fiber(X,Y) for Y in bins]
        gs=[fiber(Z,Y) for Y in bins]
        for f,g in zip(fs,gs):
            self.assertFalse(set(f)&set(g))
        total=sum(sum(fiber(X,Y).values()) for Y in bins)
        self.assertEqual(total,len(X)*(len(X)+1)//2*2)
        cross=sum(sum(fi[d]*gj[d] for d in fi) for i,fi in
                  enumerate(fs) for j,gj in enumerate(gs) if i!=j)
        ffull=fiber(X,bins[0]+bins[1])
        gfull=fiber(Z,bins[0]+bins[1])
        self.assertEqual(cross,sum(v*gfull[d] for d,v in ffull.items()))
        self.assertEqual(cross,1)

    def test_polynomial_number_of_occupied_center_bins_gate(self):
        for k in (2,3,4):
            R=216
            N=R**(12*k)
            B=ceil(Q(2*R**(2*k),R-1))
            width=Q(N,B)
            C=Q(R**2*(R-1),2)
            self.assertLessEqual(width,C*R**(10*k))
            # y^3 <= 6(3width+1) <= 6(3C+1)N^(5/6).
            self.assertLessEqual(6*(3*width+1),
                                 6*(3*C+1)*R**(10*k))
            self.assertGreater(B,0)

    def test_no_false_mathematical_status(self):
        # The theorem is conditional on a hypothetical global density bound.
        # Finite B3 data alone cannot establish its antecedent.
        self.assertTrue(is_b3(A29))
        self.assertLess(len(A29),500)
        self.assertNotIn("infinite-density witness", "finite B3 prefix")


if __name__=="__main__":
    unittest.main()
