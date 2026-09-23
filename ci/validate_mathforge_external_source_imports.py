#!/usr/bin/env python3
"""Validate the sole Programme authority for the MATHFORGE semantic catalog."""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

# The validator is the governed execution root for the two deterministic
# builders. Importing their build functions keeps replay tooling within the
# repository's reachability graph without regenerating admitted artifacts in CI.
try:
    from .build_external_semantic_catalog_index import build as build_public_catalog
    from .build_mathforge_external_source_imports import build as build_import_registry
except ImportError:  # Direct script execution from the repository root.
    from build_external_semantic_catalog_index import build as build_public_catalog
    from build_mathforge_external_source_imports import build as build_import_registry

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "governance" / "mathforge_external_source_imports.json"
SCHEMA_PATH = ROOT / "schemas" / "mathforge_external_source_import.schema.json"
PROJECTION_PATH = ROOT / "governance" / "math_core_semantic_catalog_projection.json"
PROJECTION_SCHEMA_PATH = ROOT / "schemas" / "math_core_semantic_catalog_projection.schema.json"
PUBLIC_INDEX_PATH = ROOT / "docs" / "assets" / "external-semantic-catalog-index.json"

# Replaced with the exact protected MATHFORGE readback before admission.
EXPECTED_PROVIDER_COMMIT = "638190868060e60e109197af602fda4fb80fd02b"
EXPECTED_ENTRY_COUNT = 17_288
EXPECTED_PROVIDERS = {
    "RM-AMPHORA-001": {
        "legacy_source_ids": ["RM-AMPHORA-001"],
        "snapshot_id": "RM-AMPHORA-001-F22D0F28",
        "upstream_revision": "f22d0f28b55e6e777acf82e722d97ae982dff02e",
        "visibility": "public_full_text",
        "inventory_count": 14_056,
    },
    "FC-GDM": {
        "legacy_source_ids": ["FC-GDM-001", "FC-GDM-002"],
        "snapshot_id": "FC-GDM-85F86371",
        "upstream_revision": "85f863718beeec7b58a3a1926ee92e3472bc2020",
        "visibility": "public_metadata_only",
        "inventory_count": 3_232,
    },
}
# path -> (git blob sha1, sha256); generated from the protected MATHFORGE commit.
EXPECTED_ARTIFACTS: dict[str, tuple[str, str]] = {
    "catalog/entries/formal-conjectures-00000.jsonl": ("bde080f555ac1c07a6047fbab0137cd48d3a5cc3", "33d1929f630431fe731cf0880cd01312cee3c7fa043ed5f1d4499fa28c0533fd"),
    "catalog/entries/formal-conjectures-00001.jsonl": ("49c3fc04c06cff45698dfd66b995020891aa3e4e", "b9284333f076b0b4b702f08d977c8e0bdede815599e22750e0c70c5ee214c54f"),
    "catalog/entries/researchmath-00000.jsonl": ("f6ebd104e8003d35e3fef24d9d90f3bb6d1fe101", "4bc4ead2a587703acb0d544f9d02d56e0bd3c469971912a6c09630a3b41a1add"),
    "catalog/entries/researchmath-00001.jsonl": ("08d72032414349d7417947fa69304a311f8c09d3", "ee498dd91851fff74f487c4c21c334e0c3da383cd50f600a7e3c2b2a709bd596"),
    "catalog/entries/researchmath-00002.jsonl": ("e5d6e595c1f0c1352a2bd90e4abb91bf6b1b76ed", "ba9932103bb442855587e09b1fcf570aea6fec54ea69c60d4e0fe746c19f2d03"),
    "catalog/entries/researchmath-00003.jsonl": ("5608a1120790523a0e2ff479b9150e0bfe34ccf8", "c63330c6e6567eaf48869b6a0935534d1b7c5dce08f2ab1b3859d0b41dadbbe9"),
    "catalog/entries/researchmath-00004.jsonl": ("13183203281b6ff85ae928abc901b96f02da2b41", "71912f6d19e3f0c07b99140c3a6ba6ced91c7c55f31e37539ea625140bf19e70"),
    "catalog/entries/researchmath-00005.jsonl": ("89c47dd64b6cb61d9a6a9be8158e9b003dde5c34", "eeb10ec8fb00f93c16d5f9556232e6bd5b20cec1ca7e810a62d225c7be85ce98"),
    "catalog/entries/researchmath-00006.jsonl": ("77318f1c9ebcdc1da29e048970e9dc7d31922f1d", "8926fbbb45f3e60da4a8ce706588dbf0e7b3ed188f0bf1f9f6c20ca3a79665ba"),
    "catalog/entries/researchmath-00007.jsonl": ("5818f689641fd417ee7d5918ae5a0bd3a9c96527", "8d347d23eb928af4f70a7e54754842ddab75fd9b8650e9cc27fe4d3acc542082"),
    "catalog/manifest.json": ("4eb09fa37451e7644c870525db64fa6cc73a609b", "9bd37b7f655dc652ab3b7174e3785ec97fb8ee230c97e1f3a8be77ec254f4dc2"),
    "catalog/providers/FC-GDM-85F86371-composition.json": ("bc0a92eeefc69e92a2e08c99f903b93f966257d8", "d63066c67be1aa341466da4fa85d6d1eb4530fe435d2f359e634eebb6982e4d1"),
    "catalog/providers/FC-GDM-85F86371.json": ("5e74d0ceec81d313e9c858ec5bd4014fa543314f", "faa43f174717ef0126114b9bbd61bb9fdc827ce7eb9f64e56c1e63c7b15608db"),
    "catalog/providers/RM-AMPHORA-001-F22D0F28-composition.json": ("7adc5cb304b5a82b6d9800e461cade887c142829", "10d555b41718107676039a2e42984229a613e420d134b1061af0bcc733d5aceb"),
    "catalog/providers/RM-AMPHORA-001-F22D0F28.json": ("42521ace8b5a951f969cbd024b5211dae39e4477", "f5ed514bad9ad0a6ad39baa2e2eabaa3232c95f94f5892da7b925c53e6c264dc"),
    "catalog/relations/relations.json": ("9bac7553de345d901e565f39d57bd78780864356", "0dbaf1a15a8f76d2bcb61db872d11e024adf7c3233ac930297f75cdbd8abab09"),
    "catalog/relations/researchmath-duplicate-candidates.json": ("f4b544f87097214771e402ed1c9a5a27f7e93761", "90e49dcc14acba378faf4d89f2ba6b1b50d75c8511cf9ba12988d01502ec91f8"),
    "governance/external_sources.json": ("01edc3108a6292c36a9e8820b5262631e7db7623", "22defed8f755c716ee756d127a8943c2c0f50531eaafa5d1385decb83b659daf"),
}
ALLOWED_TIERS = {"SOURCE_LOCKED", "NORMALIZED_REPLAYED", "SEMANTICALLY_REVIEWED", "CAMPAIGN_CONCORDANT"}
ALLOWED_PREDICATES = {"same_statement", "formalizes", "specializes", "generalizes", "implies", "related", "duplicate_candidate", "conflicts", "rejected_match"}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def schema_errors(instance: Any, schema_path: Path, label: str) -> list[str]:
    schema = load(schema_path)
    return [
        f"{label}: {error.json_path}: {error.message}"
        for error in sorted(
            Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(instance),
            key=lambda item: list(item.path),
        )
    ]


