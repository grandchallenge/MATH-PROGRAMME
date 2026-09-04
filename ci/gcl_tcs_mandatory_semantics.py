from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from jsonschema import Draft202012Validator, FormatChecker

from ci.gcl_tcs_normative_agreement import (
    DECL_SCHEMA,
    MATRIX,
    POLICY,
    RECORD_SCHEMA,
    _load_json,
    _load_yaml,
    load_matrix,
)

ROOT = Path(__file__).resolve().parents[1]
COVERAGE = Path("governance/gcl_tcs_mandatory_semantic_coverage.json")
CONTRACT_MANIFEST = Path("governance/contract_test_manifest.json")
NEW_TEST = "tests/test_gcl_tcs_mandatory_semantics.py"
EXCEPTION_TEST = "tests/test_gcl_tcs_exception_control.py"
EXPECTED_SOURCE_SHA256 = "ea750b9b80b53c7d6ed755978fa4bdf59413fad93cec1db81eb3238372ce61c9"

MATRIX_ROWS = {
    "N-4.7-02",
    "N-6.4-01",
    "N-6.5-01",
    "N-7.2-01",
    "N-7.2-02",
    "N-7.3-01",
    "N-7.4-01",
    "N-9.1-01",
    "N-10.1-01",
    "N-10.1-03",
    "N-10.2-01",
    "N-10.3-01",
    "N-10.4-01",
    "N-10.5-01",
    "N-10.6-01",
    "N-12.3-01",
    "N-12.4-01",
    "N-12.5-01",
    "N-12.5-02",
    "N-13.1-01",
    "N-13.1-02",
    "N-13.1-03",
    "N-17-01",
}

REUSED_EXCEPTION_ROWS = {"N-12.4-01", "N-12.5-01", "N-12.5-02"}


def _as_mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def validation_errors(instance: Any, schema: Mapping[str, Any]) -> list[str]:
    validator = Draft202012Validator(dict(schema), format_checker=FormatChecker())
    return [error.message for error in validator.iter_errors(instance)]


def schema_required_field_sets(
    declaration_schema: Mapping[str, Any], record_schema: Mapping[str, Any]
) -> dict[str, list[str]]:
    props = _as_mapping(declaration_schema.get("properties"))
    defs = _as_mapping(declaration_schema.get("$defs"))
    record_defs = _as_mapping(record_schema.get("$defs"))

    def required(block: Any) -> list[str]:
        vals = _as_mapping(block).get("required", [])
        return sorted(str(value) for value in vals) if isinstance(vals, list) else []

    def object_branch_required(def_name: str) -> list[str]:
        block = _as_mapping(defs.get(def_name))
        branches = block.get("oneOf", [])
        if not isinstance(branches, list):
            return []
        for branch in branches:
            if isinstance(branch, Mapping) and branch.get("type") == "object":
                return required(branch)
        return []

    result = {
        "declaration": required(declaration_schema),
        "declaration.standard": required(defs.get("standardIdentifier")),
        "declaration.primary_profile": required(defs.get("profile")),
        "declaration.dependency": required(defs.get("dependency")),
        "declaration.location_or_not_applicable": object_branch_required("locationOrNotApplicable"),
        "declaration.location_or_explicit_empty": object_branch_required("locationOrExplicitEmpty"),
        "declaration.review_reference": required(defs.get("reviewReference")),
        "declaration.exception_reference": required(defs.get("exceptionReference")),
        "declaration.conformance_dimensions": required(props.get("conformance_dimensions")),
        "declaration.licence_and_access": required(props.get("licence_and_access")),
        "declaration.generated_content": required(props.get("generated_content")),
    }
    for name in (
        "claimRecord",
        "evidenceRecord",
        "reviewRecord",
        "exceptionRecord",
        "gateRecord",
        "conformanceStatement",
        "releaseRecord",
    ):
        result[f"record.{name}"] = required(record_defs.get(name))
    return result


