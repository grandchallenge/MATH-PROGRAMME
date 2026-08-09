#!/usr/bin/env python3
"""Fail-closed validator for CMDG-CONDENSED-CM3-001."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
P = ROOT.joinpath
RECORD = P("governance", "cmdg_condensed_cm3_001.json")
SCHEMA = P("schemas", "cmdg_condensed_cm3.schema.json")
NODES = P("fixtures", "cmdg", "condensed_cm3_001", "nodes.json")
EDGES = P("fixtures", "cmdg", "condensed_cm3_001", "edges.json")
NODE_SCHEMA = P("schemas", "cmdg_node.schema.json")
EDGE_SCHEMA = P("schemas", "cmdg_edge.schema.json")
FORMAL_DIR = P("fixtures", "formal", "CMDG-NAT-CONCORDANCE-001")
LEAN = FORMAL_DIR / "CMDGCondensedCM3.lean"
LAKEFILE = FORMAL_DIR / "lakefile.toml"
EXTRACTOR = P("fixtures", "cmdg", "extractor_001", "condensed_cm3.json")

REPO_BASE = "941fa3b2003327fc6f540d8da73b329baf7340ae"
REPO_BASE_TREE = "2353d13de3cf3a0fe28758da17204766344c52bf"
CM2_MERGE = "9122d5f6765b552df1e491bad01df6fbbb96a6d1"
CM2_TREE = "b67e4e8e2c53126c9fc8f8a50d20126d4728e59b"
MATHLIB = "79d0395a1825a6264ad5d269e35e60537518955e"
TOOLCHAIN_BLOB = "fd85b262bf1c734663aa8292b0101f672168788f"
LAKE_MANIFEST_BLOB = "9e478e09f622406970dc9613f6cf323ade82f787"

CM2_FILES = {
    "governance/cmdg_condensed_cm2_001.json": "11ceaa9577add91a1fa231cab9f403b5d4df2db0",
    "fixtures/cmdg/condensed_cm2_001/nodes.json": "956f10d335c7c9ffb3d17cb121eef7b28f4e998a",
    "fixtures/cmdg/condensed_cm2_001/edges.json": "cdb9e903c93c3daafa4fe5b514bcb7759e608cff",
    "fixtures/formal/CMDG-NAT-CONCORDANCE-001/CMDGCondensedCM2.lean": "d97aceabb4e2ef9db474745192a45a6cc8d7cc00",
}

SOURCE_LINEAGE = {
    "CondensedMod / CondensedAb / Abelian instance": ("Mathlib/Condensed/Module.lean", "f5834efa0d5bf1289187abe3319536186d67a405"),
    "Condensed AB5 / AB4 / AB4Star instances": ("Mathlib/Condensed/AB.lean", "4c731d5cb9005146b522c23c19a9d81f536f57c1"),
    "CategoryTheory.sheafIsAbelian": ("Mathlib/CategoryTheory/Sites/Abelian.lean", "d5250edfc56c2d79c7dae942fe0ab1e8a93ac707"),
    "Sheaf exact-colimit/exact-limit machinery": ("Mathlib/CategoryTheory/Abelian/GrothendieckAxioms/Sheaf.lean", "2601697678b5ed6ea3c0c95c2a074e39732a1c66"),
    "ModuleCat AB5 / AB4 / AB4Star source instances": ("Mathlib/Algebra/Category/ModuleCat/AB.lean", "183a3dd6be8be75c2dacefa46e496207184e7e1c"),
}

NODE_IDS = {
    "CMDG:CM3:PINNED_CONDENSED_MODEL", "CMDG:CM3:MODULECAT_COEFFICIENT",
    "CMDG:CM3:CONDENSED_MOD", "CMDG:CM3:SHEAF_ABELIAN_TRANSFER",
    "CMDG:CM3:ABELIAN_CONDENSED_MOD", "CMDG:CM3:CONDENSED_AB",
    "CMDG:CM3:EXACT_COLIMIT_TRANSPORT", "CMDG:CM3:AB5_CONDENSED_MOD",
    "CMDG:CM3:AB4_CONDENSED_MOD", "CMDG:CM3:EXACT_LIMIT_TRANSPORT",
    "CMDG:CM3:AB4STAR_CONDENSED_MOD",
}
SEMANTIC_EDGE_IDS = {
    "CMDG:E:CM3.MODEL.CM2", "CMDG:E:CM3.CONDENSEDMOD.MODEL",
    "CMDG:E:CM3.CONDENSEDMOD.MODULECAT", "CMDG:E:CM3.ABELIAN.TRANSFER",
    "CMDG:E:CM3.ABELIAN.CONDENSEDMOD", "CMDG:E:CM3.CONDENSEDAB.CONDENSEDMOD",
    "CMDG:E:CM3.AB5.EXACTCOLIMIT", "CMDG:E:CM3.AB5.ABELIAN",
    "CMDG:E:CM3.AB4.AB5", "CMDG:E:CM3.AB4STAR.EXACTLIMIT",
}
REQUIRED_DECLARATIONS = {
    "CMDG.CondensedCM3.cm3Abelian", "CMDG.CondensedCM3.cm3AB5",
    "CMDG.CondensedCM3.cm3AB4", "CMDG.CondensedCM3.cm3AB4Star",
    "CMDG.CondensedCM3.cm3CondensedAbAbelian", "CMDG.CondensedCM3.cm3CondensedAbAB5",
    "CMDG.CondensedCM3.cm3CondensedAbAB4", "CMDG.CondensedCM3.cm3CondensedAbAB4Star",
}


class CM3Error(RuntimeError):
    def __init__(self, code: str, message: Any):
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = str(message)


def reject(code: str, message: Any) -> None:
    raise CM3Error(code, message)


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
    if (record.get("repository_baseline"), record.get("repository_baseline_tree")) != (REPO_BASE, REPO_BASE_TREE):
        reject("REPOSITORY_BASELINE_DRIFT", record.get("repository_baseline"))
    if record.get("predecessor_disposition") != "CMDG_CONDENSED_CM2_001_PROTECTED_CLOSED":
        reject("CM2_TERMINAL_DISPOSITION_DRIFT", record.get("predecessor_disposition"))

    cm2 = record.get("protected_cm2", {})
    if cm2.get("merge_commit") != CM2_MERGE or cm2.get("merge_tree") != CM2_TREE:
        reject("PROTECTED_CM2_IDENTITY_DRIFT", cm2)
    if cm2.get("authority") != "PROTECTED_REUSE_NO_REDEFINITION":
        reject("CM2_AUTHORITY_REDEFINITION", cm2.get("authority"))
    for path, expected in CM2_FILES.items():
        if git_blob(P(path)) != expected:
            reject("PROTECTED_CM2_BLOB_DRIFT", path)

    env = record.get("environment", {})
    if env.get("mathlib_commit") != MATHLIB or env.get("toolchain_blob_sha1") != TOOLCHAIN_BLOB or env.get("lake_manifest_blob_sha1") != LAKE_MANIFEST_BLOB:
        reject("PINNED_ENVIRONMENT_DRIFT", env)

    target = record.get("formal_target", {})
    exact = {
        "formal_cardinality_policy": "NO_CARDINALITY_BOUND",
        "concordance_status": "PARTIAL_INTERFACE_ONLY",
        "cm_scope": "CM3_ABELIAN_AB5_AB4_AB4STAR_ONLY",
        "c04_candidate_judgment": "SATISFIED_FOR_CM3_AB_INTERFACE_IF_PROTECTED_ADMITTED",
        "c04_authority_status": "NOT_YET_CONFERRED_PENDING_INDEPENDENT_REVIEW_AND_PROTECTED_ADMISSION",
    }
    for key, value in exact.items():
        if target.get(key) != value:
            reject("CM3_TARGET_BOUNDARY_DRIFT", f"{key}={target.get(key)!r}")

    got_src = {x.get("declaration"): (x.get("path"), x.get("git_blob_sha1")) for x in record.get("source_lineage", [])}
    if got_src != SOURCE_LINEAGE:
        reject("SOURCE_LINEAGE_DRIFT", got_src)

    ids = set()
    for node in nodes:
        validate_schema(node, NODE_SCHEMA, "NODE_SCHEMA_VIOLATION")
        if node["node_id"] in ids:
            reject("DUPLICATE_NODE", node["node_id"])
        ids.add(node["node_id"])
    if ids != NODE_IDS:
        reject("CM3_NODE_SET_DRIFT", sorted(ids ^ NODE_IDS))

    semantic = set()
    edge_ids = set()
    for edge in edges:
        validate_schema(edge, EDGE_SCHEMA, "EDGE_SCHEMA_VIOLATION")
        if edge["edge_id"] in edge_ids:
            reject("DUPLICATE_EDGE", edge["edge_id"])
        edge_ids.add(edge["edge_id"])
        if edge["layer"] == "G_semantic":
            semantic.add(edge["edge_id"])
            if edge["authority_state"] != "PROPOSED":
                reject("PREMATURE_SEMANTIC_AUTHORITY", edge["edge_id"])
            if edge.get("proposal_origin", {}).get("origin") != "HUMAN":
                reject("TOOL_ORIGIN_SEMANTIC_AUTHORITY", edge["edge_id"])
        elif edge["authority_state"] != "OBSERVED":
            reject("NONSEMANTIC_AUTHORITY_DRIFT", edge["edge_id"])
    if semantic != SEMANTIC_EDGE_IDS:
        reject("CM3_SEMANTIC_EDGE_SET_DRIFT", sorted(semantic ^ SEMANTIC_EDGE_IDS))

    formal = record.get("formal_evidence", {})
    if set(formal.get("required_declarations", [])) != REQUIRED_DECLARATIONS:
        reject("FORMAL_DECLARATION_SET_DRIFT", formal.get("required_declarations"))

    if re.search(r"(?m)^[ \t]*(sorry|axiom)(?:[ \t]|$)", lean_text):
        reject("FORMAL_PLACEHOLDER_OR_LOCAL_AXIOM", "sorry/axiom")
    for surface in [
        "import Mathlib.Condensed.AB",
        "noncomputable def cm3Abelian (",
        "noncomputable def cm3AB5 (",
        "noncomputable def cm3AB4 (",
        "noncomputable def cm3AB4Star (",
        "noncomputable def cm3CondensedAbAbelian",
        "noncomputable def cm3CondensedAbAB5",
        "noncomputable def cm3CondensedAbAB4 :",
        "noncomputable def cm3CondensedAbAB4Star :",
    ]:
        if surface not in lean_text:
            reject("FORMAL_EVIDENCE_SURFACE_MISSING", surface)
    if "[[lean_lib]]\nname = \"CMDGCondensedCM3\"" not in LAKEFILE.read_text(encoding="utf-8"):
        reject("LAKE_TARGET_MISSING", "CMDGCondensedCM3")

    if extractor.get("fixture_id") != "CMDG-LEAN-EXTRACTOR-CONDENSED-CM3-001":
        reject("EXTRACTOR_IDENTITY_DRIFT", extractor.get("fixture_id"))
    if extractor.get("module") != "CMDGCondensedCM3":
        reject("EXTRACTOR_MODULE_DRIFT", extractor.get("module"))
    if set(extractor.get("roots", [])) != {
        "CMDG.CondensedCM3.cm3CondensedAbAbelian", "CMDG.CondensedCM3.cm3CondensedAbAB5",
        "CMDG.CondensedCM3.cm3CondensedAbAB4", "CMDG.CondensedCM3.cm3CondensedAbAB4Star",
    }:
        reject("EXTRACTOR_ROOT_DRIFT", extractor.get("roots"))
    if extractor.get("expected_toolchain_git_blob_sha1") != TOOLCHAIN_BLOB or extractor.get("expected_lake_manifest_git_blob_sha1") != LAKE_MANIFEST_BLOB:
        reject("EXTRACTOR_ENVIRONMENT_DRIFT", extractor)
    if any(extractor.get("claim_boundary", {}).values()):
        reject("EXTRACTOR_AUTHORITY_OVERCLAIM", extractor.get("claim_boundary"))

    claims = record.get("claim_boundary", {})
    prohibited = [
        "cm3_semantic_authority_conferred", "is_grothendieck_abelian_conferred",
        "separator_or_generator_conferred", "derived_category_or_ext_or_cohomology_conferred",
        "enough_injectives_or_projectives_conferred", "full_clausen_scholze_concordance_conferred",
        "pyknotic_cardinal_bounded_equivalence_conferred", "solid_or_liquid_conferred",
        "c04_discharged_beyond_cm3", "c05_discharged", "c06_discharged",
        "graph_certified_conferred", "dependency_minimality_or_uniqueness_claim",
        "global_dependency_completeness_claim", "semantic_authority_conferred_by_artifact_alone",
    ]
    if any(claims.get(k) is not False for k in prohibited):
        reject("PROHIBITED_AUTHORITY_PROMOTION", {k: claims.get(k) for k in prohibited})
    if claims.get("cm3_abelian_ab_candidate") is not True or claims.get("c04_cm3_interface_candidate_satisfied") is not True:
        reject("CM3_CANDIDATE_STATUS_DRIFT", claims)
    if claims.get("independent_review_required") is not True or claims.get("protected_admission_required") is not True:
        reject("REVIEW_OR_ADMISSION_GATE_WEAKENED", claims)


def main() -> int:
    validate_payload(load(RECORD), load(NODES), load(EDGES), LEAN.read_text(encoding="utf-8"), load(EXTRACTOR))
    print("CMDG-CONDENSED-CM3-001 candidate package valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
