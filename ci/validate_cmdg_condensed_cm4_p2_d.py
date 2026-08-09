#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "governance/cmdg_condensed_cm4_p2_d_001.json"
SCHEMA = ROOT / "schemas/cmdg_condensed_cm4_p2_d.schema.json"
REPORT = ROOT / "governance/CMDG-CONDENSED-CM4-P2-D-001.md"
LEAN = ROOT / "fixtures/formal/CMDG-NAT-CONCORDANCE-001/CMDGCondensedCM4P2D.lean"

EXPECTED_BASE = "fa283a283c4584c79af86fec632d50aa49e6d640"
EXPECTED_BASE_TREE = "49f644c8ff4462015833d6477dfb6fde5b847970"
EXPECTED_PREDECESSOR_HEAD = "0892a8ed137013822d910a4212ce024da6997dc5"
EXPECTED_PREDECESSOR_TREE = "90b8640fc3c75f35fff143be0e2be08ae6231a17"
EXPECTED_PREDECESSOR_MERGE = "baeee7329e12c73b422251edfb88a643108d7667"
EXPECTED_PREDECESSOR_RUN = 31317585106
EXPECTED_MATHLIB = "79d0395a1825a6264ad5d269e35e60537518955e"
EXPECTED_MATHLIB_TREE = "d76f5e09b832a08949f6d8ad4fb80ce30527da64"

EXPECTED_SOURCES = {
    "Mathlib/Condensed/Discrete/Module.lean": "b3ba358aa6b01b2de4cfedf6480ac22e863241d3",
    "Mathlib/Algebra/Category/ModuleCat/Monoidal/Closed.lean": "119610224bb253a976b03764f4e24fd3f662dc6c",
    "Mathlib/CategoryTheory/Sites/Monoidal.lean": "64b111b39f9f44dcab88a7fbe60411ef5008532c",
    "Mathlib/CategoryTheory/Monoidal/Closed/FunctorCategory/Basic.lean": "6f3c9a844bc5f98ef1754263de2e2c54496356ea",
    "Mathlib/CategoryTheory/Monoidal/Closed/Basic.lean": "57dd533860e4be3957c13211f275b6f75441787c",
    "Mathlib/CategoryTheory/Monoidal/Closed/Enrichment.lean": "6083cfbfd92a9e274a6559de438d43e2a3ac600d",
}

