#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]
RECORD = ROOT / "governance/openai_ten_proofs_cert_state_sync.json"
SCHEMA = ROOT / "schemas/openai_ten_proofs_cert_state_sync.schema.json"
HISTORICAL_OVERLAY = ROOT / "governance/openai_ten_proofs_umbrella_sync.json"
EXPECTED_HISTORICAL_OVERLAY_BLOB = "710e8949df5f60efee5b2a7ca53b0f4750c2bfa8"
EXPECTED_OWNERSHIP = {
    "forge": "source_identity_semantic_nonvacuity_and_revision_loci",
    "solve": "producer_packets_and_handoff_provenance",
    "cert": "route_adjudication_disposition_and_output",
    "programme": "cross_repository_current_state_only",
}
EXPECTED_FAMILIES = [
    {
        "result_family": "OTP-F-EHRHART",
        "forge_semantic_state": "clear",
        "solve_producer_packet": "present",
        "cert_route_state": "qualified",
        "adjudication_count": 1,
        "restricted_cert_output_count": 1,
        "cert_disposition": "qualified_encoded_targets_only",
        "mathematical_target_proved": False,
    },
    {
        "result_family": "OTP-J1-COMPACTNESS",
        "forge_semantic_state": "clear",
        "solve_producer_packet": "present",
        "cert_route_state": "submitted",
        "adjudication_count": 0,
        "restricted_cert_output_count": 0,
        "cert_disposition": None,
        "mathematical_target_proved": False,
    },
    {
        "result_family": "OTP-J2-TWO-DEGENERATE",
        "forge_semantic_state": "clear",
        "solve_producer_packet": "present",
        "cert_route_state": "submitted",
        "adjudication_count": 0,
        "restricted_cert_output_count": 0,
        "cert_disposition": None,
        "mathematical_target_proved": False,
    },
]


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def git_blob_sha1(path: Path) -> str:
    payload = path.read_bytes()
    return hashlib.sha1(f"blob {len(payload)}\0".encode("ascii") + payload, usedforsecurity=False).hexdigest()


