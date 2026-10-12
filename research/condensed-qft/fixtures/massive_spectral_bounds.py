#!/usr/bin/env python3
"""Exact rational spectral controls for QFT-COND-001, TK-2/TK-2b.

These finite spectral samples verify formulas, NOT infinite-dimensional proofs.
Run: python3 research/condensed-qft/fixtures/massive_spectral_bounds.py
"""
from fractions import Fraction as Q


def multiplier(squared_momentum: Q, squared_mass: Q) -> Q:
    if squared_momentum < 0 or squared_mass < 0:
        raise ValueError("squared quantities must be nonnegative")
    if squared_momentum + squared_mass == 0:
        raise ZeroDivisionError("massless zero-mode singularity")
    return Q(1) / (squared_momentum + squared_mass)


def check() -> None:
    m2 = Q(4)
    grid = [Q(0), Q(1, 9), Q(1), Q(9)]
    values = [multiplier(q, m2) for q in grid]
    assert values[0] == Q(1, 4)
    assert all(Q(0) < x <= Q(1, 4) for x in values)
    assert values == sorted(values, reverse=True)

    # Fourier annulus epsilon < |p| < 2epsilon yields
    # B_0(f_epsilon, f_epsilon) >= 1/(4epsilon^2) for ||f||_2=1.
    # The continuum proof, not this sample, establishes unboundedness.
    for n in (2, 4, 8, 16):
        epsilon = Q(1, n)
        lower = Q(1) / (4 * epsilon**2)
        assert lower == Q(n * n, 4)

    try:
        multiplier(Q(0), Q(0))
    except ZeroDivisionError:
        pass
    else:
        raise AssertionError("zero-mode pole not detected")

    print("QFT-COND-001 massive/massless spectral controls: PASS")


if __name__ == "__main__":
    check()