FORBIDDEN_TRUE = {
    "p2_e_natural_equivalence_established",
    "p2_closed",
    "cm4_theorem_certified",
    "p3_closed",
    "p4_closed",
    "p5_closed",
    "p6_closed",
    "derived_complex_form_certified",
    "arbitrary_ring_generalization_certified",
    "c04_broadened",
    "c06_discharged",
    "graph_certified",
    "dependency_minimality_claim",
    "dependency_uniqueness_claim",
    "cm5_authorized",
    "global_cmdg_completeness_claim",
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate(data=None):
    record = load(RECORD) if data is None else data
    jsonschema.validate(record, load(SCHEMA))

    assert record["operation_id"] == "CMDG-CONDENSED-CM4-P2-D-001"
    assert record["parent_operation_id"] == "CMDG-CONDENSED-CM4-P2-001"
    assert record["parent_issue"] == 363
    assert record["issue"] == 369
    assert record["implementation_pr"] == 371
    assert record["repository_baseline"] == EXPECTED_BASE
    assert record["repository_baseline_tree"] == EXPECTED_BASE_TREE

    pred = record["protected_predecessor"]
    assert pred["implementation_pr"] == 364
    assert pred["reviewed_head"] == EXPECTED_PREDECESSOR_HEAD
    assert pred["protected_tree"] == EXPECTED_PREDECESSOR_TREE
    assert pred["protected_merge"] == EXPECTED_PREDECESSOR_MERGE
    assert pred["protected_replay_run"] == EXPECTED_PREDECESSOR_RUN
    assert pred["terminal_disposition"] == "OPEN_WITH_CHARACTERIZED_BLOCKER"

    env = record["environment"]
    assert env["mathlib_commit"] == EXPECTED_MATHLIB
    assert env["mathlib_tree"] == EXPECTED_MATHLIB_TREE
    assert env["coefficient_ring"] == "ULift.{u + 1} Z"

    audit = record["exact_tree_audit"]
    assert audit["dedicated_measure_locus_present"] is False
    assert audit["dedicated_measure_locus"] == "Mathlib/Condensed/Measure"
    assert audit["result"] == "RECONSTRUCTIBLE_FROM_GENERAL_CLOSED_MONOIDAL_AND_SHEAF_INTERFACES"
    sources = {row["path"]: row for row in audit["observed_sources"]}
    assert set(EXPECTED_SOURCES) <= set(sources)
    for path, blob in EXPECTED_SOURCES.items():
        row = sources[path]
        assert row["blob"] == blob
        assert row["signature"].strip()
        assert row["variance"].strip()
        assert row["universe_behavior"].strip()
        assert row["evidence_class"] == "FORMAL_REACHABILITY"

    required_decls = {
        "Mathlib/Condensed/Discrete/Module.lean": {
            "CondensedMod.LocallyConstant.functorToPresheaves",
            "CondensedMod.LocallyConstant.functor",
            "CondensedMod.LocallyConstant.functorIsoDiscrete",
            "CondensedMod.LocallyConstant.adjunction",
        },
        "Mathlib/CategoryTheory/Sites/Monoidal.lean": {
            "Presheaf.isSheaf_functorEnrichedHom",
        },
        "Mathlib/CategoryTheory/Monoidal/Closed/FunctorCategory/Basic.lean": {
            "MonoidalClosed.FunctorCategory.homEquiv",
            "MonoidalClosed.FunctorCategory.monoidalClosed",
        },
        "Mathlib/CategoryTheory/Monoidal/Closed/Basic.lean": {
            "MonoidalClosed.pre",
            "MonoidalClosed.pre_id",
            "MonoidalClosed.pre_map",
            "MonoidalClosed.internalHom",
        },
        "Mathlib/CategoryTheory/Monoidal/Closed/Enrichment.lean": {
            "MonoidalClosed.enrichedCategorySelf",
            "MonoidalClosed.enrichedOrdinaryCategorySelf",
        },
    }
    for path, decls in required_decls.items():
        assert decls <= set(sources[path]["declarations"])

    construction = record["construction"]
    assert construction["basis_dependency"] is False
    assert construction["objectwise_product_definition"] is False
    assert construction["variance"] == "COVARIANT_PROFINITE_BY_PULLBACK_THEN_INTERNAL_HOM_PRECOMPOSITION"
    assert "measureFunctor : Profinite -> CondensedMod R" in construction["condensed_functor"]
    assert "dualityHomEquiv" in construction["duality_interface"]

    concordance = record["source_concordance"]
    assert "internalHom(C(S,Z), Z)" in concordance["source_formula"]
    assert "Hom(C(S,Z), Z)" in concordance["underlying_measure_group"]
    assert concordance["product_after_basis_only"] is True
    assert "basis-free" in concordance["interpretation"]
    assert "noncanonical" in concordance["interpretation"]

    guards = record["adversarial_guards"]
    assert all(guards.values())

    stage = record["stage_result"]
    assert stage["p2_d_candidate_reconstructed"] is True
    assert stage["p2_d_protected_available"] is False
    assert stage["p2_e_available"] is False
    assert stage["p2_closed"] is False
    assert stage["candidate_disposition"] == "P2_D_RECONSTRUCTED_PENDING_PROTECTED_ADMISSION"

    claims = record["claim_boundary"]
    for key in FORBIDDEN_TRUE:
        assert claims[key] is False, key
    assert record["disposition"] == "P2_D_RECONSTRUCTED_PENDING_PROTECTED_ADMISSION"

    lean = LEAN.read_text(encoding="utf-8")
    for snippet in (
        "abbrev R := ULift.{u + 1} ℤ",
        "continuousFunctions",
        "discreteContinuousPresheaf",
        "functorEnrichedHom",
        "measurePresheafObj_isSheaf",
        "Presheaf.isSheaf_functorEnrichedHom",
        "measurePresheafFunctor : Profinite.{u} ⥤ PresheafModule",
        "MonoidalClosed.pre",
        "measureFunctor : Profinite.{u} ⥤ CondensedMod.{u} R",
        "dualityHomEquiv",
        "MonoidalClosed.FunctorCategory.homEquiv",
        "open scoped CategoryTheory.MonoidalClosed",
    ):
        assert snippet in lean, snippet

    lowered = lean.lower()
    for forbidden in ("sorry", "axiom ", "unsafe ", "implemented_by"):
        assert forbidden not in lowered, forbidden
    assert "nobeling" not in lowered, "P2-D formal construction must not choose/use a Nobeling basis"
    assert "∏" not in lean and "pi.obj" not in lowered, "P2-D must not be defined by a product substitute"
    assert "def profinitesolid" not in lowered
    assert "profiniteSolid.*≅" not in lean

    report = REPORT.read_text(encoding="utf-8")
    for required in (
        "P2_D_RECONSTRUCTED_PENDING_PROTECTED_ADMISSION",
        "does not identify",
        "Variance audit",
        "Source concordance",
        "basis-free",
        "P2-E",
        "Nonclaims",
    ):
        assert required in report, required

    return record


def mutation_tests():
    base = validate()
    mutations = []

    def mut(path, value):
        d = copy.deepcopy(base)
        cur = d
        for part in path[:-1]:
            cur = cur[part]
        cur[path[-1]] = value
        mutations.append(d)

    mut(("repository_baseline",), "0" * 40)
    mut(("environment", "mathlib_commit"), "0" * 40)
    mut(("exact_tree_audit", "observed_sources"), base["exact_tree_audit"]["observed_sources"][:-1])
    bad_signature = copy.deepcopy(base["exact_tree_audit"]["observed_sources"])
    bad_signature[0]["signature"] = ""
    mut(("exact_tree_audit", "observed_sources"), bad_signature)
    bad_class = copy.deepcopy(base["exact_tree_audit"]["observed_sources"])
    bad_class[0]["evidence_class"] = "SOURCE_CONCORDANCE"
    mut(("exact_tree_audit", "observed_sources"), bad_class)
    mut(("construction", "basis_dependency"), True)
    mut(("construction", "objectwise_product_definition"), True)
    mut(("construction", "variance"), "CONTRAVARIANT_PROFINITE")
    mut(("source_concordance", "product_after_basis_only"), False)
    mut(("adversarial_guards", "chosen_basis_substitute_rejected"), False)
    mut(("stage_result", "p2_d_protected_available"), True)
    mut(("stage_result", "p2_e_available"), True)
    mut(("stage_result", "p2_closed"), True)
    mut(("claim_boundary", "p2_e_natural_equivalence_established"), True)
    mut(("claim_boundary", "cm4_theorem_certified"), True)
    mut(("claim_boundary", "graph_certified"), True)
    mut(("disposition",), "P2_D_PROTECTED_AVAILABLE")

    for i, candidate in enumerate(mutations):
        try:
            validate(candidate)
        except Exception:
            continue
        raise AssertionError(f"mutation {i} was not rejected")


if __name__ == "__main__":
    validate()
    mutation_tests()
    print("CMDG-CONDENSED-CM4-P2-D-001 candidate validation passed")
