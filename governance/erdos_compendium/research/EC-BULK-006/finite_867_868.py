#!/usr/bin/env python3
"""Exact, finite source-fidelity fixtures for Erdős #867 and #868.

Independent methods: branch-and-bound incremental forbidden sums vs exhaustive
fixed-cardinality combinations (#867); unordered vs ordered representation
enumeration (#868). Does not certify any infinite/asymptotic theorem.
"""
from itertools import combinations
from math import comb
import json


def admissible_867(seq):
    chosen = set(seq)
    for i, a in enumerate(seq):
        total = a
        for b in seq[i+1:]:
            total += b
            if total in chosen:
                return False
    return True


def branch_bound_867(N):
    best = ()
    def search(chosen, forbidden, candidate):
        nonlocal best
        if len(chosen) + N - candidate + 1 <= len(best):
            return
        if candidate > N:
            if len(chosen) > len(best):
                best = chosen
            return
        if not (forbidden >> candidate) & 1:
            new_forbidden = forbidden
            total = candidate
            for a in reversed(chosen):
                total += a
                if total <= N:
                    new_forbidden |= 1 << total
            search(chosen + (candidate,), new_forbidden, candidate+1)
        search(chosen, forbidden, candidate+1)
    search((), 0, 1)
    return best


def direct_upper_exclusion(N, lower_bound):
    """Every size-(lower_bound+1) subset is inadmissible (independent)."""
    count = 0
    for subset in combinations(range(1, N+1), lower_bound+1):
        assert not admissible_867(subset), (N, subset)
        count += 1
    assert count == comb(N, lower_bound+1)
    return count


def ordered_unordered_868(A, n):
    unordered = [(a,b) for a in A for b in A if a <= b and a+b == n]
    ordered = [(a,b) for a in A for b in A if a+b == n]
    diagonal = int(n % 2 == 0 and n//2 in A)
    assert len(ordered) == 2*len(unordered)-diagonal
    return {'n': n, 'unordered': len(unordered),
            'ordered': len(ordered), 'diagonal': diagonal}


def main():
    checks = []
    for N in (10, 15, 20):
        witness = branch_bound_867(N)
        assert admissible_867(witness)
        checked = direct_upper_exclusion(N, len(witness))
        checks.append({'N': N, 'f_N': len(witness), 'witness': list(witness),
                       'independent_upper_combination_checks': checked})
    A = [1,2,3,4,6]
    reprs = [ordered_unordered_868(A, n) for n in (5,6,7,8,9)]
    print(json.dumps({'record_type':'EC_BULK_006_FINITE_867_868/1',
        'scope':'FINITE_ARITHMETIC_ONLY', '867':checks,
        '868':{'A':A, 'representation_checks':reprs,
               'exact_identity':'R_ordered=2*R_unordered-diagonal_indicator'}},
        indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
