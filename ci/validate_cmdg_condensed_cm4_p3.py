#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "governance/cmdg_condensed_cm4_p3_001.json"
SCHEMA = ROOT / "schemas/cmdg_condensed_cm4_p3.schema.json"
REPORT = ROOT / "governance/CMDG-CONDENSED-CM4-P3-001.md"
LEAN = ROOT / "fixtures/formal/CMDG-NAT-CONCORDANCE-001/CMDGCondensedCM4P3Audit.lean"

EXPECTED_BASE = "bc2eb8757a89cfee96f57d724480d9deb9135b4a"
EXPECTED_BASE_TREE = "49f7fd4c6a10e6067139f01ea6437400100dae71"
EXPECTED_MATHLIB = "79d0395a1825a6264ad5d269e35e60537518955e"
EXPECTED_MATHLIB_TREE = "d76f5e09b832a08949f6d8ad4fb80ce30527da64"
EXPECTED_SOURCES = {
    "Mathlib/Algebra/Homology/DerivedCategory/Ext/Basic.lean": ("2ee4d31030b25e6886bf6884046b33727385e0d3", "AVAILABLE_GENERIC_EXT"),
    "Mathlib/Algebra/Homology/DerivedCategory/Ext/EnoughInjectives.lean": ("d7b9f8c1a97059c57b9902e5e5e910310c863777", "AVAILABLE_INJECTIVE_VANISHING"),
    "Mathlib/Algebra/Homology/DerivedCategory/Ext/EnoughProjectives.lean": ("2dc52050bd2d7dc83315085de972962ca79522ed", "AVAILABLE_PROJECTIVE_VANISHING"),
    "Mathlib/CategoryTheory/Sites/Abelian.lean": ("d5250edfc56c2d79c7dae942fe0ab1e8a93ac707", "AVAILABLE_SHEAF_ABELIAN_STRUCTURE"),
    "Mathlib/CategoryTheory/Sites/GlobalSections.lean": ("9d1bb0ed58be3f99e96ba5ddaf8a33abdd9a72d7", "AVAILABLE_GLOBAL_SECTIONS_RIGHT_ADJOINT"),
    "Mathlib/CategoryTheory/Sites/SheafCohomology/Basic.lean": ("c2f49b4e071c5e5e30b7a7aaaa1fc2656d4ef7e5", "AVAILABLE_SHEAF_COHOMOLOGY_AS_EXT"),
    "Mathlib/CategoryTheory/Sites/SheafCohomology/Cech.lean": ("fa984791594387b9f3e2e435f88390e21e83ea1b", "AVAILABLE_CECH_COMPLEX_INFRASTRUCTURE"),
    "Mathlib/Condensed/Discrete/Module.lean": ("b3ba358aa6b01b2de4cfedf6480ac22e863241d3", "AVAILABLE_DISCRETE_LOCALLY_CONSTANT_MODEL"),
    "Mathlib/Condensed/Discrete/Characterization.lean": ("50046d821d15f9eb651d6b1dc91a3df94f951c79", "AVAILABLE_DISCRETE_CHARACTERIZATION"),
    "Mathlib/Condensed/Epi.lean": ("566eb699008b5158d79c743317383b4b9de6455d", "AVAILABLE_ORDINARY_CONDENSED_EPI"),
    "Mathlib/CategoryTheory/Preadditive/Projective/Internal.lean": ("ee04c3c01d315f763caca98563b19079c625fd76", "AVAILABLE_GENERIC_INTERNAL_PROJECTIVITY"),
    "Mathlib/Condensed/Light/InternallyProjective.lean": ("91b0b495e708368b0d5f58bb2865490d18d90657", "AVAILABLE_LIGHT_CONDENSED_ANALOGUE_ONLY"),
    "Mathlib/Topology/Category/Profinite/Projective.lean": ("4a0091b41978cc737b5e7c3455570628a37ac361", "AVAILABLE_PROFINITE_ENOUGH_PROJECTIVES"),
    "Mathlib/Topology/Separation/Profinite.lean": ("1bc259a4f9b82065f51d4c7f5d3c6fd7396ef122", "AVAILABLE_CLOPEN_REFINEMENT"),
}
FORBIDDEN_TRUE = {
    "p3_available", "p3_nonblocking_source_auxiliary", "p4_available", "p5_available",
    "p6_available", "cm4_theorem_certified", "derived_complex_form_certified",
    "arbitrary_ring_generalization_certified", "c04_broadened", "c06_discharged",
    "graph_certified", "dependency_minimality_claim", "dependency_uniqueness_claim",
    "cm5_authorized", "global_cmdg_completeness_claim",
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate(data=None):
    record = load(RECORD) if data is None else data
    jsonschema.validate(record, load(SCHEMA))
    assert record["operation_id"] == "CMDG-CONDENSED-CM4-P3-001"
    assert record["parent_operation_id"] == "CMDG-CONDENSED-CM4-001"
    assert record["parent_issue"] == 355
    assert record["issue"] == 448
    assert record["implementation_pr"] == 453
    assert record["repository_baseline"] == EXPECTED_BASE
    assert record["repository_baseline_tree"] == EXPECTED_BASE_TREE

    pred = record["protected_predecessor"]
    assert pred["operation"] == "CMDG-CONDENSED-CM4-001"
    assert pred["issue"] == 355
    assert pred["reconciliation_pr"] == 451
    assert pred["reviewed_head"] == "24b7a9084c4a753176fd0ba7ab91145e6bdd9022"
    assert pred["protected_merge"] == EXPECTED_BASE
    assert pred["protected_tree"] == EXPECTED_BASE_TREE
    assert pred["p3_selected"] is True
    p2 = pred["protected_p2_receipt"]
    assert p2["operation"] == "CMDG-CONDENSED-CM4-P2-001"
    assert p2["issue"] == 363
    assert p2["reconciliation_pr"] == 443
    assert p2["reviewed_head"] == "36d29b4dea3b3049016e3a7277923cb37a7579f4"
    assert p2["protected_merge"] == "2abad244b57ab148184b3033524b7ec636cb7c7f"
    assert p2["protected_tree"] == "6c8c6ba86306571ed75294977842af8b3beeb245"
    assert p2["protected_replay_run"] == 31549886295
    assert p2["terminal_readback"] == "CM4_P2_PROTECTED_CLOSED"
    assert p2["p2_closed"] is True

    env = record["environment"]
    assert env["mathlib_commit"] == EXPECTED_MATHLIB
    assert env["mathlib_tree"] == EXPECTED_MATHLIB_TREE
    assert env["coefficient_ring"] == "ULift.{u + 1} Z"

    audit = record["exact_tree_audit"]
    assert audit["result"] == "BLOCKER_NARROWED_TO_PROFINITE_DISCRETE_ACYCLICITY_OR_CERTIFIED_UNDERIVED_REDUCTION"
    rows = {row["path"]: row for row in audit["observed_sources"]}
    assert set(rows) == set(EXPECTED_SOURCES)
    for path, (blob, classification) in EXPECTED_SOURCES.items():
        assert rows[path]["blob"] == blob
        assert rows[path]["classification"] == classification
        assert rows[path]["declarations"]
    assert len(audit["not_found_in_bounded_audit"]) >= 6

    route = record["route_assessment"]
    assert route["source_path"] == "PARTIAL_INFRASTRUCTURE_AVAILABLE_BLOCKING_SPECIALIZATION_MISSING"
    assert route["p2_underived_bypass"] == "NOT_ESTABLISHED"
    assert route["light_condensed_analogue_is_authority"] is False
    assert route["absence_of_condensed_derived_directory_is_blocker"] is False

    stage = record["stage_result"]
    assert stage["p3_state"] == "BLOCKING"
    assert stage["audit_complete"] is True
    assert stage["p3_theorem_certified"] is False
    assert stage["p3_nonblocking_bypass_certified"] is False
    assert stage["candidate_disposition"] == "OPEN_WITH_CHARACTERIZED_BLOCKER"
    assert "machine-checked" in record["reopening_condition"]
    assert "CondensedMod.IsSolid" in record["reopening_condition"]

    for key in FORBIDDEN_TRUE:
        assert record["claim_boundary"][key] is False, key
    assert record["disposition"] == "OPEN_WITH_CHARACTERIZED_BLOCKER"

    lean = LEAN.read_text(encoding="utf-8")
    required = (
        "CategoryTheory.Abelian.Ext.subsingleton_of_injective",
        "CategoryTheory.Abelian.Ext.subsingleton_of_projective",
        "CategoryTheory.hasExt_of_enoughInjectives",
        "CategoryTheory.sheafIsAbelian",
        "CategoryTheory.Sheaf.ΓNatIsoLim",
        "CategoryTheory.Sheaf.H'",
        "CategoryTheory.cechComplexFunctor",
        "CategoryTheory.InternallyProjective",
        "CondensedMod.LocallyConstant.functorIsoDiscrete",
        "CondensedMod.isDiscrete_tfae",
        "CondensedMod.epi_iff_surjective_on_stonean",
        "LightCondensed.internallyProjective_iff_tensor_condition",
        "Profinite.projectivePresentation",
        "exists_clopen_partition_of_clopen_cover",
    )
    for snippet in required:
        assert snippet in lean, snippet
    lowered = lean.lower()
    for forbidden in ("sorry", "axiom ", "unsafe ", "implemented_by"):
        assert forbidden not in lowered, forbidden
    assert "theorem p3" not in lowered
    assert "instance p3" not in lowered

    report = REPORT.read_text(encoding="utf-8")
    for snippet in (
        "OPEN_WITH_CHARACTERIZED_BLOCKER", "CM4-P3 remains **BLOCKING**",
        "bounded exact-tree result", "LightCondensed.internallyProjective_iff_tensor_condition",
        "injective", "global sections", "Čech", "CondensedMod.IsSolid", "Nonclaims",
    ):
        assert snippet in report, snippet
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
    mut(("stage_result", "p3_state"), "AVAILABLE")
    mut(("stage_result", "p3_theorem_certified"), True)
    mut(("route_assessment", "p2_underived_bypass"), "CERTIFIED")
    mut(("route_assessment", "light_condensed_analogue_is_authority"), True)
    mut(("route_assessment", "absence_of_condensed_derived_directory_is_blocker"), True)
    mut(("claim_boundary", "cm4_theorem_certified"), True)
    mut(("claim_boundary", "graph_certified"), True)
    bad_sources = copy.deepcopy(base["exact_tree_audit"]["observed_sources"])
    bad_sources[-1]["blob"] = "0" * 40
    mut(("exact_tree_audit", "observed_sources"), bad_sources)
    mut(("disposition",), "P3_AVAILABLE")

    for i, candidate in enumerate(mutations):
        try:
            validate(candidate)
        except Exception:
            continue
        raise AssertionError(f"mutation {i} was not rejected")


if __name__ == "__main__":
    validate()
    mutation_tests()
    print("CMDG-CONDENSED-CM4-P3-001 audit/blocker validation passed")