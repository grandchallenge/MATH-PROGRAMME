#!/usr/bin/env python3
"""Regression tests for rendered-homepage validation."""
from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory

from validate_rendered_docs import homepage_render_errors


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

        missing = root / "missing.html"
        assert homepage_render_errors(missing) == [f"built homepage is missing: {missing}"]

    print("rendered documentation validator rejection tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
