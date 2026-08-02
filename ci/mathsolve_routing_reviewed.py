"""Current Programme-wide MATHSOLVE routing and MATHCERT disposition semantics."""
from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "governance" / "mathsolve_routing_audit.json"
SCHEMA_PATH = ROOT / "schemas" / "mathsolve_routing_registry.schema.json"
DOMAIN_REGISTRY_PATH = ROOT / "DOMAIN_REGISTRY.yaml"

EXPECTED_PROVIDER_COMMIT = "c9b9d0122017df7a117847d9ff1c2b9f6d6b75a1"
EXPECTED_PROVIDER_PULL_REQUEST = "https://github.com/grandchallenge/MATHSOLVE/pull/95"
EXPECTED_CERT_PROVIDER_COMMIT = "64e042ddb1147338ad7868a2847715fe7c1c079d"
EXPECTED_CERT_PROVIDER_PULL_REQUEST = "https://github.com/grandchallenge/MATHCERT/pull/79"
EXPECTED_CERT_REGISTRY_PATH = "governance/certification_routes.json"
EXPECTED_CERT_REGISTRY_BLOB = "cf876f43ae824f965a3aedf411671c110c380028"
EXPECTED_PREDECESSOR = {
    "path": "governance/mathcert_cross_repository_conformance.json",
    "audit_id": "MP-MC-CONFORMANCE-001",
    "status": "historical_superseded_for_current_portfolio_state",
}

EXPECTED_MANIFESTS = {
    "UC-001": ("campaign_manifests/UC-001.json", "4faf3e9e19e6c1a48461a8ad70cfb9c110daa101"),
    "NS-CI-001": ("campaign_manifests/NS-CI-001.json", "fcdd10f96b19c218ba700deb452b7da7f6b9b975"),
    "HC-001": ("campaign_manifests/HC-001.json", "48e3a0c22299147fe48cb4288cda813d7cffdcb4"),
    "BSD-001": ("campaign_manifests/BSD-001.json", "3fb3b07400915d90047a06a353537cf2e1593b9e"),
    "PNP-001": ("campaign_manifests/PNP-001.json", "6ecdfa0714828518878ccaf2cdc65756a5955186"),
    "RH-001": ("campaign_manifests/RH-001.json", "4ce2c5bcdc7bc1d0d63f7b2244898c8a651d5f64"),
    "YM-001": ("campaign_manifests/YM-001.json", "733d11811d0226fa2b2467965c3655a7d0fad963"),
    "OZ-001": ("campaign_manifests/OZ-001.json", "8b3164ab88a35ec9fba69013b44056573e846bfe"),
}
EXPECTED_HANDOFFS = {
    "UC-001": (25, "ready", "cert_handoffs/UC-001.json", "8369bc21e45be6af71d2a0cdb0c5ab3cb5313bfb"),
    "NS-CI-001": (19, "ready", "cert_handoffs/NS-CI-001.json", "40cad99646829fe40edf9c616074514407e49dee"),
    "HC-001": (23, "ready", "cert_handoffs/HC-001.json", "0c154af2e577e4367f9f5d0aeac5e15f9420172c"),
    "BSD-001": (26, "pending", "cert_handoffs/BSD-001.json", "20f8dbf016ab179cbf910d0510ad26b2bd9a24cb"),
    "PNP-001": (27, "pending", "cert_handoffs/PNP-001.json", "c9d419c43293d533de8858099d26672f1b8d9dbe"),
    "RH-001": (28, "pending", "cert_handoffs/RH-001.json", "7304f185bd817bb67b77540513dc01d05f6fcd3a"),
    "YM-001": (29, "pending", "cert_handoffs/YM-001.json", "54b7ad8156532e3dceba439356848dfa65a4d1ac"),
    "OZ-001": (30, "pending", "cert_handoffs/OZ-001.json", "b244c30b1b3aa4590a8b9ff9d63c5b66dab87663"),
}
EXPECTED_CERT_ROUTE_STATES = {
    "UC-001": "qualified",
    "NS-CI-001": "qualified",
    "HC-001": "ready",
    "BSD-001": "pending",
    "PNP-001": "pending",
    "RH-001": "qualified",
    "YM-001": "pending",
    "OZ-001": "pending",
}
EXPECTED_CERT_OUTPUTS = {
    "UC-001": {
        "repository": "grandchallenge/MATHCERT",
        "commit_sha": "214c4f4d7962883bb10172db84d5162dde2e5c4e",
        "path": "certificates/union_closed/MC-UC-WP04-QUAL-001.json",
        "digest_algorithm": "git_blob_sha1",
        "digest": "265c185d6b2b2970dc675729efa3fc4860f29204",
    },
    "NS-CI-001": {
        "repository": "grandchallenge/MATHCERT",
        "commit_sha": "b1aa08001eb8537be8e204c3866aefd5f898252e",
        "path": "certificates/formal_sources/MC-FC-WP00-NS-CI-001.json",
        "digest_algorithm": "git_blob_sha1",
        "digest": "6047ad774957974a6c2aa86bae72b51841e774a4",
    },
    "RH-001": {
        "repository": "grandchallenge/MATHCERT",
        "commit_sha": "b1aa08001eb8537be8e204c3866aefd5f898252e",
        "path": "certificates/formal_sources/MC-FC-WP00-RH-001.json",
        "digest_algorithm": "git_blob_sha1",
        "digest": "3668bbf792d994a6d8919101417f2f3cad342cdc",
    },
}
EXPECTED_QUALIFICATION_SCOPES = {
    "UC-001": "qualified_restricted_claims_only",
    "NS-CI-001": "qualified_interface_only",
    "RH-001": "qualified_interface_only",
}
ALIASES = {"UC": "UC-001"}
GATED_STAGES = {
    "WP00", "WP01", "WP02", "RESTRICTED_TARGET", "MECHANISM",
    "SPECIFICATION", "REALIZATION", "CONFRONTATION",
    "JUDGMENT", "CLAIM_PROMOTION", "INTEGRATION",
}
INTAKE_CERT_STATES = {"pending", "ready", "submitted"}
ADJUDICATED_CERT_STATES = {"certified", "qualified", "rejected", "proof_debt"}
COMPLETE_CERT_STATES = ADJUDICATED_CERT_STATES
POSITIVE_CERT_STATES = {"certified", "qualified"}
REQUIRED_WAIVER_APPROVERS = {"Referee", "Steward", "Human Steward"}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical(campaign_id: str) -> str:
    return ALIASES.get(campaign_id, campaign_id)


