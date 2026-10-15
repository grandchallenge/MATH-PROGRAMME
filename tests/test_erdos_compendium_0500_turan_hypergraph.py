"""Exact combinatorial receipts for open Erdős #500; no infinite-n resolution."""

from fractions import Fraction
from itertools import combinations, product
from math import comb


def triple_edge(colors):
    a, b, c = colors
    if len({a, b, c}) == 3:
        return True
    for i in range(3):
        if sorted(colors) == sorted((i, i, (i + 1) % 3)):
            return True
    return False


def cyclic_edges(colors):
    return frozenset(
        t for t in combinations(range(len(colors)), 3)
        if triple_edge(tuple(colors[i] for i in t))
    )


def is_k4_free(n, edges):
    e = set(edges)
    return all(
        sum(tuple(t) in e for t in combinations(four, 3)) <= 3
        for four in combinations(range(n), 4)
    )


def balanced_colors(n):
    return tuple(i % 3 for i in range(n))


def test_500_all_81_color_quadruples_cannot_span_four_edges():
    for colors in product(range(3), repeat=4):
        edges = cyclic_edges(colors)
        assert len(edges) <= 3, (colors, edges)


def test_500_balanced_turan_exact_counts_and_freeness():
    expected = [0, 0, 0, 1, 3, 7, 14, 23, 36, 54]
    for n, count in enumerate(expected):
        e = cyclic_edges(balanced_colors(n))
        assert len(e) == count, n
        assert is_k4_free(n, e)
    for k in range(1, 8):
        n = 3 * k
        e = cyclic_edges(balanced_colors(n))
        assert len(e) == (5 * k**3 - 3 * k**2) // 2
        assert 2 * len(e) == 5 * k**3 - 3 * k**2


def test_500_complete_exhaustive_n4_n5():
    for n, target in ((4, 3), (5, 7)):
        triples = list(combinations(range(n), 3))
        ex = -1
        num_optimal = 0
        for mask in range(1 << len(triples)):
            edges = {t for i, t in enumerate(triples) if mask & (1 << i)}
            if is_k4_free(n, edges):
                if len(edges) > ex:
                    ex, num_optimal = len(edges), 1
                elif len(edges) == ex:
                    num_optimal += 1
        assert ex == target
        assert num_optimal >= 1
        assert ex + 1 == (4 if n == 4 else 8)


def test_500_asymptotic_constant_not_finite_n_bound():
    assert Fraction(3, comb(4, 3)) == Fraction(3, 4)
    assert Fraction(3, 4) > Fraction(5611666, 10_000_000)
    guide = Fraction(2246662543771, 4_000_000_000_000)
    assert guide == Fraction(56166563594275, 100_000_000_000_000)
    assert guide > Fraction(5, 9)
    assert guide > Fraction(5611666, 10_000_000)
    assert guide - Fraction(5611666, 10_000_000) == Fraction(1996143771, 4_000_000_000_000)