def declaration_semantic_errors(declaration: Mapping[str, Any]) -> list[str]:
    """Machine-checkable cross-field semantics already bound by matrix row N-7.2-02."""
    errors: list[str] = []
    dimensions = declaration.get("conformance_dimensions")
    if not isinstance(dimensions, Mapping) or "ASSURED" not in dimensions.values():
        return errors
    reviews = declaration.get("review_register")
    if not isinstance(reviews, list) or not reviews:
        return ["declaration: ASSURED_requires_linked_review"]
    source_revision = declaration.get("source_revision")
    if isinstance(source_revision, str) and source_revision:
        if not any(
            isinstance(review, Mapping) and review.get("reviewed_revision") == source_revision
            for review in reviews
        ):
            errors.append("declaration: ASSURED_review_revision_mismatch")
    return errors


def gate_review_semantic_errors(
    gate_record: Mapping[str, Any], review_record: Mapping[str, Any]
) -> list[str]:
    """Pair-level semantics for N-13.1-02 and N-13.1-03 without inventing authority."""
    errors: list[str] = []
    if gate_record.get("gate_id") != review_record.get("gate_id"):
        errors.append("gate_review: gate_id_mismatch")
    if gate_record.get("reviewed_revision") != review_record.get("reviewed_revision"):
        errors.append("gate_review: reviewed_revision_mismatch")
    gate_decision = gate_record.get("decision")
    review_decision = review_record.get("decision")
    if gate_decision == "NOT_APPLICABLE" and review_decision != "NOT_APPLICABLE":
        errors.append("gate_review: NOT_APPLICABLE_requires_reviewer_approval")
    return errors


def gate_satisfies_gate(gate_record: Mapping[str, Any], review_record: Mapping[str, Any]) -> bool:
    if gate_review_semantic_errors(gate_record, review_record):
        return False
    decision = gate_record.get("decision")
    if decision == "PASS":
        return review_record.get("decision") == "PASS"
    if decision == "NOT_APPLICABLE":
        return review_record.get("decision") == "NOT_APPLICABLE"
    return False


