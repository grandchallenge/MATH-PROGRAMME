"""Exact finite Borsuk partition/diametral-colouring correspondence (#505)."""

from itertools import combinations, product
from math import ceil


def squared(a, b):
    return sum((x - y) ** 2 for x, y in zip(a, b))


def diametral_edges(points):
    assert len(points) >= 2 and len(points) == len(set(points))
    distances = {(i, j): squared(points[i], points[j])
                 for i, j in combinations(range(len(points)), 2)}
    maximum = max(distances.values())
    assert maximum > 0
    return frozenset(pair for pair, dist in distances.items() if dist == maximum), maximum


def valid_partition_coloring(points, colors):
    edges, diameter2 = diametral_edges(points)
    assert len(colors) == len(points)
    proper = all(colors[i] != colors[j] for i, j in edges)
    # Independent, direct geometric test of all pair distances within same piece.
    geometric = all(
        squared(points[i], points[j]) < diameter2
        for i, j in combinations(range(len(points)), 2)
        if colors[i] == colors[j]
    )
    assert proper == geometric
    return proper


def chromatic_number(points):
    n = len(points)
    for k in range(1, n + 1):
        for labels in product(range(k), repeat=n):
            if len(set(labels)) == k and valid_partition_coloring(points, labels):
                return k
    raise AssertionError("No valid coloring")


def _check_test_505_complete_simplex_in_affine_dimension_d_requires_dplus1():
    for d in range(1, 5):
        # Unit vectors e_i (0<=i<=d) lie in affine plane sum x_i=1, dimension d.
        points = tuple(tuple(int(i == j) for j in range(d + 1)) for i in range(d + 1))
        edges, diameter2 = diametral_edges(points)
        assert diameter2 == 2
        assert len(edges) == (d + 1) * d // 2
        assert chromatic_number(points) == d + 1


def _check_test_505_square_diameter_graph_is_matching_not_complete():
    points = ((0, 0), (1, 0), (0, 1), (1, 1))
    edges, diameter2 = diametral_edges(points)
    assert edges == {(0, 3), (1, 2)}
    assert diameter2 == 2
    assert chromatic_number(points) == 2


def _check_test_505_coloring_vs_strict_diameter_for_every_small_assignment():
    for points in (
        ((0,), (1,)),
        ((0,), (1,), (2,)),
        ((0, 0), (1, 0), (0, 1)),
        ((0, 0), (2, 0), (0, 2), (2, 2)),
        ((0, 0), (3, 0), (0, 4)),
    ):
        for k in range(1, min(len(points), 4) + 1):
            for colors in product(range(k), repeat=len(points)):
                valid_partition_coloring(points, colors)


def _check_test_505_published_and_reported_pigeonhole_bounds():
    assert ceil(352 / 5) == 71 > 64 + 1  # Jenrich-Brouwer 2014
    assert ceil(321 / 5) == 65 > 63 + 1  # Grinsztajn 2026, external claim
    # Arithmetic does NOT verify either high-dimensional Euclidean construction.


import unittest


class CompendiumFiniteQA(unittest.TestCase):
    def test_505_complete_simplex_in_affine_dimension_d_requires_dplus1(self):
        _check_test_505_complete_simplex_in_affine_dimension_d_requires_dplus1()

    def test_505_square_diameter_graph_is_matching_not_complete(self):
        _check_test_505_square_diameter_graph_is_matching_not_complete()

    def test_505_coloring_vs_strict_diameter_for_every_small_assignment(self):
        _check_test_505_coloring_vs_strict_diameter_for_every_small_assignment()

    def test_505_published_and_reported_pigeonhole_bounds(self):
        _check_test_505_published_and_reported_pigeonhole_bounds()
