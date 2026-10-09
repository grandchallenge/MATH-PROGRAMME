#!/usr/bin/env python3
"""Validate the built MkDocs homepage for visible Markdown leakage."""
from __future__ import annotations

import argparse
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

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



class CondensedChapterParser(InfoAdmonitionParser):
    """Inspect the built explainer for accessible figures and typeset mathematics."""

    def __init__(self) -> None:
        super().__init__()
        self.math_nodes = 0
        self.figure_images = 0
        self.figure_alt_missing = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        super().handle_starttag(tag, attrs)
        attributes = dict(attrs)
        classes = set((attributes.get("class") or "").split())
        if "arithmatex" in classes:
            self.math_nodes += 1
        if tag == "img" and "condensed-profinite-partitions.svg" in (
            attributes.get("src") or ""
        ):
            self.figure_images += 1
            if not (attributes.get("alt") or "").strip():
                self.figure_alt_missing = True


def condensed_chapter_render_errors(page_html: Path) -> list[str]:
    """Guard math/figure rendering, not merely the existence of Markdown source."""
    if not page_html.is_file():
        return [f"built condensed-mathematics chapter is missing: {page_html}"]
    parser = CondensedChapterParser()
    parser.feed(page_html.read_text(encoding="utf-8"))
    visible = parser.text()
    errors: list[str] = []
    for title in (
        "Condensed Mathematics for the Perplexed",
        "The difficulty: topology and algebra pull in different directions",
        "A condensed set: the precise definition",
        "The GCL CM4 result: a clearly marked landing point",
    ):
        if title not in visible:
            errors.append(f"condensed chapter missing rendered section: {title}")
    if parser.math_nodes < 12:
        errors.append(
            f"condensed chapter has too few Arithmatex math nodes: {parser.math_nodes}"
        )
    if parser.figure_images != 1:
        errors.append(
            f"condensed chapter expected one accessible partition diagram, found {parser.figure_images}"
        )
    if parser.figure_alt_missing:
        errors.append("condensed chapter partition diagram is missing alternative text")
    if parser.info_boxes < 1:
        errors.append("condensed chapter status admonition did not render")
    for label, pattern in VISIBLE_MARKDOWN_PATTERNS:
        match = pattern.search(visible)
        if match:
            errors.append(f"condensed chapter exposes {label}: {match.group(0)!r}")
    return errors


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
    errors.extend(condensed_chapter_render_errors(
        site_dir / "CONDENSED_MATHEMATICS_FOR_THE_PERPLEXED" / "index.html"
    ))
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        print(f"rendered documentation validation failed with {len(errors)} error(s)", file=sys.stderr)
        return 1

    print("rendered homepage, CM4 admonitions, and condensed explainer passed their HTML checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
