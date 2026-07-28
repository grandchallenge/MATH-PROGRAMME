#!/usr/bin/env python3
"""Validate Programme-wide MATHSOLVE routing and fail-closed promotion gates."""
from __future__ import annotations
import json
import sys
from pathlib import Path
from typing import Any
import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "governance" / "mathsolve_routing_audit.json"
SCHEMA_PATH = ROOT / "schemas" / "mathsolve_routing_registry.schema.json"
DOMAIN_REGISTRY_PATH = ROOT / "DOMAIN_REGISTRY.yaml"
EXPECTED_PROVIDER_COMMIT = "ec84e40aff4d926c5962653fd313bfb4db1adb8a"
ALIASES = {"UC": "UC-001"}
GATED_STAGES = {"WP00", "WP01", "WP02", "RESTRICTED_TARGET", "MECHANISM", "CLAIM_PROMOTION", "INTEGRATION"}


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

    entries = [entry for entry in instance.get("campaigns", []) if isinstance(entry, dict)]
    ids = [str(entry.get("campaign_id", "")) for entry in entries]
    for duplicate in sorted({item for item in ids if ids.count(item) > 1}):
        errors.append(f"MATHSOLVE routing: duplicate campaign_id {duplicate}")

    actual = set(ids)
    required = {canonical(item) for item in (active if active is not None else active_campaigns())}
    for missing in sorted(required - actual):
        errors.append(f"MATHSOLVE routing: ACTIVE campaign is uncovered: {missing}")

    for entry in entries:
        campaign_id = str(entry.get("campaign_id", ""))
        if entry.get("disposition") != "route":
            continue
        if entry.get("placement") == "programme_embedded" and entry.get("coverage_mode") != "retrospective":
            errors.append(f"MATHSOLVE routing: {campaign_id} Programme-embedded work must be retrospective")
        promotion = entry.get("promotion", {})
        if promotion.get("state") == "allowed" and promotion.get("blockers"):
            errors.append(f"MATHSOLVE routing: {campaign_id} allowed promotion retains blockers")
        if promotion.get("state") == "blocked" and not promotion.get("blockers"):
            errors.append(f"MATHSOLVE routing: {campaign_id} blocked promotion lacks blockers")
    return errors


def provider_gate_errors(
    campaign_id: str,
    stage: str,
    registry: dict[str, Any] | None = None,
) -> list[str]:
    """Return blocking errors for a future Programme promotion decision."""
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
        return []

    required = ("manifest_path", "manifest_git_blob_sha1", "solve_work_package_ids", "forge", "cert", "promotion")
    missing = [field for field in required if not entry.get(field)]
    if missing:
        return [f"{canonical_id} {stage}: incomplete MATHSOLVE route: {', '.join(missing)}"]

    if entry.get("placement") == "programme_embedded" and stage not in {"WP00"}:
        return [f"{canonical_id} {stage}: future Solve-owned work may not remain embedded in MATH-PROGRAMME"]

    if stage in {"CLAIM_PROMOTION", "INTEGRATION"}:
        cert_state = entry["cert"]["state"]
        if cert_state not in {"ready", "submitted", "certified", "qualified", "rejected", "proof_debt"}:
            return [f"{canonical_id} {stage}: resulting claims have no complete MATHCERT handoff"]
    return []


def main() -> int:
    errors = routing_errors()
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("validated MATHSOLVE routing for all ACTIVE campaigns; future Programme-embedded promotion fails closed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
