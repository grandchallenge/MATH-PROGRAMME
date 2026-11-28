"""Erdős #482: exact Graham–Pollak binary-digit and closed-form fixtures.

The finite arithmetic does not replace Graham–Pollak's infinite closed-form
proof or certify the external Stoll/Lean generalizations.
"""

from decimal import Decimal, localcontext
from math import isqrt


def recurrence(limit: int) -> list[int]:
    """One-based list; all square-root floors are computed with integers."""
    a = [0, 1]
    for _ in range(1, limit):
        t = 2 * a[-1] + 1
        a.append(isqrt((t * t) // 2))
    return a


def closed_form(n: int) -> int:
    """Original Graham–Pollak closed form for a_1=1, in exact integers."""
    assert n >= 1
    if n == 1:
        return 1
    if n % 2 == 0:
        j = n // 2
        p = 1 << (j - 1)
        return p + isqrt(2 * p * p)
    j = (n - 1) // 2
    p = 1 << (j - 1)
    return (1 << j) + isqrt(2 * p * p)


def binary_digit_from_sqrt2(n: int) -> int:
    """Nth bit of √2 when its integer 1 counts as digit #1."""
    assert n >= 1
    p = 1 << (n - 1)
    return isqrt(2 * p * p) % 2


def _check_test_482_original_sequence_and_digit_convention() -> None:
    a = recurrence(120)
    assert a[1:14] == [1, 2, 3, 4, 6, 9, 13, 19, 27, 38, 54, 77, 109]
    assert [a[2 * n + 1] - 2 * a[2 * n - 1]
            for n in range(1, 9)] == [1, 0, 1, 1, 0, 1, 0, 1]
    # The first bit after the radix point of √2 is 0;
    # d_1 instead includes the leading integer 1.
    assert isqrt(8) % 2 == 0
    assert binary_digit_from_sqrt2(1) == 1


def _check_test_482_closed_form_matches_exact_recurrence() -> None:
    a = recurrence(260)
    for n in range(1, 261):
        assert a[n] == closed_form(n)


def _check_test_482_binary_digits_120_exact_steps() -> None:
    a = recurrence(2 * 120 + 1)
    for n in range(1, 121):
        d = a[2 * n + 1] - 2 * a[2 * n - 1]
        assert d in (0, 1)
        assert d == binary_digit_from_sqrt2(n)
        # A second formula using the extracted leading-digit normalization z=√2/2.
        # a_(2n+1)=2^n + floor(2^n z); a_(2n−1)=2^(n−1)+floor(2^(n−1) z).
        assert a[2*n + 1] == (1 << n) + isqrt(2 * (1 << (n - 1))**2)
        if n > 1:
            assert a[2*n - 1] == (1 << (n - 1)) + isqrt(
                2 * (1 << (n - 2))**2)


def _check_test_482_independent_high_precision_decimal_prefix() -> None:
    """A separate decimal square-root calculation reproduces 100 bits."""
    a = recurrence(2 * 100 + 1)
    with localcontext() as ctx:
        ctx.prec = 320
        rt = Decimal(2).sqrt()
        # Rounding ambiguity is controlled by comparing at 320 and 400 digits.
        with localcontext() as higher:
            higher.prec = 400
            rt_hi = Decimal(2).sqrt()
        for n in range(1, 101):
            p = Decimal(1 << (n - 1))
            lo = int(rt * p)
            hi = int(rt_hi * p)
            assert lo == hi, f"unstable root truncation at n={n}"
            assert lo % 2 == a[2 * n + 1] - 2 * a[2 * n - 1]


def _check_test_482_reconstruction_of_prefix_of_sqrt2_over_two() -> None:
    a = recurrence(161)
    n = 70
    bits = [a[2*k + 1] - 2*a[2*k-1] for k in range(1, n+1)]
    prefix = 0
    for b in bits:
        prefix = 2 * prefix + b
    # The first n bits of sqrt(2)/2 recover floor(2^n * sqrt(2)/2).
    assert prefix == isqrt(2 * (1 << (n - 1))**2)
    assert all(x in (0, 1) for x in bits)


import unittest


class CompendiumFiniteQA(unittest.TestCase):
    def test_482_original_sequence_and_digit_convention(self):
        _check_test_482_original_sequence_and_digit_convention()

    def test_482_closed_form_matches_exact_recurrence(self):
        _check_test_482_closed_form_matches_exact_recurrence()

    def test_482_binary_digits_120_exact_steps(self):
        _check_test_482_binary_digits_120_exact_steps()

    def test_482_independent_high_precision_decimal_prefix(self):
        _check_test_482_independent_high_precision_decimal_prefix()

    def test_482_reconstruction_of_prefix_of_sqrt2_over_two(self):
        _check_test_482_reconstruction_of_prefix_of_sqrt2_over_two()
