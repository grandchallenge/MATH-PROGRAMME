#!/usr/bin/env python3
"""Adversarial rejection tests for retired repository paths."""
from __future__ import annotations

import copy

from validate_retired_paths import (
    POLICY_MARKERS,
    REFERENCE_MARKERS,
    RETIRED_PATH,
    ROOT,
    repository_texts,
    retired_path_errors,
)


def main() -> int:
    texts = repository_texts(ROOT)
    policy_text = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    assert not retired_path_errors(texts=texts, policy_text=policy_text)

    rogue_reference = copy.deepcopy(texts)
    rogue_reference["docs/rogue.md"] = f"Current artifact: `{RETIRED_PATH}`."
    assert any(
        "ungoverned reference to retired path" in error
        for error in retired_path_errors(texts=rogue_reference, policy_text=policy_text)
    )

    missing_marker = copy.deepcopy(texts)
    manifest = "FILE_MANIFEST.md"
    missing_marker[manifest] = missing_marker[manifest].replace(
        REFERENCE_MARKERS[manifest], "is retained in the current tree", 1
    )
    assert any(
        "missing retirement marker" in error
        for error in retired_path_errors(texts=missing_marker, policy_text=policy_text)
    )

    missing_identity = copy.deepcopy(texts)
    repository_docs = "docs/REPOSITORY_DOCS.md"
    missing_identity[repository_docs] = missing_identity[repository_docs].replace(
        RETIRED_PATH, "DOMAIN_04_POINCARE_ALIAS.md", 1
    )
    assert any(
        "missing retired path identity" in error
        for error in retired_path_errors(texts=missing_identity, policy_text=policy_text)
    )

    missing_policy_check = policy_text.replace(POLICY_MARKERS[0], "python3 -c 'pass'", 1)
    assert any(
        "global policy is missing retired-path check" in error
        for error in retired_path_errors(texts=texts, policy_text=missing_policy_check)
    )

    print("retired-path rejection tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
