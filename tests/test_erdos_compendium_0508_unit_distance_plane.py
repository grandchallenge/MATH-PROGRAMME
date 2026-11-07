"""Finite exact graph restrictions for #508; do NOT certify χ(plane)>=6."""

from fractions import Fraction as F
from itertools import combinations, product


# Quadratic-field coordinate a + b√3 represented by rational pair (a,b).
def add(u, v):
    return (u[0] + v[0], u[1] + v[1])


def neg(u):
    return (-u[0], -u[1])


def mul(u, v):
    return (u[0] * v[0] + 3 * u[1] * v[1],
            u[0] * v[1] + u[1] * v[0])


def coord(a=0, b=0):
    return (F(a), F(b))


def point(x=0, y=0):
    return (coord(x), coord(y))


def distance_squared(a, b):
    dx = add(a[0], neg(b[0]))
    dy = add(a[1], neg(b[1]))
    return add(mul(dx, dx), mul(dy, dy))


def unit_graph(points):
    return frozenset((i, j) for i, j in combinations(range(len(points)), 2)
                     if distance_squared(points[i], points[j]) == coord(1))


def chromatic_number(points):
    edges = unit_graph(points)
    for colors in range(1, len(points) + 1):
        if any(all(assignment[i] != assignment[j] for i, j in edges)
               for assignment in product(range(colors), repeat=len(points))):
            return colors
    raise AssertionError("No coloring")


def _check_test_508_equilateral_triangle_exact_algebraic_coordinates():
    triangle = (
        point(0, 0),
        point(1, 0),
        (coord(F(1, 2)), coord(0, F(1, 2))),
    )
    assert len(unit_graph(triangle)) == 3
    assert {distance_squared(a, b) for a, b in combinations(triangle, 2)} == {coord(1)}
    assert chromatic_number(triangle) == 3


def _check_test_508_unit_square_is_cycle_and_two_colorable():
    square = (point(0, 0), point(1, 0), point(1, 1), point(0, 1))
    assert unit_graph(square) == {(0, 1), (1, 2), (2, 3), (0, 3)}
    assert distance_squared(square[0], square[2]) == coord(2)
    assert chromatic_number(square) == 2


def _check_test_508_finite_inheritance_does_not_prove_global_upper_bound():
    pts = (point(0, 0), point(1, 0), point(2, 0))
    assert unit_graph(pts) == {(0, 1), (1, 2)}
    assert chromatic_number(pts) == 2
    # Every full plane coloring restricts to a valid finite coloring,
    # but a finite coloring cannot be extended to the plane automatically.


def _check_test_508_exact_unit_distance_not_at_most_one():
    pts = (point(0, 0), point(F(1, 2), 0), point(1, 0))
    assert distance_squared(pts[0], pts[1]) == coord(F(1, 4))
    assert unit_graph(pts) == {(0, 2)}
    assert chromatic_number(pts) == 2


import unittest


class CompendiumFiniteQA(unittest.TestCase):
    def test_508_equilateral_triangle_exact_algebraic_coordinates(self):
        _check_test_508_equilateral_triangle_exact_algebraic_coordinates()

    def test_508_unit_square_is_cycle_and_two_colorable(self):
        _check_test_508_unit_square_is_cycle_and_two_colorable()

    def test_508_finite_inheritance_does_not_prove_global_upper_bound(self):
        _check_test_508_finite_inheritance_does_not_prove_global_upper_bound()

    def test_508_exact_unit_distance_not_at_most_one(self):
        _check_test_508_exact_unit_distance_not_at_most_one()
