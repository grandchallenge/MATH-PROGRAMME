#!/usr/bin/env python3
"""Fail-closed validator for the EUCLID-GCD-E2E-001 Programme closeout."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "governance" / "euclid_gcd_e2e_001_closeout.json"
SCHEMA = ROOT / "schemas" / "euclid_gcd_e2e_001_closeout.schema.json"
PAGE = ROOT / "docs" / "EUCLID_GCD_E2E_001_PROOF_TRACE.md"

EXPECTED = {
    "programme_base": "2f9d8e718814de957b6c999ae0579c5303a7c285",
    "forge_merge": "3622bac82a39cdb9e82ec463919d9e6927c1ec0e",
    "solve_merge": "3a8493aa322f0e640c921b8824c4d7f88a8c057d",
    "cert_merge": "78b69e6a3461a83f4893d61c421b1570c08a9ba6",
    "forge_package": "079b68fb5651e0d2eee0a7b2002454d34673d84c",
    "forge_manifest": "a103b2c85dbd67973da43656fed5af567c5b7074",
    "solve_candidate": "af54ae9b9a047a36767b2599ebc649fb6fdaaa52",
    "solve_solver": "012a90e0cd84e4ad7f0fd3f1c9534a6673dc0f24",
    "solve_handoff": "01a20512c428ce4384959064ab3343a1cbb0c7d2",
    "solve_manifest": "1cdb081595da2f8b21f60a192ec8cc83c20031ac",
    "cert_output": "36c62434dbd19719d990e71ddc23729f0614ace7",
    "cert_route": "0ada97db2673db819104320d128bd994e892f1a4",
    "cert_lean": "bf0ab5bac117490299ff5bffb8ca59263ec3f2a3",
}
CLAIMS = {f"EUCLID-GCD-E2E-001-C00{i}" for i in range(1, 5)}
REQUIRED_PAGE_TOKENS = (
    "252 = 2 * 105 + 42",
    "105 = 2 * 42 + 21",
    "42 = 2 * 21 + 0",
    "21 = -2 * 252 + 5 * 105",
    "AcceptedGCDCertificate",
    "acceptedGCDCertificate_sound",
    "Nat.gcd 252 105 = 21",
    "CERTIFIED_CHECKER_SOUNDNESS_AND_CONCRETE_GCD_INSTANCE",
    EXPECTED["forge_merge"],
    EXPECTED["solve_merge"],
    EXPECTED["cert_merge"],
    "does **not** establish",
)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def semantic_errors(data: Any, page_text: str) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["closeout record must be an object"]

    programme = data.get("programme", {})
    if programme.get("protected_base") != EXPECTED["programme_base"]:
        errors.append("Programme protected-base identity drift")
    if programme.get("authority_state") != "candidate_programme_closeout_pending_exact_head_review_and_protected_merge":
        errors.append("candidate closeout authority state drift")

    for key, expected in (("forge", EXPECTED["forge_merge"]), ("solve", EXPECTED["solve_merge"]), ("cert", EXPECTED["cert_merge"])):
        stage = data.get(key, {})
        if stage.get("merge_commit") != expected:
            errors.append(f"{key} merge identity drift")
        review = stage.get("independent_review", {})
        if review.get("reviewer") != "jimsteeg" or review.get("state") != "APPROVED":
            errors.append(f"{key} independent review boundary drift")
        if not stage.get("human_steward", {}).get("disposition", "").startswith("HUMAN_STEWARD_AUTHORIZED_EXACT_HEAD_"):
            errors.append(f"{key} Human Steward disposition drift")
        if any(not isinstance(value, int) or value <= 0 for value in stage.get("exact_head_workflows", {}).values()):
            errors.append(f"{key} exact-head workflow identity invalid")
        if any(not isinstance(value, int) or value <= 0 for value in stage.get("protected_main_workflows", {}).values()):
            errors.append(f"{key} protected-main workflow identity invalid")

    solve = data.get("solve", {})
    if solve.get("merge_parents") != [solve.get("protected_base"), solve.get("reviewed_head")]:
        errors.append("Solve merge-parent binding drift")
    cert = data.get("cert", {})
    if cert.get("merge_parents") != [cert.get("protected_base"), cert.get("reviewed_head")]:
        errors.append("Cert merge-parent binding drift")
    if cert.get("disposition") != "CERTIFIED_CHECKER_SOUNDNESS_AND_CONCRETE_GCD_INSTANCE":
        errors.append("Cert disposition drift")

    artifacts = {
        "forge_package": data.get("forge", {}).get("artifacts", {}).get("forge_package", {}).get("git_blob_sha1"),
        "forge_manifest": data.get("forge", {}).get("artifacts", {}).get("provider_manifest", {}).get("git_blob_sha1"),
        "solve_candidate": solve.get("artifacts", {}).get("candidate", {}).get("git_blob_sha1"),
        "solve_solver": solve.get("artifacts", {}).get("solver", {}).get("git_blob_sha1"),
        "solve_handoff": solve.get("artifacts", {}).get("handoff", {}).get("git_blob_sha1"),
        "solve_manifest": solve.get("artifacts", {}).get("campaign_manifest", {}).get("git_blob_sha1"),
        "cert_output": cert.get("artifacts", {}).get("certification_output", {}).get("git_blob_sha1"),
        "cert_route": cert.get("artifacts", {}).get("route_overlay", {}).get("git_blob_sha1"),
        "cert_lean": cert.get("artifacts", {}).get("lean_theorem", {}).get("git_blob_sha1"),
    }
    for name, actual in artifacts.items():
        if actual != EXPECTED[name]:
            errors.append(f"{name} artifact identity drift")

    claim_ids = [item.get("claim_id") for item in data.get("certified_claims", []) if isinstance(item, dict)]
    if set(claim_ids) != CLAIMS or len(claim_ids) != len(CLAIMS):
        errors.append("certified claim membership drift")

    instance = data.get("canonical_instance", {})
    if (instance.get("a"), instance.get("b"), instance.get("d")) != (252, 105, 21):
        errors.append("canonical instance drift")
    trace = instance.get("trace", [])
    expected_trace = [(252, 105, 2, 42), (105, 42, 2, 21), (42, 21, 2, 0)]
    actual_trace = [
        (step.get("dividend"), step.get("divisor"), step.get("quotient"), step.get("remainder"))
        for step in trace if isinstance(step, dict)
    ]
    if actual_trace != expected_trace:
        errors.append("canonical Euclidean trace drift")
    else:
        for index, (dividend, divisor, quotient, remainder) in enumerate(actual_trace):
            if dividend != quotient * divisor + remainder:
                errors.append(f"trace equation {index} is false")
            if remainder < 0 or remainder >= divisor:
                errors.append(f"trace remainder bound {index} is false")
            if index < 2 and remainder <= 0:
                errors.append(f"trace strict descent {index} is false")
        if actual_trace[-1][-1] != 0:
            errors.append("trace is not terminal")
    bezout = instance.get("bezout", {})
    if bezout.get("x") * 252 + bezout.get("y") * 105 != 21:
        errors.append("Bézout witness is false")

    boundaries = data.get("boundaries", {})
    if any(value is not False for value in boundaries.values()):
        errors.append("one or more non-inflation boundaries became active")
    if data.get("successor_gates", {}).get("linear_diophantine") != "blocked_until_this_closeout_is_independently_approved_human_steward_authorized_protected_merged_and_read_back":
        errors.append("linear Diophantine gate drift")
    if data.get("successor_gates", {}).get("book_vii_microcampaign") != "blocked_until_linear_diophantine_protected_completion_and_exact_historical_source_lock":
        errors.append("Book VII gate drift")
    if data.get("protected_effect") != "none_until_exact_head_review_human_steward_disposition_protected_merge_post_merge_checks_and_publication":
        errors.append("protected-effect boundary drift")

    for token in REQUIRED_PAGE_TOKENS:
        if token not in page_text:
            errors.append(f"public proof trace is missing required token: {token}")
    return errors


def validate(record_path: Path = RECORD, schema_path: Path = SCHEMA, page_path: Path = PAGE) -> list[str]:
    data = load_json(record_path)
    schema = load_json(schema_path)
    errors = [
        f"{error.json_path}: {error.message}"
        for error in sorted(Draft202012Validator(schema).iter_errors(data), key=lambda item: list(item.path))
    ]
    if not page_path.is_file():
        return errors + ["public proof trace file is missing"]
    errors.extend(semantic_errors(data, page_path.read_text(encoding="utf-8")))
    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("\n".join(errors))
        print(f"EUCLID-GCD-E2E-001 Programme closeout failed with {len(errors)} error(s)")
        return 1
    print("validated exact cross-pillar receipt, arithmetic proof trace, bounded certification, and successor-stage gates")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
