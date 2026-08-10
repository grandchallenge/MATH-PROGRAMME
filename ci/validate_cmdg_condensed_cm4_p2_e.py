#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import re
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "governance/cmdg_condensed_cm4_p2_e_001.json"
SCHEMA = ROOT / "schemas/cmdg_condensed_cm4_p2_e.schema.json"
REPORT = ROOT / "governance/CMDG-CONDENSED-CM4-P2-E-001.md"
LEAN = ROOT / "fixtures/formal/CMDG-NAT-CONCORDANCE-001/CMDGCondensedCM4P2E.lean"

EXPECTED_BASE = "839e04e1b862ffddfe5ce1d4d733ba954cd45d96"
EXPECTED_BASE_TREE = "ac1e21d2746ad951a9aa3c747895b28f56092bf8"
EXPECTED_P2D_HEAD = "358466932fde181c927cd428613f4578f38bfc1c"
EXPECTED_P2D_TREE = "ac1e21d2746ad951a9aa3c747895b28f56092bf8"
EXPECTED_P2D_MERGE = "839e04e1b862ffddfe5ce1d4d733ba954cd45d96"
EXPECTED_P2D_REPLAY = 31342558880
EXPECTED_POLICY = 31342558852
EXPECTED_CONFORMANCE = 31342559115
EXPECTED_MATHLIB = "79d0395a1825a6264ad5d269e35e60537518955e"
EXPECTED_MATHLIB_TREE = "d76f5e09b832a08949f6d8ad4fb80ce30527da64"

EXPECTED_SOURCES = {
    "Mathlib/Condensed/Solid.lean": "f5214433f91ee87fc8fbe7e2746e0bd227faed2a",
    "Mathlib/CategoryTheory/Functor/KanExtension/Basic.lean": "1d8ed3b224af14a8d909ada051de840ae3d5c59c",
    "Mathlib/CategoryTheory/Functor/KanExtension/Pointwise.lean": "eca4f781a97fc9948e726bb4b89a9ab1bc255f96",
    "Mathlib/Condensed/Discrete/Colimit.lean": "7579e7ecc282d20d4c61d4e5d0e3e37994069e11",
    "fixtures/formal/CMDG-NAT-CONCORDANCE-001/CMDGCondensedCM4P2D.lean":
        "7515583c1b56308bbd48c2c690addd3b432eba09",
}