def artifact_map(instance: dict[str, Any]) -> tuple[dict[str, tuple[str, str]], list[str]]:
    artifacts: list[dict[str, Any]] = []
    foundry = instance.get("source_foundry", {})
    if isinstance(foundry.get("registry_artifact"), dict):
        artifacts.append(foundry["registry_artifact"])
    release = instance.get("catalog_release", {})
    if isinstance(release.get("manifest_artifact"), dict):
        artifacts.append(release["manifest_artifact"])
    artifacts.extend(item for item in release.get("relation_artifacts", []) if isinstance(item, dict))
    for provider in instance.get("providers", []):
        if not isinstance(provider, dict):
            continue
        artifacts.extend(item for item in (provider.get("manifest_artifact"), provider.get("composition_artifact")) if isinstance(item, dict))
        artifacts.extend(item for item in provider.get("catalog_shards", []) if isinstance(item, dict))
    paths = [str(item.get("path", "")) for item in artifacts]
    errors = [f"external catalog imports: duplicate artifact path {path}" for path in sorted({path for path in paths if paths.count(path) > 1})]
    return {
        str(item.get("path")): (str(item.get("git_blob_sha1")), str(item.get("sha256")))
        for item in artifacts
    }, errors


def projection_errors(instance: dict[str, Any], registry: dict[str, Any]) -> list[str]:
    errors = schema_errors(instance, PROJECTION_SCHEMA_PATH, "MATH-CORE projection")
    if instance.get("mathforge_commit") != EXPECTED_PROVIDER_COMMIT:
        errors.append("MATH-CORE projection: protected MATHFORGE commit drift")
    if instance.get("catalog_release_id") != registry.get("catalog_release", {}).get("catalog_release_id"):
        errors.append("MATH-CORE projection: catalog release drift")
    if instance.get("node_count") != EXPECTED_ENTRY_COUNT:
        errors.append("MATH-CORE projection: node count drift")
    ranges = instance.get("node_ranges", [])
    if sum(int(item.get("node_count", 0)) for item in ranges if isinstance(item, dict)) != EXPECTED_ENTRY_COUNT:
        errors.append("MATH-CORE projection: range accounting drift")
    expected_shards = {
        artifact["path"]: artifact["sha256"]
        for provider in registry.get("providers", []) if isinstance(provider, dict)
        for artifact in provider.get("catalog_shards", []) if isinstance(artifact, dict)
    }
    projected_shards = {
        item.get("artifact_path"): item.get("artifact_sha256")
        for item in ranges if isinstance(item, dict)
    }
    if projected_shards != expected_shards:
        errors.append("MATH-CORE projection: shard provenance drift")
    for edge in instance.get("typed_edges", []):
        if not isinstance(edge, dict):
            continue
        if edge.get("predicate") not in ALLOWED_PREDICATES:
            errors.append("MATH-CORE projection: untyped semantic edge")
        if edge.get("review_state") == "AUTOMATED_PROPOSAL" and edge.get("predicate") not in {"related", "duplicate_candidate"}:
            errors.append("MATH-CORE projection: automated edge exceeds proposal authority")
    return errors


