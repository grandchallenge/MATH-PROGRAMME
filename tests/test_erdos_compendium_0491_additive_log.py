"""Finite exact arithmetic fixtures for #491; not proof of Wirsing's theorem."""

from fractions import Fraction
from itertools import combinations
from math import gcd


def prime_indicator(p: int, n: int) -> int:
    return int(n % p == 0)


def finite_prime_correction(n: int, weights: dict[int, Fraction]) -> Fraction:
    return sum((weight for p, weight in weights.items() if n % p == 0), Fraction(0))


def _check_test_491_parity_indicator_is_coprime_additive_not_completely_additive():
    for a in range(1, 101):
        for b in range(1, 101):
            if gcd(a, b) == 1:
                assert prime_indicator(2, a * b) == (
                    prime_indicator(2, a) + prime_indicator(2, b)
                )
    assert prime_indicator(2, 4) == 1
    assert 2 * prime_indicator(2, 2) == 2
    assert prime_indicator(2, 4) != 2 * prime_indicator(2, 2)


def _check_test_491_finite_prime_support_coprime_additivity_and_boundedness():
    primes = (2, 3, 5, 7, 11, 13)
    for subset_size in range(4):
        for selected in combinations(primes, subset_size):
            weights = {
                p: Fraction((i + 1) * ((-1) ** i), 3)
                for i, p in enumerate(selected)
            }
            bound = sum(map(abs, weights.values()), Fraction(0))
            for n in range(1, 300):
                remainder = finite_prime_correction(n, weights)
                assert abs(remainder) <= bound
                delta = finite_prime_correction(n + 1, weights) - remainder
                assert abs(delta) <= 2 * bound
            for a in range(1, 40):
                for b in range(1, 40):
                    if gcd(a, b) == 1:
                        assert finite_prime_correction(a * b, weights) == (
                            finite_prime_correction(a, weights)
                            + finite_prime_correction(b, weights)
                        )


def _check_test_491_bounded_error_need_not_be_constant_or_zero():
    weights = {2: Fraction(3, 2)}
    values = [finite_prime_correction(n, weights) for n in range(1, 21)]
    assert set(values) == {Fraction(0), Fraction(3, 2)}
    assert all(abs(values[i + 1] - values[i]) <= Fraction(3, 2) for i in range(19))
    assert values[1] == weights[2] and values[3] == weights[2]
    # A claim that all bounded-difference additive functions equal c*log n
    # EXACTLY is incompatible with this bounded nonzero parity correction.


import unittest


class CompendiumFiniteQA(unittest.TestCase):
    def test_491_parity_indicator_is_coprime_additive_not_completely_additive(self):
        _check_test_491_parity_indicator_is_coprime_additive_not_completely_additive()

    def test_491_finite_prime_support_coprime_additivity_and_boundedness(self):
        _check_test_491_finite_prime_support_coprime_additivity_and_boundedness()

    def test_491_bounded_error_need_not_be_constant_or_zero(self):
        _check_test_491_bounded_error_need_not_be_constant_or_zero()
