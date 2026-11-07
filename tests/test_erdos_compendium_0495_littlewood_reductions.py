"""Exact rational special-case checks for open Erdős #495."""

from fractions import Fraction
from math import lcm


def nearest_integer_distance(value: Fraction) -> Fraction:
    # floor and ceil both work for negative values.
    floor = value.numerator // value.denominator
    return min(value - floor, (floor + 1) - value)


def product(n: int, alpha: Fraction, beta: Fraction) -> Fraction:
    return n * nearest_integer_distance(n * alpha) * nearest_integer_distance(n * beta)


def _check_test_495_nearest_integer_distance_and_symmetry():
    samples = [Fraction(i, q) for q in range(1, 25) for i in range(-80, 81)]
    for r in samples:
        v = nearest_integer_distance(r)
        assert 0 <= v <= Fraction(1, 2)
        assert v == nearest_integer_distance(-r)
        assert v == nearest_integer_distance(r + 13)


def _check_test_495_rational_coordinate_zero_on_shared_denominator():
    for q in range(1, 30):
        for a in range(-q, q + 1):
            alpha = Fraction(a, q)
            for beta in (Fraction(1, 7), Fraction(2, 9), Fraction(-3, 8)):
                for k in (1, 2, 3, 10):
                    assert product(k * q, alpha, beta) == 0
                    assert product(k * q, beta, alpha) == 0


def _check_test_495_exact_one_coordinate_squeeze_and_common_denominators():
    for q in range(1, 16):
        for r in range(1, 16):
            n = lcm(q, r)
            alpha, beta = Fraction(q - 1, q), Fraction(r - 1, r)
            assert product(n, alpha, beta) == 0
            for step in range(1, 40):
                candidate = product(step, alpha, beta)
                upper = Fraction(step, 2) * nearest_integer_distance(step * alpha)
                assert 0 <= candidate <= upper


import unittest


class CompendiumFiniteQA(unittest.TestCase):
    def test_495_nearest_integer_distance_and_symmetry(self):
        _check_test_495_nearest_integer_distance_and_symmetry()

    def test_495_rational_coordinate_zero_on_shared_denominator(self):
        _check_test_495_rational_coordinate_zero_on_shared_denominator()

    def test_495_exact_one_coordinate_squeeze_and_common_denominators(self):
        _check_test_495_exact_one_coordinate_squeeze_and_common_denominators()
