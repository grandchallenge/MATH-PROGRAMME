from __future__ import annotations

import importlib.util
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
PRED_DIR = HERE.parent / "OZ_RT_BZ_T3_015_A"


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot load protected predecessor: {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


pred15 = _load(PRED_DIR / "producer.py", "oz_t3_015_a_for_015_b")

ISSUE = 958
OPERATION = "OZ-RT-BZ-T3-015-B"
STAGE = "T3_015_B_COMPLETE_RATIONAL_SOLVER_STRUCTURAL_REDUCTION"
CLASS = "SOURCE_DECLARED_RATIONAL_DELTA_COEFFICIENT_CLASS_001"
PROTECTED_BASE = "a4eec4259ae6f7e12028cae1384a17ba865926e4"
PREDECESSOR_TERMINAL = "GLOBAL_RATIONAL_DELTA_DIFFERENCE_MODULE_EXTRACTED__COMPLETE_RATIONAL_SOLVER_REQUIRED"
PREDECESSOR_MODULE_SHA256 = "cdabf6d7873f3aa8e9d53b39fd7b15341dbee58ce9684911d015aee9aaae04da"
TERMINAL = "GLOBAL_RATIONAL_DELTA_SOLVER_STRUCTURE_EXTRACTED__COMPLETE_RATIONAL_SOLVER_REQUIRED"
SCALARS = ("TN1", "TN2", "TN3", "SK", "AK", "LKK", "LLK")
EXPECTED_SHIFTS = {(1, 0, 0), (2, 0, 0), (3, 0, 0), (0, 1, 0)}


def _mon(row):
    return tuple(row["monomial"])


def _analyse(module: dict) -> dict:
    if module["hypothesis_class"] != CLASS:
        raise AssertionError("protected rational coefficient class drift")
    if module["scalar_namespace"] != list(SCALARS):
        raise AssertionError("protected scalar namespace drift")

    generators = module["generators"]
    targets = module["target_records"]
    if len(generators) != 506 or len(targets) != 513:
        raise AssertionError("protected module count drift")

    by_scalar_g = defaultdict(list)
    by_scalar_t = defaultdict(list)
    all_shifts = set()
    degree_edges = []
    nonself_edges = set()
    lowering_violations = []

    for g in generators:
        scalar = g["scalar"]
        if scalar not in SCALARS:
            raise AssertionError(f"unknown generator scalar: {scalar}")
        by_scalar_g[scalar].append(g)
        src = tuple(g["support_monomial"])
        shift = tuple(g["shift"])
        all_shifts.add(shift)
        for term in g["shifted_terms"]:
            dst = tuple(term["monomial"])
            if dst == src:
                continue
            nonself_edges.add((src, dst))
            degree_edges.append((len(src), len(dst)))
            if len(dst) >= len(src):
                lowering_violations.append(
                    {
                        "channel": g["channel"],
                        "scalar": scalar,
                        "source": list(src),
                        "target": list(dst),
                    }
                )

    for row in targets:
        scalar = row["scalar"]
        if scalar not in SCALARS:
            raise AssertionError(f"unknown target scalar: {scalar}")
        by_scalar_t[scalar].append(row)

    if all_shifts != EXPECTED_SHIFTS:
        raise AssertionError(f"protected shift set drift: {sorted(all_shifts)}")

    scalar_reports = {}
    for scalar in SCALARS:
        gs = by_scalar_g[scalar]
        ts = by_scalar_t[scalar]
        support_channels = defaultdict(set)
        channel_counts = Counter()
        shift_counts = Counter()
        support_degree_counts = Counter()
        target_degree_counts = Counter()

        for g in gs:
            support = tuple(g["support_monomial"])
            support_channels[support].add(g["channel"])
            channel_counts[g["channel"]] += 1
            shift_counts[tuple(g["shift"])] += 1
            support_degree_counts[len(support)] += 1

        target_monomials = {tuple(row["monomial"]) for row in ts}
        for mon in target_monomials:
            target_degree_counts[len(mon)] += 1
        uncovered = sorted(target_monomials - set(support_channels), key=repr)
        covered = target_monomials & set(support_channels)
        multi_channel = sum(1 for channels in support_channels.values() if len(channels) > 1)

        scalar_reports[scalar] = {
            "generator_count": len(gs),
            "target_record_count": len(ts),
            "support_monomial_count": len(support_channels),
            "target_monomial_count": len(target_monomials),
            "covered_target_monomial_count": len(covered),
            "uncovered_target_monomial_count": len(uncovered),
            "uncovered_target_monomials": [list(mon) for mon in uncovered],
            "multi_channel_support_count": multi_channel,
            "single_channel_support_count": len(support_channels) - multi_channel,
            "channel_counts": dict(sorted(channel_counts.items())),
            "shift_counts": {
                str(list(shift)): count
                for shift, count in sorted(shift_counts.items(), key=lambda item: item[0])
            },
            "support_degree_counts": {
                str(k): v for k, v in sorted(support_degree_counts.items())
            },
            "target_degree_counts": {
                str(k): v for k, v in sorted(target_degree_counts.items())
            },
        }

    source_nodes = {edge[0] for edge in nonself_edges}
    sink_nodes = {edge[1] for edge in nonself_edges}
    max_degree = max((len(mon) for mon in module["coordinate_monomials"]), default=0)

    return {
        "module_sha256": PREDECESSOR_MODULE_SHA256,
        "scalar_partition_exact": set(by_scalar_g) == set(SCALARS) and set(by_scalar_t) == set(SCALARS),
        "shift_directions": [list(x) for x in sorted(all_shifts)],
        "l_shift_present": any(shift[2] != 0 for shift in all_shifts),
        "nonself_dependency_edge_count": len(nonself_edges),
        "dependency_source_node_count": len(source_nodes),
        "dependency_sink_node_count": len(sink_nodes),
        "max_monomial_degree": max_degree,
        "strict_degree_lowering": not lowering_violations,
        "degree_lowering_violations": lowering_violations,
        "scalar_reports": scalar_reports,
    }


def build_with_module() -> tuple[dict, dict]:
    predecessor = pred15.build()
    if predecessor["module_sha256"] != PREDECESSOR_MODULE_SHA256:
        raise AssertionError("T3-015-A module digest drift")
    if predecessor["terminal"] != PREDECESSOR_TERMINAL:
        raise AssertionError("T3-015-A terminal drift")

    module = predecessor["module"]
    structure = _analyse(module)
    if not structure["scalar_partition_exact"]:
        raise AssertionError("protected scalar-family partition is incomplete")
    if not structure["strict_degree_lowering"]:
        raise AssertionError("protected non-self shift graph is not degree-lowering")
    if structure["l_shift_present"]:
        raise AssertionError("unexpected l-shift channel in protected module")

    evidence = {
        "schema_version": "1.0.0",
        "issue": ISSUE,
        "operation": OPERATION,
        "stage": STAGE,
        "protected_base": PROTECTED_BASE,
        "hypothesis_class": CLASS,
        "predecessor_module_sha256": predecessor["module_sha256"],
        "structure": structure,
        "terminal": TERMINAL,
        "global_certificate_constructed": False,
        "residual_sum_zero_proved": False,
        "proof_effect": "NONE",
        "promotion_effect": "NONE",
        "t3_status": "OPEN_WITH_CHARACTERIZED_BLOCKER",
    }
    return evidence, module


def build() -> dict:
    evidence, _module = build_with_module()
    return evidence


def compact_result(evidence: dict) -> dict:
    return {
        "module_sha256": evidence["predecessor_module_sha256"],
        "shift_directions": evidence["structure"]["shift_directions"],
        "l_shift_present": evidence["structure"]["l_shift_present"],
        "strict_degree_lowering": evidence["structure"]["strict_degree_lowering"],
        "nonself_dependency_edge_count": evidence["structure"]["nonself_dependency_edge_count"],
        "max_monomial_degree": evidence["structure"]["max_monomial_degree"],
        "scalar_reports": evidence["structure"]["scalar_reports"],
        "terminal": evidence["terminal"],
    }


if __name__ == "__main__":
    print("T3_015_B_STRUCTURE " + json.dumps(compact_result(build()), sort_keys=True))
