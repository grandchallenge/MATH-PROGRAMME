#!/usr/bin/env python3
"""Validate pinned MATHFORGE provider imports and promotion coverage."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "governance" / "mathforge_provider_imports.json"
SCHEMA_PATH = ROOT / "schemas" / "mathforge_provider_import.schema.json"
DOMAIN_REGISTRY_PATH = ROOT / "DOMAIN_REGISTRY.yaml"

PROVIDER_REPOSITORY = "grandchallenge/MATHFORGE"
EXPECTED_PROVIDER_COMMIT = "2cb624cc61cd95ec0c8cfb8429d93128972289a5"
EXPECTED_IMPORTS: dict[str, tuple[str, str, str]] = {
    "UC-001": (
        "native",
        "provider_manifests/UC-001.json",
        "6d803633c2697f100d7d5b616ea1d6f16bff34bf",
    ),
    "NS-CI-001": (
        "native",
        "provider_manifests/NS-CI-001.json",
        "ed5220c31e38ba3458dc8a94a462c89c285fc22e",
    ),
    "HC-001": (
        "native",
        "provider_manifests/HC-001.json",
        "1bce7ab1e2cc7daa8f125747c69bad262adc080f",
    ),
    "BSD-001": (
        "retrospective",
        "provider_manifests/BSD-001.json",
        "c95e1f0ef8d2e662ca9bb3bb49317fa8aa7b2185",
    ),
    "PNP-001": (
        "retrospective",
        "provider_manifests/PNP-001.json",
        "dc7f740d91b5f69b22dd11af6737064d132d278a",
    ),
    "RH-001": (
        "retrospective",
        "provider_manifests/RH-001.json",
        "adcbee2583e5da2b59babefbafec943c113ba4ed",
    ),
    "YM-001": (
        "retrospective",
        "provider_manifests/YM-001.json",
        "c84694d5885f94da70b8124063d1b8ee55534470",
    ),
    "OZ-001": (
        "retrospective",
        "provider_manifests/OZ-001.json",
        "361da6642ff3ac7953b530ee0eb21659dc94fb65",
    ),
}

PROVIDER_GATED_STAGES = frozenset(
    {"WP00", "WP01", "PRIOR_ART", "RESTRICTED_TARGET"}
)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def active_domain_campaign_ids() -> set[str]:
    registry = yaml.safe_load(DOMAIN_REGISTRY_PATH.read_text(encoding="utf-8"))
    return {
        str(domain["campaign_id"])
        for domain in registry.get("domains", [])
        if isinstance(domain, dict) and domain.get("status") == "ACTIVE"
    }


def schema_errors(instance: Any) -> list[str]:
    schema = load_json(SCHEMA_PATH)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    return [
        f"governance/mathforge_provider_imports.json: {error.json_path}: {error.message}"
        for error in sorted(
            validator.iter_errors(instance), key=lambda item: list(item.path)
        )
    ]


def mathforge_provider_import_errors(
    registry: dict[str, Any] | None = None,
    *,
    active_campaigns: set[str] | None = None,
) -> list[str]:
    instance = registry if registry is not None else load_json(REGISTRY_PATH)
    errors = schema_errors(instance)

    if instance.get("provider_repository") != PROVIDER_REPOSITORY:
        errors.append("MATHFORGE imports: provider repository is not canonical")
    if instance.get("provider_commit") != EXPECTED_PROVIDER_COMMIT:
        errors.append(
            "MATHFORGE imports: provider commit drift; expected "
            f"{EXPECTED_PROVIDER_COMMIT}, found {instance.get('provider_commit')!r}"
        )

    campaigns = instance.get("campaigns", [])
    ids = [
        entry.get("campaign_id")
        for entry in campaigns
        if isinstance(entry, dict)
    ]
    duplicates = sorted(
        {campaign_id for campaign_id in ids if ids.count(campaign_id) > 1}
    )
    for duplicate in duplicates:
        errors.append(f"MATHFORGE imports: duplicate campaign_id {duplicate}")

    by_id = {
        str(entry.get("campaign_id")): entry
        for entry in campaigns
        if isinstance(entry, dict) and entry.get("campaign_id")
    }
    expected_ids = set(EXPECTED_IMPORTS)
    actual_ids = set(by_id)
    for missing in sorted(expected_ids - actual_ids):
        errors.append(f"MATHFORGE imports: registered campaign is uncovered: {missing}")
    for unknown in sorted(actual_ids - expected_ids):
        errors.append(
            f"MATHFORGE imports: unregistered provider authority: {unknown}"
        )

    domain_ids = (
        active_campaigns
        if active_campaigns is not None
        else active_domain_campaign_ids()
    )
    for missing in sorted(domain_ids - actual_ids):
        errors.append(
            f"MATHFORGE imports: ACTIVE domain campaign is uncovered: {missing}"
        )

    manifest_paths: list[str] = []
    for campaign_id, expected in EXPECTED_IMPORTS.items():
        entry = by_id.get(campaign_id)
        if not entry:
            continue
        if entry.get("disposition") != "import":
            waiver = entry.get("waiver")
            if not isinstance(waiver, dict):
                errors.append(
                    f"MATHFORGE imports: {campaign_id} has neither import nor valid waiver"
                )
            continue
        coverage_mode, path, blob_sha = expected
        if entry.get("coverage_mode") != coverage_mode:
            errors.append(
                f"MATHFORGE imports: {campaign_id} coverage mode drift; "
                f"expected {coverage_mode}, found {entry.get('coverage_mode')!r}"
            )
        if entry.get("manifest_path") != path:
            errors.append(
                f"MATHFORGE imports: {campaign_id} manifest path drift; "
                f"expected {path}, found {entry.get('manifest_path')!r}"
            )
        if entry.get("manifest_git_blob_sha1") != blob_sha:
            errors.append(
                f"MATHFORGE imports: {campaign_id} manifest identity drift; "
                f"expected {blob_sha}, "
                f"found {entry.get('manifest_git_blob_sha1')!r}"
            )
        manifest_paths.append(str(entry.get("manifest_path", "")))

    duplicate_paths = sorted(
        {path for path in manifest_paths if manifest_paths.count(path) > 1}
    )
    for duplicate in duplicate_paths:
        errors.append(f"MATHFORGE imports: duplicate manifest path {duplicate}")

    return errors


def provider_gate_errors(
    campaign_id: str,
    stage: str,
    registry: dict[str, Any] | None = None,
) -> list[str]:
    """Return blocking errors for a provider-gated promotion decision."""
    if stage not in PROVIDER_GATED_STAGES:
        return []
    instance = registry if registry is not None else load_json(REGISTRY_PATH)
    entry = next(
        (
            item
            for item in instance.get("campaigns", [])
            if isinstance(item, dict) and item.get("campaign_id") == campaign_id
        ),
        None,
    )
    if not entry:
        return [f"{campaign_id} {stage}: no MATHFORGE import or approved waiver"]
    if entry.get("disposition") == "import":
        required = (
            "coverage_mode",
            "manifest_path",
            "manifest_git_blob_sha1",
        )
        missing = [field for field in required if not entry.get(field)]
        if missing:
            return [
                f"{campaign_id} {stage}: incomplete MATHFORGE import fields: "
                f"{', '.join(missing)}"
            ]
        return []
    waiver = entry.get("waiver")
    if entry.get("disposition") == "waiver" and isinstance(waiver, dict):
        required = ("approved_by", "reason", "scope", "review_on")
        missing = [field for field in required if not waiver.get(field)]
        if missing:
            return [
                f"{campaign_id} {stage}: incomplete MATHFORGE waiver fields: "
                f"{', '.join(missing)}"
            ]
        return []
    return [f"{campaign_id} {stage}: invalid MATHFORGE provider disposition"]


def main() -> int:
    errors = mathforge_provider_import_errors()
    if errors:
        print("\n".join(errors), file=sys.stderr)
        print(
            f"MATHFORGE provider import validation failed with {len(errors)} error(s)",
            file=sys.stderr,
        )
        return 1
    print(
        "MATHFORGE provider imports are pinned: 8 campaigns, all ACTIVE domains, "
        "exact commit, manifest paths, content identities, and promotion coverage"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
