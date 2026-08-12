#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "governance/cmdg_condensed_cm4_001.json"
SCHEMA = ROOT / "schemas/cmdg_condensed_cm4.schema.json"
LEAN = ROOT / "fixtures/formal/CMDG-NAT-CONCORDANCE-001/CMDGCondensedCM4Blocker.lean"
REPORT = ROOT / "governance/CMDG-CONDENSED-CM4-001.md"

EXPECTED_BASE = "d9b9ed1a3a4c7ab56d25091e724fa585fbcea071"
EXPECTED_BASE_TREE = "2a7bd5d53af76b6705ebd526dae667a381860374"
EXPECTED_RECONCILIATION_BASE = "2abad244b57ab148184b3033524b7ec636cb7c7f"
EXPECTED_RECONCILIATION_TREE = "6c8c6ba86306571ed75294977842af8b3beeb245"
EXPECTED_C05_MERGE = "a480fcecf8137ac7bd29534043623d09afab0a12"
EXPECTED_MATHLIB = "79d0395a1825a6264ad5d269e35e60537518955e"
EXPECTED_MATHLIB_TREE = "d76f5e09b832a08949f6d8ad4fb80ce30527da64"
EXPECTED_SOLID_BLOB = "f5214433f91ee87fc8fbe7e2746e0bd227faed2a"
EXPECTED_NOBELING_BLOB = "2989eac53e537e47fd9ac93cba92d50856573173"
EXPECTED_LIGHT_PROJECTIVE_BLOB = "91b0b495e708368b0d5f58bb2865490d18d90657"
EXPECTED_P2_HEAD = "36d29b4dea3b3049016e3a7277923cb37a7579f4"
EXPECTED_P2_MERGE = "2abad244b57ab148184b3033524b7ec636cb7c7f"
EXPECTED_P2_TREE = "6c8c6ba86306571ed75294977842af8b3beeb245"
EXPECTED_P2_REPLAY = 31549886295
EXPECTED_P2_E_REPLAY = 31549886166
EXPECTED_POLICY = 31549886179
EXPECTED_GCL = 31549886679
CANDIDATE_DISPOSITION = "CM4_DEPENDENCY_RECONCILIATION_READY__P3_NEXT_PENDING_PROTECTED_ADMISSION"

