#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
LOCK = HERE / "RECURRENCE_LOCK.json"
BASELINE = HERE / "BASELINE_RESULT.json"
SEARCH = HERE / "SEARCH_RESULT.json"

EXPECTED_A0 = "41218*n^3+198849*n^2+320790*n+173057"
EXPECTED_C3 = "2*(n+3)^5*(2*n+5)*a0(n)"
EXPECTED_RANKS = [(198,199),(792,793),(1980,1981)]


def validate() -> None:
    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    result = json.loads(BASELINE.read_text(encoding="utf-8"))
    search = json.loads(SEARCH.read_text(encoding="utf-8"))
    if any(x["operation"] != "OZ-RT-BZ-T3-009" for x in (lock,result,search)):
        raise AssertionError("operation drift")
    if any(x["route"] != "T3_SEQUENCE_RECURRENCE_EXTRACTION_001" for x in (lock,result,search)):
        raise AssertionError("route drift")
    if lock["a0"] != EXPECTED_A0 or lock["coefficients"]["c3"] != EXPECTED_C3:
        raise AssertionError("locked forward recurrence coefficient drift")
    if lock["source"]["commit"] != "968477ed7e406df6542f8da6fbe1cd6ca7273c47":
        raise AssertionError("upstream recurrence source drift")
    if lock["source"]["programme_lock"] != "campaigns/odd_zeta/OZ_RT_BZ_T3_001/OZ_RT_BZ_T3_001.json":
        raise AssertionError("Programme recurrence authority drift")
    if result["execution_intake"]["protected_head"] != "fa283a283c4584c79af86fec632d50aa49e6d640":
        raise AssertionError("protected intake head drift")
    if result["execution_intake"]["protected_tree"] != "49f644c8ff4462015833d6477dfb6fde5b847970":
        raise AssertionError("protected intake tree drift")
    rows = result["finite_component_baseline"]
    if [x["n"] for x in rows] != list(range(7)):
        raise AssertionError("finite component range drift")
    if rows[1]["P5"] != [87,4] or rows[1]["W"] != [-87,2]:
        raise AssertionError("nonvacuity witness drift")
    if any(x["D"] != [0,1] for x in rows):
        raise AssertionError("finite target baseline drift")
    residuals = result["finite_residual_baseline"]
    if [x["n"] for x in residuals] != list(range(4)):
        raise AssertionError("finite recurrence range drift")
    if any(x[key] != [0,1] for x in residuals for key in ("L_P5","L_W","L_D")):
        raise AssertionError("finite recurrence residual drift")
    nv = result["nonvacuity"]
    if not nv["scalar_D_recurrence_fitting_forbidden"] or nv["finite_residuals_are_proof"]:
        raise AssertionError("vacuity/proof firewall drift")
    ms = result["moving_support"]
    if not ms["uniform_support_proof_complete"] or ms["shell_omission"]:
        raise AssertionError("moving-support zero-extension certificate drift")
    if search["common_support"]["square"] != ms["common_square"]:
        raise AssertionError("search/support square drift")
    if not search["common_support"]["uniform_zero_extension_lemma"] or search["common_support"]["shell_omission"]:
        raise AssertionError("search support firewall drift")
    if search["flux"]["basis_monomials"] != 198 or search["flux"]["basis_sha256"] != "cbdfe5798d360cb98f2d64743907a06ddc0612f88d17ef4bcef65c81c74e1438":
        raise AssertionError("protected raw-jet basis drift")
    if search["flux"]["coefficient_total_degrees"] != [0,1,2]:
        raise AssertionError("bounded degree ladder drift")
    if search["denominator_condition"]["max_harmonic_argument_on_strongest_grid"] != 63:
        raise AssertionError("harmonic denominator-bound drift")
    if search["denominator_condition"]["max_flux_linear_factor"] != 43:
        raise AssertionError("flux denominator-bound drift")
    for kind in ("D","P5","W"):
        stages=search["target_results"][kind]["stages"]
        if [(x["coefficient_rank"],x["augmented_rank"]) for x in stages] != EXPECTED_RANKS:
            raise AssertionError(f"bounded recurrence-rank drift: {kind}")
        if any(x["classification"] != "EXACT_AFFINE_INCONSISTENCY" for x in stages):
            raise AssertionError(f"bounded recurrence classification drift: {kind}")
    if search["bounded_terminal"] != "LOCKED_LBZ_NPLUS3_SYMMETRIC_RAW_JET_DIVERGENCE_DEG_LE_2_EXHAUSTED_FOR_D_P5_W":
        raise AssertionError("bounded recurrence terminal drift")
    if result["source_artifact_audit"]["RFD_ann.m"]["relevance"] != "NOT_A_T3_CERTIFICATE":
        raise AssertionError("middle-row checkpoint promoted into T3")
    if any(x["proof_effect"] != "NONE" or x["promotion_effect"] != "NONE" for x in (result,search)):
        raise AssertionError("proof or promotion inflation")
    if result["t3_status"] != "OPEN_WITH_CHARACTERIZED_BLOCKER" or search["t3_status"] != result["t3_status"]:
        raise AssertionError("T3 status inflation")
    if result["terminal"] != "RECURRENCE_INTERFACE_LOCKED_NONVACUOUS_BASELINE_AND_MOVING_SUPPORT_CERTIFIED":
        raise AssertionError("baseline terminal drift")


def main() -> int:
    validate()
    print("OZ-RT-BZ-T3-009 locked recurrence, support, and bounded negative package is valid")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
