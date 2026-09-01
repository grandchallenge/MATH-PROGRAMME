#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]
RECORD = ROOT / "governance/openai_ten_proofs_current_state_sync_002.json"
SCHEMA = ROOT / "schemas/openai_ten_proofs_current_state_sync_002.schema.json"
PREDECESSOR = ROOT / "governance/openai_ten_proofs_cert_state_sync.json"
UMBRELLA = ROOT / "governance/openai_ten_proofs_umbrella_sync.json"

EXPECTED_PREDECESSOR_BLOB = "ea0826e2d9f5a08f6bd87b7934c5ef71484add12"
EXPECTED_UMBRELLA_BLOB = "710e8949df5f60efee5b2a7ca53b0f4750c2bfa8"
EXPECTED_HEADS = {
    "programme_base": "3443dc530a5645f70130afa6a417426a8696135e",
    "forge_main": "b9dda1a5b958fd1be37a26324a025013a39584c1",
    "solve_main": "7d1f9edf16558ba4c4396126e24fd2c9ae4826f7",
    "cert_main": "5a69fd897f69cc3871f2138d162fb6ec897ef393",
}
EXPECTED_SOURCE_SUCCESSOR = "48e8bf8e0fd157688ae83a8110d63b1e500ee688"
EXPECTED_OWNERSHIP = {
    "forge": "source_identity_semantic_nonvacuity_and_revision_loci",
    "solve": "producer_packets_and_handoff_provenance",
    "cert": "route_adjudication_disposition_and_output",
    "programme": "cross_repository_current_state_only",
}
EXPECTED_QUALIFIED = [
    ("OTP-F-EHRHART", "MC-ROUTE-OTP-F-EHRHART", "27a855c949b67e71372c7f0d6601d80125d33968", "qualified_encoded_targets_only"),
    ("OTP-J1-COMPACTNESS", "MC-ROUTE-OTP-J1-COMPACTNESS", "88531e28951854961e86eec0517356999a391759", "qualified_encoded_targets_only"),
    ("OTP-J2-TWO-DEGENERATE", "MC-ROUTE-OTP-J2-TWO-DEGENERATE", "308a2eb7087fb24a07a6ae8c93a83b593468d2f7", "qualified_source_faithful_targets_only"),
    ("OTP-C-PERMANENT", "MC-ROUTE-OTP-C-PERMANENT-FORMULA", "ad10c427270cb1c747ebcacbc5c37e4c1ed1df04", "qualified_encoded_targets_only"),
]
EXPECTED_COMPLETED = [
    {
        "family": "OTP-A-SPHERE-PACKING",
        "tracker": "MATHFORGE#89",
        "forge_merge": "5a0cb9a7b7eef210dd0fce5c527d09b6eef3bc12",
        "audit_record_path": "sources/OPENAI-TEN-PROOFS-001/semantic/OTP-A-SPHERE-PACKING-BRIDGE/audit_record.json",
        "audit_record_blob": "7858b156fc4490ecc6e3572dcf449d84dcc99f93",
        "disposition": "SPHERE_PACKING_CURRENT_ROOT__SEMANTIC_AND_NONVACUITY_CLEAR__SOLVE_HANDOFF_NOT_AUTHORIZED",
        "solve_handoff_authorized": False,
        "mathcert_route_authorized": False,
    },
    {
        "family": "OTP-H-GAPCVP",
        "tracker": "MATHFORGE#90",
        "forge_merge": "b9dda1a5b958fd1be37a26324a025013a39584c1",
        "audit_record_path": "sources/OPENAI-TEN-PROOFS-001/semantic/OTP-H-GAPCVP/audit_record.json",
        "audit_record_blob": "673f541fbb552d307cc226c51d2f0fd2916b328d",
        "disposition": "PROMISE_INTERFACES_CLOSED__SEMANTIC_AND_NONVACUITY_CLEAR_CURRENT_ROOT",
        "solve_handoff_authorized": False,
        "mathcert_route_authorized": False,
    },
]
EXPECTED_QUEUE = [
    ("OTP-B1-BINARY-CODES", "queued_current_root_semantic_audit"),
    ("OTP-B2-SPHERICAL-CODES", "queued_target_surface_drift_audit"),
    ("OTP-I-RAMSEY", "queued_current_root_semantic_audit"),
    ("OTP-G-QUANTUM-PARALLEL-REPETITION", "queued_current_root_semantic_audit"),
    ("OTP-D-NON-SOFIC", "queued_current_root_semantic_audit"),
    ("OTP-E-CONNES-RIGIDITY", "queued_declaration_identity_drift_audit"),
]
EXPECTED_ORDER = [x[0] for x in EXPECTED_QUEUE]
EXPECTED_NEXT = [
    "begin_current_root_Binary_Codes_semantic_and_nonvacuity_audit",
    "preserve_Spherical_Codes_target_surface_drift_and_Connes_Rigidity_declaration_identity_drift_as_explicit_governed_differences",
    "route_new_Permanent_full_formula_and_circuit_handoffs_only_through_independent_MATHCERT_operations",
]


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def git_blob_sha1(path: Path) -> str:
    payload = path.read_bytes()
    return hashlib.sha1(
        f"blob {len(payload)}\0".encode("ascii") + payload,
        usedforsecurity=False,
    ).hexdigest()


