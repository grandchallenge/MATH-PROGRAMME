"""Erdős #466: exact four-vertex planar fixture and quantifier sanity tests.

A finite witness does not prove asymptotic N(X, delta) -> infinity.
The Graham/Sarkozy exponents require independent primary research.
"""

from collections import Counter
from fractions import Fraction
from itertools import combinations


def test_466_exact_square_disk_and_pairwise_distances() -> None:
    a = Fraction(3, 4)
    points = [(-a, -a), (-a, a), (a, -a), (a, a)]
    radius_sq = Fraction(2)
    assert len(set(points)) == 4
    assert all(x * x + y * y < radius_sq for x, y in points)
    squared_distances = Counter(
        (x1 - x2) ** 2 + (y1 - y2) ** 2
        for (x1, y1), (x2, y2) in combinations(points, 2)
    )
    assert squared_distances == {
        Fraction(9, 4): 4,
        Fraction(9, 2): 2,
    }


def test_466_nearest_integer_exclusion_is_exact() -> None:
    # Side distance 3/2 has nearest-integer gap 1/2.
    side = Fraction(3, 2)
    assert min(side - 1, 2 - side) == Fraction(1, 2)
    # Diagonal 3 sqrt(2)/2 is between 21/10 and 5/2,
    # establishing distance to nearest integer > 1/10
    # using only exact rational comparisons of squares.
    diagonal_squared = Fraction(9, 2)
    assert Fraction(21, 10) ** 2 < diagonal_squared
    assert diagonal_squared < Fraction(5, 2) ** 2
    assert Fraction(1, 10) < Fraction(1, 2)
    # Hence all six pairs satisfy ||distance|| > 1/10.


def test_466_fixed_delta_and_radius_monotonicity_fixture() -> None:
    # The *same* threshold is used for both radii: once a witness
    # fits a disk, it remains a witness in every larger disk.
    a = Fraction(3, 4)
    points = [(-a, -a), (-a, a), (a, -a), (a, a)]
    for radius in [Fraction(2), Fraction(3), Fraction(5), Fraction(101, 10)]:
        assert all(x * x + y * y <= radius * radius for x, y in points)
