#!/usr/bin/env python3
"""Dependency-free exact finite checks for EC-BULK-006 Erdős #875/#876.

Two independent implementations: (1) exhaustive masks with direct subset
sums, (2) incremental dynamic programming with bitsets and branch-and-bound.
Finite checks do not prove infinite asymptotic claims.
"""
import json
from itertools import combinations
from math import isqrt
from pathlib import Path


def admissible_direct(A):
    """#875: equal sums may not come from different subset cardinalities."""
    seen = {}
    for k in range(len(A) + 1):
        for sub in combinations(A, k):
            z = sum(sub)
            if z in seen and seen[z] != k:
                return False
            seen[z] = k
    return True


def sumfree_direct(A):
    """#876: no member is a sum of >=2 distinct smaller members."""
    for i, a in enumerate(A):
        for k in range(2, i + 1):
            if any(sum(sub) == a for sub in combinations(A[:i], k)):
                return False
    return True


def extremum_dp(N, mode):
    """Exact search; pruning is valid because each remaining integer adds <=1."""
    best, witness, nodes = 0, (), 0

    def visit(x, chosen, subset_bits, multisum_bits, layers):
        nonlocal best, witness, nodes
        nodes += 1
        if len(chosen) + max(0, N - x + 1) <= best:
            return
        if x > N:
            if len(chosen) > best:
                best, witness = len(chosen), chosen
            return
        if mode == 876:
            if not ((multisum_bits >> x) & 1):
                visit(x + 1, chosen + (x,),
                      subset_bits | (subset_bits << x),
                      multisum_bits | ((subset_bits & ~1) << x), None)
        else:
            new = [0] * (len(layers) + 1)
            for i, bits in enumerate(layers):
                new[i] |= bits
                new[i + 1] |= bits << x
            union, good = 0, True
            for bits in new:
                if union & bits:
                    good = False
                    break
                union |= bits
            if good:
                visit(x + 1, chosen + (x,), 0, 0, new)
        visit(x + 1, chosen, subset_bits, multisum_bits, layers)

    visit(1, (), 1, 0, [1])
    return {"maximum": best, "witness": list(witness), "visited_nodes": nodes}


def extremum_bruteforce(N, mode):
    """Independent exhaustive subsets; no DP states or branch pruning."""
    test = admissible_direct if mode == 875 else sumfree_direct
    best, witness, tested = 0, (), 0
    for mask in range(1 << N):
        A = tuple(i + 1 for i in range(N) if (mask >> i) & 1)
        tested += 1
        if len(A) >= best and test(A) and len(A) > best:
            best, witness = len(A), A
    return {"maximum": best, "witness": list(witness), "tested": tested}


def terminal_admissible(N, k):
    A = tuple(range(N - k + 1, N + 1))
    return admissible_direct(A)


def main():
    report = {"scope": "finite mathematical checks only; no infinite proof", "cross_checks": {},
              "dp_extrema": {}, "terminal_interval_tests": 0, "finite_876_formula_tests": 0}
    # Independent brute-force and DP extremal encodings.
    for N in (8, 10, 12, 14):
        report["cross_checks"][str(N)] = {}
        for mode in (875, 876):
            a = extremum_bruteforce(N, mode)
            b = extremum_dp(N, mode)
            assert a["maximum"] == b["maximum"], (N, mode, a, b)
            report["cross_checks"][str(N)][str(mode)] = {
                "max": a["maximum"], "bruteforce_witness": a["witness"],
                "dp_witness": b["witness"], "subsets_checked": a["tested"]}
    for N in (16, 18, 20, 24, 30, 36):
        report["dp_extrema"][str(N)] = {}
        for mode in (875, 876):
            a = extremum_dp(N, mode)
            assert (admissible_direct if mode == 875 else sumfree_direct)(a["witness"])
            report["dp_extrema"][str(N)][str(mode)] = a
    for N in range(2, 121):
        kstar = isqrt(4 * N + 1) - 1
        for k in range(1, min(kstar + 3, N) + 1):
            expected = (k + 1) ** 2 <= 4 * N + 1
            actual = terminal_admissible(N, k)
            assert expected == actual, (N, k, expected, actual)
            report["terminal_interval_tests"] += 1
    for N in range(1, 37):
        got = extremum_dp(N, 876)["maximum"]
        assert got == N // 2 + 1, (N, got)
        report["finite_876_formula_tests"] += 1
    witness = (4, 5, 6, 7, 8)
    assert sumfree_direct(witness) and not admissible_direct(witness)
    assert 4 + 5 + 6 == 7 + 8
    report["strict_converse_counterexample"] = {
        "set": list(witness), "sum_of_three": 15, "sum_of_two": 15,
        "satisfies_876": True, "satisfies_875": False}
    report["all_assertions_passed"] = True
    target = Path(__file__).with_suffix('.json')
    target.write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print(json.dumps({"result": "PASS", "report": str(target),
                      "terminal_tests": report["terminal_interval_tests"],
                      "formula_tests": report["finite_876_formula_tests"],
                      "cross_checked_N": [8, 10, 12, 14]}))


if __name__ == '__main__':
    main()
