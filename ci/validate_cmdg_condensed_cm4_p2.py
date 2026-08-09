#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "governance/cmdg_condensed_cm4_p2_001.json"
SCHEMA = ROOT / "schemas/cmdg_condensed_cm4_p2.schema.json"
LEAN = ROOT / "fixtures/formal/CMDG-NAT-CONCORDANCE-001/CMDGCondensedCM4P2Blocker.lean"
REPORT = ROOT / "governance/CMDG-CONDENSED-CM4-P2-001.md"

EXPECTED_BASE = "5aa885344835be0c462542ab6dce8e17a0b75401"
EXPECTED_BASE_TREE = "cf86f3b98631a4cf3ede24b068ffb0ae092c9a05"
EXPECTED_PARENT_HEAD = "2ddfa2acd531020a29f71f70c5d309dc641846f6"
EXPECTED_PARENT_RUN = 31315335494
EXPECTED_MATHLIB = "79d0395a1825a6264ad5d269e35e60537518955e"
EXPECTED_MATHLIB_TREE = "d76f5e09b832a08949f6d8ad4fb80ce30527da64"
EXPECTED_SOLID_BLOB = "f5214433f91ee87fc8fbe7e2746e0bd227faed2a"
EXPECTED_NOBELING_BLOB = "2989eac53e537e47fd9ac93cba92d50856573173"
EXPECTED_DISCRETE_MODULE_BLOB = "b3ba358aa6b01b2de4cfedf6480ac22e863241d3"

