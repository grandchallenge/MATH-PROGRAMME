#!/usr/bin/env python3
"""Validate the stable semantic content of the Chaidez pedagogy contract."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONTRACT = ROOT / "pedagogy" / "chaidez_protocol_contract.json"

EXPECTED = {
    "result_status_fields": [
        "result_status",
        "conditional_on",
        "strongest_supported_claim",
        "not_claimed",
        "computation_class",
        "certification_state",
        "first_executable_step",
    ],
    "exposition_sequence": [
        "PLAIN_OBJECT",
        "EXACT_OBSTRUCTION",
        "WORKING_MODEL",
        "RESTRICTED_CLAIM",
        "THEOREM_SPINE",
        "MATHEMATICAL_ACTION",
        "DEBT_AND_CLAIM_BOUNDARY",
        "FIRST_EXECUTABLE_STEP",
    ],
    "trust_quartet": [
        "WHAT_IS_PROVED",
        "WHAT_IS_CHECKED",
        "WHAT_REMAINS_OPEN",
        "WHAT_REQUIRES_EXTERNAL_VERIFICATION",
    ],
    "computation_classes": [
        "EXPLORATORY_EVIDENCE",
        "REGRESSION_AUDIT",
        "EXACT_FINITE_VERIFICATION",
        "CONTINUUM_PROOF",
    ],
    "proof_debt_categories": [
        "MISSING_LEMMA",
        "UNPROVED_BRIDGE",
        "EXTERNAL_SOURCE",
        "COMPUTATIONAL_REPLAY",
        "SEMANTIC_CORRESPONDENCE",
        "ANALYTIC_ESTIMATE",
        "FORMALIZATION_BLOCKER",
    ],
    "spine_node_fields": [
        "node_id",
        "role",
        "status",
        "dependencies",
        "discharge_criterion",
        "proof_debt_ids",
    ],
    "required_work_package_artifacts": [
        "RESULT_STATUS",
        "LAY_COMPANION",
        "OBJECT_AND_OBSTRUCTION",
        "STATUS_AUDIT",
        "CLAIM_LEDGER",
        "THEOREM_SPINE",
        "DEPENDENCY_DAG",
        "PROOFS_AND_COMPUTATIONS",
        "FAILURE_AND_NEGATIVE_RESULTS",
        "PROOF_DEBT_REGISTER",
        "CERT_HANDOFF",
        "NEXT_EXECUTABLE_STEP",
    ],
}

GATE_FIELDS = [
    "theorem_spine_audited",
    "dependencies_named",
    "proof_debt_register_current",
    "trust_quartet_complete",
    "first_executable_step_present",
    "next_package_names_spine_node",
]


def validate(path: Path) -> list[str]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"cannot load contract: {exc}"]

    errors: list[str] = []
    if data.get("schema_version") != "1.0.0":
        errors.append("schema_version must be 1.0.0")
    if data.get("protocol_id") != "CHAIDEZ-PEDAGOGY-001":
        errors.append("protocol_id must be CHAIDEZ-PEDAGOGY-001")
    if data.get("campaign_unit") != "SINGLE_THEOREM_SPINE":
        errors.append("campaign_unit must be SINGLE_THEOREM_SPINE")

    for field, expected in EXPECTED.items():
        if data.get(field) != expected:
            errors.append(f"{field} must match the canonical ordered list")

    gate = data.get("escalation_gate")
    if not isinstance(gate, dict):
        errors.append("escalation_gate must be an object")
    else:
        if set(gate) != set(GATE_FIELDS):
            errors.append("escalation_gate fields must match the canonical set")
        for field in GATE_FIELDS:
            if gate.get(field) is not True:
                errors.append(f"escalation_gate.{field} must be true")

    return errors


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_CONTRACT
    errors = validate(path)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"valid Chaidez pedagogy contract: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
