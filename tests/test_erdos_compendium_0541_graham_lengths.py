"""Exact bounded index-sequence zero-sum length checks for proved #541.

A sequence has n indexed positions; equal residue values are allowed.
No finite search certifies the 2010 theorem for arbitrary modulus.
"""
from itertools import product


def lengths_by_masks(a):
    n=len(a)
    return {
        mask.bit_count()
        for mask in range(1,1<<n)
        if sum(a[i] for i in range(n) if mask&(1<<i))%n==0
    }


def lengths_by_dynamic(a):
    n=len(a)
    state={(0,0)}
    for x in a:
        state |= {((s+x)%n,k+1) for s,k in state}
    return {k for s,k in state if s==0 and k>0}


def prefix_witness(a):
    n=len(a)
    prefix=0
    seen={0:0}
    for j,x in enumerate(a,1):
        prefix=(prefix+x)%n
        if prefix in seen:
            return tuple(range(seen[prefix],j))
        seen[prefix]=j
    raise AssertionError("Davenport prefix-pigeonhole failure")


def _check_test_541_exhaustive_all_moduli_through_six():
    for n in range(1,7):
        for a in product(range(n), repeat=n):
            lengths=lengths_by_masks(a)
            assert lengths==lengths_by_dynamic(a)
            assert lengths  # No vacuous hypothesis.
            if len(lengths)==1:
                assert len(set(a))<=2


def _check_test_541_prefix_zero_sum_certificate():
    for n in range(1,7):
        for a in product(range(n),repeat=n):
            positions=prefix_witness(a)
            assert positions
            assert sum(a[i] for i in positions)%n==0
            assert 1<=len(positions)<=n


def _check_test_541_one_and_two_value_extremizers():
    for n in range(2,22):
        a=(1,)*n
        assert lengths_by_dynamic(a)=={n}
        b=(0,)+(1,)*(n-1)
        assert lengths_by_dynamic(b)=={1}
        assert len(set(b))==2


def _check_test_541_multiset_and_index_semantics():
    a=(1,1,2,2)
    assert len(set(a))==2
    assert lengths_by_masks(a)=={2,3}
    assert lengths_by_masks((0,0,1,1))=={1,2}
    # Two equal values at different indices produce distinct subsets.
    # The original theorem forbids three distinct VALUES only when
    # all zero-sum index subsets have one common length.


import unittest


class CompendiumFiniteQA(unittest.TestCase):
    def test_541_exhaustive_all_moduli_through_six(self):
        _check_test_541_exhaustive_all_moduli_through_six()

    def test_541_prefix_zero_sum_certificate(self):
        _check_test_541_prefix_zero_sum_certificate()

    def test_541_one_and_two_value_extremizers(self):
        _check_test_541_one_and_two_value_extremizers()

    def test_541_multiset_and_index_semantics(self):
        _check_test_541_multiset_and_index_semantics()
