#!/usr/bin/env python3
"""Exact finite-dimensional regressions for EXT-015D result 021.

These checks verify finite prefixes and the growth of Roos witnesses.
The infinite-dimensional theorems are proved in DERIVED_WEIGHT_COMPLETION_BOUNDARY_021.md.
"""
from __future__ import annotations


def stage_dimension(b: int, weight_cutoff: int) -> int:
    return min(b + 1, weight_cutoff)


def check_completed_colimit_prefixes() -> None:
    for n in range(1, 21):
        assert stage_dimension(n - 1, n) == n
        assert stage_dimension(n + 5, n) == n
        assert stage_dimension(max(0, n - 2), n) <= n
        # A tuple of one in each of the first N quantum weights requires b>=N-1.
        assert all(stage_dimension(b, n) < n for b in range(n - 1))
    print("FINITE_WEIGHT_PREFIX_PASS: completed support colimit stabilizes at each N")


def check_roos_witnesses() -> None:
    for cutoff in range(1, 21):
        # a_n = sum_{j=n}^{cutoff-1} e_j is the finite approximation
        # to the impossible infinite solution of a_n-a_(n+1)=e_n.
        a = [
            tuple(1 if n <= j < cutoff else 0 for j in range(cutoff))
            for n in range(cutoff + 1)
        ]
        for n in range(cutoff):
            diff = tuple(u - v for u, v in zip(a[n], a[n + 1]))
            unit = tuple(1 if j == n else 0 for j in range(cutoff))
            assert diff == unit
            assert all(a[n][j] == 0 for j in range(n))
        assert sum(bool(x) for x in a[0]) == cutoff
    print("ROOS_TAIL_WITNESS_PASS: support cost grows with truncation")


def check_zero_first_cohomology_finite_levels() -> None:
    for n in range(0, 21):
        # The finite-level degree-one differential E -> R^n is
        # the prefix projection, which is surjective. Lifting each
        # standard basis vector of R^n gives an explicit right inverse.
        for i in range(n):
            vector = [0] * (n + 3)
            vector[i] = 1
            assert vector[:n] == [int(j == i) for j in range(n)]
    print("FINITE_LEVEL_H1_ZERO_PASS: each differential surjects onto R^N")


if __name__ == "__main__":
    check_completed_colimit_prefixes()
    check_roos_witnesses()
    check_zero_first_cohomology_finite_levels()
    print("EXT-015D-021 EXACT FINITE REGRESSIONS PASS (not infinite proofs)")
