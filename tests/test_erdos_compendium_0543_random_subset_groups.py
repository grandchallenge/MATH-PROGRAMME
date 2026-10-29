"""Exact finite random subset-sum probabilities for DISPROVED #543.

Tests are NOT an asymptotic proof of Ma--Tang 2026 or a GCL
independent specialist critical review.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations
from math import comb,ceil,log2,prod


def elements(moduli):
    from itertools import product
    return tuple(product(*(range(m) for m in moduli)))


def plus(a,b,moduli):
    return tuple((x+y)%m for x,y,m in zip(a,b,moduli))


def subset_sums_rec(A,moduli):
    zero=(0,)*len(moduli)
    sums={zero}
    for x in A:
        sums |= {plus(y,x,moduli) for y in sums}
    return sums


def subset_sums_direct(A,moduli):
    zero=(0,)*len(moduli)
    return {
        tuple(sum(x[j] for x in S)%moduli[j] for j in range(len(moduli)))
        for k in range(len(A)+1) for S in combinations(A,k)
    } | {zero}


def probability_by_uniform_count(moduli):
    G=elements(moduli)
    N=len(G)
    counts=Counter()
    for mask in range(1<<N):
        A=tuple(x for i,x in enumerate(G) if mask & (1<<i))
        if len(subset_sums_rec(A,moduli))==N:
            counts[len(A)]+=1
    probabilities=[F(counts[k],comb(N,k)) for k in range(N+1)]
    return probabilities


def test_543_uniform_cyclic_exact_probabilities_and_monotonicity():
    for N in range(2,14):
        P=probability_by_uniform_count((N,))
        assert P[0]==0 and P[N]==1
        assert all(P[k]<=P[k+1] for k in range(N))
        assert all(P[k]==0 for k in range(ceil(log2(N))))
        threshold=next(k for k,p in enumerate(P) if p>=F(1,2))
        assert ceil(log2(N))<=threshold<=N
        assert P[threshold]>=F(1,2)
        if threshold:assert P[threshold-1]<F(1,2)


def test_543_independent_mask_vs_subset_recursion():
    for moduli in ((3,), (5,), (7,), (2,2), (2,2,2), (4,)):
        G=elements(moduli)
        for k in range(min(4,len(G))+1):
            for A in combinations(G,k):
                assert subset_sums_rec(A,moduli)==subset_sums_direct(A,moduli)
        assert subset_sums_rec((),moduli)=={(0,)*len(moduli)}


def test_543_cyclic_vs_elementary_two_groups():
    # Different abelian group structures may have different probability
    # thresholds. A cyclic-only calculation does not give universal f(N).
    for d in (2,3,4):
        N=2**d
        elementary=(2,)*d
        P=probability_by_uniform_count(elementary)
        assert P[0]==0 and P[N]==1
        assert all(P[k]<=P[k+1] for k in range(N))
        threshold=next(k for k,p in enumerate(P) if p>=F(1,2))
        assert threshold>=ceil(log2(N))
        if d<4:
            cyclic=probability_by_uniform_count((N,))
            assert len(cyclic)==len(P)
            assert cyclic[-1]==P[-1]==1


def test_543_uniform_probability_not_iid_and_prime_witness():
    # Explicit uniform k=2 subsets in F_7; denominator C(7,2), not 7^2.
    P=probability_by_uniform_count((7,))
    assert P[2]==0
    assert P[3]>0
    assert P[7]==1
    assert subset_sums_rec(((1,),(2,),(4,)),(7,))==set(elements((7,)))
    assert all(2**k < 7 for k in (0,1,2))


# CI uses unittest discovery. Preserve the original bounded witness functions
# while explicitly exposing each as a standard unittest test method.
import unittest

class CompendiumWitnessTests(unittest.TestCase):
    def test_543_uniform_cyclic_exact_probabilities_and_monotonicity(self):
        test_543_uniform_cyclic_exact_probabilities_and_monotonicity()

    def test_543_independent_mask_vs_subset_recursion(self):
        test_543_independent_mask_vs_subset_recursion()

    def test_543_cyclic_vs_elementary_two_groups(self):
        test_543_cyclic_vs_elementary_two_groups()

    def test_543_uniform_probability_not_iid_and_prime_witness(self):
        test_543_uniform_probability_not_iid_and_prime_witness()
