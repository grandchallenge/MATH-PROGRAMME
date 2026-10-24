"""Exact subdivision-map fixtures for #492, not an a.e. distribution proof."""

from fractions import Fraction


def interpolation_for_progression(x: Fraction, step: int) -> Fraction:
    assert step >= 1 and x >= step
    interval_number = x // step
    left = interval_number * step
    return (x - left) / step


def fractional_part(x: Fraction) -> Fraction:
    return x - (x.numerator // x.denominator)


def _check_test_492_arithmetic_progression_fractional_part_exact():
    for d in range(1, 11):
        for numerator in range(d * 6, d * 6 + 400):
            x = Fraction(numerator, 6)
            assert interpolation_for_progression(x, d) == fractional_part(x / d)


def _check_test_492_half_open_boundary_and_ratio_tends_one():
    for d in range(1, 12):
        for k in range(1, 50):
            left = d * k
            assert interpolation_for_progression(Fraction(left), d) == 0
            assert interpolation_for_progression(Fraction(left + d, 1), d) == 0
            assert interpolation_for_progression(Fraction(left) + Fraction(d, 2), d) == Fraction(1, 2)
            assert Fraction((k + 1) * d, k * d) == Fraction(k + 1, k)
    # At x approaching the next boundary, the value approaches one,
    # but AT the boundary the half-open convention resets to zero.


def _check_test_492_rational_slope_is_a_special_failure_not_schmidt_example():
    # For rational alpha/d, n*alpha/d has a finite set of fractional parts,
    # hence is NOT uniformly distributed in the continuum.
    alpha = Fraction(4, 3)
    d = 2
    seen = {interpolation_for_progression(alpha * n, d) for n in range(3, 203)}
    assert seen == {Fraction(0), Fraction(1, 3), Fraction(2, 3)}
    # This countable exceptional family cannot refute an "almost every alpha" claim.


import unittest


class CompendiumFiniteQA(unittest.TestCase):
    def test_492_arithmetic_progression_fractional_part_exact(self):
        _check_test_492_arithmetic_progression_fractional_part_exact()

    def test_492_half_open_boundary_and_ratio_tends_one(self):
        _check_test_492_half_open_boundary_and_ratio_tends_one()

    def test_492_rational_slope_is_a_special_failure_not_schmidt_example(self):
        _check_test_492_rational_slope_is_a_special_failure_not_schmidt_example()
