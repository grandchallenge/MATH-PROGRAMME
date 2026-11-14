"""Exact finite primes for the elementary n^-2 Heilbronn construction (#507)."""

from fractions import Fraction as F
from itertools import combinations


PRIMES = (3, 5, 7, 11, 13, 17, 19, 23, 29, 31)


def parabola_points(p):
    return tuple((F(i, p) - F(1, 2), F((i * i) % p, p) - F(1, 2))
                 for i in range(p))


def twice_oriented_area(a, b, c):
    return ((b[0] - a[0]) * (c[1] - a[1])
            - (c[0] - a[0]) * (b[1] - a[1]))


def _check_test_507_prime_parabola_rational_area_vandermonde():
    for p in PRIMES:
        pts = parabola_points(p)
        assert len(set(pts)) == p
        assert all(x * x + y * y <= 1 for x, y in pts)
        for i, j, k in combinations(range(p), 3):
            val = twice_oriented_area(pts[i], pts[j], pts[k])
            numerator = val * p * p
            assert numerator.denominator == 1
            assert numerator.numerator % p == ((j - i) * (k - i) * (k - j)) % p
            assert numerator.numerator % p != 0
            assert abs(val) >= F(1, p * p)
            # Area = absolute determinant / 2, not absolute determinant.


def _check_test_507_exact_triangle_area_order_and_no_collinearity():
    for p in PRIMES:
        points = parabola_points(p)
        areas = tuple(abs(twice_oriented_area(*t)) / 2
                      for t in combinations(points, 3))
        assert len(areas) == p * (p - 1) * (p - 2) // 6
        assert min(areas) >= F(1, 2 * p * p)


def _check_test_507_unit_disk_vs_unit_square_and_subset_monotonicity():
    for p in PRIMES:
        pts = parabola_points(p)
        assert all(-F(1, 2) <= a < F(1, 2) and
                   -F(1, 2) <= b < F(1, 2) for a, b in pts)
        full = min(abs(twice_oriented_area(*t)) for t in combinations(pts, 3))
        subset = pts[:max(3, p // 2)]
        small = min(abs(twice_oriented_area(*t)) for t in combinations(subset, 3))
        assert small >= full


import unittest


class CompendiumFiniteQA(unittest.TestCase):
    def test_507_prime_parabola_rational_area_vandermonde(self):
        _check_test_507_prime_parabola_rational_area_vandermonde()

    def test_507_exact_triangle_area_order_and_no_collinearity(self):
        _check_test_507_exact_triangle_area_order_and_no_collinearity()

    def test_507_unit_disk_vs_unit_square_and_subset_monotonicity(self):
        _check_test_507_unit_disk_vs_unit_square_and_subset_monotonicity()
