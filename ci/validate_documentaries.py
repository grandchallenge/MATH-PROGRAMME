#!/usr/bin/env python3
"""Validate manifest-discovered Documentary Library contracts."""
from __future__ import annotations

import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Iterable

import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
DOCUMENTARIES = DOCS / "documentaries"
FORBIDDEN_SOURCE_LABELS = ("Authoritative LaTeX", "Authoritative source:", "Read the LaTeX source")
TIER_MINIMUMS = {"reference": (5, 5, 3), "full": (6, 6, 5), "orientation": (5, 6, 4)}
OPEN_SURFACES = ('class="definition-box"', 'class="theorem-box"', 'class="conjecture-box"', 'class="imported-box"', 'class="warning-box"')
REFERENCE_SURFACES = ('class="claim-box"', 'class="guardrail"', 'class="proof-spine"')


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def schema_errors(instance: Any, schema: dict[str, Any], label: str) -> list[str]:
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    return [f"{label}{error.json_path}: {error.message}" for error in sorted(validator.iter_errors(instance), key=lambda item: list(item.path))]


def duplicate_values(values: Iterable[str]) -> set[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for value in values:
        if value in seen:
            duplicates.add(value)
        seen.add(value)
    return duplicates


def normalized_human_text(value: Any) -> str:
    return str(value).replace("–", "-").replace("—", "-").replace("‑", "-")


def is_open_status(value: Any) -> bool:
    return normalized_human_text(value).strip().lower().startswith("open ")


def source_record_fields(text: str) -> dict[str, Any]:
    patterns = {
        "title": r"(?m)^% Title:\s*(.+?)\s*$",
        "subject": r"(?m)^% Subject:\s*(.+?)\s*$",
        "pages": r"(?m)^% Pages:\s*(\d+)\s*$",
        "latex_sha256": r"(?m)^% Complete LaTeX source SHA-256:\s*([0-9a-f]{64})\s*$",
        "bundle_sha256": r"(?m)^% (?:Authoritative )?[Cc]omplete illustrated source bundle SHA-256:\s*([0-9a-f]{64})\s*$",
        "pdf_sha256": r"(?m)^% Rendered PDF SHA-256:\s*([0-9a-f]{64})\s*$",
    }
    fields: dict[str, Any] = {}
    for name, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            fields[name] = int(match.group(1)) if name == "pages" else match.group(1)
    return fields


def release_identity_strings(volume: dict[str, Any]) -> list[str]:
    values: list[str] = []
    for key in ("rendered_pdf", "latex_source", "authoritative_source_bundle"):
        artifact = volume[key]
        values += [f"{artifact['bytes']:,}", artifact["sha256"], artifact["availability"]]
    return values


def discovered_edition_records(root: Path = ROOT) -> set[str]:
    return {path.name for path in (root / "docs/documentaries").glob("*.edition.json")}


def _domains(root: Path) -> dict[str, dict[str, Any]]:
    registry = yaml.safe_load((root / "DOMAIN_REGISTRY.yaml").read_text(encoding="utf-8"))
    return {domain["domain_id"]: domain for domain in registry.get("domains", [])}


def collection_discovery_errors(manifest: dict[str, Any], root: Path = ROOT, *, discovered_records: set[str] | None = None, index_text: str | None = None, mkdocs_text: str | None = None) -> list[str]:
    errors: list[str] = []
    volumes = manifest.get("volumes", [])
    expected = {str(volume.get("edition_record", "")) for volume in volumes}
    discovered = discovered_records if discovered_records is not None else discovered_edition_records(root)
    for name in sorted(expected - discovered):
        errors.append(f"documentary discovery: manifest edition record is missing: {name}")
    for name in sorted(discovered - expected):
        errors.append(f"documentary discovery: orphaned edition record is not in manifest: {name}")
    tiers = [str(volume.get("documentary_tier", "")) for volume in volumes]
    if tiers.count("reference") != 1:
        errors.append("documentary discovery: exactly one reference tier is required")
    if "full" not in tiers:
        errors.append("documentary discovery: at least one full tier is required")
    if "orientation" not in tiers:
        errors.append("documentary discovery: at least one orientation tier is required")
    index_text = index_text if index_text is not None else (root / "docs/documentaries/index.md").read_text(encoding="utf-8")
    mkdocs_text = mkdocs_text if mkdocs_text is not None else (root / "mkdocs.yml").read_text(encoding="utf-8")
    for volume in volumes:
        slug = str(volume.get("slug", "<unknown>"))
        page = str(volume.get("web_page", ""))
        edition = str(volume.get("edition_record", ""))
        if f"({page})" not in index_text:
            errors.append(f"{slug}: collection index is missing web page {page}")
        if f"({edition})" not in index_text:
            errors.append(f"{slug}: collection index is missing edition record {edition}")
        if f"documentaries/{page}" not in mkdocs_text:
            errors.append(f"{slug}: MkDocs navigation is missing web page {page}")
    return errors


def _scope_errors(volume: dict[str, Any], domain: dict[str, Any] | None) -> list[str]:
    slug = str(volume.get("slug", "<unknown>"))
    tier = volume.get("documentary_tier")
    scope = volume.get("scope_relation")
    allowed = {"reference": {"solved_theorem_archive"}, "full": {"campaign_documentary"}, "orientation": {"campaign_documentary", "parent_challenge_orientation"}}
    errors: list[str] = []
    if tier in allowed and scope not in allowed[tier]:
        errors.append(f"{slug}: documentary tier {tier!r} is incompatible with scope relation {scope!r}")
    if domain:
        archived = domain.get("status") == "ARCHIVED"
        if scope == "solved_theorem_archive" and not archived:
            errors.append(f"{slug}: solved_theorem_archive requires an ARCHIVED domain")
        if scope != "solved_theorem_archive" and archived:
            errors.append(f"{slug}: open documentary scope requires an ACTIVE domain")
    return errors


def manifest_semantic_errors(manifest: dict[str, Any], root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    volumes = manifest.get("volumes", [])
    domains = _domains(root)
    directory = root / "docs/documentaries"
    for field in ("slug", "title", "source_record", "web_page", "edition_record"):
        for duplicate in sorted(duplicate_values(str(volume.get(field, "")) for volume in volumes)):
            errors.append(f"documentary manifest: duplicate {field}: {duplicate}")
    for volume in volumes:
        slug = str(volume.get("slug", "<unknown>"))
        domain = domains.get(volume.get("domain_id"))
        campaign = volume.get("campaign_id")
        if not domain:
            errors.append(f"{slug}: unknown domain_id {volume.get('domain_id')!r}")
        elif domain.get("campaign_id") != campaign:
            errors.append(f"{slug}: campaign_id {campaign!r} does not match domain {volume.get('domain_id')} campaign {domain.get('campaign_id')!r}")
        errors += _scope_errors(volume, domain)
        paths = {
            "source record": directory / str(volume.get("source_record", "")),
            "web page": directory / str(volume.get("web_page", "")),
            "edition record": directory / str(volume.get("edition_record", "")),
            "claim authority": root / str(volume.get("claim_authority", "")),
        }
        for label, path in paths.items():
            if not path.is_file():
                errors.append(f"{slug}: {label} is missing: {path.relative_to(root)}")
        if domain:
            expected_authority = "docs/POINCARE_RECONSTRUCTION_ARCHIVE.md" if volume.get("scope_relation") == "solved_theorem_archive" else domain.get("canonical_entry")
            if volume.get("claim_authority") != expected_authority:
                errors.append(f"{slug}: claim authority {volume.get('claim_authority')!r} does not match expected authority {expected_authority!r}")
        source = paths["source record"]
        if source.is_file():
            record = source_record_fields(source.read_text(encoding="utf-8"))
            expected = {"title": volume.get("title"), "subject": volume.get("topic"), "pages": volume.get("pages"), "latex_sha256": volume.get("latex_source", {}).get("sha256"), "bundle_sha256": volume.get("authoritative_source_bundle", {}).get("sha256"), "pdf_sha256": volume.get("rendered_pdf", {}).get("sha256")}
            for field, value in expected.items():
                actual = record.get(field)
                matches = normalized_human_text(actual) == normalized_human_text(value) if field in {"title", "subject"} else actual == value
                if not matches:
                    errors.append(f"{slug}: source record {field} {actual!r} does not match manifest {value!r}")
        page = paths["web page"]
        if page.is_file():
            text = page.read_text(encoding="utf-8")
            for value, label in ((volume.get("title"), "manifest title"), (campaign, f"campaign crosswalk {campaign}")):
                if str(value) not in text:
                    errors.append(f"{slug}: web page is missing {label}")
            if "claim boundary" not in text.lower():
                errors.append(f"{slug}: web page is missing explicit claim boundary")
            if "source record" not in text.lower():
                errors.append(f"{slug}: web page does not identify the source record")
            if "authoritative source artifact" not in text.lower() and "authoritative complete illustrated source bundle" not in text.lower():
                errors.append(f"{slug}: web page does not identify the authoritative source")
            for forbidden in FORBIDDEN_SOURCE_LABELS:
                if forbidden in text:
                    errors.append(f"{slug}: misleading source label remains: {forbidden}")
            for identity in release_identity_strings(volume):
                if identity not in text:
                    errors.append(f"{slug}: web page is missing release identity {identity}")
    return errors


def _svg_errors(path: Path, slug: str, plate_id: str) -> list[str]:
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as exc:
        return [f"{slug}: plate {plate_id} is invalid XML: {exc}"]
    ns = {"svg": "http://www.w3.org/2000/svg"}
    errors: list[str] = []
    if root.find("svg:title", ns) is None:
        errors.append(f"{slug}: plate {plate_id} is missing SVG title")
    if root.find("svg:desc", ns) is None:
        errors.append(f"{slug}: plate {plate_id} is missing SVG description")
    return errors


def web_edition_errors(volume: dict[str, Any], edition: dict[str, Any], page_text: str, root: Path = ROOT) -> list[str]:
    slug = str(volume.get("slug", "<unknown>"))
    tier = str(volume.get("documentary_tier", ""))
    errors: list[str] = []
    for actual, expected, label in ((edition.get("volume_id"), slug, "volume_id"), (edition.get("title"), volume.get("title"), "title"), (edition.get("asset_base"), "docs_root", "asset_base"), (edition.get("schema_version"), "1.1.0", "schema_version")):
        if actual != expected:
            errors.append(f"{slug}: edition {label} does not match {expected!r}")
    normalized_page = page_text.replace("$p$-adic", "p-adic")
    claim_boundary = str(edition.get("claim_boundary", ""))
    if claim_boundary not in normalized_page and not (tier == "reference" and "Final claim boundary" in page_text):
        errors.append(f"{slug}: page does not contain the edition claim boundary")
    manifest_status = str(volume.get("status", ""))
    if is_open_status(manifest_status):
        if manifest_status not in str(edition.get("status", "")):
            errors.append(f"{slug}: exact open status is missing from edition record")
        if page_text.count(manifest_status) < 2:
            errors.append(f"{slug}: exact open status must appear at least twice")
    elif "Solved classical theorem" not in str(edition.get("status", "")):
        errors.append(f"{slug}: solved status is missing from edition record")
    markers = (f'data-gcl-reader="{slug}"', 'data-edition="1.1.0"', '<article class="monograph-body"', 'id="monograph-start" tabindex="-1"', 'href="#monograph-start"', 'aria-live="polite"', "source TeX remain")
    for marker in markers:
        if marker not in page_text:
            errors.append(f"{slug}: page is missing required marker {marker}")
    if '<main class="monograph-body"' in page_text:
        errors.append(f"{slug}: nested main landmark is forbidden")
    surfaces = REFERENCE_SURFACES if tier == "reference" else OPEN_SURFACES
    if tier != "reference":
        if "documentary-status.css" not in page_text:
            errors.append(f"{slug}: open edition is missing documentary-status.css")
        if "data-plate-dialog" not in page_text:
            errors.append(f"{slug}: open edition is missing the plate dialog")
    for marker in surfaces:
        if marker not in page_text:
            errors.append(f"{slug}: {tier} tier is missing surface {marker}")
    for field, minimum in zip(("plates", "chapters", "appendices"), TIER_MINIMUMS.get(tier, (0, 0, 0))):
        if len(edition.get(field, [])) < minimum:
            errors.append(f"{slug}: {tier} tier requires at least {minimum} {field}")
    plates = edition.get("plates", [])
    ids = [str(plate.get("id", "")) for plate in plates]
    assets = [str(plate.get("asset", "")) for plate in plates]
    for duplicate in sorted(duplicate_values(ids)):
        errors.append(f"{slug}: duplicate plate id {duplicate}")
    for duplicate in sorted(duplicate_values(assets)):
        errors.append(f"{slug}: duplicate plate asset {duplicate}")
    for plate in plates:
        plate_id = str(plate.get("id", ""))
        asset_name = str(plate.get("asset", ""))
        if plate.get("authority") != "pedagogical_orientation_only":
            errors.append(f"{slug}: plate {plate_id} has invalid authority")
        if len(str(plate.get("alt", ""))) < 20:
            errors.append(f"{slug}: plate {plate_id} alternative text is too short")
        asset = root / "docs" / asset_name
        if not asset.is_file():
            errors.append(f"{slug}: missing plate asset {asset_name}")
            continue
        if asset_name not in page_text:
            errors.append(f"{slug}: page does not reference plate asset {asset_name}")
        if asset.suffix == ".svg":
            errors += _svg_errors(asset, slug, plate_id)
    sections = edition.get("chapters", []) + edition.get("appendices", [])
    section_ids = [str(section.get("id", "")) for section in sections]
    for duplicate in sorted(duplicate_values(section_ids)):
        errors.append(f"{slug}: duplicate section id {duplicate}")
    for section_id in section_ids:
        if f'id="{section_id}"' not in page_text:
            errors.append(f"{slug}: page is missing section id {section_id}")
        if f'href="#{section_id}"' not in page_text:
            errors.append(f"{slug}: contents are missing section link {section_id}")
    for source in edition.get("sources", []):
        if source not in page_text:
            errors.append(f"{slug}: page is missing source URL {source}")
    math = edition.get("math_rendering", {})
    if str(math.get("script_url", "")) not in page_text:
        errors.append(f"{slug}: pinned MathJax URL does not match")
    for marker in ('crossorigin="anonymous"', 'referrerpolicy="no-referrer"', 'data-archival-role="enhancement-only"'):
        if marker not in page_text:
            errors.append(f"{slug}: MathJax policy attribute missing: {marker}")
    if str(volume.get("edition_record", "")) not in page_text:
        errors.append(f"{slug}: page is missing its edition-record link")
    if "ARTIFACT_MANIFEST.json" not in page_text and tier != "reference":
        errors.append(f"{slug}: page is missing the artifact-manifest link")
    return errors


def documentary_contract_errors(root: Path = ROOT, *, manifest: dict[str, Any] | None = None, discovered_records: set[str] | None = None) -> list[str]:
    manifest = manifest or load_json(root / "docs/documentaries/ARTIFACT_MANIFEST.json")
    manifest_schema = load_json(root / "schemas/documentary_manifest.schema.json")
    web_schema = load_json(root / "docs/documentaries/documentary_web.schema.json")
    Draft202012Validator.check_schema(manifest_schema)
    Draft202012Validator.check_schema(web_schema)
    errors = schema_errors(manifest, manifest_schema, "docs/documentaries/ARTIFACT_MANIFEST.json")
    errors += manifest_semantic_errors(manifest, root)
    errors += collection_discovery_errors(manifest, root, discovered_records=discovered_records)
    domains = _domains(root)
    all_assets: list[str] = []
    for volume in manifest.get("volumes", []):
        slug = str(volume.get("slug", "<unknown>"))
        edition_path = root / "docs/documentaries" / str(volume.get("edition_record", ""))
        page_path = root / "docs/documentaries" / str(volume.get("web_page", ""))
        if not edition_path.is_file() or not page_path.is_file():
            continue
        edition = load_json(edition_path)
        page_text = page_path.read_text(encoding="utf-8")
        errors += schema_errors(edition, web_schema, str(edition_path.relative_to(root)))
        errors += web_edition_errors(volume, edition, page_text, root)
        all_assets += [str(plate.get("asset", "")) for plate in edition.get("plates", [])]
        domain = domains.get(volume.get("domain_id"))
        if domain:
            label = f"Domain {int(domain['programme_number']):02d}"
            reference_crosswalk = volume.get("documentary_tier") == "reference" and str(volume.get("campaign_id", "")) in page_text
            if label not in page_text and not reference_crosswalk:
                errors.append(f"{slug}: page is missing programme crosswalk {label}")
    for duplicate in sorted(duplicate_values(all_assets)):
        errors.append(f"documentary collection: duplicate plate asset {duplicate}")
    required = (root / "docs/javascripts/documentary.js", root / "docs/javascripts/documentary-mathjax.js", root / "docs/stylesheets/documentary.css", root / "docs/stylesheets/documentary-status.css", root / "reviews/documentation/DOCUMENTARY-LIBRARY.agent_review.yaml", root / "docs/decisions/ADR-0010_DOCUMENTARY_LIBRARY_AUTHORITY.md")
    for path in required:
        if not path.is_file():
            errors.append(f"documentary authority file is missing: {path.relative_to(root)}")
    reader_css = required[2].read_text(encoding="utf-8") if required[2].is_file() else ""
    for marker in ("@media(max-width:680px)", "prefers-reduced-motion", "@media print", ":focus-visible"):
        if marker not in reader_css:
            errors.append(f"documentary reader CSS is missing {marker}")
    status_css = required[3].read_text(encoding="utf-8") if required[3].is_file() else ""
    for volume in manifest.get("volumes", []):
        if volume.get("documentary_tier") != "reference":
            selector = f'.gcl-monograph[data-gcl-reader="{volume["slug"]}"]'
            if selector not in status_css:
                errors.append(f"{volume['slug']}: status CSS is missing scoped palette")
    for marker in ("@media(max-width:680px)", "@media print"):
        if marker not in status_css:
            errors.append(f"documentary status CSS is missing {marker}")
    return errors


def main() -> int:
    errors = documentary_contract_errors()
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        print(f"documentary validation failed with {len(errors)} error(s)", file=sys.stderr)
        return 1
    count = len(load_json(DOCUMENTARIES / "ARTIFACT_MANIFEST.json").get("volumes", []))
    print(f"documentary manifest discovery and {count}-edition contracts are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
