"""Exact finite-sieve gap-moment fixtures; #489 general case remains open."""

from fractions import Fraction
from itertools import combinations
from math import lcm


def periodic_residues(moduli: tuple[int, ...]) -> tuple[int, list[int]]:
    assert all(a >= 2 for a in moduli)
    period = lcm(*moduli) if moduli else 1
    residues = [
        r for r in range(1, period + 1)
        if all(r % a != 0 for a in moduli)
    ]
    assert residues and residues[0] == 1
    return period, residues


def cyclic_gaps(period: int, residues: list[int]) -> list[int]:
    gaps = [v - u for u, v in zip(residues, residues[1:])]
    gaps.append(period + residues[0] - residues[-1])
    assert sum(gaps) == period
    return gaps


def predicted_limit(moduli: tuple[int, ...]) -> Fraction:
    period, residues = periodic_residues(moduli)
    return Fraction(sum(g * g for g in cyclic_gaps(period, residues)), period)


def exact_gap_square_sum(moduli: tuple[int, ...], x: int) -> int:
    # Need the very next survivor even when it lies beyond the cutoff.
    period, residues = periodic_residues(moduli)
    survivors = [
        k * period + r
        for k in range((x // period) + 3)
        for r in residues
    ]
    return sum(
        (v - u) ** 2
        for u, v in zip(survivors, survivors[1:])
        if u < x
    )


def test_489_exact_small_examples():
    assert predicted_limit(()) == 1
    assert predicted_limit((2,)) == 2
    assert predicted_limit((2, 3)) == Fraction(10, 3)
    period, residues = periodic_residues((2, 3))
    assert (period, residues, cyclic_gaps(period, residues)) == (6, [1, 5], [4, 2])
    # The term starting at 5 is included for x=6, although its endpoint is 7.
    assert exact_gap_square_sum((2, 3), 6) == 20
    assert exact_gap_square_sum((2, 3), 5) == 16


def test_489_sieve_periodicity_exact_shift():
    for n in range(0, 6):
        for moduli in combinations(range(2, 7), n):
            period, residues = periodic_residues(moduli)
            block_energy = sum(g * g for g in cyclic_gaps(period, residues))
            for x in (2, 3, 6, period, period + 1, 2 * period + 5):
                assert (
                    exact_gap_square_sum(moduli, x + period)
                    - exact_gap_square_sum(moduli, x)
                ) == block_energy


def test_489_uniform_periodic_error_bounded_by_one_block():
    for mask in range(1 << 6):
        moduli = tuple(a for i, a in enumerate(range(2, 8)) if mask & (1 << i))
        period, residues = periodic_residues(moduli)
        energy = sum(g * g for g in cyclic_gaps(period, residues))
        limit = Fraction(energy, period)
        for x in (2, 3, 7, 21, period + 1, 2 * period + 3):
            actual = exact_gap_square_sum(moduli, x)
            assert abs(Fraction(actual) - limit * x) <= 2 * energy


def test_489_squarefree_is_not_finite_periodicity():
    # The first prime-square exclusion prefixes are strictly increasing,
    # so this test may NOT be used to infer a bound independent of the cutoff.
    assert predicted_limit((4,)) == Fraction(3, 2)
    assert predicted_limit((4, 9)) != predicted_limit((4,))
    assert predicted_limit((4, 9, 25)) != predicted_limit((4, 9))
