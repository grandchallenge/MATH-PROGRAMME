#!/usr/bin/env python3
"""Fail-closed validator for CMDG-CONDENSED-CM1-001."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
P = ROOT.joinpath

RECORD = P("governance", "cmdg_condensed_cm1_001.json")
SCHEMA = P("schemas", "cmdg_condensed_cm1.schema.json")
NODES = P("fixtures", "cmdg", "condensed_cm1_001", "nodes.json")
EDGES = P("fixtures", "cmdg", "condensed_cm1_001", "edges.json")
NODE_SCHEMA = P("schemas", "cmdg_node.schema.json")
EDGE_SCHEMA = P("schemas", "cmdg_edge.schema.json")
FORMAL_DIR = P("fixtures", "formal", "CMDG-NAT-CONCORDANCE-001")
LEAN = FORMAL_DIR / "CMDGCondensedCM1.lean"
TOOLCHAIN = FORMAL_DIR / "lean-toolchain"
LAKE_MANIFEST = FORMAL_DIR / "lake-manifest.json"
LAKEFILE = FORMAL_DIR / "lakefile.toml"
EXTRACTOR = P("fixtures", "cmdg", "extractor_001", "condensed_cm1.json")

BASE = "9d305f836a208c987cd351bc22b899d39c6fc472"
BASE_TREE = "4f2fb47171a10e66cb4ec5841fdf3098b9a1fcb2"
LEAN_COMMIT = "62eed1db4d67327ec8120be05f1a1b0847d74561"
MATHLIB = "79d0395a1825a6264ad5d269e35e60537518955e"
TOOLCHAIN_BLOB = "fd85b262bf1c734663aa8292b0101f672168788f"
LAKE_MANIFEST_BLOB = "9e478e09f622406970dc9613f6cf323ade82f787"

V0_FILES = {
    "governance/cmdg_vertical_spine_v0_001.json":
        "8192f82b64de901d4f980b0981127244a1fa531d",
    "fixtures/cmdg/vertical_spine_v0_001/nodes.json":
        "77cd1b6a9aab8dcb098b11421a1d4c7b848d6623",
    "fixtures/cmdg/vertical_spine_v0_001/edges.json":
        "71d698f7e5896a35b7dcf2c5e5d4e72358a458fa",
    "fixtures/formal/CMDG-NAT-CONCORDANCE-001/CMDGVerticalSpineV0.lean":
        "46fac24748c11593a839a066dc0fde00648838ea",
}

SOURCE_LINEAGE = {
    "CondensedSet":
        ("Mathlib/Condensed/Basic.lean", "926e02ac2875d912631dac221bca13990c7d9506"),
    "CategoryTheory.sheafSections":
        ("Mathlib/CategoryTheory/Sites/Sheaf.lean", "d247c155dd0f59d8b63520b06795bed1fce6b1bc"),
    "CategoryTheory.constantSheaf":
        ("Mathlib/CategoryTheory/Sites/ConstantSheaf.lean", "bc580cbb21f0458c7cae2f432310a7f27ee9192b"),
    "CategoryTheory.constantSheafAdj":
        ("Mathlib/CategoryTheory/Sites/ConstantSheaf.lean", "bc580cbb21f0458c7cae2f432310a7f27ee9192b"),
    "CompHaus.isTerminalPUnit":
        ("Mathlib/Topology/Category/CompHaus/Limits.lean", "908ec21388ee0a7d2d6dfdb9c62fbb564a09e41e"),
    "Condensed.discrete":
        ("Mathlib/Condensed/Discrete/Basic.lean", "064c024b17326bd1bf33f932ca3292f1fe6fcf17"),
    "Condensed.underlying":
        ("Mathlib/Condensed/Discrete/Basic.lean", "064c024b17326bd1bf33f932ca3292f1fe6fcf17"),
    "Condensed.discreteUnderlyingAdj":
        ("Mathlib/Condensed/Discrete/Basic.lean", "064c024b17326bd1bf33f932ca3292f1fe6fcf17"),
    "CategoryTheory.Adjunction.homEquiv":
        ("Mathlib/CategoryTheory/Adjunction/Basic.lean", "f0e132087a6b1ffa3b39f9dea236a59173e8ce9b"),
}

NODE_IDS = {
    "CMDG:CM1:FORMAL_CONDENSED_SET_MODEL",
    "CMDG:CM1:DISCRETE_FUNCTOR",
    "CMDG:CM1:UNDERLYING_FUNCTOR",
    "CMDG:CM1:TERMINAL_POINT",
    "CMDG:CM1:CONSTANT_SHEAF_ADJUNCTION",
    "CMDG:CM1:DISCRETE_UNDERLYING_ADJUNCTION",
}
NODE_MODES = {
    "CMDG:CM1:FORMAL_CONDENSED_SET_MODEL": "CONCORDANT",
    "CMDG:CM1:DISCRETE_FUNCTOR": "REUSED",
    "CMDG:CM1:UNDERLYING_FUNCTOR": "REUSED",
    "CMDG:CM1:TERMINAL_POINT": "REUSED",
    "CMDG:CM1:CONSTANT_SHEAF_ADJUNCTION": "REUSED",
    "CMDG:CM1:DISCRETE_UNDERLYING_ADJUNCTION": "CONCORDANT",
}
SEMANTIC_EDGE_IDS = {
    "CMDG:E:CM1.MODEL.V0",
    "CMDG:E:CM1.DISCRETE.MODEL",
    "CMDG:E:CM1.UNDERLYING.MODEL",
    "CMDG:E:CM1.UNDERLYING.TERMINAL",
    "CMDG:E:CM1.CONSTANT_ADJ.DISCRETE",
    "CMDG:E:CM1.CONSTANT_ADJ.TERMINAL",
    "CMDG:E:CM1.ADJ.DISCRETE",
    "CMDG:E:CM1.ADJ.UNDERLYING",
    "CMDG:E:CM1.ADJ.CONSTANT_ADJ",
    "CMDG:E:CM1.ADJ.V0",
}
REQUIRED_DECLARATIONS = {
    "CMDG.CondensedCM1.cm1Discrete",
    "CMDG.CondensedCM1.cm1Underlying",
    "CMDG.CondensedCM1.cm1Adj",
    "CMDG.CondensedCM1.cm1HomEquiv",
    "CMDG.CondensedCM1.cm1Unit",
    "CMDG.CondensedCM1.cm1Counit",
}
EXPECTED_AXIOMS = ["Classical.choice", "Quot.sound", "propext"]


class CM1Error(RuntimeError):
    def __init__(self, code: str, message: Any):
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = str(message)


def reject(code: str, message: Any) -> None:
    raise CM1Error(code, message)


def load(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        reject("JSON_LOAD_FAILED", f"{path}: {exc}")


def git_blob(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def validate_schema(value: Any, schema_path: Path, code: str) -> None:
    errors = sorted(
        Draft202012Validator(load(schema_path)).iter_errors(value),
        key=lambda e: list(e.path),
    )
    if errors:
        reject(code, errors[0].message)


def validate_payload(
    record: dict[str, Any],
    nodes: list[dict[str, Any]],
    edges: list[dict[str, Any]],
    lean_text: str,
    extractor: dict[str, Any],
) -> None:
    validate_schema(record, SCHEMA, "RECORD_SCHEMA_VIOLATION")

    if (record.get("protected_baseline"), record.get("protected_baseline_tree")) != (BASE, BASE_TREE):
        reject("AUTHORITY_BASELINE_DRIFT", "protected baseline/tree")

    pv0 = record.get("protected_v0", {})
    if pv0.get("authority") != "PROTECTED_REUSE_NO_REDEFINITION":
        reject("V0_AUTHORITY_REDEFINITION", pv0.get("authority"))
    if pv0.get("terminal_node") != "CMDG:V0:DISCRETE_UNDERLYING_ADJUNCTION":
        reject("V0_TERMINAL_DRIFT", pv0.get("terminal_node"))

    target = record.get("formal_target", {})
    exact_target = {
        "formal_cardinality_policy": "NO_CARDINALITY_BOUND",
        "formal_source_characterization": "CLOSER_TO_PYKNOTIC_OBJECTS",
        "concordance_status": "PARTIAL_INTERFACE_ONLY",
        "cm_scope": "CM1_DISCRETE_UNDERLYING_ADJUNCTION_ONLY",
        "c04_status": "SATISFIED_FOR_CM1_INTERFACE_ONLY_NOT_CM2_PLUS",
    }
    for key, value in exact_target.items():
        if target.get(key) != value:
            reject("CONDENSED_TARGET_BOUNDARY_DRIFT", f"{key}={target.get(key)!r}")

    lineage = record.get("construction_lineage", {})
    expected_lineage = {
        "discrete": "Condensed.discrete",
        "discrete_definition": "CategoryTheory.constantSheaf",
        "underlying": "Condensed.underlying",
        "underlying_definition": "CategoryTheory.sheafSections evaluated at CompHaus.of PUnit",
        "terminal_point": "CompHaus.isTerminalPUnit",
        "general_adjunction": "CategoryTheory.constantSheafAdj",
        "cm1_adjunction": "Condensed.discreteUnderlyingAdj",
        "hom_equivalence": "CategoryTheory.Adjunction.homEquiv",
    }
    if lineage != expected_lineage:
        reject("CONSTRUCTION_LINEAGE_DRIFT", lineage)

    src = record.get("source_lineage", [])
    if len(src) != len(SOURCE_LINEAGE):
        reject("SOURCE_LINEAGE_CARDINALITY_DRIFT", len(src))
    got_src = {x.get("declaration"): (x.get("path"), x.get("git_blob_sha1")) for x in src}
    if got_src != SOURCE_LINEAGE:
        reject("SOURCE_LINEAGE_DRIFT", got_src)

    ids: set[str] = set()
    for node in nodes:
        validate_schema(node, NODE_SCHEMA, "NODE_SCHEMA_VIOLATION")
        nid = node["node_id"]
        if nid in ids:
            reject("DUPLICATE_NODE", nid)
        ids.add(nid)
        if node.get("engagement_mode") != NODE_MODES.get(nid):
            reject("NODE_ENGAGEMENT_MODE_DRIFT", nid)
    if ids != NODE_IDS:
        reject("CM1_NODE_SET_DRIFT", sorted(ids ^ NODE_IDS))

    semantic: set[str] = set()
    edge_ids: set[str] = set()
    for edge in edges:
        validate_schema(edge, EDGE_SCHEMA, "EDGE_SCHEMA_VIOLATION")
        eid = edge["edge_id"]
        if eid in edge_ids:
            reject("DUPLICATE_EDGE", eid)
        edge_ids.add(eid)
        layer = edge["layer"]
        if layer == "G_semantic":
            semantic.add(eid)
            if edge["authority_state"] != "PROPOSED":
                reject("PREMATURE_SEMANTIC_AUTHORITY", eid)
            origin = edge.get("proposal_origin", {})
            if origin.get("origin") != "HUMAN":
                reject("TOOL_ORIGIN_SEMANTIC_AUTHORITY", eid)
            if edge.get("source", {}).get("kind") == "IMPLEMENTATION_ARTIFACT" or \
                    edge.get("target", {}).get("kind") == "IMPLEMENTATION_ARTIFACT":
                reject("IMPORT_AS_SEMANTIC_AUTHORITY", eid)
        elif layer in {"G_proof", "G_implementation", "G_provenance"}:
            if edge["authority_state"] != "OBSERVED":
                reject("NONSEMANTIC_AUTHORITY_DRIFT", eid)
        else:
            reject("UNEXPECTED_GRAPH_LAYER", layer)
    if semantic != SEMANTIC_EDGE_IDS:
        reject("CM1_SEMANTIC_EDGE_SET_DRIFT", sorted(semantic ^ SEMANTIC_EDGE_IDS))

    formal = record.get("formal_evidence", {})
    if set(formal.get("required_declarations", [])) != REQUIRED_DECLARATIONS:
        reject("FORMAL_DECLARATION_SET_DRIFT", formal.get("required_declarations"))
    if formal.get("root_declaration") != "CMDG.CondensedCM1.cm1Adj":
        reject("FORMAL_ROOT_DRIFT", formal.get("root_declaration"))
    if formal.get("expected_axioms") != EXPECTED_AXIOMS:
        reject("AXIOM_PROFILE_DRIFT", formal.get("expected_axioms"))

    if re.search(r"(?m)^[ \t]*(sorry|axiom)(?:[ \t]|$)", lean_text):
        reject("FORMAL_PLACEHOLDER_OR_LOCAL_AXIOM", "sorry/axiom")
    lean_surfaces = [
        "noncomputable def cm1Discrete",
        "noncomputable def cm1Underlying",
        "noncomputable def cm1Adj",
        "noncomputable def cm1HomEquiv",
        "noncomputable def cm1Unit",
        "noncomputable def cm1Counit",
        "Condensed.discreteUnderlyingAdj",
        ".homEquiv",
        ".unit.app",
        ".counit.app",
    ]
    for surface in lean_surfaces:
        if surface not in lean_text:
            reject("FORMAL_EVIDENCE_SURFACE_MISSING", surface)

    if extractor.get("schema_version") != "1.0.0" or \
            extractor.get("fixture_id") != "CMDG-LEAN-EXTRACTOR-CONDENSED-CM1-001":
        reject("EXTRACTOR_IDENTITY_DRIFT", extractor.get("fixture_id"))
    if extractor.get("project_dir") != "fixtures/formal/CMDG-NAT-CONCORDANCE-001" or \
            extractor.get("module") != "CMDGCondensedCM1":
        reject("EXTRACTOR_PROJECT_DRIFT", extractor)
    if extractor.get("roots") != ["CMDG.CondensedCM1.cm1Adj"]:
        reject("EXTRACTOR_ROOT_DRIFT", extractor.get("roots"))
    if extractor.get("expected_toolchain_git_blob_sha1") != TOOLCHAIN_BLOB or \
            extractor.get("expected_lake_manifest_git_blob_sha1") != LAKE_MANIFEST_BLOB:
        reject("EXTRACTOR_ENVIRONMENT_DRIFT", extractor)
    if extractor.get("expected_axioms") != {
        "CMDG.CondensedCM1.cm1Adj": EXPECTED_AXIOMS
    }:
        reject("EXTRACTOR_AXIOM_PROFILE_DRIFT", extractor.get("expected_axioms"))
    if any(extractor.get("claim_boundary", {}).values()):
        reject("EXTRACTOR_AUTHORITY_OVERCLAIM", extractor.get("claim_boundary"))

    claims = record.get("claim_boundary", {})
    required_false = [
        "full_clausen_scholze_concordance_conferred",
        "discrete_fully_faithful_conferred",
        "every_condensed_object_discrete_claim",
        "cm2_or_stronger_conferred",
        "global_dependency_completeness_claim",
        "dependency_minimality_or_uniqueness_claim",
        "graph_certified_conferred",
        "c04_discharged_beyond_cm1",
        "c05_discharged",
        "c06_discharged",
        "semantic_authority_conferred_by_artifact_alone",
    ]
    if any(claims.get(k) is not False for k in required_false):
        reject("PROHIBITED_AUTHORITY_PROMOTION", {k: claims.get(k) for k in required_false})
    for key in ["cm1_adjunction_candidate", "c04_cm1_interface_satisfied",
                "independent_review_required", "protected_admission_required"]:
        if claims.get(key) is not True:
            reject("REQUIRED_CM1_GATE_MISSING", key)

    if record.get("graph", {}).get("graph_certified") is not False:
        reject("GRAPH_CERTIFIED_OVERCLAIM", record.get("graph"))


def validate_repository() -> None:
    record = load(RECORD)
    nodes = load(NODES)
    edges = load(EDGES)
    extractor = load(EXTRACTOR)
    lean_text = LEAN.read_text(encoding="utf-8")
    validate_payload(record, nodes, edges, lean_text, extractor)

    for rel, expected in V0_FILES.items():
        actual = git_blob(P(*rel.split("/")))
        if actual != expected:
            reject("PROTECTED_V0_IDENTITY_DRIFT", f"{rel}: {actual}")

    if git_blob(TOOLCHAIN) != TOOLCHAIN_BLOB:
        reject("TOOLCHAIN_BLOB_DRIFT", git_blob(TOOLCHAIN))
    if git_blob(LAKE_MANIFEST) != LAKE_MANIFEST_BLOB:
        reject("LAKE_MANIFEST_BLOB_DRIFT", git_blob(LAKE_MANIFEST))
    manifest = load(LAKE_MANIFEST)
    try:
        mathlib_rev = next(x["rev"] for x in manifest["packages"] if x["name"] == "mathlib")
    except Exception as exc:
        reject("MATHLIB_MANIFEST_READ_FAILED", exc)
    if mathlib_rev != MATHLIB:
        reject("MATHLIB_PIN_DRIFT", mathlib_rev)

    lakefile = LAKEFILE.read_text(encoding="utf-8")
    if 'name = "CMDGCondensedCM1"' not in lakefile:
        reject("CM1_LEAN_TARGET_MISSING", "CMDGCondensedCM1")

    print("CMDG CM1 candidate valid; independent exact-head review and protected admission remain required")


def main() -> int:
    try:
        validate_repository()
    except CM1Error as exc:
        print(str(exc))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
