#!/usr/bin/env python3
"""Bounded independent graph-counting oracle for ERDOS-PV-0560-B.

Finite tests support a separately written general proof; do not infer that
exhaustive finite enumeration proves the theorem or the open diagonal case.
"""
from fractions import Fraction
from itertools import combinations
from math import comb, exp
import json
import random

TASK = "ERDOS-PV-0560-B"
SOURCE_SHA256 = "2bafa6656b0d797f8b7637be2d7ff77e7682e329467a9df9c858da7e9b7708c1"


def parameters(s, t):
    if type(s) is not int or type(t) is not int or s < 2 or t < s + 2:
        raise ValueError("requires s >= 2, t >= s+2")


def neighbors(n, graph_mask):
    if type(n) is not int or not 0 <= n <= 9:
        raise ValueError("finite graph size outside 0..9")
    edges = tuple(combinations(range(n), 2))
    if type(graph_mask) is not int or not 0 <= graph_mask < 2 ** len(edges):
        raise ValueError("invalid edge mask")
    ans = [0] * n
    for bit, (u, v) in enumerate(edges):
        if graph_mask >> bit & 1:
            ans[u] |= 1 << v
            ans[v] |= 1 << u
    return tuple(ans)


def graph_edges(adj):
    n = len(adj)
    if n > 9 or any(type(x) is not int or x < 0 or x >= 2 ** n for x in adj):
        raise ValueError("invalid adjacency")
    for i in range(n):
        if adj[i] >> i & 1:
            raise ValueError("self loop")
        for j in range(i):
            if bool(adj[i] >> j & 1) != bool(adj[j] >> i & 1):
                raise ValueError("asymmetry")
    return sum(x.bit_count() for x in adj) // 2


def producer(adj, s, t):
    """Count by common-neighbor intersection; bucket by degree order."""
    parameters(s, t)
    q = graph_edges(adj)
    n = len(adj)
    order = sorted(range(n), key=lambda v: (-adj[v].bit_count(), v))
    ranks = {v: i + 1 for i, v in enumerate(order)}
    degree = tuple(adj[v].bit_count() for v in order)
    buckets = [0] * n
    for side in combinations(range(n), s):
        common = (1 << n) - 1
        for v in side:
            common &= adj[v]
        assert all(not (common >> v & 1) for v in side)
        if common.bit_count() >= t:
            buckets[max(ranks[v] for v in side)-1] += comb(common.bit_count(), t)
    bound = tuple(comb(i-1, s-1) * comb(d, t) if i >= s and d >= t else 0
                  for i, d in enumerate(degree, start=1))
    assert all(i*d <= 2*q for i, d in enumerate(degree, start=1))
    assert all(a <= b for a, b in zip(buckets, bound))
    return sum(buckets), tuple(buckets), bound


def oracle(adj, s, t):
    """Independent pair enumeration (does not use common-neighbor counts)."""
    parameters(s, t)
    n = len(adj)
    total = 0
    for S in combinations(range(n), s):
        rest = [v for v in range(n) if v not in S]
        for T in combinations(rest, t):
            if all((adj[u] >> v) & 1 for u in S for v in T):
                total += 1
    return total


def integral_factor(s, t):
    parameters(s, t)
    a = t - s
    return Fraction(s-1, a-1) * Fraction(s, s-1) ** a


def first_moment(number_of_copies, s, t):
    parameters(s, t)
    if type(number_of_copies) is not int or number_of_copies < 0:
        raise ValueError("invalid number of copies")
    return Fraction(number_of_copies, 2 ** (s*t-1))


def check_graph(adj, s, t):
    q = graph_edges(adj)
    count, buckets, upper = producer(adj, s, t)
    independent = oracle(adj, s, t)
    if count != independent:
        raise AssertionError(f"producer/oracle disagree: {len(adj)}, {s}, {t}")
    if any(a > b for a, b in zip(buckets, upper)):
        raise AssertionError("Ni bound failed")
    if q == 0:
        assert count == 0
    elif count > (4 * exp(2) * q / (s*t)) ** t:
        raise AssertionError("numerical counting bound failed")
    return count, buckets, upper


def exhaustive():
    seen, positive, maximum, tight = 0, 0, 0, 0
    for mask in range(2 ** comb(6, 2)):
        adj = neighbors(6, mask)
        count, buckets, upper = check_graph(adj, 2, 4)
        seen += 1
        positive += (count != 0)
        maximum = max(maximum, count)
        tight += any(a and a == b for a, b in zip(buckets, upper))
    return {"n":6, "s":2, "t":4, "graph_cases":seen,
            "positive_cases":positive, "max_copies":maximum,
            "tight_positive_bucket_cases":tight}


def samples():
    rng = random.Random(5600560)
    results = []
    for n, s, t, trials in (
        (7,2,4,700),(7,2,5,600),(8,2,4,700),
        (8,2,6,500),(8,3,5,550),(9,3,6,350)
    ):
        nonzero = 0
        for i in range(trials):
            full = 2 ** comb(n, 2) - 1
            if i == trials-1:
                mask = full
            else:
                probability = Fraction(1 + (i % 7)*2, 16)
                mask = sum((rng.random() < probability) << bit
                           for bit in range(comb(n,2)))
            count, _, _ = check_graph(neighbors(n,mask),s,t)
            nonzero += count > 0
        results.append({"n":n,"s":s,"t":t,
                        "cases":trials,"positive_cases":nonzero})
    return results


def regenerate():
    checked = 0
    for s in range(2, 23):
        for t in range(s+2,61):
            # Exact rational finite regression, not a proof by sampling.
            assert integral_factor(s,t) <= 2 ** t
            checked += 1
    # e < 3, and 2*(18/25)**4 < 1 is strict in Q.
    assert 2 * Fraction(18,25) ** 4 < 1
    assert first_moment(1,2,4) == Fraction(1,128)
    full = exhaustive()
    sampled = samples()
    return {"record_type":"ERDOS-PV-0560-B-FINITE-CERTIFICATE/1",
            "assignment_id":TASK,"source_issue_body_sha256":SOURCE_SHA256,
            "claim_ref":"refs/heads/gcl-pv-claims/"+TASK,
            "universal_proof_location":"B_OFF_DIAGONAL_COPY_COUNT_PROOF_001.md",
            "exhaustive":full,"sampled":sampled,
            "total_graph_oracle_checks":full["graph_cases"]+sum(x["cases"] for x in sampled),
            "exact_integral_factor_parameter_checks":checked,
            "strict_first_moment_gate":"2*(18/25)^4 < 1",
            "status":"FINITE_REGRESSION_PASS_NOT_A_GENERAL_PROOF",
            "claim_boundary":{"diagonal_conjecture_solved":False,
                              "lean_kernel_replayed":False,
                              "mathcert_certified":False}}


if __name__ == "__main__":
    print(json.dumps(regenerate(), sort_keys=True, indent=2))
