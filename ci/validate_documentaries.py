#!/usr/bin/env python3
"""Validate admitted and pre-admission Documentary Library contracts."""

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
CANDIDATE_REGISTRY = DOCUMENTARIES / "DOCUMENTARY_CANDIDATES.json"

FORBIDDEN_SOURCE_LABELS = (
    "Authoritative LaTeX",
    "Authoritative source:",
    "Read the LaTeX source",
)
TIER_MINIMUMS = {
    "reference": (5, 5, 3),
    "full": (6, 6, 5),
    "orientation": (5, 6, 4),
}
OPEN_SURFACES = (
    'class="definition-box"',
    'class="theorem-box"',
    'class="conjecture-box"',
    'class="imported-box"',
    'class="warning-box"',
)
REFERENCE_SURFACES = (
    'class="claim-box"',
    'class="guardrail"',
    'class="proof-spine"',
)
SHARED_CSS = {
    "docs/stylesheets/documentary.css",
    "docs/stylesheets/documentary-status.css",
}
SHARED_JS = {
    "docs/javascripts/documentary.js",
    "docs/javascripts/documentary-mathjax.js",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def schema_errors(instance: Any, schema: dict[str, Any], label: str) -> list[str]:
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    return [
        f"{label}{error.json_path}: {error.message}"
        for error in sorted(validator.iter_errors(instance), key=lambda item: list(item.path))
    ]


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


def discovered_web_pages(root: Path = ROOT) -> set[str]:
    return {
        path.name
        for path in (root / "docs/documentaries").glob("*.md")
        if path.name != "index.md"
    }


def discovered_source_records(root: Path = ROOT) -> set[str]:
    return {
        f"sources/{path.name}"
        for path in (root / "docs/documentaries/sources").glob("*.tex")
    }


def discovered_documentary_assets(root: Path = ROOT) -> set[str]:
    asset_root = root / "docs/assets/documentaries"
    if not asset_root.is_dir():
        return set()
    return {
        path.relative_to(root / "docs").as_posix()
        for path in asset_root.rglob("*")
        if path.is_file()
    }


def discovered_asset_directories(root: Path = ROOT) -> set[str]:
    asset_root = root / "docs/assets/documentaries"
    if not asset_root.is_dir():
        return set()
    return {path.name for path in asset_root.iterdir() if path.is_dir()}


def discovered_candidate_locks(root: Path = ROOT) -> set[str]:
    """Discover all documentary source locks, including locks retained after admission."""
    return {
        path.relative_to(root).as_posix()
        for path in (root / "campaigns").glob("**/artifacts/*SOURCE_LOCK.json")
    }


def discovered_shared_authority_files(root: Path = ROOT) -> tuple[set[str], set[str]]:
    css = {
        path.relative_to(root).as_posix()
        for path in (root / "docs/stylesheets").glob("documentary*.css")
    }
    js = {
        path.relative_to(root).as_posix()
        for path in (root / "docs/javascripts").glob("documentary*.js")
    }
    return css, js


def _domains(root: Path) -> dict[str, dict[str, Any]]:
    registry = yaml.safe_load((root / "DOMAIN_REGISTRY.yaml").read_text(encoding="utf-8"))
    return {domain["domain_id"]: domain for domain in registry.get("domains", [])}


def _expected_assets(manifest: dict[str, Any], root: Path) -> set[str]:
    assets: set[str] = set()
    for volume in manifest.get("volumes", []):
        path = root / "docs/documentaries" / str(volume.get("edition_record", ""))
        if path.is_file():
            edition = load_json(path)
            assets.update(str(plate.get("asset", "")) for plate in edition.get("plates", []))
    return assets


def _static_documentary_errors(
    manifest: dict[str, Any],
    root: Path,
    *,
    root_files: set[str] | None = None,
) -> list[str]:
    expected_json = {
        "ARTIFACT_MANIFEST.json",
        "DOCUMENTARY_CANDIDATES.json",
        "documentary_web.schema.json",
        *(str(volume.get("edition_record", "")) for volume in manifest.get("volumes", [])),
    }
    expected_md = {
        "index.md",
        *(str(volume.get("web_page", "")) for volume in manifest.get("volumes", [])),
    }
    if root_files is None:
        root_files = {
            path.name
            for path in (root / "docs/documentaries").iterdir()
            if path.is_file()
        }
    errors: list[str] = []
    for name in sorted(root_files):
        suffix = Path(name).suffix.lower()
        if suffix == ".json" and name not in expected_json:
            errors.append(f"documentary static inventory: orphaned JSON file {name}")
        elif suffix == ".md" and name not in expected_md:
            errors.append(f"documentary static inventory: orphaned web page {name}")
        elif suffix in {".txt", ".tex"}:
            errors.append(f"documentary static inventory: forbidden root static file {name}")
    return errors


def _expected_source_locks(
    manifest: dict[str, Any], candidates: dict[str, Any]
) -> set[str]:
    return {
        str(record.get("source_lock", ""))
        for record in [
            *manifest.get("volumes", []),
            *candidates.get("candidates", []),
        ]
        if record.get("source_lock")
    }


def collection_discovery_errors(
    manifest: dict[str, Any],
    root: Path = ROOT,
    *,
    candidates: dict[str, Any] | None = None,
    discovered_records: set[str] | None = None,
    discovered_pages: set[str] | None = None,
    discovered_sources: set[str] | None = None,
    discovered_assets: set[str] | None = None,
    discovered_asset_dirs: set[str] | None = None,
    discovered_candidate_records: set[str] | None = None,
    discovered_css: set[str] | None = None,
    discovered_js: set[str] | None = None,
    root_files: set[str] | None = None,
    index_text: str | None = None,
    mkdocs_text: str | None = None,
) -> list[str]:
    errors: list[str] = []
    candidates = candidates if candidates is not None else load_json(
        root / "docs/documentaries/DOCUMENTARY_CANDIDATES.json"
    )
    volumes = manifest.get("volumes", [])

    expected_editions = {str(volume.get("edition_record", "")) for volume in volumes}
    actual_editions = discovered_records if discovered_records is not None else discovered_edition_records(root)
    for name in sorted(expected_editions - actual_editions):
        errors.append(f"documentary discovery: manifest edition record is missing: {name}")
    for name in sorted(actual_editions - expected_editions):
        errors.append(f"documentary discovery: orphaned edition record is not in manifest: {name}")

    expected_pages = {str(volume.get("web_page", "")) for volume in volumes}
    actual_pages = discovered_pages if discovered_pages is not None else discovered_web_pages(root)
    for name in sorted(expected_pages - actual_pages):
        errors.append(f"documentary discovery: manifest web page is missing: {name}")
    for name in sorted(actual_pages - expected_pages):
        errors.append(f"documentary discovery: orphaned web page is not in manifest: {name}")

    expected_sources = {str(volume.get("source_record", "")) for volume in volumes}
    actual_sources = discovered_sources if discovered_sources is not None else discovered_source_records(root)
    for name in sorted(expected_sources - actual_sources):
        errors.append(f"documentary discovery: admitted source record is missing: {name}")
    for name in sorted(actual_sources - expected_sources):
        errors.append(f"documentary discovery: orphaned admitted source record is not in manifest: {name}")

    expected_assets = _expected_assets(manifest, root)
    actual_assets = discovered_assets if discovered_assets is not None else discovered_documentary_assets(root)
    for name in sorted(expected_assets - actual_assets):
        errors.append(f"documentary discovery: declared asset is missing: {name}")
    for name in sorted(actual_assets - expected_assets):
        errors.append(f"documentary discovery: orphaned documentary asset is undeclared: {name}")

    expected_dirs = {str(volume.get("slug", "")) for volume in volumes}
    actual_dirs = discovered_asset_dirs if discovered_asset_dirs is not None else discovered_asset_directories(root)
    for name in sorted(expected_dirs - actual_dirs):
        errors.append(f"documentary discovery: asset directory is missing: {name}")
    for name in sorted(actual_dirs - expected_dirs):
        errors.append(f"documentary discovery: orphaned asset directory is undeclared: {name}")

    expected_locks = _expected_source_locks(manifest, candidates)
    actual_locks = (
        discovered_candidate_records
        if discovered_candidate_records is not None
        else discovered_candidate_locks(root)
    )
    for name in sorted(expected_locks - actual_locks):
        errors.append(f"documentary source-lock discovery: registered source lock is missing: {name}")
    for name in sorted(actual_locks - expected_locks):
        errors.append(f"documentary source-lock discovery: orphaned source lock is unregistered: {name}")

    actual_css, actual_js = discovered_shared_authority_files(root)
    if discovered_css is not None:
        actual_css = discovered_css
    if discovered_js is not None:
        actual_js = discovered_js
    for name in sorted(SHARED_CSS - actual_css):
        errors.append(f"documentary authority: shared CSS file is missing: {name}")
    for name in sorted(actual_css - SHARED_CSS):
        errors.append(f"documentary authority: orphaned shared CSS file: {name}")
    for name in sorted(SHARED_JS - actual_js):
        errors.append(f"documentary authority: shared JavaScript file is missing: {name}")
    for name in sorted(actual_js - SHARED_JS):
        errors.append(f"documentary authority: orphaned shared JavaScript file: {name}")

    errors += _static_documentary_errors(manifest, root, root_files=root_files)

    tiers = [str(volume.get("documentary_tier", "")) for volume in volumes]
    if tiers.count("reference") != 1:
        errors.append("documentary discovery: exactly one reference tier is required")
    if "full" not in tiers:
        errors.append("documentary discovery: at least one full tier is required")
    if "orientation" not in tiers:
        errors.append("documentary discovery: at least one orientation tier is required")

    index_text = index_text if index_text is not None else (
        root / "docs/documentaries/index.md"
    ).read_text(encoding="utf-8")
    mkdocs_text = mkdocs_text if mkdocs_text is not None else (
        root / "mkdocs.yml"
    ).read_text(encoding="utf-8")
    if "DOCUMENTARY_CANDIDATES.json" not in index_text:
        errors.append("documentary candidates: collection index is missing candidate-registry link")
    if "documentaries/DOCUMENTARY_CANDIDATES.json" not in mkdocs_text:
        errors.append("documentary candidates: MkDocs navigation is missing candidate registry")
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
    allowed = {
        "reference": {"solved_theorem_archive"},
        "full": {"campaign_documentary"},
        "orientation": {"campaign_documentary", "parent_challenge_orientation"},
    }
    errors: list[str] = []
    if tier in allowed and scope not in allowed[tier]:
        errors.append(
            f"{slug}: documentary tier {tier!r} is incompatible with scope relation {scope!r}"
        )
    if domain:
        archived = domain.get("status") == "ARCHIVED"
        if scope == "solved_theorem_archive" and not archived:
            errors.append(f"{slug}: solved_theorem_archive requires an ARCHIVED domain")
        if scope != "solved_theorem_archive" and archived:
            errors.append(f"{slug}: open documentary scope requires an ACTIVE domain")
    return errors


def _status_errors(record: dict[str, Any], label: str) -> list[str]:
    claim_status = record.get("claim_status")
    problem_class = record.get("problem_class")
    open_classes = {"millennium_open_problem", "open_conjecture"}
    solved_classes = {"solved_classical_theorem", "solved_problem_reconstruction"}
    if claim_status == "open" and problem_class not in open_classes:
        return [f"{label}: open claim status is incompatible with problem class {problem_class!r}"]
    if claim_status == "solved" and problem_class not in solved_classes:
        return [f"{label}: solved claim status is incompatible with problem class {problem_class!r}"]
    return []


def _source_lock_semantic_errors(
    volume: dict[str, Any], root: Path, slug: str
) -> list[str]:
    source_lock = volume.get("source_lock")
    if not source_lock:
        return []
    path = root / str(source_lock)
    if not path.is_file():
        return [f"{slug}: source lock is missing: {source_lock}"]
    lock = load_json(path)
    comparisons = {
        "domain_id": volume.get("domain_id"),
        "campaign_id": volume.get("campaign_id"),
        "title": volume.get("title"),
        "subject": volume.get("topic"),
        "claim_status": volume.get("claim_status"),
        "problem_class": volume.get("problem_class"),
        "display_status": volume.get("display_status"),
        "claim_authority": volume.get("claim_authority"),
        "proposed_documentary_tier": volume.get("documentary_tier"),
    }
    errors: list[str] = []
    for field, expected in comparisons.items():
        actual = lock.get(field)
        if field in {"title", "subject"}:
            matches = normalized_human_text(actual) == normalized_human_text(expected)
        else:
            matches = actual == expected
        if not matches:
            errors.append(
                f"{slug}: source lock {field} {actual!r} does not match manifest {expected!r}"
            )
    expected_release = {
        key: volume.get(key)
        for key in ("rendered_pdf", "latex_source", "authoritative_source_bundle")
    }
    if lock.get("release_artifacts") != expected_release:
        errors.append(f"{slug}: source-lock release artifacts do not match manifest")
    return errors


def manifest_semantic_errors(manifest: dict[str, Any], root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    volumes = manifest.get("volumes", [])
    domains = _domains(root)
    directory = root / "docs/documentaries"

    for field in ("slug", "title", "source_record", "web_page", "edition_record"):
        for duplicate in sorted(
            duplicate_values(str(volume.get(field, "")) for volume in volumes)
        ):
            errors.append(f"documentary manifest: duplicate {field}: {duplicate}")
    locks = [str(volume["source_lock"]) for volume in volumes if volume.get("source_lock")]
    for duplicate in sorted(duplicate_values(locks)):
        errors.append(f"documentary manifest: duplicate source_lock: {duplicate}")

    for volume in volumes:
        slug = str(volume.get("slug", "<unknown>"))
        domain = domains.get(volume.get("domain_id"))
        campaign = volume.get("campaign_id")
        errors += _status_errors(volume, slug)
        if not domain:
            errors.append(f"{slug}: unknown domain_id {volume.get('domain_id')!r}")
        elif domain.get("campaign_id") != campaign:
            errors.append(
                f"{slug}: campaign_id {campaign!r} does not match domain "
                f"{volume.get('domain_id')} campaign {domain.get('campaign_id')!r}"
            )
        errors += _scope_errors(volume, domain)
        errors += _source_lock_semantic_errors(volume, root, slug)

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
            expected_authority = (
                "docs/POINCARE_RECONSTRUCTION_ARCHIVE.md"
                if volume.get("scope_relation") == "solved_theorem_archive"
                else domain.get("canonical_entry")
            )
            if volume.get("claim_authority") != expected_authority:
                errors.append(
                    f"{slug}: claim authority {volume.get('claim_authority')!r} "
                    f"does not match expected authority {expected_authority!r}"
                )

        source = paths["source record"]
        if source.is_file():
            record = source_record_fields(source.read_text(encoding="utf-8"))
            expected = {
                "title": volume.get("title"),
                "subject": volume.get("topic"),
                "pages": volume.get("pages"),
                "latex_sha256": volume.get("latex_source", {}).get("sha256"),
                "bundle_sha256": volume.get("authoritative_source_bundle", {}).get("sha256"),
                "pdf_sha256": volume.get("rendered_pdf", {}).get("sha256"),
            }
            for field, value in expected.items():
                actual = record.get(field)
                matches = (
                    normalized_human_text(actual) == normalized_human_text(value)
                    if field in {"title", "subject"}
                    else actual == value
                )
                if not matches:
                    errors.append(
                        f"{slug}: source record {field} {actual!r} "
                        f"does not match manifest {value!r}"
                    )

        page = paths["web page"]
        if page.is_file():
            text = page.read_text(encoding="utf-8")
            for value, label in (
                (volume.get("title"), "manifest title"),
                (campaign, f"campaign crosswalk {campaign}"),
            ):
                if str(value) not in text:
                    errors.append(f"{slug}: web page is missing {label}")
            if "claim boundary" not in text.lower():
                errors.append(f"{slug}: web page is missing explicit claim boundary")
            if "source record" not in text.lower():
                errors.append(f"{slug}: web page does not identify the source record")
            if (
                "authoritative source artifact" not in text.lower()
                and "authoritative complete illustrated source bundle" not in text.lower()
            ):
                errors.append(f"{slug}: web page does not identify the authoritative source")
            for forbidden in FORBIDDEN_SOURCE_LABELS:
                if forbidden in text:
                    errors.append(f"{slug}: misleading source label remains: {forbidden}")
            for identity in release_identity_strings(volume):
                if identity not in text:
                    errors.append(f"{slug}: web page is missing release identity {identity}")
    return errors


def candidate_semantic_errors(
    candidates: dict[str, Any], manifest: dict[str, Any], root: Path = ROOT
) -> list[str]:
    errors: list[str] = []
    domains = _domains(root)
    items = candidates.get("candidates", [])
    admitted_slugs = {str(volume.get("slug", "")) for volume in manifest.get("volumes", [])}
    for field in ("slug", "source_record", "source_lock", "review_record"):
        for duplicate in sorted(
            duplicate_values(str(item.get(field, "")) for item in items)
        ):
            errors.append(f"documentary candidates: duplicate {field}: {duplicate}")
    for candidate in items:
        slug = str(candidate.get("slug", "<unknown>"))
        errors += _status_errors(candidate, f"candidate {slug}")
        if slug in admitted_slugs:
            errors.append(f"candidate {slug}: slug is already admitted by ARTIFACT_MANIFEST.json")
        domain = domains.get(candidate.get("domain_id"))
        if not domain:
            errors.append(f"candidate {slug}: unknown domain_id {candidate.get('domain_id')!r}")
        elif domain.get("campaign_id") != candidate.get("campaign_id"):
            errors.append(f"candidate {slug}: campaign_id does not match domain registry")
        elif candidate.get("claim_authority") != domain.get("canonical_entry"):
            errors.append(f"candidate {slug}: claim authority does not match domain canonical entry")
        for key in ("source_record", "source_lock", "review_record", "claim_authority"):
            path = root / str(candidate.get(key, ""))
            if not path.is_file():
                errors.append(f"candidate {slug}: {key} is missing: {candidate.get(key)!r}")
        source_record = str(candidate.get("source_record", ""))
        if source_record.startswith("docs/"):
            errors.append(f"candidate {slug}: pre-admission source record must remain outside docs/")
        lock_path = root / str(candidate.get("source_lock", ""))
        if lock_path.is_file():
            lock = load_json(lock_path)
            comparisons = {
                "domain_id": candidate.get("domain_id"),
                "campaign_id": candidate.get("campaign_id"),
                "title": candidate.get("title"),
                "subject": candidate.get("topic"),
                "claim_status": candidate.get("claim_status"),
                "problem_class": candidate.get("problem_class"),
                "display_status": candidate.get("display_status"),
                "claim_authority": candidate.get("claim_authority"),
                "source_record": candidate.get("source_record"),
                "proposed_documentary_tier": candidate.get("proposed_documentary_tier"),
                "public_copy_policy": candidate.get("public_copy_policy"),
            }
            for field, expected in comparisons.items():
                if lock.get(field) != expected:
                    errors.append(
                        f"candidate {slug}: source lock {field} {lock.get(field)!r} "
                        f"does not match registry {expected!r}"
                    )
            if lock.get("release_artifacts") != candidate.get("release_artifacts"):
                errors.append(f"candidate {slug}: release artifacts do not match source lock")
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


def web_edition_errors(
    volume: dict[str, Any],
    edition: dict[str, Any],
    page_text: str,
    root: Path = ROOT,
) -> list[str]:
    slug = str(volume.get("slug", "<unknown>"))
    tier = str(volume.get("documentary_tier", ""))
    errors: list[str] = []
    for actual, expected, label in (
        (edition.get("volume_id"), slug, "volume_id"),
        (edition.get("title"), volume.get("title"), "title"),
        (edition.get("asset_base"), "docs_root", "asset_base"),
        (edition.get("schema_version"), "1.1.0", "schema_version"),
    ):
        if actual != expected:
            errors.append(f"{slug}: edition {label} does not match {expected!r}")

    normalized_page = page_text.replace("$p$-adic", "p-adic")
    claim_boundary = str(edition.get("claim_boundary", ""))
    if claim_boundary not in normalized_page:
        reference_boundary = tier == "reference" and "Final claim boundary" in page_text
        if not reference_boundary:
            errors.append(f"{slug}: page does not contain the edition claim boundary")

    display_status = str(volume.get("display_status", ""))
    if display_status not in str(edition.get("status", "")):
        errors.append(f"{slug}: edition status is missing display status {display_status!r}")
    if volume.get("claim_status") == "open":
        if page_text.count(display_status) < 2:
            errors.append(f"{slug}: open display status must appear at least twice")
    elif display_status not in page_text:
        errors.append(f"{slug}: solved display status is missing from page")

    markers = (
        f'data-gcl-reader="{slug}"',
        'data-edition="1.1.0"',
        '<article class="monograph-body"',
        'id="monograph-start" tabindex="-1"',
        'href="#monograph-start"',
        'aria-live="polite"',
        "source TeX remain",
    )
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

    minimums = TIER_MINIMUMS.get(tier, (0, 0, 0))
    for field, minimum in zip(("plates", "chapters", "appendices"), minimums):
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
    for marker in (
        'crossorigin="anonymous"',
        'referrerpolicy="no-referrer"',
        'data-archival-role="enhancement-only"',
    ):
        if marker not in page_text:
            errors.append(f"{slug}: MathJax policy attribute missing: {marker}")

    if str(volume.get("edition_record", "")) not in page_text:
        errors.append(f"{slug}: page is missing its edition-record link")
    if "ARTIFACT_MANIFEST.json" not in page_text and tier != "reference":
        errors.append(f"{slug}: page is missing the artifact-manifest link")
    return errors


def documentary_contract_errors(
    root: Path = ROOT,
    *,
    manifest: dict[str, Any] | None = None,
    candidates: dict[str, Any] | None = None,
    discovered_records: set[str] | None = None,
) -> list[str]:
    manifest = manifest or load_json(root / "docs/documentaries/ARTIFACT_MANIFEST.json")
    candidates = candidates or load_json(root / "docs/documentaries/DOCUMENTARY_CANDIDATES.json")
    manifest_schema = load_json(root / "schemas/documentary_manifest.schema.json")
    candidate_schema = load_json(root / "schemas/documentary_candidate_registry.schema.json")
    web_schema = load_json(root / "docs/documentaries/documentary_web.schema.json")
    Draft202012Validator.check_schema(manifest_schema)
    Draft202012Validator.check_schema(candidate_schema)
    Draft202012Validator.check_schema(web_schema)

    errors = schema_errors(manifest, manifest_schema, "docs/documentaries/ARTIFACT_MANIFEST.json")
    errors += schema_errors(candidates, candidate_schema, "docs/documentaries/DOCUMENTARY_CANDIDATES.json")
    errors += manifest_semantic_errors(manifest, root)
    errors += candidate_semantic_errors(candidates, manifest, root)
    errors += collection_discovery_errors(
        manifest,
        root,
        candidates=candidates,
        discovered_records=discovered_records,
    )

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
            reference_crosswalk = (
                volume.get("documentary_tier") == "reference"
                and str(volume.get("campaign_id", "")) in page_text
            )
            if label not in page_text and not reference_crosswalk:
                errors.append(f"{slug}: page is missing programme crosswalk {label}")

    for duplicate in sorted(duplicate_values(all_assets)):
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
    manifest = load_json(ROOT / "docs/documentaries/ARTIFACT_MANIFEST.json")
    candidates = load_json(ROOT / "docs/documentaries/DOCUMENTARY_CANDIDATES.json")
    print(
        f"documentary contracts are valid for {len(manifest['volumes'])} admitted edition(s) "
        f"and {len(candidates['candidates'])} pre-admission candidate(s)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
