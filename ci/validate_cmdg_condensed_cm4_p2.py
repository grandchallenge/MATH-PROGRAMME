#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import re
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "governance/cmdg_condensed_cm4_p2_001.json"
SCHEMA = ROOT / "schemas/cmdg_condensed_cm4_p2.schema.json"
BLOCKER_LEAN = ROOT / "fixtures/formal/CMDG-NAT-CONCORDANCE-001/CMDGCondensedCM4P2Blocker.lean"
P2D_LEAN = ROOT / "fixtures/formal/CMDG-NAT-CONCORDANCE-001/CMDGCondensedCM4P2D.lean"
P2E_E3_LEAN = ROOT / "fixtures/formal/CMDG-NAT-CONCORDANCE-001/CMDGCondensedCM4P2EE3.lean"
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

EXPECTED_RECONCILIATION_BASE = "e35f3647f31f7092dec9de192f6b09186b2b1127"
EXPECTED_RECONCILIATION_TREE = "015097bae518d16f37fb17e9601fba62c6f8a711"

EXPECTED_P2D = {
    "issue": 369,
    "implementation_pr": 371,
    "reviewed_head": "358466932fde181c927cd428613f4578f38bfc1c",
    "protected_tree": "ac1e21d2746ad951a9aa3c747895b28f56092bf8",
    "protected_merge": "839e04e1b862ffddfe5ce1d4d733ba954cd45d96",
    "protected_replay_run": 31342558880,
    "programme_policy_run": 31342558852,
    "gcl_conformance_run": 31342559115,
    "state": "AVAILABLE",
}
EXPECTED_P2E = {
    "issue": 370,
    "implementation_pr": 376,
    "reviewed_head": "1968046f46d3633c640431a9fe82e03055219ab2",
    "protected_tree": "015097bae518d16f37fb17e9601fba62c6f8a711",
    "protected_merge": "e35f3647f31f7092dec9de192f6b09186b2b1127",
    "protected_replay_run": 31547026193,
    "programme_policy_run": 31547026219,
    "gcl_conformance_run": 31547026590,
    "state": "AVAILABLE",
}
EXPECTED_DISPOSITION = "P2_CLOSURE_READY_PENDING_PROTECTED_ADMISSION"

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
    role = target["objectwise_product_role"]
    for token in ("noncanonical", "not a substitute", "not an independent CM4-P2 closure requirement"):
        assert token in role

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

    reconciliation = record["reconciliation"]
    assert reconciliation["baseline_main"] == EXPECTED_RECONCILIATION_BASE
    assert reconciliation["baseline_tree"] == EXPECTED_RECONCILIATION_TREE
    assert reconciliation["p2_d"] == EXPECTED_P2D
    assert reconciliation["p2_e"] == EXPECTED_P2E
    assert reconciliation["p2_f_classification"] == "NON_BLOCKING_AUXILIARY_OBJECTWISE_PRESENTATION"
    p2f_reason = reconciliation["p2_f_rationale"]
    for token in ("basis-dependent", "rejects it as a substitute for naturality", "no remaining independent closure obligation"):
        assert token in p2f_reason

    matrix = {row["id"]: row for row in record["interface_matrix"]}
    assert set(matrix) == {f"CM4-P2-{c}" for c in "ABCDEF"}
    for key in ("CM4-P2-A", "CM4-P2-B", "CM4-P2-C", "CM4-P2-D", "CM4-P2-E"):
        assert matrix[key]["status"] == "AVAILABLE"
        assert matrix[key]["closure_role"] == "REQUIRED"
        assert matrix[key]["reopen_condition"] == "NONE"

    p2f = matrix["CM4-P2-F"]
    assert p2f["status"] == "PARTIAL"
    assert p2f["closure_role"] == "NON_BLOCKING_AUXILIARY"
    assert "NONE_FOR_P2_CLOSURE" in p2f["reopen_condition"]
    assert "basis" in p2f["reopen_condition"]
    assert "must not be promoted to naturality" in p2f["reopen_condition"]

    stage = record["stage_result"]
    assert stage["p2_acceptance_reconciled"] is True
    assert stage["p2_closure_candidate"] is True
    assert stage["p2_protected_closed"] is False
    assert stage["canonical_kan_presentation_available"] is True
    assert stage["locally_constant_interface_available"] is True
    assert stage["canonical_measure_dual_functor_available"] is True
    assert stage["natural_equivalence_available"] is True
    assert stage["p2_f_blocks_closure"] is False
    assert stage["terminal_operational_disposition"] == EXPECTED_DISPOSITION

    claims = record["claim_boundary"]
    assert claims["p2_blocker_characterized"] is True
    for key in FORBIDDEN_TRUE:
        assert claims[key] is False, key
    assert record["disposition"] == EXPECTED_DISPOSITION

    blocker_lean = BLOCKER_LEAN.read_text(encoding="utf-8")
    for snippet in (
        "Condensed.profiniteSolid",
        "Condensed.profiniteSolidIsPointwiseRightKanExtension",
        "CondensedMod.LocallyConstant.functorIsoDiscrete",
        "LocallyConstant.freeOfProfinite",
        "theorem nobelingAvailable",
        "Module.Free ℤ (LocallyConstant S ℤ)",
    ):
        assert snippet in blocker_lean, snippet

    p2d_lean = P2D_LEAN.read_text(encoding="utf-8")
    for snippet in ("measureFunctor", "dualityHomEquiv", "measurePresheafObj"):
        assert snippet in p2d_lean, snippet

    e3_lean = P2E_E3_LEAN.read_text(encoding="utf-8")
    for snippet in (
        "Condensed.profiniteSolidIsPointwiseRightKanExtension",
        "RightKanReconstruction.measureFunctorIsRightKanExtension",
        "FiniteDualTransport.finiteComparisonNatIso.hom",
        "rightKanExtensionUniqueOfIso",
        "rightKanExtensionUnique",
        "measureProfiniteSolidNatIsoOfIso",
        "measureProfiniteSolidNatIso",
    ):
        assert snippet in e3_lean, snippet

    for source in (blocker_lean, p2d_lean, e3_lean):
        assert not re.search(r"(?m)^\s*(sorry|axiom)(\s|$)", source)
        assert "unsafe " not in source.lower()
        assert "implemented_by" not in source.lower()
    for forbidden in ("LocallyConstant.freeOfProfinite", "Nobeling", "Nöbeling"):
        assert forbidden not in e3_lean

    report = REPORT.read_text(encoding="utf-8")
    for token in (
        "P2-D — `AVAILABLE`",
        "P2-E — `AVAILABLE`",
        "P2-F — `PARTIAL`, but `NON_BLOCKING_AUXILIARY`",
        "P2_CLOSURE_READY_PENDING_PROTECTED_ADMISSION",
        "must not be promoted to naturality",
        "does **not** certify CM4",
    ):
        assert token in report

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

    mut(("reconciliation", "baseline_main"), "0" * 40)
    mut(("reconciliation", "p2_d", "protected_merge"), "0" * 40)
    mut(("reconciliation", "p2_e", "protected_replay_run"), 1)
    mut(("reconciliation", "p2_f_classification"), "REQUIRED")
    mut(("stage_result", "p2_acceptance_reconciled"), False)
    mut(("stage_result", "p2_closure_candidate"), False)
    mut(("stage_result", "p2_f_blocks_closure"), True)
    mut(("claim_boundary", "p2_closed"), True)
    mut(("claim_boundary", "cm4_theorem_certified"), True)
    mut(("claim_boundary", "p3_closed"), True)
    mut(("claim_boundary", "graph_certified"), True)
    mut(("disposition",), "P2_CLOSED")

    for target_id in ("CM4-P2-D", "CM4-P2-E"):
        d = copy.deepcopy(base)
        for row in d["interface_matrix"]:
            if row["id"] == target_id:
                row["status"] = "BLOCKING"
        mutations.append(d)

    d = copy.deepcopy(base)
    for row in d["interface_matrix"]:
        if row["id"] == "CM4-P2-F":
            row["closure_role"] = "REQUIRED"
    mutations.append(d)

    d = copy.deepcopy(base)
    d["target"]["objectwise_product_role"] = "Chosen basis gives the required natural equivalence."
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
    print("CMDG-CONDENSED-CM4-P2-001 reconciliation / closure-candidate validation passed")
