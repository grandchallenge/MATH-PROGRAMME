"""Exact finite source-fidelity checks for Erdős #490 (not the analytic proof)."""

from itertools import combinations
from math import isqrt


def injective_products(A: tuple[int, ...], B: tuple[int, ...]) -> bool:
    products = [a * b for a in A for b in B]
    return len(products) == len(set(products))


def unique_by_pairs(A: tuple[int, ...], B: tuple[int, ...]) -> bool:
    pairs = [(a, b) for a in A for b in B]
    return all(
        a * b != c * d
        for i, (a, b) in enumerate(pairs)
        for c, d in pairs[i + 1:]
    )


def is_prime(p: int) -> bool:
    return p >= 2 and all(p % d != 0 for d in range(2, isqrt(p) + 1))


def large_prime_construction(N: int) -> tuple[tuple[int, ...], tuple[int, ...]]:
    return (
        tuple(range(1, N // 2 + 1)),
        tuple(p for p in range(N // 2 + 1, N + 1) if is_prime(p)),
    )


def _check_test_490_cartesian_product_collision_and_correct_witness():
    assert not injective_products((2, 3), (4, 6))
    assert not injective_products((2, 3), (2, 3))
    assert injective_products((1, 2, 3), (5,))
    assert injective_products((), (1, 2, 3))
    assert not unique_by_pairs((2, 3), (4, 6))


def _check_test_490_large_prime_witness_to_three_hundred():
    for N in range(2, 301):
        A, B = large_prime_construction(N)
        assert all(1 <= x <= N for x in A + B)
        assert injective_products(A, B), N


def _check_test_490_exhaustive_small_cartesian_pairs_and_exact_maximum():
    for N in range(1, 9):
        subsets = [
            tuple(x for x in range(1, N + 1) if mask & (1 << (x - 1)))
            for mask in range(1 << N)
        ]
        maximum_fast = 0
        maximum_independent = 0
        for A in subsets:
            for B in subsets:
                first = injective_products(A, B)
                assert first == unique_by_pairs(A, B), (N, A, B)
                if first:
                    maximum_fast = max(maximum_fast, len(A) * len(B))
                    maximum_independent = max(maximum_independent, len(set(a * b for a in A for b in B)))
        assert maximum_fast == maximum_independent
        assert N <= maximum_fast <= N * N


def _check_test_490_cardinality_cannot_ignore_collisions():
    # These elements are individually distinct, but ordered cross-products are not.
    A, B = (2, 3, 4), (3, 4, 6)
    products = [a * b for a in A for b in B]
    assert len(products) == 9
    assert len(set(products)) < 9


import unittest


class CompendiumFiniteQA(unittest.TestCase):
    def test_490_cartesian_product_collision_and_correct_witness(self):
        _check_test_490_cartesian_product_collision_and_correct_witness()

    def test_490_large_prime_witness_to_three_hundred(self):
        _check_test_490_large_prime_witness_to_three_hundred()

    def test_490_exhaustive_small_cartesian_pairs_and_exact_maximum(self):
        _check_test_490_exhaustive_small_cartesian_pairs_and_exact_maximum()

    def test_490_cardinality_cannot_ignore_collisions(self):
        _check_test_490_cardinality_cannot_ignore_collisions()
