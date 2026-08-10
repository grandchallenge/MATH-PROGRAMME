#!/usr/bin/env python3
"""Adversarial rejection tests for retired repository paths."""
from __future__ import annotations

import copy

from validate_retired_paths import (
    POLICY_MARKERS,
    REFERENCE_MARKERS,
    RETIRED_PATH,
    ROOT,
    load_crosswalk,
    load_policy_registry,
    repository_texts,
    retired_path_errors,
)


def remove_policy_command(registry: dict, marker: str) -> dict:
    mutated = copy.deepcopy(registry)
    parts = marker.split()
    for entries in mutated.get("shards", {}).values():
        if parts in entries:
            entries.remove(parts)
            return mutated
    raise AssertionError(f"policy command not found in registry: {marker}")


def main() -> int:
    texts = repository_texts(ROOT)
    crosswalk = load_crosswalk(ROOT)
    policy_registry = load_policy_registry(ROOT)
    policy_text = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    assert not retired_path_errors(
        texts=texts,
        policy_text=policy_text,
        crosswalk=crosswalk,
        policy_registry=policy_registry,
    )

    rogue_reference = copy.deepcopy(texts)
    rogue_reference["docs/rogue.md"] = f"Current artifact: `{RETIRED_PATH}`."
    assert any(
        "ungoverned reference to retired path" in error
        for error in retired_path_errors(
            texts=rogue_reference,
            policy_text=policy_text,
            crosswalk=crosswalk,
            policy_registry=policy_registry,
        )
    )

    missing_marker = copy.deepcopy(texts)
    manifest = "FILE_MANIFEST.md"
    missing_marker[manifest] = missing_marker[manifest].replace(
        REFERENCE_MARKERS[manifest], "is retained in the current tree", 1
    )
    assert any(
        "missing retirement marker" in error
        for error in retired_path_errors(
            texts=missing_marker,
            policy_text=policy_text,
            crosswalk=crosswalk,
            policy_registry=policy_registry,
        )
    )

    missing_adr_marker = copy.deepcopy(texts)
    adr = "docs/decisions/ADR-0011_FULL_WORKFLOW_COVERAGE.md"
    missing_adr_marker[adr] = missing_adr_marker[adr].replace(
        REFERENCE_MARKERS[adr], "the legacy alias was noted", 1
    )
    assert any(
        "missing retirement marker" in error
        for error in retired_path_errors(
            texts=missing_adr_marker,
            policy_text=policy_text,
            crosswalk=crosswalk,
            policy_registry=policy_registry,
        )
    )

    missing_identity = copy.deepcopy(texts)
    repository_docs = "docs/REPOSITORY_DOCS.md"
    missing_identity[repository_docs] = missing_identity[repository_docs].replace(
        RETIRED_PATH, "DOMAIN_04_POINCARE_ALIAS.md", 1
    )
    assert any(
        "missing retired path identity" in error
        for error in retired_path_errors(
            texts=missing_identity,
            policy_text=policy_text,
            crosswalk=crosswalk,
            policy_registry=policy_registry,
        )
    )

    duplicate_crosswalk = copy.deepcopy(crosswalk)
    duplicate_crosswalk["references"].append(
        copy.deepcopy(duplicate_crosswalk["references"][0])
    )
    assert any(
        "duplicate path" in error
        for error in retired_path_errors(
            texts=texts,
            policy_text=policy_text,
            crosswalk=duplicate_crosswalk,
            policy_registry=policy_registry,
        )
    )

    bad_relation = copy.deepcopy(crosswalk)
    bad_relation["references"][0]["relation"] = "current_authority"
    assert any(
        "unsupported historical identity relation" in error
        for error in retired_path_errors(
            texts=texts,
            policy_text=policy_text,
            crosswalk=bad_relation,
            policy_registry=policy_registry,
        )
    )

    missing_crosswalk_marker = copy.deepcopy(texts)
    target = crosswalk["references"][0]
    missing_crosswalk_marker[target["path"]] = missing_crosswalk_marker[
        target["path"]
    ].replace(target["required_marker"], "alias retained", 1)
    assert any(
        "crosswalk target is missing required marker" in error
        for error in retired_path_errors(
            texts=missing_crosswalk_marker,
            policy_text=policy_text,
            crosswalk=crosswalk,
            policy_registry=policy_registry,
        )
    )

    missing_policy_route = remove_policy_command(policy_registry, POLICY_MARKERS[0])
    assert any(
        "global policy is missing retired-path check" in error
        for error in retired_path_errors(
            texts=texts,
            policy_text=policy_text,
            crosswalk=crosswalk,
            policy_registry=missing_policy_route,
        )
    )

    missing_policy_test_route = remove_policy_command(policy_registry, POLICY_MARKERS[1])
    assert any(
        "global policy is missing retired-path check" in error
        for error in retired_path_errors(
            texts=texts,
            policy_text=policy_text,
            crosswalk=crosswalk,
            policy_registry=missing_policy_test_route,
        )
    )

    print("retired-path and historical-identity rejection tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
