"""Exact semantic and sparse-exponent fixtures for proved #516.

No finite polynomial or partial sum can replace the Fuchs 1963 proof.
"""
from fractions import Fraction as F
from math import factorial


def geometric_exponents(k):
    return 2**k


def square_exponents(k):
    return k*k


def reciprocal_gaps(exponent, first, last):
    return sum((F(1, exponent(k+1)-exponent(k))
                for k in range(first, last+1)), F(0))


def _check_test_516_both_families_have_fabry_gaps_but_different_reciprocal_sums():
    for k in range(1, 130):
        if k >= 4:
            assert F(geometric_exponents(k), k) >= k  # eventual 2^k >= k²
        assert F(square_exponents(k), k) == k
        assert geometric_exponents(k+1) > geometric_exponents(k)
        assert square_exponents(k+1) > square_exponents(k)
    for K in (1, 2, 4, 16, 64, 128):
        g = reciprocal_gaps(geometric_exponents, 1, K)
        assert g == 1 - F(1, 2**K)
        assert g < 1  # Sum over all geometric gaps is 1.
        sq = reciprocal_gaps(square_exponents, 1, K)
        lower = sum((F(1, 3*k) for k in range(1, K+1)), F(0))
        assert sq >= lower
        # Diverges as harmonic series, despite n_k/k = k -> infinity.


def _check_test_516_binomial_circle_minimum_maximum_and_maximum_term():
    for q in range(1, 11):
        for r in (F(1, 2), F(3, 4), F(1), F(3, 2), F(2), F(7)):
            rq = r**q
            M = 1 + rq
            m_min = abs(1 - rq)
            mu = max(F(1), rq)
            assert 0 <= m_min <= M
            assert mu <= M
            # Every phase of z^q is attained around the circle,
            # so extrema of |1+z^q| are |1-r^q| and 1+r^q.
            if r == 1:
                assert m_min == 0 and mu == 1 and M == 2
            if r > 1:
                assert M - m_min == 2 and mu == rq
            assert mu != m_min or r == F(1, 2)


def _check_test_516_square_exponent_entire_series_has_finite_order_one():
    for K in range(1, 26):
        terms = [F(K**(k*k), factorial(k*k)) for k in range(1, 12)]
        e_trunc = sum((F(K**n, factorial(n)) for n in range(0, 122)), F(0))
        assert sum(terms, F(0)) <= e_trunc
        # Every selected exponent appears in the ordinary exp series.
        assert all(k*k < 122 for k in range(1, 12))
    # Analytically |f(z)| <= exp(|z|), because all terms are a
    # subset of the Taylor series for exp(|z|).


def _check_test_516_logarithm_zero_and_maximum_term_guard():
    # r=1: min_circle |1+z^q|=0, cannot evaluate ordinary log(min).
    for q in range(1, 20):
        r = F(1)
        assert abs(1-r**q) == 0
        assert max(F(1), r**q) == 1
        assert 1+r**q == 2
        # Ratio log minimum/log maximum is extended-real -infinity,
        # NOT the ratio of log largest term to log maximum.


import unittest


class CompendiumFiniteQA(unittest.TestCase):
    def test_516_both_families_have_fabry_gaps_but_different_reciprocal_sums(self):
        _check_test_516_both_families_have_fabry_gaps_but_different_reciprocal_sums()

    def test_516_binomial_circle_minimum_maximum_and_maximum_term(self):
        _check_test_516_binomial_circle_minimum_maximum_and_maximum_term()

    def test_516_square_exponent_entire_series_has_finite_order_one(self):
        _check_test_516_square_exponent_entire_series_has_finite_order_one()

    def test_516_logarithm_zero_and_maximum_term_guard(self):
        _check_test_516_logarithm_zero_and_maximum_term_guard()
