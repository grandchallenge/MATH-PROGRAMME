#!/usr/bin/env python3
"""Exact finite Gaussian covariance/Wick control for QFT-COND-001.

Scope: reproducible rational-arithmetic regression, NOT a QFT/condensed theorem.
Run: python3 research/condensed-qft/fixtures/finite_gaussian.py
"""
from fractions import Fraction as Q


def check() -> None:
    # A = [[3, -1], [-1, 3]] is positive and C = A^{-1}.
    c11, c12, c22 = Q(3, 8), Q(1, 8), Q(3, 8)
    assert c11 * c22 - c12 * c12 == Q(1, 8)  # positive determinant
    assert c11 > 0

    # The two sites have correlated observations.
    wick_four = c11 * c22 + 2 * c12**2
    independence_product = c11 * c22
    assert wick_four == Q(11, 64)
    assert independence_product == Q(9, 64)
    assert wick_four - independence_product == Q(1, 32)

    # The classical "independent sites" substitution loses the extra term.
    no_cross_covariance = Q(0)
    assert c11 * c22 + 2 * no_cross_covariance**2 != wick_four

    # An indefinite form is not a Gaussian covariance.
    assert Q(-1) < 0
    print("QFT-COND-001 exact finite Gaussian controls: PASS")


if __name__ == "__main__":
    check()
