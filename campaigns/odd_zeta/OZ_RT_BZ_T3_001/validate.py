#!/usr/bin/env python3
from __future__ import annotations
import json
import sys
from pathlib import Path
from jsonschema import Draft202012Validator

PKG = Path(__file__).resolve().parent
RECORD = PKG / "OZ_RT_BZ_T3_001.json"
SCHEMA = PKG / "OZ_RT_BZ_T3_001.schema.json"

def load_record():
    return json.loads(RECORD.read_text(encoding="utf-8"))

def errors(record=None) -> list[str]:
    out: list[str] = []
    record = load_record() if record is None else record
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    for err in Draft202012Validator(schema).iter_errors(record):
        out.append(f"schema{err.json_path}: {err.message}")

    target = record.get("target_lock", {})
    finite = record.get("finite_evidence", {})
    failed = record.get("failed_route_ledger", {})
    resources = record.get("resource_ledger", {})
    cert = record.get("certificate_status", {})
    disposition = record.get("disposition", {})

    source = target.get("source", {})
    expected = {
        "commit": "968477ed7e406df6542f8da6fbe1cd6ca7273c47",
        "statement_blob": "da46db62471fbed81d861772c1d2d03d80782e23",
        "bridge_blob": "002c96d28123e5949c38656f26677ae5a723ee93",
        "finite_verifier_blob": "be458d969e1f8c989c8007a2b181506f84fd7f48",
        "recurrence_blob": "9495275bc31e5a8f535c68f027f3b24d12c07ae1",
    }
    for key, value in expected.items():
        if source.get(key) != value:
            out.append(f"source identity drift: {key}")

    identity = target.get("identity", {})
    if identity.get("label") != "T3":
        out.append("target label drift")
    if identity.get("quantifier") != "for every integer n >= 0":
        out.append("uniform quantifier missing")
    if "W1(k,l)+2*w5_sym(n,k,l)" not in identity.get("normalized_zero_form", ""):
        out.append("normalized zero form drift")
    if target.get("domain", {}).get("endpoints") != "all four boundary edges and corners are included":
        out.append("endpoint lock missing")

    replay = finite.get("source_replay", {})
    if replay.get("exact_sum_range") != {"n_min": 0, "n_max": 34}:
        out.append("finite exact-sum range drift")
    if replay.get("recurrence_residual_range") != {"n_min": 0, "n_max": 31}:
        out.append("finite recurrence range drift")
    if finite.get("theorem_effect") != "NONE":
        out.append("finite evidence inflated")
    if finite.get("finite_agreement_is_proof") is not False:
        out.append("finite agreement promoted")
    if finite.get("finite_recurrence_residual_is_proof") is not False:
        out.append("finite recurrence promoted")

    routes = {row["id"]: row for row in failed.get("routes", [])}
    required = {
        "LOCAL_RESIDUE_LIVE1", "WEIGHTED_TOWERS_LIVE2",
        "EXTENDED_FIXED_LETTER_LIVE3", "RATIONAL_N_DEG2",
        "XY_JETS", "MOMENT_TOWERS", "DELTA_CERTIFICATE",
    }
    if set(routes) != required:
        out.append("failed-route ledger incomplete")
    if routes.get("DELTA_CERTIFICATE", {}).get("result") != "NO_CERTIFICATE_PRODUCED":
        out.append("creative-telescoping blocker drift")
    if failed.get("class_boundary") != "The source refutes listed fixed-letter/local-residue hypothesis classes, not T3 itself.":
        out.append("class-versus-theorem boundary missing")
    if failed.get("exact_counterexample_found") is not False or failed.get("uniform_proof_found") is not False:
        out.append("failed-route ledger overclaims result")

    symbolic = resources.get("symbolic_route", {})
    for field in ("producer_available_at_pinned_source", "candidate_certificate_available",
                  "independent_verifier_input_available", "search_basis_locked", "degree_bounds_locked"):
        if symbolic.get(field) is not False:
            out.append(f"symbolic blocker must remain false: {field}")
    if symbolic.get("result") != "BLOCKED_BEFORE_REPLAYABLE_SEARCH":
        out.append("resource disposition drift")

    if cert.get("proof_certificate", {}).get("present") is not False:
        out.append("fabricated proof certificate")
    if cert.get("counterexample_certificate", {}).get("present") is not False:
        out.append("fabricated counterexample")
    if cert.get("may_claim_proof") is not False or cert.get("may_claim_refutation") is not False:
        out.append("certificate status promotes claim")

    if disposition.get("status") != "OPEN_WITH_CHARACTERIZED_BLOCKER":
        out.append("terminal disposition drift")
    if disposition.get("proof_found") is not False or disposition.get("counterexample_found") is not False:
        out.append("terminal disposition overclaims")
    effect = disposition.get("route_effect", {})
    if effect.get("sharp_12_may_advance") is not False:
        out.append("sharp-12 gate opened")
    if effect.get("T1_top_open") is not True or effect.get("DEPTH_open") is not True:
        out.append("independent sharp-12 blockers suppressed")
    if effect.get("quarantined_lean_may_be_repaired") is not False:
        out.append("Lean quarantine opened without proof object")
    return out

def main() -> int:
    found = errors()
    if found:
        for item in found:
            print(item, file=sys.stderr)
        return 1
    print("OZ T3 target, finite evidence, failed routes, resources, and blocker disposition are valid")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
