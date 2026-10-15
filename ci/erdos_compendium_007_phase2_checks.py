#!/usr/bin/env python3
"""Repeatable exact arithmetic for EC-BULK-007 #1054, #1061, #1062, #1063.

This is finite evidence, not certification of any asymptotic problem.
"""
import json
from collections import defaultdict
from math import comb, isqrt


def sigma_trial(n):
    return sum(i for i in range(1, n + 1) if n % i == 0)


def sigma_sieve(limit):
    values = [0] * (limit + 1)
    for d in range(1, limit + 1):
        for n in range(d, limit + 1, d):
            values[n] += d
    return values


def divisor_representations(bound_m=1000, bound_n=35):
    seen = defaultdict(list)
    for m in range(1, bound_m + 1):
        divs = [d for d in range(1, m + 1) if m % d == 0]
        s = 0
        for k, d in enumerate(divs, start=1):
            s += d
            if s <= bound_n:
                seen[s].append((m, k, divs[:k]))
    assert 2 not in seen and 5 not in seen
    checks = {3: (2, 2, [1, 2]), 4: (3, 2, [1, 3]),
              6: (5, 2, [1, 5]), 7: (4, 3, [1, 2, 4]),
              9: (15, 3, [1, 3, 5]), 10: (12, 4, [1, 2, 3, 4])}
    for n, witness in checks.items():
        assert seen[n][0] == witness, (n, seen[n][0])
    return {"checked_m_through": bound_m,
            "n_2_and_5_missing_in_finite_search": True,
            "independent_elementary_nonrepresentability_proof_in_source_audit": True,
            "examples": {str(n): {"m": m, "k": k, "prefix": prefix}
                         for n, (m, k, prefix) in checks.items()}}


def divisor_pair_count():
    bound = 40
    sigma = sigma_sieve(bound)
    assert all(sigma[n] == sigma_trial(n) for n in range(1, bound + 1))
    data = {}
    for N in (10, 20, 40):
        pairs = [(a, b) for a in range(1, N) for b in range(1, N - a + 1)
                 if sigma[a] + sigma[b] == sigma[a + b]]
        data[N] = pairs
    assert [len(data[n]) for n in (10, 20, 40)] == [8, 12, 26]
    assert data[10] == [(1, 2), (2, 1), (2, 6), (2, 8),
                        (4, 5), (5, 4), (6, 2), (8, 2)]
    return {"ordered_pair_counts": {str(n): len(pairs) for n, pairs in data.items()},
            "pairs_x10": data[10], "sigma_independent_algorithms_agree": True}


def fork_free(seq):
    return all(sum(a != b and b % a == 0 for b in seq) <= 1 for a in seq)


def fork_maxima():
    best = []
    witnesses = []
    for n in range(1, 16):
        maxsz = 0
        witness = []
        for mask in range(1 << n):
            if mask.bit_count() <= maxsz:
                continue
            selected = [i + 1 for i in range(n) if mask >> i & 1]
            if fork_free(selected):
                maxsz = len(selected)
                witness = selected
        assert fork_free(list(range(n // 3 + 1, n + 1)))
        assert maxsz >= n - n // 3
        best.append(maxsz)
        witnesses.append(witness)
    assert best == [1, 2, 2, 3, 4, 4, 5, 6, 6, 7, 8, 8, 9, 10, 10]
    return {"exhaustive_n_through": 15, "maxima": best,
            "witness_n15": witnesses[-1], "forkfree_interval_lower_bound_examples_pass": True}


def binomial_exceptions():
    vals = {}
    for k in range(2, 10):
        first = None
        for n in range(2 * k, 10001):
            C = comb(n, k)
            bad = [i for i in range(k) if C % (n - i)]
            if len(bad) == 1:
                first = {"n": n, "bad_i": bad[0], "choose": C}
                break
        assert first is not None
        vals[str(k)] = first
    assert [vals[str(k)]["n"] for k in range(2, 10)] == [4, 6, 9, 12, 75, 30, 70, 56]
    return {"k_2_through_9": vals, "integer_binomial_checks": "PASS"}


def main():
    out = {"record_type": "EC_BULK_007_FINITE_ARITHMETIC_PHASE_2/1",
           "cohort_id": "EC-BULK-007",
           "is_mathematical_certification": False,
           "problem_1054": divisor_representations(),
           "problem_1061": divisor_pair_count(),
           "problem_1062": fork_maxima(),
           "problem_1063": binomial_exceptions(),
           "result": "FINITE_CHECKS_PASS"}
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
