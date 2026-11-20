#!/usr/bin/env python3
"""Exact star-allocation corroboration for the b>=4 infinite theorem.

The mathematical arbitrary-host lower bound is proved in the associated paper.
No finite search is promoted to an unbounded theorem.
"""
from itertools import permutations, product

RED1, BLUE1 = (1, 1), None
RED2, BLUE2 = (3, 1, 1), (2, 2, 1)


def dominates(capacities, target):
    """Fast exact star-forest containment for a disjoint union of stars."""
    capacities = sorted(capacities, reverse=True)
    target = sorted(target, reverse=True)
    return len(capacities) >= len(target) and all(
        x >= y for x, y in zip(capacities, target)
    )


def injection_oracle(capacities, target):
    """Separately implemented factorial-size injective embedding oracle."""
    return any(
        all(capacities[i] >= want for i, want in zip(indices, target))
        for indices in permutations(range(len(capacities)), len(target))
    )


def count_avoiders(host, red_target, blue_target, independent=False):
    avoiders = []
    total = 0
    for red in product(*(range(k + 1) for k in host)):
        blue = tuple(k - r for k, r in zip(host, red))
        red_hit = dominates(red, red_target)
        blue_hit = dominates(blue, blue_target)
        if independent:
            assert red_hit == injection_oracle(red, red_target), (
                host, red, "red recognizer disagreement"
            )
            assert blue_hit == injection_oracle(blue, blue_target), (
                host, red, "blue recognizer disagreement"
            )
        total += 1
        if not (red_hit or blue_hit):
            avoiders.append((red, blue))
    return total, avoiders


def antidiagonal(n, m):
    """Compute canonical joint-residual star-arm antidiagonal (k=3..s+t)."""
    out = []
    for k in range(3, len(n) + len(m) + 1):
        out.append(max(
            n[i - 1] + m[k - i - 1] - 1
            for i in range(1, len(n) + 1)
            if 1 <= k - i <= len(m)
        ))
    return tuple(out)


def check_main_family():
    for b in range(4, 15):
        full_blue = (b, 2, 2, 1)
        upper = (b, b, 3, 2, 1)
        saturated = (b, b, 2, 2, 1)
        assert antidiagonal((3, 1, 1), full_blue) == upper
        assert sum(upper) == 2 * b + 6
        assert sum(saturated) == 2 * b + 5
        checks = ((RED1, full_blue), (RED2, BLUE2))
        up_counts = []
        lo_counts = []
        for red_target, blue_target in checks:
            up_total, up_bad = count_avoiders(
                upper, red_target, blue_target, independent=(b <= 6)
            )
            lo_total, lo_bad = count_avoiders(
                saturated, red_target, blue_target, independent=(b <= 6)
            )
            assert not up_bad, (b, red_target, up_bad[:2])
            up_counts.append(up_total)
            lo_counts.append((lo_total, lo_bad))
        assert lo_counts[0][1] == [], ("saturated R1 failed", b)
        red_witness = (2, 2, 2, 2, 1)
        blue_witness = (b - 2, b - 2, 0, 0, 0)
        assert (red_witness, blue_witness) in lo_counts[1][1]
        assert up_counts == [(b + 1) ** 2 * 24] * 2
        assert all(total == (b + 1) ** 2 * 18 for total, _ in lo_counts)
        if b == 5:
            assert up_counts[0] == 864
            assert lo_counts[0][0] == 648
            assert len(lo_counts[1][1]) == 9
        print("B221_CERTIFIED_ALLOCATION", b, "upper", up_counts[0],
              "saturated", lo_counts[0][0],
              "saturated_R2_avoiders", len(lo_counts[1][1]))


def check_boundary():
    b = 3
    h = (b, 2, 2, 1)
    naive_host = (b, b, 3, 2, 1)
    canonical = antidiagonal((3, 1, 1), h)
    assert canonical == (4, 4, 3, 2, 1), canonical
    assert sum(naive_host) == 12 and sum(canonical) == 14
    fail_red, fail_blue = (2, 2, 2, 1, 0), (1, 1, 1, 1, 1)
    assert all(r + s == t for r, s, t in zip(fail_red, fail_blue, naive_host))
    assert not dominates(fail_red, RED2)
    assert not dominates(fail_blue, BLUE2)
    assert (fail_red, fail_blue) in count_avoiders(
        naive_host, RED2, BLUE2, independent=True
    )[1]
    assert count_avoiders(canonical, RED1, h, independent=True)[1] == []
    assert count_avoiders(canonical, RED2, BLUE2, independent=True)[1] == []
    assert not (h[0] == h[1])
    tied_h = (2, 2, 2, 1)
    assert tied_h.count(max(tied_h)) == 3
    print("B3_BOUNDARY_REPLAY_PASS",
          "naive12_not_joint", "canonical14_joint", "exact12to14_open")
    print("B2_UNIQUE_MAX_HYPOTHESIS_FALSE")


def check_unbounded_arithmetic():
    for b in (4, 5, 6, 17, 41, 100, 1000000):
        assert antidiagonal((3, 1, 1), (b, 2, 2, 1)) == (b, b, 3, 2, 1)
        assert b - 1 >= 3
        assert (b + 5) + b + 1 == 2 * b + 6
    print("B221_SYMBOLIC_BOUNDARY_INVARIANTS_PASS")


if __name__ == "__main__":
    check_main_family()
    check_boundary()
    check_unbounded_arithmetic()
    print("ERDOS561_B221_INFINITE_FAMILY_BOUNDED_REPLAY_PASS")
