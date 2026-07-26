#!/usr/bin/env python3
"""Adversarial rejection tests for retired repository paths."""
from __future__ import annotations

import copy

from validate_retired_paths import (
    REFERENCE_MARKERS,
    RETIRED_PATH,
    ROOT,
    repository_texts,
    retired_path_errors,
)


def main() -> int:
    texts = repository_texts(ROOT)
    assert not retired_path_errors(texts=texts)

    rogue_reference = copy.deepcopy(texts)
    rogue_reference["docs/rogue.md"] = f"Current artifact: `{RETIRED_PATH}`."
    assert any(
        "ungoverned reference to retired path" in error
        for error in retired_path_errors(texts=rogue_reference)
    )

    missing_marker = copy.deepcopy(texts)
    manifest = "FILE_MANIFEST.md"
    missing_marker[manifest] = missing_marker[manifest].replace(
        REFERENCE_MARKERS[manifest], "is retained in the current tree", 1
    )
    assert any(
        "missing retirement marker" in error
        for error in retired_path_errors(texts=missing_marker)
    )

    missing_identity = copy.deepcopy(texts)
    repository_docs = "docs/REPOSITORY_DOCS.md"
    missing_identity[repository_docs] = missing_identity[repository_docs].replace(
        RETIRED_PATH, "DOMAIN_04_POINCARE_ALIAS.md", 1
    )
    assert any(
        "missing retired path identity" in error
        for error in retired_path_errors(texts=missing_identity)
    )

    print("retired-path rejection tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
