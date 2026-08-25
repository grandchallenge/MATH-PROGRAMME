#!/usr/bin/env python3
"""Compatibility entry point for governed release-trust administration.

Select the named default-branch release-trust profile even when a repository has
additional active branch rulesets for construction or development lanes.
"""
from __future__ import annotations

from typing import Any

import release_trust_admin as admin


def branch_ruleset(client: Any, repository: str) -> dict[str, Any]:
    expected_name = admin.RULESET_NAMES.get(repository)
    if not expected_name:
        raise admin.ReleaseTrustError(f"{repository}: no governed ruleset name is registered")

    listing = client.request("GET", f"/repos/{repository}/rulesets")
    if not isinstance(listing, list):
        raise admin.ReleaseTrustError(f"{repository}: ruleset listing is not a list")

    candidates = [
        item
        for item in listing
        if isinstance(item, dict)
        and item.get("target") == "branch"
        and item.get("enforcement") == "active"
        and item.get("name") == expected_name
    ]
    if len(candidates) != 1:
        raise admin.ReleaseTrustError(
            f"{repository}: expected exactly one active governed branch ruleset named "
            f"{expected_name!r}, found {len(candidates)}"
        )

    ruleset_id = candidates[0].get("id")
    if not ruleset_id:
        raise admin.ReleaseTrustError(
            f"{repository}: governed branch ruleset {expected_name!r} has no id"
        )

    raw = client.request("GET", f"/repos/{repository}/rulesets/{ruleset_id}")
    if not isinstance(raw, dict):
        raise admin.ReleaseTrustError(
            f"{repository}: governed branch ruleset {expected_name!r} is not an object"
        )

    normalized = admin.normalize_ruleset(raw)
    expected_structure = {
        "name": expected_name,
        "target": "branch",
        "enforcement": "active",
        "ref_include": ["~DEFAULT_BRANCH"],
        "ref_exclude": [],
    }
    drift = [
        f"{key}={normalized.get(key)!r}"
        for key, value in expected_structure.items()
        if normalized.get(key) != value
    ]
    if drift:
        raise admin.ReleaseTrustError(
            f"{repository}: governed default-branch ruleset selector rejected structural drift: "
            + ", ".join(drift)
        )
    return raw


def main() -> int:
    admin.branch_ruleset = branch_ruleset
    return admin.main()


if __name__ == "__main__":
    raise SystemExit(main())
