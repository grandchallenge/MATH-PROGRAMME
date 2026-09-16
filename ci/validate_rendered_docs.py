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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--site-dir",
        default=str(ROOT / "site"),
        help="MkDocs output directory; defaults to repository site/",
    )
    args = parser.parse_args()

    errors = homepage_render_errors(Path(args.site_dir) / "index.html")
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        print(f"rendered documentation validation failed with {len(errors)} error(s)", file=sys.stderr)
        return 1

    print("rendered homepage contains no visible Markdown leakage and all front-door sections are present")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
