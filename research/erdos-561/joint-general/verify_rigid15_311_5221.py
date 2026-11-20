#!/usr/bin/env python3
"""Exact bounded star-host allocation replay for restricted Erdős 561."""
from itertools import permutations, product

RESIDUALS = (((1, 1), (5, 2, 2, 1)),
             ((3, 1, 1), (2, 2, 1)))
LOWER = (5, 5, 2, 2, 1)
UPPER = (5, 5, 3, 2, 1)


def contains_forest(host_arm_counts, target):
    """Injectively assign every required star to a distinct host centre."""
    return any(
        all(host_arm_counts[i] >= requested for i, requested in zip(choice, target))
        for choice in permutations(range(len(host_arm_counts)), len(target))
    )


def enumerate_allocations(host, red_target, blue_target):
    bad = []
    total = 0
    for red in product(*(range(size + 1) for size in host)):
        blue = tuple(size - red_count for size, red_count in zip(host, red))
        total += 1
        if not contains_forest(red, red_target) and not contains_forest(blue, blue_target):
            bad.append((red, blue))
    return total, bad


def main():
    n, m = (3, 1, 1), (5, 2, 2, 1)
    antidiagonal = tuple(
        max(n[i - 1] + m[k - i - 1] - 1
            for i in range(1, len(n) + 1) if 1 <= k - i <= len(m))
        for k in range(3, len(n) + len(m) + 1)
    )
    assert antidiagonal == UPPER
    assert sum(UPPER) == 16 and sum(LOWER) == 15

    for name, host in (("upper", UPPER), ("forced_lower", LOWER)):
        for number, (red_target, blue_target) in enumerate(RESIDUALS, 1):
            total, bad = enumerate_allocations(host, red_target, blue_target)
            if name == "upper" or number == 1:
                assert not bad, (name, number, bad[:2])
            else:
                assert len(bad) == 9, len(bad)
                witness = ((2, 2, 2, 2, 1), (3, 3, 0, 0, 0))
                assert witness in bad
                assert not contains_forest(witness[0], red_target)
                assert not contains_forest(witness[1], blue_target)
            print("EXACT", name, "residual", number,
                  "allocations", total, "avoiding", len(bad))
    print("ERDOS561_311_5221_RESTRICTED_16_EDGE_REPLAY_PASS")


if __name__ == "__main__":
    main()
