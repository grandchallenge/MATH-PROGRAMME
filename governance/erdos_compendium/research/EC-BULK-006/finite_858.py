#!/usr/bin/env python3
"""Erdos #858: independent exact small-N antichain/rough-tree audit.

No finite experiment verifies the published N->infinity constant.
"""
from __future__ import annotations
from fractions import Fraction
from math import isqrt, log
import json


def spf(n: int) -> int:
    assert n >= 2
    for d in range(2, isqrt(n) + 1):
        if n % d == 0:
            return d
    return n


def forbidden(a: int, b: int) -> bool:
    assert 1 <= a < b
    return b % a == 0 and spf(b // a) > a


def audit(N: int) -> dict:
    assert N >= 1
    parent = {1: 0}
    children = {n: [] for n in range(1, N + 1)}
    for b in range(2, N + 1):
        # Construct independently from the literal divisibility condition.
        parent[b] = max(a for a in range(1, b) if forbidden(a, b))
        children[parent[b]].append(b)

    # Pairwise semantic equivalence: forbidden relation iff tree ancestry.
    for a in range(1, N + 1):
        for b in range(a + 1, N + 1):
            node, ancestor = b, False
            while node > 1:
                node = parent[node]
                if node == a:
                    ancestor = True
                    break
            assert ancestor == forbidden(a, b), (N, a, b)

    # Independent weighted-antichain dynamic program on the rooted tree.
    def opt(n: int) -> Fraction:
        return max(Fraction(1, n), sum((opt(c) for c in children[n]), Fraction()))

    value = opt(1)
    if N <= 15:
        # Brute force ALL 2^N subsets, directly testing the original rule.
        exhaustive = Fraction()
        for mask in range(1 << N):
            members = [n for n in range(1, N + 1) if (mask >> (n - 1)) & 1]
            if any(forbidden(a, b) for i, a in enumerate(members) for b in members[i + 1:]):
                continue
            exhaustive = max(exhaustive, sum((Fraction(1, a) for a in members), Fraction()))
        assert exhaustive == value, (N, exhaustive, value)

    # Every integer strictly above sqrt(N) is admissible: t > a => at > a^2 > N.
    terminal = sum((Fraction(1, n) for n in range(isqrt(N) + 1, N + 1)), Fraction())
    assert value >= terminal
    return {'N': N, 'maximum_exact': str(value), 'maximum_float': float(value),
            'terminal_interval_lower_exact': str(terminal),
            'normalized_float': float(value / log(N)) if N > 1 else None,
            'exhaustive_independent_subset_check': N <= 15}


def main() -> None:
    Ns = [1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 14, 15, 20, 30, 50, 100]
    data = [audit(n) for n in Ns]
    assert {z['N']: z['maximum_exact'] for z in data if z['N'] in (4, 5, 6, 7, 10)} == {
        4: '13/12', 5: '77/60', 6: '77/60', 7: '599/420', 10: '4189/2520'}
    print(json.dumps({'record_type': 'EC_BULK_006_858_FINITE/1',
                      'scope': 'FINITE_CHECK_ONLY_NOT_ASYMPTOTIC_PROOF',
                      'independent_methods': ['all-subsets exhaustive original-pair test for N<=15',
                                              'weighted antichain dynamic programming on rough tree',
                                              'pairwise forbidden-versus-ancestry equivalence'],
                      'values': data}, indent=2))


if __name__ == '__main__':
    main()
