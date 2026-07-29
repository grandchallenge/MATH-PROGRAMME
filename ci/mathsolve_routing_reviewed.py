"""Reviewed Programme-wide MATHSOLVE routing and promotion semantics."""
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
EXPECTED_PROVIDER_COMMIT = "68bbe0ae63c454b0dc63bedd0bc9f5501f8d5c03"
EXPECTED_PROVIDER_PULL_REQUEST = "https://github.com/grandchallenge/MATHSOLVE/pull/72"
EXPECTED_MANIFESTS = {
    "UC-001": ("campaign_manifests/UC-001.json", "8124414182c2270af55f6aabb51ec150e6747591"),
    "NS-CI-001": ("campaign_manifests/NS-CI-001.json", "94cc70ca569ad6a116c1c4e8211ff4ec253267f5"),
    "HC-001": ("campaign_manifests/HC-001.json", "181149b6a7984a28ca1b03e7a1b1706a8bc74923"),
    "BSD-001": ("campaign_manifests/BSD-001.json", "a7f18f3af5e9706c4bc85f620eaa3aa8006f793d"),
    "PNP-001": ("campaign_manifests/PNP-001.json", "af2cc7c0f1fe2cb120ac07c98efac1fddcd831d6"),
    "RH-001": ("campaign_manifests/RH-001.json", "44c21c400dfaba49ccd817ce54ee04c1ec3b8201"),
    "YM-001": ("campaign_manifests/YM-001.json", "6239090b508b6a8fbcb6b758b7173f63415b70c2"),
    "OZ-001": ("campaign_manifests/OZ-001.json", "ca8007abc58f25f8934f99c9f18fdcb6bebb11c7"),
}
ALIASES = {"UC": "UC-001"}
GATED_STAGES = {
    "WP00", "WP01", "WP02", "RESTRICTED_TARGET", "MECHANISM",
    "SPECIFICATION", "REALIZATION", "CONFRONTATION",
    "JUDGMENT", "CLAIM_PROMOTION", "INTEGRATION",
}
COMPLETE_CERT_STATES = {
    "ready", "submitted", "certified", "qualified", "rejected", "proof_debt"
}
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
    """Return every campaign that currently requires a Solve route.

    The portfolio contains all active domains plus governed pre-admission
    campaigns such as OZ-001. The explicit manifest inventory is the authority
    for the latter; pre-admission is not silently reclassified as ACTIVE.
    """
    return set(EXPECTED_MANIFESTS)


def waiver_errors(campaign_id: str, waiver: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    approvers = {str(item) for item in waiver.get("approved_by", [])}
    if not REQUIRED_WAIVER_APPROVERS.issubset(approvers):
        errors.append(
            f"MATHSOLVE routing: {campaign_id} waiver requires Referee, Steward, and Human Steward approval"
        )
    if not str(waiver.get("human_steward_authorization", "")).strip():
        errors.append(
            f"MATHSOLVE routing: {campaign_id} waiver lacks Human Steward authorization identity"
        )
    review_on = str(waiver.get("review_on", ""))
    if review_on and review_on < date.today().isoformat():
        errors.append(
            f"MATHSOLVE routing: {campaign_id} waiver review date has passed: {review_on}"
        )
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
    if instance.get("provider_commit") != EXPECTED_PROVIDER_COMMIT:
        errors.append(
            "MATHSOLVE routing: provider commit drift; expected "
            f"{EXPECTED_PROVIDER_COMMIT}, found {instance.get('provider_commit')!r}"
        )
    if instance.get("provider_pull_request") != EXPECTED_PROVIDER_PULL_REQUEST:
        errors.append(
            "MATHSOLVE routing: provider pull-request drift; expected "
            f"{EXPECTED_PROVIDER_PULL_REQUEST}, found {instance.get('provider_pull_request')!r}"
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
            errors.append(
                f"MATHSOLVE routing: {campaign_id} manifest path drift; expected {expected_path}"
            )
        if entry.get("manifest_git_blob_sha1") != expected_blob:
            errors.append(
                f"MATHSOLVE routing: {campaign_id} manifest identity drift; expected {expected_blob}"
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
        if (
            entry.get("placement") == "programme_embedded"
            and entry.get("coverage_mode") != "retrospective"
        ):
            errors.append(
                f"MATHSOLVE routing: {campaign_id} Programme-embedded work must be retrospective"
            )
        promotion = entry.get("promotion", {})
        cert_state = entry.get("cert", {}).get("state")
        if promotion.get("state") == "allowed":
            if promotion.get("blockers"):
                errors.append(
                    f"MATHSOLVE routing: {campaign_id} allowed promotion retains blockers"
                )
            if cert_state not in POSITIVE_CERT_STATES:
                errors.append(
                    f"MATHSOLVE routing: {campaign_id} allowed promotion lacks certified or qualified Cert state"
                )
        if promotion.get("state") == "blocked" and not promotion.get("blockers"):
            errors.append(
                f"MATHSOLVE routing: {campaign_id} blocked promotion lacks blockers"
            )
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
            item
            for item in instance.get("campaigns", [])
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
        return [
            f"{canonical_id} {stage}: incomplete MATHSOLVE route: {', '.join(missing)}"
        ]
    if entry.get("placement") == "programme_embedded" and stage != "WP00":
        return [
            f"{canonical_id} {stage}: future Solve-owned work may not remain embedded in MATH-PROGRAMME"
        ]

    cert_state = entry["cert"]["state"]
    if stage in {"JUDGMENT", "INTEGRATION"} and cert_state not in COMPLETE_CERT_STATES:
        return [
            f"{canonical_id} {stage}: resulting claims have no complete MATHCERT disposition"
        ]
    if stage == "CLAIM_PROMOTION":
        if entry["promotion"]["state"] != "allowed":
            return [f"{canonical_id} {stage}: campaign promotion remains blocked"]
        if cert_state not in POSITIVE_CERT_STATES:
            return [
                f"{canonical_id} {stage}: claim promotion requires certified or qualified MATHCERT disposition"
            ]
    return []


def main() -> int:
    errors = routing_errors()
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(
        "validated Solve routing portfolio, active-domain coverage, scoped waivers, Cert identities, and promotion semantics"
    )
    return 0
