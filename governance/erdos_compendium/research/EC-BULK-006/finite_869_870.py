#!/usr/bin/env python3
"""Exact, bounded checks for EC-BULK-006 #869/#870; not an infinite proof."""
from __future__ import annotations
from collections import Counter
from itertools import combinations_with_replacement
import json
import random


def unordered_pair_counts(a: set[int]) -> Counter:
    out = Counter()
    for x, y in combinations_with_replacement(sorted(a), 2):
        out[x + y] += 1
    return out


def direct_sumset(a: set[int]) -> set[int]:
    return {x + y for x in a for y in a}


def minimal_cover(a: set[int], targets: range) -> tuple[set[int], dict[int, int]]:
    # Deletion algorithm on a FINITE list of target sums.
    s = set(a)
    target = set(targets)
    assert target <= direct_sumset(s)
    for x in sorted(s):
        if target <= direct_sumset(s - {x}):
            s.remove(x)
    certificates = {}
    for x in sorted(s):
        missing = target - direct_sumset(s - {x})
        assert missing
        certificates[x] = min(missing)
    return s, certificates


def count_by_combinations(a: tuple[int, ...], k: int, n: int) -> int:
    return sum(sum(t) == n for s in range(1, k + 1)
               for t in combinations_with_replacement(a, s))


def count_by_dp(a: tuple[int, ...], k: int, n: int) -> int:
    # Coin-change DP indexed by exact number of summands and sum.
    dp = [[0] * (n + 1) for _ in range(k + 1)]
    dp[0][0] = 1
    for coin in a:
        for size in range(1, k + 1):
            for total in range(coin, n + 1):
                dp[size][total] += dp[size - 1][total - coin]
    return sum(dp[size][n] for size in range(1, k + 1))


def main() -> None:
    N = 160
    targets = range(60, 161)
    chosen = None
    for seed in range(2000):
        rng = random.Random(seed)
        b = {x for x in range(1, N + 1) if rng.randrange(2) == 0}
        c = set(range(1, N + 1)) - b
        if set(targets) <= direct_sumset(b) and set(targets) <= direct_sumset(c):
            chosen = seed, b, c
            break
    assert chosen is not None
    seed, b, c = chosen
    assert b.isdisjoint(c) and b | c == set(range(1, N + 1))
    a = b | c
    rb, rc, ra = map(unordered_pair_counts, (b, c, a))
    for n in range(2, 2 * N + 1):
        cross = sum(1 for x in b if n - x in c)
        assert ra[n] == rb[n] + rc[n] + cross
    minimal, essential = minimal_cover(a, targets)
    assert set(targets) <= direct_sumset(minimal)
    # Two independent pair-counting methods agree on coverage.
    assert set(targets) <= set(unordered_pair_counts(minimal))
    assert all(set(targets) - direct_sumset(minimal - {x}) for x in minimal)
    assert set(targets) <= direct_sumset(a - {min(a)})
    # #870: nondecreasing, positive, repetition allowed, 1..k summands.
    coins = (1, 2, 3, 5, 8, 13)
    checks = {}
    for k in (2, 3, 4):
        checks[str(k)] = {}
        for n in range(1, 31):
            x = count_by_combinations(coins, k, n)
            y = count_by_dp(coins, k, n)
            assert x == y, (k, n, x, y)
            if n in (3, 10, 20, 30):
                checks[str(k)][str(n)] = x
    assert count_by_combinations((3,), 3, 3) == 1
    assert sum(sum(t) == 3 for t in combinations_with_replacement((3,), 3)) == 0
    # Source-fidelity exception: original 1988 exact-h basis differs from the
    # maintained at-most-k convention. A={1 mod 3} is an at-most-3 basis,
    # but its exact-three sumset contains only multiples of three.
    residue_set = {x for x in range(1, 101) if x % 3 == 1}
    for n in range(3, 101):
        atmost = any(count_by_combinations(tuple(sorted(residue_set)), 3, n)
                     for _ in (0,))
        assert atmost
        exact3 = any(sum(t) == n for t in
                     combinations_with_replacement(sorted(residue_set), 3))
        assert exact3 == (n % 3 == 0), n
    out = {
        'record_type': 'EC-BULK-006_FINITE_0869_0870/1',
        'authority': 'FINITE_CHECK_ONLY_NO_ASYMPTOTIC_OR_LEAN_CERTIFICATION',
        '869': {
            'partition_seed': seed, 'ambient': [1, N],
            'finite_target_range': [targets.start, targets.stop - 1],
            'B_size': len(b), 'C_size': len(c),
            'B_and_C_both_cover_all_targets': True,
            'unordered_pair_decomposition_all_n_2_to_320': True,
            'finite_minimal_subcover_size': len(minimal),
            'finite_minimal_subcover': sorted(minimal),
            'essentiality_certificates': {str(x): essential[x] for x in sorted(essential)},
            'caveat': 'Finite target families ALWAYS admit a minimal subcover. This is NOT a counterexample to #869.'
        },
        '870': {
            'basis_sample': list(coins), 'counts_at_most_k': checks,
            'algorithms': ['combinations_with_replacement', 'coin_change_DP'],
            'sample_exact_vs_at_most': {'A': [3], 'k': 3, 'n': 3, 'exact_k': 0, 'at_most_k': 1},
            'original_exact_vs_modern_at_most_basis': {
                'A': 'all positive integers congruent to 1 mod 3',
                'at_most_3_basis': True, 'exact_3_basis': False,
                'checked_n': [3, 100],
                'proof': '1,2,3 summands cover residue classes 1,2,0 respectively; every exact triple is 0 mod 3'},
            'caveat': 'The finite identity tests the representation semantics only, not the claimed infinite theorem.'
        }
    }
    print(json.dumps(out, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
