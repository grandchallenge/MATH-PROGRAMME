#!/usr/bin/env python3
"""Regression tests for rendered-homepage validation."""
from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory

from validate_rendered_docs import (
    admonition_render_errors,
    condensed_chapter_render_errors,
    homepage_render_errors,
)


def main() -> int:
    with TemporaryDirectory() as directory:
        root = Path(directory)
        index = root / "index.html"

        index.write_text(
            """<!doctype html><html><body>
            <h1>Mathematics Programme</h1>
            <h2>What the programme is</h2>
            <h2>How a claim moves</h2>
            <h2>Current frontier</h2>
            <h2>Where to go next</h2>
            <h2>Claim boundary</h2>
            </body></html>""",
            encoding="utf-8",
        )
        assert not homepage_render_errors(index)

        index.write_text(
            """<!doctype html><html><body>
            <h1>Mathematics Programme</h1>
            <h2>What the programme is</h2>
            <h2>How a claim moves</h2>
            <h2>Current frontier</h2>
            <h2>Where to go next</h2>
            <h2>Claim boundary</h2>
            <p>### BSD-001</p>
            <p>**Status:** active</p>
            <p>| --- | --- |</p>
            </body></html>""",
            encoding="utf-8",
        )
        errors = homepage_render_errors(index)
        assert any("ATX heading marker" in error for error in errors)
        assert any("Markdown emphasis marker" in error for error in errors)
        assert any("Markdown table separator" in error for error in errors)

        cm4_page = root / "CMDG_CM4" / "index.html"
        cm4_page.parent.mkdir(parents=True)
        cm4_page.write_text(
            '<html><body><div class="admonition info">'
            '<p class="admonition-title">Research surface authority</p>'
            '<p>Protected mathematical claims</p></div></body></html>',
            encoding="utf-8",
        )
        assert not admonition_render_errors(cm4_page, "Research surface authority")

        cm4_page.write_text(
            '<html><body><p>!!! info "Research surface authority"</p>'
            '<p>Protected mathematical claims</p></body></html>',
            encoding="utf-8",
        )
        errors = admonition_render_errors(cm4_page, "Research surface authority")
        assert any("literal !!! info" in error for error in errors)
        assert any("no rendered info admonition" in error for error in errors)

        cm4_page.write_text(
            '<html><body><p>Research surface authority</p></body></html>',
            encoding="utf-8",
        )
        assert any(
            "no rendered info admonition" in error
            for error in admonition_render_errors(cm4_page, "Research surface authority")
        )

        missing_admonition_page = root / "CMDG_CM4_RESEARCH_GUIDE" / "index.html"
        assert admonition_render_errors(
            missing_admonition_page, "Live work is issue-led"
        ) == [f"built admonition page is missing: {missing_admonition_page}"]

        chapter = root / "CONDENSED_MATHEMATICS_FOR_THE_PERPLEXED" / "index.html"
        chapter.parent.mkdir(parents=True)
        headings = "".join(
            f"<h2>{heading}</h2>" for heading in (
                "Condensed Mathematics for the Perplexed",
                "The difficulty: topology and algebra pull in different directions",
                "A condensed set: the precise definition",
                "The GCL CM4 result: a clearly marked landing point",
            )
        )
        math_nodes = "".join(
            '<span class="arithmatex">\\(x+y\\)</span>'
            for _ in range(15)
        )
        figure = (
            '<img src="../assets/condensed-profinite-partitions.svg" '
            'alt="Binary refinement diagram">'
        )
        info = '<div class="admonition info">Introductory status</div>'
        chapter.write_text(
            f"<html><body>{headings}{math_nodes}{figure}{info}</body></html>",
            encoding="utf-8",
        )
        assert not condensed_chapter_render_errors(chapter)

        chapter.write_text(
            f"<html><body>{headings}{figure}{info}</body></html>",
            encoding="utf-8",
        )
        assert any("Arithmatex math nodes" in error
                   for error in condensed_chapter_render_errors(chapter))

        chapter.write_text(
            f'<html><body>{headings}{math_nodes}'
            '<img src="../assets/condensed-profinite-partitions.svg" '
            'alt="">{info}</body></html>',
            encoding="utf-8",
        )
        errors = condensed_chapter_render_errors(chapter)
        assert any("missing alternative text" in error for error in errors)

        missing = root / "missing.html"
        assert homepage_render_errors(missing) == [f"built homepage is missing: {missing}"]

    print("rendered documentation validator rejection tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
