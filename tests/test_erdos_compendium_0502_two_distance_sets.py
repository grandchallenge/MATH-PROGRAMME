"""Exact squared-distance and polynomial witnesses for two-distance lower construction."""

from itertools import combinations
from math import comb


def weight_two_points(d: int) -> tuple[tuple[int, ...], ...]:
    assert d >= 1
    return tuple(
        tuple(1 if k in pair else 0 for k in range(d + 1))
        for pair in combinations(range(d + 1), 2)
    )


def squared_distance(x: tuple[int, ...], y: tuple[int, ...]) -> int:
    assert len(x) == len(y)
    return sum((a - b) ** 2 for a, b in zip(x, y))


def _check_test_502_exact_two_distances_and_ambient_affine_dimension():
    for d in range(3, 9):
        points = weight_two_points(d)
        assert len(points) == comb(d + 1, 2)
        assert len(set(points)) == len(points)
        assert all(sum(p) == 2 for p in points)
        ds = {
            squared_distance(x, y)
            for x, y in combinations(points, 2)
        }
        assert ds == {2, 4}, (d, ds)
        assert comb(d + 1, 2) <= comb(d + 2, 2)
        assert comb(d + 2, 2) - comb(d + 1, 2) == d + 1


def _check_test_502_polynomial_matrix_positive_scalar_identity():
    for d in range(3, 8):
        points = weight_two_points(d)
        for i, a in enumerate(points):
            for j, b in enumerate(points):
                r2 = squared_distance(a, b)
                value = (2 - r2) * (4 - r2)
                assert value == (8 if i == j else 0), (d, i, j, r2)
        # A diagonal 8I has every eigenvalue positive: r_+ = |A|.


def _check_test_502_small_d_not_valid_as_exact_two_distance_witness():
    for d in (1, 2):
        points = weight_two_points(d)
        ds = {squared_distance(a, b) for a, b in combinations(points, 2)}
        assert ds != {2, 4}
    assert len(weight_two_points(1)) == 1
    assert len(weight_two_points(2)) == 3


import unittest


class CompendiumFiniteQA(unittest.TestCase):
    def test_502_exact_two_distances_and_ambient_affine_dimension(self):
        _check_test_502_exact_two_distances_and_ambient_affine_dimension()

    def test_502_polynomial_matrix_positive_scalar_identity(self):
        _check_test_502_polynomial_matrix_positive_scalar_identity()

    def test_502_small_d_not_valid_as_exact_two_distance_witness(self):
        _check_test_502_small_d_not_valid_as_exact_two_distance_witness()
