#!/usr/bin/env python3
"""Independent bounded arithmetic checks; no host-Ramsey enumeration."""
import itertools
import json


def profiles():
    for length in range(1, 5):
        for a in itertools.combinations_with_replacement(range(1, 6), length):
            yield a[::-1]


def main():
    lists = list(profiles())
    tested = old_pass = new_pass = parity_pass = 0
    for n, m in itertools.product(lists, repeat=2):
        s, t = len(n), len(m)
        weights = [
            max(n[i] + m[k - i] - 1
                for i in range(s) if 0 <= k - i < t)
            for k in range(s + t - 1)
        ]
        for k, w in enumerate(weights):
            tail = weights[k:]
            assert tail == sorted(tail, reverse=True)
            L, W, D = len(tail), sum(tail), w - 1
            pairs = [(i, k - i) for i in range(s) if 0 <= k-i < t]
            max_pairs = [(i, j) for i, j in pairs if n[i]+m[j]-1 == w]
            runs = [(sum(a == n[i] for a in n[i:]),
                     sum(b == m[j] for b in m[j:]), i, j)
                    for i, j in max_pairs]
            P = tail.count(w)
            assert P == max(u+v-1 for u, v, _, _ in runs)
            tested += 1
            if D < 2 or any(n[i] == 1 or m[j] == 1 for i, j in max_pairs):
                continue
            M = max(max(sum(n[i:]), sum(m[j:])) for i, j in pairs)
            pmax = (2*(W-1)-L-M)//(D-1)
            if pmax < D+1:
                continue
            old_pass += 1
            if pmax < P*(D+1) or P*D >= 2*L:
                continue
            new_pass += 1
            if any((n[i]-1)%2 == 0 or (m[j]-1)%2 == 0
                   for u, v, i, j in runs if u+v-1 == P):
                if pmax < (P+1)*(D+1):
                    continue
            parity_pass += 1
    return {
        "scope": "ordered positive profiles, each length 1..4 and arms 1..5; arithmetic filters for hypothetical least-L counterexamples, not solved instances",
        "frontiers": tested,
        "old_single_core_guard_survivors": old_pass,
        "plateau_guard_survivors": new_pass,
        "plateau_and_even_cap_guard_survivors": parity_pass,
        "excluded_by_new_guards": old_pass-parity_pass,
        "status": "PASS",
    }


if __name__ == "__main__":
    print(json.dumps(main(), indent=2))
