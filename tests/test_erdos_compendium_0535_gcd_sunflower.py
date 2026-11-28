"""Exact prime-power-layer/gcd sunflower equivalence for open #535.

Finite enumeration is source/semantic QA, NOT an asymptotic sunflower
estimate, nor a proof of the conjectured exponent.
"""
from itertools import combinations
from math import gcd
from sympy import factorint


def layers(n):
    assert n>=1
    return frozenset((p,j) for p,e in factorint(n).items()
                     for j in range(1,e+1))


def constant_pairwise_gcd(seq):
    return len({gcd(a,b) for a,b in combinations(seq,2)})==1


def sunflower(seq):
    return len({layers(a)&layers(b) for a,b in combinations(seq,2)})==1


def f_direct(N,r):
    bad=[sum(1<<(x-1) for x in seq)
         for seq in combinations(range(1,N+1),r)
         if constant_pairwise_gcd(seq)]
    return max(mask.bit_count() for mask in range(1<<N)
               if not any((mask&constraint)==constraint for constraint in bad))


def f_incremental(N,r):
    all_bad={
        last:[
            frozenset(seq[:-1]) for seq in combinations(range(1,N+1),r)
            if constant_pairwise_gcd(seq) and seq[-1]==last]
        for last in range(1,N+1)
    }
    best=0
    def rec(next_val,picked):
        nonlocal best
        if len(picked)+N-next_val+1<=best:return
        if next_val>N:
            best=max(best,len(picked));return
        if not any(B.issubset(picked) for B in all_bad[next_val]):
            rec(next_val+1,picked|{next_val})
        rec(next_val+1,picked)
    rec(1,frozenset())
    return best


def _check_test_535_prime_power_layer_intersection_equals_gcd():
    for a in range(1,101):
        for b in range(1,101):
            assert layers(a)&layers(b)==layers(gcd(a,b))
    assert layers(1)==frozenset()
    assert (layers(4)&layers(8))!=layers(2)
    assert layers(4)&layers(8)==layers(4)


def _check_test_535_pairwise_equal_gcd_iff_sunflower():
    for N in (8,13,17):
        for r in (3,4):
            for seq in combinations(range(1,N+1),r):
                assert constant_pairwise_gcd(seq)==sunflower(seq)
    assert constant_pairwise_gcd((6,10,14))
    assert not constant_pairwise_gcd((6,10,15))


def _check_test_535_exact_small_extremal_counts_two_algorithms():
    for r, Ns in ((3,(5,6,7,8,9,10,11,12,13)),(4,(6,7,8,9,10))):
        for N in Ns:
            a=f_direct(N,r)
            b=f_incremental(N,r)
            assert a==b
            assert 1<=a<=N
            assert N-(a+1)<N
    # Original Erdős definition was the FIRST size FORCING the
    # configuration. It is one more than modern MAX avoiding size.


def _check_test_535_squarefree_support_does_not_preserve_gcd():
    assert set(factorint(2))==set(factorint(4))==set(factorint(8))
    assert gcd(2,8)==2 and gcd(4,8)==4
    assert layers(2)!=layers(4)!=layers(8)
    # The stronger 1973 Ω-version has extra gcd(a_i/d,d)=1
    # and is not merely the original sunflower statement.


import unittest


class CompendiumFiniteQA(unittest.TestCase):
    def test_535_prime_power_layer_intersection_equals_gcd(self):
        _check_test_535_prime_power_layer_intersection_equals_gcd()

    def test_535_pairwise_equal_gcd_iff_sunflower(self):
        _check_test_535_pairwise_equal_gcd_iff_sunflower()

    def test_535_exact_small_extremal_counts_two_algorithms(self):
        _check_test_535_exact_small_extremal_counts_two_algorithms()

    def test_535_squarefree_support_does_not_preserve_gcd(self):
        _check_test_535_squarefree_support_does_not_preserve_gcd()
