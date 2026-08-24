#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]
RECORD = ROOT / "governance/openai_ten_proofs_current_state_sync_003.json"
SCHEMA = ROOT / "schemas/openai_ten_proofs_current_state_sync_003.schema.json"
SYNC002 = ROOT / "governance/openai_ten_proofs_current_state_sync_002.json"
CERT_SYNC = ROOT / "governance/openai_ten_proofs_cert_state_sync.json"
UMBRELLA = ROOT / "governance/openai_ten_proofs_umbrella_sync.json"

EXPECTED_BLOBS = {
    "sync002": "667f184186b3abe0d8b9a48f579671b9792848cc",
    "cert_sync": "ea0826e2d9f5a08f6bd87b7934c5ef71484add12",
    "umbrella": "710e8949df5f60efee5b2a7ca53b0f4750c2bfa8",
}
EXPECTED_HEADS = {
    "programme_base": "0642ae323cdad7b67a4e2da669d7bd772c45f4b8",
    "forge_main": "ed8a65410336489ea5646808265c44f5387bebb8",
    "solve_main": "c19735edf4c16ac9765bb66c7209bbf11bf1312e",
    "cert_main": "10d3f5ccd69f45e39ce23d758801bde8c6040401",
}
EXPECTED_OWNERSHIP = {
    "forge": "source_identity_semantic_nonvacuity_and_revision_loci",
    "solve": "producer_packets_and_handoff_provenance",
    "cert": "route_adjudication_disposition_and_output",
    "programme": "cross_repository_current_state_only",
}
EXPECTED_QUALIFIED = [
    ("OTP-F-EHRHART", "encoded_ehrhart_targets", "MC-ROUTE-OTP-F-EHRHART", "27a855c949b67e71372c7f0d6601d80125d33968", "qualified_encoded_targets_only"),
    ("OTP-J1-COMPACTNESS", "encoded_compactness_targets", "MC-ROUTE-OTP-J1-COMPACTNESS", "88531e28951854961e86eec0517356999a391759", "qualified_encoded_targets_only"),
    ("OTP-J2-TWO-DEGENERATE", "source_faithful_two_target_surface", "MC-ROUTE-OTP-J2-TWO-DEGENERATE", "308a2eb7087fb24a07a6ae8c93a83b593468d2f7", "qualified_source_faithful_targets_only"),
    ("OTP-C-PERMANENT", "variable_leaf_formula", "MC-ROUTE-OTP-C-PERMANENT-FORMULA", "ad10c427270cb1c747ebcacbc5c37e4c1ed1df04", "qualified_encoded_targets_only"),
    ("OTP-C-PERMANENT", "full_formula_consequences", "MC-ROUTE-OTP-C-PERMANENT-FULL-FORMULA", "2940f551805794b96c7b0793bfe0d14e9fcd9954", "qualified_encoded_targets_only"),
    ("OTP-C-PERMANENT", "theorem_1_1_circuit", "MC-ROUTE-OTP-C-PERMANENT-CIRCUIT", "9d0eb4a83df73440b17cb6809ede5cdcc0a8e385", "qualified_encoded_targets_only"),
]
EXPECTED_REPLAY = [
    ("OTP-H-GAPCVP", "OTP-H-GAPCVP-CERT-WP-001", "10e6f3ee20d7a6e89feb27aef0115fa27710d5e4", "0f811d163f0d36b028cf6539963e2cf278517137"),
    ("OTP-B1-BINARY-CODES", "OTP-B1-BINARY-CODES-CERT-WP-001", "83a8951a89a72a892d5fdc132d6a22e508d6cdc2", "19e1eaf5e24ce212bb020c8c40d4177ff5b4f8f9"),
    ("OTP-B2-SPHERICAL-CODES", "OTP-B2-SPHERICAL-CODES-CERT-WP-001", "be26d65ba147922ec0975419196b5fdbc7427b8a", "50dc2c9c5bc8aad49f22414536102cef0e82ce20"),
]
EXPECTED_FORGE_PENDING = [
    ("OTP-I-RAMSEY", "dbf3b099331a1807c4d3036e7a6a406711ea7cf3", "a7c014fb623b66355ef5d6260e5b994d99d67a6d"),
    ("OTP-G-QUANTUM-PARALLEL-REPETITION", "f0a40146cca7fd39c5724ed5be033ee9092625ac", "bfcbee0fd6174b8856b17c3d56ee320f27c18ec6"),
    ("OTP-D-NON-SOFIC", "081928fceaca9606af4920559f8b79d5e40225a7", "a9a5a2d56fceda6ebddf0c729d97c7cbeaf0d48b"),
    ("OTP-E-CONNES-RIGIDITY", "ed8a65410336489ea5646808265c44f5387bebb8", "ab38a22d029bacc09d7567166b3b5e380f207f99"),
]


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def git_blob_sha1(path: Path) -> str:
    payload = path.read_bytes()
    return hashlib.sha1(f"blob {len(payload)}\0".encode("ascii") + payload, usedforsecurity=False).hexdigest()


