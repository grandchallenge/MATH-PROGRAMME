"""Exact finite verification of density-sensitive mixed-centered identities.

No test treats a finite B3 set as evidence for infinite positive density.
"""
from itertools import combinations_with_replacement as triples
from random import Random
from fractions import Fraction
import unittest

A29=(1,2,5,14,33,72,125,219,376,573,745,1209,1557,2442,
     3098,4048,5298,6704,7839,10987,12332,15465,
     19144,24546,28974,34406,37769,45864,50877)


def is_b3(A):
    sums=[sum(t) for t in triples(A,3)]
    return len(sums)==len(set(sums))


def mixed_data(X,Y):
    A=tuple(X)+tuple(Y)
    color={a:0 for a in X}
    color.update({a:1 for a in Y})
    bylag={}
    count=weight=0
    for a,b in triples(A,2):
        for c in A:
            if color[a]==color[b]==color[c]:continue
            d=a+b-2*c
            count+=1
            w=1 if a==b else 2
            weight+=w
            bylag[d]=bylag.get(d,0)+w
    return count,weight,bylag


class MixedBudgetTests(unittest.TestCase):
    def test_exact_mixed_identities_and_true_matching_support(self):
        self.assertTrue(is_b3(A29))
        rng=Random(41)
        for n in (1,2,3,5,8,12,20,28):
            for _ in range(4):
                A=list(A29);rng.shuffle(A)
                X=tuple(A[:n]);Y=tuple(A[n:])
                if not Y:continue
                x=len(X);y=len(Y);m=x+y
                count,weight,lag=mixed_data(X,Y)
                self.assertEqual(count,x*y*(3*m+2)//2)
                self.assertEqual(weight,3*x*y*m)
                self.assertNotIn(0,lag)
                self.assertTrue(all(w<=m for w in lag.values()))
                self.assertGreaterEqual(len(lag),3*x*y)

    def test_two_separated_blocks_in_genuine_finite_B3(self):
        # This tests the actual mixed identities, not the infinite-density
        # hypothesis that would force their sizes on EVERY large scale.
        N=max(A29)
        R=65
        X=tuple(a for a in A29 if a<=N/R**2)
        Y=tuple(a for a in A29 if a>N/R)
        self.assertTrue(X and Y)
        self.assertLess(max(X)*R,min(Y))
        count,weight,lag=mixed_data(X,Y)
        m=len(X)+len(Y)
        self.assertEqual(weight,3*len(X)*len(Y)*m)
        self.assertEqual(count,len(X)*len(Y)*(3*m+2)//2)
        self.assertGreaterEqual(len(lag),3*len(X)*len(Y))
        self.assertLess(len(lag),4*N)

    def test_density_hypothesis_algebra_parameterized(self):
        # Generic cardinality inequalities used in the conditional theorem.
        # Values here are REAL BOUNDS, not a manufactured B3 sequence.
        for c in (Fraction(1,1),Fraction(1,2),Fraction(1,4)):
            R=(6/c)**3
            self.assertEqual(Fraction(1,1)/(6/c),c/6)
            xcoeff=c**3/36
            ycoeff=c/2
            mcoeff=xcoeff+ycoeff
            self.assertGreaterEqual(Fraction(3,2)*xcoeff*ycoeff*mcoeff,
                                    c**5/96)
            self.assertGreaterEqual(3*xcoeff*ycoeff*mcoeff,c**5/48)
            self.assertEqual(3*xcoeff*ycoeff,c**4/24)
            self.assertGreater(R,1)

    def test_multicut_exact_span_multiplicity(self):
        rng=Random(593)
        for k in (2,3,4,6,9):
            A=list(A29[:18]);rng.shuffle(A)
            blocks=[tuple(A[i::k]) for i in range(k)]
            index={a:i for i,block in enumerate(blocks) for a in block}
            all_A=tuple(a for block in blocks for a in block)
            cut_total=0
            for j in range(k-1):
                for a,b in triples(all_A,2):
                    for c in all_A:
                        sides=(index[a]<=j,index[b]<=j,index[c]<=j)
                        if not(sides[0]==sides[1]==sides[2]):
                            cut_total+=1
            span_total=sum(max(index[a],index[b],index[c])-
                           min(index[a],index[b],index[c])
                           for a,b in triples(all_A,2) for c in all_A)
            self.assertEqual(cut_total,span_total)

    def test_genuine_critical_finite_prefix_has_room_in_global_budget(self):
        A=A29
        X=set(A[:14]);Y=set(A[14:])
        _count,weight,lag=mixed_data(tuple(X),tuple(Y))
        self.assertEqual(weight,18270)
        self.assertEqual(len(lag),9094)
        self.assertEqual(max(lag.values()),6)
        self.assertLessEqual(max(lag.values()),len(A))
        self.assertGreaterEqual(len(lag),3*len(X)*len(Y))
        self.assertLess(len(lag),4*max(A))
        self.assertEqual(sum(lag.values()),weight)

    def test_non_B3_negative_control_keeps_combinatorial_identities(self):
        X=(1,2,3);Y=(10,11,12)
        self.assertFalse(is_b3(X+Y))
        count,weight,_=mixed_data(X,Y)
        x=y=3;m=6
        self.assertEqual(count,x*y*(3*m+2)//2)
        self.assertEqual(weight,3*x*y*m)
        # B3 is essential for matching, and these formal counts alone
        # have no bearing on whether the finite union is realizable.

if __name__=='__main__':
    unittest.main()
