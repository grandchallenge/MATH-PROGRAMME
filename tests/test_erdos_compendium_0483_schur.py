"""Finite original-statement fixtures for Erdős #483 (Schur forcing thresholds).

Finite SAT-like backtracking does not establish any exponential upper bound.
Equal summands a=b are explicitly included. S(k) is the *last* avoidable
length; f(k)=S(k)+1 is the *first* forced length.
"""

from itertools import combinations_with_replacement


def schur_avoiding(colors: list[int]) -> bool:
    """Color of integer n is colors[n-1]."""
    N = len(colors)
    for a in range(1, N + 1):
        for b in range(a, N + 1):
            c = a + b
            if c > N:
                break
            if colors[a - 1] == colors[b - 1] == colors[c - 1]:
                return False
    return True


def canonical_witness(k: int, N: int) -> tuple[list[int] | None, int]:
    """Explore all k-colorings modulo permutations of color names.

    The next color is either previously used or one fresh color.
    Every other fresh color is equivalent to that one by a permutation.
    """
    colors = [-1] * N
    calls = 0

    def search(t: int, n_used: int) -> list[int] | None:
        nonlocal calls
        calls += 1
        if t == N:
            return colors.copy()
        # We are about to assign the integer t+1. Every decomposition
        # a+b=t+1 is included, including a=b.
        forbidden = set()
        for a in range(1, (t + 1) // 2 + 1):
            b = t + 1 - a
            if colors[a - 1] == colors[b - 1] and colors[a - 1] >= 0:
                forbidden.add(colors[a - 1])
        for col in range(min(k, n_used + 1)):
            if col in forbidden:
                continue
            colors[t] = col
            witness = search(t + 1, max(n_used, col + 1))
            if witness is not None:
                return witness
        colors[t] = -1
        return None

    return search(0, 0), calls


def _check_test_483_exact_first_three_schur_thresholds() -> None:
    for k, last_safe, first_forced in ((1, 1, 2), (2, 4, 5), (3, 13, 14)):
        coloring, _ = canonical_witness(k, last_safe)
        assert coloring is not None and schur_avoiding(coloring)
        impossible, _ = canonical_witness(k, first_forced)
        assert impossible is None


def _check_test_483_reproduce_explicit_colorings_and_dfs_coverage() -> None:
    safe2 = [0, 1, 1, 0]
    safe3 = [0, 1, 1, 0, 2, 2, 0, 2, 2, 0, 1, 1, 0]
    assert schur_avoiding(safe2) and schur_avoiding(safe3)
    assert canonical_witness(2, 5) == (None, 6)
    assert canonical_witness(3, 14) == (None, 327)
    assert canonical_witness(3, 13)[0] == safe3


def _check_test_483_equal_summands_not_weak_schur() -> None:
    assert schur_avoiding([0])
    assert not schur_avoiding([0, 0])  # 1+1=2
    assert schur_avoiding([0, 1])  # one-color forcing threshold is 2
    # Independent brute-force verifier detects a collision in any all-one
    # coloring of [1,2] and in all two-colorings of [1,5].
    assert all(
        not schur_avoiding([(mask >> i) & 1 for i in range(5)])
        for mask in range(1 << 5)
    )


def _check_test_483_ramsey_edge_differences_exact_triangle_identity() -> None:
    N = 13
    safe = [0, 1, 1, 0, 2, 2, 0, 2, 2, 0, 1, 1, 0]
    # For each triangle i<j<l on vertex set 0,...,N,
    # edge differences are a=j-i, b=l-j, c=l-i, a+b=c.
    for i in range(N + 1):
        for j in range(i + 1, N + 1):
            for ell in range(j + 1, N + 1):
                a, b, c = j - i, ell - j, ell - i
                assert a + b == c
                assert not (safe[a - 1] == safe[b - 1] == safe[c - 1])


def _check_test_483_ageron_lower_bound_off_by_one_translation() -> None:
    # S(k+5) >= 380 S(k) + 148 => f(k+5) >= 380 f(k)-231
    for f_k in (2, 5, 14, 45, 161):
        S_k = f_k - 1
        lower_S = 380 * S_k + 148
        lower_f = lower_S + 1
        assert lower_f == 380 * f_k - 231
    assert 380 * 14 - 231 == 5089


import unittest


class CompendiumFiniteQA(unittest.TestCase):
    def test_483_exact_first_three_schur_thresholds(self):
        _check_test_483_exact_first_three_schur_thresholds()

    def test_483_reproduce_explicit_colorings_and_dfs_coverage(self):
        _check_test_483_reproduce_explicit_colorings_and_dfs_coverage()

    def test_483_equal_summands_not_weak_schur(self):
        _check_test_483_equal_summands_not_weak_schur()

    def test_483_ramsey_edge_differences_exact_triangle_identity(self):
        _check_test_483_ramsey_edge_differences_exact_triangle_identity()

    def test_483_ageron_lower_bound_off_by_one_translation(self):
        _check_test_483_ageron_lower_bound_off_by_one_translation()
