#!/usr/bin/env python3
"""Validate the candidate GCL GitHub-native truth spine and review envelope."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = ROOT / "governance" / "gcl_truth_spine_registry.json"
DEFAULT_REGISTRY_SCHEMA = ROOT / "schemas" / "gcl_truth_spine_registry.schema.json"
DEFAULT_MATRIX = ROOT / "governance" / "cross_repository_authority_matrix.json"
DEFAULT_MATRIX_SCHEMA = ROOT / "schemas" / "cross_repository_authority_matrix.schema.json"
DEFAULT_DESIGNATION = ROOT / "governance" / "gcl_delegated_referee_office.json"
DEFAULT_DESIGNATION_SCHEMA = ROOT / "schemas" / "gcl_delegated_referee_office.schema.json"
DEFAULT_STEWARD_RELEASE = ROOT / "governance" / "gcl_truth_spine_steward_release.json"
DEFAULT_STEWARD_RELEASE_SCHEMA = ROOT / "schemas" / "gcl_truth_spine_steward_release.schema.json"
DEFAULT_REFEREE_REVIEW = ROOT / "governance" / "gcl_truth_spine_referee_review.json"
DEFAULT_REFEREE_REVIEW_SCHEMA = ROOT / "schemas" / "gcl_truth_spine_referee_review.schema.json"
DEFAULT_PROMOTION = ROOT / "governance" / "gcl_truth_spine_promotion_record.json"
DEFAULT_PROMOTION_SCHEMA = ROOT / "schemas" / "gcl_truth_spine_promotion_record.schema.json"

SUBJECT_COMMIT = "d2a78b0b25497da192f23045d35869cd483ea15c"
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
EXPECTED_SEMANTIC_ARTIFACTS = {
    "governance/gcl_truth_spine_registry.json": "c4b30773be2f3151b3e975131ab6510245a3810b",
    "governance/cross_repository_authority_matrix.json": "efb009bf11bd9f6f7b82cac210dc2035036e3f46",
    "schemas/gcl_truth_spine_registry.schema.json": "17bfdbee116f43cbc6eb27e2c4234e3f0789d961",
    "schemas/cross_repository_authority_matrix.schema.json": "7d654bd59499a6a7cb74e2075ff245a7fd7af812",
    "docs/governance/GCL_TRUTH_SPINE.md": "886b81fe1dff1874df21ab69cdc84e34887cd4e0",
    "docs/governance/GCL_TRUTH_SPINE_CONFORMANCE_2026_07_31.md": "d3d60514cb0ea8e30a9c198453a90eec4d5d59c9",
}


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


def all_false(value: dict[str, Any]) -> bool:
    return bool(value) and all(item is False for item in value.values())


def artifact_map(items: list[dict[str, Any]]) -> dict[str, str]:
    return {str(item.get("path")): str(item.get("blob")) for item in items}


def git_blob_sha(path: Path) -> str:
    payload = path.read_bytes()
    header = f"blob {len(payload)}\0".encode("utf-8")
    return hashlib.sha1(header + payload).hexdigest()


def registry_semantic_errors(registry: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if registry.get("effective") is not False:
        errors.append("registry: candidate cannot be effective before protected activation")
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
    if any(gate.get(key) is not False for key in (
        "non_author_referee_review_complete",
        "human_steward_release_complete",
        "may_promote_now",
    )):
        errors.append("registry: reviewed subject must remain immutable; successor promotion record owns gate completion")
    if not all_false(registry.get("claim_boundaries", {})):
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
    if not all_false(matrix.get("claim_boundaries", {})):
        errors.append("matrix: claim boundary inflated")
    return errors


def designation_semantic_errors(designation: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if designation.get("effective") is not False or designation.get("activation") != "PROTECTED_MERGE_ONLY":
        errors.append("designation: standing office cannot be effective before protected merge")
    if designation.get("term") != "UNTIL_REVOKED" or designation.get("expires_at") is not None:
        errors.append("designation: standing term drift")
    if any(value is not True for value in designation.get("operating_rules", {}).values()):
        errors.append("designation: Referee operating rule weakened")
    independence = designation.get("independence_model", {})
    if independence.get("institutional_independence") != "ROLE_SEPARATION":
        errors.append("designation: role-separation independence missing")
    if len(independence.get("automatic_disqualification", [])) < 4:
        errors.append("designation: disqualification controls incomplete")
    if not all_false(designation.get("claim_boundaries", {})):
        errors.append("designation: claim boundary inflated")
    return errors


def steward_semantic_errors(release: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if release.get("subject_commit") != SUBJECT_COMMIT:
        errors.append("steward: exact approved subject drift")
    if release.get("disposition") != "APPROVE_FOR_PROTECTED_MERGE":
        errors.append("steward: approval disposition missing")
    source = release.get("source", {})
    if source.get("delegated_effectuation") is not True or source.get("recorded_pr_comment_id") != 5149236892:
        errors.append("steward: delegated approval source not bound")
    authority = release.get("administrative_effectuation_authority", {})
    if authority.get("semantic_change_to_approved_subject_permitted") is not False:
        errors.append("steward: semantic change improperly delegated")
    if authority.get("renewed_human_approval_required_for_semantic_change") is not True:
        errors.append("steward: renewed approval control missing")
    evidence = release.get("evidence", {})
    if evidence != {
        "gcl_conformance_run": 30678750162,
        "gcl_conformance_conclusion": "success",
        "programme_policy_run": 30678750001,
        "programme_policy_conclusion": "success",
    }:
        errors.append("steward: approved-subject workflow evidence drift")
    artifacts = artifact_map(release.get("approved_subject_artifacts", []))
    for path, blob in EXPECTED_SEMANTIC_ARTIFACTS.items():
        if artifacts.get(path) != blob:
            errors.append(f"steward: approved semantic artifact drift: {path}")
    if not all_false(release.get("claim_boundaries", {})):
        errors.append("steward: claim boundary inflated")
    return errors


def referee_semantic_errors(review: dict[str, Any], designation: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if review.get("subject_commit") != SUBJECT_COMMIT:
        errors.append("referee: exact reviewed subject drift")
    if review.get("designation_id") != designation.get("designation_id"):
        errors.append("referee: designation identity mismatch")
    reviewer = review.get("reviewer", {})
    if reviewer.get("office_identity") != designation.get("office_identity"):
        errors.append("referee: office identity mismatch")
    disclosure = review.get("independence_disclosure", {})
    if disclosure.get("role_separation_used") is not True:
        errors.append("referee: role separation not disclosed")
    if disclosure.get("model_or_provider_separate_from_authoring_assistant") is not False:
        errors.append("referee: independence disclosure must remain accurate")
    if disclosure.get("reviewer_modified_reviewed_subject_after_assignment") is not False:
        errors.append("referee: reviewer modified reviewed subject")
    if disclosure.get("counts_as_required_referee_under_human_delegation") is not True:
        errors.append("referee: delegated jurisdiction missing")
    if review.get("semantic_change_to_reviewed_subject_authorized") is not False:
        errors.append("referee: semantic change improperly authorized")
    if review.get("disposition") != "APPROVE_WITH_ADMINISTRATIVE_CORRECTION":
        errors.append("referee: disposition drift")
    if review.get("blocking_findings_remaining") is not False:
        errors.append("referee: blocking finding remains")
    findings = review.get("findings", [])
    ids = [item.get("finding_id") for item in findings]
    if len(ids) != len(set(ids)):
        errors.append("referee: duplicate finding identifiers")
    if not any(item.get("finding_id") == "GCL-TS-RF-004" for item in findings):
        errors.append("referee: activation correction finding missing")
    artifacts = artifact_map(review.get("reviewed_subject_artifacts", []))
    for path, blob in EXPECTED_SEMANTIC_ARTIFACTS.items():
        if artifacts.get(path) != blob:
            errors.append(f"referee: reviewed semantic artifact drift: {path}")
    if not all_false(review.get("claim_boundaries", {})):
        errors.append("referee: claim boundary inflated")
    return errors


def promotion_semantic_errors(
    promotion: dict[str, Any],
    registry: dict[str, Any],
    designation: dict[str, Any],
    release: dict[str, Any],
    review: dict[str, Any],
    root: Path = ROOT,
) -> list[str]:
    errors: list[str] = []
    if promotion.get("registry_id") != registry.get("registry_id"):
        errors.append("promotion: registry identity mismatch")
    if promotion.get("subject_commit") != SUBJECT_COMMIT:
        errors.append("promotion: approved subject drift")
    if release.get("subject_commit") != promotion.get("subject_commit") or review.get("subject_commit") != promotion.get("subject_commit"):
        errors.append("promotion: Steward and Referee subjects disagree")
    if review.get("designation_id") != designation.get("designation_id"):
        errors.append("promotion: Referee designation mismatch")
    if promotion.get("effective_before_protected_merge") is not False:
        errors.append("promotion: premature effectiveness")
    activation = promotion.get("activation", {})
    if activation.get("issue_or_pr_comment_alone_can_activate") is not False:
        errors.append("promotion: mutable discussion granted activation authority")
    if activation.get("effective_on_condition") is not True or activation.get("post_merge_attestation_required") is not True:
        errors.append("promotion: protected activation contract incomplete")
    if any(value is not True for value in promotion.get("gate_disposition", {}).values()):
        errors.append("promotion: gate disposition incomplete")
    expected_refs = {
        "human_steward_release": "governance/gcl_truth_spine_steward_release.json",
        "referee_review": "governance/gcl_truth_spine_referee_review.json",
        "referee_designation": "governance/gcl_delegated_referee_office.json",
    }
    if promotion.get("approval_records") != expected_refs:
        errors.append("promotion: approval record references drift")
    preserved = artifact_map(promotion.get("preserved_semantic_artifacts", []))
    if preserved != EXPECTED_SEMANTIC_ARTIFACTS:
        errors.append("promotion: preserved semantic artifact set drift")
    for relative, expected_blob in EXPECTED_SEMANTIC_ARTIFACTS.items():
        path = root / relative
        if not path.is_file():
            errors.append(f"promotion: semantic artifact missing: {relative}")
        elif git_blob_sha(path) != expected_blob:
            errors.append(f"promotion: reviewed semantic artifact changed: {relative}")
    envelope = promotion.get("administrative_envelope", {})
    if envelope.get("must_preserve_semantic_artifact_blobs") is not True:
        errors.append("promotion: semantic artifact preservation weakened")
    if envelope.get("renewed_review_required_if_semantic_artifact_blob_changes") is not True:
        errors.append("promotion: renewed review trigger missing")
    if not all_false(promotion.get("claim_boundaries", {})):
        errors.append("promotion: claim boundary inflated")
    return errors


def review_envelope_errors(root: Path = ROOT) -> list[str]:
    documents = [
        (DEFAULT_DESIGNATION, DEFAULT_DESIGNATION_SCHEMA, "designation"),
        (DEFAULT_STEWARD_RELEASE, DEFAULT_STEWARD_RELEASE_SCHEMA, "steward"),
        (DEFAULT_REFEREE_REVIEW, DEFAULT_REFEREE_REVIEW_SCHEMA, "referee"),
        (DEFAULT_PROMOTION, DEFAULT_PROMOTION_SCHEMA, "promotion"),
    ]
    errors: list[str] = []
    loaded: dict[str, dict[str, Any]] = {}
    for path, schema_path, label in documents:
        if not path.is_file():
            errors.append(f"{label}: required record missing: {path.relative_to(root)}")
            continue
        instance = load_json(path)
        loaded[label] = instance
        errors.extend(schema_errors(instance, load_json(schema_path), label))
    if len(loaded) != len(documents):
        return errors

    designation = loaded["designation"]
    release = loaded["steward"]
    review = loaded["referee"]
    promotion = loaded["promotion"]
    registry = load_json(DEFAULT_REGISTRY)
    errors.extend(designation_semantic_errors(designation))
    errors.extend(steward_semantic_errors(release))
    errors.extend(referee_semantic_errors(review, designation))
    errors.extend(promotion_semantic_errors(promotion, registry, designation, release, review, root))
    return errors


def validate(registry_path: Path, registry_schema_path: Path, matrix_path: Path, matrix_schema_path: Path) -> list[str]:
    registry = load_json(registry_path)
    matrix = load_json(matrix_path)
    return (
        schema_errors(registry, load_json(registry_schema_path), "registry")
        + schema_errors(matrix, load_json(matrix_schema_path), "matrix")
        + registry_semantic_errors(registry)
        + matrix_semantic_errors(matrix, registry)
        + review_envelope_errors()
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
    print("GCL truth spine: valid candidate authority contract and approved review envelope")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
