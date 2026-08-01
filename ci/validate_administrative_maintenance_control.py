#!/usr/bin/env python3
"""Validate the candidate administrative maintenance control.

The JSON Schema checks shape and fixed invariants. These semantic checks preserve
cross-field policy boundaries that are awkward to express in schema alone.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONTROL = ROOT / "governance" / "administrative_maintenance_control.json"
DEFAULT_SCHEMA = ROOT / "schemas" / "administrative_maintenance_control.schema.json"

EXPECTED_REPOSITORIES = {
    "math_programme": "grandchallenge/MATH-PROGRAMME",
    "mathforge": "grandchallenge/MATHFORGE",
    "mathsolve": "grandchallenge/MATHSOLVE",
    "mathcert": "grandchallenge/MATHCERT",
    "intellect": "grandchallenge/INTELLECT",
}

EXPECTED_DECISIONS = {f"D{i}" for i in range(1, 9)}

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


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def schema_errors(control: dict[str, Any], schema: dict[str, Any]) -> list[str]:
    validator = Draft202012Validator(schema)
    return [
        f"schema: {'/'.join(str(part) for part in error.absolute_path) or '<root>'}: {error.message}"
        for error in sorted(validator.iter_errors(control), key=lambda item: list(item.absolute_path))
    ]


def semantic_errors(control: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    if control.get("control_id") != "MP-ADMIN-MAINT-001":
        errors.append("semantic: unexpected control_id")

    foundation = control.get("foundation", {})
    if foundation.get("seventh_pass_merge") != "3cb6bfb9f132a4cfef279d0d3bf2309d99d0d6f1":
        errors.append("semantic: foundation must pin the seventh-pass protected merge")
    if foundation.get("seventh_pass_record_blob") != "4f2f13117e7ada0dda2f9dcaeeaa963f5e084f13":
        errors.append("semantic: foundation must pin the seventh-pass closure record blob")

    roles = control.get("repository_roles", {})
    actual_repositories = {
        key: value.get("repository")
        for key, value in roles.items()
        if isinstance(value, dict)
    }
    if actual_repositories != EXPECTED_REPOSITORIES:
        errors.append("semantic: repository role matrix must cover the exact five-repository umbrella")

    invariants = control.get("core_clarity_invariants", {})
    false_invariants = sorted(key for key, value in invariants.items() if value is not True)
    if false_invariants:
        errors.append(f"semantic: Core Clarity invariants must all be true: {false_invariants}")

    loops = control.get("control_loops", {})
    event_loop = loops.get("event_triggered_synchronization", {})
    if event_loop.get("binding") is not True:
        errors.append("semantic: event-triggered material synchronization must remain binding")
    for loop_name in (
        "weekly_structural_sweep",
        "monthly_administrative_review",
        "quarterly_deep_conformance_review",
        "annual_constitutional_review",
    ):
        loop = loops.get(loop_name, {})
        if loop.get("binding") is not False or loop.get("council_decision") != "D1":
            errors.append(f"semantic: {loop_name} must remain provisional under Council decision D1")

    decisions = control.get("council_decisions", {})
    if set(decisions) != EXPECTED_DECISIONS:
        errors.append("semantic: Council decision set must be exactly D1-D8")

    if control.get("status") == "CANDIDATE_PENDING_COUNCIL_DECISION":
        if control.get("effective") is not False:
            errors.append("semantic: candidate control cannot be effective")
        unresolved = sorted(key for key, value in decisions.items() if value != "PENDING")
        if unresolved:
            errors.append(f"semantic: candidate Council decisions must remain PENDING: {unresolved}")
        gate = control.get("promotion_gate", {})
        if gate.get("council_decisions_resolved") is not False:
            errors.append("semantic: candidate cannot report Council decisions resolved")
        if gate.get("may_promote_now") is not False:
            errors.append("semantic: candidate cannot be promotable")

    workflow = control.get("workflow_coverage_requirements", {})
    capabilities = set(workflow.get("required_capabilities", []))
    if capabilities != REQUIRED_CAPABILITIES:
        errors.append("semantic: workflow capability set is incomplete or inflated")
    coverage_fields = set(workflow.get("required_fields_per_capability", []))
    if coverage_fields != REQUIRED_COVERAGE_FIELDS:
        errors.append("semantic: workflow coverage evidence fields are incomplete or inflated")
    if workflow.get("yaml_presence_alone_is_sufficient") is not False:
        errors.append("semantic: workflow-file presence alone cannot establish coverage")

    tracker = control.get("tracker_hygiene", {})
    if tracker.get("tracker_can_create_authority") is not False:
        errors.append("semantic: issue trackers cannot create protected authority")
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
    if waiver.get("binding") is not False or waiver.get("council_decision") != "D3":
        errors.append("semantic: waiver policy must remain nonbinding pending D3")
    if waiver.get("claim_promotion_by_waiver_allowed") is not False:
        errors.append("semantic: waivers cannot authorize claim promotion")

    review = control.get("independent_review_policy", {})
    if review.get("binding") is not False or review.get("council_decision") != "D4":
        errors.append("semantic: independent-review policy must remain nonbinding pending D4")

    emergency = control.get("emergency_override_policy", {})
    if emergency.get("binding") is not False or emergency.get("council_decision") != "D6":
        errors.append("semantic: emergency policy must remain nonbinding pending D6")
    emergency_prohibitions = set(emergency.get("prohibited_actions", []))
    if emergency_prohibitions != PROHIBITED_EMERGENCY_ACTIONS:
        errors.append("semantic: emergency override prohibitions must remain exact")
    if emergency.get("automatic_expiry_required") is not True:
        errors.append("semantic: emergency override must expire automatically")
    if emergency.get("fail_closed_reversion_required") is not True:
        errors.append("semantic: emergency override must revert fail closed")

    circuit = control.get("maintenance_burden_circuit_breaker", {})
    if circuit.get("binding") is not False or circuit.get("council_decision") != "D7":
        errors.append("semantic: burden circuit breaker must remain nonbinding pending D7")

    communication = control.get("communication_profile", {})
    if communication.get("council_decision") != "D8":
        errors.append("semantic: communication profile must be governed by D8")
    if communication.get("gcl_tcs_00_binding") is not False:
        errors.append("semantic: GCL-TCS-00 cannot be binding before G8/G9 completion")
    if communication.get("canonical_mathematical_claim_ledger_remains_controlling") is not True:
        errors.append("semantic: canonical mathematical claim ledger must remain controlling")

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

    print("administrative maintenance control: valid candidate")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
