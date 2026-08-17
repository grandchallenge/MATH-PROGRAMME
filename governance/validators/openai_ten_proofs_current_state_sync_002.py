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
    "programme_base": "df4e81fb254ccc585c8ffad80a99798507579863",
    "forge_main": "48e8bf8e0fd157688ae83a8110d63b1e500ee688",
    "solve_main": "7d1f9edf16558ba4c4396126e24fd2c9ae4826f7",
    "cert_main": "5a69fd897f69cc3871f2138d162fb6ec897ef393",
}
EXPECTED_OWNERSHIP = {
    "forge": "source_identity_semantic_nonvacuity_and_revision_loci",
    "solve": "producer_packets_and_handoff_provenance",
    "cert": "route_adjudication_disposition_and_output",
    "programme": "cross_repository_current_state_only",
}
EXPECTED_QUALIFIED = [
    ("OTP-F-EHRHART", "MC-ROUTE-OTP-F-EHRHART", "27a855c949b67e71372c7f0d6601d80125d33968"),
    ("OTP-J1-COMPACTNESS", "MC-ROUTE-OTP-J1-COMPACTNESS", "88531e28951854961e86eec0517356999a391759"),
    ("OTP-J2-TWO-DEGENERATE", "MC-ROUTE-OTP-J2-TWO-DEGENERATE", "308a2eb7087fb24a07a6ae8c93a83b593468d2f7"),
    ("OTP-C-PERMANENT", "MC-ROUTE-OTP-C-PERMANENT-FORMULA", "ad10c427270cb1c747ebcacbc5c37e4c1ed1df04"),
]
EXPECTED_QUEUE = [
    "OTP-A-SPHERE-PACKING",
    "OTP-H-GAPCVP",
    "OTP-B1-BINARY-CODES",
    "OTP-B2-SPHERICAL-CODES",
    "OTP-I-RAMSEY",
    "OTP-G-QUANTUM-PARALLEL-REPETITION",
    "OTP-D-NON-SOFIC",
    "OTP-E-CONNES-RIGIDITY",
]
EXPECTED_ORDER = [
    "OTP-A-SPHERE-PACKING_and_OTP-H-GAPCVP",
    "OTP-B1-BINARY-CODES",
    "OTP-B2-SPHERICAL-CODES",
    "OTP-I-RAMSEY",
    "OTP-G-QUANTUM-PARALLEL-REPETITION",
    "OTP-D-NON-SOFIC",
    "OTP-E-CONNES-RIGIDITY",
]


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def git_blob_sha1(path: Path) -> str:
    payload = path.read_bytes()
    return hashlib.sha1(f"blob {len(payload)}\0".encode("ascii") + payload, usedforsecurity=False).hexdigest()


def validation_errors(*, record=None, schema=None, predecessor_blob=None, umbrella_blob=None) -> list[str]:
    record = load(RECORD) if record is None else record
    schema = load(SCHEMA) if schema is None else schema
    predecessor_blob = git_blob_sha1(PREDECESSOR) if predecessor_blob is None else predecessor_blob
    umbrella_blob = git_blob_sha1(UMBRELLA) if umbrella_blob is None else umbrella_blob
    errors: list[str] = []

    if schema.get("additionalProperties") is not False:
        errors.append("current-state successor schema must remain closed")
    errors.extend(f"schema violation: {e.message}" for e in Draft202012Validator(schema).iter_errors(record))

    if predecessor_blob != EXPECTED_PREDECESSOR_BLOB:
        errors.append("predecessor Programme current-state record drift")
    if umbrella_blob != EXPECTED_UMBRELLA_BLOB:
        errors.append("historical Programme umbrella record drift")

    supersession = record.get("supersession", {})
    predecessor = supersession.get("predecessor_programme_record", {})
    historical = supersession.get("historical_umbrella_record", {})
    if predecessor.get("git_blob_sha1") != EXPECTED_PREDECESSOR_BLOB or predecessor.get("mutation_prohibited") is not True:
        errors.append("predecessor Programme record supersession drift")
    if historical.get("git_blob_sha1") != EXPECTED_UMBRELLA_BLOB or historical.get("mutation_prohibited") is not True:
        errors.append("historical umbrella supersession drift")

    if record.get("ownership") != EXPECTED_OWNERSHIP:
        errors.append("cross-repository ownership collapse or drift")
    if record.get("protected_heads") != EXPECTED_HEADS:
        errors.append("protected-head identity drift")

    source = record.get("formal_source_authority", {})
    if source.get("protected_successor_merge") != EXPECTED_HEADS["forge_main"]:
        errors.append("formal-source successor merge drift")
    if source.get("successor_record_blob") != "6993ce9fac2c65ffae7f2a0c7d728aab828ed532":
        errors.append("formal-source successor record blob drift")
    if source.get("current_root_for_unresolved_families") != "94bc0feb6a9ff12c7d31d6de640a725c9d43d2b6":
        errors.append("current unresolved-family root drift")
    if source.get("current_tree_for_unresolved_families") != "174289e4d4958cb0509874e6e53400e098213de7":
        errors.append("current unresolved-family tree drift")
    if source.get("unresolved_family_count") != 8:
        errors.append("unresolved-family count drift")

    cert = record.get("cert_authority", {})
    if cert.get("route_registry_blob") != "2d17473b4731aa9d9c630b1e7777ad4bd794d993":
        errors.append("MATHCERT route-registry blob drift")
    qualified = cert.get("qualified_restricted_surfaces", [])
    observed = [(x.get("family"), x.get("route"), x.get("certificate_blob")) for x in qualified]
    if observed != EXPECTED_QUALIFIED:
        errors.append("restricted qualification identity or ordering drift")
    if cert.get("aggregate_output_count") != 0:
        errors.append("aggregate output inflation")
    if cert.get("mathematical_targets_marked_proved") != 0:
        errors.append("mathematical proof promotion")

    permanent = record.get("permanent_successor_surfaces", [])
    if len(permanent) != 2:
        errors.append("Permanent successor surface count drift")
    else:
        if permanent[0].get("solve_merge") != "bebc35818c6d3b79ddc7e348c9bffd328279cd24" or permanent[0].get("cert_route_state") != "not_registered":
            errors.append("Permanent full-formula producer state drift")
        if permanent[1].get("solve_merge") != "7d1f9edf16558ba4c4396126e24fd2c9ae4826f7" or permanent[1].get("cert_route_state") != "not_registered":
            errors.append("Permanent circuit producer state drift")

    queue = record.get("unresolved_family_queue", [])
    if [x.get("family") for x in queue] != EXPECTED_QUEUE:
        errors.append("unresolved-family queue drift")
    if record.get("execution_order") != EXPECTED_ORDER:
        errors.append("governed execution order drift")

    limitations = record.get("preserved_limitations", {})
    if limitations.get("aggregate_ten_proofs_authority") is not False:
        errors.append("aggregate Ten Proofs authority inflation")
    if limitations.get("proof_body_compared_in_full") is not False:
        errors.append("proof-body comparison inflation")
    if limitations.get("whole_document_semantic_equivalence") != "not_established":
        errors.append("whole-document semantic-equivalence inflation")

    boundary = str(record.get("claim_boundary", ""))
    for token in (
        "does not rewrite predecessor source records",
        "infer semantic clearance from isolated replay",
        "broaden any restricted certificate",
        "eight unresolved families",
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
    print("validated OTP current-state successor 002 and fail-closed authority boundaries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
