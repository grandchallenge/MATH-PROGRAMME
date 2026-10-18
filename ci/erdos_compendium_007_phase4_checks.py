#!/usr/bin/env python3
"""Exact finite witnesses for Erdős #1069, #1072 and #1073.

These bounded computations do not imply any asymptotic result or editorial admission.
"""
import json
from math import gcd, isqrt


def is_prime(n):
    return n >= 2 and all(n % d for d in range(2, isqrt(n) + 1))


def grid_rich_lines(q):
    points = [(x, y) for x in range(q) for y in range(q)]
    lines = set()
    for i, (x, y) in enumerate(points):
        for u, v in points[i + 1:]:
            a, b = v - y, x - u
            c = a * x + b * y
            g = gcd(gcd(abs(a), abs(b)), abs(c))
            a, b, c = a // g, b // g, c // g
            if a < 0 or (a == 0 and b < 0):
                a, b, c = -a, -b, -c
            lines.add((a, b, c))
    return sum(sum(a*x + b*y == c for x, y in points) >= q
               for a, b, c in lines)


def factorial_prime_indices(limit):
    result = {}
    for p in range(2, limit+1):
        if not is_prime(p):
            continue
        residue = 1
        for n in range(p):
            if n:
                residue = residue * n % p
            if (residue + 1) % p == 0:
                result[p] = n
                break
        assert p in result  # Wilson's endpoint
    return result


def factorial_composites(limit):
    result = {}
    for u in range(4, limit+1):
        if is_prime(u):
            continue
        residue = 1
        for n in range(u):
            if n:
                residue = residue * n % u
            if (residue + 1) % u == 0:
                result[u] = n
                break
    return result


def main():
    grids = {q: grid_rich_lines(q) for q in (3, 4, 5)}
    assert grids == {3: 8, 4: 10, 5: 12}
    primes = factorial_prime_indices(150)
    assert len(primes) == 35 and primes[2] == 0
    endpoints = [p for p, n in primes.items() if n == p-1]
    assert endpoints == [3, 5, 13, 17, 31, 37, 41, 53, 73, 89, 97, 101, 107, 113]
    composites = factorial_composites(1000)
    assert composites == {25:4, 121:5, 169:12, 437:18, 551:18, 667:18, 721:6}
    # Independent direct factorial replay for each qualifying modulus.
    import math
    assert all((math.factorial(n)+1) % u == 0 for u, n in composites.items())
    result = {
        'record_type': 'EC_BULK_007_FINITE_ARITHMETIC_PHASE_4/1',
        'cohort_id': 'EC-BULK-007',
        'mathematical_certification': False,
        'problem_1069': {'q_by_q_grid_k_q_rich_lines': {str(k):v for k,v in grids.items()}},
        'problem_1072': {'all_primes_through':150,'prime_count':len(primes),
                         'f_of_2':0,'f_equals_p_minus_1_primes':endpoints},
        'problem_1073': {'all_composite_moduli_through':1000,
                         'minimal_witnesses':{str(k):v for k,v in composites.items()},
                         'A_of_1001':len(composites), 'factorial_direct_crosscheck':True},
        'result': 'FINITE_CHECKS_PASS'}
    print(json.dumps(result,indent=2,ensure_ascii=False))


if __name__ == '__main__':
    main()
