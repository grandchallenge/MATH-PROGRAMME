"""Exact He–Tang Laurent coefficient identities, not a certified B bound."""
from fractions import Fraction as F


def triangular(n):
    return n * (n + 1) // 2


def coefficient(n, K=2, eps=-1):
    """a_n = eps^[n(n-1)/2] * K^[-n(n+1)/2], all integer n."""
    return F(eps ** triangular(n - 1), K ** triangular(n))


def _check_test_513_triangular_exponents_and_exact_laurent_scaling():
    for eps in (-1, 1):
        for n in range(-20, 21):
            assert coefficient(n, eps=eps) * (2 ** n) == (
                coefficient(n - 1, eps=eps) * (eps ** (n - 1))
            )


def _check_test_513_positive_series_maximum_term_two_ties():
    for m in range(1, 13):
        terms = [abs(coefficient(n)) * 2 ** (m * n) for n in range(0, m + 18)]
        maximum = max(terms)
        assert terms[m-1] == terms[m] == maximum
        assert maximum == 2 ** (m * (m - 1) // 2)
        assert [n for n, t in enumerate(terms) if t == maximum] == [m-1, m]
        # Remaining infinite tail decreases geometrically in consecutive ratios.


def _check_test_513_transcendental_coefficient_root_decay():
    for n in range(1, 15):
        assert abs(coefficient(n)) == F(1, 2 ** triangular(n))
        # |a_n|^(1/n) = 2^[-(n+1)/2] tends to 0.
        assert triangular(n) == n * (n + 1) // 2
    assert coefficient(-1) == -1  # eps=-1, n=-1 gives eps^1 and K^0
    assert coefficient(0) == 1


def _check_test_513_polynomial_exclusion_semantic_guard():
    # For f(z)=z+1, mu(r)=r, M(r)=r+1 for r>=1,
    # so allowing polynomials would give liminf ratio=1.
    for r in (1, 2, 5, 10, 100, 10000):
        assert F(r, r + 1) < 1
    assert F(10000, 10001) > F(99, 100)


import unittest


class CompendiumFiniteQA(unittest.TestCase):
    def test_513_triangular_exponents_and_exact_laurent_scaling(self):
        _check_test_513_triangular_exponents_and_exact_laurent_scaling()

    def test_513_positive_series_maximum_term_two_ties(self):
        _check_test_513_positive_series_maximum_term_two_ties()

    def test_513_transcendental_coefficient_root_decay(self):
        _check_test_513_transcendental_coefficient_root_decay()

    def test_513_polynomial_exclusion_semantic_guard(self):
        _check_test_513_polynomial_exclusion_semantic_guard()
