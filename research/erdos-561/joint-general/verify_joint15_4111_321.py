#!/usr/bin/env python3
"""Independent finite upper-host and five-core checks; not a universal graph proof."""
import argparse
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
HOST = (5, 4, 3, 2, 1)
R1, B1 = (1, 1, 1), (3, 2, 1)
R2, B2 = (4, 1, 1, 1), (2, 1)


def direct_assignment(caps, needs):
    """Independent permutation-based disjoint-host-component assignment."""
    for p in itertools.permutations(range(len(caps)), len(needs)):
        if all(caps[p[i]] >= need for i, need in enumerate(needs)):
            return True
    return False


def dynamic_assignment(caps, needs):
    """Different implementation: bitmask dynamic programming over host components."""
    reachable = {0}
    full = (1 << len(needs)) - 1
    for cap in caps:
        nxt = set(reachable)
        for covered in reachable:
            for j, need in enumerate(needs):
                if not (covered & (1 << j)) and cap >= need:
                    nxt.add(covered | (1 << j))
        reachable = nxt
    return full in reachable


def core_patterns():
    edges = list(itertools.combinations(range(5), 2))
    by_q = {}
    for q in range(1, 5):
        count = 0
        for missing in itertools.combinations(edges, q):
            degrees = [sum(v in e for e in missing) for v in range(5)]
            x = max(range(5), key=lambda v: degrees[v])
            assert degrees[x] >= 1
            left = [v for v in range(5) if v != x]
            remaining_missing = {tuple(sorted(e)) for e in missing if x not in e}
            assert len(remaining_missing) <= 2
            matchings = [
                ((left[0], left[1]), (left[2], left[3])),
                ((left[0], left[2]), (left[1], left[3])),
                ((left[0], left[3]), (left[1], left[2])),
            ]
            assert any(all(tuple(sorted(e)) not in remaining_missing for e in m)
                       for m in matchings)
            count += 1
        assert count == (10, 45, 120, 210)[q - 1]
        by_q[str(q)] = count
    assert sum(by_q.values()) == 385
    return by_q


def verify():
    weights = {}
    n, m = (4, 1, 1, 1), (3, 2, 1)
    for k in range(2, len(n) + len(m) + 1):
        weights[k] = max(a + b - 1 for i, a in enumerate(n, start=1)
                         for j, b in enumerate(m, start=1) if i + j == k)
    assert tuple(weights.values()) == (6, 5, 4, 3, 2, 1)
    assert sum(weights.values()) == 21
    assert sum(weights[k] for k in range(3, 8)) == 15

    total_allocations = 0
    for red in itertools.product(*(range(h + 1) for h in HOST)):
        blue = tuple(h - r for h, r in zip(HOST, red))
        assert direct_assignment(red, R1) or direct_assignment(blue, B1)
        assert direct_assignment(red, R2) or direct_assignment(blue, B2)
        total_allocations += 1
    assert total_allocations == 720

    # All actual 15-edge masks; no reduction to one mask per arm-count vector.
    total_masks = 0
    for mask in range(1 << sum(HOST)):
        red = []
        pos = 0
        for h in HOST:
            red.append(((mask >> pos) & ((1 << h) - 1)).bit_count())
            pos += h
        blue = tuple(h - r for h, r in zip(HOST, red))
        assert dynamic_assignment(red, R1) or dynamic_assignment(blue, B1)
        assert dynamic_assignment(red, R2) or dynamic_assignment(blue, B2)
        total_masks += 1
    assert total_masks == 32768

    core = core_patterns()
    return {
        "disposition": "BOUNDED_CHECKED_PAPER_THEOREM_UNDER_REVIEW",
        "original_red": list(n),
        "original_blue": list(m),
        "original_antidiagonal_weights": list(weights.values()),
        "canonical_original_edges": 21,
        "joint_tail_edges": 15,
        "separate_residual_lower_bounds": [12, 14],
        "switching_surplus": 1,
        "upper_host_star_edges": list(HOST),
        "upper_allocation_vectors": total_allocations,
        "upper_actual_edge_colouring_masks": total_masks,
        "maximum_degree_four_missing_core_patterns_by_q": core,
        "missing_core_pattern_total": sum(core.values()),
        "full_unrestricted_conjecture_status": "OPEN",
        "mathematical_certification": "NOT_ISSUED",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-evidence", action="store_true")
    args = parser.parse_args()
    actual = verify()
    out = HERE / "JOINT_4111_321_MATCHING_CORE_EVIDENCE.json"
    payload = json.dumps(actual, indent=2, ensure_ascii=False) + "\n"
    if args.write_evidence:
        out.write_text(payload)
    else:
        assert out.read_text() == payload, "evidence bytes differ from deterministic replay"
    print("ERDOS561_JOINT_4111_321_PASS allocations=720 masks=32768 core_patterns=385")
