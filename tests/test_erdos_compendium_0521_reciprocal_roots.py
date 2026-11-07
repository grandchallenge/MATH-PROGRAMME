"""Exact finite reciprocal-root audit for #521.

A fixed-degree distribution equality is not an almost-sure statement for
one nested random coefficient sequence.
"""
from collections import Counter
from itertools import product
import sympy as S

X = S.symbols("x")


def poly(signs):
    return S.Poly(sum(a * X**k for k, a in enumerate(signs)), X)


def split_roots(p):
    """Distinct real root counts strictly inside and outside [-1,1]."""
    total = int(p.count_roots(-S.oo, S.oo))
    inclusive = int(p.count_roots(-1, 1))
    at_boundary = int(p.eval(-1) == 0) + int(p.eval(1) == 0)
    return inclusive - at_boundary, total - inclusive, at_boundary


def _check_test_521_reversal_identity_and_exact_real_root_bijection():
    for n in range(1, 7):
        for signs in product((-1, 1), repeat=n+1):
            p, q = poly(signs), poly(signs[::-1])
            assert S.expand(X**n * p.as_expr().subs(X, 1/X) - q.as_expr()) == 0
            inside_p, outside_p, boundary_p = split_roots(p)
            inside_q, outside_q, boundary_q = split_roots(q)
            assert inside_p == outside_q, (n, signs)
            assert outside_p == inside_q, (n, signs)
            assert boundary_p == boundary_q
            assert sum((inside_p, outside_p, boundary_p)) <= n


def _check_test_521_inner_outer_fixed_degree_distributions_match():
    for n in range(1, 7):
        inner_hist = Counter()
        outer_hist = Counter()
        for signs in product((-1, 1), repeat=n+1):
            inner, outer, boundary = split_roots(poly(signs))
            inner_hist[inner] += 1
            outer_hist[outer] += 1
        assert inner_hist == outer_hist
        assert sum(inner_hist.values()) == 2**(n+1)


def _check_test_521_example_roots_have_different_regions():
    p = S.Poly(1+X-X**2, X)
    assert split_roots(p) == (1, 1, 0)
    q = S.Poly(-1+X+X**2, X)
    assert split_roots(q) == (1, 1, 0)


def _check_test_521_reversed_arrays_are_not_nested_prefixes():
    coefficients = (1, -1, 1, -1, -1)
    q_2 = coefficients[:3][::-1]
    q_3 = coefficients[:4][::-1]
    assert q_3[:3] != q_2
    # Therefore reversal laws at individual n do not imply a
    # common-sample-space almost-sure limit as n increases.


import unittest


class CompendiumFiniteQA(unittest.TestCase):
    def test_521_reversal_identity_and_exact_real_root_bijection(self):
        _check_test_521_reversal_identity_and_exact_real_root_bijection()

    def test_521_inner_outer_fixed_degree_distributions_match(self):
        _check_test_521_inner_outer_fixed_degree_distributions_match()

    def test_521_example_roots_have_different_regions(self):
        _check_test_521_example_roots_have_different_regions()

    def test_521_reversed_arrays_are_not_nested_prefixes(self):
        _check_test_521_reversed_arrays_are_not_nested_prefixes()
