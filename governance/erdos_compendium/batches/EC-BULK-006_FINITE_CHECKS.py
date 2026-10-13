#!/usr/bin/env python3
"""Independent finite arithmetic fixtures for EC-BULK-006 #853-855.

Finite checks are not evidence of any asymptotic conjecture.
Run: python3 governance/erdos_compendium/batches/EC-BULK-006_FINITE_CHECKS.py
"""
from __future__ import annotations

import hashlib
import json
from math import gcd, isqrt
from pathlib import Path


def primality_trial(n: int) -> bool:
    if n < 2:
        return False
    return all(n % d != 0 for d in range(2, isqrt(n) + 1))


def primes_sieve(bound: int) -> list[int]:
    flags = bytearray(b'\x01') * (bound + 1)
    flags[:2] = b'\x00\x00'
    for d in range(2, isqrt(bound) + 1):
        if flags[d]:
            flags[d * d::d] = b'\x00' * (((bound - d * d) // d) + 1)
    return [n for n in range(bound + 1) if flags[n]]


def prime_gap_first_missing(primes: list[int], count: int) -> int:
    assert 0 < count < len(primes)
    observed = {primes[j + 1] - primes[j] for j in range(count)}
    t = 2
    while t in observed:
        t += 2
    return t


def primorial_stats(primes: list[int], k: int) -> dict:
    modulus = 1
    for q in primes[:k]:
        modulus *= q
    a = [n for n in range(1, modulus) if gcd(n, modulus) == 1]
    # Independent wheel computation, using divisibility marks rather than gcd.
    alive = bytearray(b'\x01') * modulus
    alive[0] = 0
    for q in primes[:k]:
        alive[::q] = b'\x00' * (len(alive[::q]))
    b = [n for n in range(1, modulus) if alive[n]]
    assert a == b, f'wheel / gcd mismatch for k={k}'
    gaps = {a[j + 1] - a[j] for j in range(len(a) - 1)}
    missing = 2
    while missing in gaps:
        missing += 2
    assert all(g % 2 == 0 for g in gaps)
    return {'k': k, 'primorial': modulus, 'phi': len(a),
            'max_gap': max(gaps), 'first_missing_even': missing,
            'distinct_consecutive_gaps': len(gaps)}


def main() -> None:
    primes = primes_sieve(1000)
    assert primes == [n for n in range(1001) if primality_trial(n)]
    r = {str(x): prime_gap_first_missing(primes, x) for x in (4, 10, 30, 100)}
    assert r == {'4': 6, '10': 8, '30': 10, '100': 16}
    primorials = [primorial_stats(primes, k) for k in (3, 4, 5, 6, 7, 8)]
    expected = [(30, 6, 8, 3), (210, 10, 12, 5), (2310, 14, 16, 7),
                (30030, 22, 20, 10), (510510, 26, 28, 13),
                (9699690, 34, 32, 16)]
    assert [(z['primorial'], z['max_gap'], z['first_missing_even'],
             z['distinct_consecutive_gaps']) for z in primorials] == expected
    pi = {str(x): sum(n <= x for n in primes) for x in (20, 100, 120)}
    assert pi == {'20': 8, '100': 25, '120': 30}
    assert pi['120'] <= pi['100'] + pi['20']
    output = {'record_type': 'ERDOS_COMPENDIUM_FINITE_CHECKS/1',
              'cohort_id': 'EC-BULK-006',
              'authority': 'FINITE_ARITHMETIC_ONLY_NO_ASYMPTOTIC_CLAIMS',
              'checks': {'853_prime_gap_missing': r,
                         '854_primorial_gaps': primorials,
                         '855_prime_count': pi},
              'methods': ['Sieve of Eratosthenes versus trial primality',
                          'GCD totatives versus independently marked wheel']}
    print(json.dumps(output, indent=2))


if __name__ == '__main__':
    main()
