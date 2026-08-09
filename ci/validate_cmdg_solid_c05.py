#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "governance/cmdg_solid_c05_001.json"
SCHEMA = ROOT / "schemas/cmdg_solid_c05.schema.json"
NODES = ROOT / "fixtures/cmdg/solid_c05_001/nodes.json"
EDGES = ROOT / "fixtures/cmdg/solid_c05_001/edges.json"
LEAN = ROOT / "fixtures/formal/CMDG-NAT-CONCORDANCE-001/CMDGSolidC05.lean"

EXPECTED_BASE = "e99defaabbc0d971e6299360ac03084e516c31c3"
EXPECTED_BASE_TREE = "041b4f7afa647fec06d3303503b53fa0fc65350d"
EXPECTED_CM3 = "4d8cd462f2836349704b4325766bcff679574404"
EXPECTED_MATHLIB = "79d0395a1825a6264ad5d269e35e60537518955e"
EXPECTED_SOLID_BLOB = "f5214433f91ee87fc8fbe7e2746e0bd227faed2a"

FORBIDDEN_TRUE = {
    "c05_semantic_authority_conferred", "pinned_general_ring_semantics_conferred",
    "pinned_reconstructed_equivalence_conferred", "noncommutative_general_ring_reconstruction_conferred",
    "nontrivial_solid_object_conferred", "profinite_solid_object_is_solid_conferred",
    "solid_subcategory_abelian_conferred", "solidification_reflector_conferred",
    "tensor_or_internal_hom_closure_conferred", "derived_solid_conferred", "liquid_conferred",
    "cm4_conferred", "c04_broadened", "c06_discharged", "graph_certified_conferred",
    "dependency_minimality_or_uniqueness_claim", "global_dependency_completeness_claim",
}

REQUIRED_NODE_IDS = {
    "CMDG:C05:PINNED_SOLID_PREDICATE", "CMDG:C05:MATHLIB_GENERAL_RING_DEFECT",
    "CMDG:C05:FINITE_TYPE_Z_ALGEBRA_PROFILE", "CMDG:C05:FINITE_TYPE_Z_ALGEBRA_SOLID",
    "CMDG:C05:ZX", "CMDG:C05:EVALUATION_RING_HOM", "CMDG:C05:RESTRICTION_OF_SCALARS",
    "CMDG:C05:GENERAL_COMM_RING_OBJECT", "CMDG:C05:ELEMENTWISE_RESTRICTED_OBJECT",
    "CMDG:C05:GENERAL_COMM_RING_SOLID_RECONSTRUCTED", "CMDG:C05:CONCORDANCE_MATRIX",
    "CMDG:C05:DEFINITION_AUTHORITY_BOUNDARY",
}

REQUIRED_LEAN_SNIPPETS = (
    "Condensed.profiniteSolid R", "profiniteSolidIsPointwiseRightKanExtension",
    "hA.isIso_solidification_map", "Algebra.FiniteType ℤ R",
    "ULift.{u + 1} (Polynomial ℤ)", "Polynomial.eval₂RingHom (Int.castRingHom R) r",
    "ModuleCat.restrictScalars f", "sheafCompose _", "∀ r : R",
    "GeneralCommRingSolidReconstructed",
)

