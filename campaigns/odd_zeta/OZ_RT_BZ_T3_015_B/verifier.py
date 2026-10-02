from __future__ import annotations

import importlib.util
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
PRED_DIR = HERE.parent / "OZ_RT_BZ_T3_015_A"


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot load protected verifier predecessor: {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


pred15v = _load(PRED_DIR / "verifier.py", "oz_t3_015_a_verifier_for_015_b")

CLASS = "SOURCE_DECLARED_RATIONAL_DELTA_COEFFICIENT_CLASS_001"
PROTECTED_BASE = "a4eec4259ae6f7e12028cae1384a17ba865926e4"
PREDECESSOR_MODULE_SHA256 = "cdabf6d7873f3aa8e9d53b39fd7b15341dbee58ce9684911d015aee9aaae04da"
TERMINAL = "GLOBAL_RATIONAL_DELTA_SOLVER_STRUCTURE_EXTRACTED__COMPLETE_RATIONAL_SOLVER_REQUIRED"
SCALARS = ("TN1", "TN2", "TN3", "SK", "AK", "LKK", "LLK")
EXPECTED_SHIFTS = {(1, 0, 0), (2, 0, 0), (3, 0, 0), (0, 1, 0)}


def _independent_structure(module: dict) -> dict:
    by_g = defaultdict(list)
    by_t = defaultdict(list)
    shifts = set()
    edges = set()
    violations = []

    for g in reversed(module["generators"]):
        scalar = g["scalar"]
        by_g[scalar].append(g)
        src = tuple(g["support_monomial"])
        shift = tuple(g["shift"])
        shifts.add(shift)
        for term in reversed(g["shifted_terms"]):
            dst = tuple(term["monomial"])
            if dst == src:
                continue
            edges.add((src, dst))
            if len(dst) >= len(src):
                violations.append((scalar, g["channel"], src, dst))

    for row in reversed(module["target_records"]):
        by_t[row["scalar"]].append(row)

    reports = {}
    for scalar in SCALARS:
        support_channels = defaultdict(set)
        channel_counts = Counter()
        shift_counts = Counter()
        support_degrees = Counter()
        target_degrees = Counter()
        for g in reversed(by_g[scalar]):
            mon = tuple(g["support_monomial"])
            support_channels[mon].add(g["channel"])
            channel_counts[g["channel"]] += 1
            shift_counts[tuple(g["shift"])] += 1
            support_degrees[len(mon)] += 1
        target_mons = {tuple(row["monomial"]) for row in by_t[scalar]}
        for mon in target_mons:
            target_degrees[len(mon)] += 1
        uncovered = sorted(target_mons.difference(support_channels), key=repr)
        multi = sum(len(channels) > 1 for channels in support_channels.values())
        reports[scalar] = {
            "generator_count": len(by_g[scalar]),
            "target_record_count": len(by_t[scalar]),
            "support_monomial_count": len(support_channels),
            "target_monomial_count": len(target_mons),
            "covered_target_monomial_count": len(target_mons.intersection(support_channels)),
            "uncovered_target_monomial_count": len(uncovered),
            "uncovered_target_monomials": [list(mon) for mon in uncovered],
            "multi_channel_support_count": multi,
            "single_channel_support_count": len(support_channels) - multi,
            "channel_counts": dict(sorted(channel_counts.items())),
            "shift_counts": {
                str(list(k)): v for k, v in sorted(shift_counts.items(), key=lambda item: item[0])
            },
            "support_degree_counts": {str(k): v for k, v in sorted(support_degrees.items())},
            "target_degree_counts": {str(k): v for k, v in sorted(target_degrees.items())},
        }

    coordinates = [tuple(mon) for mon in module["coordinate_monomials"]]
    return {
        "module_sha256": PREDECESSOR_MODULE_SHA256,
        "scalar_partition_exact": set(by_g) == set(SCALARS) and set(by_t) == set(SCALARS),
        "shift_directions": [list(x) for x in sorted(shifts)],
        "l_shift_present": any(x[2] != 0 for x in shifts),
        "nonself_dependency_edge_count": len(edges),
        "dependency_source_node_count": len({a for a, _ in edges}),
        "dependency_sink_node_count": len({b for _, b in edges}),
        "max_monomial_degree": max((len(mon) for mon in coordinates), default=0),
        "strict_degree_lowering": not violations,
        "degree_lowering_violations": [
            {"scalar": scalar, "channel": channel, "source": list(src), "target": list(dst)}
            for scalar, channel, src, dst in violations
        ],
        "scalar_reports": reports,
    }


def verify(evidence: dict) -> dict:
    reconstructed = pred15v.reconstruct_module()
    if reconstructed["module_sha256"] != PREDECESSOR_MODULE_SHA256:
        raise AssertionError("independent T3-015-A module digest drift")
    structure = _independent_structure(reconstructed["module"])
    if evidence["predecessor_module_sha256"] != reconstructed["module_sha256"]:
        raise AssertionError("producer predecessor digest mismatch")
    if evidence["structure"] != structure:
        raise AssertionError("independent structural solver reduction mismatch")
    if evidence["protected_base"] != PROTECTED_BASE:
        raise AssertionError("protected base drift")
    if evidence["terminal"] != TERMINAL:
        raise AssertionError("terminal drift")
    if evidence["global_certificate_constructed"] or evidence["residual_sum_zero_proved"]:
        raise AssertionError("claim firewall violated")
    if evidence["proof_effect"] != "NONE" or evidence["promotion_effect"] != "NONE":
        raise AssertionError("claim effect drift")
    if evidence["t3_status"] != "OPEN_WITH_CHARACTERIZED_BLOCKER":
        raise AssertionError("T3 status drift")
    if set(tuple(x) for x in structure["shift_directions"]) != EXPECTED_SHIFTS:
        raise AssertionError("shift-direction drift")
    if structure["l_shift_present"] or not structure["strict_degree_lowering"]:
        raise AssertionError("solver structure is not the expected triangular n/k-shift module")
    return {
        "independent_structure_replay_complete": True,
        "producer_structure_imported_as_authority": False,
        "module_sha256": reconstructed["module_sha256"],
        "shift_directions": structure["shift_directions"],
        "strict_degree_lowering": structure["strict_degree_lowering"],
        "scalar_reports": structure["scalar_reports"],
        "terminal": TERMINAL,
    }
