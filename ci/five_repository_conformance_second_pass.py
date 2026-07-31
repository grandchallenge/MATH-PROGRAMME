"""Policy checks for the second-pass five-repository conformance addendum."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
AUDIT_PATH = ROOT / "governance" / "five_repository_conformance_second_pass.json"
SCHEMA_PATH = ROOT / "schemas" / "five_repository_conformance_second_pass.schema.json"

EXPECTED_HEADS = {
    "math_programme": "1cb128768803fdebcc9d7a0c8299399e467b01a9",
    "mathforge": "0faee396ffa56c568ee0ae6a348bdb43ca80ac4d",
    "mathsolve": "916f3434abcce29098ba7508a3b457a461461193",
    "mathcert": "0258e4f0bca0d90fac05b62aeef108f16dccffdd",
    "intellect": "7ce82ee5ad5614459ee4bffa57d22dc39adacbc1",
}
EXPECTED_CAMPAIGN_TRACKERS = {
    "UC-001": 1,
    "NS-CI-001": 55,
    "HC-001": 65,
    "BSD-001": 66,
    "PNP-001": 162,
    "RH-001": 163,
    "YM-001": 164,
    "OZ-001": 113,
}
EXPECTED_PORTFOLIO = {
    "qualified_interface_only": {"NS-CI-001", "RH-001"},
    "ready_intake": {"UC-001", "HC-001"},
    "pending": {"BSD-001", "PNP-001", "YM-001", "OZ-001"},
    "archived_outside_current_routing": {"PC-001"},
}
FORBIDDEN_TRACKERS = {86, 88, 89}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def validation_errors(audit: dict[str, Any] | None = None) -> list[str]:
    errors: list[str] = []
    if audit is None:
        audit = load_json(AUDIT_PATH)
        schema = load_json(SCHEMA_PATH)
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        errors.extend(
            f"governance/five_repository_conformance_second_pass.json: "
            f"{error.json_path}: {error.message}"
            for error in sorted(validator.iter_errors(audit), key=lambda item: list(item.path))
        )

    if audit.get("subject_heads") != EXPECTED_HEADS:
        errors.append("second-pass audit: subject-head identity drift")

    predecessor = audit.get("predecessor", {})
    if predecessor.get("publication_commit") != EXPECTED_HEADS["math_programme"]:
        errors.append("second-pass audit: predecessor publication commit drift")
    if predecessor.get("interpretation") != "conformant_at_pinned_subject_heads_not_self_inclusive":
        errors.append("second-pass audit: predecessor self-inclusion semantics drift")

    publication = audit.get("publication_semantics", {})
    if publication.get("self_inclusive_head_claim") is not False:
        errors.append("second-pass audit: self-inclusive head claim is prohibited")
    if publication.get("artifact_can_pin_own_future_merge_commit") is not False:
        errors.append("second-pass audit: impossible self-hash claim is prohibited")
    if publication.get("external_post_merge_attestation_required") is not True:
        errors.append("second-pass audit: external publication attestation is required")
    if publication.get("attestation_issue") != 165:
        errors.append("second-pass audit: publication attestation issue drift")

    ci = audit.get("ci_semantics", {})
    if ci.get("evidence_kind") != "pull_request_head_and_merge_ref_against_protected_base":
        errors.append("second-pass audit: CI evidence kind drift")
    if ci.get("post_merge_push_replay_claimed") is not False:
        errors.append("second-pass audit: unperformed post-merge push replay claimed")

    programme_trackers = audit.get("canonical_trackers", {}).get("programme_campaigns", {})
    if programme_trackers != EXPECTED_CAMPAIGN_TRACKERS:
        errors.append("second-pass audit: canonical Programme campaign tracker set drift")
    if FORBIDDEN_TRACKERS & set(programme_trackers.values()):
        errors.append("second-pass audit: pull request substituted for canonical tracker")
    if set(audit.get("forbidden_tracker_substitutions", [])) != FORBIDDEN_TRACKERS:
        errors.append("second-pass audit: forbidden tracker substitution set drift")

    portfolio = audit.get("portfolio", {})
    for key, expected in EXPECTED_PORTFOLIO.items():
        if set(portfolio.get(key, [])) != expected:
            errors.append(f"second-pass audit: {key} portfolio drift")

    active = set().union(
        EXPECTED_PORTFOLIO["qualified_interface_only"],
        EXPECTED_PORTFOLIO["ready_intake"],
        EXPECTED_PORTFOLIO["pending"],
    )
    if set(audit.get("preserved_blockers", {})) != active:
        errors.append("second-pass audit: blocker coverage does not equal active portfolio")
    if any(not values for values in audit.get("preserved_blockers", {}).values()):
        errors.append("second-pass audit: empty mathematical blocker list")

    boundaries = audit.get("claim_boundaries", {})
    for field in (
        "mathematical_target_proved",
        "novelty_claim_authorized",
        "priority_claim_authorized",
        "release_trust_issues_reopened",
    ):
        if boundaries.get(field) is not False:
            errors.append(f"second-pass audit: prohibited boundary inflation in {field}")
    if boundaries.get("operational_release_complete_preserved") is not True:
        errors.append("second-pass audit: operational release closure not preserved")

    if audit.get("identity_mismatch_count_at_subject_heads") != 0:
        errors.append("second-pass audit: identity mismatch count must be zero")
    if audit.get("unresolved_governance_mismatch_count") != 0:
        errors.append("second-pass audit: governance mismatch count must be zero")

    findings = audit.get("second_pass_findings", [])
    if {item.get("disposition") for item in findings} != {"corrected"}:
        errors.append("second-pass audit: every recorded finding must be corrected")
    return errors
