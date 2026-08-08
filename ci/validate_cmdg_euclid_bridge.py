#!/usr/bin/env python3
"""Fail-closed validation for CMDG-EUCLID-BRIDGE-001."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "governance" / "cmdg_euclid_bridge_001.json"
NODES = ROOT / "fixtures" / "cmdg" / "euclid_bridge_001" / "nodes.json"
EDGES = ROOT / "fixtures" / "cmdg" / "euclid_bridge_001" / "edges.json"
NODE_SCHEMA = ROOT / "schemas" / "cmdg_node.schema.json"
EDGE_SCHEMA = ROOT / "schemas" / "cmdg_edge.schema.json"
BRIDGE_SOURCE = ROOT / "fixtures" / "formal" / "CMDG-NAT-CONCORDANCE-001" / "CMDGEuclidBridge.lean"
TOOLCHAIN = ROOT / "fixtures" / "formal" / "CMDG-NAT-CONCORDANCE-001" / "lean-toolchain"
MANIFEST = ROOT / "fixtures" / "formal" / "CMDG-NAT-CONCORDANCE-001" / "lake-manifest.json"
CLOSEOUT = ROOT / "governance" / "euclid_gcd_e2e_001_closeout.json"
ORIGINAL_CONFIG = ROOT / "fixtures" / "cmdg" / "extractor_001" / "euclid_gcd_original.json"
BRIDGE_CONFIG = ROOT / "fixtures" / "cmdg" / "extractor_001" / "euclid_bridge.json"
WORKFLOW = ROOT / ".github" / "workflows" / "cmdg-euclid-bridge.yml"

BASELINE = "25f5fef222433f60f28b375d6ea814b844b5b062"
CLOSEOUT_BLOB = "8d2d666398625cffac9f01f30a8877616cee1ee6"
MATHCERT_COMMIT = "78b69e6a3461a83f4893d61c421b1570c08a9ba6"
MATHCERT_SOURCE_BLOB = "bf0ab5bac117490299ff5bffb8ca59263ec3f2a3"
ORIGINAL_TOOLCHAIN_BLOB = "dd1256f68cc62a04c1fb9599a7cd0582f1e6d016"
ORIGINAL_MANIFEST_BLOB = "2abef608042abe9569085042bf3d1ac64ec1c6b7"
BRIDGE_TOOLCHAIN_BLOB = "fd85b262bf1c734663aa8292b0101f672168788f"
BRIDGE_MANIFEST_BLOB = "9e478e09f622406970dc9613f6cf323ade82f787"
MATHLIB = "79d0395a1825a6264ad5d269e35e60537518955e"
ORIGINAL_ROOTS = [
    "MathCert.NumberTheory.acceptedGCDCertificate_sound",
    "MathCert.NumberTheory.euclidTrace252105",
    "MathCert.NumberTheory.bezout252105",
    "MathCert.NumberTheory.gcd252105",
    "MathCert.NumberTheory.accepted252105",
    "MathCert.NumberTheory.accepted252105_sound",
]
BRIDGE_ROOT = "CMDG.EuclidBridge.euclid_gcd_relational_bridge"
OPS = ["ZERO", "SUCCESSOR", "ADDITION", "MULTIPLICATION", "ORDER", "DIVISIBILITY"]
TRANSPORTED = ["RELATIONAL_GCD_SPECIFICATION", "EUCLIDEAN_TRACE_252_105"]


class BridgeError(RuntimeError):
    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message


def reject(code: str, message: str) -> None:
    raise BridgeError(code, message)


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        reject("JSON_LOAD_FAILED", f"{path}: {exc}")


def git_blob_sha1(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def schema_validate(value: Any, schema_path: Path, code: str) -> None:
    schema = load_json(schema_path)
    errors = sorted(Draft202012Validator(schema).iter_errors(value), key=lambda e: list(e.path))
    if errors:
        reject(code, errors[0].message)


def validate_authority(record: dict[str, Any]) -> None:
    if record.get("operation_id") != "CMDG-EUCLID-BRIDGE-001" or record.get("protected_baseline") != BASELINE:
        reject("AUTHORITY_BASELINE_DRIFT", str(record.get("protected_baseline")))
    a = record["euclid_authority"]
    if a["programme_closeout_blob_sha1"] != CLOSEOUT_BLOB or git_blob_sha1(CLOSEOUT) != CLOSEOUT_BLOB:
        reject("EUCLID_CLOSEOUT_IDENTITY_DRIFT", git_blob_sha1(CLOSEOUT))
    if a["mathcert_merge_commit"] != MATHCERT_COMMIT or a["mathcert_source_blob_sha1"] != MATHCERT_SOURCE_BLOB:
        reject("MATHCERT_SOURCE_IDENTITY_DRIFT", str(a))
    if a["roots"] != ORIGINAL_ROOTS:
        reject("EUCLID_THEOREM_ROOT_DRIFT", str(a["roots"]))


def validate_environments(record: dict[str, Any]) -> None:
    original = record["original_proof_environment"]
    if original != {
        "lean_toolchain": "leanprover/lean4:v4.29.1",
        "toolchain_blob_sha1": ORIGINAL_TOOLCHAIN_BLOB,
        "lake_manifest_blob_sha1": ORIGINAL_MANIFEST_BLOB,
        "mathcert_commit": MATHCERT_COMMIT,
    }:
        reject("ORIGINAL_ENVIRONMENT_DRIFT", str(original))
    bridge = record["bridge_proof_environment"]
    if git_blob_sha1(TOOLCHAIN) != BRIDGE_TOOLCHAIN_BLOB or git_blob_sha1(MANIFEST) != BRIDGE_MANIFEST_BLOB:
        reject("BRIDGE_ENVIRONMENT_PIN_DRIFT", "local Lean pins changed")
    if bridge["toolchain_blob_sha1"] != BRIDGE_TOOLCHAIN_BLOB or bridge["lake_manifest_blob_sha1"] != BRIDGE_MANIFEST_BLOB or bridge["mathlib_commit"] != MATHLIB:
        reject("BRIDGE_RECORDED_PIN_DRIFT", str(bridge))
    if bridge["root"] != BRIDGE_ROOT:
        reject("BRIDGE_ROOT_DRIFT", bridge["root"])


def validate_scope(record: dict[str, Any]) -> None:
    scope = record["semantic_scope"]
    if scope["transport_route"] != ["N_DTT", "N_NNO", "N_ZFC"]:
        reject("TRANSPORT_DIRECTION_DRIFT", str(scope["transport_route"]))
    if scope["admitted_operation_dependencies"] != OPS:
        reject("NAT_OPERATION_SCOPE_DRIFT", str(scope["admitted_operation_dependencies"]))
    if scope["transported_objects"] != TRANSPORTED:
        reject("TRANSPORT_OBJECT_SCOPE_DRIFT", str(scope["transported_objects"]))
    if scope["gcd_function_transport"] != "NOT_ADMITTED":
        reject("GCD_FUNCTION_TRANSPORT_OVERCLAIM", scope["gcd_function_transport"])
    if scope["bezout_integer_transport"] != "OUT_OF_SCOPE_PENDING_INTEGER_CONCORDANCE":
        reject("INTEGER_BEZOUT_TRANSPORT_OVERCLAIM", scope["bezout_integer_transport"])
    if scope["zfc_scope"] != "FINITE_VON_NEUMANN_IMAGE_ONLY":
        reject("SYNTACTIC_ZFC_OVERCLAIM", scope["zfc_scope"])


def validate_formal_bridge(record: dict[str, Any]) -> None:
    source = BRIDGE_SOURCE.read_text(encoding="utf-8")
    required = [
        "def DTTIsGCD", "def NNOIsGCD", "def ZFCFiniteImageIsGCD",
        "theorem dtt_to_nno_gcd", "theorem nno_to_zfc_finite_image_gcd",
        "theorem dtt_gcd_252_105_21", "theorem dtt_trace_252_105",
        "theorem nno_trace_252_105", "theorem zfc_finite_image_trace_252_105",
        "theorem euclid_gcd_relational_bridge",
    ]
    missing = [needle for needle in required if needle not in source]
    if missing:
        reject("FORMAL_BRIDGE_DECLARATION_MISSING", str(missing))
    if re.search(r"^[ \t]*(sorry|axiom)(?:[ \t]|$)", source, re.MULTILINE):
        reject("FORMAL_PLACEHOLDER_OR_AXIOM", "bridge contains sorry or local axiom")
    if re.search(r"theorem\s+\w*bezout", source, re.IGNORECASE):
        reject("INTEGER_BEZOUT_SCOPE_VIOLATION", "bridge must not reconstruct/transport Bezout")
    formal = record["formal_bridge"]
    if formal["root"] != BRIDGE_ROOT or formal["source"] != str(BRIDGE_SOURCE.relative_to(ROOT)):
        reject("FORMAL_BINDING_DRIFT", str(formal))


def validate_graph(record: dict[str, Any]) -> None:
    nodes = load_json(NODES)
    edges = load_json(EDGES)
    if not isinstance(nodes, list) or not nodes:
        reject("NODE_SET_MALFORMED", "nodes must be nonempty")
    if not isinstance(edges, list) or not edges:
        reject("EDGE_SET_MALFORMED", "edges must be nonempty")
    node_ids = set()
    for node in nodes:
        schema_validate(node, NODE_SCHEMA, "NODE_SCHEMA_VIOLATION")
        if node["node_id"] in node_ids:
            reject("DUPLICATE_NODE", node["node_id"])
        node_ids.add(node["node_id"])
    edge_ids = set()
    for edge in edges:
        schema_validate(edge, EDGE_SCHEMA, "EDGE_SCHEMA_VIOLATION")
        if edge["edge_id"] in edge_ids:
            reject("DUPLICATE_EDGE", edge["edge_id"])
        edge_ids.add(edge["edge_id"])
        if edge["layer"] in {"G_semantic", "CROSS_LAYER"} and edge["authority_state"] != "PROPOSED":
            reject("UNREVIEWED_SEMANTIC_AUTHORITY", edge["edge_id"])
        if edge["layer"] in {"G_proof", "G_implementation", "G_provenance"} and edge["authority_state"] != "OBSERVED":
            reject("NONSEMANTIC_AUTHORITY_DRIFT", edge["edge_id"])
        if edge["relation"] == "REALIZES_AS" and any(edge["realization"]["automatic_claims"].values()):
            reject("REALIZATION_AUTOMATIC_OVERCLAIM", edge["edge_id"])
    if record["graph"] != {
        "nodes": "fixtures/cmdg/euclid_bridge_001/nodes.json",
        "edges": "fixtures/cmdg/euclid_bridge_001/edges.json",
        "semantic_edge_authority": "PROPOSED",
        "derived_closure_authoritative": False,
    }:
        reject("GRAPH_BINDING_DRIFT", str(record["graph"]))


def validate_extractors() -> None:
    original = load_json(ORIGINAL_CONFIG)
    if original["project_dir"] != "external/MATHCERT" or original["module"] != "MathCert.Domains.NumberTheory.EuclidGCD" or original["roots"] != ORIGINAL_ROOTS:
        reject("ORIGINAL_EXTRACTOR_ROOT_DRIFT", str(original.get("roots")))
    if original["expected_toolchain_git_blob_sha1"] != ORIGINAL_TOOLCHAIN_BLOB or original["expected_lake_manifest_git_blob_sha1"] != ORIGINAL_MANIFEST_BLOB:
        reject("ORIGINAL_EXTRACTOR_PIN_DRIFT", "MATHCERT extractor pins changed")
    bridge = load_json(BRIDGE_CONFIG)
    if bridge["roots"] != [BRIDGE_ROOT] or bridge["module"] != "CMDGEuclidBridge":
        reject("BRIDGE_EXTRACTOR_ROOT_DRIFT", str(bridge.get("roots")))
    if bridge["expected_toolchain_git_blob_sha1"] != BRIDGE_TOOLCHAIN_BLOB or bridge["expected_lake_manifest_git_blob_sha1"] != BRIDGE_MANIFEST_BLOB:
        reject("BRIDGE_EXTRACTOR_PIN_DRIFT", "bridge extractor pins changed")
    for config in (original, bridge):
        boundary = config.get("claim_boundary", {})
        if any(boundary.values()):
            reject("EXTRACTOR_AUTHORITY_PROMOTION", str(boundary))


def validate_workflow_binding() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")
    for needle in (MATHCERT_COMMIT, MATHCERT_SOURCE_BLOB, "euclid_gcd_original.json", "euclid_bridge.json"):
        if needle not in text:
            reject("WORKFLOW_AUTHORITY_BINDING_MISSING", needle)


def validate_claim_boundary(record: dict[str, Any]) -> None:
    b = record["claim_boundary"]
    prohibited = [
        "original_euclid_certification_modified", "new_or_stronger_gcd_theorem_conferred",
        "nat_gcd_function_transport_conferred", "integer_bezout_transport_conferred",
        "syntactic_zfc_realization_conferred", "foundational_equivalence_conferred",
        "dependency_minimality_claim", "global_dependency_completeness_claim", "graph_certified_conferred",
    ]
    if any(b[k] for k in prohibited):
        reject("PROHIBITED_AUTHORITY_PROMOTION", str({k: b[k] for k in prohibited}))
    if not b["independent_review_required"] or not b["protected_admission_required"]:
        reject("ADMISSION_GATE_BYPASS", "review and protected admission remain mandatory")
    if not b["c04_c05_c06_unchanged"]:
        reject("UNRELATED_CORRECTION_GATE_DRIFT", "C04-C06 must remain unchanged")


def validate_record(record: dict[str, Any]) -> None:
    validate_authority(record)
    validate_environments(record)
    validate_scope(record)
    validate_formal_bridge(record)
    validate_graph(record)
    validate_extractors()
    validate_workflow_binding()
    validate_claim_boundary(record)


def main() -> int:
    try:
        record = load_json(RECORD)
        if not isinstance(record, dict):
            reject("RECORD_ROOT_MALFORMED", "bridge record must be an object")
        validate_record(record)
    except BridgeError as exc:
        print(f"CMDG Euclid bridge validation FAILED [{exc.code}]: {exc.message}")
        return 1
    print("CMDG Euclid bridge validation PASS")
    print("scope: bounded relational gcd and trace bridge only; Nat.gcd-function and Int-Bezout transport remain outside authority")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
