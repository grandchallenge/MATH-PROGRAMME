#!/usr/bin/env python3
"""Validate the Documentary Library across legacy and historical-micro edition classes.

The legacy validator remains authoritative for reference/full/orientation editions.
Source-locked historical micro-editions use a separate closed manifest-member schema
and their edition-local closed schema, so admitting a web-only historical reader does
not weaken the release, domain, or monograph contracts of the existing library.
"""

from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

import validate_documentaries as legacy

ROOT = Path(__file__).resolve().parents[1]
MICRO_TIER = "micro"
MICRO_SCHEMA = ROOT / "schemas/documentary_historical_micro.schema.json"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def schema_errors(instance: Any, schema: dict[str, Any], label: str) -> list[str]:
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    return [
        f"{label}{error.json_path}: {error.message}"
        for error in sorted(validator.iter_errors(instance), key=lambda item: list(item.path))
    ]


def _legacy_projection(manifest: dict[str, Any]) -> dict[str, Any]:
    projected = deepcopy(manifest)
    projected["volumes"] = [
        volume
        for volume in manifest.get("volumes", [])
        if volume.get("documentary_tier") != MICRO_TIER
    ]
    return projected


def _micro_volumes(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        volume
        for volume in manifest.get("volumes", [])
        if volume.get("documentary_tier") == MICRO_TIER
    ]


def _claim_authority_path(root: Path, value: str) -> Path:
    """Resolve the bounded historical-manifest spelling to a repository path."""
    parts = list(Path(value).parts)
    if parts and parts[0] == "..":
        parts = parts[1:]
    return root.joinpath(*parts)


def _micro_asset_paths(volume: dict[str, Any], root: Path) -> set[str]:
    edition_path = root / "docs/documentaries" / str(volume.get("edition_record", ""))
    if not edition_path.is_file():
        return set()
    edition = load_json(edition_path)
    return {
        str(plate.get("asset", ""))
        for plate in edition.get("plates", [])
        if plate.get("asset")
    }


def _micro_root_files(volume: dict[str, Any], root: Path) -> set[str]:
    names = {
        str(volume.get("web_page", "")),
        str(volume.get("edition_record", "")),
    }
    edition_path = root / "docs/documentaries" / str(volume.get("edition_record", ""))
    if edition_path.is_file():
        edition = load_json(edition_path)
        schema_name = str(edition.get("schema", ""))
        if schema_name:
            names.add(schema_name)
    return {name for name in names if name}


