"""Policy checks for final third-pass umbrella closure."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
CLOSURE_PATH = ROOT / "governance" / "five_repository_conformance_third_pass_closure.json"
SCHEMA_PATH = ROOT / "schemas" / "five_repository_conformance_third_pass_closure.schema.json"
STAGED_PATH = ROOT / "governance" / "five_repository_conformance_third_pass.json"
RUNTIME_PATH = ROOT / "governance" / "umbrella_runtime_contract.json"
CAMPAIGN_PATH = ROOT / "governance" / "governed_campaign_registry.json"
ROUTING_PATH = ROOT / "governance" / "mathsolve_routing_audit.json"

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
EXPECTED_PORTFOLIO = {
    "qualified_interface_only": {"NS-CI-001", "RH-001"},
    "ready_intake": {"UC-001", "HC-001"},
    "pending": {"BSD-001", "PNP-001", "YM-001", "OZ-001"},
    "archived_outside_current_routing": {"PC-001"},
}
EXPECTED_BLOCKERS = set(EXPECTED_PROGRAMME_TRACKERS)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def validation_errors(
    closure: dict[str, Any] | None = None,
    staged: dict[str, Any] | None = None,
    runtime: dict[str, Any] | None = None,
    campaigns: dict[str, Any] | None = None,
    routing: dict[str, Any] | None = None,
) -> list[str]:
    errors: list[str] = []
    if closure is None:
        closure = load_json(CLOSURE_PATH)
        schema = load_json(SCHEMA_PATH)
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        errors.extend(
            f"third-pass closure: {error.json_path}: {error.message}"
            for error in sorted(validator.iter_errors(closure), key=lambda item: list(item.path))
        )
    if staged is None:
        staged = load_json(STAGED_PATH)
    if runtime is None:
        runtime = load_json(RUNTIME_PATH)
    if campaigns is None:
        campaigns = load_json(CAMPAIGN_PATH)
    if routing is None:
        routing = load_json(ROUTING_PATH)

    programme = closure.get("programme_stage", {})
    expected_programme = {
        "repository": "grandchallenge/MATH-PROGRAMME",
        "merge_commit": "b620703ccc38e10382488dd87d743ea0af0461cf",
        "reviewed_head": "2ddc8639081d403b6e1a1b8236874dd6a9e940b8",
        "pull_request": 169,
        "policy_run_id": 30633465214,
        "gcl_run_id": 30633466116,
    }
    for key, value in expected_programme.items():
        if programme.get(key) != value:
            errors.append(f"third-pass closure: Programme {key} drift")

    expected_programme_artifacts = {
        "staged_audit": ("governance/five_repository_conformance_third_pass.json", "5ee5fcc74337acf6209c9166c84310d4709fe8d9"),
        "runtime_contract": ("governance/umbrella_runtime_contract.json", "6828f552cdd3aff006aed7f23477d2541af4b2e7"),
        "campaign_registry": ("governance/governed_campaign_registry.json", "b1f1e4682d0f3ff0108d020e466fa2ecb0809b57"),
        "routing_registry": ("governance/mathsolve_routing_audit.json", "4a27ec8aaaa60f919ba51028807b83dc522bfcff"),
    }
    for field, (path, digest) in expected_programme_artifacts.items():
        artifact = programme.get(field, {})
        if artifact != {"path": path, "digest_algorithm": "git_blob_sha1", "digest": digest}:
            errors.append(f"third-pass closure: Programme {field} identity drift")

    intellect = closure.get("intellect_stage", {})
    expected_intellect = {
        "repository": "grandchallenge/INTELLECT",
        "merge_commit": "712700f7f4de40fdd89342d718b1ea3bd3a02cc2",
        "reviewed_head": "fdd8d394f79c5ba2e0a1421998684b141def29f4",
        "pull_request": 16,
        "ci_run_id": 30634525842,
        "gcl_run_id": 30634526564,
    }
    for key, value in expected_intellect.items():
        if intellect.get(key) != value:
            errors.append(f"third-pass closure: INTELLECT {key} drift")
    expected_intellect_artifacts = {
        "provider_module": ("src/grand_intellect/mathsolve_cert_current.py", "2088fca1c622c52c0ea395a57c8221e3d41995c5"),
        "qualification_fixture": ("tests/fixtures/rh_ns_interface_qualifications.json", "e2f8d5ea88379e9f4f522cb7e42eb50071e7612e"),
    }
    for field, (path, digest) in expected_intellect_artifacts.items():
        artifact = intellect.get(field, {})
        if artifact != {"path": path, "digest_algorithm": "git_blob_sha1", "digest": digest}:
            errors.append(f"third-pass closure: INTELLECT {field} identity drift")

    if staged.get("status") != "PROGRAMME_CORRECTION_REVIEWED_INTELLECT_REPIN_REQUIRED":
        errors.append("third-pass closure: staged audit status drift")
    if staged.get("reviewed_correction_unresolved_mismatch_count") != 1:
        errors.append("third-pass closure: staged mismatch evidence drift")
    if runtime.get("contract_id") != "MP-UMBRELLA-RUNTIME-003":
        errors.append("third-pass closure: runtime contract identity drift")
    if runtime.get("consumer_independence") != {
        "pins_intellect_commit": False,
        "contains_downstream_completion_obligation": False,
        "consumer_repins_by_artifact_reference": True,
    }:
        errors.append("third-pass closure: runtime consumer-independence drift")

    campaign_map = {
        item["campaign_id"]: item.get("programme_tracker_issue")
        for item in campaigns.get("campaigns", [])
        if isinstance(item, dict) and item.get("campaign_id") in EXPECTED_PROGRAMME_TRACKERS
    }
    if campaign_map != EXPECTED_PROGRAMME_TRACKERS:
        errors.append("third-pass closure: governed campaign tracker map drift")
    if closure.get("programme_tracker_mirrors") != EXPECTED_PROGRAMME_TRACKERS:
        errors.append("third-pass closure: Programme tracker mirror drift")
    if closure.get("cert_tracker_mirrors") != EXPECTED_CERT_TRACKERS:
        errors.append("third-pass closure: Cert tracker mirror drift")

    route_states = {"qualified_interface_only": set(), "ready_intake": set(), "pending": set()}
    for item in routing.get("campaigns", []):
        campaign_id = item.get("campaign_id")
        state = item.get("cert", {}).get("route_state")
        if state == "qualified":
            route_states["qualified_interface_only"].add(campaign_id)
        elif state == "ready":
            route_states["ready_intake"].add(campaign_id)
        elif state == "pending":
            route_states["pending"].add(campaign_id)
    for key, expected in EXPECTED_PORTFOLIO.items():
        if set(closure.get("portfolio", {}).get(key, [])) != expected:
            errors.append(f"third-pass closure: {key} closure portfolio drift")
        if key != "archived_outside_current_routing" and route_states[key] != expected:
            errors.append(f"third-pass closure: {key} routing portfolio drift")

    if closure.get("third_pass_findings") != {f"TP-0{i}": "corrected" for i in range(1, 7)}:
        errors.append("third-pass closure: finding closure drift")
    blockers = closure.get("preserved_blockers", {})
    if set(blockers) != EXPECTED_BLOCKERS or any(not value for value in blockers.values()):
        errors.append("third-pass closure: mathematical blocker coverage drift")

    authority = closure.get("authority_model", {})
    if authority.get("state_authority") != "protected_branch_repository_records":
        errors.append("third-pass closure: protected repository authority missing")
    if authority.get("github_issue_role") != "mutable_navigational_mirror":
        errors.append("third-pass closure: issue mirror boundary missing")
    if authority.get("runtime_contract_is_consumer_independent") is not True:
        errors.append("third-pass closure: runtime consumer independence missing")

    boundaries = closure.get("claim_boundaries", {})
    for key in ("mathematical_target_proved", "novelty_claim_authorized", "priority_claim_authorized", "release_trust_issues_reopened"):
        if boundaries.get(key) is not False:
            errors.append(f"third-pass closure: prohibited boundary inflation in {key}")
    if boundaries.get("operational_release_complete_preserved") is not True:
        errors.append("third-pass closure: operational release closure not preserved")

    for key in ("identity_mismatch_count", "authority_mismatch_count", "tracker_coverage_mismatch_count"):
        if closure.get(key) != 0:
            errors.append(f"third-pass closure: {key} must be zero")
    if closure.get("remaining_cross_repository_obligations") != []:
        errors.append("third-pass closure: cross-repository obligation remains")

    publication = closure.get("publication_semantics", {})
    if publication != {
        "self_inclusive_head_claim": False,
        "artifact_can_pin_own_future_merge_commit": False,
        "external_post_merge_attestation_required": True,
        "attestation_issue": 167,
    }:
        errors.append("third-pass closure: publication semantics drift")
    return errors
