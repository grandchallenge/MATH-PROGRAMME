"""Current umbrella reconciliation and campaign-scope policy module."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
AUDIT_PATH = ROOT / "governance" / "umbrella_current_state_conformance.json"
AUDIT_SCHEMA_PATH = ROOT / "schemas" / "umbrella_current_state_conformance.schema.json"
CAMPAIGN_PATH = ROOT / "governance" / "governed_campaign_registry.json"
CAMPAIGN_SCHEMA_PATH = ROOT / "schemas" / "governed_campaign_registry.schema.json"
ROUTING_PATH = ROOT / "governance" / "mathsolve_routing_audit.json"
DOMAIN_PATH = ROOT / "DOMAIN_REGISTRY.yaml"

EXPECTED_ROUTING = {
    "qualified": {"NS-CI-001", "RH-001"},
    "ready": {"UC-001", "HC-001"},
    "pending": {"BSD-001", "PNP-001", "YM-001", "OZ-001"},
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
    "PC-001": None,
}
FORBIDDEN_TRACKER_SUBSTITUTIONS = {86, 88, 89}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _schema_errors(path: Path, schema_path: Path) -> list[str]:
    instance = load_json(path)
    schema = load_json(schema_path)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    return [
        f"{path.relative_to(ROOT)}: {error.json_path}: {error.message}"
        for error in sorted(validator.iter_errors(instance), key=lambda item: list(item.path))
    ]


def validation_errors(
    audit: dict[str, Any] | None = None,
    campaigns: dict[str, Any] | None = None,
    routing: dict[str, Any] | None = None,
) -> list[str]:
    errors: list[str] = []
    if audit is None:
        errors.extend(_schema_errors(AUDIT_PATH, AUDIT_SCHEMA_PATH))
        audit = load_json(AUDIT_PATH)
    if campaigns is None:
        errors.extend(_schema_errors(CAMPAIGN_PATH, CAMPAIGN_SCHEMA_PATH))
        campaigns = load_json(CAMPAIGN_PATH)
    if routing is None:
        routing = load_json(ROUTING_PATH)

    if audit.get("predecessor", {}).get("status") != "historical_superseded_for_current_portfolio_state":
        errors.append("umbrella audit: predecessor must be explicitly historical and superseded")
    boundaries = audit.get("claim_boundaries", {})
    if boundaries.get("mathematical_target_proved") is not False:
        errors.append("umbrella audit: reconciliation may not prove a mathematical target")
    if boundaries.get("operational_release_complete_preserved") is not True:
        errors.append("umbrella audit: operational release closure must remain preserved")
    if boundaries.get("release_trust_issues_reopened") is not False:
        errors.append("umbrella audit: release-trust issues may not be reopened")

    entries = {
        str(item.get("campaign_id")): item
        for item in routing.get("campaigns", [])
        if isinstance(item, dict)
    }
    actual = {"qualified": set(), "ready": set(), "pending": set()}
    for campaign_id, entry in entries.items():
        state = entry.get("cert", {}).get("route_state")
        if state == "qualified":
            actual["qualified"].add(campaign_id)
            if entry.get("cert", {}).get("qualification_scope") != "qualified_interface_only":
                errors.append(f"umbrella audit: {campaign_id} qualification is not interface-only")
            if entry.get("promotion", {}).get("state") != "blocked":
                errors.append(f"umbrella audit: {campaign_id} qualification may not enable promotion")
        elif state == "ready":
            actual["ready"].add(campaign_id)
        elif state == "pending":
            actual["pending"].add(campaign_id)
        else:
            errors.append(f"umbrella audit: unexpected current route state {campaign_id}:{state}")
    for state, expected in EXPECTED_ROUTING.items():
        if actual[state] != expected:
            errors.append(
                f"umbrella audit: {state} portfolio drift; expected {sorted(expected)}, found {sorted(actual[state])}"
            )

    campaign_entries = campaigns.get("campaigns", [])
    ids = [str(item.get("campaign_id")) for item in campaign_entries if isinstance(item, dict)]
    if len(ids) != len(set(ids)):
        errors.append("governed campaign registry: duplicate campaign identifier")
    if set(ids) != set(entries) | {"PC-001"}:
        errors.append("governed campaign registry: must equal routing portfolio plus archived PC-001")
    by_id = {str(item.get("campaign_id")): item for item in campaign_entries if isinstance(item, dict)}
    if by_id.get("OZ-001", {}).get("domain_id") is not None:
        errors.append("governed campaign registry: OZ-001 must remain an additional campaign outside principal domains")
    if by_id.get("PC-001", {}).get("routing_member") is not False:
        errors.append("governed campaign registry: archived PC-001 may not enter the current routing portfolio")
    if campaigns.get("legacy_aliases") != {"UC": "UC-001"}:
        errors.append("governed campaign registry: UC alias drift")

    actual_tracker_ids: list[int] = []
    for campaign_id, expected_issue in EXPECTED_PROGRAMME_TRACKERS.items():
        entry = by_id.get(campaign_id, {})
        actual_issue = entry.get("programme_tracker_issue")
        if actual_issue != expected_issue:
            errors.append(
                f"governed campaign registry: {campaign_id} tracker drift; "
                f"expected {expected_issue}, found {actual_issue}"
            )
        if isinstance(actual_issue, int):
            actual_tracker_ids.append(actual_issue)
    if len(actual_tracker_ids) != len(set(actual_tracker_ids)):
        errors.append("governed campaign registry: Programme tracker issues must be unique")
    if FORBIDDEN_TRACKER_SUBSTITUTIONS & set(actual_tracker_ids):
        errors.append("governed campaign registry: pull request substituted for campaign tracker")

    claim_boundary = str(campaigns.get("claim_boundary", ""))
    if "Protected-branch repository records are authoritative" not in claim_boundary:
        errors.append("governed campaign registry: repository authority boundary missing")
    if "GitHub issues are mutable navigational mirrors" not in claim_boundary:
        errors.append("governed campaign registry: issue mirror boundary missing")

    domains = yaml.safe_load(DOMAIN_PATH.read_text(encoding="utf-8"))
    domain_ids = {
        str(item.get("domain_id"))
        for item in domains.get("domains", [])
        if isinstance(item, dict)
    }
    registered_domain_ids = {
        str(item.get("domain_id"))
        for item in campaign_entries
        if isinstance(item, dict) and item.get("domain_id") is not None
    }
    if domain_ids != registered_domain_ids:
        errors.append("governed campaign registry: principal domain coverage drift")
    return errors


def main() -> int:
    errors = validation_errors()
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("validated current five-repository subject heads, portfolio states, exact campaign tracker mirrors, repository authority, historical supersession, and claim boundaries")
    return 0
