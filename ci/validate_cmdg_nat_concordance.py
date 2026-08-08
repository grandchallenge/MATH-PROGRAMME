#!/usr/bin/env python3
"""Fail-closed validation for CMDG-NAT-CONCORDANCE-001."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "cmdg_nat_concordance.schema.json"
RECORD = ROOT / "governance" / "cmdg_nat_concordance_001.json"
PROFILE = ROOT / "governance" / "cmdg_nat_concordance_foundations_profile_001.json"
NODE_SCHEMA = ROOT / "schemas" / "cmdg_node.schema.json"
EDGE_SCHEMA = ROOT / "schemas" / "cmdg_edge.schema.json"
NODES = ROOT / "fixtures" / "cmdg" / "nat_concordance_001" / "nodes.json"
EDGES = ROOT / "fixtures" / "cmdg" / "nat_concordance_001" / "edges.json"
LEAN_SOURCE = ROOT / "fixtures" / "formal" / "CMDG-NAT-CONCORDANCE-001" / "CMDGNatConcordance.lean"
TOOLCHAIN = ROOT / "fixtures" / "formal" / "CMDG-NAT-CONCORDANCE-001" / "lean-toolchain"
MANIFEST = ROOT / "fixtures" / "formal" / "CMDG-NAT-CONCORDANCE-001" / "lake-manifest.json"
EXTRACTOR_CONFIG = ROOT / "fixtures" / "cmdg" / "extractor_001" / "nat_concordance.json"

EXPECTED_BASELINE = "f518ae19aa46733c77727ee353983721aa8ffa85"
EXPECTED_PROFILE = "CMDG-NAT-CONCORDANCE-FOUNDATIONS-PROFILE-001"
EXPECTED_TOOLCHAIN_BLOB = "fd85b262bf1c734663aa8292b0101f672168788f"
EXPECTED_MANIFEST_BLOB = "9e478e09f622406970dc9613f6cf323ade82f787"
EXPECTED_MATHLIB = "79d0395a1825a6264ad5d269e35e60537518955e"
MAPS = {
    "CMDG:NAT:MAP:DTT_TO_ZFC": ("N_DTT", "N_ZFC"),
    "CMDG:NAT:MAP:DTT_TO_NNO": ("N_DTT", "N_NNO"),
    "CMDG:NAT:MAP:NNO_TO_ZFC": ("N_NNO", "N_ZFC"),
}
OPERATIONS = {"ZERO", "SUCCESSOR", "ADDITION", "MULTIPLICATION", "ORDER", "DIVISIBILITY"}
EXPECTED_THEOREMS = {
    ("CMDG:NAT:MAP:DTT_TO_ZFC", "ZERO"): "CMDG.NatConcordance.zNat_zero",
    ("CMDG:NAT:MAP:DTT_TO_ZFC", "SUCCESSOR"): "CMDG.NatConcordance.zNat_succ",
    ("CMDG:NAT:MAP:DTT_TO_ZFC", "ADDITION"): "CMDG.NatConcordance.zAdd_zNat",
    ("CMDG:NAT:MAP:DTT_TO_ZFC", "MULTIPLICATION"): "CMDG.NatConcordance.zMul_zNat",
    ("CMDG:NAT:MAP:DTT_TO_ZFC", "ORDER"): "CMDG.NatConcordance.zLe_zNat",
    ("CMDG:NAT:MAP:DTT_TO_ZFC", "DIVISIBILITY"): "CMDG.NatConcordance.zDvd_zNat",
    ("CMDG:NAT:MAP:DTT_TO_NNO", "ZERO"): "CMDG.NatConcordance.dttToNNO_zero",
    ("CMDG:NAT:MAP:DTT_TO_NNO", "SUCCESSOR"): "CMDG.NatConcordance.dttToNNO_succ",
    ("CMDG:NAT:MAP:DTT_TO_NNO", "ADDITION"): "CMDG.NatConcordance.dttToNNO_add",
    ("CMDG:NAT:MAP:DTT_TO_NNO", "MULTIPLICATION"): "CMDG.NatConcordance.dttToNNO_mul",
    ("CMDG:NAT:MAP:DTT_TO_NNO", "ORDER"): "CMDG.NatConcordance.dttToNNO_le",
    ("CMDG:NAT:MAP:DTT_TO_NNO", "DIVISIBILITY"): "CMDG.NatConcordance.dttToNNO_dvd",
    ("CMDG:NAT:MAP:NNO_TO_ZFC", "ZERO"): "CMDG.NatConcordance.nnoToZfc_zero",
    ("CMDG:NAT:MAP:NNO_TO_ZFC", "SUCCESSOR"): "CMDG.NatConcordance.nnoToZfc_succ",
    ("CMDG:NAT:MAP:NNO_TO_ZFC", "ADDITION"): "CMDG.NatConcordance.nnoToZfc_add",
    ("CMDG:NAT:MAP:NNO_TO_ZFC", "MULTIPLICATION"): "CMDG.NatConcordance.nnoToZfc_mul",
    ("CMDG:NAT:MAP:NNO_TO_ZFC", "ORDER"): "CMDG.NatConcordance.nnoToZfc_le",
    ("CMDG:NAT:MAP:NNO_TO_ZFC", "DIVISIBILITY"): "CMDG.NatConcordance.nnoToZfc_dvd",
}


class ConcordanceError(RuntimeError):
    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message


def reject(code: str, message: str) -> None:
    raise ConcordanceError(code, message)


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        reject("JSON_LOAD_FAILED", f"{path}: {exc}")


def validate_json_schema(value: Any, schema_path: Path, code: str) -> None:
    schema = load_json(schema_path)
    Draft202012Validator.check_schema(schema)
    errors = sorted(Draft202012Validator(schema).iter_errors(value), key=lambda e: list(e.path))
    if errors:
        err = errors[0]
        path = ".".join(str(p) for p in err.path) or "<root>"
        reject(code, f"{path}: {err.message}")


def git_blob_sha1(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def validate_profile_binding(record: dict[str, Any]) -> None:
    if record["protected_baseline"] != EXPECTED_BASELINE:
        reject("PROTECTED_BASELINE_DRIFT", record["protected_baseline"])
    binding = record["foundational_profile"]
    if binding["profile_id"] != EXPECTED_PROFILE or binding["protected_merge"] != EXPECTED_BASELINE:
        reject("FOUNDATIONAL_PROFILE_BINDING_DRIFT", str(binding))
    profile = load_json(PROFILE)
    if profile.get("profile_id") != EXPECTED_PROFILE or profile.get("schema_version") != "1.0.0":
        reject("FOUNDATIONAL_PROFILE_IDENTITY_DRIFT", str(profile.get("profile_id")))
    if profile["semantic_set_realization_profile"]["programme_realizes_as_status"] != "NOT_ADMITTED":
        reject("SYNTACTIC_ZFC_REALIZATION_OVERCLAIM", "profile boundary no longer matches admitted prerequisite")


def validate_environment(record: dict[str, Any]) -> None:
    env = record["proof_environment"]
    if git_blob_sha1(TOOLCHAIN) != EXPECTED_TOOLCHAIN_BLOB:
        reject("LEAN_TOOLCHAIN_PIN_DRIFT", git_blob_sha1(TOOLCHAIN))
    if git_blob_sha1(MANIFEST) != EXPECTED_MANIFEST_BLOB:
        reject("LAKE_MANIFEST_PIN_DRIFT", git_blob_sha1(MANIFEST))
    manifest = load_json(MANIFEST)
    mathlib = [p for p in manifest.get("packages", []) if isinstance(p, dict) and p.get("name") == "mathlib"]
    if len(mathlib) != 1 or mathlib[0].get("rev") != EXPECTED_MATHLIB:
        reject("MATHLIB_PIN_DRIFT", str(mathlib))
    if env["toolchain_blob_sha1"] != EXPECTED_TOOLCHAIN_BLOB or env["lake_manifest_blob_sha1"] != EXPECTED_MANIFEST_BLOB:
        reject("RECORDED_PIN_DRIFT", str(env))


def validate_realizations(record: dict[str, Any]) -> None:
    r = record["realizations"]
    if set(r) != {"N_DTT", "N_ZFC", "N_NNO"}:
        reject("REALIZATION_IDENTITY_DRIFT", str(sorted(r)))
    if r["N_DTT"]["formal_locator"] != "Nat":
        reject("DTT_IDENTITY_DRIFT", r["N_DTT"]["formal_locator"])
    if r["N_ZFC"]["formal_locator"] != "CMDG.NatConcordance.zNat":
        reject("ZFC_NAT_IDENTITY_DRIFT", r["N_ZFC"]["formal_locator"])
    if r["N_NNO"]["formal_locator"] != "CMDG.NatConcordance.natTypeNNO":
        reject("NNO_IDENTITY_DRIFT", r["N_NNO"]["formal_locator"])
    if any(item["definitional_identity_to_other_foundations"] for item in r.values()):
        reject("DEFINITIONAL_IDENTITY_OVERCLAIM", "foundational realizations must remain distinct")


def validate_transports(record: dict[str, Any]) -> None:
    maps = record["transport_maps"]
    by_id = {item["map_id"]: item for item in maps}
    if set(by_id) != set(MAPS) or len(by_id) != len(maps):
        reject("TRANSPORT_MAP_SET_DRIFT", str(sorted(by_id)))
    for map_id, (source, target) in MAPS.items():
        item = by_id[map_id]
        if (item["source"], item["target"]) != (source, target):
            reject("TRANSPORT_DIRECTION_DRIFT", map_id)
    matrix = record["operation_matrix"]
    keys = [(item["map_id"], item["operation"]) for item in matrix]
    if len(keys) != len(set(keys)):
        reject("DUPLICATE_OPERATION_EVIDENCE", "duplicate map/operation pair")
    expected_keys = {(m, op) for m in MAPS for op in OPERATIONS}
    if set(keys) != expected_keys:
        reject("INCOMPLETE_OPERATION_MATRIX", f"missing={sorted(expected_keys - set(keys))}")
    source = LEAN_SOURCE.read_text(encoding="utf-8")
    for item in matrix:
        key = (item["map_id"], item["operation"])
        expected = EXPECTED_THEOREMS[key]
        if item["theorem"] != expected:
            reject("OPERATION_THEOREM_DRIFT", f"{key}: {item['theorem']} != {expected}")
        short = expected.rsplit(".", 1)[1]
        if f"theorem {short}" not in source:
            reject("FORMAL_THEOREM_MISSING", expected)
    if "theorem bounded_concordance" not in source or "structure TypeNNO" not in source:
        reject("FORMAL_ROOT_MISSING", "bounded concordance or NNO universal contract missing")


def validate_graph(record: dict[str, Any]) -> None:
    nodes = load_json(NODES)
    edges = load_json(EDGES)
    if not isinstance(nodes, list) or len(nodes) != 3:
        reject("NODE_SET_MALFORMED", "expected exactly three natural-number realization nodes")
    if not isinstance(edges, list) or len(edges) != 6:
        reject("EDGE_SET_MALFORMED", "expected three transport and three realization proposals")
    for node in nodes:
        validate_json_schema(node, NODE_SCHEMA, "NODE_SCHEMA_VIOLATION")
    node_ids = {node["node_id"] for node in nodes}
    if node_ids != {"CMDG:NAT:N_DTT", "CMDG:NAT:N_ZFC", "CMDG:NAT:N_NNO"}:
        reject("NODE_IDENTITY_DRIFT", str(sorted(node_ids)))
    for edge in edges:
        validate_json_schema(edge, EDGE_SCHEMA, "EDGE_SCHEMA_VIOLATION")
        if edge["authority_state"] != "PROPOSED":
            reject("UNREVIEWED_DIRECT_AUTHORITY", edge["edge_id"])
        if edge["relation"] == "REALIZES_AS":
            if any(edge["realization"]["automatic_claims"].values()):
                reject("REALIZATION_AUTOMATIC_OVERCLAIM", edge["edge_id"])
    if record["graph_authority"]["edge_authority_state"] != "PROPOSED":
        reject("GRAPH_AUTHORITY_PROMOTION", record["graph_authority"]["edge_authority_state"])


def validate_extractor(record: dict[str, Any]) -> None:
    config = load_json(EXTRACTOR_CONFIG)
    root = record["formal_evidence"]["root_theorem"]
    if config.get("roots") != [root]:
        reject("EXTRACTOR_ROOT_DRIFT", str(config.get("roots")))
    expected = record["formal_evidence"]["expected_axioms"]
    if config.get("expected_axioms", {}).get(root) != expected:
        reject("AXIOM_EXPECTATION_DRIFT", str(config.get("expected_axioms")))
    boundary = config.get("claim_boundary", {})
    if any(boundary.values()):
        reject("EXTRACTOR_AUTHORITY_PROMOTION", str(boundary))


def validate_claim_boundary(record: dict[str, Any]) -> None:
    b = record["claim_boundary"]
    if not b["bounded_foundational_concordance_candidate"]:
        reject("CANDIDATE_SCOPE_LOST", "bounded concordance candidate flag must remain true")
    prohibited = {
        "conferred_by_artifact_alone",
        "foundational_equivalence_conferred",
        "consistency_claim",
        "standard_model_claim",
        "graph_certified_conferred",
        "global_dependency_completeness_claim",
    }
    if any(b[key] for key in prohibited):
        reject("PROHIBITED_AUTHORITY_PROMOTION", str({k: b[k] for k in prohibited}))
    if not b["independent_review_required"] or not b["protected_admission_required"]:
        reject("ADMISSION_GATE_BYPASS", "independent review and protected admission are mandatory")
    if not b["c04_c05_c06_unchanged"]:
        reject("UNRELATED_CORRECTION_GATE_DRIFT", "C04-C06 must remain unchanged")


def validate_record(record: dict[str, Any]) -> None:
    validate_json_schema(record, SCHEMA, "SCHEMA_VIOLATION")
    validate_profile_binding(record)
    validate_environment(record)
    validate_realizations(record)
    validate_transports(record)
    validate_graph(record)
    validate_extractor(record)
    validate_claim_boundary(record)


def main() -> int:
    try:
        record = load_json(RECORD)
        if not isinstance(record, dict):
            reject("RECORD_ROOT_MALFORMED", "concordance record must be an object")
        validate_record(record)
    except ConcordanceError as exc:
        print(f"CMDG NAT concordance validation FAILED [{exc.code}]: {exc.message}")
        return 1
    print("CMDG NAT concordance validation PASS")
    print("scope: bounded machine-checked candidate only; independent review and protected admission remain mandatory")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
