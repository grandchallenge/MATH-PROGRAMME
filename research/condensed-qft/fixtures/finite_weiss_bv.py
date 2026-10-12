#!/usr/bin/env python3
"""Exact finite checks for QFT-COND-003: not an infinite-dimensional proof."""
from fractions import Fraction as F
from itertools import product

X = (0, 1, 2)
A, B, C = frozenset((0, 1)), frozenset((1, 2)), frozenset((0, 2))


def covered(cover, n):
    return {tuple(t) for u in cover for t in product(u, repeat=n)}


def missing(cover, n):
    return set(product(X, repeat=n)) - covered(cover, n)


def h0_rank(cover, n):
    """H_0 rank of finite-discrete Cech for functions on X^n.

    At each covered tuple the intersection indices form a simplex;
    missing tuples contribute nothing. Higher homology vanishes.
    """
    return len(covered(cover, n))


def bv_obstruction(P):
    """Coefficient of (d Delta + Delta d)(theta_0 theta_1)."""
    return F(P[0][1]) - F(P[1][0])


def check():
    # Ordinary cover is not even 2-Weiss.
    assert missing((A, B), 1) == set()
    assert missing((A, B), 2) == {(0, 2), (2, 0)}
    assert h0_rank((A, B), 2) == 7

    # A 2-Weiss cover need not be 3-Weiss.
    pairs = (A, B, C)
    assert missing(pairs, 2) == set()
    assert len(missing(pairs, 3)) == 6
    assert h0_rank(pairs, 2) == 9
    assert h0_rank(pairs, 3) == 21

    # A genuine Weiss cover of finite X includes all three points.
    weiss = (A, B, C, frozenset(X))
    for n in range(1, 5):
        assert missing(weiss, n) == set()
        assert h0_rank(weiss, n) == 3 ** n

    # Self-adjointness gives anticommution of BV operators.
    P_symmetric = ((F(3), F(-1)), (F(-1), F(3)))
    P_asymmetric = ((F(3), F(1)), (F(-1), F(3)))
    assert bv_obstruction(P_symmetric) == 0
    assert bv_obstruction(P_asymmetric) == 2
    print("QFT-COND-003 finite Weiss/BV exact checks: PASS")


if __name__ == "__main__":
    check()
