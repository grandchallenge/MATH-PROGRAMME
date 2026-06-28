#!/usr/bin/env python3
"""Validate public documentation navigation and coherence contracts."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

REQUIRED_REPOSITORY_DOCS = {
    "ARCHITECTURE_OVERVIEW.md",
    "CERTIFICATION_LADDER.md",
    "CLAIM_LEDGER_STANDARD.md",
    "CLASSIFICATION_DISCOVERY_STANDARD.md",
    "DOMAIN_01_UNION_CLOSED_MASTER_PLAN.md",
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


def local_markdown_link_errors(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    pattern = re.compile(r"\[[^\]]+\]\((?!https?://|mailto:|#)([^)\s]+\.md(?:#[^)]+)?)\)")
    for match in pattern.finditer(text):
        target = match.group(1).split("#", 1)[0]
        if not (path.parent / target).exists():
            errors.append(f"{path.relative_to(ROOT)}: missing local Markdown target {match.group(1)}")
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
        if "Gröbner" in path.read_text(encoding="utf-8"):
            errors.append(f"{path.relative_to(ROOT)}: use ASCII Groebner in visible prose")
        errors.extend(local_markdown_link_errors(path))

    repository_docs = (DOCS / "REPOSITORY_DOCS.md").read_text(encoding="utf-8")
    for document in sorted(REQUIRED_REPOSITORY_DOCS):
        if document not in repository_docs:
            errors.append(f"docs/REPOSITORY_DOCS.md: missing repository root entry {document}")

    return errors


def main() -> int:
    errors = validate_documents()
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        print(f"documentation validation failed with {len(errors)} error(s)", file=sys.stderr)
        return 1
    print("documentation navigation and coherence contracts are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
