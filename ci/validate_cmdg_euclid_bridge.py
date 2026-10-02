#!/usr/bin/env python3
"""Fail-closed validator for CMDG-EUCLID-BRIDGE-001."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
P = lambda *x: ROOT.joinpath(*x)
RECORD = P("governance", "cmdg_euclid_bridge_001.json")
NODES = P("fixtures", "cmdg", "euclid_bridge_001", "nodes.json")
EDGES = P("fixtures", "cmdg", "euclid_bridge_001", "edges.json")
NODE_SCHEMA = P("schemas", "cmdg_node.schema.json")
EDGE_SCHEMA = P("schemas", "cmdg_edge.schema.json")
SOURCE = P("fixtures", "formal", "CMDG-NAT-CONCORDANCE-001", "CMDGEuclidBridge.lean")
TOOL = P("fixtures", "formal", "CMDG-NAT-CONCORDANCE-001", "lean-toolchain")
MAN = P("fixtures", "formal", "CMDG-NAT-CONCORDANCE-001", "lake-manifest.json")
CLOSE = P("governance", "euclid_gcd_e2e_001_closeout.json")
OCFG = P("fixtures", "cmdg", "extractor_001", "euclid_gcd_original.json")
BCFG = P("fixtures", "cmdg", "extractor_001", "euclid_bridge.json")
WF = P(".github", "workflows", "cmdg-euclid-bridge.yml")
SHARED_WF = P(".github", "workflows", "cmdg-formal-lane-replay.yml")
FORMAL_REGISTRY = P("governance", "formal_validation_registry.json")
BASE = "25f5fef222433f60f28b375d6ea814b844b5b062"
CLOSE_BLOB = "a5e390ee01b23862a79d53a7cac1c0d6f0930608"
MC = "78b69e6a3461a83f4893d61c421b1570c08a9ba6"
MC_SRC = "bf0ab5bac117490299ff5bffb8ca59263ec3f2a3"
OT = "33e0c088939ad08c9f2b1befa3118a423b06ad7d"
OM = "4d92c79ff638dceb6c44472e1e96bbac9cebcdfd"
BT = "fd85b262bf1c734663aa8292b0101f672168788f"
BM = "9e478e09f622406970dc9613f6cf323ade82f787"
ML = "79d0395a1825a6264ad5d269e35e60537518955e"
ROOTS = [
    "MathCert.NumberTheory.acceptedGCDCertificate_sound",
    "MathCert.NumberTheory.euclidTrace252105",
    "MathCert.NumberTheory.bezout252105",
    "MathCert.NumberTheory.gcd252105",
    "MathCert.NumberTheory.accepted252105",
    "MathCert.NumberTheory.accepted252105_sound",
]
BROOT = "CMDG.EuclidBridge.euclid_gcd_relational_bridge"
OPS = ["ZERO", "SUCCESSOR", "ADDITION", "MULTIPLICATION", "ORDER", "DIVISIBILITY"]


class BridgeError(RuntimeError):
    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message


def reject(code: str, message: str) -> None:
    raise BridgeError(code, message)


def load(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        reject("JSON_LOAD_FAILED", f"{path}: {exc}")


def blob(path: Path) -> str:
    payload = path.read_bytes()
    return hashlib.sha1(f"blob {len(payload)}\0".encode() + payload).hexdigest()


def schema(value, path: Path, code: str) -> None:
    errors = sorted(Draft202012Validator(load(path)).iter_errors(value), key=lambda e: list(e.path))
    if errors:
        reject(code, errors[0].message)


def validate_execution_binding() -> None:
    """Bind execution to the governed formal lane without duplicating theorem authority in YAML."""
    registry = load(FORMAL_REGISTRY)
    lanes = [lane for lane in registry.get("lanes", []) if lane.get("id") == "cmdg-euclid-bridge"]
    if len(lanes) != 1:
        reject("FORMAL_LANE_BINDING_DRIFT", f"expected one cmdg-euclid-bridge lane, found {len(lanes)}")
    lane = lanes[0]
    expected = {
        "family": "CMDG",
        "execution_kind": "cmdg-lean-closure",
        "package_dir": "fixtures/formal/CMDG-NAT-CONCORDANCE-001",
        "promotion_workflow": ".github/workflows/cmdg-euclid-bridge.yml",
        "development_targets": ["CMDGEuclidBridge.lean"],
        "formal_sources": ["CMDGEuclidBridge.lean"],
    }
    for key, value in expected.items():
        if lane.get(key) != value:
            reject("FORMAL_LANE_BINDING_DRIFT", f"{key}: {lane.get(key)!r} != {value!r}")
    source_path = "fixtures/formal/CMDG-NAT-CONCORDANCE-001/CMDGEuclidBridge.lean"
    if source_path not in lane.get("material_patterns", []):
        reject("FORMAL_LANE_BINDING_DRIFT", "Euclid source missing from material closure")
    if ["python3", "ci/validate_cmdg_euclid_bridge.py"] not in lane.get("validator_commands", []):
        reject("FORMAL_LANE_BINDING_DRIFT", "Euclid validator missing from lane commands")

    workflow = WF.read_text(encoding="utf-8")
    for marker in (
        "workflow_call:",
        "workflow_dispatch:",
        "uses: ./.github/workflows/cmdg-formal-lane-replay.yml",
        "lane: cmdg-euclid-bridge",
    ):
        if marker not in workflow:
            reject("WORKFLOW_EXECUTION_BINDING_MISSING", marker)
    for forbidden in ("pull_request:", "push:", "schedule:"):
        if forbidden in workflow:
            reject("WORKFLOW_EXECUTION_SCOPE_DRIFT", forbidden)

    shared = SHARED_WF.read_text(encoding="utf-8")
    for marker in (
        'run: test "$GITHUB_REF" = "refs/heads/main"',
        'ci/formal_validation.py run --lane "${{ inputs.lane }}" --mode promotion',
    ):
        if marker not in shared:
            reject("WORKFLOW_EXECUTION_BINDING_MISSING", marker)


def validate_record(r: dict[str, Any]) -> None:
    if r.get("operation_id") != "CMDG-EUCLID-BRIDGE-001" or r.get("protected_baseline") != BASE:
        reject("AUTHORITY_BASELINE_DRIFT", str(r.get("protected_baseline")))
    authority = r["euclid_authority"]
    if authority["programme_closeout_blob_sha1"] != CLOSE_BLOB or blob(CLOSE) != CLOSE_BLOB:
        reject("EUCLID_CLOSEOUT_IDENTITY_DRIFT", blob(CLOSE))
    if authority["mathcert_merge_commit"] != MC or authority["mathcert_source_blob_sha1"] != MC_SRC:
        reject("MATHCERT_SOURCE_IDENTITY_DRIFT", str(authority))
    if authority["roots"] != ROOTS:
        reject("EUCLID_THEOREM_ROOT_DRIFT", str(authority["roots"]))
    if r["original_proof_environment"] != {
        "lean_toolchain": "leanprover/lean4:v4.29.1",
        "toolchain_blob_sha1": OT,
        "lake_manifest_blob_sha1": OM,
        "mathcert_commit": MC,
    }:
        reject("ORIGINAL_ENVIRONMENT_DRIFT", str(r["original_proof_environment"]))
    bridge = r["bridge_proof_environment"]
    if blob(TOOL) != BT or blob(MAN) != BM:
        reject("BRIDGE_ENVIRONMENT_PIN_DRIFT", "local pins changed")
    if (
        bridge["toolchain_blob_sha1"],
        bridge["lake_manifest_blob_sha1"],
        bridge["mathlib_commit"],
        bridge["root"],
    ) != (BT, BM, ML, BROOT):
        reject("BRIDGE_RECORDED_PIN_DRIFT", str(bridge))

    scope = r["semantic_scope"]
    if scope["transport_route"] != ["N_DTT", "N_NNO", "N_ZFC"]:
        reject("TRANSPORT_DIRECTION_DRIFT", str(scope["transport_route"]))
    if scope["admitted_operation_dependencies"] != OPS:
        reject("NAT_OPERATION_SCOPE_DRIFT", str(scope["admitted_operation_dependencies"]))
    if scope["transported_objects"] != ["RELATIONAL_GCD_SPECIFICATION", "EUCLIDEAN_TRACE_252_105"]:
        reject("TRANSPORT_OBJECT_SCOPE_DRIFT", str(scope["transported_objects"]))
    if scope["gcd_function_transport"] != "NOT_ADMITTED":
        reject("GCD_FUNCTION_TRANSPORT_OVERCLAIM", scope["gcd_function_transport"])
    if scope["bezout_integer_transport"] != "OUT_OF_SCOPE_PENDING_INTEGER_CONCORDANCE":
        reject("INTEGER_BEZOUT_TRANSPORT_OVERCLAIM", scope["bezout_integer_transport"])
    if scope["zfc_scope"] != "FINITE_VON_NEUMANN_IMAGE_ONLY":
        reject("SYNTACTIC_ZFC_OVERCLAIM", scope["zfc_scope"])

    text = SOURCE.read_text(encoding="utf-8")
    declarations = [
        "def DTTIsGCD",
        "def NNOIsGCD",
        "def ZFCFiniteImageIsGCD",
        "theorem dtt_to_nno_gcd",
        "theorem nno_to_zfc_finite_image_gcd",
        "theorem dtt_gcd_252_105_21",
        "theorem dtt_trace_252_105",
        "theorem nno_trace_252_105",
        "theorem zfc_finite_image_trace_252_105",
        "theorem euclid_gcd_relational_bridge",
    ]
    for declaration in declarations:
        if declaration not in text:
            reject("FORMAL_BRIDGE_DECLARATION_MISSING", declaration)
    if re.search(r"^[ \t]*(sorry|axiom)(?:[ \t]|$)", text, re.M):
        reject("FORMAL_PLACEHOLDER_OR_AXIOM", "sorry/axiom")
    if re.search(r"theorem\s+\w*bezout", text, re.I):
        reject("INTEGER_BEZOUT_SCOPE_VIOLATION", "local Bezout theorem")
    if r["formal_bridge"]["root"] != BROOT or r["formal_bridge"]["source"] != str(SOURCE.relative_to(ROOT)):
        reject("FORMAL_BINDING_DRIFT", str(r["formal_bridge"]))

    nodes = load(NODES)
    edges = load(EDGES)
    seen: set[str] = set()
    for node in nodes:
        schema(node, NODE_SCHEMA, "NODE_SCHEMA_VIOLATION")
        if node["node_id"] in seen:
            reject("DUPLICATE_NODE", node["node_id"])
        seen.add(node["node_id"])
    seen = set()
    for edge in edges:
        schema(edge, EDGE_SCHEMA, "EDGE_SCHEMA_VIOLATION")
        if edge["edge_id"] in seen:
            reject("DUPLICATE_EDGE", edge["edge_id"])
        seen.add(edge["edge_id"])
        if edge["layer"] in {"G_semantic", "CROSS_LAYER"} and edge["authority_state"] != "PROPOSED":
            reject("UNREVIEWED_SEMANTIC_AUTHORITY", edge["edge_id"])
        if edge["layer"] in {"G_proof", "G_implementation", "G_provenance"} and edge["authority_state"] != "OBSERVED":
            reject("NONSEMANTIC_AUTHORITY_DRIFT", edge["edge_id"])
        if edge["relation"] == "REALIZES_AS" and any(edge["realization"]["automatic_claims"].values()):
            reject("REALIZATION_AUTOMATIC_OVERCLAIM", edge["edge_id"])
    if r["graph"]["semantic_edge_authority"] != "PROPOSED" or r["graph"]["derived_closure_authoritative"]:
        reject("GRAPH_BINDING_DRIFT", str(r["graph"]))

    original = load(OCFG)
    bridge_cfg = load(BCFG)
    if original["project_dir"] != "external/MATHCERT" or original["roots"] != ROOTS:
        reject("ORIGINAL_EXTRACTOR_ROOT_DRIFT", str(original["roots"]))
    if (original["expected_toolchain_git_blob_sha1"], original["expected_lake_manifest_git_blob_sha1"]) != (OT, OM):
        reject("ORIGINAL_EXTRACTOR_PIN_DRIFT", "pins")
    if bridge_cfg["roots"] != [BROOT] or bridge_cfg["module"] != "CMDGEuclidBridge":
        reject("BRIDGE_EXTRACTOR_ROOT_DRIFT", str(bridge_cfg["roots"]))
    if (bridge_cfg["expected_toolchain_git_blob_sha1"], bridge_cfg["expected_lake_manifest_git_blob_sha1"]) != (BT, BM):
        reject("BRIDGE_EXTRACTOR_PIN_DRIFT", "pins")
    if any(any(cfg["claim_boundary"].values()) for cfg in (original, bridge_cfg)):
        reject("EXTRACTOR_AUTHORITY_PROMOTION", "boundary")

    validate_execution_binding()

    claim_boundary = r["claim_boundary"]
    for key in [
        "original_euclid_certification_modified",
        "new_or_stronger_gcd_theorem_conferred",
        "nat_gcd_function_transport_conferred",
        "integer_bezout_transport_conferred",
        "syntactic_zfc_realization_conferred",
        "foundational_equivalence_conferred",
        "dependency_minimality_claim",
        "global_dependency_completeness_claim",
        "graph_certified_conferred",
    ]:
        if claim_boundary[key]:
            reject("PROHIBITED_AUTHORITY_PROMOTION", key)
    if not claim_boundary["independent_review_required"] or not claim_boundary["protected_admission_required"]:
        reject("ADMISSION_GATE_BYPASS", "review/protected admission")
    if not claim_boundary["c04_c05_c06_unchanged"]:
        reject("UNRELATED_CORRECTION_GATE_DRIFT", "C04-C06")


def main() -> int:
    try:
        validate_record(load(RECORD))
    except BridgeError as exc:
        print(f"CMDG Euclid bridge validation FAILED [{exc.code}]: {exc.message}")
        return 1
    print("CMDG Euclid bridge validation PASS")
    print("scope: relational gcd + trace only; Nat.gcd-function and Int-Bezout transport excluded")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