FORBIDDEN_TRUE = {
    "cm4_theorem_certified",
    "cm4_protected_closed",
    "derived_complex_form_certified",
    "arbitrary_finite_type_z_algebra_free_solid_certified",
    "arbitrary_commutative_ring_certified",
    "noncommutative_ring_certified",
    "pinned_reconstructed_c05_equivalence_certified",
    "solid_subcategory_abelian_certified",
    "solidification_reflector_certified",
    "tensor_internal_hom_closure_certified",
    "liquid_mathematics_certified",
    "c04_broadened",
    "c06_discharged",
    "graph_certified",
    "dependency_minimality_claim",
    "dependency_uniqueness_claim",
    "global_cmdg_completeness_claim",
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate(data=None):
    record = load(RECORD) if data is None else data
    jsonschema.validate(record, load(SCHEMA))

    assert record["repository_baseline"] == EXPECTED_BASE
    assert record["repository_baseline_tree"] == EXPECTED_BASE_TREE
    predecessor = record["protected_predecessor"]
    assert predecessor["merge_commit"] == EXPECTED_C05_MERGE
    assert predecessor["terminal_disposition"] == "CMDG_SOLID_C05_001_PROTECTED_CLOSED"

    env = record["environment"]
    assert env["mathlib_commit"] == EXPECTED_MATHLIB
    assert env["mathlib_tree"] == EXPECTED_MATHLIB_TREE

    target = record["formal_target"]["lean_statement"]
    assert "∀ S : Profinite.{u}" in target
    assert "ULift.{u + 1} ℤ" in target
    assert "CondensedMod.IsSolid" in target
    assert "Condensed.profiniteSolid" in target

    sources = {row["path"]: row for row in record["exact_tree_audit"]["observed_sources"]}
    assert sources["Mathlib/Condensed/Solid.lean"]["blob"] == EXPECTED_SOLID_BLOB
    assert sources["Mathlib/Topology/Category/Profinite/Nobeling/Induction.lean"]["blob"] == EXPECTED_NOBELING_BLOB
    assert sources["Mathlib/Condensed/Light/InternallyProjective.lean"]["blob"] == EXPECTED_LIGHT_PROJECTIVE_BLOB
    assert "LocallyConstant.freeOfProfinite" in sources["Mathlib/Topology/Category/Profinite/Nobeling/Induction.lean"]["declarations"]

    absent = set(record["exact_tree_audit"]["absent_plausible_loci"])
    assert {
        "Mathlib/Condensed/Derived",
        "Mathlib/Condensed/Measure",
        "Mathlib/Condensed/Real",
        "Mathlib/Condensed/Circle",
    } <= absent
    assert "DOES_NOT_CLAIM_RELEVANT_CATEGORY_THEORY_IS_GLOBALLY_ABSENT" in record["exact_tree_audit"]["absence_interpretation"]

    reconciliation = record["dependency_reconciliation"]
    assert reconciliation["reconciliation_baseline"] == EXPECTED_RECONCILIATION_BASE
    assert reconciliation["reconciliation_baseline_tree"] == EXPECTED_RECONCILIATION_TREE
    receipt = reconciliation["protected_p2_receipt"]
    assert receipt == {
        "operation": "CMDG-CONDENSED-CM4-P2-001",
        "issue": "MATH-PROGRAMME#363",
        "pull_request": "MATH-PROGRAMME#443",
        "reviewed_head": EXPECTED_P2_HEAD,
        "protected_merge": EXPECTED_P2_MERGE,
        "protected_tree": EXPECTED_P2_TREE,
        "protected_p2_replay": EXPECTED_P2_REPLAY,
        "protected_p2_e_replay": EXPECTED_P2_E_REPLAY,
        "programme_policy": EXPECTED_POLICY,
        "gcl_conformance": EXPECTED_GCL,
        "state": "PROTECTED_CLOSED",
    }
    assert set(reconciliation["remaining_root_blockers"]) == {"CM4-P3", "CM4-P5"}
    assert reconciliation["selected_next_lane"] == "CM4-P3"
    assert reconciliation["selection_class"] == "OPERATIONAL_SELECTION_NOT_MINIMALITY_OR_UNIQUENESS_THEOREM"
    assert "separately governed direct alternative" in reconciliation["p4_route_rule"]
    assert "MUST NOT continue to be represented as blocking" in reconciliation["p2_effect"]

    matrix = {row["id"]: row for row in record["prerequisite_matrix"]}
    assert set(matrix) == {"CM4-P1", "CM4-P2", "CM4-P3", "CM4-P4", "CM4-P5", "CM4-P6"}

    assert matrix["CM4-P1"]["status"] == "AVAILABLE"
    assert matrix["CM4-P1"]["reopen_condition"] == "NONE"

    p2 = matrix["CM4-P2"]
    assert p2["status"] == "AVAILABLE"
    assert p2["route_role"] == "PROTECTED_CLOSED"
    assert p2["reopen_condition"] == "NONE"
    assert p2["depends_on"] == []
    assert "31549886295 SUCCESS" in p2["evidence"][1]

    p3 = matrix["CM4-P3"]
    assert p3["status"] == "BLOCKING"
    assert p3["route_role"] == "READY_NEXT"
    assert p3["depends_on"] == []
    assert p3["reopen_condition"] != "NONE"

    p5 = matrix["CM4-P5"]
    assert p5["status"] == "BLOCKING"
    assert p5["route_role"] == "SOURCE_ROUTE_PREREQUISITE_FOR_P4"
    assert p5["depends_on"] == []
    assert p5["reopen_condition"] != "NONE"

    p4 = matrix["CM4-P4"]
    assert p4["status"] == "BLOCKING"
    assert p4["route_role"] == "WAITS_ON_P5_SOURCE_ROUTE_OR_SEPARATELY_GOVERNED_DIRECT_ALTERNATIVE"
    assert p4["depends_on"] == ["CM4-P5"]
    assert "direct alternative" in p4["reopen_condition"]

    p6 = matrix["CM4-P6"]
    assert p6["status"] == "PARTIAL_BLOCKING"
    assert p6["route_role"] == "WAITS_ON_P3_AND_P4_P2_DISCHARGED"
    assert p6["depends_on"] == ["CM4-P3", "CM4-P4"]
    assert p6["reopen_condition"] != "NONE"

    stage = record["stage_a_result"]
    assert stage["dependency_reconciliation_complete"] is True
    assert stage["dependency_closure_sufficient"] is False
    assert stage["theorem_attempt_authorized"] is False
    assert stage["p2_protected_closed"] is True
    assert stage["p2_blocks_cm4"] is False
    assert stage["selected_next_lane"] == "CM4-P3"
    assert stage["next_lane_opening_authorized"] is False
    assert stage["terminal_operational_disposition"] == CANDIDATE_DISPOSITION
    assert record["disposition"] == CANDIDATE_DISPOSITION

    claims = record["claim_boundary"]
    assert claims["blocker_characterized"] is True
    for key in FORBIDDEN_TRUE:
        assert claims[key] is False, key

    lean = LEAN.read_text(encoding="utf-8")
    required_lean = (
        "def CM4Target : Prop",
        "∀ S : Profinite.{u}",
        "ULift.{u + 1} ℤ",
        "CondensedMod.IsSolid ZLift",
        "Condensed.profiniteSolid ZLift",
        "theorem nobelingAvailable",
        "Module.Free ℤ (LocallyConstant S ℤ)",
        "infer_instance",
    )
    for snippet in required_lean:
        assert snippet in lean, snippet
    lowered = lean.lower()
    for forbidden in ("sorry", "axiom ", "unsafe ", "implemented_by"):
        assert forbidden not in lowered, forbidden
    assert "theorem cm4target" not in lowered

    report = REPORT.read_text(encoding="utf-8")
    assert CANDIDATE_DISPOSITION in report
    assert "This package does **not** certify CM4" in report
    assert "CM4-P2 — protected-closed / available" in report
    assert "CM4-P3 — selected next lane" in report
    assert "P5 → P4" in report
    for key in ("CM4-P1", "CM4-P2", "CM4-P3", "CM4-P4", "CM4-P5", "CM4-P6"):
        assert key in report

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
    mut(("dependency_reconciliation", "reconciliation_baseline"), "0" * 40)
    mut(("dependency_reconciliation", "protected_p2_receipt", "reviewed_head"), "0" * 40)
    mut(("dependency_reconciliation", "protected_p2_receipt", "protected_p2_replay"), 0)
    mut(("dependency_reconciliation", "selected_next_lane"), "CM4-P4")
    mut(("dependency_reconciliation", "remaining_root_blockers"), ["CM4-P3", "CM4-P4"])
    mut(("stage_a_result", "p2_blocks_cm4"), True)
    mut(("stage_a_result", "selected_next_lane"), "CM4-P5")
    mut(("stage_a_result", "next_lane_opening_authorized"), True)
    mut(("stage_a_result", "dependency_closure_sufficient"), True)
    mut(("stage_a_result", "theorem_attempt_authorized"), True)
    mut(("disposition",), "CMDG_CONDENSED_CM4_001_PROTECTED_CLOSED")
    mut(("claim_boundary", "cm4_theorem_certified"), True)
    mut(("claim_boundary", "c06_discharged"), True)
    mut(("claim_boundary", "graph_certified"), True)
    mut(("claim_boundary", "dependency_minimality_claim"), True)
    mut(("claim_boundary", "dependency_uniqueness_claim"), True)

    by_id = {row["id"]: i for i, row in enumerate(base["prerequisite_matrix"])}

    d = copy.deepcopy(base)
    d["prerequisite_matrix"][by_id["CM4-P2"]]["status"] = "BLOCKING"
    mutations.append(d)

    d = copy.deepcopy(base)
    d["prerequisite_matrix"][by_id["CM4-P3"]]["route_role"] = "WAIT"
    mutations.append(d)

    d = copy.deepcopy(base)
    d["prerequisite_matrix"][by_id["CM4-P4"]]["depends_on"] = []
    mutations.append(d)

    d = copy.deepcopy(base)
    d["prerequisite_matrix"][by_id["CM4-P5"]]["route_role"] = "OPTIONAL"
    mutations.append(d)

    d = copy.deepcopy(base)
    d["prerequisite_matrix"][by_id["CM4-P6"]]["status"] = "AVAILABLE"
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
    print("CMDG-CONDENSED-CM4-001 dependency reconciliation validation passed")
