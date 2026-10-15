"""Exact rational circumcircle enumeration for #506; no large-n lower theorem."""

from fractions import Fraction as F
from itertools import combinations
from math import comb


BASE = (
    (F(1), F(0)),
    (F(3, 5), F(4, 5)),
    (F(5, 13), F(12, 13)),
    (F(8, 17), F(15, 17)),
    (F(7, 25), F(24, 25)),
    (F(20, 29), F(21, 29)),
    (F(9, 41), F(40, 41)),
)


def rational_center_circle(n):
    assert 4 <= n <= 15
    m = n - 1
    points = [(F(0), F(0))]
    for i in range(m // 2):
        x, y = BASE[i]
        points.extend(((x, y), (-x, -y)))
    if m % 2:
        points.append((F(0), F(1)))
    assert len(points) == n and len(set(points)) == n
    assert all(x * x + y * y == 1 for x, y in points[1:])
    return tuple(points)


def normalized_circle(a, b, c):
    """Return x²+y²+D*x+E*y+F=0, or None for collinear triples."""
    det = (b[0] - a[0]) * (c[1] - a[1]) - (c[0] - a[0]) * (b[1] - a[1])
    if det == 0:
        return None
    rhs_b = (a[0] * a[0] + a[1] * a[1]) - (b[0] * b[0] + b[1] * b[1])
    rhs_c = (a[0] * a[0] + a[1] * a[1]) - (c[0] * c[0] + c[1] * c[1])
    D = (rhs_b * (c[1] - a[1]) - rhs_c * (b[1] - a[1])) / det
    E = ((b[0] - a[0]) * rhs_c - (c[0] - a[0]) * rhs_b) / det
    C = -(a[0] * a[0] + a[1] * a[1] + D * a[0] + E * a[1])
    return D, E, C


def distinct_circles(points):
    circles = set()
    for t in combinations(points, 3):
        circle = normalized_circle(*t)
        if circle is not None:
            circles.add(circle)
    return circles


def test_506_antipodal_circle_centre_exact_count_multiple_parities():
    for n in range(4, 16):
        pts = rational_center_circle(n)
        circles = distinct_circles(pts)
        expected = 1 + comb(n - 1, 2) - (n - 1) // 2
        assert len(circles) == expected, (n, len(circles), expected)
        assert (F(0), F(0), F(-1)) in circles  # outer unit circle
        # A finite exact construction proves an UPPER bound for min c(n).
    assert len(distinct_circles(rational_center_circle(8))) == 19 < comb(7, 2)
    assert len(distinct_circles(rational_center_circle(5))) == 5


def test_506_collinear_sets_determine_no_circles():
    for n in range(3, 14):
        pts = tuple((F(i), F(0)) for i in range(n))
        assert distinct_circles(pts) == set()
        # They are not all on a circle but violate necessary noncollinearity.


def test_506_antipodal_triples_are_collinear():
    for n in range(4, 15):
        pts = rational_center_circle(n)
        centre = pts[0]
        missing = sum(
            normalized_circle(centre, a, b) is None
            for a, b in combinations(pts[1:], 2)
        )
        assert missing == (n - 1) // 2
        # Generic off-circle point would not lose these antipodal-pair circles.


def test_506_circle_normalization_independent_of_triple_order():
    pts = rational_center_circle(7)
    for a, b, c in combinations(pts, 3):
        expected = normalized_circle(a, b, c)
        assert normalized_circle(c, a, b) == expected
        assert normalized_circle(b, c, a) == expected
        if expected is not None:
            D, E, C = expected
            for x, y in (a, b, c):
                assert x * x + y * y + D * x + E * y + C == 0
