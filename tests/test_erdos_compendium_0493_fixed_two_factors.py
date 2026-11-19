"""Exact integer witnesses for the literal Erdős #493 statement."""


def witness(n: int) -> tuple[int, int]:
    assert n >= 0
    return 2, n + 2


def product_minus_sum(items: tuple[int, ...]) -> int:
    value = 1
    for x in items:
        value *= x
    return value - sum(items)


def _check_test_493_every_nonnegative_target_in_bounded_range():
    for n in range(100_001):
        a = witness(n)
        assert len(a) == 2 and min(a) >= 2
        assert product_minus_sum(a) == n


def _check_test_493_original_quantifier_and_endpoint():
    for n in (0, 1, 2, 10, 123, 100_000, 10**18):
        a1, a2 = witness(n)
        assert a1 == 2
        assert a2 == n + 2
        assert product_minus_sum((a1, a2)) == n
    assert witness(0) == (2, 2)
    assert witness(1) == (2, 3)


def _check_test_493_one_factor_cannot_represent_positive_integer():
    for a in range(2, 301):
        assert product_minus_sum((a,)) == 0
    # A distinctness or bound on a2 independent of n would be a new statement.


import unittest


class CompendiumFiniteQA(unittest.TestCase):
    def test_493_every_nonnegative_target_in_bounded_range(self):
        _check_test_493_every_nonnegative_target_in_bounded_range()

    def test_493_original_quantifier_and_endpoint(self):
        _check_test_493_original_quantifier_and_endpoint()

    def test_493_one_factor_cannot_represent_positive_integer(self):
        _check_test_493_one_factor_cannot_represent_positive_integer()
