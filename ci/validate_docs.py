#!/usr/bin/env python3
"""Validate public documentation navigation, authority, and coverage contracts."""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

REQUIRED_REPOSITORY_DOCS = {
    "ARCHITECTURE_OVERVIEW.md",
    "CERTIFICATION_LADDER.md",
    "CLAIM_LEDGER_STANDARD.md",
    "CLASSIFICATION_DISCOVERY_STANDARD.md",
    "DOMAIN_01_UNION_CLOSED_MASTER_PLAN.md",
    "DOMAIN_02_NAVIER_STOKES_CRITICAL_INTEGRABILITY_MASTER_PLAN.md",
    "DOMAIN_03_HODGE_CONJECTURE_MASTER_PLAN.md",
    "DOMAIN_04_BIRCH_SWINNERTON_DYER_MASTER_PLAN.md",
    "DOMAIN_05_POINCARE_RECONSTRUCTION_MASTER_PLAN.md",
    "DOMAIN_REGISTRY.yaml",
    "FILE_MANIFEST.md",
    "GOVERNANCE.md",
    "GRAND_CHALLENGE_PEDAGOGY_STANDARD.md",
    "GRAND_CHALLENGE_WORK_PACKAGE_STANDARD.md",
    "HANDOFF_STANDARD.md",
    "MATHCERT_SPEC.md",
    "MATHFORGE_SPEC.md",
    "MATHSOLVE_SPEC.md",
    "THURSTONIAN_ETHOS.md",
    "WP01_UNION_CLOSED_STATUS_SPINE.md",
    "WP02_UNION_CLOSED_LEAN_HANDOFF.md",
}

EXPECTED_DOMAIN_IDS = {"UC", "NSCI", "HC", "BSD", "PC"}
REQUIRED_STATUS_TERMS = {
    "Claim and support status",
    "Artifact lifecycle status",
    "Campaign disposition",
    "MATH-PROGRAMME",
}


def strip_frontmatter(text: str) -> str:
    lines = text.splitlines()
    if lines and lines[0] == "---":
        for index, line in enumerate(lines[1:], 1):
            if line == "---":
                return "\n".join(lines[index + 1 :])
    return text


def without_fenced_blocks(text: str) -> str:
    output: list[str] = []
    in_fence = False
    fence_marker = ""
    for line in text.splitlines():
        marker = line[:3]
        if marker in {"```", "~~~"}:
            if not in_fence:
                in_fence = True
                fence_marker = marker
            elif marker == fence_marker:
                in_fence = False
            continue
        if not in_fence:
            output.append(line)
    return "\n".join(output)


def nav_documents() -> set[str]:
    text = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
    return set(re.findall(r"(?<![\w/-])([A-Za-z0-9_./-]+\.md)", text))


def docs_documents() -> set[str]:
    return {path.relative_to(DOCS).as_posix() for path in DOCS.rglob("*.md")}


def rendered_h1_count(path: Path) -> int:
    text = without_fenced_blocks(strip_frontmatter(path.read_text(encoding="utf-8")))
    markdown_h1s = re.findall(r"(?m)^#\s+\S.*$", text)
    html_h1s = re.findall(r"<h1(?:\s[^>]*)?>", text, flags=re.IGNORECASE)
    return len(markdown_h1s) + len(html_h1s)


def local_link_targets(text: str) -> list[str]:
    markdown = re.findall(
        r"\[[^\]]+\]\((?!https?://|mailto:|#)([^)\s]+\.md(?:#[^)]+)?)\)",
        text,
    )
    html = re.findall(
        r'href=["\'](?!https?://|mailto:|#)([^"\']+\.md(?:#[^"\']+)?)',
        text,
    )
    return markdown + html


def local_markdown_link_errors(path: Path) -> list[str]:
    errors: list[str] = []
    for reference in local_link_targets(path.read_text(encoding="utf-8")):
        target = reference.split("#", 1)[0]
        if not (path.parent / target).exists():
            errors.append(f"{path.relative_to(ROOT)}: missing local Markdown target {reference}")
    return errors


def duplicate_values(values: list[Any]) -> set[Any]:
    seen: set[Any] = set()
    duplicates: set[Any] = set()
    for value in values:
        if value in seen:
            duplicates.add(value)
        seen.add(value)
    return duplicates