def public_index_errors(instance: dict[str, Any], registry: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if instance.get("schema_version") != "2.0.0" or instance.get("mathforge_commit") != EXPECTED_PROVIDER_COMMIT:
        errors.append("public semantic catalog: identity drift")
    if instance.get("catalog_release_id") != registry.get("catalog_release", {}).get("catalog_release_id"):
        errors.append("public semantic catalog: release drift")
    entries = instance.get("entries", [])
    if not isinstance(entries, list) or instance.get("entry_count") != EXPECTED_ENTRY_COUNT or len(entries) != EXPECTED_ENTRY_COUNT:
        return errors + ["public semantic catalog: inventory count drift"]
    counts = Counter(str(entry.get("provider")) for entry in entries if isinstance(entry, dict))
    expected_counts = Counter({provider: values["inventory_count"] for provider, values in EXPECTED_PROVIDERS.items()})
    if counts != expected_counts:
        errors.append("public semantic catalog: provider accounting drift")
    ids = [entry.get("id") for entry in entries if isinstance(entry, dict)]
    if len(ids) != len(set(ids)):
        errors.append("public semantic catalog: duplicate catalog identifier")
    allowed_fields = {"id", "title", "provider", "msc", "status", "language", "assurance", "campaign", "visibility", "warning"}
    for entry in entries:
        if not isinstance(entry, dict):
            errors.append("public semantic catalog: malformed entry")
            continue
        if set(entry) != allowed_fields:
            errors.append(f"public semantic catalog: unexpected fields for {entry.get('id')}")
        if entry.get("assurance") not in ALLOWED_TIERS:
            errors.append(f"public semantic catalog: unknown assurance tier for {entry.get('id')}")
        if entry.get("provider") == "FC-GDM":
            if entry.get("visibility") != "metadata_only" or not str(entry.get("warning", "")).startswith("Metadata only"):
                errors.append(f"public semantic catalog: restricted DeepMind entry exposed for {entry.get('id')}")
            if any(token in str(entry.get("title", "")) for token in (":=", "∀ ", "∃ ", "→")):
                errors.append(f"public semantic catalog: probable Lean statement exposure for {entry.get('id')}")
        elif entry.get("provider") == "RM-AMPHORA-001" and entry.get("visibility") != "full_text":
            errors.append(f"public semantic catalog: ResearchMath visibility drift for {entry.get('id')}")
    return errors


def import_errors(
    registry: dict[str, Any] | None = None,
    *,
    projection: dict[str, Any] | None = None,
    public_index: dict[str, Any] | None = None,
) -> list[str]:
    instance = registry if registry is not None else load(REGISTRY_PATH)
    errors = schema_errors(instance, SCHEMA_PATH, "external catalog imports")
    foundry = instance.get("source_foundry", {})
    if foundry.get("commit") != EXPECTED_PROVIDER_COMMIT:
        errors.append("external catalog imports: protected MATHFORGE commit drift")
    release = instance.get("catalog_release", {})
    if release.get("catalog_release_id") != "GCL-CATALOG-TWO-PROVIDER-001" or release.get("entry_count") != EXPECTED_ENTRY_COUNT:
        errors.append("external catalog imports: catalog release identity or count drift")
    providers = instance.get("providers", [])
    by_id = {item.get("provider_id"): item for item in providers if isinstance(item, dict)}
    if set(by_id) != set(EXPECTED_PROVIDERS):
        errors.append("external catalog imports: provider set drift")
    for provider_id, expected in EXPECTED_PROVIDERS.items():
        item = by_id.get(provider_id, {})
        for field, value in expected.items():
            if item.get(field) != value:
                errors.append(f"external catalog imports: {provider_id} {field} drift")
        if item.get("programme_disposition") != "READ_ONLY_SEMANTIC_CATALOG":
            errors.append(f"external catalog imports: {provider_id} gained Programme authority")
    actual_artifacts, artifact_errors = artifact_map(instance)
    errors.extend(artifact_errors)
    if actual_artifacts != EXPECTED_ARTIFACTS:
        errors.append("external catalog imports: protected MATHFORGE artifact identities drift")
    if instance.get("legacy_registry") != {"path": "governance/mathforge_provider_imports.json", "disposition": "HISTORICAL_COMPATIBILITY_ONLY", "authority": False}:
        errors.append("external catalog imports: legacy registry authority drift")
    boundaries = instance.get("routing_boundaries", {})
    if any(boundaries.get(field) is not False for field in ("catalog_creates_result", "catalog_creates_claim", "catalog_creates_certificate")):
        errors.append("external catalog imports: forbidden authority inference")
    projection_instance = projection if projection is not None else load(PROJECTION_PATH)
    public_instance = public_index if public_index is not None else load(PUBLIC_INDEX_PATH)
    errors.extend(projection_errors(projection_instance, instance))
    errors.extend(public_index_errors(public_instance, instance))
    return errors


def main() -> int:
    errors = import_errors()
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("Programme semantic catalog import is pinned to protected MATHFORGE artifacts: 17,288 read-only entries, license-gated publication, typed projection, and no result, claim, or certificate authority")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
