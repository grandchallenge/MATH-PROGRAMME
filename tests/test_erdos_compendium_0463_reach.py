"""Finite falsification hooks for the documentary Erdős #463 reach formulation.

No finite test certifies an eventual or density-one assertion.
"""

from math import isqrt


def least_prime_factor(m: int) -> int:
    for d in range(2, isqrt(m) + 1):
        if m % d == 0:
            return d
    return m


def reach(n: int) -> int:
    """Largest allowed composite shift; a proved O(sqrt(n)) candidate bound."""
    shifts = [0]
    for m in range(n + 1, n + isqrt(n) + 4):
        p = least_prime_factor(m)
        if p < m and m - n < p:
            shifts.append(m - n)
    return max(shifts)


def _check_test_463_exact_reach_examples() -> None:
    assert {n: reach(n) for n in (10, 15, 20, 23, 30, 100, 200)} == {
        10: 0, 15: 1, 20: 1, 23: 2, 30: 0, 100: 0, 200: 9
    }
    assert least_prime_factor(209) == 11
    assert 209 - 11 < 200 < 209


def _check_test_463_search_bound_against_independent_full_enumeration() -> None:
    # Small brute-force oracle is deliberately not restricted by the sqrt bound.
    for n in range(1, 301):
        unrestricted = max(
            [0] + [
                m - n
                for m in range(n + 1, n + 301)
                if (p := least_prime_factor(m)) < m and m - n < p
            ]
        )
        assert reach(n) == unrestricted


def _check_test_463_prime_square_infinite_subsequence_pattern() -> None:
    for q in (2, 3, 5, 7, 11, 13, 17, 31, 61):
        assert least_prime_factor(q) == q
        n, m = q * q - q + 1, q * q
        assert least_prime_factor(m) == q
        assert m - q < n
        assert m - n == q - 1
        assert reach(n) >= q - 1


import unittest


class CompendiumFiniteQA(unittest.TestCase):
    def test_463_exact_reach_examples(self):
        _check_test_463_exact_reach_examples()

    def test_463_search_bound_against_independent_full_enumeration(self):
        _check_test_463_search_bound_against_independent_full_enumeration()

    def test_463_prime_square_infinite_subsequence_pattern(self):
        _check_test_463_prime_square_infinite_subsequence_pattern()
