#!/usr/bin/env python3
"""Independent finite checks for EC-BULK-007 #1053, #1055, #1056.

Finite fixtures do not prove any open Erdős problem.
"""
from __future__ import annotations
from functools import lru_cache
from math import isqrt, prod
import json

LIMIT = 2000


def sieve_primes(n):
    flag = [True] * (n + 1)
    flag[0:2] = [False, False]
    for p in range(2, isqrt(n) + 1):
        if flag[p]:
            for q in range(p * p, n + 1, p):
                flag[q] = False
    return [p for p in range(n + 1) if flag[p]]


def prime_factors(n):
    ans = []
    q = 2
    while q * q <= n:
        if n % q == 0:
            ans.append(q)
            while n % q == 0:
                n //= q
        q += 1
    if n > 1:
        ans.append(n)
    return ans


def sigma_by_sieve(limit):
    s = [0] * (limit + 1)
    for d in range(1, limit + 1):
        for m in range(d, limit + 1, d):
            s[m] += d
    return s


def sigma_by_trial(n):
    return sum(d for d in range(1, n + 1) if n % d == 0)


def is_squarefree(n):
    d = 2
    while d * d <= n:
        if n % (d * d) == 0:
            return False
        d += 1
    return True


def rank_iterative(primes):
    ranks = {}
    for p in primes:
        fs = prime_factors(p + 1)
        ranks[p] = 1 if set(fs) <= {2, 3} else 1 + max(ranks[q] for q in fs if q > 3)
    return ranks


@lru_cache(None)
def rank_recursive(p):
    fs = prime_factors(p + 1)
    return 1 if set(fs) <= {2, 3} else 1 + max(rank_recursive(q) for q in fs if q > 3)


def block_values(bounds):
    return [prod(range(a, b)) for a, b in zip(bounds, bounds[1:])]


def main():
    sigma = sigma_by_sieve(10000)
    assert all(sigma[n] == sigma_by_trial(n) for n in range(1, 1001))
    multiperfect = [(n, sigma[n] // n) for n in range(1, 10001) if sigma[n] % n == 0]
    sq = [(n, k) for n, k in multiperfect if is_squarefree(n)]
    assert sq == [(1, 1), (6, 2)], sq
    assert [(n, sigma[n]) for n in (6, 28, 120)] == [(6, 12), (28, 56), (120, 360)]
    primes = sieve_primes(LIMIT)
    ranks = rank_iterative(primes)
    assert all(ranks[p] == rank_recursive(p) for p in primes)
    first = {}
    for p in primes:
        first.setdefault(ranks[p], p)
    assert [first[r] for r in range(1, 6)] == [2, 13, 37, 73, 1021]
    cases = [(11, [3, 5, 8], [12, 210]), (17, [2, 6, 12, 16], [120, 332640, 32760])]
    for modulus, bounds, expected in cases:
        assert block_values(bounds) == expected
        assert all(v % modulus == 1 for v in expected)
    result = {
        "record_type": "EC_BULK_007_FINITE_ARITHMETIC/1",
        "cohort_id": "EC-BULK-007",
        "proof_certification": False,
        "problem_1053": {"sigma_test_range": [1, 1000], "multiple_perfect_through": 10000,
                         "sigma_6_28_120": [12, 56, 360],
                         "squarefree_multiply_perfect": sq, "count_multiply_perfect": len(multiperfect)},
        "problem_1055": {"prime_bound": LIMIT, "prime_count": len(primes),
                         "two_rank_algorithms_agree": True,
                         "least_class_prime_1_to_5": [first[r] for r in range(1, 6)]},
        "problem_1056": {"verified_witnesses": [
            {"p": 11, "bounds": [3, 5, 8], "products": [12, 210]},
            {"p": 17, "bounds": [2, 6, 12, 16], "products": [120, 332640, 32760]}]},
        "result": "FINITE_CHECKS_PASS"
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
