"""Exact rational multiples of pi for #504; detects a real catalogue formula error."""

from fractions import Fraction
from itertools import combinations


def regular_polygon_largest_angle_over_pi(N):
    assert N >= 3
    # For vertices indexed a<b<c, the triangle angle coefficients are the
    # three positive cyclic gaps divided by N, by the inscribed-angle theorem.
    biggest = Fraction(0)
    for a, b, c in combinations(range(N), 3):
        gaps = (b - a, c - b, N - (c - a))
        assert sum(gaps) == N and min(gaps) >= 1
        biggest = max(biggest, Fraction(max(gaps), N))
    return biggest


def catalogue_first_branch(N, m):
    assert m >= 2 and 2 ** (m - 1) < N <= 2**m
    boundary = Fraction(2 ** (m - 1)) + Fraction(2) ** (m - 3)
    assert Fraction(N) <= boundary
    return Fraction(1) - Fraction(1, 2 * m - 1)


def _check_test_504_regular_polygon_exact_max_and_small_source_cases():
    for N in range(3, 30):
        assert regular_polygon_largest_angle_over_pi(N) == Fraction(N - 2, N)
    assert regular_polygon_largest_angle_over_pi(3) == Fraction(1, 3)
    assert regular_polygon_largest_angle_over_pi(4) == Fraction(1, 2)
    assert regular_polygon_largest_angle_over_pi(5) == Fraction(3, 5)
    assert regular_polygon_largest_angle_over_pi(6) == Fraction(2, 3)


def _check_test_504_catalogue_both_branches_false_at_small_N():
    # N=3 lies in the SECOND branch at m=2, not the first.
    assert Fraction(3) > Fraction(2) + Fraction(1, 2)
    catalogue_second_at_3 = Fraction(1) - Fraction(1, 2)
    assert catalogue_second_at_3 == Fraction(1, 2)
    assert Fraction(1, 3) < catalogue_second_at_3
    assert catalogue_first_branch(5, 3) == Fraction(4, 5)
    # Alpha_5 <= largest angle of ANY 5-point construction:
    assert regular_polygon_largest_angle_over_pi(5) < catalogue_first_branch(5, 3)
    # The first-hand 1960 source records alpha_5=3/5*pi and alpha_6=2/3*pi.
    assert catalogue_first_branch(5, 3) > Fraction(2, 3)
    # This would make alpha_5 > alpha_6, contrary to monotonicity.


def _check_test_504_source_verified_cases_and_hypothetical_numerator_two():
    source_cases = {
        3: Fraction(1, 3),
        4: Fraction(1, 2),
        5: Fraction(3, 5),
        6: Fraction(2, 3),
        7: Fraction(2, 3),
        8: Fraction(2, 3),
    }
    assert list(source_cases.values()) == sorted(source_cases.values())
    for N, exact_value in source_cases.items():
        assert regular_polygon_largest_angle_over_pi(N) >= exact_value
    # Possible transcription-repair hypothesis only, NOT a proven Sendov formula.
    assert Fraction(1) - Fraction(2, 2 * 2 - 1) == source_cases[3]
    assert Fraction(1) - Fraction(2, 2 * 3 - 1) == source_cases[5]


def _check_test_504_three_point_minimax_elementary_pigeonhole():
    # Triangle angles sum pi, hence largest coefficient >=1/3.
    for denom in range(3, 22):
        for a in range(1, denom):
            for b in range(1, denom - a):
                c = denom - a - b
                if c > 0:
                    assert max(Fraction(a, denom), Fraction(b, denom), Fraction(c, denom)) >= Fraction(1, 3)
    assert max((Fraction(1, 3),) * 3) == Fraction(1, 3)


import unittest


class CompendiumFiniteQA(unittest.TestCase):
    def test_504_regular_polygon_exact_max_and_small_source_cases(self):
        _check_test_504_regular_polygon_exact_max_and_small_source_cases()

    def test_504_catalogue_both_branches_false_at_small_N(self):
        _check_test_504_catalogue_both_branches_false_at_small_N()

    def test_504_source_verified_cases_and_hypothetical_numerator_two(self):
        _check_test_504_source_verified_cases_and_hypothetical_numerator_two()

    def test_504_three_point_minimax_elementary_pigeonhole(self):
        _check_test_504_three_point_minimax_elementary_pigeonhole()