def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def validate(data=None):
    record = load(RECORD) if data is None else data
    jsonschema.validate(record, load(SCHEMA))
    assert record["repository_baseline"] == EXPECTED_BASE
    assert record["repository_baseline_tree"] == EXPECTED_BASE_TREE
    assert record["protected_cm3"]["merge_commit"] == EXPECTED_CM3
    assert record["protected_cm3"]["terminal_disposition"] == "CMDG_CONDENSED_CM3_001_PROTECTED_CLOSED"
    assert record["environment"]["mathlib_commit"] == EXPECTED_MATHLIB
    lineage = {x["path"]: x["git_blob_sha1"] for x in record["source_lineage"]}
    assert lineage["Mathlib/Condensed/Solid.lean"] == EXPECTED_SOLID_BLOB
    for path in (
        "Mathlib/Condensed/Module.lean", "Mathlib/Algebra/Category/ModuleCat/ChangeOfRings.lean",
        "Mathlib/CategoryTheory/Sites/Whiskering.lean", "Mathlib/Algebra/Polynomial/Eval/Defs.lean",
        "Mathlib/RingTheory/FiniteType.lean", "Mathlib/Algebra/Ring/ULift.lean",
    ):
        assert path in lineage
    defect = record["pinned_defect"]
    assert defect["defect_recorded_in_source"] is True
    assert defect["defect"] == "PINNED_SOURCE_STATES_CURRENT_PREDICATE_IS_NOT_CORRECT_GENERAL_RING_DEFINITION"
    assert defect["recommended_reconstruction"].startswith("FOR_EVERY_")
    assert "NOT_GENERAL_RING_SEMANTIC_AUTHORITY" in defect["semantic_effect"]
    layers = record["definition_layers"]
    assert layers["FINITE_TYPE_Z_ALGEBRA_SOLID"]["ring_profile"].startswith("[CommRing R]")
    reconstructed = layers["GENERAL_COMM_RING_SOLID_RECONSTRUCTED"]
    assert reconstructed["quantification"] == "FOR_ALL_ELEMENTS"
    assert "commutative ring" in reconstructed["ring_profile"]
    assert "EQUIVALENCE_NOT_PRESUMED" in reconstructed["authority"]
    relations = {row["relationship"] for row in record["concordance_matrix"]}
    assert {"RESTRICTED_REALIZATION", "RECONSTRUCTED_FROM_SOURCE_GUIDANCE", "UNPROVED_EQUIVALENCE", "OUT_OF_SCOPE"} <= relations
    claims = record["claim_boundary"]
    assert claims["definition_boundary_candidate"] is True
    assert claims["c05_candidate_satisfied"] is True
    for key in FORBIDDEN_TRUE:
        assert claims[key] is False, key
    assert record["graph"]["graph_certified"] is False
    nodes = load(NODES)["nodes"]
    node_ids = {n["id"] for n in nodes}
    assert REQUIRED_NODE_IDS <= node_ids
    edges = load(EDGES)["edges"]
    assert all(e["source"] in node_ids and e["target"] in node_ids for e in edges)
    assert all(e["layer"] in {"semantic", "proof", "implementation", "provenance"} for e in edges)
    lean = LEAN.read_text(encoding="utf-8")
    for snippet in REQUIRED_LEAN_SNIPPETS:
        assert snippet in lean, snippet
    lowered = lean.lower()
    for forbidden in ("sorry", "axiom ", "unsafe ", "implemented_by"):
        assert forbidden not in lowered, forbidden
    return record

def mutation_tests():
    base = validate()
    mutations = []
    def mut(path, value):
        d = copy.deepcopy(base); cur = d
        for part in path[:-1]: cur = cur[part]
        cur[path[-1]] = value; mutations.append(d)
    mut(("protected_cm3", "merge_commit"), "0" * 40)
    mut(("environment", "mathlib_commit"), "0" * 40)
    mut(("pinned_defect", "defect_recorded_in_source"), False)
    mut(("pinned_defect", "recommended_reconstruction"), "EXISTS_r")
    mut(("definition_layers", "FINITE_TYPE_Z_ALGEBRA_SOLID", "ring_profile"), "[Ring R]")
    mut(("definition_layers", "GENERAL_COMM_RING_SOLID_RECONSTRUCTED", "quantification"), "EXISTS_ELEMENT")
    mut(("definition_layers", "GENERAL_COMM_RING_SOLID_RECONSTRUCTED", "authority"), "EQUIVALENT_TO_PINNED")
    mut(("concordance_matrix", 4, "relationship"), "IDENTICAL")
    for key in FORBIDDEN_TRUE: mut(("claim_boundary", key), True)
    g = copy.deepcopy(base); g["graph"]["graph_certified"] = True; mutations.append(g)
    for i, d in enumerate(mutations):
        try: validate(d)
        except Exception: continue
        raise AssertionError(f"mutation {i} was not rejected")

if __name__ == "__main__":
    validate(); mutation_tests(); print("CMDG-SOLID-C05-001 validation passed")
