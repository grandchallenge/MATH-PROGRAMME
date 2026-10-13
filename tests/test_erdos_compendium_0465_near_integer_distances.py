"""Exact geometric and asymptotic-interface fixtures for Erdős #465.

The published Sárközy and Konyagin bounds are imported *as statements*,
not tested or certified by finite arithmetic.
"""

from fractions import Fraction
from math import isqrt


def test_465_equidistant_triangle_in_unit_disk() -> None:
    # P1=(1,0), P2=(-1/2,sqrt(3)/2), P3=(-1/2,-sqrt(3)/2).
    # All three squared circumradii equal 1.
    assert Fraction(1, 4) + Fraction(3, 4) == 1
    # Every pairwise squared distance equals 3.
    assert Fraction(9, 4) + Fraction(3, 4) == 3
    assert Fraction(3, 4) * 4 == 3
    # Nearest-integer gap 2-sqrt(3) strictly exceeds delta=1/4:
    assert Fraction(3, 1) < Fraction(7, 4) ** 2


def test_465_pairwise_separation_is_weaker_than_forbidden_distances() -> None:
    # |distance| >= delta does not imply that it avoids *all* integers.
    distance = Fraction(3, 1)
    delta = Fraction(1, 4)
    assert distance >= delta
    assert min(distance - 3, 4 - distance) == 0 < delta


def test_465_sqrt_bound_implies_sublinear_in_exact_finite_examples() -> None:
    # Pure inequality check for arbitrary chosen C=3. No finite test
    # establishes the analytic theorem or the existence of its C_delta.
    C = 3
    for m in (100, 1_000, 10_000, 100_000):
        X = m * m
        upper = C * m
        assert Fraction(upper, X) == Fraction(C, m)
        if m > 100:
            assert upper < X
        assert upper < X * m
