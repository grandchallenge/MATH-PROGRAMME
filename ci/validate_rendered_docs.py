#!/usr/bin/env python3
"""Validate the built MkDocs homepage for visible Markdown leakage."""
from __future__ import annotations

import argparse
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

from audit_math_typography import audit

ROOT = Path(__file__).resolve().parents[1]


class VisibleTextParser(HTMLParser):
    """Collect visible text while ignoring script and style payloads."""

    def __init__(self) -> None:
        super().__init__()
        self._ignored_depth = 0
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"script", "style"}:
            self._ignored_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style"} and self._ignored_depth:
            self._ignored_depth -= 1

    def handle_data(self, data: str) -> None:
        if not self._ignored_depth:
            self.parts.append(data)

    def text(self) -> str:
        return "\n".join(self.parts)


VISIBLE_MARKDOWN_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("ATX heading marker", re.compile(r"(?m)^\s*#{1,6}\s+\S")),
    ("Markdown emphasis marker", re.compile(r"\*\*[^*\n]+\*\*")),
    ("Markdown link syntax", re.compile(r"\[[^\]\n]+\]\([^)\n]+\)")),
    ("Markdown image syntax", re.compile(r"!\[[^\]\n]*\]\([^)\n]+\)")),
    ("Markdown table separator", re.compile(r"(?m)^\s*\|?\s*:?-{3,}:?\s*\|")),
)

REQUIRED_HOME_SECTIONS = (
    "What the programme is",
    "How a claim moves",
    "Current frontier",
    "Where to go next",
    "Claim boundary",
)


def homepage_render_errors(index_html: Path) -> list[str]:
    if not index_html.is_file():
        return [f"built homepage is missing: {index_html}"]

    parser = VisibleTextParser()
    parser.feed(index_html.read_text(encoding="utf-8"))
    visible = parser.text()

    errors: list[str] = []
    for label, pattern in VISIBLE_MARKDOWN_PATTERNS:
        match = pattern.search(visible)
        if match:
            excerpt = " ".join(match.group(0).split())
            errors.append(f"homepage exposes {label}: {excerpt!r}")

    for section in REQUIRED_HOME_SECTIONS:
        if section not in visible:
            errors.append(f"homepage is missing rendered section: {section}")

    return errors



class InfoAdmonitionParser(VisibleTextParser):
    """Detect the actual rendered info panel, not just its visible prose."""

    def __init__(self) -> None:
        super().__init__()
        self.info_boxes = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        super().handle_starttag(tag, attrs)
        if tag == "div":
            classes = set((dict(attrs).get("class") or "").split())
            if {"admonition", "info"}.issubset(classes):
                self.info_boxes += 1


def admonition_render_errors(page_html: Path, expected_title: str) -> list[str]:
    """Protect against MkDocs emitting literal !!! info instead of an info panel."""
    if not page_html.is_file():
        return [f"built admonition page is missing: {page_html}"]

    parser = InfoAdmonitionParser()
    parser.feed(page_html.read_text(encoding="utf-8"))
    visible = parser.text()

    errors: list[str] = []
    if re.search(r'(?m)^\s*!!!\s+info\b', visible):
        errors.append(f"{page_html} exposes literal !!! info markup")
    if parser.info_boxes == 0:
        errors.append(f"{page_html} has no rendered info admonition")
    if expected_title not in visible:
        errors.append(f"{page_html} is missing admonition title: {expected_title}")
    return errors


class CM4DisplayMathParser(HTMLParser):
    """Capture only actual display-math Arithmatex containers."""

    def __init__(self) -> None:
        super().__init__()
        self._depth = 0
        self._parts: list[str] = []
        self.displays: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if self._depth:
            self._depth += 1
        elif tag == "div" and "arithmatex" in (dict(attrs).get("class") or "").split():
            self._depth = 1
            self._parts = []

    def handle_endtag(self, tag: str) -> None:
        if self._depth:
            self._depth -= 1
            if not self._depth:
                self.displays.append("".join(self._parts))

    def handle_data(self, data: str) -> None:
        if self._depth:
            self._parts.append(data)


def cm4_display_math_errors(page_html: Path) -> list[str]:
    """Guard the known CM4 formula against silent raw-TeX publication.

    A generic wrapper-count audit missed a bare [ ... ] display, since it
    counted no math source and consequently demanded no generated wrapper.
    This page-specific witness binds the intended formula to an actual
    display (not inline) Arithmatex container before client-side MathJax.
    It does not claim to prove JavaScript/browser glyph rendering.
    """
    if not page_html.is_file():
        return [f"built CM4 result page is missing: {page_html}"]

    parsed = CM4DisplayMathParser()
    parsed.feed(page_html.read_text(encoding="utf-8"))
    expected = re.compile(
        r"\\mathbb\s*\{?Z\}?\s*\[S\]\s*\^\s*\{\s*\\square\s*\}"
    )
    if not any(expected.search(display) for display in parsed.displays):
        return [
            f"{page_html} has no Arithmatex display for "
            r"\mathbb Z[S]^{\square}; possible raw TeX or missing math wrapper"
        ]
    return []


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--site-dir",
        default=str(ROOT / "site"),
        help="MkDocs output directory; defaults to repository site/",
    )
    args = parser.parse_args()

    site_dir = Path(args.site_dir)
    errors = homepage_render_errors(site_dir / "index.html")
    for relative_path, title in (
        ("CMDG_CM4/index.html", "Research surface authority"),
        ("CMDG_CM4_RESEARCH_GUIDE/index.html", "Live work is issue-led"),
    ):
        errors.extend(admonition_render_errors(site_dir / relative_path, title))
    errors.extend(cm4_display_math_errors(site_dir / "CMDG_CM4" / "index.html"))
    # Whole-repository GFM-source audit plus checks on actual built Arithmatex HTML.
    # Publish the complete finding inventory without failing established legacy pages;
    # enforce strict typography on the newly repaired CM4 mathematical flagships.
    math_report = audit(ROOT, site_dir, github_live=True)
    (site_dir / "math-typography-audit.json").write_text(
        json.dumps(math_report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    flagship_pages = {
        "docs/CMDG_CM4_MATHEMATICAL_NOTE.md",
        "docs/CONDENSED_MATHEMATICS_FOR_THE_PERPLEXED.md",
        "docs/PRIME_INFORMATION_GEOMETRY.md",
        "docs/PRIME_INFORMATION_TRANSITION.md",
    }
    for finding in math_report["findings"] + math_report.get("rendered_findings", []):
        if finding["path"] in flagship_pages and finding.get("context", "markdown") == "markdown":
            errors.append(f"{finding['path']}: {finding['kind']} at line {finding.get('line', 0)}")
    print(
        f"math typography audit: {math_report['scanned_markdown_files']} files, "
        f"{math_report['scanned_public_markdown_files']} public pages, "
        f"{len(math_report['findings'])} source findings, "
        f"{len(math_report.get('rendered_findings', []))} rendered findings; "
        "full inventory in site/math-typography-audit.json"
    )
    print("math typography findings by class:",
          json.dumps(math_report["findings_by_kind_and_context"], sort_keys=True))
    print("math typography top ordinary Markdown paths:",
          json.dumps(math_report["top_markdown_paths"][:12]))
    print("MkDocs rendered math findings:",
          json.dumps(math_report.get("rendered_findings", [])))
    print("GitHub live GFM render probe:",
          json.dumps(math_report.get("github_render_probe", [])))
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        print(f"rendered documentation validation failed with {len(errors)} error(s)", file=sys.stderr)
        return 1

    print("rendered homepage and CM4 info admonitions passed their HTML checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
