"""Policy checks for the third-pass umbrella authority and tracker correction."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
AUDIT_PATH = ROOT / "governance" / "five_repository_conformance_third_pass.json"
SCHEMA_PATH = ROOT / "schemas" / "five_repository_conformance_third_pass.schema.json"
CAMPAIGN_PATH = ROOT / "governance" / "governed_campaign_registry.json"
PREDECESSOR_PATH = ROOT / "governance" / "five_repository_conformance_second_pass.json"

EXPECTED_BASE_HEADS = {
    "math_programme": "96bebd6d9125555c6279106633318d7e32e890fe",
    "mathforge": "0faee396ffa56c568ee0ae6a348bdb43ca80ac4d",
    "mathsolve": "916f3434abcce29098ba7508a3b457a461461193",
    "mathcert": "0258e4f0bca0d90fac05b62aeef108f16dccffdd",
    "intellect": "7ce82ee5ad5614459ee4bffa57d22dc39adacbc1",
}
EXPECTED_PROGRAMME_TRACKERS = {
    "UC-001": 1,
    "NS-CI-001": 55,
    "HC-001": 65,
    "BSD-001": 66,
    "PNP-001": 162,
    "RH-001": 163,
    "YM-001": 164,
    "OZ-001": 113,
}
EXPECTED_CERT_TRACKERS = {
    "UC-001": 25,
    "NS-CI-001": 19,
    "HC-001": 23,
    "BSD-001": 26,
    "PNP-001": 27,
    "RH-001": 28,
    "YM-001": 29,
    "OZ-001": 30,
}
EXPECTED_PREDECESSOR_CERT_TRACKERS = {
    "UC-001": 25,
    "NS-CI-001": 19,
    "HC-001": 23,
    "RH-001": 28,
    "OZ-001": 30,
}
EXPECTED_PORTFOLIO = {
    "qualified_interface_only": {"NS-CI-001", "RH-001"},
    "ready_intake": {"UC-001", "HC-001"},
    "pending": {"BSD-001", "PNP-001", "YM-001", "OZ-001"},
    "archived_outside_current_routing": {"PC-001"},
}
EXPECTED_CERT_ROUTE_REGISTRY = {
    "repository": "grandchallenge/MATHCERT",
    "commit_sha": "0258e4f0bca0d90fac05b62aeef108f16dccffdd",
    "path": "governance/certification_routes.json",
    "digest_algorithm": "git_blob_sha1",
    "digest": "5b3e8d48b9f6c5b03ed3dc439bf9e43876e017b1",
    "route_count": 8,
}
FORBIDDEN_PROGRAMME_TRACKERS = {86, 88, 89}
ACTIVE_CAMPAIGNS = set(EXPECTED_PROGRAMME_TRACKERS)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def validation_errors(
    audit: dict[str, Any] | None = None,
    campaigns: dict[str, Any] | None = None,
    predecessor: dict[str, Any] | None = None,
) -> list[str]:
    errors: list[str] = []
    if audit is None:
        audit = load_json(AUDIT_PATH)
        schema = load_json(SCHEMA_PATH)
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        errors.extend(
            f"governance/five_repository_conformance_third_pass.json: "
            f"{error.json_path}: {error.message}"
            for error in sorted(validator.iter_errors(audit), key=lambda item: list(item.path))
        )
    if campaigns is None:
        campaigns = load_json(CAMPAIGN_PATH)
    if predecessor is None:
        predecessor = load_json(PREDECESSOR_PATH)

    if audit.get("protected_base_heads") != EXPECTED_BASE_HEADS:
        errors.append("third-pass audit: protected-base head drift")

    predecessor_ref = audit.get("predecessor", {})
    if predecessor_ref.get("publication_commit") != EXPECTED_BASE_HEADS["math_programme"]:
        errors.append("third-pass audit: predecessor publication commit drift")
    if predecessor_ref.get("git_blob_sha1") != "f86c5101b738fc82f7a20ef5db7ebe600b79f147":
        errors.append("third-pass audit: predecessor blob drift")
    if predecessor_ref.get("interpretation") != "historical_incomplete_tracker_coverage_and_authority_semantics":
        errors.append("third-pass audit: predecessor interpretation drift")

    predecessor_cert = predecessor.get("canonical_trackers", {}).get("cert", {})
    if predecessor_cert != EXPECTED_PREDECESSOR_CERT_TRACKERS:
        errors.append("third-pass audit: predecessor Cert tracker snapshot drift")
    omitted = set(EXPECTED_CERT_TRACKERS) - set(predecessor_cert)
    if omitted != {"BSD-001", "PNP-001", "YM-001"}:
        errors.append("third-pass audit: predecessor omitted-route set drift")

    authority = audit.get("authority_model", {})
    if authority.get("state_authority") != "protected_branch_repository_records":
        errors.append("third-pass audit: protected repository authority is required")
    if authority.get("github_issue_role") != "mutable_navigational_mirror":
        errors.append("third-pass audit: GitHub issue role must remain navigational mirror")
    if authority.get("issue_mutation_can_change_lifecycle_state") is not False:
        errors.append("third-pass audit: issue mutation may not change lifecycle state")
    if authority.get("issue_mutation_can_change_cert_state") is not False:
        errors.append("third-pass audit: issue mutation may not change Cert state")
    if authority.get("protected_branch_review_required_for_state_change") is not True:
        errors.append("third-pass audit: protected-branch review must gate state changes")

    programme_trackers = audit.get("programme_tracker_mirrors", {})
    cert_trackers = audit.get("cert_tracker_mirrors", {})
    if programme_trackers != EXPECTED_PROGRAMME_TRACKERS:
        errors.append("third-pass audit: Programme tracker mirror drift")
    if cert_trackers != EXPECTED_CERT_TRACKERS:
        errors.append("third-pass audit: Cert tracker mirror drift")
    if FORBIDDEN_PROGRAMME_TRACKERS & set(programme_trackers.values()):
        errors.append("third-pass audit: pull request substituted for Programme tracker")
    if set(audit.get("forbidden_programme_tracker_substitutions", [])) != FORBIDDEN_PROGRAMME_TRACKERS:
        errors.append("third-pass audit: forbidden Programme tracker set drift")

    campaign_map = {
        str(item.get("campaign_id")): item
        for item in campaigns.get("campaigns", [])
        if isinstance(item, dict)
    }
    if set(campaign_map) != ACTIVE_CAMPAIGNS | {"PC-001"}:
        errors.append("third-pass audit: governed campaign registry coverage drift")
    for campaign_id, expected_issue in EXPECTED_PROGRAMME_TRACKERS.items():
        actual_issue = campaign_map.get(campaign_id, {}).get("programme_tracker_issue")
        if actual_issue != expected_issue:
            errors.append(
                f"third-pass audit: governed registry {campaign_id} tracker drift; "
                f"expected {expected_issue}, found {actual_issue}"
            )
    if campaign_map.get("PC-001", {}).get("programme_tracker_issue") is not None:
        errors.append("third-pass audit: archived PC-001 must not have an active tracker mirror")
    claim_boundary = str(campaigns.get("claim_boundary", ""))
    if "Protected-branch repository records are authoritative" not in claim_boundary:
        errors.append("third-pass audit: campaign registry repository-authority boundary missing")
    if "GitHub issues are mutable navigational mirrors" not in claim_boundary:
        errors.append("third-pass audit: campaign registry issue-mirror boundary missing")

    if audit.get("external_cert_route_registry") != EXPECTED_CERT_ROUTE_REGISTRY:
        errors.append("third-pass audit: external Cert route registry identity drift")

    coverage = audit.get("mirror_coverage", {})
    if coverage != {
        "programme_campaign_count": 8,
        "cert_route_count": 8,
        "total_mirror_count": 16,
        "complete": True,
    }:
        errors.append("third-pass audit: 8+8 mirror coverage drift")

    portfolio = audit.get("portfolio", {})
    for key, expected in EXPECTED_PORTFOLIO.items():
        if set(portfolio.get(key, [])) != expected:
            errors.append(f"third-pass audit: {key} portfolio drift")

    blockers = audit.get("preserved_blockers", {})
    if set(blockers) != ACTIVE_CAMPAIGNS:
        errors.append("third-pass audit: blocker coverage does not equal active portfolio")
    if any(not values for values in blockers.values()):
        errors.append("third-pass audit: empty blocker list")

    boundaries = audit.get("claim_boundaries", {})
    for field in (
        "mathematical_target_proved",
        "novelty_claim_authorized",
        "priority_claim_authorized",
        "release_trust_issues_reopened",
    ):
        if boundaries.get(field) is not False:
            errors.append(f"third-pass audit: prohibited boundary inflation in {field}")
    if boundaries.get("operational_release_complete_preserved") is not True:
        errors.append("third-pass audit: operational release closure not preserved")

    if audit.get("pre_correction_governance_mismatch_count") != 5:
        errors.append("third-pass audit: pre-correction mismatch count drift")
    if audit.get("reviewed_correction_unresolved_mismatch_count") != 0:
        errors.append("third-pass audit: unresolved mismatch count must be zero")

    publication = audit.get("publication_semantics", {})
    if publication.get("self_inclusive_head_claim") is not False:
        errors.append("third-pass audit: self-inclusive head claim is prohibited")
    if publication.get("artifact_can_pin_own_future_merge_commit") is not False:
        errors.append("third-pass audit: impossible self-hash claim is prohibited")
    if publication.get("external_post_merge_attestation_required") is not True:
        errors.append("third-pass audit: external publication attestation is required")
    if publication.get("attestation_issue") != 167:
        errors.append("third-pass audit: publication attestation issue drift")

    findings = audit.get("third_pass_findings", [])
    if {item.get("id") for item in findings} != {"TP-01", "TP-02", "TP-03", "TP-04", "TP-05"}:
        errors.append("third-pass audit: finding identifier coverage drift")
    if {item.get("disposition") for item in findings} != {"corrected"}:
        errors.append("third-pass audit: every finding must be corrected")
    return errors
