"""Exact circle-interval and harmonic sanity checks for solved #526.

Shepp's 1972 infinite-covering probability theorem is NOT proved by
these finite rational-arc tests. Published criterion assumes lengths
in nonincreasing order; the independent placements are exchangeable.
"""
from fractions import Fraction as F
from itertools import permutations


def harmonic(n):
    return sum((F(1,k) for k in range(1,n+1)),F(0))


def circle_interval_segments(start, length):
    assert F(0)<=start<F(1) and F(0)<=length<F(1)
    end=start+length
    if end<=1:
        return [(start,end)] if length else []
    return [(start,F(1)),(F(0),end-1)]


def circle_covered_length(arcs):
    """Exact Lebesgue measure of the finite circle union."""
    pieces=[]
    for start, length in arcs:
        pieces.extend(circle_interval_segments(start,length))
    if not pieces:
        return F(0)
    pieces.sort()
    merged=[]
    for lo,hi in pieces:
        if merged and lo<=merged[-1][1]:
            merged[-1]=(merged[-1][0],max(hi,merged[-1][1]))
        else:
            merged.append((lo,hi))
    return sum((hi-lo for lo,hi in merged),F(0))


def _check_test_526_finite_arc_union_order_does_not_matter():
    arcs=((F(0),F(1,4)),(F(3,4),F(1,2)),(F(1,4),F(1,3)),
          (F(2,3),F(1,12)))
    reference=circle_covered_length(arcs)
    assert reference<=1
    for p in permutations(arcs):
        assert circle_covered_length(p)==reference
    # Permuting PAIRS (length, uniform centre) leaves the union unchanged.
    # Assigning reordered lengths fresh iid uniform centres preserves its law.


def _check_test_526_rational_arc_wraparound_and_pointwise_hit_probability():
    assert circle_covered_length(((F(3,4),F(1,2)),))==F(1,2)
    assert circle_covered_length(((F(0),F(1,2)),(F(1,2),F(1,2))))==1
    lengths=(F(1,2),F(1,3),F(1,4),F(1,5))
    uncovered=F(1)
    for a in lengths:
        uncovered*=1-a
        assert F(0)<uncovered<1
    assert uncovered==F(1,5)  # telescopes product k/(k+1)
    # Infinite product ->0 if the length sum diverges, for each fixed x.
    # The fact that each x is covered a.s. is not full-circle coverage a.s.


def _check_test_526_exact_harmonic_prefix_and_dyadic_block_controls():
    for n in range(1,200):
        assert harmonic(n+1)-harmonic(n)==F(1,n+1)
    for n in (1,2,4,8,16,32,64,128):
        block=harmonic(2*n)-harmonic(n)
        assert F(1,2)<=block<1
    # Integral comparison gives log(n+1)<=H_n<=1+log n,
    # hence Shepp c/n term is bounded between
    # (n+1)^c/n^2 and exp(c)*n^(c-2).
    # Divergence iff c>=1 follows from the p-series test.


def _check_test_526_constant_over_n_threshold_is_borderline():
    for c in (F(1,2),F(1),F(3,2)):
        exponent=c-2
        assert (exponent>=-1)==(c>=1)
    # At c=1, only exact c/n or adequate partial-sum control suffices:
    # ell_n = 1/n - 2/(n log n) eventually yields a convergent
    # n^-1 (log n)^-2 Shepp series despite ell_n~1/n.


import unittest


class CompendiumFiniteQA(unittest.TestCase):
    def test_526_finite_arc_union_order_does_not_matter(self):
        _check_test_526_finite_arc_union_order_does_not_matter()

    def test_526_rational_arc_wraparound_and_pointwise_hit_probability(self):
        _check_test_526_rational_arc_wraparound_and_pointwise_hit_probability()

    def test_526_exact_harmonic_prefix_and_dyadic_block_controls(self):
        _check_test_526_exact_harmonic_prefix_and_dyadic_block_controls()

    def test_526_constant_over_n_threshold_is_borderline(self):
        _check_test_526_constant_over_n_threshold_is_borderline()
