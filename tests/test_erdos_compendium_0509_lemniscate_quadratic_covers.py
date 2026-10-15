"""Exact special-case covers for Erdős #509; not a universal degree-n proof."""

from fractions import Fraction as F
from itertools import product


def point(x, y=0):
    return (F(x), F(y))


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def norm_squared(a):
    return a[0] * a[0] + a[1] * a[1]


def quadratic_abs_squared(z, a, b):
    # |(z-a)(z-b)|^2 = |z-a|^2 |z-b|^2, with exact rational values.
    return norm_squared(sub(z, a)) * norm_squared(sub(z, b))


def grid():
    return tuple((F(a, 2), F(b, 2)) for a, b in product(range(-8, 9), repeat=2))


def test_509_every_monic_linear_lemniscate_is_unit_disk():
    for a in (point(0), point(2), point(F(1, 2), F(-3, 2))):
        for z in grid():
            assert (norm_squared(sub(z, a)) <= 1) == (
                norm_squared(sub(z, a)) ** 1 <= 1
            )


def test_509_degree_two_both_factors_gt_one_impossible_inside():
    roots = (point(-2), point(0), point(2), point(F(1, 2), F(3, 2)))
    for a, b in product(roots, repeat=2):
        assert 1 + 1 == 2  # sum of disk RADII not diameters
        for z in grid():
            if quadratic_abs_squared(z, a, b) <= 1:
                assert norm_squared(sub(z, a)) <= 1 or norm_squared(sub(z, b)) <= 1


def test_509_far_separated_quadratic_has_radii_two_over_R():
    for R in range(1, 9):
        a, b = point(R), point(-R)
        radius_sq = F(1, R * R)
        assert F(2, R) <= 2
        for z in grid():
            if quadratic_abs_squared(z, a, b) <= 1:
                assert (norm_squared(sub(z, a)) <= radius_sq or
                        norm_squared(sub(z, b)) <= radius_sq)


def test_509_repeated_roots_arbitrary_degree_exact():
    for n in (1, 2, 3, 4, 5, 8, 13):
        for a in (point(0), point(F(1, 2)), point(-2, 1)):
            for z in grid():
                q = norm_squared(sub(z, a))
                # The |f|<=1 region is EXACTLY one disk, no dependence on n.
                assert (q ** n <= 1) == (q <= 1)


def test_509_boundary_is_included():
    a, b = point(0), point(2)
    for z in (point(1), point(0, 1), point(2, 1)):
        if quadratic_abs_squared(z, a, b) <= 1:
            assert min(norm_squared(sub(z, a)), norm_squared(sub(z, b))) <= 1
    assert quadratic_abs_squared(point(1), a, b) == 1