def validation_errors(*, record=None, schema=None, historical_blobs=None) -> list[str]:
    record = load(RECORD) if record is None else record
    schema = load(SCHEMA) if schema is None else schema
    historical_blobs = historical_blobs or {
        "sync002": git_blob_sha1(SYNC002),
        "cert_sync": git_blob_sha1(CERT_SYNC),
        "umbrella": git_blob_sha1(UMBRELLA),
    }
    errors: list[str] = []

    if schema.get("additionalProperties") is not False:
        errors.append("successor schema must remain closed")
    errors.extend(f"schema violation: {e.message}" for e in Draft202012Validator(schema).iter_errors(record))

    for key, expected in EXPECTED_BLOBS.items():
        if historical_blobs.get(key) != expected:
            errors.append(f"historical record drift: {key}")

    if record.get("record_id") != "MP-OTP-CURRENT-STATE-SYNC-003":
        errors.append("record identity drift")
    if record.get("active_campaign_member") is not False:
        errors.append("Programme campaign-activation inflation")
    if record.get("ownership") != EXPECTED_OWNERSHIP:
        errors.append("repository ownership collapse or drift")
    if record.get("protected_heads") != EXPECTED_HEADS:
        errors.append("protected-head drift")

    supersession = record.get("supersession", {})
    expected_supersession = {
        "predecessor_current_state_sync": {"path": "governance/openai_ten_proofs_current_state_sync_002.json", "git_blob_sha1": EXPECTED_BLOBS["sync002"], "mutation_prohibited": True},
        "predecessor_programme_record": {"path": "governance/openai_ten_proofs_cert_state_sync.json", "git_blob_sha1": EXPECTED_BLOBS["cert_sync"], "mutation_prohibited": True},
        "historical_umbrella_record": {"path": "governance/openai_ten_proofs_umbrella_sync.json", "git_blob_sha1": EXPECTED_BLOBS["umbrella"], "mutation_prohibited": True},
        "effect": "current_cross_repository_state_without_rewriting_historical_programme_records",
    }
    if supersession != expected_supersession:
        errors.append("supersession chain drift")

    source = record.get("source_authority", {})
    for key, expected in {
        "official_pdf_revision": "2026-08-06",
        "official_pdf_bytes": 2487031,
        "official_pdf_sha256": "ebc561ab5c53dbd240e17a8fdb6fffeb648591eca85dbfc7466f563638f8c566",
        "formal_root": "94bc0feb6a9ff12c7d31d6de640a725c9d43d2b6",
        "formal_tree": "174289e4d4958cb0509874e6e53400e098213de7",
        "lean_version": "4.32.0",
    }.items():
        if source.get(key) != expected:
            errors.append(f"source authority drift: {key}")

    cert = record.get("cert_authority", {})
    if cert.get("global_route_registry_blob") != "b9bb0dc9e18856f50a88162df37c20c034327439":
        errors.append("global route-registry drift")
    observed_qualified = [(x.get("family"), x.get("surface"), x.get("route"), x.get("certificate_blob"), x.get("disposition")) for x in cert.get("restricted_qualified_surfaces", [])]
    if observed_qualified != EXPECTED_QUALIFIED:
        errors.append("restricted qualification surface drift")
    if cert.get("aggregate_output_count") != 0:
        errors.append("aggregate output inflation")
    if cert.get("mathematical_targets_marked_proved") != 0:
        errors.append("mathematical proof promotion")

    a = record.get("a_sphere_packing_frontier", {})
    expected_a = {
        "family": "OTP-A-SPHERE-PACKING",
        "route": "MC-ROUTE-OTP-A-SPHERE-PACKING",
        "route_state": "submitted",
        "adjudication_merge": "10d3f5ccd69f45e39ce23d758801bde8c6040401",
        "adjudication_path": "governance/result_family_adjudications/OTP-A-SPHERE-PACKING.json",
        "adjudication_blob": "3e0b34dbc74fdbe123f551d559e4f93fc1901c48",
        "adjudication_disposition": "adjudication_clear_protected_four_targets_only",
        "cert_output": None,
        "mathematical_target_proved": False,
        "may_issue_output": False,
        "next_boundary": "separately_governed_restricted_output_design",
    }
    if a != expected_a:
        errors.append("A adjudication/output frontier drift or premature output authority")

    observed_replay = [(x.get("family"), x.get("work_package"), x.get("protected_merge"), x.get("work_package_blob")) for x in record.get("cert_replay_frontier", [])]
    if observed_replay != EXPECTED_REPLAY:
        errors.append("H/B1/B2 replay frontier drift")
    if any(x.get("next_boundary") != "exact_replay_evidence_only" for x in record.get("cert_replay_frontier", [])):
        errors.append("premature route proposal/adjudication authority for H/B1/B2")

    observed_forge = [(x.get("family"), x.get("forge_merge"), x.get("audit_record_blob")) for x in record.get("forge_clear_downstream_pending", [])]
    if observed_forge != EXPECTED_FORGE_PENDING:
        errors.append("I/G/D/E Forge-clear frontier drift")
    if any(x.get("next_boundary") != "solve_handoff_requires_separate_authority" for x in record.get("forge_clear_downstream_pending", [])):
        errors.append("unauthorized downstream authority inferred for I/G/D/E")

    limits = record.get("preserved_limitations", {})
    if limits != {
        "whole_document_byte_equivalence": "not_established_between_all_revisions",
        "whole_document_semantic_equivalence": "not_established",
        "proof_body_compared_in_full": False,
        "aggregate_ten_proofs_authority": False,
        "aggregate_certification_object": False,
        "cross_family_authority_transfer": False,
    }:
        errors.append("preserved limitations weakened")

    boundary = str(record.get("claim_boundary", ""))
    for token in (
        "still-submitted route with cert_output null",
        "exact replay/evidence as the next boundary",
        "no Solve handoff or Cert authority is inferred",
        "Historical Programme records are preserved byte-identically",
        "aggregate OpenAI Ten Proofs route",
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
    print("validated OTP current-state successor 003: A adjudication / H-B1-B2 replay / I-G-D-E Forge frontier")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
