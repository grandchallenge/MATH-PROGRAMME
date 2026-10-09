#!/usr/bin/env python3
"""Regression tests for rendered-homepage validation."""
from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory

from validate_rendered_docs import admonition_render_errors, homepage_render_errors
from audit_math_typography import source_issues, source_math_count, rendered_issues


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

        missing = root / "missing.html"
        assert homepage_render_errors(missing) == [f"built homepage is missing: {missing}"]

    # Math source checks distinguish prose from code, and inspect built HTML.
    with TemporaryDirectory() as directory:
        root = Path(directory)
        docs = root / "docs"
        docs.mkdir()
        note = docs / "note.md"
        note.write_text(
            "# Note\n\nInline $x^2$ and displayed:\n\n$\n x^2+y^2=z^2\n$\n"
            "\n" + chr(96) * 3 + "tex\n"
            "\\operatorname{ThisIsCode}\n"
            + chr(96) * 3 + "\n",
            encoding="utf-8",
        )
        assert source_math_count(note) == 2
        assert not source_issues(note, root)
        note.write_text(
            "original derived-$\\mathrm{RHom}$ and \\(x\\) "
            "$\\operatorname{rank}$.\n",
            encoding="utf-8",
        )
        kinds = {f["kind"] for f in source_issues(note, root)}
        assert "math-prose-adjacency" in kinds
        assert "legacy-inline-delimiter" in kinds
        assert "github-unsupported-operatorname" in kinds

        note.write_text("An equation $x$ and $y^2$.\n", encoding="utf-8")
        site = root / "site"
        built = site / "note" / "index.html"
        built.parent.mkdir(parents=True)
        built.write_text('<span class="arithmatex">x</span>', encoding="utf-8")
        checked, failures = rendered_issues(root, site)
        assert checked == 1
        assert failures and failures[0]["kind"] == "arithmatex-wrapper-shortfall"
        built.write_text(
            '<span class="arithmatex">x</span><div class="arithmatex">y</div>',
            encoding="utf-8",
        )
        assert rendered_issues(root, site) == (1, [])

    print("rendered documentation validator rejection tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
