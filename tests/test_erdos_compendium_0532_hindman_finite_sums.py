"""Exact bounded source semantics for Erdős #532 (Hindman's theorem).

No finite enumeration establishes Hindman's infinitary theorem, and
source-reported Lean results are not GCL kernel certification.
"""
from itertools import combinations, product


def all_finite_sums(generators):
    return {
        sum(sub)
        for size in range(1, len(generators)+1)
        for sub in combinations(generators, size)
    }


def recursive_finite_sums(generators):
    sums=set()
    for a in generators:
        assert a>0
        sums |= {a} | {a+s for s in sums}
    return sums


def monochromatic(colouring, sums):
    return len({colouring[x] for x in sums})==1


def _check_test_532_two_independent_nonempty_finite_sums_implementations():
    for size in range(1,7):
        for generators in combinations(range(1,10), size):
            direct=all_finite_sums(generators)
            recursive=recursive_finite_sums(generators)
            assert direct==recursive
            assert all(x>0 for x in direct)
            assert len(direct)<=2**size-1


def _check_test_532_distinct_subset_sums_versus_colliding_subset_sums():
    for m in range(1,13):
        A=tuple(2**j for j in range(m))
        sums=recursive_finite_sums(A)
        assert len(sums)==2**m-1
        assert sums==set(range(1,2**m))
    assert recursive_finite_sums((1,2,3))=={1,2,3,4,5,6}
    assert len(recursive_finite_sums((1,2,3)))==6


def _check_test_532_finite_folkman_shadow_F2_equals_nine():
    # This is a finite consequence of Hindman, already checked separately
    # under #531; it does not prove the infinite theorem.
    families=[
        (a,b,{a,b,a+b})
        for a,b in combinations(range(1,10),2)
        if a+b<=9
    ]
    assert len(families)==16
    for bits in range(2**9):
        c={x:(bits>>(x-1))&1 for x in range(1,10)}
        assert any(monochromatic(c, sums) for _,_,sums in families)
    witness8=116
    c8={x:(witness8>>(x-1))&1 for x in range(1,9)}
    assert all(not monochromatic(c8,{a,b,a+b})
               for a,b in combinations(range(1,9),2) if a+b<=8)


def _check_test_532_all_finite_subset_sizes_have_same_colour_in_predicate():
    A=(2,5,11)
    sums=recursive_finite_sums(A)
    assert len(sums)==7
    c={n:0 for n in sums}
    assert monochromatic(c,sums)
    c[A[0]]=1
    assert not monochromatic(c,sums)
    # Merely monochromatic sums of each FIXED cardinality may permit
    # different colours for different cardinalities. That weaker property
    # is not the registered question.
    B=(1,2,4)
    by_size=[{sum(sub) for sub in combinations(B,j)} for j in (1,2,3)]
    assert set.union(*by_size)==all_finite_sums(B)
    assert {len(x) for x in by_size}=={1,3}


import unittest


class CompendiumFiniteQA(unittest.TestCase):
    def test_532_two_independent_nonempty_finite_sums_implementations(self):
        _check_test_532_two_independent_nonempty_finite_sums_implementations()

    def test_532_distinct_subset_sums_versus_colliding_subset_sums(self):
        _check_test_532_distinct_subset_sums_versus_colliding_subset_sums()

    def test_532_finite_folkman_shadow_F2_equals_nine(self):
        _check_test_532_finite_folkman_shadow_F2_equals_nine()

    def test_532_all_finite_subset_sizes_have_same_colour_in_predicate(self):
        _check_test_532_all_finite_subset_sizes_have_same_colour_in_predicate()
