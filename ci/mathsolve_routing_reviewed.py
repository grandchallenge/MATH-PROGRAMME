"""Reviewed Programme-wide MATHSOLVE routing and MATHCERT disposition semantics."""
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
EXPECTED_PROVIDER_COMMIT = "cdb34f47829942bd89a3f7f754b412527eaafb92"
EXPECTED_PROVIDER_PULL_REQUEST = "https://github.com/grandchallenge/MATHSOLVE/pull/74"
EXPECTED_CERT_PROVIDER_COMMIT = "3854dd1b4f6e162a7e74c3da1993f022ee691e5e"
EXPECTED_CERT_REGISTRY_PATH = "governance/certification_routes.json"
EXPECTED_CERT_REGISTRY_BLOB = "065f0531e4d763b389b207d4922d5a85b4335ee3"
EXPECTED_MANIFESTS = {
    "UC-001": ("campaign_manifests/UC-001.json", "17ed0c7278098061201f14f337e4f4a81f9a0ef4"),
    "NS-CI-001": ("campaign_manifests/NS-CI-001.json", "35f7cd6ccf0e27f199571189fcb34a3f8adc31d7"),
    "HC-001": ("campaign_manifests/HC-001.json", "b3efb4e44dd6ab70765e602b4837bc23355eac3d"),
    "BSD-001": ("campaign_manifests/BSD-001.json", "ff634c6303d8ba322edb739c9112466adca1d3b1"),
    "PNP-001": ("campaign_manifests/PNP-001.json", "64c67206556c19ae77c1eb5afa8297aae9af224e"),
    "RH-001": ("campaign_manifests/RH-001.json", "0b58fa0ed35907eddf89062069793987b3b03f2e"),
    "YM-001": ("campaign_manifests/YM-001.json", "d8825019a6e65aa6210887d217a6a903cf09bdba"),
    "OZ-001": ("campaign_manifests/OZ-001.json", "2cdeb2059af2e4cafe53e6c3cf88a9b27fa622b4"),
}
EXPECTED_HANDOFFS = {
    "UC-001": (25, "ready", "cert_handoffs/UC-001.json", "8369bc21e45be6af71d2a0cdb0c5ab3cb5313bfb"),
    "NS-CI-001": (19, "ready", "cert_handoffs/NS-CI-001.json", "58b10636bd614e91e6c35900b9f5fb68e7f88afb"),
    "HC-001": (23, "ready", "cert_handoffs/HC-001.json", "0c154af2e577e4367f9f5d0aeac5e15f9420172c"),
    "BSD-001": (26, "pending", "cert_handoffs/BSD-001.json", "20f8dbf016ab179cbf910d0510ad26b2bd9a24cb"),
    "PNP-001": (27, "pending", "cert_handoffs/PNP-001.json", "c9d419c43293d533de8858099d26672f1b8d9dbe"),
    "RH-001": (28, "pending", "cert_handoffs/RH-001.json", "525ca580e3b29ed7fcc690f2ce810a26a17a9df2"),
    "YM-001": (29, "pending", "cert_handoffs/YM-001.json", "54b7ad8156532e3dceba439356848dfa65a4d1ac"),
    "OZ-001": (30, "pending", "cert_handoffs/OZ-001.json", "b244c30b1b3aa4590a8b9ff9d63c5b66dab87663"),
}
EXPECTED_CERT_ROUTE_STATES = {campaign_id: "pending" for campaign_id in EXPECTED_MANIFESTS}
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
    return {
        canonical(str(item["campaign_id"]))
        for item in data.get("domains", [])
        if isinstance(item, dict) and item.get("status") == "ACTIVE"
    }


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
        "certification_route_registry_path": EXPECTED_CERT_REGISTRY_PATH,
        "certification_route_registry_git_blob_sha1": EXPECTED_CERT_REGISTRY_BLOB,
    }
    for field, expected in expected_top.items():
        if instance.get(field) != expected:
            errors.append(
                f"MATHSOLVE routing: {field} drift; expected {expected}, found {instance.get(field)!r}"
            )

    entries = [entry for entry in instance.get("campaigns", []) if isinstance(entry, dict)]
    ids = [str(entry.get("campaign_id", "")) for entry in entries]
    for duplicate in sorted({item for item in ids if ids.count(item) > 1}):
        errors.append(f"MATHSOLVE routing: duplicate campaign_id {duplicate}")
    actual = set(ids)
    active_required = {
        canonical(item) for item in (active if active is not None else active_campaigns())
    }
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
        expected_handoff_id = f"MC-HANDOFF-{campaign_id}"
        expected_handoff = {
            "repository": "grandchallenge/MATHSOLVE",
            "handoff_id": expected_handoff_id,
            "state": handoff_state,
            "path": handoff_path,
            "git_blob_sha1": handoff_blob,
        }
        for field, expected in expected_handoff.items():
            if handoff.get(field) != expected:
                errors.append(
                    f"MATHSOLVE routing: {campaign_id} handoff {field} drift; expected {expected}"
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
    if entry.get("placement") == "programme_embedded" and stage != "WP00":
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
        "validated Solve manifests and packets, exact MATHCERT provider identity, "
        "intake/adjudication separation, scoped waivers, and promotion semantics"
    )
    return 0
