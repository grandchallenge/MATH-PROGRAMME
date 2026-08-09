#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
LOCK = HERE / "RECURRENCE_LOCK.json"
BASELINE = HERE / "BASELINE_RESULT.json"

EXPECTED_A0 = "41218*n^3+198849*n^2+320790*n+173057"
EXPECTED_C3 = "2*(n+3)^5*(2*n+5)*a0(n)"


def validate() -> None:
    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    result = json.loads(BASELINE.read_text(encoding="utf-8"))
    if lock["operation"] != "OZ-RT-BZ-T3-009" or result["operation"] != "OZ-RT-BZ-T3-009":
        raise AssertionError("operation drift")
    if lock["route"] != "T3_SEQUENCE_RECURRENCE_EXTRACTION_001" or result["route"] != lock["route"]:
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
    if result["moving_support"]["uniform_support_proof_complete"]:
        raise AssertionError("moving-support proof inflated")
    if result["source_artifact_audit"]["RFD_ann.m"]["relevance"] != "NOT_A_T3_CERTIFICATE":
        raise AssertionError("middle-row checkpoint promoted into T3")
    if result["proof_effect"] != "NONE" or result["promotion_effect"] != "NONE":
        raise AssertionError("proof or promotion inflation")
    if result["t3_status"] != "OPEN_WITH_CHARACTERIZED_BLOCKER":
        raise AssertionError("T3 status inflation")
    if result["terminal"] != "RECURRENCE_INTERFACE_LOCKED_FINITE_COMPONENT_BASELINE_REPLAYED":
        raise AssertionError("baseline terminal drift")


def main() -> int:
    validate()
    print("OZ-RT-BZ-T3-009 recurrence lock and finite baseline package is valid")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