FORBIDDEN_TRUE = {
    "p2_e_protected_available",
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

    assert record["operation_id"] == "CMDG-CONDENSED-CM4-P2-E-001"
    assert record["parent_operation_id"] == "CMDG-CONDENSED-CM4-P2-001"
    assert record["parent_issue"] == 363
    assert record["issue"] == 370
    assert record["implementation_pr"] == 376
    assert record["repository_baseline"] == EXPECTED_BASE
    assert record["repository_baseline_tree"] == EXPECTED_BASE_TREE

    pred = record["protected_predecessor"]
    assert pred["operation_id"] == "CMDG-CONDENSED-CM4-P2-D-001"
    assert pred["issue"] == 369
    assert pred["implementation_pr"] == 371
    assert pred["reviewed_head"] == EXPECTED_P2D_HEAD
    assert pred["protected_tree"] == EXPECTED_P2D_TREE
    assert pred["protected_merge"] == EXPECTED_P2D_MERGE
    assert pred["protected_replay_run"] == EXPECTED_P2D_REPLAY
    assert pred["programme_policy_run"] == EXPECTED_POLICY
    assert pred["gcl_conformance_run"] == EXPECTED_CONFORMANCE
    assert pred["state"] == "AVAILABLE"

    env = record["environment"]
    assert env["mathlib_commit"] == EXPECTED_MATHLIB
    assert env["mathlib_tree"] == EXPECTED_MATHLIB_TREE
    assert env["coefficient_ring"] == "ULift.{u + 1} Z"

    audit = record["exact_tree_audit"]
    assert audit["result"] == "FORMAL_ROUTE_REACHABLE_WITH_TWO_CONSTRUCTION_OBLIGATIONS"
    sources = {row["path"]: row for row in audit["observed_sources"]}
    assert set(sources) == set(EXPECTED_SOURCES)
    for path, blob in EXPECTED_SOURCES.items():
        row = sources[path]
        assert row["blob"] == blob
        assert row["declarations"]
        assert row["signature"].strip()
        assert row["variance"].strip()
        assert row["universe_behavior"].strip()
        assert row["evidence_class"] == "FORMAL_REACHABILITY"
        assert row["role"].strip()

    target = record["theorem_target"]
    assert target["fixture"] == \
        "fixtures/formal/CMDG-NAT-CONCORDANCE-001/CMDGCondensedCM4P2E.lean"
    assert target["finite_comparison"] == \
        "FintypeCat.toProfinite ⋙ measureFunctor ≅ Condensed.finFree R"
    assert target["global_comparison"] == \
        "measureFunctor ≅ Condensed.profiniteSolid R"
    assert target["basis_dependency"] is False
    assert target["objectwise_only_allowed"] is False
    assert target["variance"] == "COVARIANT_PROFINITE_NATURAL_ISO"

    arch = record["proof_architecture"]
    assert arch["finite_level_comparison"]["state"] == "OPEN_CONSTRUCTION"
    assert arch["measure_right_kan_extension"]["state"] == "OPEN_CONSTRUCTION"
    assert arch["kan_extension_uniqueness"]["state"] == "FORMALLY_AVAILABLE"

    guards = record["adversarial_guards"]
    assert all(guards.values())

    stage = record["stage_result"]
    assert stage["p2_d_protected_available"] is True
    assert stage["p2_e_theorem_target_frozen"] is True
    assert stage["p2_e_natural_equivalence_established"] is False
    assert stage["p2_e_protected_available"] is False
    assert stage["p2_closed"] is False
    assert stage["candidate_disposition"] == \
        "P2_E_COMPARISON_AUDIT_COMPLETE_RECONSTRUCTION_ACTIVE"

    for key in FORBIDDEN_TRUE:
        assert record["claim_boundary"][key] is False

    assert record["disposition"] == \
        "P2_E_COMPARISON_AUDIT_COMPLETE_RECONSTRUCTION_ACTIVE"

    lean = LEAN.read_text(encoding="utf-8")
    assert "abbrev FiniteComparisonTarget := finiteMeasure ≅ finiteFree" in lean
    assert "abbrev ComparisonTarget := measureFunctor ≅ solidFunctor" in lean
    for token in (
        "#check Condensed.profiniteSolidIsPointwiseRightKanExtension",
        "#check Functor.rightKanExtensionUniqueOfIso",
        "#check Condensed.isColimitLocallyConstantPresheafDiagram",
        "#check CMDG.CondensedCM4P2D.measureFunctor",
    ):
        assert token in lean

    assert not re.search(r"(?m)^\s*(sorry|axiom)(\s|$)", lean)
    assert "LocallyConstant.freeOfProfinite" not in lean
    assert "Nobeling" not in lean
    assert "Nöbeling" not in lean

    report = REPORT.read_text(encoding="utf-8")
    for token in (
        "FORMAL_ROUTE_REACHABLE_WITH_TWO_CONSTRUCTION_OBLIGATIONS",
        "E1 — canonical finite comparison",
        "E2 — measure functor as right Kan extension",
        "E3 — canonical uniqueness",
        "P2_E_COMPARISON_AUDIT_COMPLETE_RECONSTRUCTION_ACTIVE",
        "does **not** establish",
    ):
        assert token in report

    return record


def mutated(mutator):
    data = copy.deepcopy(load(RECORD))
    mutator(data)
    return data


def main() -> int:
    validate()
    print("CMDG-CONDENSED-CM4-P2-E-001 comparison audit record: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
