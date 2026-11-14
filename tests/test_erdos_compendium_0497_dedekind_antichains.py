"""Exact small-n Dedekind counts by two independent finite definitions."""

from math import comb


def antichain(family: tuple[int, ...]) -> bool:
    return all(
        not (a & b == a or a & b == b)
        for i, a in enumerate(family)
        for b in family[i + 1 :]
    )


def upward_closed(family_bits: int, n: int) -> bool:
    members = range(1 << n)
    return all(
        not (family_bits & (1 << a)) or not (a & b == a) or bool(family_bits & (1 << b))
        for a in members
        for b in members
    )


def upward_closure(family: tuple[int, ...], n: int) -> int:
    return sum(
        1 << b
        for b in range(1 << n)
        if any(a & b == a for a in family)
    )


def _check_test_497_two_independent_exact_dedekind_counts():
    for n, expected in enumerate((2, 3, 6, 20, 168)):
        antichains = 0
        upsets = 0
        images = set()
        total_subsets = 1 << n
        for family_bits in range(1 << total_subsets):
            family = tuple(a for a in range(total_subsets) if family_bits & (1 << a))
            if antichain(family):
                antichains += 1
                images.add(upward_closure(family, n))
            if upward_closed(family_bits, n):
                upsets += 1
        assert antichains == upsets == len(images) == expected, n


def _check_test_497_zero_universe_and_empty_antichain_are_distinct():
    assert antichain(())
    assert antichain((0,))
    assert upward_closure((), 0) == 0
    assert upward_closure((0,), 0) == 1
    assert not antichain((0, 1))  # empty subset and a nonempty subset comparable


def _check_test_497_middle_layer_exact_lower_bound():
    for n in range(1, 9):
        middle = tuple(a for a in range(1 << n) if a.bit_count() == n // 2)
        assert len(middle) == comb(n, n // 2)
        assert antichain(middle)
        assert antichain(tuple(middle[i] for i in range(len(middle)) if i % 2 == 0))


import unittest


class CompendiumFiniteQA(unittest.TestCase):
    def test_497_two_independent_exact_dedekind_counts(self):
        _check_test_497_two_independent_exact_dedekind_counts()

    def test_497_zero_universe_and_empty_antichain_are_distinct(self):
        _check_test_497_zero_universe_and_empty_antichain_are_distinct()

    def test_497_middle_layer_exact_lower_bound(self):
        _check_test_497_middle_layer_exact_lower_bound()