def active_campaigns() -> set[str]:
    data = yaml.safe_load(DOMAIN_REGISTRY_PATH.read_text(encoding="utf-8"))
    active = {
        canonical(str(item["campaign_id"]))
        for item in data.get("domains", [])
        if isinstance(item, dict) and item.get("status") == "ACTIVE"
    }
    active.add("OZ-001")
    return active


def routing_portfolio() -> set[str]:
    return set(EXPECTED_MANIFESTS)


def waiver_errors(campaign_id: str, waiver: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    approvers = {str(item) for item in waiver.get("approved_by", [])}
    if not REQUIRED_WAIVER_APPROVERS.issubset(approvers):
        errors.append(
            f"MATHSOLVE routing: {campaign_id} waiver requires Referee, Steward, and Human Steward approval"
        )
    if not str(waiver.get("human_steward_authorization", "")).strip():
        errors.append(f"MATHSOLVE routing: {campaign_id} waiver lacks Human Steward authorization identity")
    review_on = str(waiver.get("review_on", ""))
    if review_on and review_on < date.today().isoformat():
        errors.append(f"MATHSOLVE routing: {campaign_id} waiver review date has passed: {review_on}")
    return errors


def _exact_mapping_errors(label: str, actual: Any, expected: dict[str, Any]) -> list[str]:
    if not isinstance(actual, dict):
        return [f"{label} is missing or malformed"]
    return [
        f"{label} {field} drift; expected {value}"
        for field, value in expected.items()
        if actual.get(field) != value
    ]


def routing_errors(
    registry: dict[str, Any] | None = None,
    *,
    active: set[str] | None = None,
) -> list[str]:
    instance = registry if registry is not None else load_json(REGISTRY_PATH)
    schema = load_json(SCHEMA_PATH)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = [
        f"governance/mathsolve_routing_audit.json: {error.json_path}: {error.message}"
        for error in sorted(validator.iter_errors(instance), key=lambda item: list(item.path))
    ]

    expected_top = {
        "provider_commit": EXPECTED_PROVIDER_COMMIT,
        "provider_pull_request": EXPECTED_PROVIDER_PULL_REQUEST,
        "certification_provider_commit": EXPECTED_CERT_PROVIDER_COMMIT,
        "certification_provider_pull_request": EXPECTED_CERT_PROVIDER_PULL_REQUEST,
        "certification_route_registry_path": EXPECTED_CERT_REGISTRY_PATH,
        "certification_route_registry_git_blob_sha1": EXPECTED_CERT_REGISTRY_BLOB,
    }
    for field, expected in expected_top.items():
        if instance.get(field) != expected:
            errors.append(
                f"MATHSOLVE routing: {field} drift; expected {expected}, found {instance.get(field)!r}"
            )
    if instance.get("predecessor") != EXPECTED_PREDECESSOR:
        errors.append("MATHSOLVE routing: historical predecessor or supersession status drift")

    entries = [entry for entry in instance.get("campaigns", []) if isinstance(entry, dict)]
    ids = [str(entry.get("campaign_id", "")) for entry in entries]
    for duplicate in sorted({item for item in ids if ids.count(item) > 1}):
        errors.append(f"MATHSOLVE routing: duplicate campaign_id {duplicate}")
    actual = set(ids)
    active_required = {canonical(item) for item in (active if active is not None else active_campaigns())}
    portfolio = routing_portfolio()
    for missing in sorted(active_required - actual):
        errors.append(f"MATHSOLVE routing: ACTIVE campaign is uncovered: {missing}")
    for missing in sorted(portfolio - actual):
        errors.append(f"MATHSOLVE routing: governed routing campaign is uncovered: {missing}")
    for unknown in sorted(actual - portfolio):
        errors.append(f"MATHSOLVE routing: unrecognized routing campaign: {unknown}")

    by_id = {str(entry.get("campaign_id")): entry for entry in entries}
    for campaign_id, (expected_path, expected_blob) in EXPECTED_MANIFESTS.items():
        entry = by_id.get(campaign_id)
        if entry is None or entry.get("disposition") != "route":
            continue
        if entry.get("manifest_path") != expected_path:
            errors.append(f"MATHSOLVE routing: {campaign_id} manifest path drift; expected {expected_path}")
        if entry.get("manifest_git_blob_sha1") != expected_blob:
            errors.append(f"MATHSOLVE routing: {campaign_id} manifest identity drift; expected {expected_blob}")

        issue_number, handoff_state, handoff_path, handoff_blob = EXPECTED_HANDOFFS[campaign_id]
        cert = entry.get("cert", {})
        expected_issue = f"https://github.com/grandchallenge/MATHCERT/issues/{issue_number}"
        if cert.get("route_issue") != expected_issue:
            errors.append(f"MATHSOLVE routing: {campaign_id} Cert route issue drift; expected {expected_issue}")
        if cert.get("route_state") != EXPECTED_CERT_ROUTE_STATES[campaign_id]:
            errors.append(
                f"MATHSOLVE routing: {campaign_id} Cert provider state drift; "
                f"expected {EXPECTED_CERT_ROUTE_STATES[campaign_id]}"
            )
        handoff = cert.get("handoff", {})
        expected_handoff = {
            "repository": "grandchallenge/MATHSOLVE",
            "handoff_id": f"MC-HANDOFF-{campaign_id}",
            "state": handoff_state,
            "path": handoff_path,
            "git_blob_sha1": handoff_blob,
        }
        for field, expected in expected_handoff.items():
            if handoff.get(field) != expected:
                errors.append(
                    f"MATHSOLVE routing: {campaign_id} handoff {field} drift; expected {expected}"
                )

        expected_output = EXPECTED_CERT_OUTPUTS.get(campaign_id)
        actual_output = cert.get("cert_output")
        scope = cert.get("qualification_scope")
        if expected_output is None:
            if actual_output is not None:
                errors.append(f"MATHSOLVE routing: {campaign_id} intake route may not carry a Cert output")
            if scope is not None:
                errors.append(f"MATHSOLVE routing: {campaign_id} intake route may not carry qualification scope")
        else:
            errors.extend(_exact_mapping_errors(
                f"MATHSOLVE routing: {campaign_id} Cert output", actual_output, expected_output
            ))
            expected_scope = EXPECTED_QUALIFICATION_SCOPES[campaign_id]
            if scope != expected_scope:
                errors.append(
                    f"MATHSOLVE routing: {campaign_id} qualification scope drift; expected {expected_scope}"
                )
            if not any("unproved" in str(item).lower() for item in entry.get("promotion", {}).get("blockers", [])):
                errors.append(
                    f"MATHSOLVE routing: {campaign_id} qualification lacks an explicit unproved-target blocker"
                )

    for entry in entries:
        campaign_id = str(entry.get("campaign_id", ""))
        if entry.get("disposition") == "waiver":
            waiver = entry.get("waiver")
            if isinstance(waiver, dict):
                errors.extend(waiver_errors(campaign_id, waiver))
            continue
        if entry.get("disposition") != "route":
            continue
        if entry.get("placement") == "programme_embedded" and entry.get("coverage_mode") != "retrospective":
            errors.append(f"MATHSOLVE routing: {campaign_id} Programme-embedded work must be retrospective")
        promotion = entry.get("promotion", {})
        route_state = entry.get("cert", {}).get("route_state")
        if promotion.get("state") == "allowed":
            if promotion.get("blockers"):
                errors.append(f"MATHSOLVE routing: {campaign_id} allowed promotion retains blockers")
            if route_state not in POSITIVE_CERT_STATES:
                errors.append(
                    f"MATHSOLVE routing: {campaign_id} allowed promotion lacks certified or qualified MATHCERT state"
                )
        if promotion.get("state") == "blocked" and not promotion.get("blockers"):
            errors.append(f"MATHSOLVE routing: {campaign_id} blocked promotion lacks blockers")
    return errors


def provider_gate_errors(
    campaign_id: str,
    stage: str,
    registry: dict[str, Any] | None = None,
) -> list[str]:
    if stage not in GATED_STAGES:
        return []
    instance = registry if registry is not None else load_json(REGISTRY_PATH)
    canonical_id = canonical(campaign_id)
    entry = next(
        (
            item for item in instance.get("campaigns", [])
            if isinstance(item, dict) and item.get("campaign_id") == canonical_id
        ),
        None,
    )
    if entry is None:
        return [f"{canonical_id} {stage}: no MATHSOLVE route or approved waiver"]
    if entry.get("disposition") == "waiver":
        waiver = entry.get("waiver")
        if not isinstance(waiver, dict):
            return [f"{canonical_id} {stage}: malformed MATHSOLVE waiver"]
        if waiver_errors(canonical_id, waiver):
            return [f"{canonical_id} {stage}: invalid MATHSOLVE waiver"]
        if stage not in set(waiver.get("stages", [])):
            return [f"{canonical_id} {stage}: MATHSOLVE waiver does not cover this stage"]
        return []

    required = (
        "manifest_path", "manifest_git_blob_sha1", "solve_work_package_ids",
        "forge", "cert", "promotion",
    )
    missing = [field for field in required if not entry.get(field)]
    if missing:
        return [f"{canonical_id} {stage}: incomplete MATHSOLVE route: {', '.join(missing)}"]
    if entry.get("placement") == "programme_embedded" and stage not in {"WP00", "JUDGMENT", "INTEGRATION"}:
        return [f"{canonical_id} {stage}: future Solve-owned work may not remain embedded in MATH-PROGRAMME"]

    cert = entry["cert"]
    if not cert.get("handoff"):
        return [f"{canonical_id} {stage}: no content-addressed MATHCERT handoff packet"]
    route_state = cert["route_state"]
    if stage in {"JUDGMENT", "INTEGRATION"} and route_state not in ADJUDICATED_CERT_STATES:
        return [f"{canonical_id} {stage}: MATHCERT route has no adjudicated disposition"]
    if stage == "CLAIM_PROMOTION":
        if entry["promotion"]["state"] != "allowed":
            return [f"{canonical_id} {stage}: campaign promotion remains blocked"]
        if route_state not in POSITIVE_CERT_STATES:
            return [f"{canonical_id} {stage}: claim promotion requires certified or qualified MATHCERT disposition"]
    return []


def main() -> int:
    errors = routing_errors()
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(
        "validated current Solve manifests and packets, exact Cert outputs, "
        "bounded qualifications, historical supersession, and promotion boundaries"
    )
    return 0
