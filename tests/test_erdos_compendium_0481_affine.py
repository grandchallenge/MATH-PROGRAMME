"""Exact finite witnesses and harmonic inequalities for Erdős #481.

Tests concern the proved modern hypothesis a_i >= 1, b_i >= 0, with
sum_i 1/a_i > 1. They do not certify an unrestricted signed-domain
interpretation of Erdős–Graham's 1980 question or a Lean proof.
"""

from fractions import Fraction
from math import prod


def next_generation(rows, a, b):
    assert len(a) == len(b)
    return [(a[i] * x + b[i], word + (i,))
            for x, word in rows for i in range(len(a))]


def generations(a, b, count):
    rows = [(1, ())]
    result = [rows]
    for _ in range(count - 1):
        rows = next_generation(rows, a, b)
        result.append(rows)
    return result


def first_duplicate(rows):
    seen = {}
    for value, word in rows:
        if value in seen:
            return value, seen[value], word
        seen[value] = word
    return None


def reciprocal_sum(rows):
    return sum((Fraction(1, x) for x, _ in rows), Fraction(0))


def _check_test_481_distinct_words_collide_at_third_generation() -> None:
    a, b = [2, 2, 3], [0, 1, 1]
    assert sum((Fraction(1, x) for x in a), Fraction(0)) == Fraction(4, 3)
    rows = generations(a, b, 3)
    assert [x for x, _ in rows[1]] == [2, 3, 4]
    assert [len(s) for s in rows] == [1, 3, 9]
    collision = first_duplicate(rows[2])
    assert collision == (7, (0, 2), (1, 1))
    assert rows[2][2][0] == 7 and rows[2][4][0] == 7


def _check_test_481_identity_is_a_minimum_growth_exception() -> None:
    rows = generations([1, 2], [0, 0], 5)
    assert [min(x for x, _ in r) for r in rows] == [1, 1, 1, 1, 1]
    assert first_duplicate(rows[2]) == (2, (0, 1), (1, 0))
    assert len(rows[2]) == 4


def _check_test_481_nonidentity_minimum_growth_and_harmonic_bound() -> None:
    a, b = [2, 2, 3], [0, 1, 1]
    rows = generations(a, b, 4)
    for k, row in enumerate(rows, 1):
        assert min(x for x, _ in row) >= k
    # Test recurrence only at distinct levels, as required for the
    # proof by contradiction.
    C = sum((Fraction(1, x) for x in a), Fraction(0))
    D = sum((Fraction(y, x * x) for x, y in zip(a, b)), Fraction(0))
    for k in (1, 2):
        S = reciprocal_sum(rows[k - 1])
        T = reciprocal_sum(rows[k])
        assert first_duplicate(rows[k - 1]) is None
        assert T >= (C - D / k) * S
        assert S <= sum((Fraction(1, j) for j in range(1, len(rows[k - 1]) + 1)),
                        Fraction(0))


def _check_test_481_sufficient_not_necessary_reciprocal_threshold() -> None:
    a, b = [2, 3, 6], [0, 1, 1]
    assert sum((Fraction(1, x) for x in a), Fraction(0)) == 1
    rows = generations(a, b, 3)
    assert first_duplicate(rows[-1]) is not None


def _check_test_481_labelled_maps_cannot_be_silently_deduplicated() -> None:
    rows = generations([2, 2], [0, 0], 2)
    assert [x for x, _ in rows[-1]] == [2, 2]
    assert first_duplicate(rows[-1]) == (2, (0,), (1,))
    assert len(rows[-1]) == 2
    assert len({x for x, _ in rows[-1]}) == 1


import unittest


class CompendiumFiniteQA(unittest.TestCase):
    def test_481_distinct_words_collide_at_third_generation(self):
        _check_test_481_distinct_words_collide_at_third_generation()

    def test_481_identity_is_a_minimum_growth_exception(self):
        _check_test_481_identity_is_a_minimum_growth_exception()

    def test_481_nonidentity_minimum_growth_and_harmonic_bound(self):
        _check_test_481_nonidentity_minimum_growth_and_harmonic_bound()

    def test_481_sufficient_not_necessary_reciprocal_threshold(self):
        _check_test_481_sufficient_not_necessary_reciprocal_threshold()

    def test_481_labelled_maps_cannot_be_silently_deduplicated(self):
        _check_test_481_labelled_maps_cannot_be_silently_deduplicated()
