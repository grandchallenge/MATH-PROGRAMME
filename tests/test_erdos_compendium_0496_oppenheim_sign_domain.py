"""Exact sign and zero-triple interfaces; NOT an Oppenheim proof."""

from fractions import Fraction
from itertools import product


def quadratic(alpha: Fraction, x: int, y: int, z: int) -> Fraction:
    return x * x + y * y - alpha * z * z


def _check_test_496_negative_alpha_positive_triples_strict_lower_bound():
    for alpha in (Fraction(-1, 3), Fraction(-2), Fraction(-7, 5)):
        for x, y, z in product(range(1, 13), repeat=3):
            value = quadratic(alpha, x, y, z)
            assert value >= 2 + abs(alpha)
            assert abs(value) >= 2 + abs(alpha) > Fraction(1)


def _check_test_496_positive_alpha_gives_indefinite_real_form():
    for alpha in (Fraction(1, 13), Fraction(1), Fraction(5, 3), Fraction(100)):
        assert quadratic(alpha, 1, 0, 0) == 1
        assert quadratic(alpha, 0, 0, 1) == -alpha < 0
        assert quadratic(alpha, 0, 0, 0) == 0
        # Those sign examples are NOT positive-coordinate witnesses.


def _check_test_496_all_zero_triple_is_spurious_witness():
    for alpha in (Fraction(-3, 2), Fraction(-1, 10), Fraction(2, 7), Fraction(13)):
        assert quadratic(alpha, 0, 0, 0) == 0
    # Do not let (0,0,0) satisfy a claimed nontrivial integer theorem.


def _check_test_496_even_under_independent_coordinate_reflections():
    for alpha in (Fraction(-3, 2), Fraction(2, 7), Fraction(13)):
        for x, y, z in product(range(1, 6), repeat=3):
            q = quadratic(alpha, x, y, z)
            for sx, sy, sz in product((-1, 1), repeat=3):
                assert quadratic(alpha, sx * x, sy * y, sz * z) == q
    # Reflection can make a witness positive ONLY if all original coordinates nonzero.


import unittest


class CompendiumFiniteQA(unittest.TestCase):
    def test_496_negative_alpha_positive_triples_strict_lower_bound(self):
        _check_test_496_negative_alpha_positive_triples_strict_lower_bound()

    def test_496_positive_alpha_gives_indefinite_real_form(self):
        _check_test_496_positive_alpha_gives_indefinite_real_form()

    def test_496_all_zero_triple_is_spurious_witness(self):
        _check_test_496_all_zero_triple_is_spurious_witness()

    def test_496_even_under_independent_coordinate_reflections(self):
        _check_test_496_even_under_independent_coordinate_reflections()
