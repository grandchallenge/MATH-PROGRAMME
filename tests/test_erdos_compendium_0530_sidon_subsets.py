"""Exact finite Sidon certificates for open Erdős #530.

Including doubled elements in unordered pair sums is mandatory.
Neither finite enumeration nor cube-root maximality proves ell(N)~sqrt N.
"""
from fractions import Fraction as F
from itertools import combinations


def sidon_pair_sums(S):
    sums = [a+b for i,a in enumerate(S) for b in S[i:]]
    return len(sums) == len(set(sums))


def sidon_positive_differences(S):
    ordered = sorted(S)
    diffs = [ordered[j]-ordered[i]
             for i in range(len(ordered)) for j in range(i+1,len(ordered))]
    return len(diffs) == len(set(diffs))


def sidon_max(A):
    A = tuple(A)
    for r in range(len(A),-1,-1):
        for S in combinations(A,r):
            if sidon_pair_sums(S):
                return r,S
    raise AssertionError("empty set is Sidon")


def _check_test_530_double_sums_and_affine_invariance():
    examples = [(1,2,3),(1,2,4),(0,1,3,7),(-3,0,3,5),
                (F(1,2),F(2,3),F(5,4),F(8,7))]
    assert not sidon_pair_sums((1,2,3))
    assert sidon_pair_sums((1,2,4))
    for A in examples:
        for k in range(len(A)+1):
            for S in combinations(A,k):
                direct = sidon_pair_sums(S)
                assert direct == sidon_positive_differences(S)
                for scale, shift in ((F(3),F(5)),(F(-2,3),F(7,4))):
                    T = tuple(scale*x+shift for x in S)
                    assert sidon_pair_sums(T) == direct


def _check_test_530_small_intervals_exact_maxima():
    values = []
    for N in range(1,12):
        m,w = sidon_max(range(1,N+1))
        assert sidon_pair_sums(w)
        assert len(w) == m
        assert all(not sidon_pair_sums(S)
                   for S in combinations(range(1,N+1),m+1))
        values.append(m)
    assert values == [1,2,2,3,3,3,4,4,4,4,4]


def _check_test_530_every_maximal_sidon_obstructs_extension():
    for A in ((1,2,3,4,5,6),(-5,-2,0,1,4,8),(0,3,4,7,12,18)):
        m,S=sidon_max(A)
        triple={a+b-c for a in S for b in S for c in S}
        half={(a+b)/2 for a in S for b in S}
        assert all(x in triple or x in half for x in A if x not in S)
        assert len(A) <= m + m**3 + m**2
    # General argument: a maximal-by-inclusion Sidon set has size m,
    # every outside x creates x+s=a+b or 2x=a+b.
    # This yields N<=m+m^3+m^2 and only a cube-root guarantee.


def _check_test_530_exact_pair_counting_with_repetition():
    for m in range(1,20):
        S=tuple(2**k for k in range(m))
        assert sidon_pair_sums(S)  # Powers of two are Sidon (also doubles).
        sums={a+b for i,a in enumerate(S) for b in S[i:]}
        assert len(sums)==m*(m+1)//2


import unittest


class CompendiumFiniteQA(unittest.TestCase):
    def test_530_double_sums_and_affine_invariance(self):
        _check_test_530_double_sums_and_affine_invariance()

    def test_530_small_intervals_exact_maxima(self):
        _check_test_530_small_intervals_exact_maxima()

    def test_530_every_maximal_sidon_obstructs_extension(self):
        _check_test_530_every_maximal_sidon_obstructs_extension()

    def test_530_exact_pair_counting_with_repetition(self):
        _check_test_530_exact_pair_counting_with_repetition()