def coverage_contract_errors(
    coverage: Mapping[str, Any] | None = None,
    matrix: Mapping[str, Any] | None = None,
    declaration_schema: Mapping[str, Any] | None = None,
    record_schema: Mapping[str, Any] | None = None,
    policy: Mapping[str, Any] | None = None,
    contract_manifest: Mapping[str, Any] | None = None,
    root: Path = ROOT,
) -> list[str]:
    errors: list[str] = []
    coverage = coverage or _load_json(COVERAGE, root)
    matrix = matrix or load_matrix(root)
    declaration_schema = declaration_schema or _load_json(DECL_SCHEMA, root)
    record_schema = record_schema or _load_json(RECORD_SCHEMA, root)
    policy = policy or _load_yaml(POLICY, root)
    contract_manifest = contract_manifest or _load_json(CONTRACT_MANIFEST, root)

    standard = coverage.get("standard")
    if not isinstance(standard, Mapping) or (
        standard.get("id"), standard.get("version"), standard.get("status")
    ) != ("GCL-TCS-00", "0.1.0", "candidate"):
        errors.append("coverage: candidate_identity_drift")
    if coverage.get("authority_boundary") != "CANDIDATE_READINESS_ONLY__NO_V1_PROMOTION":
        errors.append("coverage: authority_boundary_drift")

    agreement = coverage.get("agreement_matrix")
    if not isinstance(agreement, Mapping):
        errors.append("coverage: agreement_matrix_missing")
    else:
        if agreement.get("path") != str(MATRIX):
            errors.append("coverage: agreement_matrix_path_drift")
        if agreement.get("assembled_normative_sha256") != EXPECTED_SOURCE_SHA256:
            errors.append("coverage: normative_source_digest_drift")
        rows = agreement.get("required_row_ids")
        if not isinstance(rows, list) or set(rows) != MATRIX_ROWS:
            errors.append("coverage: matrix_row_set_incomplete")

    matrix_rows = matrix.get("rows")
    by_id = {
        row.get("id"): row
        for row in matrix_rows
        if isinstance(matrix_rows, list) and isinstance(row, Mapping)
    } if isinstance(matrix_rows, list) else {}
    for row_id in sorted(MATRIX_ROWS):
        row = by_id.get(row_id)
        if not isinstance(row, Mapping):
            errors.append(f"coverage: matrix_row_missing:{row_id}")
        elif row.get("gap") != "CLOSED":
            errors.append(f"coverage: matrix_row_not_closed:{row_id}")

    actual_sets = schema_required_field_sets(declaration_schema, record_schema)
    recorded_sets = coverage.get("required_field_sets")
    if not isinstance(recorded_sets, Mapping):
        errors.append("coverage: required_field_sets_missing")
    else:
        if set(recorded_sets) != set(actual_sets):
            errors.append("coverage: required_field_set_names_drift")
        for name, fields in actual_sets.items():
            values = recorded_sets.get(name)
            if not isinstance(values, list) or sorted(values) != fields:
                errors.append(f"coverage: required_field_set_drift:{name}")

    mandatory = _as_mapping(policy.get("mandatory_metadata")).get("core")
    if not isinstance(mandatory, list) or set(mandatory) != set(actual_sets["declaration"]):
        errors.append("coverage: policy_declaration_required_fields_drift")

    record_contracts = _as_mapping(policy.get("record_contracts"))
    policy_to_schema = {
        "evidence": "record.evidenceRecord",
        "review": "record.reviewRecord",
        "exception": "record.exceptionRecord",
        "gate": "record.gateRecord",
        "conformance_statement": "record.conformanceStatement",
        "release": "record.releaseRecord",
    }
    for policy_name, schema_name in policy_to_schema.items():
        required_fields = _as_mapping(record_contracts.get(policy_name)).get("required_fields")
        if not isinstance(required_fields, list) or set(required_fields) != set(actual_sets[schema_name]):
            errors.append(f"coverage: policy_record_required_fields_drift:{policy_name}")
    claim_fields = _as_mapping(record_contracts.get("claim")).get("required_fields")
    if not isinstance(claim_fields, list):
        errors.append("coverage: policy_record_required_fields_drift:claim")
    else:
        expected_claim = set(actual_sets["record.claimRecord"]) | {"statement_or_immutable_pointer"}
        if set(claim_fields) != expected_claim:
            errors.append("coverage: policy_record_required_fields_drift:claim")

    semantic_cases = coverage.get("semantic_cases")
    if not isinstance(semantic_cases, list) or not semantic_cases:
        errors.append("coverage: semantic_cases_missing")
    else:
        covered_rows: set[str] = set()
        for case in semantic_cases:
            if not isinstance(case, Mapping):
                errors.append("coverage: malformed_semantic_case")
                continue
            case_rows = case.get("matrix_rows")
            test = case.get("test")
            if not isinstance(case_rows, list) or not all(isinstance(x, str) for x in case_rows):
                errors.append("coverage: malformed_semantic_case_rows")
            else:
                covered_rows.update(case_rows)
            if not isinstance(test, str) or not test:
                errors.append("coverage: semantic_case_without_test")
        if not (MATRIX_ROWS - REUSED_EXCEPTION_ROWS).issubset(covered_rows):
            errors.append("coverage: semantic_matrix_rows_without_direct_test")

    reused = coverage.get("reused_dedicated_controls")
    reused_rows: set[str] = set()
    if isinstance(reused, list):
        for item in reused:
            if isinstance(item, Mapping) and item.get("test") == EXCEPTION_TEST:
                rows = item.get("matrix_rows")
                if isinstance(rows, list):
                    reused_rows.update(str(x) for x in rows)
    if not REUSED_EXCEPTION_ROWS.issubset(reused_rows):
        errors.append("coverage: dedicated_exception_control_not_reused")

    tests = contract_manifest.get("tests")
    paths = {
        item.get("path") for item in tests if isinstance(tests, list) and isinstance(item, Mapping)
    } if isinstance(tests, list) else set()
    if NEW_TEST not in paths:
        errors.append("coverage: new_test_not_governed")
    if EXCEPTION_TEST not in paths:
        errors.append("coverage: exception_test_not_governed")

    if coverage.get("completeness_claim") != "MANDATORY_MACHINE_FIELD_AND_FIELD_SEMANTIC_COVERAGE_COMPLETE__CANDIDATE_READINESS_ONLY":
        errors.append("coverage: completeness_claim_drift")
    return sorted(set(errors))
