#!/usr/bin/env python3
"""Fail-closed validator for CMDG-CONDENSED-CM2-001."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
P = ROOT.joinpath

RECORD = P("governance", "cmdg_condensed_cm2_001.json")
SCHEMA = P("schemas", "cmdg_condensed_cm2.schema.json")
NODES = P("fixtures", "cmdg", "condensed_cm2_001", "nodes.json")
EDGES = P("fixtures", "cmdg", "condensed_cm2_001", "edges.json")
NODE_SCHEMA = P("schemas", "cmdg_node.schema.json")
EDGE_SCHEMA = P("schemas", "cmdg_edge.schema.json")
FORMAL_DIR = P("fixtures", "formal", "CMDG-NAT-CONCORDANCE-001")
LEAN = FORMAL_DIR / "CMDGCondensedCM2.lean"
TOOLCHAIN = FORMAL_DIR / "lean-toolchain"
LAKE_MANIFEST = FORMAL_DIR / "lake-manifest.json"
LAKEFILE = FORMAL_DIR / "lakefile.toml"
EXTRACTOR = P("fixtures", "cmdg", "extractor_001", "condensed_cm2.json")

BASE = "2b9013b2947acfa092666214d49b6d4a661f6a12"
BASE_TREE = "f843f7501da2f052904d4a760fb8d37eafcae110"
MATHLIB = "79d0395a1825a6264ad5d269e35e60537518955e"
TOOLCHAIN_BLOB = "fd85b262bf1c734663aa8292b0101f672168788f"
LAKE_MANIFEST_BLOB = "9e478e09f622406970dc9613f6cf323ade82f787"

CM1_FILES = {
    "governance/cmdg_condensed_cm1_001.json": "d85305fe900eeb10f3857f82635841a5f175b222",
    "fixtures/cmdg/condensed_cm1_001/nodes.json": "8cfb190a53d4438876ec573e259f94957486090c",
    "fixtures/cmdg/condensed_cm1_001/edges.json": "a1c0ca35457da4831a261e8235eac34a1de184b0",
    "fixtures/formal/CMDG-NAT-CONCORDANCE-001/CMDGCondensedCM1.lean": "6cf27a35aa2f90197117690f0865bc2bb70b9966",
}

SOURCE_LINEAGE = {
    "CondensedSet": ("Mathlib/Condensed/Basic.lean", "926e02ac2875d912631dac221bca13990c7d9506"),
    "deprecated Condensed CartesianClosed import shim": ("Mathlib/Condensed/CartesianClosed.lean", "0ce243384482c50191f8e4426baebe38bb21fd10"),
    "CartesianMonoidalCategory (Sheaf J A) instance": ("Mathlib/CategoryTheory/Sites/CartesianMonoidal.lean", "c161990e16c398e0b6f09cebec717cb7050bd3af"),
    "CategoryTheory.CartesianMonoidalCategory.tensorProductIsBinaryProduct": ("Mathlib/CategoryTheory/Monoidal/Cartesian/Basic.lean", "5c0fb0d708fde466348ad1fc79d4547be0daf5d0"),
    "CategoryTheory.instMonoidalClosedSheafOfHasSheafifyOfFunctorOpposite": ("Mathlib/CategoryTheory/Sites/CartesianClosed.lean", "6d1e5cc05246533221dab116dc065341830bbaf3"),
    "CategoryTheory.HasSheafify / sheafificationAdjunction": ("Mathlib/CategoryTheory/Sites/Sheafification.lean", "231e46274c7217803239cd2052697018edbf7ef0"),
    "left-exact sheafification support": ("Mathlib/CategoryTheory/Sites/LeftExact.lean", "6b6033102820772cdbd2d75694b3f5b67965aae9"),
    "CategoryTheory.cartesianClosedOfReflective'": ("Mathlib/CategoryTheory/Monoidal/Closed/Ideal.lean", "b85d7de5f231fd1328583508dc4500467c9d596f"),
    "CategoryTheory.Closed / MonoidalClosed / ihom.adjunction": ("Mathlib/CategoryTheory/Monoidal/Closed/Basic.lean", "57dd533860e4be3957c13211f275b6f75441787c"),
    "Type and presheaf MonoidalClosed instances": ("Mathlib/CategoryTheory/Monoidal/Closed/Types.lean", "1e3a030a37164fcc34b31ad5dee6d771bd7d38ef"),
}

NODE_IDS = {
    "CMDG:CM2:FORMAL_CONDENSED_SET_MODEL",
    "CMDG:CM2:CARTESIAN_MONOIDAL_STRUCTURE",
    "CMDG:CM2:SHEAFIFICATION_REFLECTION",
    "CMDG:CM2:GENERIC_SHEAF_CARTESIAN_CLOSED",
    "CMDG:CM2:ARBITRARY_CONDENSED_OBJECT",
    "CMDG:CM2:TENSOR_LEFT_PRODUCT_FUNCTOR",
    "CMDG:CM2:INTERNAL_HOM_RIGHT_ADJOINT",
    "CMDG:CM2:CARTESIAN_CLOSED_ADJUNCTION",
    "CMDG:CM2:EXPONENTIAL_UNIVERSAL_INTERFACE",
}
SEMANTIC_EDGE_IDS = {
    "CMDG:E:CM2.MODEL.CM1",
    "CMDG:E:CM2.CARTESIAN.MODEL",
    "CMDG:E:CM2.SHEAFIFY.MODEL",
    "CMDG:E:CM2.GENERIC.CARTESIAN",
    "CMDG:E:CM2.GENERIC.SHEAFIFY",
    "CMDG:E:CM2.TENSOR.OBJECT",
    "CMDG:E:CM2.TENSOR.CARTESIAN",
    "CMDG:E:CM2.RIGHTADJ.GENERIC",
    "CMDG:E:CM2.ADJ.TENSOR",
    "CMDG:E:CM2.ADJ.RIGHTADJ",
    "CMDG:E:CM2.UNIVERSAL.ADJ",
}
REQUIRED_DECLARATIONS = {
    "CMDG.CondensedCM2.cm2CartesianMonoidal",
    "CMDG.CondensedCM2.cm2MonoidalClosed",
    "CMDG.CondensedCM2.cm2ProductWitness",
    "CMDG.CondensedCM2.cm2Closed",
    "CMDG.CondensedCM2.cm2TensorLeft",
    "CMDG.CondensedCM2.cm2RightAdj",
    "CMDG.CondensedCM2.cm2Adj",
    "CMDG.CondensedCM2.cm2HomEquiv",
    "CMDG.CondensedCM2.cm2Unit",
    "CMDG.CondensedCM2.cm2Counit",
    "CMDG.CondensedCM2.cm2Evaluation",
}
EXPECTED_AXIOMS = ["Classical.choice", "Quot.sound", "propext"]


class CM2Error(RuntimeError):
    def __init__(self, code: str, message: Any):
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = str(message)


def reject(code: str, message: Any) -> None:
    raise CM2Error(code, message)


def load(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        reject("JSON_LOAD_FAILED", f"{path}: {exc}")


def git_blob(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def validate_schema(value: Any, schema_path: Path, code: str) -> None:
    errors = sorted(Draft202012Validator(load(schema_path)).iter_errors(value), key=lambda e: list(e.path))
    if errors:
        reject(code, errors[0].message)


def validate_payload(record, nodes, edges, lean_text, extractor) -> None:
    validate_schema(record, SCHEMA, "RECORD_SCHEMA_VIOLATION")

    if (record.get("protected_baseline"), record.get("protected_baseline_tree")) != (BASE, BASE_TREE):
        reject("AUTHORITY_BASELINE_DRIFT", "protected CM1 baseline/tree")

    pcm1 = record.get("protected_cm1", {})
    if pcm1.get("authority") != "PROTECTED_REUSE_NO_REDEFINITION":
        reject("CM1_AUTHORITY_REDEFINITION", pcm1.get("authority"))
    if pcm1.get("terminal_disposition") != "CMDG_CONDENSED_CM1_001_PROTECTED_CLOSED":
        reject("CM1_TERMINAL_DISPOSITION_DRIFT", pcm1.get("terminal_disposition"))
    for path, expected in CM1_FILES.items():
        if git_blob(P(path)) != expected:
            reject("PROTECTED_CM1_BLOB_DRIFT", path)
    for key, path_key, blob_key in [
        ("record", "record_ref", "record_blob_sha1"),
        ("nodes", "nodes_ref", "nodes_blob_sha1"),
        ("edges", "edges_ref", "edges_blob_sha1"),
        ("formal", "formal_probe_ref", "formal_probe_blob_sha1"),
    ]:
        path = pcm1.get(path_key)
        if path not in CM1_FILES or pcm1.get(blob_key) != CM1_FILES[path]:
            reject("CM1_BINDING_DRIFT", key)

    target = record.get("formal_target", {})
    exact_target = {
        "formal_cardinality_policy": "NO_CARDINALITY_BOUND",
        "formal_source_characterization": "CLOSER_TO_PYKNOTIC_OBJECTS",
        "concordance_status": "PARTIAL_INTERFACE_ONLY",
        "cm_scope": "CM2_CARTESIAN_CLOSEDNESS_ONLY",
        "c04_candidate_judgment": "SATISFIED_FOR_CM2_INTERFACE_IF_PROTECTED_ADMITTED",
        "c04_authority_status": "NOT_YET_CONFERRED_PENDING_INDEPENDENT_REVIEW_AND_PROTECTED_ADMISSION",
    }
    for key, value in exact_target.items():
        if target.get(key) != value:
            reject("CM2_TARGET_BOUNDARY_DRIFT", f"{key}={target.get(key)!r}")

    src = record.get("source_lineage", [])
    got_src = {x.get("declaration"): (x.get("path"), x.get("git_blob_sha1")) for x in src}
    if got_src != SOURCE_LINEAGE:
        reject("SOURCE_LINEAGE_DRIFT", got_src)

    ids = set()
    for node in nodes:
        validate_schema(node, NODE_SCHEMA, "NODE_SCHEMA_VIOLATION")
        if node["node_id"] in ids:
            reject("DUPLICATE_NODE", node["node_id"])
        ids.add(node["node_id"])
    if ids != NODE_IDS:
        reject("CM2_NODE_SET_DRIFT", sorted(ids ^ NODE_IDS))

    semantic = set()
    edge_ids = set()
    for edge in edges:
        validate_schema(edge, EDGE_SCHEMA, "EDGE_SCHEMA_VIOLATION")
        eid = edge["edge_id"]
        if eid in edge_ids:
            reject("DUPLICATE_EDGE", eid)
        edge_ids.add(eid)
        if edge["layer"] == "G_semantic":
            semantic.add(eid)
            if edge["authority_state"] != "PROPOSED":
                reject("PREMATURE_SEMANTIC_AUTHORITY", eid)
            if edge.get("proposal_origin", {}).get("origin") != "HUMAN":
                reject("TOOL_ORIGIN_SEMANTIC_AUTHORITY", eid)
            if edge.get("source", {}).get("kind") == "IMPLEMENTATION_ARTIFACT" or edge.get("target", {}).get("kind") == "IMPLEMENTATION_ARTIFACT":
                reject("IMPORT_AS_SEMANTIC_AUTHORITY", eid)
        elif edge["layer"] in {"G_proof", "G_implementation", "G_provenance"}:
            if edge["authority_state"] != "OBSERVED":
                reject("NONSEMANTIC_AUTHORITY_DRIFT", eid)
        else:
            reject("UNEXPECTED_GRAPH_LAYER", edge["layer"])
    if semantic != SEMANTIC_EDGE_IDS:
        reject("CM2_SEMANTIC_EDGE_SET_DRIFT", sorted(semantic ^ SEMANTIC_EDGE_IDS))

    formal = record.get("formal_evidence", {})
    if set(formal.get("required_declarations", [])) != REQUIRED_DECLARATIONS:
        reject("FORMAL_DECLARATION_SET_DRIFT", formal.get("required_declarations"))
    if formal.get("root_declaration") != "CMDG.CondensedCM2.cm2Adj":
        reject("FORMAL_ROOT_DRIFT", formal.get("root_declaration"))
    if formal.get("expected_axioms") != EXPECTED_AXIOMS:
        reject("AXIOM_PROFILE_DRIFT", formal.get("expected_axioms"))

    if re.search(r"(?m)^[ \t]*(sorry|axiom)(?:[ \t]|$)", lean_text):
        reject("FORMAL_PLACEHOLDER_OR_LOCAL_AXIOM", "sorry/axiom")
    for surface in [
        "noncomputable def cm2CartesianMonoidal",
        "noncomputable def cm2MonoidalClosed",
        "noncomputable def cm2ProductWitness",
        "tensorProductIsBinaryProduct",
        "noncomputable def cm2Closed",
        "MonoidalClosed.closed",
        "noncomputable def cm2RightAdj",
        ".rightAdj",
        "noncomputable def cm2Adj",
        ".adj",
        "noncomputable def cm2HomEquiv",
        ".homEquiv",
        "noncomputable def cm2Unit",
        ".unit.app",
        "noncomputable def cm2Counit",
        ".counit.app",
        "noncomputable def cm2Evaluation",
    ]:
        if surface not in lean_text:
            reject("FORMAL_EVIDENCE_SURFACE_MISSING", surface)

    if "[[lean_lib]]\nname = \"CMDGCondensedCM2\"" not in LAKEFILE.read_text(encoding="utf-8"):
        reject("LAKE_TARGET_MISSING", "CMDGCondensedCM2")

    if extractor.get("fixture_id") != "CMDG-LEAN-EXTRACTOR-CONDENSED-CM2-001":
        reject("EXTRACTOR_IDENTITY_DRIFT", extractor.get("fixture_id"))
    if extractor.get("module") != "CMDGCondensedCM2" or extractor.get("roots") != ["CMDG.CondensedCM2.cm2Adj"]:
        reject("EXTRACTOR_ROOT_DRIFT", extractor)
    if extractor.get("expected_toolchain_git_blob_sha1") != TOOLCHAIN_BLOB or extractor.get("expected_lake_manifest_git_blob_sha1") != LAKE_MANIFEST_BLOB:
        reject("EXTRACTOR_ENVIRONMENT_DRIFT", extractor)
    if extractor.get("expected_axioms") != {"CMDG.CondensedCM2.cm2Adj": EXPECTED_AXIOMS}:
        reject("EXTRACTOR_AXIOM_PROFILE_DRIFT", extractor.get("expected_axioms"))
    if any(extractor.get("claim_boundary", {}).values()):
        reject("EXTRACTOR_AUTHORITY_OVERCLAIM", extractor.get("claim_boundary"))

    claims = record.get("claim_boundary", {})
    required_false = [
        "cm2_semantic_authority_conferred",
        "deprecated_import_shim_sufficient_proof",
        "full_clausen_scholze_concordance_conferred",
        "pyknotic_cardinal_bounded_equivalence_conferred",
        "internal_hom_pointwise_function_space_claim",
        "underlying_preserves_exponentials_claim",
        "discrete_preserves_exponentials_claim",
        "cm3_or_stronger_conferred",
        "solid_or_liquid_conferred",
        "global_dependency_completeness_claim",
        "dependency_minimality_or_uniqueness_claim",
        "graph_certified_conferred",
        "c04_discharged_beyond_cm2",
        "c05_discharged",
        "c06_discharged",
        "semantic_authority_conferred_by_artifact_alone",
    ]
    if any(claims.get(k) is not False for k in required_false):
        reject("PROHIBITED_AUTHORITY_PROMOTION", {k: claims.get(k) for k in required_false})
    if claims.get("cm2_cartesian_closed_candidate") is not True or claims.get("c04_cm2_interface_candidate_satisfied") is not True:
        reject("CM2_CANDIDATE_JUDGMENT_MISSING", claims)
    if claims.get("independent_review_required") is not True or claims.get("protected_admission_required") is not True:
        reject("ADMISSION_GATE_WEAKENED", claims)

    if record.get("candidate_disposition") != "CM2_CANDIDATE_PENDING_INDEPENDENT_REVIEW_AND_PROTECTED_ADMISSION":
        reject("CANDIDATE_DISPOSITION_DRIFT", record.get("candidate_disposition"))


def validate_repository() -> None:
    if git_blob(TOOLCHAIN) != TOOLCHAIN_BLOB:
        reject("TOOLCHAIN_BLOB_DRIFT", git_blob(TOOLCHAIN))
    if git_blob(LAKE_MANIFEST) != LAKE_MANIFEST_BLOB:
        reject("LAKE_MANIFEST_BLOB_DRIFT", git_blob(LAKE_MANIFEST))
    manifest = load(LAKE_MANIFEST)
    mathlib = next((p for p in manifest.get("packages", []) if p.get("name") == "mathlib"), None)
    if not mathlib or mathlib.get("rev") != MATHLIB:
        reject("MATHLIB_MANIFEST_DRIFT", mathlib)
    validate_payload(load(RECORD), load(NODES), load(EDGES), LEAN.read_text(encoding="utf-8"), load(EXTRACTOR))


def main() -> int:
    try:
        validate_repository()
    except CM2Error as exc:
        print(str(exc))
        return 1
    print("CMDG-CONDENSED-CM2-001 validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
