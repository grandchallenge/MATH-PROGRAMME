#!/usr/bin/env python3
"""Erdos #859: exact small-t divisor-subset density, two independent methods.

For fixed t, membership is periodic modulo lcm(1,...,t). The output does
not address the open t->infinity power-law asymptotic.
"""
from __future__ import annotations
from fractions import Fraction
from math import lcm
import json


def minimal_witnesses(t: int) -> list[int]:
    assert t >= 1
    lcms: set[int] = set()

    def partitions(next_part: int, remaining: int, current_lcm: int) -> None:
        if remaining == 0:
            lcms.add(current_lcm)
            return
        for part in range(next_part, remaining + 1):
            partitions(part + 1, remaining - part, lcm(current_lcm, part))

    partitions(1, t, 1)
    # Keep only minimal witnesses in the divisibility order.
    return sorted(m for m in lcms if not any(d != m and m % d == 0 for d in lcms))


def direct_divisor_subset(n: int, t: int) -> bool:
    # Independent from the witness-generation algorithm.
    reachable = 1
    for d in range(1, t + 1):
        if n % d == 0:
            reachable |= reachable << d
    return bool((reachable >> t) & 1)


def audit(t: int) -> dict:
    period = lcm(*range(1, t + 1))
    witnesses = minimal_witnesses(t)
    count = 0
    for n in range(1, period + 1):
        by_witness = any(n % m == 0 for m in witnesses)
        by_subset = direct_divisor_subset(n, t)
        assert by_witness == by_subset, (t, n, witnesses)
        count += by_witness
    density = Fraction(count, period)
    assert density >= Fraction(1, t)
    return {'t': t, 'period': period, 'minimal_lcm_witnesses': witnesses,
            'favorable_residues': count, 'density_exact': str(density)}


def main() -> None:
    values = [audit(t) for t in range(1, 13)]
    expected = ['1', '1/2', '2/3', '1/2', '7/15', '7/15',
                '16/35', '3/7', '17/45', '2/5', '13/33', '43/99']
    assert [r['density_exact'] for r in values] == expected
    print(json.dumps({'record_type': 'EC_BULK_006_859_FINITE/1',
                      'authority': 'EXACT_FINITE_PERIODICITY_ONLY',
                      'methods': ['independent subset-sum bitset on divisors of each n',
                                  'enumeration of distinct partitions of t and minimal LCM witnesses'],
                      'values': values}, indent=2))


if __name__ == '__main__':
    main()
