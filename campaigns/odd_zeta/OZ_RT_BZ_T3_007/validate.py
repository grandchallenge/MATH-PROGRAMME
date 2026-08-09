#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from jsonschema import Draft202012Validator

HERE = Path(__file__).resolve().parent
R = json.loads((HERE / "OZ_RT_BZ_T3_007.json").read_text(encoding="utf-8"))
S = json.loads((HERE / "SEARCH_RESULT.json").read_text(encoding="utf-8"))
SC = json.loads((HERE / "OZ_RT_BZ_T3_007.schema.json").read_text(encoding="utf-8"))

CANONICAL_RESULT_SHA256 = "921564abff65b1cd8e42946be4d853c34680bf65cbbe0aa45211152c58f3c1ba"
BASIS_SHA256 = "cbdfe5798d360cb98f2d64743907a06ddc0612f88d17ef4bcef65c81c74e1438"
NORMALIZATION_SHA256 = "69738508f28433f9090f93621c8da3bc6b18279fd70941a31d07fb96b607700b"


def digest(v) -> str:
    return hashlib.sha256(json.dumps(v, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def errors(record=R, result=S):
    out = [f"schema{e.json_path}: {e.message}" for e in Draft202012Validator(SC).iter_errors(record)]
    a = record.get("authority", {})
    expected_authority = {
        "issue": 359,
        "predecessor_issue": 356,
        "predecessor_pr": 357,
        "predecessor_merge": "d9b9ed1a3a4c7ab56d25091e724fa585fbcea071",
        "predecessor_tree": "2a7bd5d53af76b6705ebd526dae667a381860374",
        "programme_base_commit": "d9b9ed1a3a4c7ab56d25091e724fa585fbcea071",
        "programme_base_tree": "2a7bd5d53af76b6705ebd526dae667a381860374",
    }
    for k, v in expected_authority.items():
        if a.get(k) != v:
            out.append(f"authority drift: {k}")
    if digest(result) != CANONICAL_RESULT_SHA256:
        out.append("canonical search-result digest drift")
    if record.get("artifacts", {}).get("search_result_sha256") != digest(result):
        out.append("record/result digest mismatch")
    if result.get("route") != "COUPLED_WEIGHT5_RAW_JET_ORDER3_4_SEARCH_001":
        out.append("route drift")
    if result.get("search_class", {}).get("orders") != [3, 4]:
        out.append("order drift")
    if result.get("search_class", {}).get("a_degree") != 2:
        out.append("a-degree drift")
    if result.get("search_class", {}).get("certificate_coefficient_degrees") != [0, 1, 2]:
        out.append("certificate-degree ladder drift")
    if result.get("certificate_denominator") != "(l+1)^3*(k+l+1)":
        out.append("certificate denominator drift")
    if result.get("basis", {}).get("basis_sha256") != BASIS_SHA256:
        out.append("raw-jet basis drift")
    if result.get("basis", {}).get("monomial_count") != 198:
        out.append("raw-jet basis cardinality drift")
    if result.get("basis", {}).get("one_body_only_count") != 158 or result.get("basis", {}).get("one_nested_atom_count") != 40:
        out.append("raw-jet basis cardinality drift")
    if not result.get("basis", {}).get("k_l_swap_invariant") or result.get("mirror_status") != "EXACTLY_EQUIVALENT_BY_K_L_SWAP":
        out.append("mirror-equivalence drift")
    norm = result.get("coordinate_normalization", {})
    if norm.get("monomial_multiplier_count") != 198:
        out.append("normalization cardinality drift")
    if norm.get("multiplier_vector_sha256") != NORMALIZATION_SHA256:
        out.append("normalization digest drift")
    if not norm.get("all_nonzero_integers") or not norm.get("all_nonzero_mod_prime"):
        out.append("normalization invertibility drift")
    if norm.get("rank_effect") != "INVERTIBLE_DIAGONAL_RESCALING_PRESERVES_RANK_OVER_Q_AND_MOD_P":
        out.append("normalization rank-boundary drift")
    if result.get("exact_target_cross_checks") != 135:
        out.append("target cross-lock contraction")
    o3 = result.get("order3_full_weight5_module", {}).get("stages", [])
    o4 = result.get("order4_full_weight5_module", {}).get("stages", [])
    if [(x.get("order"), x.get("q_coefficient_degree"), x.get("unknowns")) for x in o3] != [(3, 0, 222), (3, 1, 816), (3, 2, 2004)]:
        out.append("order-3 unknown-count drift")
    if [(x.get("order"), x.get("q_coefficient_degree"), x.get("unknowns")) for x in o4] != [(4, 0, 228), (4, 1, 822), (4, 2, 2010)]:
        out.append("order-4 unknown-count drift")
    if [x.get("full_grid_rows") for x in o3] != [273, 998, 2088]:
        out.append("order-3 sample-grid contraction")
    if [x.get("full_grid_rows") for x in o4] != [308, 880, 2240]:
        out.append("order-4 sample-grid contraction")
    if [x.get("rank_witness_rows") for x in o3] != [222, 816, 2004]:
        out.append("order-3 witness contraction")
    if [x.get("rank_witness_rows") for x in o4] != [228, 822, 2010]:
        out.append("order-4 witness contraction")
    if [x.get("certificate_unknowns") for x in o3] != [198, 792, 1980] or [x.get("certificate_unknowns") for x in o4] != [198, 792, 1980]:
        out.append("weight-five certificate-dimension drift")
    if any(x.get("rank") != x.get("unknowns") or x.get("nullity") != 0 for x in o3 + o4):
        out.append("weight-five module rank inflation/drift")
    if result.get("order3_full_weight5_module", {}).get("strongest_frontier") != "COUPLED_WEIGHT5_RAW_JET_ORDER3_ADEG_LE_2_QCOEFFDEG_LE_2":
        out.append("order-3 frontier drift")
    if result.get("order4_full_weight5_module", {}).get("strongest_frontier") != "COUPLED_WEIGHT5_RAW_JET_ORDER4_ADEG_LE_2_QCOEFFDEG_LE_2":
        out.append("order-4 frontier drift")
    if result.get("terminal") != "ORDER3_4_COMPLETE_WEIGHT5_MODULE_BOUNDED_CLASS_EXHAUSTED":
        out.append("terminal search classification drift")
    d = record.get("disposition", {})
    if d.get("status") != "OPEN_WITH_CHARACTERIZED_BLOCKER" or d.get("proof_effect") != "NONE" or d.get("promotion_effect") != "NONE":
        out.append("disposition inflation")
    if d.get("bounded_search_terminal") != "ORDER3_4_COMPLETE_WEIGHT5_MODULE_BOUNDED_CLASS_EXHAUSTED":
        out.append("bounded-search terminal drift")
    if d.get("proof_found") or d.get("counterexample_found") or not d.get("not_a_refutation"):
        out.append("proof/refutation inflation")
    if d.get("next_distinct_route") != "SYMMETRIC_2D_RAW_JET_DIVERGENCE_001":
        out.append("next-route drift")
    if d.get("alternative_route") != "T3_SEQUENCE_RECURRENCE_EXTRACTION_001":
        out.append("alternative-route drift")
    if any(record.get("nonclaims", {}).values()):
        out.append("nonclaim promoted")
    if result.get("proof_effect") != "NONE" or result.get("promotion_effect") != "NONE" or result.get("t3_status") != "OPEN_WITH_CHARACTERIZED_BLOCKER":
        out.append("result claim inflation")
    if result.get("next_distinct_routes") != ["SYMMETRIC_2D_RAW_JET_DIVERGENCE_001", "T3_SEQUENCE_RECURRENCE_EXTRACTION_001"]:
        out.append("result successor-route drift")
    return out


def main() -> int:
    e = errors()
    if e:
        print("\n".join(e), file=sys.stderr)
        return 1
    print("OZ-RT-BZ-T3-007 exact bounded order-3/4 raw-jet exhaustion package is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