def validation_errors(*, record=None, schema=None, predecessor_blob=None, umbrella_blob=None) -> list[str]:
    record = load(RECORD) if record is None else record
    schema = load(SCHEMA) if schema is None else schema
    predecessor_blob = git_blob_sha1(PREDECESSOR) if predecessor_blob is None else predecessor_blob
    umbrella_blob = git_blob_sha1(UMBRELLA) if umbrella_blob is None else umbrella_blob
    errors: list[str] = []

    if schema.get("additionalProperties") is not False:
        errors.append("current-state successor schema must remain closed")
    errors.extend(
        f"schema violation: {e.message}"
        for e in Draft202012Validator(schema).iter_errors(record)
    )

    if predecessor_blob != EXPECTED_PREDECESSOR_BLOB:
        errors.append("predecessor Programme current-state record drift")
    if umbrella_blob != EXPECTED_UMBRELLA_BLOB:
        errors.append("historical Programme umbrella record drift")

    if record.get("schema_version") != "1.1.0":
        errors.append("schema version drift")
    if record.get("record_id") != "MP-OTP-CURRENT-STATE-SYNC-002":
        errors.append("record identity drift")
    if record.get("candidate_id") != "OPENAI-TEN-PROOFS-001":
        errors.append("candidate identity drift")
    if record.get("lifecycle_state") != (
        "four_restricted_cert_qualifications_two_additional_permanent_solve_surfaces_"
        "two_current_root_forge_clearances_six_current_root_unresolved_families"
    ):
        errors.append("lifecycle state drift")
    if record.get("active_campaign_member") is not False:
        errors.append("campaign activation inflation")

    supersession = record.get("supersession", {})
    predecessor = supersession.get("predecessor_programme_record", {})
    historical = supersession.get("historical_umbrella_record", {})
    if predecessor != {
        "path": "governance/openai_ten_proofs_cert_state_sync.json",
        "git_blob_sha1": EXPECTED_PREDECESSOR_BLOB,
        "mutation_prohibited": True,
    }:
        errors.append("predecessor Programme supersession drift")
    if historical != {
        "path": "governance/openai_ten_proofs_umbrella_sync.json",
        "git_blob_sha1": EXPECTED_UMBRELLA_BLOB,
        "mutation_prohibited": True,
    }:
        errors.append("historical umbrella supersession drift")

    if record.get("ownership") != EXPECTED_OWNERSHIP:
        errors.append("cross-repository ownership collapse or drift")
    if record.get("protected_heads") != EXPECTED_HEADS:
        errors.append("protected-head identity drift")

    source = record.get("formal_source_authority", {})
    if source.get("protected_successor_merge") != EXPECTED_SOURCE_SUCCESSOR:
        errors.append("formal-source successor merge drift")
    if source.get("protected_successor_merge") == EXPECTED_HEADS["forge_main"]:
        errors.append("formal-source successor identity collapsed into current Forge main")
    if source.get("successor_record_blob") != "6993ce9fac2c65ffae7f2a0c7d728aab828ed532":
        errors.append("formal-source successor record blob drift")
    if source.get("current_root_for_unresolved_families") != "94bc0feb6a9ff12c7d31d6de640a725c9d43d2b6":
        errors.append("current unresolved-family root drift")
    if source.get("current_tree_for_unresolved_families") != "174289e4d4958cb0509874e6e53400e098213de7":
        errors.append("current unresolved-family tree drift")
    if source.get("unresolved_family_count") != 6:
        errors.append("unresolved-family count drift")

    cert = record.get("cert_authority", {})
    if cert.get("route_registry_blob") != "2d17473b4731aa9d9c630b1e7777ad4bd794d993":
        errors.append("MATHCERT route-registry blob drift")
    observed_qualified = [
        (x.get("family"), x.get("route"), x.get("certificate_blob"), x.get("disposition"))
        for x in cert.get("qualified_restricted_surfaces", [])
    ]
    if observed_qualified != EXPECTED_QUALIFIED:
        errors.append("restricted qualification identity, disposition or ordering drift")
    if cert.get("aggregate_output_count") != 0:
        errors.append("aggregate output inflation")
    if cert.get("mathematical_targets_marked_proved") != 0:
        errors.append("mathematical proof promotion")

    permanent = record.get("permanent_successor_surfaces", [])
    if len(permanent) != 2 or any(x.get("cert_route_state") != "not_registered" for x in permanent):
        errors.append("Permanent successor routing inflation")

    if record.get("current_root_completed_families") != EXPECTED_COMPLETED:
        errors.append("protected current-root Forge completion identity or authority drift")

    queue = record.get("unresolved_family_queue", [])
    observed_queue = [(x.get("family"), x.get("state")) for x in queue]
    if observed_queue != EXPECTED_QUEUE:
        errors.append("unresolved-family queue or state drift")
    if any(x.get("family") in {"OTP-A-SPHERE-PACKING", "OTP-H-GAPCVP"} for x in queue):
        errors.append("protected-complete A/H family reinserted into unresolved queue")
    if record.get("execution_order") != EXPECTED_ORDER:
        errors.append("governed execution order drift")

    expected_limitations = {
        "all_lean_state": "separate_integration_debt",
        "whole_document_byte_equivalence": "not_established_between_all_revisions",
        "whole_document_semantic_equivalence": "not_established",
        "proof_body_compared_in_full": False,
        "aggregate_ten_proofs_authority": False,
    }
    if record.get("preserved_limitations") != expected_limitations:
        errors.append("preserved limitation drift or authority inflation")
    if record.get("next_controlled_obligations") != EXPECTED_NEXT:
        errors.append("next controlled obligation drift")

    boundary = str(record.get("claim_boundary", ""))
    for token in (
        "Sphere Packing and GapCVP",
        "without converting either clearance into a Solve handoff",
        "six remaining unresolved families",
        "does not rewrite predecessor source records",
        "broaden any restricted certificate",
        "aggregate OpenAI Ten Proofs certification object",
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
    print("validated OTP current-state successor 002 at two Forge clearances / six unresolved families")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
