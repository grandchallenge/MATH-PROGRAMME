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
E1_LEAN = ROOT / "fixtures/formal/CMDG-NAT-CONCORDANCE-001/CMDGCondensedCM4P2EE1.lean"
E2_CORE = ROOT / "fixtures/formal/CMDG-NAT-CONCORDANCE-001/CMDGCondensedCM4P2EE2Core.lean"
E2_LEAN = ROOT / "fixtures/formal/CMDG-NAT-CONCORDANCE-001/CMDGCondensedCM4P2EE2.lean"
E3_LEAN = ROOT / "fixtures/formal/CMDG-NAT-CONCORDANCE-001/CMDGCondensedCM4P2EE3.lean"

EXPECTED_BASE = "839e04e1b862ffddfe5ce1d4d733ba954cd45d96"
EXPECTED_BASE_TREE = "ac1e21d2746ad951a9aa3c747895b28f56092bf8"
EXPECTED_E1_HEAD = "a7ab8c2fc26bc1c8e9d62f184d7779c8a48e14f8"
EXPECTED_E1_RUN = 31457490712
EXPECTED_E2_HEAD = "eefb8f3495018038047361c2cac2924a083f354a"
EXPECTED_E2_RUN = 31493933246
EXPECTED_E3_HEAD = "58e4aaf77e9965dbb2552376a7433ba4ccfc8657"
EXPECTED_E3_RUN = 31542402818
EXPECTED_DISPOSITION = "P2_E_NATURAL_EQUIVALENCE_ESTABLISHED_PENDING_PROTECTED_ADMISSION"
EXPECTED_SOURCES = {
    "Mathlib/Condensed/Solid.lean": "f5214433f91ee87fc8fbe7e2746e0bd227faed2a",
    "Mathlib/CategoryTheory/Functor/KanExtension/Basic.lean": "1d8ed3b224af14a8d909ada051de840ae3d5c59c",
    "Mathlib/CategoryTheory/Functor/KanExtension/Pointwise.lean": "eca4f781a97fc9948e726bb4b89a9ab1bc255f96",
    "Mathlib/Condensed/Discrete/Colimit.lean": "7579e7ecc282d20d4c61d4e5d0e3e37994069e11",
    "fixtures/formal/CMDG-NAT-CONCORDANCE-001/CMDGCondensedCM4P2D.lean": "7515583c1b56308bbd48c2c690addd3b432eba09",
}
FORBIDDEN_TRUE = {
    "p2_e_protected_available", "p2_closed", "cm4_theorem_certified",
    "p3_closed", "p4_closed", "p5_closed", "p6_closed",
    "derived_complex_form_certified", "arbitrary_ring_generalization_certified",
    "c04_broadened", "c06_discharged", "graph_certified",
    "dependency_minimality_claim", "dependency_uniqueness_claim",
    "cm5_authorized", "global_cmdg_completeness_claim",
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate(data=None):
    record = load(RECORD) if data is None else data
    jsonschema.validate(record, load(SCHEMA))

    assert record["operation_id"] == "CMDG-CONDENSED-CM4-P2-E-001"
    assert record["parent_operation_id"] == "CMDG-CONDENSED-CM4-P2-001"
    assert record["parent_issue"] == 363 and record["issue"] == 370
    assert record["implementation_pr"] == 376
    assert record["repository_baseline"] == EXPECTED_BASE
    assert record["repository_baseline_tree"] == EXPECTED_BASE_TREE

    scope = record["scope"]
    for token in ("P2-E only", "RECONSTRUCTION/EQUIVALENCE", "P2-D REPRESENTATION", "duality alone carries no reconstruction authority"):
        assert token in scope

    pred = record["protected_predecessor"]
    assert pred["reviewed_head"] == "358466932fde181c927cd428613f4578f38bfc1c"
    assert pred["protected_tree"] == EXPECTED_BASE_TREE
    assert pred["protected_merge"] == EXPECTED_BASE
    assert pred["protected_replay_run"] == 31342558880
    assert pred["programme_policy_run"] == 31342558852
    assert pred["gcl_conformance_run"] == 31342559115
    assert pred["state"] == "AVAILABLE"

    env = record["environment"]
    assert env["lean_commit"] == "62eed1db4d67327ec8120be05f1a1b0847d74561"
    assert env["mathlib_commit"] == "79d0395a1825a6264ad5d269e35e60537518955e"
    assert env["mathlib_tree"] == "d76f5e09b832a08949f6d8ad4fb80ce30527da64"
    assert env["coefficient_ring"] == "ULift.{u + 1} Z"

    audit = record["exact_tree_audit"]
    assert audit["result"] == "FORMAL_ROUTE_REACHABLE_WITH_TWO_CONSTRUCTION_OBLIGATIONS"
    sources = {row["path"]: row for row in audit["observed_sources"]}
    assert set(sources) == set(EXPECTED_SOURCES)
    for path, blob in EXPECTED_SOURCES.items():
        assert sources[path]["blob"] == blob
        assert sources[path]["evidence_class"] == "FORMAL_REACHABILITY"
        for key in ("declarations", "signature", "variance", "universe_behavior", "role"):
            assert sources[path][key]
    p2d_role = sources["fixtures/formal/CMDG-NAT-CONCORDANCE-001/CMDGCondensedCM4P2D.lean"]["role"]
    assert "P2-D REPRESENTATION" in p2d_role and "no reconstruction/equivalence authority" in p2d_role

    target = record["theorem_target"]
    assert target["finite_comparison"] == "FintypeCat.toProfinite ⋙ measureFunctor ≅ Condensed.finFree R"
    assert target["global_comparison"] == "measureFunctor ≅ Condensed.profiniteSolid R"
    assert target["basis_dependency"] is False and target["objectwise_only_allowed"] is False
    assert target["variance"] == "COVARIANT_PROFINITE_NATURAL_ISO"

    arch = record["proof_architecture"]
    assert arch["finite_level_comparison"]["state"] == "CERTIFIED"
    assert arch["measure_right_kan_extension"]["state"] == "CLOSED_MACHINE_CERTIFIED"
    assert arch["kan_extension_uniqueness"]["state"] == "CLOSED_MACHINE_CERTIFIED"

    e1 = arch["finite_level_comparison"]["requirement"]
    for token in ("E1 CERTIFIED", "finiteComparisonNatIso", EXPECTED_E1_HEAD, str(EXPECTED_E1_RUN), "comparison data, not an inference from duality alone"):
        assert token in e1

    e2 = arch["measure_right_kan_extension"]["requirement"]
    for token in (
        "E2 CLOSED_MACHINE_CERTIFIED", EXPECTED_E2_HEAD, str(EXPECTED_E2_RUN),
        "discreteContinuousPresheafIsColimit", "measurePresheafInternalHomNatIso",
        "finiteQuotientMeasureConeIso", "measureFunctorMapConeIsLimit",
        "measureFunctorStructuredArrowIsLimit", "measureRightExtensionIsPointwise",
        "measureFunctorIsRightKanExtension", "P2-D REPRESENTATION",
    ):
        assert token in e2

    e3 = arch["kan_extension_uniqueness"]["requirement"]
    for token in (
        "E3 CLOSED_MACHINE_CERTIFIED", EXPECTED_E3_HEAD, str(EXPECTED_E3_RUN),
        "Condensed.profiniteSolidIsPointwiseRightKanExtension",
        "IsPointwiseRightKanExtension.isRightKanExtension",
        "measureFunctorIsRightKanExtension", "finiteComparisonNatIso.hom",
        "rightKanExtensionUniqueOfIso", "rightKanExtensionUnique",
        "measureProfiniteSolidNatIsoOfIso", "measureProfiniteSolidNatIso",
        "measureFunctor ≅ Condensed.profiniteSolid R",
    ):
        assert token in e3

    assert all(record["adversarial_guards"].values())
    stage = record["stage_result"]
    assert stage["p2_d_protected_available"] is True
    assert stage["p2_e_theorem_target_frozen"] is True
    assert stage["p2_e_natural_equivalence_established"] is True
    assert stage["p2_e_protected_available"] is False
    assert stage["p2_closed"] is False
    assert stage["candidate_disposition"] == EXPECTED_DISPOSITION
    for key in FORBIDDEN_TRUE:
        assert record["claim_boundary"][key] is False
    assert record["disposition"] == EXPECTED_DISPOSITION

    stage_a = LEAN.read_text(encoding="utf-8")
    assert "abbrev FiniteComparisonTarget := finiteMeasure ≅ finiteFree" in stage_a
    assert "abbrev ComparisonTarget := measureFunctor ≅ solidFunctor" in stage_a
    e1_lean = E1_LEAN.read_text(encoding="utf-8")
    assert "noncomputable def finiteComparisonNatIso" in e1_lean
    e2_core = E2_CORE.read_text(encoding="utf-8")
    for token in ("discreteContinuousPresheafIsColimit", "measurePresheafInternalHomNatIso", "finiteQuotientMeasureConeIso", "measurePresheafFunctorMapConeIsLimit"):
        assert token in e2_core
    e2_lean = E2_LEAN.read_text(encoding="utf-8")
    for token in ("measureFunctorMapConeIsLimit", "measureFunctorStructuredArrowIsLimit", "measureRightExtensionIsPointwise", "measureFunctorIsRightKanExtension", "Profinite.Extend.isLimitCone", "isRightKanExtension"):
        assert token in e2_lean
    e3_lean = E3_LEAN.read_text(encoding="utf-8")
    for token in (
        "profiniteSolidRightExtensionIsPointwise",
        "Condensed.profiniteSolidIsPointwiseRightKanExtension",
        "profiniteSolidIsRightKanExtension",
        "RightKanReconstruction.measureFunctorIsRightKanExtension",
        "FiniteDualTransport.finiteComparisonNatIso.hom",
        "rightKanExtensionUniqueOfIso", "Iso.refl (Condensed.finFree R)",
        "rightKanExtensionUnique", "measureProfiniteSolidNatIsoOfIso",
        "measureProfiniteSolidNatIso",
    ):
        assert token in e3_lean
    for source in (stage_a, e1_lean, e2_core, e2_lean, e3_lean):
        assert not re.search(r"(?m)^\s*(sorry|axiom)(\s|$)", source)
        for forbidden in ("LocallyConstant.freeOfProfinite", "Nobeling", "Nöbeling"):
            assert forbidden not in source

    report = REPORT.read_text(encoding="utf-8")
    for token in (
        "Programme semantic boundary — representation versus reconstruction",
        "P2-D — `REPRESENTATION`", "P2-E — `RECONSTRUCTION/EQUIVALENCE`",
        "duality does not imply reconstruction", "FORMAL_ROUTE_REACHABLE_WITH_TWO_CONSTRUCTION_OBLIGATIONS",
        "E1 — canonical finite comparison", "E2 — measure functor as right Kan extension",
        "CLOSED_MACHINE_CERTIFIED", EXPECTED_E2_HEAD, str(EXPECTED_E2_RUN),
        "E3 — canonical uniqueness", EXPECTED_E3_HEAD, str(EXPECTED_E3_RUN),
        "measureProfiniteSolidNatIso", EXPECTED_DISPOSITION,
        "does **not** establish protected P2-E availability",
    ):
        assert token in report
    return record


def mutated(mutator):
    data = copy.deepcopy(load(RECORD))
    mutator(data)
    return data


def main() -> int:
    validate()
    print("CMDG-CONDENSED-CM4-P2-E-001 E1/E2/E3 certification record: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
