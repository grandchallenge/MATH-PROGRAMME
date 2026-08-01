#!/usr/bin/env python3
"""Validate the accelerated Core Clarity maintenance control."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONTROL = ROOT / "governance" / "administrative_maintenance_control.json"
DEFAULT_SCHEMA = ROOT / "schemas" / "administrative_maintenance_control.schema.json"
DECISION_PATH = ROOT / "governance" / "administrative_maintenance_council_decision.json"

EXPECTED_REPOSITORIES = {
    "math_programme": "grandchallenge/MATH-PROGRAMME",
    "mathforge": "grandchallenge/MATHFORGE",
    "mathsolve": "grandchallenge/MATHSOLVE",
    "mathcert": "grandchallenge/MATHCERT",
    "intellect": "grandchallenge/INTELLECT",
}

EXPECTED_DECISIONS = {
    "D1": "APPROVE_WITH_CORRECTION",
    "D2": "APPROVE_WITH_CORRECTION",
    "D3": "APPROVE_WITH_CORRECTION",
    "D4": "APPROVE",
    "D5": "APPROVE_WITH_CORRECTION",
    "D6": "APPROVE_WITH_CORRECTION",
    "D7": "APPROVE_WITH_CORRECTION",
    "D8": "APPROVE_WITH_CORRECTION",
}

EXPECTED_CADENCES = {
    "structural_sweep": "PT16H48M",
    "administrative_portfolio_review": "P3D",
    "deep_conformance_review": "P9D",
    "constitutional_review": "P36DT12H",
}

REQUIRED_CAPABILITIES = {
    "schema and contract validation",
    "unit tests",
    "adversarial mutation tests",
    "source or provider validation where applicable",
    "campaign admission and routing validation where applicable",
    "formal or certificate replay where applicable",
    "documentation build where applicable",
    "GCL conformance",
    "protected-branch and release-trust evidence",
}

REQUIRED_COVERAGE_FIELDS = {
    "repository",
    "capability",
    "workflow_name_or_nonapplicability_record",
    "trigger",
    "required_check_state",
    "evidence_location",
    "failure_evidence_location",
    "owner",
    "repair_route",
    "last_verified_identity",
}

PROHIBITED_EMERGENCY_ACTIONS = {
    "claim promotion",
    "campaign admission",
    "certification adjudication",
    "branch-protection weakening",
    "required evidence deletion",
}

COUNCIL_ONLY_WAIVERS = {
    "cross-repository waiver",
    "provenance waiver",
    "certification waiver",
    "required-check waiver",
}


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def schema_errors(control: dict[str, Any], schema: dict[str, Any]) -> list[str]:
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    return [
        f"schema: {'/'.join(str(part) for part in error.absolute_path) or '<root>'}: {error.message}"
        for error in sorted(validator.iter_errors(control), key=lambda item: list(item.absolute_path))
    ]


def semantic_errors(control: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    if control.get("control_id") != "MP-ADMIN-MAINT-001":
        errors.append("semantic: unexpected control_id")
    if control.get("status") != "APPROVED_ACCELERATED_PILOT":
        errors.append("semantic: control must record the approved accelerated pilot")
    if control.get("effective") is not True or control.get("activation") != "PROTECTED_MERGE_ONLY":
        errors.append("semantic: control must activate only through protected merge")

    decision_ref = control.get("decision_record", {})
    if decision_ref.get("id") != "MP-ADMIN-DECISION-001" or decision_ref.get("adr") != "ADR-0016":
        errors.append("semantic: binding decision record identity drift")
    if DECISION_PATH.is_file():
        decision = load_json(DECISION_PATH)
        if decision.get("decision_id") != decision_ref.get("id"):
            errors.append("semantic: control and Council decision identifiers disagree")
        if decision.get("acceleration", {}).get("factor") != 0.1:
            errors.append("semantic: Council decision must preserve the 0.1 acceleration factor")

    foundation = control.get("foundation", {})
    if foundation.get("seventh_pass_merge") != "3cb6bfb9f132a4cfef279d0d3bf2309d99d0d6f1":
        errors.append("semantic: foundation must pin the seventh-pass protected merge")
    if foundation.get("seventh_pass_record_blob") != "4f2f13117e7ada0dda2f9dcaeeaa963f5e084f13":
        errors.append("semantic: foundation must pin the seventh-pass closure record blob")

    acceleration = control.get("acceleration", {})
    if acceleration.get("factor") != 0.1:
        errors.append("semantic: maintenance acceleration factor must be exactly 0.1")
    if acceleration.get("pilot_duration") != "P9D":
        errors.append("semantic: accelerated pilot duration must be P9D")
    if acceleration.get("event_triggered_obligations_remain_immediate") is not True:
        errors.append("semantic: event-triggered obligations cannot be delayed by cadence")

    roles = control.get("repository_roles", {})
    actual_repositories = {
        key: value.get("repository")
        for key, value in roles.items()
        if isinstance(value, dict)
    }
    if actual_repositories != EXPECTED_REPOSITORIES:
        errors.append("semantic: repository role matrix must cover the exact five-repository umbrella")
    intellect_responsibilities = set(roles.get("intellect", {}).get("responsibilities", []))
    if "maintenance contract adoption and freshness enforcement" not in intellect_responsibilities:
        errors.append("semantic: INTELLECT must own maintenance adoption and freshness enforcement")

    invariants = control.get("core_clarity_invariants", {})
    false_invariants = sorted(key for key, value in invariants.items() if value is not True)
    if false_invariants:
        errors.append(f"semantic: Core Clarity invariants must all be true: {false_invariants}")

    loops = control.get("control_loops", {})
    event_loop = loops.get("event_triggered_synchronization", {})
    if event_loop.get("binding") is not True or event_loop.get("cadence") != "IMMEDIATE_ON_MATERIAL_CHANGE":
        errors.append("semantic: material synchronization must be binding and immediate")
    for loop_name, cadence in EXPECTED_CADENCES.items():
        loop = loops.get(loop_name, {})
        if loop.get("binding") is not True or loop.get("cadence") != cadence:
            errors.append(f"semantic: {loop_name} must use accelerated cadence {cadence}")

    decisions = control.get("council_decisions", {})
    if decisions != EXPECTED_DECISIONS:
        errors.append("semantic: Council decision set or dispositions drifted")

    workflow = control.get("workflow_coverage_requirements", {})
    if set(workflow.get("required_capabilities", [])) != REQUIRED_CAPABILITIES:
        errors.append("semantic: workflow capability set is incomplete or inflated")
    if set(workflow.get("required_fields_per_capability", [])) != REQUIRED_COVERAGE_FIELDS:
        errors.append("semantic: workflow coverage evidence fields are incomplete or inflated")
    if workflow.get("yaml_presence_alone_is_sufficient") is not False:
        errors.append("semantic: workflow-file presence alone cannot establish coverage")

    tracker = control.get("tracker_hygiene", {})
    if tracker.get("tracker_can_create_authority") is not False:
        errors.append("semantic: issue trackers cannot create protected authority")
    if tracker.get("refresh_target") != "PT7H12M" or tracker.get("refresh_target_binding") is not True:
        errors.append("semantic: tracker refresh target must be binding PT7H12M")
    if tracker.get("stale_tracker_overrides_protected_state") is not False:
        errors.append("semantic: stale tracker cannot override protected state")
    if tracker.get("contradictory_tracker_blocks_reconciliation_closure") is not True:
        errors.append("semantic: identified contradictory tracker must block reconciliation closure")

    classification = control.get("material_change_classification", {})
    nonmaterial = set(classification.get("nonmaterial_changes", []))
    if "repository head movement that leaves consumed artifact blobs unchanged" not in nonmaterial:
        errors.append("semantic: unchanged consumed blobs must remain a nonmaterial head movement")
    if classification.get("uncertain_classification_disposition") != "ESCALATE_AND_FAIL_CLOSED":
        errors.append("semantic: uncertain change classification must escalate and fail closed")

    waiver = control.get("waiver_policy", {})
    if waiver.get("binding") is not True or waiver.get("council_decision") != "D3":
        errors.append("semantic: waiver policy must be binding under D3")
    if waiver.get("steward_local_administrative_limit") != "P3D":
        errors.append("semantic: ordinary Steward waiver limit must be accelerated to P3D")
    if not COUNCIL_ONLY_WAIVERS.issubset(set(waiver.get("council_required_for", []))):
        errors.append("semantic: critical waiver classes must require Council authority")
    if waiver.get("claim_promotion_by_waiver_allowed") is not False:
        errors.append("semantic: waivers cannot authorize claim promotion")

    review = control.get("independent_review_policy", {})
    if review.get("binding") is not True or review.get("council_decision") != "D4":
        errors.append("semantic: independent-review policy must be binding under D4")

    emergency = control.get("emergency_override_policy", {})
    if emergency.get("binding") is not True or emergency.get("council_decision") != "D6":
        errors.append("semantic: emergency policy must be binding under D6")
    if emergency.get("maximum_duration") != "PT7H12M":
        errors.append("semantic: emergency duration must be accelerated to PT7H12M")
    if emergency.get("steward_review_deadline") != "PT2H24M":
        errors.append("semantic: emergency Steward review must be accelerated to PT2H24M")
    if emergency.get("council_and_referee_retrospective_deadline") != "PT16H48M":
        errors.append("semantic: emergency retrospective must be accelerated to PT16H48M")
    if set(emergency.get("prohibited_actions", [])) != PROHIBITED_EMERGENCY_ACTIONS:
        errors.append("semantic: emergency override prohibitions must remain exact")
    if emergency.get("automatic_expiry_required") is not True or emergency.get("fail_closed_reversion_required") is not True:
        errors.append("semantic: emergency override must expire and revert fail closed")

    circuit = control.get("maintenance_burden_circuit_breaker", {})
    if circuit.get("binding") is not True or circuit.get("council_decision") != "D7":
        errors.append("semantic: burden circuit breaker must be binding under D7")
    if circuit.get("campaign_level_fail_closed") is not True:
        errors.append("semantic: missing critical coverage must fail the affected campaign closed")
    trigger_text = " ".join(circuit.get("triggers", []))
    for required in ("PT16H48M", "two active campaigns", "twenty percent"):
        if required not in trigger_text:
            errors.append(f"semantic: circuit-breaker trigger missing {required}")

    communication = control.get("communication_profile", {})
    if communication.get("binding") is not True or communication.get("council_decision") != "D8":
        errors.append("semantic: communication profile policy must be binding under D8")
    if communication.get("gcl_tcs_00_binding") is not False:
        errors.append("semantic: GCL-TCS-00 cannot be binding before G8/G9 completion")
    if communication.get("canonical_mathematical_claim_ledger_remains_controlling") is not True:
        errors.append("semantic: canonical mathematical claim ledger must remain controlling")

    intellect = control.get("intellect_buy_in", {})
    if intellect.get("required") is not True:
        errors.append("semantic: INTELLECT buy-in is mandatory")
    if intellect.get("exact_protected_pin_required_after_programme_merge") is not True:
        errors.append("semantic: INTELLECT must exact-pin the protected Programme merge")
    if intellect.get("final_closure_allowed_without_intellect_protected_adoption") is not False:
        errors.append("semantic: final closure cannot precede protected INTELLECT adoption")

    gate = control.get("promotion_gate", {})
    prerequisites = (
        gate.get("council_decisions_resolved") is True
        and gate.get("human_steward_release_complete") is True
        and gate.get("non_author_referee_review_complete") is True
        and gate.get("intellect_phase_a_buy_in_complete") is True
    )
    if gate.get("may_merge_programme_control") is not prerequisites:
        errors.append("semantic: Programme merge gate must equal resolved Council, Steward, Referee, and INTELLECT Phase A prerequisites")
    if gate.get("final_cross_repository_closure_complete") is True and intellect.get("phase") != "PHASE_B_PROTECTED_ADOPTION_COMPLETE":
        errors.append("semantic: final closure requires protected INTELLECT Phase B adoption")

    claim_boundaries = control.get("claim_boundaries", {})
    authorized = sorted(key for key, value in claim_boundaries.items() if value is not False)
    if authorized:
        errors.append(f"semantic: administrative control cannot authorize claims: {authorized}")

    return errors


def validate(control_path: Path, schema_path: Path) -> list[str]:
    control = load_json(control_path)
    schema = load_json(schema_path)
    return schema_errors(control, schema) + semantic_errors(control)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--control", type=Path, default=DEFAULT_CONTROL)
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    args = parser.parse_args()

    errors = validate(args.control, args.schema)
    if errors:
        for error in errors:
            print(error)
        return 1

    print("administrative maintenance control: valid accelerated pilot")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