def _micro_semantic_errors(
    volume: dict[str, Any], schema: dict[str, Any], root: Path
) -> list[str]:
    slug = str(volume.get("slug", "<unknown>"))
    errors = schema_errors(
        volume,
        schema,
        f"docs/documentaries/ARTIFACT_MANIFEST.json:{slug}",
    )

    source_path = root / "docs/documentaries" / str(volume.get("source_record", ""))
    page_path = root / "docs/documentaries" / str(volume.get("web_page", ""))
    edition_path = root / "docs/documentaries" / str(volume.get("edition_record", ""))
    claim_path = _claim_authority_path(root, str(volume.get("claim_authority", "")))
    for label, path in (
        ("source reference", source_path),
        ("web page", page_path),
        ("edition record", edition_path),
        ("claim authority", claim_path),
    ):
        if not path.is_file():
            try:
                relative = path.relative_to(root)
            except ValueError:
                relative = path
            errors.append(f"{slug}: {label} is missing: {relative}")

    if not source_path.is_file() or not edition_path.is_file():
        return errors

    source = load_json(source_path)
    edition = load_json(edition_path)
    edition_schema_name = str(edition.get("schema", ""))
    edition_schema_path = root / "docs/documentaries" / edition_schema_name
    if not edition_schema_name or not edition_schema_path.is_file():
        errors.append(f"{slug}: closed edition schema is missing: {edition_schema_name!r}")
    else:
        edition_schema = load_json(edition_schema_path)
        Draft202012Validator.check_schema(edition_schema)
        errors += schema_errors(
            edition,
            edition_schema,
            str(edition_schema_path.relative_to(root)),
        )

    for actual, expected, label in (
        (edition.get("volume_id"), volume.get("slug"), "volume_id"),
        (edition.get("campaign_id"), volume.get("campaign_id"), "campaign_id"),
        (edition.get("title"), volume.get("title"), "title"),
        (edition.get("documentary_tier"), MICRO_TIER, "documentary_tier"),
        (edition.get("source_reference"), volume.get("source_record"), "source_reference"),
    ):
        if actual != expected:
            errors.append(f"{slug}: edition {label} {actual!r} does not match {expected!r}")

    source_lock = str(volume.get("source_lock", ""))
    expected_repository, _, expected_merge = source_lock.partition("@")
    if source.get("source_repository") != expected_repository:
        errors.append(f"{slug}: source-reference repository does not match protected locator")
    if source.get("source_lock_merge") != expected_merge:
        errors.append(f"{slug}: source-reference merge does not match protected locator")
    if source.get("campaign_id") != volume.get("campaign_id"):
        errors.append(f"{slug}: source-reference campaign does not match manifest")

    transcription = source.get("transcription", {})
    governed = volume.get("governed_transcription", {})
    for actual, expected, label in (
        (transcription.get("git_blob_sha1"), governed.get("git_blob_sha1"), "transcription Git blob"),
        (transcription.get("sha256"), governed.get("sha256"), "transcription SHA-256"),
        (transcription.get("byte_length"), governed.get("bytes"), "transcription byte length"),
    ):
        if actual != expected:
            errors.append(f"{slug}: {label} does not match manifest")

    source_bundle = volume.get("authoritative_source_bundle", {})
    if source_bundle.get("release_locator") != source_lock:
        errors.append(f"{slug}: authoritative source locator does not match source lock")
    if source_bundle.get("sha256") != governed.get("sha256"):
        errors.append(f"{slug}: authoritative source SHA-256 does not match governed transcription")
    if source_bundle.get("bytes") != governed.get("bytes"):
        errors.append(f"{slug}: authoritative source byte length does not match governed transcription")

    if page_path.is_file():
        page_text = page_path.read_text(encoding="utf-8")
        if str(volume.get("display_status", "")).lower() not in page_text.lower():
            # Historical pages may use a longer status phrase, but the source-locked marker is mandatory.
            if "source-locked historical" not in page_text.lower():
                errors.append(f"{slug}: web page is missing source-locked historical status")
        for plate in edition.get("plates", []):
            plate_id = str(plate.get("id", ""))
            asset_name = str(plate.get("asset", ""))
            if plate.get("authority") != "pedagogical_orientation_only":
                errors.append(f"{slug}: plate {plate_id} has invalid authority")
            asset_path = root / "docs" / asset_name
            if not asset_path.is_file():
                errors.append(f"{slug}: missing plate asset {asset_name}")
                continue
            if asset_name not in page_text:
                errors.append(f"{slug}: page does not reference plate asset {asset_name}")
            if asset_path.suffix == ".svg":
                errors += legacy._svg_errors(asset_path, slug, plate_id)

    mkdocs_path = root / "mkdocs.yml"
    if mkdocs_path.is_file():
        mkdocs_text = mkdocs_path.read_text(encoding="utf-8")
        if f"documentaries/{volume.get('web_page', '')}" not in mkdocs_text:
            errors.append(f"{slug}: MkDocs navigation is missing micro-edition page")

    return errors


def _legacy_discovery_errors(
    legacy_manifest: dict[str, Any],
    micro: list[dict[str, Any]],
    candidates: dict[str, Any],
    root: Path,
) -> list[str]:
    micro_editions = {str(volume.get("edition_record", "")) for volume in micro}
    micro_pages = {str(volume.get("web_page", "")) for volume in micro}
    micro_assets: set[str] = set()
    micro_asset_dirs: set[str] = set()
    micro_root_files: set[str] = set()
    for volume in micro:
        assets = _micro_asset_paths(volume, root)
        micro_assets.update(assets)
        for asset in assets:
            path = Path(asset)
            parts = path.parts
            if len(parts) >= 3 and parts[0] == "assets" and parts[1] == "documentaries":
                micro_asset_dirs.add(parts[2])
        micro_root_files.update(_micro_root_files(volume, root))

    root_files = {
        path.name
        for path in (root / "docs/documentaries").iterdir()
        if path.is_file()
    }

    return legacy.collection_discovery_errors(
        legacy_manifest,
        root,
        candidates=candidates,
        discovered_records=legacy.discovered_edition_records(root) - micro_editions,
        discovered_pages=legacy.discovered_web_pages(root) - micro_pages,
        discovered_sources=legacy.discovered_source_records(root),
        discovered_assets=legacy.discovered_documentary_assets(root) - micro_assets,
        discovered_asset_dirs=legacy.discovered_asset_directories(root) - micro_asset_dirs,
        discovered_candidate_records=legacy.discovered_candidate_locks(root),
        root_files=root_files - micro_root_files,
    )


