#!/usr/bin/env python3
"""Validate the candidate GCL GitHub-native truth spine."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = ROOT / "governance" / "gcl_truth_spine_registry.json"
DEFAULT_REGISTRY_SCHEMA = ROOT / "schemas" / "gcl_truth_spine_registry.schema.json"
DEFAULT_MATRIX = ROOT / "governance" / "cross_repository_authority_matrix.json"
DEFAULT_MATRIX_SCHEMA = ROOT / "schemas" / "cross_repository_authority_matrix.schema.json"

EXPECTED_RECORD_CLASSES = {
    "campaign_manifest", "provider_manifest", "solve_manifest", "cert_route",
    "handoff_packet", "claim_ledger", "review_record", "promotion_record",
    "waiver_record", "evidence_manifest", "negative_knowledge_record",
}
EXPECTED_REPOSITORIES = {
    "grandchallenge/MATH-PROGRAMME", "grandchallenge/MATHFORGE",
    "grandchallenge/MATHSOLVE", "grandchallenge/MATHCERT",
    "grandchallenge/INTELLECT",
}
EXPECTED_PRECEDENCE = [
    "protected_normative_record", "immutable_subject_bound_evidence",
    "review_and_decision_record", "generated_projection_or_report",
    "mutable_issue_or_discussion_mirror",
]


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def schema_errors(instance: dict[str, Any], schema: dict[str, Any], label: str) -> list[str]:
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    return [
        f"{label} schema: {'/'.join(map(str, error.absolute_path)) or '<root>'}: {error.message}"
        for error in sorted(validator.iter_errors(instance), key=lambda item: list(item.absolute_path))
    ]


def registry_semantic_errors(registry: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if registry.get("effective") is not False:
        errors.append("registry: candidate cannot be effective")
    precedence = registry.get("authority_precedence", [])
    if [item.get("rank") for item in precedence] != [1, 2, 3, 4, 5]:
        errors.append("registry: precedence ranks drift")
    if [item.get("authority_class") for item in precedence] != EXPECTED_PRECEDENCE:
        errors.append("registry: precedence order drift")
    if [item.get("authority_class") for item in precedence if item.get("may_define_current_state")] != ["protected_normative_record"]:
        errors.append("registry: only protected records may define current state")

    records = registry.get("record_classes", [])
    ids = [item.get("record_class_id") for item in records]
    if len(ids) != len(set(ids)) or set(ids) != EXPECTED_RECORD_CLASSES:
        errors.append("registry: canonical record class set drift")
    for item in records:
        rid = item.get("record_class_id", "<unknown>")
        if item.get("content_digest_required") is not True:
            errors.append(f"registry: {rid} lacks content identity")
        if item.get("issue_mirror_policy") not in {"navigation_only", "not_authoritative"}:
            errors.append(f"registry: {rid} grants issue authority")
        if not str(item.get("failure_disposition", "")).startswith("FAIL_CLOSED_"):
            errors.append(f"registry: {rid} does not fail closed")
        if not item.get("historical_rule") or not item.get("supersession_rule"):
            errors.append(f"registry: {rid} lacks history semantics")
        if "schema validation" not in set(item.get("required_ci", [])):
            errors.append(f"registry: {rid} lacks schema validation")

    if any(value is not True for value in registry.get("canonical_invariants", {}).values()):
        errors.append("registry: canonical invariant weakened")
    projection = registry.get("future_projection_boundary", {})
    if projection != {
        "aether_bridge_status": "ON_HOLD_PENDING_RESOURCE_AVAILABILITY",
        "aether_may_become_required_now": False,
        "aether_exclusive_institutional_facts_allowed": False,
        "records_should_support_future_optional_ingestion": True,
    }:
        errors.append("registry: AETHER boundary widened")
    gate = registry.get("promotion_gate", {})
    ready = gate.get("non_author_referee_review_complete") is True and gate.get("human_steward_release_complete") is True
    if gate.get("may_promote_now") is not ready:
        errors.append("registry: promotion gate inconsistent")
    if any(value is not False for value in registry.get("claim_boundaries", {}).values()):
        errors.append("registry: claim boundary inflated")
    return errors


def matrix_semantic_errors(matrix: dict[str, Any], registry: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if matrix.get("effective") is not False or matrix.get("registry_id") != registry.get("registry_id"):
        errors.append("matrix: candidate state or registry identity drift")
    entries = matrix.get("repositories", [])
    names = [item.get("repository") for item in entries]
    if len(names) != len(set(names)) or set(names) != EXPECTED_REPOSITORIES:
        errors.append("matrix: exact five-repository set required")
    valid = {item.get("record_class_id") for item in registry.get("record_classes", [])}
    for item in entries:
        referenced = set(item.get("produces_record_classes", [])) | set(item.get("consumes_record_classes", []))
        if referenced - valid:
            errors.append(f"matrix: {item.get('repository')} references unknown class")
        if not item.get("fallback") or not item.get("prohibited_authority"):
            errors.append(f"matrix: {item.get('repository')} lacks fallback or boundary")
    if any(value is not True for value in matrix.get("cross_repository_rules", {}).values()):
        errors.append("matrix: cross-repository rule weakened")
    external = matrix.get("external_systems", [])
    expected = {
        "system": "fyremael/AETHER",
        "current_role": "separate semantic-kernel and design-partner product programme",
        "institutional_authority": False,
        "required_for_gcl_operation": False,
        "bridge_status": "ON_HOLD_PENDING_RESOURCE_AVAILABILITY",
        "exclusive_institutional_facts_allowed": False,
    }
    if external != [expected]:
        errors.append("matrix: AETHER boundary widened")
    if any(value is not False for value in matrix.get("claim_boundaries", {}).values()):
        errors.append("matrix: claim boundary inflated")
    return errors


def validate(registry_path: Path, registry_schema_path: Path, matrix_path: Path, matrix_schema_path: Path) -> list[str]:
    registry = load_json(registry_path)
    matrix = load_json(matrix_path)
    return (
        schema_errors(registry, load_json(registry_schema_path), "registry")
        + schema_errors(matrix, load_json(matrix_schema_path), "matrix")
        + registry_semantic_errors(registry)
        + matrix_semantic_errors(matrix, registry)
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--registry-schema", type=Path, default=DEFAULT_REGISTRY_SCHEMA)
    parser.add_argument("--matrix", type=Path, default=DEFAULT_MATRIX)
    parser.add_argument("--matrix-schema", type=Path, default=DEFAULT_MATRIX_SCHEMA)
    args = parser.parse_args()
    errors = validate(args.registry, args.registry_schema, args.matrix, args.matrix_schema)
    if errors:
        print("\n".join(errors))
        return 1
    print("GCL truth spine: valid candidate authority contract")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
