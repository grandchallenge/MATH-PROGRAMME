#!/usr/bin/env python3
"""QFT-COND-002 exact finite controls for the Hermite/Schwartz liquid tower.

Proof authority remains Clausen--Scholze Theorem 4.11 and Remark 4.12.
Only elementary rational inequalities are replayed here.

Usage: python3 research/condensed-qft/fixtures/hermite_liquid_tower.py
"""
from fractions import Fraction as Q
from math import comb, factorial


def shell_count(d: int, n: int) -> int:
    """Number of nonnegative d-indices with sum n."""
    assert d >= 1 and n >= 0
    return comb(n + d - 1, d - 1)


def weight_sum(d: int, cutoff: int) -> Q:
    """Sum lambda^(1/2) for lambda_n=(1+n)^(-2(d+1))."""
    return sum((Q(shell_count(d, n), (n + 1) ** (d + 1))
                for n in range(cutoff + 1)), Q(0))


def test_shell_bounds() -> None:
    for d in range(1, 7):
        for n in range(0, 35):
            count = shell_count(d, n)
            assert count <= (n + 1) ** (d - 1)

            # Critical case: L=2d, q=1/2 yields the harmonic
            # LOWER bound shell term >= 1/((d-1)! * (n+1)).
            assert Q(count, (n + 1) ** d) >= Q(
                1, factorial(d - 1) * (n + 1)
            )

        for cutoff in (0, 1, 2, 5, 10, 30):
            summation = weight_sum(d, cutoff)
            # For the admissible choice L=2(d+1), q=1/2,
            # shell term <= 1/(n+1)^2.
            harmonic_square = sum(
                (Q(1, (n + 1) ** 2) for n in range(cutoff + 1)), Q(0)
            )
            assert Q(0) < summation <= harmonic_square
            assert harmonic_square <= Q(2) - Q(1, cutoff + 1)


def test_product_tower() -> None:
    # The q-summability of product weights is multiplicative:
    # sum_{nu,mu} (lambda_nu lambda'_mu)^q
    # = (sum_nu lambda_nu^q)(sum_mu lambda'_mu^q).
    for a, b in ((1, 1), (1, 2), (2, 3), (3, 2)):
        for cutoff in (0, 2, 5):
            left = weight_sum(a, cutoff)
            right = weight_sum(b, cutoff)
            double = sum(
                (
                    Q(shell_count(a, n), (n + 1) ** (a + 1))
                    * Q(shell_count(b, k), (k + 1) ** (b + 1))
                    for n in range(cutoff + 1)
                    for k in range(cutoff + 1)
                ), Q(0)
            )
            assert double == left * right
            assert double <= Q(4)

    # Cofinality of polynomial weights on the product index.
    for n in range(0, 20):
        for k in range(0, 20):
            assert 1 + n + k <= (1 + n) * (1 + k)
            assert (1 + n) * (1 + k) <= (1 + n + k) ** 2


def test_invalid_exponent_is_rejected() -> None:
    # The forbidden endpoint exponent L=2d gives harmonic
    # divergence, not summability. A finite sample cannot prove
    # divergence; the explicit lower bound in test_shell_bounds
    # together with the divergent harmonic series is the proof.
    for d in (1, 2, 3, 5):
        partials = []
        for cutoff in (5, 20, 60):
            partials.append(
                sum((Q(shell_count(d, n), (n + 1) ** d)
                     for n in range(cutoff + 1)), Q(0))
            )
        assert partials[0] < partials[1] < partials[2]


def main() -> None:
    test_shell_bounds()
    test_product_tower()
    test_invalid_exponent_is_rejected()
    print("QFT-COND-002 Hermite liquid tower: exact finite controls PASS")


if __name__ == "__main__":
    main()