def validation_errors(*, record=None, schema=None, historical_overlay_blob=None) -> list[str]:
    record = load(RECORD) if record is None else record
    schema = load(SCHEMA) if schema is None else schema
    historical_overlay_blob = git_blob_sha1(HISTORICAL_OVERLAY) if historical_overlay_blob is None else historical_overlay_blob
    errors: list[str] = []

    if schema.get("additionalProperties") is not False:
        errors.append("Cert-state sync schema must remain closed")
    errors.extend(f"schema violation: {error.message}" for error in Draft202012Validator(schema).iter_errors(record))

    if historical_overlay_blob != EXPECTED_HISTORICAL_OVERLAY_BLOB:
        errors.append("historical Programme overlay blob drift")
    historical = record.get("supersession", {}).get("historical_programme_overlay", {})
    if historical.get("git_blob_sha1") != EXPECTED_HISTORICAL_OVERLAY_BLOB or historical.get("mutation_prohibited") is not True:
        errors.append("historical Programme overlay supersession drift")

    if record.get("ownership") != EXPECTED_OWNERSHIP:
        errors.append("cross-repository ownership boundary drift")

    forge = record.get("forge_authority", {})
    if forge.get("repository") != "grandchallenge/MATHFORGE":
        errors.append("Forge repository identity drift")
    if forge.get("semantic_merge") != "cb0a203c36a9ef33270d62ab369df7bc27d3b242":
        errors.append("Forge semantic merge drift")
    if forge.get("provider_manifest", {}).get("git_blob_sha1") != "fe1dab478e4ef9d6ddfe1b94a289fe7b51f58472":
        errors.append("Forge provider manifest blob drift")
    if [item.get("git_blob_sha1") for item in forge.get("semantic_records", [])] != [
        "a3dc4de4c38a80b7aec1fae6506b08e14d2e58bb",
        "659396358d0d999c00011645f72602f30ccf6b0e",
        "7bd168c46921f64364b20021b6315d68f0fde7d0",
    ]:
        errors.append("Forge semantic record identity drift")

    solve = record.get("solve_authority", {})
    if solve.get("repository") != "grandchallenge/MATHSOLVE":
        errors.append("Solve repository identity drift")
    if solve.get("handoff_merge") != "443daf537dc7e4ee34ab43aeb01508d9177816ab":
        errors.append("Solve handoff merge drift")
    if solve.get("handoff_registry_blob") != "82b4cc14a3c7700ab51ee25f06e6ba03c72e499c":
        errors.append("Solve handoff registry blob drift")
    if [item.get("git_blob_sha1") for item in solve.get("producer_packets", [])] != [
        "4653985d4980113514266c3c421804437bacb019",
        "2d9c6e555a03b71eb33c476321e7f2d311ed168f",
        "0d226492bf13e13bc1a437be01104db3d4c96f79",
    ]:
        errors.append("Solve producer packet identity drift")

    cert = record.get("cert_authority", {})
    expected_cert = {
        "repository": "grandchallenge/MATHCERT",
        "route_registration_merge": "cec85b13f5be48439e02fbbfedcf7ca1d839c097",
        "ehrhart_adjudication_merge": "41a2d699204d73543a4ac4bd33b2865d3803c5d6",
        "ehrhart_execution_merge": "1d5b1e6514787005ed75e363df7ea953dcd9391a",
        "ehrhart_documentary_closure_merge": "150344d25b50895203c59f4193a8e97bb1cbbf81",
        "closure_exact_reviewed_head": "207df8462f427e0c41604614ebe1a291ad89273f",
        "closure_review_id": 4840018727,
        "closure_human_steward_disposition_comment": 5160923732,
        "route_registry_blob": "0487c3ebf702229741f16a544d68af25cf994e41",
        "ehrhart_adjudication_blob": "dcea25320169b9309ebf6c7f48249df9a312555f",
        "ehrhart_certificate_id": "MC-OTP-F-EHRHART-QUAL-001",
        "ehrhart_certificate_blob": "27a855c949b67e71372c7f0d6601d80125d33968",
        "ehrhart_attestation_blob": "d8b36ffdb3b5e732b385c9bac5576aa96dd1fcbe",
        "ehrhart_successor_closure_blob": "c50a397a84873b358a54db2e602058da103b75e8",
    }
    for key, value in expected_cert.items():
        if cert.get(key) != value:
            errors.append(f"Cert authority drift: {key}")

    if record.get("result_family_state") != EXPECTED_FAMILIES:
        errors.append("result-family cross-repository state drift")

    totals = record.get("tranche_totals", {})
    expected_totals = {
        "semantic_clear_count": 3,
        "solve_producer_packet_count": 3,
        "registered_cert_route_count": 3,
        "adjudication_count": 1,
        "restricted_cert_output_count": 1,
        "aggregate_output_count": 0,
        "mathematical_targets_marked_proved": 0,
    }
    if totals != expected_totals:
        errors.append("tranche totals drift")

    remaining = record.get("remaining_state", {})
    expected_remaining = {
        "unexamined_result_family_count": 9,
        "blocked_repair_lanes": ["OTP-C-PERMANENT", "OTP-H-GAPCVP"],
        "all_lean_state": "failed_namespace_collision",
        "whole_document_byte_equivalence": "not_established_between_all_revisions",
        "whole_document_semantic_equivalence": "not_established",
        "proof_body_compared_in_full": False,
        "aggregate_ten_proofs_authority": False,
    }
    if remaining != expected_remaining:
        errors.append("remaining-state or claim-boundary drift")

    if record.get("next_controlled_obligation") != "OTP-J1-COMPACTNESS-CERT-EVIDENCE-REFRESH-001":
        errors.append("next controlled obligation drift")

    boundary = str(record.get("claim_boundary", ""))
    for token in (
        "division of authority among Forge, Solve, Cert, and Programme",
        "does not prove the Ehrhart source theorem",
        "all equality cases",
        "whole-document equivalence",
        "Compactness or Two-degenerate",
        "aggregate ten-proofs certification authority",
        "commercial claims",
    ):
        if token not in boundary:
            errors.append(f"claim boundary missing token: {token}")
    return errors


def main() -> int:
    errors = validation_errors()
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("validated OTP Cert-state sync and cross-repository authority separation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
