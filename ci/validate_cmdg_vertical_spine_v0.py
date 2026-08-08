#!/usr/bin/env python3
"""Fail-closed validator for CMDG-VERTICAL-SPINE-V0-001."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
P = lambda *parts: ROOT.joinpath(*parts)

RECORD = P("governance", "cmdg_vertical_spine_v0_001.json")
NODES = P("fixtures", "cmdg", "vertical_spine_v0_001", "nodes.json")
EDGES = P("fixtures", "cmdg", "vertical_spine_v0_001", "edges.json")
NODE_SCHEMA = P("schemas", "cmdg_node.schema.json")
EDGE_SCHEMA = P("schemas", "cmdg_edge.schema.json")
LEAN_INTERFACE = P("fixtures", "formal", "CMDG-NAT-CONCORDANCE-001", "CMDGVerticalSpineV0.lean")
TOOLCHAIN = P("fixtures", "formal", "CMDG-NAT-CONCORDANCE-001", "lean-toolchain")
LAKE_MANIFEST = P("fixtures", "formal", "CMDG-NAT-CONCORDANCE-001", "lake-manifest.json")
NAT_RECORD = P("governance", "cmdg_nat_concordance_001.json")
EUCLID_RECORD = P("governance", "cmdg_euclid_bridge_001.json")
NAT_NODES = P("fixtures", "cmdg", "nat_concordance_001", "nodes.json")
EUCLID_NODES = P("fixtures", "cmdg", "euclid_bridge_001", "nodes.json")

BASE = "16a9e568e89cabbe989414ff8adb2599cdf24f5a"
BASE_TREE = "dc464829ec5b798a922d059364dc5b40f577c12e"
LEAN_COMMIT = "62eed1db4d67327ec8120be05f1a1b0847d74561"
MATHLIB_COMMIT = "79d0395a1825a6264ad5d269e35e60537518955e"
TOOLCHAIN_BLOB = "fd85b262bf1c734663aa8292b0101f672168788f"
MANIFEST_BLOB = "9e478e09f622406970dc9613f6cf323ade82f787"
NAT_RECORD_BLOB = "b06786dce9587149bdc6dba6bc32b037637dd379"
EUCLID_RECORD_BLOB = "ebff50f400a68e4c45852aad45dbc1aabdee559c"
NAT_NODES_BLOB = "955b593ae56accae2e71310c8cbc78842e0325ac"
EUCLID_NODES_BLOB = "1d58a548e549cf2751f4db32151d5c13af51ba86"

EXPECTED_NEW_NODES = {
    "CMDG:V0:LEAN_SUBSTRATE",
    "CMDG:V0:FOL_SEMANTICS",
    "CMDG:V0:ALGEBRA_RING_INTERFACE",
    "CMDG:V0:CATEGORY",
    "CMDG:V0:TOPOLOGICAL_SPACES",
    "CMDG:V0:COMPACT_HAUSDORFF",
    "CMDG:V0:PROFINITE",
    "CMDG:V0:GROTHENDIECK_TOPOLOGY",
    "CMDG:V0:COHERENT_TOPOLOGY_COMPHAUS",
    "CMDG:V0:SHEAF",
    "CMDG:V0:CONDENSED_SET",
    "CMDG:V0:DISCRETE_UNDERLYING_ADJUNCTION",
}
EXPECTED_SOURCE_PATHS = {
    "CMDG:V0:FOL_SEMANTICS": "Mathlib/ModelTheory/Semantics.lean",
    "CMDG:V0:ALGEBRA_RING_INTERFACE": "Mathlib/Algebra/Category/Ring/Basic.lean",
    "CMDG:V0:CATEGORY": "Mathlib/CategoryTheory/Category/Basic.lean",
    "CMDG:V0:TOPOLOGICAL_SPACES": "Mathlib/Topology/Category/TopCat/Basic.lean",
    "CMDG:V0:COMPACT_HAUSDORFF": "Mathlib/Topology/Category/CompHaus/Basic.lean",
    "CMDG:V0:PROFINITE": "Mathlib/Topology/Category/Profinite/Basic.lean",
    "CMDG:V0:GROTHENDIECK_TOPOLOGY": "Mathlib/CategoryTheory/Sites/Grothendieck.lean",
    "CMDG:V0:COHERENT_TOPOLOGY_COMPHAUS": "Mathlib/Condensed/Basic.lean",
    "CMDG:V0:SHEAF": "Mathlib/CategoryTheory/Sites/Sheaf.lean",
    "CMDG:V0:CONDENSED_SET": "Mathlib/Condensed/Basic.lean",
    "CMDG:V0:DISCRETE_UNDERLYING_ADJUNCTION": "Mathlib/Condensed/Discrete/Basic.lean",
}
EXPECTED_CHECKS = [
    "#check FirstOrder.Language",
    "#check RingCat",
    "#check CategoryTheory.Category",
    "#check TopCat",
    "#check CompHaus",
    "#check Profinite",
    "#check CategoryTheory.GrothendieckTopology",
    "#check CategoryTheory.Sheaf",
    "#check CategoryTheory.coherentTopology",
    "#check Condensed",
    "#check CondensedSet",
    "#check Condensed.discrete",
    "#check Condensed.underlying",
    "#check Condensed.discreteUnderlyingAdj",
]
EXPECTED_BACKTRACES = [
    ["CMDG:V0:DISCRETE_UNDERLYING_ADJUNCTION", "CMDG:V0:CONDENSED_SET", "CMDG:V0:SHEAF", "CMDG:V0:GROTHENDIECK_TOPOLOGY", "CMDG:V0:CATEGORY"],
    ["CMDG:V0:CONDENSED_SET", "CMDG:V0:COHERENT_TOPOLOGY_COMPHAUS", "CMDG:V0:COMPACT_HAUSDORFF", "CMDG:V0:TOPOLOGICAL_SPACES", "CMDG:V0:CATEGORY"],
    ["CMDG:V0:PROFINITE", "CMDG:V0:COMPACT_HAUSDORFF", "CMDG:V0:TOPOLOGICAL_SPACES", "CMDG:V0:CATEGORY"],
    ["CMDG:V0:ALGEBRA_RING_INTERFACE", "CMDG:V0:CATEGORY"],
]
EXPECTED_SEMANTIC_EDGES = {
    "CMDG:E:V0.RINGCAT.CATEGORY",
    "CMDG:E:V0.TOPCAT.CATEGORY",
    "CMDG:E:V0.COMPHAUS.TOPCAT",
    "CMDG:E:V0.PROFINITE.COMPHAUS",
    "CMDG:E:V0.COHERENT.COMPHAUS",
    "CMDG:E:V0.COHERENT.GROTHENDIECK",
    "CMDG:E:V0.SHEAF.GROTHENDIECK",
    "CMDG:E:V0.SHEAF.CATEGORY",
    "CMDG:E:V0.CONDENSED.SHEAF",
    "CMDG:E:V0.CONDENSED.COHERENT",
    "CMDG:E:V0.DISCRETE.CONDENSED",
}

class V0Error(RuntimeError):
    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message

def reject(code: str, message: str) -> None:
    raise V0Error(code, message)

def load(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        reject("JSON_LOAD_FAILED", f"{path}: {exc}")

def blob(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()

def schema(value: Any, path: Path, code: str) -> None:
    errors = sorted(Draft202012Validator(load(path)).iter_errors(value), key=lambda e: list(e.path))
    if errors:
        reject(code, errors[0].message)

def _edge_map(edges: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {e["edge_id"]: e for e in edges}

def validate_payload(record: dict[str, Any], nodes: list[dict[str, Any]], edges: list[dict[str, Any]],
                     lean_text: str) -> None:
    if record.get("schema_version") != "1.0.0" or record.get("operation_id") != "CMDG-VERTICAL-SPINE-V0-001":
        reject("OPERATION_IDENTITY_DRIFT", str(record.get("operation_id")))
    if (record.get("protected_baseline"), record.get("protected_baseline_tree")) != (BASE, BASE_TREE):
        reject("AUTHORITY_BASELINE_DRIFT", str((record.get("protected_baseline"), record.get("protected_baseline_tree"))))
    if record.get("predecessor_disposition") != "CMDG_EUCLID_BRIDGE_001_PROTECTED_CLOSED":
        reject("PREDECESSOR_DISPOSITION_DRIFT", str(record.get("predecessor_disposition")))

    env = record.get("environment", {})
    expected_env = {
        "lean_toolchain": "leanprover/lean4:v4.33.0-rc1",
        "lean_commit": LEAN_COMMIT,
        "toolchain_blob_sha1": TOOLCHAIN_BLOB,
        "lake_manifest_blob_sha1": MANIFEST_BLOB,
        "mathlib_repository": "leanprover-community/mathlib4",
        "mathlib_commit": MATHLIB_COMMIT,
    }
    if env != expected_env:
        reject("PROOF_ENVIRONMENT_DRIFT", str(env))

    reuse = {x.get("node_id"): x for x in record.get("protected_reuse", [])}
    if set(reuse) != {"CMDG:NAT:N_DTT", "CMDG:EUCLID:GCD:E2E001"}:
        reject("PROTECTED_REUSE_SET_DRIFT", str(sorted(reuse)))
    if reuse["CMDG:NAT:N_DTT"].get("artifact_blob_sha1") != NAT_RECORD_BLOB or reuse["CMDG:NAT:N_DTT"].get("node_fixture_blob_sha1") != NAT_NODES_BLOB:
        reject("NAT_REUSE_IDENTITY_DRIFT", str(reuse["CMDG:NAT:N_DTT"]))
    if reuse["CMDG:EUCLID:GCD:E2E001"].get("artifact_blob_sha1") != EUCLID_RECORD_BLOB or reuse["CMDG:EUCLID:GCD:E2E001"].get("node_fixture_blob_sha1") != EUCLID_NODES_BLOB:
        reject("EUCLID_REUSE_IDENTITY_DRIFT", str(reuse["CMDG:EUCLID:GCD:E2E001"]))
    if any(x.get("authority") != "PROTECTED_REUSE_NO_REDEFINITION" for x in reuse.values()):
        reject("PROTECTED_AUTHORITY_REDEFINITION", "protected anchors must be reused without redefinition")

    node_ids: set[str] = set()
    for node in nodes:
        schema(node, NODE_SCHEMA, "NODE_SCHEMA_VIOLATION")
        node_id = node["node_id"]
        if node_id in node_ids:
            reject("DUPLICATE_NODE", node_id)
        node_ids.add(node_id)
    if node_ids != EXPECTED_NEW_NODES:
        reject("V0_NODE_SET_DRIFT", str(sorted(node_ids ^ EXPECTED_NEW_NODES)))
    if any(n.get("engagement_mode") not in {"REUSED", "RECONSTRUCTED", "CONCORDANT"} for n in nodes):
        reject("UNCLASSIFIED_REUSE_MODE", "every V0 node must have an admitted engagement mode")
    modes = {n["node_id"]: n["engagement_mode"] for n in nodes}
    if modes["CMDG:V0:CONDENSED_SET"] != "CONCORDANT" or modes["CMDG:V0:DISCRETE_UNDERLYING_ADJUNCTION"] != "CONCORDANT":
        reject("CONDENSED_CONCORDANCE_OVERCLAIM", str(modes))
    if any(modes[n] != "REUSED" for n in EXPECTED_NEW_NODES - {"CMDG:V0:CONDENSED_SET", "CMDG:V0:DISCRETE_UNDERLYING_ADJUNCTION"}):
        reject("REUSE_CLASSIFICATION_DRIFT", str(modes))

    catalog = {x.get("node_id"): x.get("path") for x in record.get("source_catalog", [])}
    if catalog != EXPECTED_SOURCE_PATHS:
        reject("SOURCE_CATALOG_DRIFT", str(catalog))

    route = record.get("route", {})
    if route.get("start_node") != "CMDG:V0:LEAN_SUBSTRATE" or route.get("terminal_node") != "CMDG:V0:DISCRETE_UNDERLYING_ADJUNCTION":
        reject("V0_ENDPOINT_DRIFT", str((route.get("start_node"), route.get("terminal_node"))))
    if route.get("ordering_authoritative") is not False:
        reject("ROUTE_ORDER_AUTHORITY_OVERCLAIM", "expository route ordering must be non-authoritative")
    ordered = route.get("ordered_nodes", [])
    if not ordered or ordered[0] != route["start_node"] or ordered[-1] != route["terminal_node"]:
        reject("BROKEN_V0_ROUTE", str(ordered))
    if len(ordered) != len(set(ordered)):
        reject("DUPLICATE_ROUTE_NODE", str(ordered))
    required_route = EXPECTED_NEW_NODES | {"CMDG:NAT:N_DTT"}
    if set(ordered) != required_route:
        reject("ROUTE_NODE_COVERAGE_DRIFT", str(sorted(set(ordered) ^ required_route)))
    if route.get("dependency_backtraces") != EXPECTED_BACKTRACES:
        reject("DEPENDENCY_BACKTRACE_DRIFT", str(route.get("dependency_backtraces")))

    layers: set[str] = set()
    emap = _edge_map(edges)
    if len(emap) != len(edges):
        reject("DUPLICATE_EDGE", "edge ids must be unique")
    for edge in edges:
        schema(edge, EDGE_SCHEMA, "EDGE_SCHEMA_VIOLATION")
        edge_id = edge["edge_id"]
        layers.add(edge["layer"])
        if edge["layer"] == "G_semantic":
            if edge["authority_state"] != "PROPOSED":
                reject("UNREVIEWED_SEMANTIC_AUTHORITY", edge_id)
            if edge.get("proposal_origin", {}).get("origin") != "HUMAN":
                reject("TOOL_ORIGIN_SEMANTIC_AUTHORITY", edge_id)
        elif edge["authority_state"] != "OBSERVED":
            reject("NONSEMANTIC_AUTHORITY_DRIFT", edge_id)
        if edge["authority_state"] == "DERIVED":
            reject("DERIVED_EDGE_AS_DIRECT_AUTHORITY", edge_id)
        if edge["relation"] == "EQUIVALENT_TO":
            reject("UNCERTIFIED_EQUIVALENCE_IN_V0", edge_id)
        if edge["relation"] == "REALIZES_AS":
            reject("FOUNDATIONAL_REALIZATION_PROMOTION", edge_id)
    semantic_ids = {e["edge_id"] for e in edges if e["layer"] == "G_semantic"}
    if EXPECTED_SEMANTIC_EDGES != semantic_ids:
        reject("SEMANTIC_EDGE_SET_DRIFT", str(sorted(EXPECTED_SEMANTIC_EDGES ^ semantic_ids)))
    if not {"G_semantic", "G_proof", "G_implementation", "G_provenance"} <= layers:
        reject("GRAPH_LAYER_COVERAGE_INCOMPLETE", str(sorted(layers)))

    def must_edge(edge_id: str, source: str, target: str) -> None:
        e = emap.get(edge_id)
        if not e or e["source"]["identity"] != source or e["target"]["identity"] != target:
            reject("SEMANTIC_DEPENDENCY_DRIFT", edge_id)

    must_edge("CMDG:E:V0.RINGCAT.CATEGORY", "CMDG:V0:ALGEBRA_RING_INTERFACE", "CMDG:V0:CATEGORY")
    must_edge("CMDG:E:V0.TOPCAT.CATEGORY", "CMDG:V0:TOPOLOGICAL_SPACES", "CMDG:V0:CATEGORY")
    must_edge("CMDG:E:V0.COMPHAUS.TOPCAT", "CMDG:V0:COMPACT_HAUSDORFF", "CMDG:V0:TOPOLOGICAL_SPACES")
    must_edge("CMDG:E:V0.PROFINITE.COMPHAUS", "CMDG:V0:PROFINITE", "CMDG:V0:COMPACT_HAUSDORFF")
    must_edge("CMDG:E:V0.COHERENT.COMPHAUS", "CMDG:V0:COHERENT_TOPOLOGY_COMPHAUS", "CMDG:V0:COMPACT_HAUSDORFF")
    must_edge("CMDG:E:V0.CONDENSED.SHEAF", "CMDG:V0:CONDENSED_SET", "CMDG:V0:SHEAF")
    must_edge("CMDG:E:V0.CONDENSED.COHERENT", "CMDG:V0:CONDENSED_SET", "CMDG:V0:COHERENT_TOPOLOGY_COMPHAUS")
    must_edge("CMDG:E:V0.DISCRETE.CONDENSED", "CMDG:V0:DISCRETE_UNDERLYING_ADJUNCTION", "CMDG:V0:CONDENSED_SET")

    semantic_pairs = {(e["source"]["identity"], e["target"]["identity"]) for e in edges if e["layer"] == "G_semantic"}
    for trace in EXPECTED_BACKTRACES:
        for source, target in zip(trace, trace[1:]):
            if (source, target) not in semantic_pairs:
                reject("BROKEN_SEMANTIC_BACKTRACE", f"{source} -> {target}")

    trust = record.get("trust_boundary", {})
    if trust.get("policy") != "PINNED_EXTERNAL_SOURCE_REUSE" or trust.get("all_reused_nodes_declared") is not True:
        reject("TRUST_BOUNDARY_INCOMPLETE", str(trust))
    if trust.get("unclassified_external_nodes_allowed") is not False:
        reject("UNCLASSIFIED_EXTERNAL_TRUST_ALLOWED", str(trust))
    if trust.get("semantic_reconciler_may_confer_authority") is not False:
        reject("SEMANTIC_RECONCILER_AUTHORITY_PROMOTION", str(trust))

    c04 = record.get("condensed_target_profile", {})
    if c04.get("formal_target") != "CondensedSet.{u} := Sheaf (coherentTopology CompHaus.{u}) (Type (u + 1))":
        reject("CONDENSED_TARGET_IDENTITY_DRIFT", str(c04.get("formal_target")))
    if c04.get("formal_target_revision") != MATHLIB_COMMIT:
        reject("CONDENSED_TARGET_PIN_DRIFT", str(c04.get("formal_target_revision")))
    if c04.get("formal_cardinality_policy") != "NO_CARDINALITY_BOUND":
        reject("CONDENSED_CARDINALITY_PROFILE_MISSING", str(c04.get("formal_cardinality_policy")))
    if c04.get("formal_source_characterization") != "CLOSER_TO_PYKNOTIC_OBJECTS":
        reject("PYKNOTIC_BOUNDARY_MISSING", str(c04.get("formal_source_characterization")))
    if c04.get("concordance_status") != "PARTIAL_INTERFACE_ONLY":
        reject("CONDENSED_FULL_CONCORDANCE_OVERCLAIM", str(c04.get("concordance_status")))
    if c04.get("cm_scope") != "CM0_CM1_INTERFACE_ONLY":
        reject("CONDENSED_CM_SCOPE_OVERCLAIM", str(c04.get("cm_scope")))
    if c04.get("c04_status") != "ADVANCED_FOR_V0_TERMINAL_PROFILE_NOT_GLOBALLY_DISCHARGED":
        reject("C04_STATUS_OVERCLAIM", str(c04.get("c04_status")))
    terminal = c04.get("terminal_interface", {})
    if terminal != {
        "discrete": "Condensed.discrete",
        "underlying": "Condensed.underlying",
        "adjunction": "Condensed.discreteUnderlyingAdj",
        "module": "Mathlib/Condensed/Discrete/Basic.lean",
    }:
        reject("TERMINAL_INTERFACE_DRIFT", str(terminal))

    graph = record.get("graph", {})
    if graph.get("semantic_edge_authority") != "PROPOSED_PENDING_INDEPENDENT_EXACT_HEAD_REVIEW_AND_PROTECTED_ADMISSION":
        reject("SEMANTIC_AUTHORITY_STATE_DRIFT", str(graph))
    if graph.get("derived_closure_authoritative") is not False or graph.get("graph_certified") is not False:
        reject("GRAPH_AUTHORITY_OVERCLAIM", str(graph))

    cb = record.get("claim_boundary", {})
    prohibited = [
        "v0_unique_or_minimal",
        "foundational_equivalence_conferred",
        "syntactic_zfc_realization_conferred",
        "all_domains_fully_formalized",
        "condensed_full_concordance_conferred",
        "cm2_or_stronger_conferred",
        "global_dependency_completeness_claim",
        "graph_certified_conferred",
        "c05_discharged",
        "c06_discharged",
    ]
    for key in prohibited:
        if cb.get(key) is not False:
            reject("PROHIBITED_AUTHORITY_PROMOTION", key)
    if cb.get("independent_review_required") is not True or cb.get("protected_admission_required") is not True:
        reject("ADMISSION_GATE_BYPASS", str(cb))
    if record.get("candidate_disposition") != "V0_CANDIDATE_PENDING_INDEPENDENT_REVIEW":
        reject("CANDIDATE_DISPOSITION_DRIFT", str(record.get("candidate_disposition")))

    if re.search(r"^[ \t]*(sorry|axiom)(?:[ \t]|$)", lean_text, re.M):
        reject("FORMAL_INTERFACE_PLACEHOLDER_OR_AXIOM", "V0 interface probe contains sorry/axiom")
    for check in EXPECTED_CHECKS:
        if check not in lean_text:
            reject("FORMAL_INTERFACE_CHECK_MISSING", check)

def validate_repository() -> None:
    if blob(TOOLCHAIN) != TOOLCHAIN_BLOB or blob(LAKE_MANIFEST) != MANIFEST_BLOB:
        reject("PINNED_FORMAL_ENVIRONMENT_DRIFT", f"{blob(TOOLCHAIN)} {blob(LAKE_MANIFEST)}")
    if blob(NAT_RECORD) != NAT_RECORD_BLOB or blob(EUCLID_RECORD) != EUCLID_RECORD_BLOB:
        reject("PROTECTED_REGRESSION_RECORD_DRIFT", f"{blob(NAT_RECORD)} {blob(EUCLID_RECORD)}")
    if blob(NAT_NODES) != NAT_NODES_BLOB or blob(EUCLID_NODES) != EUCLID_NODES_BLOB:
        reject("PROTECTED_REGRESSION_NODE_DRIFT", f"{blob(NAT_NODES)} {blob(EUCLID_NODES)}")
    validate_payload(load(RECORD), load(NODES), load(EDGES), LEAN_INTERFACE.read_text(encoding="utf-8"))

def main() -> int:
    try:
        validate_repository()
    except V0Error as exc:
        print(f"CMDG V0 validation FAILED [{exc.code}]: {exc.message}")
        return 1
    print("CMDG V0 validation PASS")
    print("scope: demonstration/certified spine candidate; C04 terminal profile bounded; C05/C06 and GRAPH_CERTIFIED remain open")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
