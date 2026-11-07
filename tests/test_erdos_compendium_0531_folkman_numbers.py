"""Exact finite Folkman-number source interface for open Erdős #531.

All subset sums must lie in the coloured interval; distinct generator
values are compulsory. This tests k<=3 locally, not growth of F(k).
"""
from itertools import combinations


def nonempty_subset_sums(A):
    k=len(A)
    return frozenset(
        sum(A[j] for j in range(k) if bits & (1<<j))
        for bits in range(1,1<<k))


def candidates(N,k):
    return tuple(
        (A,nonempty_subset_sums(A))
        for A in combinations(range(1,N+1),k)
        if sum(A)<=N)


def is_monochromatic(bits, values):
    return len({(bits >> (v-1)) & 1 for v in values}) == 1


def avoids_witnesses(bits, families):
    return all(not is_monochromatic(bits,sums) for A,sums in families)


def direct_strict_schur(bits,N):
    for a in range(1,N+1):
        for b in range(a+1,N+1):
            if a+b<=N:
                if ((bits>>(a-1))&1)==((bits>>(b-1))&1)==((bits>>(a+b-1))&1):
                    return (a,b,a+b)
    return None


def _check_test_531_exact_folkman_F1_F2():
    assert candidates(1,1) == (((1,),frozenset({1})),)
    family8 = candidates(8,2)
    family9 = candidates(9,2)
    assert len(family8)==12 and len(family9)==16
    witness8=116
    assert avoids_witnesses(witness8,family8)
    assert direct_strict_schur(witness8,8) is None
    for color in range(1<<8):
        assert avoids_witnesses(color,family8) == (direct_strict_schur(color,8) is None)
    assert all(not avoids_witnesses(color,family9) for color in range(1<<9))
    assert all(direct_strict_schur(color,9) is not None for color in range(1<<9))
    # Monotonicity of the Ramsey property extends F(2)<=9 to all N>=9.
    # 8-colouring witnesses F(2)>8. Thus F(2)=9 exactly.


def _check_test_531_all_finite_sums_stay_inside_interval():
    for N in range(1,13):
        for k in (1,2,3):
            for A,sums in candidates(N,k):
                assert len(A)==k
                assert len(set(A))==k
                assert max(sums)==sum(A)<=N
                assert min(sums)>=1
                assert all(v in range(1,N+1) for v in sums)


def _check_test_531_collision_changes_random_coloring_probability():
    A=(1,2,3)
    sums=nonempty_subset_sums(A)
    assert len(sums)==6 < 2**len(A)-1  # 3=1+2 gives one collision.
    # There are 2^(N-|FS|)*2 colourings monochromatic on FS.
    N=sum(A)
    number=sum(is_monochromatic(color,sums) for color in range(1<<N))
    assert number == 2**(N-len(sums)+1)
    # Probability 2^(1-|FS|), not 2^(2-2^k) when collisions occur.


def _check_test_531_doubling_chains_force_opposite_colours():
    def v2(x):
        return (x & -x).bit_length()-1
    for N in (8,16,32,64):
        colors={n:v2(n)%2 for n in range(1,N+1)}
        for x in range(1,N//2+1):
            assert colors[2*x] == 1-colors[x]
    # Published 2017 coloring randomises by odd-part chains,
    # while ensuring this deterministic parity rule.
    # The rule alone is not asserted to reproduce their full bound.


import unittest


class CompendiumFiniteQA(unittest.TestCase):
    def test_531_exact_folkman_F1_F2(self):
        _check_test_531_exact_folkman_F1_F2()

    def test_531_all_finite_sums_stay_inside_interval(self):
        _check_test_531_all_finite_sums_stay_inside_interval()

    def test_531_collision_changes_random_coloring_probability(self):
        _check_test_531_collision_changes_random_coloring_probability()

    def test_531_doubling_chains_force_opposite_colours(self):
        _check_test_531_doubling_chains_force_opposite_colours()
