"""Finite checks for the B3 short outer-difference reservoir and correlation gate."""
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations_with_replacement as triples
from math import ceil
from random import Random
import unittest

A29=(1,2,5,14,33,72,125,219,376,573,745,1209,1557,2442,
     3098,4048,5298,6704,7839,10987,12332,15465,
     19144,24546,28974,34406,37769,45864,50877)


def is_b3(A):
    s=[sum(x) for x in triples(A,3)]
    return len(s)==len(set(s))


def positive_differences(A):
    return Counter(a-b for a in A for b in A if a>b)


def split_equal_bins(Z, count, lo=None, hi=None):
    assert count>=1
    lo=min(Z) if lo is None else lo
    hi=max(Z) if hi is None else hi
    assert hi>lo
    bins=[[] for _ in range(count)]
    for z in Z:
        assert lo<=z<=hi
        bins[min(count-1, int(Fraction((z-lo)*count,hi-lo)))].append(z)
    return bins


def interbin_positive_differences(bins):
    pairs=[]
    for i,X in enumerate(bins):
        for Y in bins[i+1:]:
            pairs.extend((b-a) for a in X for b in Y)
    return pairs


def pair_sums(X):
    return {a+b for a,b in triples(X,2)}


def centered(X,W):
    return Counter(p-2*z for p in pair_sums(X) for z in W)


class LocalOuterDifferenceTests(unittest.TestCase):
    def test_B3_differences_have_no_duplicate_nonzero_lags(self):
        self.assertTrue(is_b3(A29))
        self.assertEqual(len(positive_differences(A29)),
                         len(A29)*(len(A29)-1)//2)
        self.assertTrue(all(v==1 for v in positive_differences(A29).values()))
        rng=Random(41)
        for n in (3,7,14,20):
            subset=tuple(rng.sample(A29,n))
            self.assertEqual(len(positive_differences(subset)),n*(n-1)//2)

    def test_exact_interbin_support_weight_and_sidon_injection(self):
        Z=A29
        bins=split_equal_bins(Z,100,0,51000)
        m=len(Z)
        maxbin=max(map(len,bins))
        self.assertLessEqual(maxbin,m/2)
        cross=interbin_positive_differences(bins)
        expected=(m*m-sum(len(b)**2 for b in bins))//2
        self.assertEqual(len(cross),expected)
        self.assertEqual(len(set(cross)),expected)
        self.assertGreaterEqual(expected, m*m//4)
        self.assertTrue(all(0<d<=51000 for d in cross))

    def test_translated_interval_cubic_bound(self):
        rng=Random(593)
        for n in (1,2,3,6,11,19,29):
            X=tuple(rng.sample(A29,n))
            D=max(X)-min(X)
            triple_count=n*(n+1)*(n+2)//6
            self.assertLessEqual(triple_count,3*D+1)
            self.assertLessEqual(n**3,18*D+6)
        self.assertTrue(is_b3((19000,19001,19004)))

    def test_exact_correlations_and_local_nonnegative_gate(self):
        self.assertTrue(is_b3(A29))
        for ni,nj in ((2,3),(3,3),(4,5),(7,8)):
            X=A29[:ni];Y=A29[ni:ni+nj];W=A29[ni+nj:]
            if len(W)<2:continue
            Fi=centered(X,W);Fj=centered(Y,W)
            overlap=sum(v*Fj[d] for d,v in Fi.items())
            Pi=pair_sums(X);Pj=pair_sums(Y)
            R=Counter(p-q for p in Pi for q in Pj)
            dif=positive_differences(W)
            total=sum(R[2*h]+R[-2*h] for h in dif)
            self.assertEqual(overlap,total)
            self.assertEqual(R[0],0)
            fine=split_equal_bins(W,100,min(W)-1,max(W)+1)
            short={h for h in interbin_positive_differences(fine)
                   if h<=max(W)-min(W)}
            self.assertEqual(len(short),len(set(short)))
            self.assertLessEqual(
                sum(R[2*h]+R[-2*h] for h in short),overlap)

    def test_non_B3_hostile_differences_repeat(self):
        A=(1,2,3,4,5)
        self.assertFalse(is_b3(A))
        ps=positive_differences(A)
        self.assertGreater(sum(ps.values()),len(ps))
        bins=[[1,2],[3,4,5]]
        dif=interbin_positive_differences(bins)
        self.assertGreater(len(dif),len(set(dif)))

    def test_symbolic_density_constants_are_asymptotically_compatible(self):
        # These are parameter tests, not synthetic infinite B3 witnesses.
        for c in (Fraction(1),Fraction(1,2),Fraction(1,4)):
            R=int((6/c)**3)
            J=R**2
            # N=R^72 ensures N^(1/18)=R^4.
            m_coefficient=Fraction(c,2*J)*R**24
            maxbin_upper=3*R**20
            self.assertLessEqual(2*maxbin_upper,m_coefficient)
            distinct_lower=Fraction(c*c,16*J*J)*R**48
            self.assertGreater(distinct_lower,0)
            self.assertEqual(Fraction(1,J),Fraction(1,R**2))
            self.assertLess(3*R**20,m_coefficient)
            # The exponent gap 1/3 - 5/18 is exactly 1/18.
            self.assertEqual(Fraction(1,3)-Fraction(5,18),Fraction(1,18))


if __name__=="__main__":
    unittest.main()