def _legacy_web_errors(legacy_manifest: dict[str, Any], root: Path) -> list[str]:
    errors: list[str] = []
    web_schema = load_json(root / "docs/documentaries/documentary_web.schema.json")
    Draft202012Validator.check_schema(web_schema)
    domains = legacy._domains(root)
    all_assets: list[str] = []

    for volume in legacy_manifest.get("volumes", []):
        slug = str(volume.get("slug", "<unknown>"))
        edition_path = root / "docs/documentaries" / str(volume.get("edition_record", ""))
        page_path = root / "docs/documentaries" / str(volume.get("web_page", ""))
        if not edition_path.is_file() or not page_path.is_file():
            continue
        edition = load_json(edition_path)
        page_text = page_path.read_text(encoding="utf-8")
        errors += legacy.schema_errors(
            edition,
            web_schema,
            str(edition_path.relative_to(root)),
        )
        errors += legacy.web_edition_errors(volume, edition, page_text, root)
        all_assets += [str(plate.get("asset", "")) for plate in edition.get("plates", [])]
        domain = domains.get(volume.get("domain_id"))
        if domain:
            label = f"Domain {int(domain['programme_number']):02d}"
            reference_crosswalk = (
                volume.get("documentary_tier") == "reference"
                and str(volume.get("campaign_id", "")) in page_text
            )
            if label not in page_text and not reference_crosswalk:
                errors.append(f"{slug}: page is missing programme crosswalk {label}")

    for duplicate in sorted(legacy.duplicate_values(all_assets)):
        errors.append(f"documentary collection: duplicate plate asset {duplicate}")

    required = (
        root / "docs/javascripts/documentary.js",
        root / "docs/javascripts/documentary-mathjax.js",
        root / "docs/stylesheets/documentary.css",
        root / "docs/stylesheets/documentary-status.css",
        root / "reviews/documentation/DOCUMENTARY-LIBRARY.agent_review.yaml",
        root / "docs/decisions/ADR-0010_DOCUMENTARY_LIBRARY_AUTHORITY.md",
        root / "docs/documentaries/DOCUMENTARY_CANDIDATES.json",
        root / "schemas/documentary_candidate_registry.schema.json",
    )
    for path in required:
        if not path.is_file():
            errors.append(f"documentary authority file is missing: {path.relative_to(root)}")

    reader_css = required[2].read_text(encoding="utf-8") if required[2].is_file() else ""
    for marker in (
        "@media(max-width:680px)",
        "prefers-reduced-motion",
        "@media print",
        ":focus-visible",
    ):
        if marker not in reader_css:
            errors.append(f"documentary reader CSS is missing {marker}")

    status_css = required[3].read_text(encoding="utf-8") if required[3].is_file() else ""
    for volume in legacy_manifest.get("volumes", []):
        if volume.get("documentary_tier") != "reference":
            selector = f'.gcl-monograph[data-gcl-reader="{volume["slug"]}"]'
            if selector not in status_css:
                errors.append(f"{volume['slug']}: status CSS is missing scoped palette")
    for marker in ("@media(max-width:680px)", "@media print"):
        if marker not in status_css:
            errors.append(f"documentary status CSS is missing {marker}")
    return errors


def documentary_contract_errors(root: Path = ROOT) -> list[str]:
    manifest = load_json(root / "docs/documentaries/ARTIFACT_MANIFEST.json")
    candidates = load_json(root / "docs/documentaries/DOCUMENTARY_CANDIDATES.json")
    legacy_manifest = _legacy_projection(manifest)
    micro = _micro_volumes(manifest)

    legacy_schema = load_json(root / "schemas/documentary_manifest.schema.json")
    candidate_schema = load_json(root / "schemas/documentary_candidate_registry.schema.json")
    micro_schema = load_json(MICRO_SCHEMA if root == ROOT else root / "schemas/documentary_historical_micro.schema.json")
    Draft202012Validator.check_schema(legacy_schema)
    Draft202012Validator.check_schema(candidate_schema)
    Draft202012Validator.check_schema(micro_schema)

    errors = legacy.schema_errors(
        legacy_manifest,
        legacy_schema,
        "docs/documentaries/ARTIFACT_MANIFEST.json (legacy projection)",
    )
    errors += legacy.schema_errors(
        candidates,
        candidate_schema,
        "docs/documentaries/DOCUMENTARY_CANDIDATES.json",
    )

    # Preserve global identity uniqueness across both edition classes.
    for field in ("slug", "title", "source_record", "web_page", "edition_record"):
        values = [str(volume.get(field, "")) for volume in manifest.get("volumes", [])]
        for duplicate in sorted(legacy.duplicate_values(values)):
            errors.append(f"documentary manifest: duplicate {field}: {duplicate}")

    errors += legacy.manifest_semantic_errors(legacy_manifest, root)
    errors += legacy.candidate_semantic_errors(candidates, manifest, root)
    errors += _legacy_discovery_errors(legacy_manifest, micro, candidates, root)
    errors += _legacy_web_errors(legacy_manifest, root)

    for volume in micro:
        errors += _micro_semantic_errors(volume, micro_schema, root)

    return errors


def main() -> int:
    errors = documentary_contract_errors()
    if errors:
        for error in errors:
            print(error)
        print(f"documentary library validation failed with {len(errors)} error(s)")
        return 1
    manifest = load_json(ROOT / "docs/documentaries/ARTIFACT_MANIFEST.json")
    print(
        f"documentary library contracts are valid for {len(manifest.get('volumes', []))} admitted edition(s)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
