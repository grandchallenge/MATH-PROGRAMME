#!/usr/bin/env python3
"""Fail-closed validator for OZ-RT-SHARP12-T1TOP-001."""
from __future__ import annotations
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RECORD = ROOT / "OZ_RT_SHARP12_T1TOP_001.json"
EXPECTED_MISSING = {
    "T1-PRODUCER-001", "T1-TELESCOPER-001", "T1-CERTIFICATE-001",
    "T1-SINGULARITY-001", "T1-BOUNDARY-001", "T1-RECURRENCE-COMPARE-001",
    "T1-INITIAL-001", "T1-VERIFIER-001"
}
EXPECTED_REOPEN = {f"T1-REOPEN-0{i}" for i in range(1, 8)}

class ValidationError(RuntimeError):
    pass

def reject(message: str) -> None:
    raise ValidationError(message)

def load() -> dict:
    return json.loads(RECORD.read_text(encoding="utf-8"))

def validate(d: dict) -> None:
    if d.get("$schema") != "OZ_RT_SHARP12_T1TOP_001.schema.json": reject("schema drift")
    if d.get("record_id") != "OZ-RT-SHARP12-T1TOP-001" or d.get("programme_issue") != 306: reject("record identity drift")
    a = d.get("authority", {})
    if a.get("source_commit") != "790685b7ee4f642a8a88a1bd120636d1b8b39ea8": reject("source commit drift")
    if a.get("source_tree") != "646ee73dd9066e059b043fad64fb20959f111cbf": reject("source tree drift")
    if a.get("sharp12_blob") != "6a347e2a483ec781afac98016635ce1d73b3c38e": reject("Sharp-12 blob drift")
    if a.get("later_source_head_audited") != "6cc0bf07137815ceeef0d9f340559f85352391e5" or a.get("later_source_changes_target_locus") is not False: reject("later source reconciliation drift")
    t = d.get("target_lock", {})
    if t.get("label") != "T1-top" or t.get("representative") != "w5_I": reject("target representative drift")
    if "for every integer n >= 0" != t.get("quantifier"): reject("quantifier drift")
    if d.get("terminal_disposition") != "OPEN_WITH_CHARACTERIZED_BLOCKER": reject("terminal disposition drift")
    if d.get("proof_effect") != "NONE" or d.get("promotion_effect") != "NONE": reject("claim promotion")
    s = d.get("certificate_search", {})
    if s.get("result") != "UNBOUNDED_T1TOP_CERTIFICATE_NOT_PRESENT_IN_GOVERNED_SOURCE": reject("certificate-search result drift")
    for key in ("proof_certificate_present","counterexample_present","deterministic_t1_producer_present","independent_verifier_input_present","finite_evidence_is_proof","t3_is_substitute","later_delta_supplies_certificate"):
        if s.get(key) is not False: reject(f"unsupported certificate assertion: {key}")
    missing = d.get("missing_objects", [])
    if {x.get("id") for x in missing} != EXPECTED_MISSING or len(missing) != 8: reject("missing-object ledger incomplete")
    if any(x.get("state") != "ABSENT" for x in missing): reject("missing certificate object falsely promoted")
    rr = d.get("reopening_requirements", [])
    if {x.get("id") for x in rr} != EXPECTED_REOPEN or len(rr) != 7: reject("reopening requirements incomplete")
    evidence = d.get("source_evidence", [])
    if len(evidence) < 7: reject("source evidence incomplete")
    if not any(x.get("id") == "T1-EVIDENCE-004" and x.get("classification") == "CHARACTERIZED_COMPUTATIONAL_WALL" for x in evidence): reject("missing weight-5 computational wall")
    nc = d.get("nonclaims", {})
    for k, v in nc.items():
        if v is not False: reject(f"nonclaim violated: {k}")

def main() -> int:
    validate(load())
    print("OZ-RT-SHARP12-T1TOP-001 validation: OK")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
