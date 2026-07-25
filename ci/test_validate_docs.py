#!/usr/bin/env python3
"""Regression tests for documentation navigation, authority, and coverage checks."""
from __future__ import annotations

import copy
from pathlib import Path
from tempfile import TemporaryDirectory

import yaml

from validate_docs import (
    ROOT,
    authority_contract_errors,
    domain_contract_errors,
    local_link_targets,
    nav_documents,
    rendered_h1_count,
    strip_frontmatter,
    without_fenced_blocks,
)


def main() -> int:
    assert strip_frontmatter("---\nhide:\n  - toc\n---\n# Title") == "# Title"
    assert "inside" not in without_fenced_blocks("before\n```text\n# inside\n```\nafter")
    assert local_link_targets('[Page](page.md) <a href="other.md#section">Other</a>') == [
        "page.md",
        "other.md#section",
    ]

    with TemporaryDirectory() as directory:
        path = Path(directory) / "page.md"
        path.write_text("# Title\n\n## Subtitle\n", encoding="utf-8")
        assert rendered_h1_count(path) == 1
        path.write_text("# Title\n\n<h1>Duplicate</h1>\n", encoding="utf-8")
        assert rendered_h1_count(path) == 2

    registry = yaml.safe_load((ROOT / "DOMAIN_REGISTRY.yaml").read_text(encoding="utf-8"))
    nav = nav_documents()
    assert not domain_contract_errors(registry, nav)
    assert not authority_contract_errors()

    duplicate_number = copy.deepcopy(registry)
    duplicate_number["domains"][1]["programme_number"] = duplicate_number["domains"][0][
        "programme_number"
    ]
    assert any(
        "duplicate programme_number" in error
        for error in domain_contract_errors(duplicate_number, nav)
    )

    missing_public_page = copy.deepcopy(registry)
    missing_public_page["domains"][0]["public_page"] = "docs/domains/missing.md"
    assert any(
        "public_page must be" in error or "public page is missing" in error
        for error in domain_contract_errors(missing_public_page, nav)
    )

    missing_adr = copy.deepcopy(registry)
    missing_adr["domains"][0]["governance_refs"] = ["ADR-9999"]
    assert any(
        "does not resolve uniquely" in error
        for error in domain_contract_errors(missing_adr, nav)
    )

    print("documentation validator rejection tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
