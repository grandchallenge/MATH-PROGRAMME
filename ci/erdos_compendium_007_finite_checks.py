#!/usr/bin/env python3
"""Independent finite checks for EC-BULK-007 #1053, #1055, #1056.

Finite fixtures do not prove any open Erdős problem.
"""
from __future__ import annotations
from functools import lru_cache
from math import isqrt, prod, factorial, gcd
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
    # Three further bounded claims: Korselt witnesses, Luca small cases, factorial subtraction.
    def isprime_trial(n):
        return n >= 2 and all(n % d for d in range(2, isqrt(n) + 1))
    def korselt(n):
        fs = prime_factors(n)
        return n > 1 and not isprime_trial(n) and prod(fs) == n and all((n - 1) % (p - 1) == 0 for p in fs)
    carmichael = [(n, prime_factors(n)) for n in (561, 1105, 1729)]
    assert all(korselt(n) for n, _ in carmichael)
    # Independent direct modular verification of the universal Fermat property for each finite witness.
    assert all(all(pow(a, n - 1, n) == 1 for a in range(1, n) if gcd(a, n) == 1) for n, _ in carmichael)
    factvals = [factorial(n) + 1 for n in range(1, 6)]
    assert factvals == [2, 3, 7, 25, 121]
    subtractions = {}
    for prime in (101, 211):
        assert isprime_trial(prime)
        fs = [factorial(k) for k in range(1, 10) if factorial(k) < prime]
        diffs = [prime - f for f in fs]
        assert all(x > 1 and not isprime_trial(x) for x in diffs)
        subtractions[prime] = diffs
    assert subtractions == {101: [100, 99, 95, 77], 211: [210, 209, 205, 187, 91]}
    # #1060: divisor-count collision problem. k*sigma(k) >= k^2.
    n_bound = 65536
    root = isqrt(n_bound)
    sig2 = sigma_by_sieve(root)
    assert all(sig2[k] == sigma_by_trial(k) for k in range(1, root + 1))
    from collections import defaultdict
    inverse = defaultdict(list)
    for k in range(1, root + 1):
        value = k * sig2[k]
        if value <= n_bound:
            inverse[value].append(k)
    collisions = [(n, inverse[n]) for n in sorted(inverse) if len(inverse[n]) >= 2]
    assert collisions == [
        (336, [12, 14]), (5952, [48, 62]), (10080, [60, 70]),
        (27776, [112, 124]), (44352, [132, 154]),
        (60480, [160, 189]), (61152, [156, 182])]
    assert max(len(v) for v in inverse.values()) == 2
    # #1064: exact totient comparison, with phi(0)=0 as in natural-number arithmetic.
    phi_limit = 200000
    phi = list(range(phi_limit + 1))
    for p0 in range(2, phi_limit + 1):
        if phi[p0] == p0:
            for q in range(p0, phi_limit + 1, p0):
                phi[q] -= phi[q] // p0
    counts = [0, 0, 0]
    first_less = []
    for n in range(1, phi_limit + 1):
        a = phi[n]
        b = phi[n - a]
        if a > b:
            counts[0] += 1
        elif a == b:
            counts[1] += 1
        else:
            counts[2] += 1
            if len(first_less) < 10:
                first_less.append(n)
    assert counts == [194833, 175, 4992]
    assert first_less == [30, 60, 66, 120, 132, 138, 174, 210, 240, 246]
    for k in range(1, 20):
        n = 15 * 2**k
        if n <= phi_limit:
            assert phi[n] == 4 * 2**k and phi[n - phi[n]] == 5 * 2**k
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
        "problem_1060": {"n_bound_exhaustive": n_bound,
                          "two_sigma_algorithms_agree": True,
                          "max_multiplicity": 2,
                          "collisions": [{"n": n, "preimages": pre} for n, pre in collisions]},
        "problem_1064": {"n_bound_exhaustive": phi_limit,
                          "gt_eq_lt_counts": counts,
                          "first_strict_less_values": first_less,
                          "exceptional_family": "15*2^k, k>=1 (symbolic totient identity)"},
        "problem_1057": {"korselt_witnesses": [n for n, _ in carmichael],
                          "finite_fermat_check_all_coprime_bases": True},
        "problem_1058": {"factorial_plus_one_n_1_to_5": factvals,
                          "historical_n_equals_1_indexing_exception": True},
        "problem_1059": {"checked_prime_subtractions": {str(k): v for k, v in subtractions.items()}},
        "problem_1056": {"verified_witnesses": [
            {"p": 11, "bounds": [3, 5, 8], "products": [12, 210]},
            {"p": 17, "bounds": [2, 6, 12, 16], "products": [120, 332640, 32760]}]},
        "result": "FINITE_CHECKS_PASS"
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