FORBIDDEN_TRUE = {
    "p2_closed",
    "cm4_theorem_certified",
    "cm4_protected_closed",
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

    assert record["operation_id"] == "CMDG-CONDENSED-CM4-P2-001"
    assert record["parent_operation_id"] == "CMDG-CONDENSED-CM4-001"
    assert record["parent_issue"] == 355
    assert record["issue"] == 363
    assert record["repository_baseline"] == EXPECTED_BASE
    assert record["repository_baseline_tree"] == EXPECTED_BASE_TREE

    parent = record["parent_protected_state"]
    assert parent["reviewed_head"] == EXPECTED_PARENT_HEAD
    assert parent["protected_merge"] == EXPECTED_BASE
    assert parent["protected_replay_run"] == EXPECTED_PARENT_RUN
    assert parent["terminal_disposition"] == "OPEN_WITH_CHARACTERIZED_BLOCKER"

    env = record["environment"]
    assert env["mathlib_commit"] == EXPECTED_MATHLIB
    assert env["mathlib_tree"] == EXPECTED_MATHLIB_TREE

    target = record["target"]
    assert "canonical measure/dual" in target["semantic_target"]
    assert "natural equivalence" in target["semantic_target"]
    assert "noncanonical" in target["objectwise_product_role"]
    assert "not a substitute" in target["objectwise_product_role"]

    sources = {row["path"]: row for row in record["exact_tree_audit"]["observed_sources"]}
    solid = sources["Mathlib/Condensed/Solid.lean"]
    assert solid["blob"] == EXPECTED_SOLID_BLOB
    for decl in (
        "Condensed.finFree",
        "Condensed.profiniteSolid",
        "Condensed.profiniteSolidCounit",
        "Condensed.profiniteSolidIsPointwiseRightKanExtension",
        "Condensed.profiniteSolidification",
    ):
        assert decl in solid["declarations"]

    nobeling = sources["Mathlib/Topology/Category/Profinite/Nobeling/Induction.lean"]
    assert nobeling["blob"] == EXPECTED_NOBELING_BLOB
    assert "LocallyConstant.freeOfProfinite" in nobeling["declarations"]

    discrete = sources["Mathlib/Condensed/Discrete/Module.lean"]
    assert discrete["blob"] == EXPECTED_DISCRETE_MODULE_BLOB
    for decl in (
        "CondensedMod.LocallyConstant.functor",
        "CondensedMod.LocallyConstant.functorIsoDiscrete",
        "CondensedMod.LocallyConstant.adjunction",
    ):
        assert decl in discrete["declarations"]

    audit = record["exact_tree_audit"]
    assert "Mathlib/Condensed/Measure" in audit["absent_plausible_loci"]
    assert "BOUNDED_LOCUS_ABSENCE_ONLY" in audit["absence_interpretation"]
    assert "GLOBALLY_ABSENT" in audit["absence_interpretation"]

    matrix = {row["id"]: row for row in record["interface_matrix"]}
    assert set(matrix) == {f"CM4-P2-{c}" for c in "ABCDEF"}
    for key in ("CM4-P2-A", "CM4-P2-B", "CM4-P2-C"):
        assert matrix[key]["status"] == "AVAILABLE"
        assert matrix[key]["reopen_condition"] == "NONE"
    for key in ("CM4-P2-D", "CM4-P2-E"):
        assert matrix[key]["status"] == "BLOCKING"
        assert matrix[key]["reopen_condition"] != "NONE"
    assert matrix["CM4-P2-F"]["status"] == "PARTIAL"
    assert "basis" in matrix["CM4-P2-F"]["reopen_condition"]

    stage = record["stage_result"]
    assert stage["p2_bridge_closed"] is False
    assert stage["canonical_kan_presentation_available"] is True
    assert stage["locally_constant_interface_available"] is True
    assert stage["canonical_measure_dual_functor_available"] is False
    assert stage["natural_equivalence_available"] is False
    assert stage["terminal_operational_disposition"] == "OPEN_WITH_CHARACTERIZED_BLOCKER"

    claims = record["claim_boundary"]
    assert claims["p2_blocker_characterized"] is True
    for key in FORBIDDEN_TRUE:
        assert claims[key] is False, key
    assert record["disposition"] == "OPEN_WITH_CHARACTERIZED_BLOCKER"

    lean = LEAN.read_text(encoding="utf-8")
    for snippet in (
        "Condensed.profiniteSolid",
        "Condensed.profiniteSolidIsPointwiseRightKanExtension",
        "CondensedMod.LocallyConstant.functorIsoDiscrete",
        "LocallyConstant.freeOfProfinite",
        "theorem nobelingAvailable",
        "Module.Free ℤ (LocallyConstant S ℤ)",
    ):
        assert snippet in lean, snippet
    lowered = lean.lower()
    for forbidden in ("sorry", "axiom ", "unsafe ", "implemented_by"):
        assert forbidden not in lowered, forbidden
    assert "theorem p2bridge" not in lowered
    assert "theorem cm4target" not in lowered

    report = REPORT.read_text(encoding="utf-8")
    assert "OPEN_WITH_CHARACTERIZED_BLOCKER" in report
    assert "does **not** certify CM4" in report
    assert "P2-D" in report and "P2-E" in report
    assert "noncanonical" in report

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
    mut(("parent_protected_state", "terminal_disposition"), "CLOSED")
    mut(("environment", "mathlib_commit"), "0" * 40)
    mut(("stage_result", "p2_bridge_closed"), True)
    mut(("stage_result", "canonical_measure_dual_functor_available"), True)
    mut(("stage_result", "natural_equivalence_available"), True)
    mut(("claim_boundary", "p2_closed"), True)
    mut(("claim_boundary", "cm4_theorem_certified"), True)
    mut(("claim_boundary", "p3_closed"), True)
    mut(("claim_boundary", "graph_certified"), True)
    mut(("disposition",), "CMDG_CONDENSED_CM4_P2_001_PROTECTED_CLOSED")

    for target_id in ("CM4-P2-D", "CM4-P2-E"):
        d = copy.deepcopy(base)
        for row in d["interface_matrix"]:
            if row["id"] == target_id:
                row["status"] = "AVAILABLE"
        mutations.append(d)

    d = copy.deepcopy(base)
    d["target"]["objectwise_product_role"] = "Chosen basis gives a natural equivalence."
    mutations.append(d)

    for i, d in enumerate(mutations):
        try:
            validate(d)
        except Exception:
            continue
        raise AssertionError(f"mutation {i} was not rejected")


if __name__ == "__main__":
    validate()
    mutation_tests()
    print("CMDG-CONDENSED-CM4-P2-001 blocker validation passed")
