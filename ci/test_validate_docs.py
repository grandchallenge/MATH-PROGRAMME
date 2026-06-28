#!/usr/bin/env python3
"""Regression tests for documentation coherence checks."""
from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory

from validate_docs import rendered_h1_count, strip_frontmatter, without_fenced_blocks


def main() -> int:
    assert strip_frontmatter("---\nhide:\n  - toc\n---\n# Title") == "# Title"
    assert "inside" not in without_fenced_blocks("before\n```text\n# inside\n```\nafter")

    with TemporaryDirectory() as directory:
        path = Path(directory) / "page.md"
        path.write_text("# Title\n\n## Subtitle\n", encoding="utf-8")
        assert rendered_h1_count(path) == 1
        path.write_text("# Title\n\n<h1>Duplicate</h1>\n", encoding="utf-8")
        assert rendered_h1_count(path) == 2

    print("documentation validator rejection tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
