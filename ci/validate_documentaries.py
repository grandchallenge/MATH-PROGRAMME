#!/usr/bin/env python3
"""Validate Documentary Library authority, crosswalk, release, and web-edition contracts."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
DOCUMENTARIES = DOCS / "documentaries"
MANIFEST_PATH = DOCUMENTARIES / "ARTIFACT_MANIFEST.json"
MANIFEST_SCHEMA_PATH = ROOT / "schemas" / "documentary_manifest.schema.json"
WEB_SCHEMA_PATH = DOCUMENTARIES / "documentary_web.schema.json"
POINCARE_EDITION_PATH = DOCUMENTARIES / "poincare.edition.json"
POINCARE_PAGE_PATH = DOCUMENTARIES / "poincare.md"

FORBIDDEN_SOURCE_LABELS = (
    "Authoritative LaTeX",
    "Authoritative source:",
    "Read the LaTeX source",
)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def schema_errors(instance: Any, schema: dict[str, Any], label: str) -> list[str]:
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    return [
        f"{label}{error.json_path}: {error.message}"
        for error in sorted(validator.iter_errors(instance), key=lambda item: list(item.path))
    ]


def duplicate_values(values: list[str]) -> set[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for value in values:
        if value in seen:
            duplicates.add(value)
        seen.add(value)
    return duplicates


def source_record_fields(text: str) -> dict[str, Any]:
    fields: dict[str, Any] = {}
    patterns = {
        "title": r"(?m)^% Title:\s*(.+?)\s*$",
        "subject": r"(?m)^% Subject:\s*(.+?)\s*$",
        "pages": r"(?m)^% Pages:\s*(\d+)\s*$",
        "latex_sha256": r"(?m)^% Complete LaTeX source SHA-256:\s*([0-9a-f]{64})\s*$",
        "bundle_sha256": r"(?m)^% (?:Authoritative )?[Cc]omplete illustrated source bundle SHA-256:\s*([0-9a-f]{64})\s*$",
        "pdf_sha256": r"(?m)^% Rendered PDF SHA-256:\s*([0-9a-f]{64})\s*$",
    }
    for name, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            fields[name] = int(match.group(1)) if name == "pages" else match.group(1)
    return fields


def release_identity_strings(volume: dict[str, Any]) -> list[str]:
    strings: list[str] = []
    for key in ("rendered_pdf", "latex_source", "authoritative_source_bundle"):
        artifact = volume[key]
        strings.extend(
            [
                f"{artifact['bytes']:,}",
                artifact["sha256"],
                artifact["availability"],
            ]
        )
    return strings


def manifest_semantic_errors(
    manifest: dict[str, Any],
    root: Path = ROOT,
) -> list[str]:
    errors: list[str] = []
    documentaries = root / "docs" / "documentaries"
    registry = yaml.safe_load((root / "DOMAIN_REGISTRY.yaml").read_text(encoding="utf-8"))
    domains = {domain["domain_id"]: domain for domain in registry.get("domains", [])}
    volumes = manifest.get("volumes", [])

    for field in ("slug", "title", "source_record", "web_page"):
        for duplicate in sorted(duplicate_values([str(volume.get(field, "")) for volume in volumes])):
            errors.append(f"documentary manifest: duplicate {field}: {duplicate}")

    for volume in volumes:
        slug = volume.get("slug", "<unknown>")
        domain_id = volume.get("domain_id")
        campaign_id = volume.get("campaign_id")
        domain = domains.get(domain_id)
        if domain is None:
            errors.append(f"{slug}: unknown domain_id {domain_id!r}")
        elif domain.get("campaign_id") != campaign_id:
            errors.append(
                f"{slug}: campaign_id {campaign_id!r} does not match domain {domain_id} "
                f"campaign {domain.get('campaign_id')!r}"
            )

        source_record = documentaries / str(volume.get("source_record", ""))
        web_page = documentaries / str(volume.get("web_page", ""))
        claim_authority = root / str(volume.get("claim_authority", ""))
        if not source_record.is_file():
            errors.append(f"{slug}: source record is missing: {volume.get('source_record')}")
        if not web_page.is_file():
            errors.append(f"{slug}: web page is missing: {volume.get('web_page')}")
        if not claim_authority.is_file():
            errors.append(f"{slug}: claim authority is missing: {volume.get('claim_authority')}")

        if source_record.is_file():
            record = source_record_fields(source_record.read_text(encoding="utf-8"))
            expected = {
                "title": volume.get("title"),
                "pages": volume.get("pages"),
                "latex_sha256": volume.get("latex_source", {}).get("sha256"),
                "bundle_sha256": volume.get("authoritative_source_bundle", {}).get("sha256"),
                "pdf_sha256": volume.get("rendered_pdf", {}).get("sha256"),
            }
            for field, value in expected.items():
                if record.get(field) != value:
                    errors.append(
                        f"{slug}: source record {field} {record.get(field)!r} does not match manifest {value!r}"
                    )

        if web_page.is_file():
            text = web_page.read_text(encoding="utf-8")
            if str(volume.get("title", "")) not in text:
                errors.append(f"{slug}: web page is missing manifest title")
            if str(campaign_id) not in text:
                errors.append(f"{slug}: web page is missing campaign crosswalk {campaign_id}")
            if "Claim boundary" not in text and "claim boundary" not in text:
                errors.append(f"{slug}: web page is missing explicit claim boundary")
            if "source record" not in text.lower():
                errors.append(f"{slug}: web page does not identify the committed pointer as a source record")
            if "authoritative source artifact" not in text.lower() and "authoritative complete illustrated source bundle" not in text.lower():
                errors.append(f"{slug}: web page does not identify the authoritative source artifact")
            for forbidden in FORBIDDEN_SOURCE_LABELS:
                if forbidden in text:
                    errors.append(f"{slug}: misleading documentary source label remains: {forbidden}")
            for identity in release_identity_strings(volume):
                if identity not in text:
                    errors.append(f"{slug}: web page is missing release identity value {identity}")

    return errors


def web_edition_errors(
    edition: dict[str, Any],
    page_text: str,
    root: Path = ROOT,
) -> list[str]:
    errors: list[str] = []
    docs = root / "docs"

    if edition.get("asset_base") != "docs_root":
        errors.append("poincare.edition.json: asset_base must be docs_root")
    for plate in edition.get("plates", []):
        asset = str(plate.get("asset", ""))
        if not (docs / asset).is_file():
            errors.append(f"poincare.edition.json: missing plate asset {asset}")
        if asset and asset not in page_text:
            errors.append(f"docs/documentaries/poincare.md: plate asset not referenced: {asset}")

    section_ids = [
        str(section.get("id", ""))
        for section in edition.get("chapters", []) + edition.get("appendices", [])
    ]
    for duplicate in sorted(duplicate_values(section_ids)):
        errors.append(f"poincare.edition.json: duplicate section id {duplicate}")
    for section_id in section_ids:
        if f'id="{section_id}"' not in page_text:
            errors.append(f"docs/documentaries/poincare.md: missing edition section id {section_id}")

    if '<main class="monograph-body"' in page_text:
        errors.append("docs/documentaries/poincare.md: nested main landmark is forbidden")
    if '<article class="monograph-body"' not in page_text:
        errors.append("docs/documentaries/poincare.md: manuscript must use an article landmark")
    target = re.search(r'<div class="monograph-reader"[^>]*id="monograph-start"[^>]*>', page_text)
    if not target or 'tabindex="-1"' not in target.group(0):
        errors.append("docs/documentaries/poincare.md: skip target must be programmatically focusable")
    if 'href="#monograph-start"' not in page_text:
        errors.append("docs/documentaries/poincare.md: skip link target is missing")

    math = edition.get("math_rendering", {})
    script_url = str(math.get("script_url", ""))
    if script_url and script_url not in page_text:
        errors.append("docs/documentaries/poincare.md: pinned MathJax script URL does not match edition record")
    for required in (
        'crossorigin="anonymous"',
        'referrerpolicy="no-referrer"',
        'data-archival-role="enhancement-only"',
    ):
        if required not in page_text:
            errors.append(f"docs/documentaries/poincare.md: MathJax policy attribute missing: {required}")
    if "source TeX remain" not in page_text and "source TeX remains" not in page_text:
        errors.append("docs/documentaries/poincare.md: no-JavaScript source-TeX fallback is not stated")
    if 'data-edition="1.1.0"' not in page_text:
        errors.append("docs/documentaries/poincare.md: rendered edition version does not match 1.1.0")

    return errors


def documentary_contract_errors(
    root: Path = ROOT,
    manifest: dict[str, Any] | None = None,
    edition: dict[str, Any] | None = None,
    poincare_text: str | None = None,
) -> list[str]:
    errors: list[str] = []
    manifest = manifest if manifest is not None else load_json(root / "docs/documentaries/ARTIFACT_MANIFEST.json")
    manifest_schema = load_json(root / "schemas/documentary_manifest.schema.json")
    Draft202012Validator.check_schema(manifest_schema)
    errors.extend(schema_errors(manifest, manifest_schema, "docs/documentaries/ARTIFACT_MANIFEST.json"))
    errors.extend(manifest_semantic_errors(manifest, root))

    web_schema = load_json(root / "docs/documentaries/documentary_web.schema.json")
    Draft202012Validator.check_schema(web_schema)
    edition = edition if edition is not None else load_json(root / "docs/documentaries/poincare.edition.json")
    errors.extend(schema_errors(edition, web_schema, "docs/documentaries/poincare.edition.json"))
    poincare_text = (
        poincare_text
        if poincare_text is not None
        else (root / "docs/documentaries/poincare.md").read_text(encoding="utf-8")
    )
    errors.extend(web_edition_errors(edition, poincare_text, root))

    required_files = (
        root / "docs/javascripts/documentary.js",
        root / "docs/javascripts/documentary-mathjax.js",
        root / "docs/stylesheets/documentary.css",
        root / "reviews/documentation/DOCUMENTARY-LIBRARY.agent_review.yaml",
        root / "docs/decisions/ADR-0010_DOCUMENTARY_LIBRARY_AUTHORITY.md",
    )
    for path in required_files:
        if not path.is_file():
            errors.append(f"documentary authority contract: required file missing: {path.relative_to(root)}")

    return errors


def main() -> int:
    errors = documentary_contract_errors()
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        print(f"documentary validation failed with {len(errors)} error(s)", file=sys.stderr)
        return 1
    print("documentary authority, release, crosswalk, and web-edition contracts are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
