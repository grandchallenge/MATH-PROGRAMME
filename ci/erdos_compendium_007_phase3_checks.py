#!/usr/bin/env python3
"""Finite checks for EC-BULK-007 #1065 and #1066.

Only finite arithmetic and exact rational-coordinate graph checks; no infinite proofs.
"""
import itertools
import json
from fractions import Fraction


def is_prime(n):
    return n >= 2 and all(n % d for d in range(2, int(n**0.5) + 1))


def prime_patterns(limit=1000):
    primes = [p for p in range(2, limit + 1) if is_prime(p)]
    small, large = {}, {}
    for q in primes:
        a = 1
        k = 0
        while a * q + 1 <= limit:
            p = a * q + 1
            if is_prime(p):
                small.setdefault(p, (k, q))
            b = a
            l = 0
            while b * q + 1 <= limit:
                x = b * q + 1
                if is_prime(x):
                    large.setdefault(x, (k, l, q))
                b *= 3
                l += 1
            a *= 2
            k += 1
    for p, (k, q) in small.items():
        assert p == 2**k * q + 1 and is_prime(p) and is_prime(q)
        assert p in large
    for p, (k, l, q) in large.items():
        assert p == 2**k * 3**l * q + 1 and is_prime(p) and is_prime(q)
    for k, q, p in ((0, 2, 3), (1, 3, 7), (1, 5, 11),
                    (2, 3, 13), (2, 7, 29), (3, 5, 41)):
        assert small[p] == (k, q)
    assert not is_prime(2**4 * 3 + 1)
    return {"p_cutoff": limit, "small_count": len(small), "large_count": len(large),
            "first_ten_small": sorted(small)[:10], "first_ten_large": sorted(large)[:10],
            "smaller_family_subset_of_larger": True,
            "k0_only_witness": [3]}


def exact_geometry_triangle_unions():
    # Each point is (x, y_coefficient) representing (x, y_coefficient*sqrt(3)).
    vertices = []
    for group in range(3):
        shift = Fraction(10 * group)
        vertices.extend(((shift, Fraction(0)),
                         (shift + Fraction(1), Fraction(0)),
                         (shift + Fraction(1, 2), Fraction(1, 2))))
    def squared(a, b):
        dx = a[0] - b[0]
        dy = a[1] - b[1]
        return dx * dx + 3 * dy * dy
    edges = []
    for i, j in itertools.combinations(range(9), 2):
        distance = squared(vertices[i], vertices[j])
        assert distance >= 1
        if distance == 1:
            edges.append((i, j))
    expected = [(i, j) for group in range(3)
                for i, j in itertools.combinations(range(group * 3, group * 3 + 3), 2)]
    assert edges == expected
    maxima = []
    for n in (3, 6, 9):
        mn = [(i, j) for i, j in edges if i < n and j < n]
        best = max((mask.bit_count() for mask in range(1 << n)
                    if all(not (mask & 1 << i and mask & 1 << j) for i, j in mn)), default=0)
        maxima.append(best)
    assert maxima == [1, 2, 3]
    return {"number_triangles": 3, "separation_shift": 10,
            "exact_rational_squared_distance_arithmetic": True,
            "independence_max_for_n_3_6_9": maxima,
            "unbounded_repetition_requires_separate_mathematical_argument": True}


def main():
    print(json.dumps({
        "record_type": "EC_BULK_007_FINITE_ARITHMETIC_PHASE_3/1",
        "cohort_id": "EC-BULK-007", "mathematical_certification": False,
        "problem_1065": prime_patterns(),
        "problem_1066": exact_geometry_triangle_unions(),
        "problem_1067": "Elementary K4 has exactly three maximal internally vertex-disjoint paths per pair; not an infinite counterexample",
        "problem_1068": "Elementary K_aleph1 contains countable K_aleph0, but this is not the universal theorem",
        "result": "FINITE_CHECKS_PASS"}, indent=2))


if __name__ == "__main__":
    main()