def domain_contract_errors(registry: dict[str, Any], nav: set[str]) -> list[str]:
    errors: list[str] = []
    domains = registry.get("domains", [])
    ids = [domain.get("domain_id") for domain in domains]
    numbers = [domain.get("programme_number") for domain in domains]
    slugs = [domain.get("slug") for domain in domains]
    campaigns = [domain.get("campaign_id") for domain in domains]

    for label, values in (
        ("domain_id", ids),
        ("programme_number", numbers),
        ("slug", slugs),
        ("campaign_id", campaigns),
    ):
        for duplicate in sorted(duplicate_values(values), key=str):
            errors.append(f"DOMAIN_REGISTRY.yaml: duplicate {label}: {duplicate}")

    if set(ids) != EXPECTED_DOMAIN_IDS:
        errors.append(
            "DOMAIN_REGISTRY.yaml: canonical domain set must be "
            + ", ".join(sorted(EXPECTED_DOMAIN_IDS))
        )
    if sorted(numbers) != list(range(1, len(domains) + 1)):
        errors.append("DOMAIN_REGISTRY.yaml: programme_number values must be contiguous from 1")

    decision_index = (DOCS / "AGENT_COUNCIL_DECISION_RECORDS.md").read_text(encoding="utf-8")
    catalogue = (DOCS / "domains" / "index.md").read_text(encoding="utf-8")
    for domain in domains:
        label = domain.get("domain_id", "<unknown>")
        slug = domain.get("slug", "")
        public_page = domain.get("public_page", "")
        canonical_entry = domain.get("canonical_entry", "")
        expected_public_page = f"docs/domains/{slug}.md"
        if public_page != expected_public_page:
            errors.append(
                f"{label}: public_page must be {expected_public_page}, found {public_page!r}"
            )
        public_path = ROOT / public_page
        if not public_path.is_file():
            errors.append(f"{label}: public page is missing: {public_page}")
        nav_path = public_page.removeprefix("docs/")
        if nav_path not in nav:
            errors.append(f"{label}: public page is not in mkdocs nav: {nav_path}")
        if not (ROOT / canonical_entry).is_file():
            errors.append(f"{label}: canonical entry is missing: {canonical_entry}")
        if domain.get("campaign_id", "") not in catalogue:
            errors.append(f"docs/domains/index.md: missing campaign {domain.get('campaign_id')}")
        if public_path.is_file():
            page_text = public_path.read_text(encoding="utf-8")
            if canonical_entry not in page_text:
                errors.append(f"{public_page}: missing canonical entry reference {canonical_entry}")
            if "Claim boundary" not in page_text and "claim boundary" not in page_text:
                errors.append(f"{public_page}: missing explicit claim boundary")
        for adr in domain.get("governance_refs", []):
            matching = list((DOCS / "decisions").glob(f"{adr}_*.md"))
            if len(matching) != 1:
                errors.append(f"{label}: governance ref {adr} does not resolve uniquely")
            if adr not in decision_index:
                errors.append(f"docs/AGENT_COUNCIL_DECISION_RECORDS.md: missing {adr}")

    return errors


def authority_contract_errors() -> list[str]:
    errors: list[str] = []
    root_pedagogy = (ROOT / "GRAND_CHALLENGE_PEDAGOGY_STANDARD.md").read_text(
        encoding="utf-8"
    )
    if "docs/GRAND_CHALLENGE_PEDAGOGY_STANDARD.md" not in root_pedagogy:
        errors.append(
            "GRAND_CHALLENGE_PEDAGOGY_STANDARD.md: must point to the canonical docs standard"
        )
    if "Canonical pointer" not in root_pedagogy:
        errors.append("GRAND_CHALLENGE_PEDAGOGY_STANDARD.md: missing Canonical pointer status")

    historical = (DOCS / "INTEGRATION_AUDIT_2026_06_21.md").read_text(encoding="utf-8")
    if "Historical snapshot" not in historical:
        errors.append("docs/INTEGRATION_AUDIT_2026_06_21.md: missing historical snapshot notice")

    status_text = (DOCS / "STATUS_TAXONOMY.md").read_text(encoding="utf-8")
    for term in sorted(REQUIRED_STATUS_TERMS):
        if term not in status_text:
            errors.append(f"docs/STATUS_TAXONOMY.md: missing required term {term}")

    mkdocs = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
    index = (DOCS / "index.md").read_text(encoding="utf-8")
    editions = set(re.findall(r"Edition (20\d{2}\.\d{2})", mkdocs, flags=re.IGNORECASE))
    editions.update(re.findall(r"edition (20\d{2}\.\d{2})", index, flags=re.IGNORECASE))
    if editions != {"2026.07"}:
        errors.append(f"edition markers must agree on 2026.07, found {sorted(editions)}")

    manifest = (ROOT / "FILE_MANIFEST.md").read_text(encoding="utf-8")
    if "Current governed inventory" not in manifest:
        errors.append("FILE_MANIFEST.md: missing current governed inventory status")

    return errors


def validate_documents() -> list[str]:
    errors: list[str] = []
    nav = nav_documents()
    docs = docs_documents()
    for document in sorted(docs - nav):
        errors.append(f"docs/{document}: missing from mkdocs nav")
    for document in sorted(nav - docs):
        errors.append(f"mkdocs.yml: nav target missing from docs: {document}")

    for path in sorted(DOCS.rglob("*.md")):
        count = rendered_h1_count(path)
        if count != 1:
            errors.append(f"{path.relative_to(ROOT)}: expected 1 rendered h1, found {count}")
        errors.extend(local_markdown_link_errors(path))

    repository_docs = (DOCS / "REPOSITORY_DOCS.md").read_text(encoding="utf-8")
    for document in sorted(REQUIRED_REPOSITORY_DOCS):
        if document not in repository_docs:
            errors.append(f"docs/REPOSITORY_DOCS.md: missing repository root entry {document}")

    registry = yaml.safe_load((ROOT / "DOMAIN_REGISTRY.yaml").read_text(encoding="utf-8"))
    errors.extend(domain_contract_errors(registry, nav))
    errors.extend(authority_contract_errors())
    return errors


def main() -> int:
    errors = validate_documents()
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        print(f"documentation validation failed with {len(errors)} error(s)", file=sys.stderr)
        return 1
    print("documentation navigation, authority, and domain coverage contracts are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
