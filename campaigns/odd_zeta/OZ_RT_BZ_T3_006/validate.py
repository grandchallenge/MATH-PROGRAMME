#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from jsonschema import Draft202012Validator

HERE = Path(__file__).resolve().parent
R = json.loads((HERE / "OZ_RT_BZ_T3_006.json").read_text(encoding="utf-8"))
S = json.loads((HERE / "SEARCH_RESULT.json").read_text(encoding="utf-8"))
SC = json.loads((HERE / "OZ_RT_BZ_T3_006.schema.json").read_text(encoding="utf-8"))


def digest(v) -> str:
    return hashlib.sha256(json.dumps(v, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def errors(record=R, result=S):
    out = [f"schema{e.json_path}: {e.message}" for e in Draft202012Validator(SC).iter_errors(record)]
    a = record.get("authority", {})
    expected = {
        "issue": 356,
        "predecessor_issue": 341,
        "predecessor_pr": 344,
        "predecessor_merge": "e99defaabbc0d971e6299360ac03084e516c31c3",
        "predecessor_tree": "041b4f7afa647fec06d3303503b53fa0fc65350d",
        "programme_base_commit": "d2cdd1cfb57feb648bdd624a3362dae646a8b72f",
        "programme_base_tree": "3b7cc40fbf7f82cb1c219aef6b9733429e83e54f",
    }
    for k, v in expected.items():
        if a.get(k) != v:
            out.append(f"authority drift: {k}")
    if digest(result) != "c1a9fd34f2b54a1b6cda1908e68428fab8761c739e8478501dd3b8db9ec858b2":
        out.append("canonical search-result digest drift")
    if record.get("artifacts", {}).get("search_result_sha256") != digest(result):
        out.append("record/result digest mismatch")
    if result.get("certificate_denominator") != "(l+1)^3*(k+l+1)" or record.get("search", {}).get("certificate_denominator") != result.get("certificate_denominator"):
        out.append("certificate denominator drift")
    if result.get("basis", {}).get("basis_sha256") != "cbdfe5798d360cb98f2d64743907a06ddc0612f88d17ef4bcef65c81c74e1438":
        out.append("raw-jet basis drift")
    if result.get("basis", {}).get("monomial_count") != 198 or result.get("basis", {}).get("one_nested_atom_count") != 40 or result.get("basis", {}).get("one_body_only_count") != 158:
        out.append("raw-jet basis cardinality drift")
    if not result.get("basis", {}).get("k_l_swap_invariant") or result.get("mirror_status") != "EXACTLY_EQUIVALENT_BY_K_L_SWAP":
        out.append("mirror-equivalence drift")
    if result.get("exact_target_cross_checks") != 135:
        out.append("target cross-lock contraction")
    scalar = result.get("stage_a_scalar_envelope", {}).get("stages", [])
    if len(scalar) != 7 or [(x.get("a_degree"), x.get("q_degree")) for x in scalar] != [(d, d + 2) for d in range(7)]:
        out.append("scalar ladder drift")
    if [x.get("equations") for x in scalar] != [166, 166, 166, 166, 238, 328, 438]:
        out.append("scalar sample-grid contraction")
    if any(x.get("rank") != x.get("unknowns") or x.get("nullity") != 0 for x in scalar):
        out.append("scalar rank inflation/drift")
    module = result.get("stage_b_full_weight5_module", {}).get("stages", [])
    expected_module = [(0, 216), (1, 810), (2, 1998)]
    if [(x.get("q_coefficient_degree"), x.get("unknowns")) for x in module] != expected_module:
        out.append("weight-five module ladder drift")
    if [x.get("full_grid_rows") for x in module] != [328, 1118, 2278] or [x.get("rank_witness_rows") for x in module] != [216, 810, 1998]:
        out.append("weight-five sample-grid contraction")
    if [x.get("certificate_unknowns") for x in module] != [198, 792, 1980]:
        out.append("weight-five certificate-dimension drift")
    if any(x.get("rank") != x.get("unknowns") or x.get("nullity") != 0 for x in module):
        out.append("weight-five module rank inflation/drift")
    if result.get("stage_b_full_weight5_module", {}).get("strongest_frontier") != "COUPLED_WEIGHT5_RAW_JET_ORDER2_ADEG_LE_2_QCOEFFDEG_LE_2":
        out.append("strongest frontier drift")
    if result.get("terminal") != "ORDER2_COMPLETE_WEIGHT5_MODULE_BOUNDED_CLASS_EXHAUSTED":
        out.append("terminal search classification drift")
    d = record.get("disposition", {})
    if d.get("status") != "OPEN_WITH_CHARACTERIZED_BLOCKER" or d.get("proof_effect") != "NONE" or d.get("promotion_effect") != "NONE":
        out.append("disposition inflation")
    if d.get("proof_found") or d.get("counterexample_found") or not d.get("not_a_refutation"):
        out.append("proof/refutation inflation")
    if d.get("next_distinct_route") != "COUPLED_WEIGHT5_RAW_JET_ORDER3_4_SEARCH_001":
        out.append("next-route drift")
    if any(record.get("nonclaims", {}).values()):
        out.append("nonclaim promoted")
    if result.get("proof_effect") != "NONE" or result.get("promotion_effect") != "NONE" or result.get("t3_status") != "OPEN_WITH_CHARACTERIZED_BLOCKER":
        out.append("result claim inflation")
    return out


def main() -> int:
    e = errors()
    if e:
        print("\n".join(e), file=sys.stderr)
        return 1
    print("OZ-RT-BZ-T3-006 exact bounded order-2 raw-jet exhaustion package is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
