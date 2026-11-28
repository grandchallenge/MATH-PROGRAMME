"""Exact finite fixtures for Erdős #464.

The original question is about fractional-part nondensity, not the vacuous
nondensity of nearest-integer distances in [0, 1]. A finite prefix cannot
certify the universal lacunary theorem or replace Pollington/de Mathan.
"""

from fractions import Fraction
from math import isqrt


def square_indicator(j: int) -> int:
    return int(isqrt(j) ** 2 == j)


def binary_digit(position: int) -> int:
    """Position 0 is first fractional binary digit."""
    k, parity = divmod(position, 2)
    s = square_indicator(k)
    return s if parity == 0 else 1 - s


def frac_binary_prefix(start: int, bits: int = 28) -> Fraction:
    return sum(
        (Fraction(binary_digit(start + i), 2 ** (i + 1)) for i in range(bits)),
        Fraction(0),
    )


def _check_test_464_all_paired_digits_are_complements() -> None:
    for j in range(0, 10001):
        assert binary_digit(2 * j) + binary_digit(2 * j + 1) == 1


def _check_test_464_exact_binary_shift_separation() -> None:
    # Every three-bit block includes an opposite-digit designated pair.
    # The infinite mathematical argument is uniform; this tests its fixture.
    for shift in range(0, 10001):
        digits = [binary_digit(shift + j) for j in range(3)]
        assert digits not in ([0, 0, 0], [1, 1, 1])
        # A 28-bit prefix lies strictly within the closed safe interval;
        # the actual untruncated fraction is bounded by the same three bits.
        x = frac_binary_prefix(shift)
        assert Fraction(1, 8) <= x <= Fraction(7, 8)


def _check_test_464_fractional_part_vs_nearest_integer_distance() -> None:
    # Norms are always <=1/2. Thus literal 'not dense in [0,1]'
    # for a set of such norms is vacuous and is not the original claim.
    for k in range(2, 100):
        x = Fraction(7 * k, 11)
        fractional = x - (x.numerator // x.denominator)
        norm = min(fractional, 1 - fractional)
        assert 0 <= norm <= Fraction(1, 2)
    assert all(2 ** (k + 1) >= Fraction(6, 5) * 2 ** k for k in range(20))


import unittest


class CompendiumFiniteQA(unittest.TestCase):
    def test_464_all_paired_digits_are_complements(self):
        _check_test_464_all_paired_digits_are_complements()

    def test_464_exact_binary_shift_separation(self):
        _check_test_464_exact_binary_shift_separation()

    def test_464_fractional_part_vs_nearest_integer_distance(self):
        _check_test_464_fractional_part_vs_nearest_integer_distance()
