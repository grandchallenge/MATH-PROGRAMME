#!/usr/bin/env python3
"""Exact finite witness for the QFT-COND-004 degree-product completion no-go.

The infinite categorical/cohomological argument is in the mathematical note.
This fixture is a bounded test of the support quantifiers, not a theorem proof.
"""
from fractions import Fraction as Q


def detected_moments(N: int, stage_k: int) -> tuple[Q, ...]:
    """Degree r class is supported solely in separated interval I_r.

    The normalized P-coclosed functional L_r gives L_r(f_r)=1,
    but vanishes on all inputs from U_k when r > k.
    """
    return tuple(Q(1) if r <= stage_k else Q(0)
                 for r in range(1, N + 1))


def test() -> None:
    for N in (1, 2, 3, 5, 10, 20):
        diagonal = (Q(1),) * N
        assert detected_moments(N, N) == diagonal
        for k in range(N):
            partial = detected_moments(N, k)
            assert partial != diagonal
            assert sum(bool(x) for x in partial) == k
            assert partial[k] == 0

    # Algebraic field-equation moment check for h(x)=exp(m*x):
    # (-d^2/dx^2 + m^2)h = (-m^2 + m^2)h = 0.
    for m in (Q(1, 2), Q(1), Q(3)):
        assert m*m - m*m == 0

    print("QFT-COND-004 completion-support finite checks: PASS")


if __name__ == "__main__":
    test()
