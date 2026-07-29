#!/usr/bin/env python3
"""Validate the executable Groebner application portfolio."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from validate_symbolic_resource_budgets import (
    SymbolicBudgetError,
    validate as validate_symbolic_budgets,
    validate_lane,
)

MANIFEST = Path("applications/grobner_manifest.json")
EXPECTED_LANES = {
    "APP-DIO-01",
    "APP-GEO-02",
    "APP-SIG-03",
    "APP-ROB-04",
    "APP-SDK-05",
    "APP-REC-06",
}
EXPECTED_FOUNDATIONS = {"UF-INV-001", "RAD-NIL-002"}
ALLOWED_STATUSES = {"next_fixture", "queued"}


class ManifestError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ManifestError(message)


def nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate(path: Path = MANIFEST) -> None:
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ManifestError(f"{path}: cannot load manifest: {exc}") from exc

    require(isinstance(manifest, dict), "manifest must be an object")
    require(manifest.get("schema_version") == "2.0.0", "unsupported schema version")
    require(nonempty(manifest.get("governing_rule")), "governing rule is required")

    foundations = manifest.get("foundation_fixtures")
    require(isinstance(foundations, list), "foundation_fixtures must be a list")
    foundation_ids = {
        item.get("fixture_id")
        for item in foundations
        if isinstance(item, dict)
        and item.get("status") == "merged_ci_enforced"
        and nonempty(item.get("capability"))
    }
    require(foundation_ids == EXPECTED_FOUNDATIONS, "both checked foundation fixtures are required")

    lanes = manifest.get("lanes")
    require(isinstance(lanes, list) and len(lanes) == 6, "manifest must contain exactly six lanes")
    by_id = {lane.get("lane_id"): lane for lane in lanes if isinstance(lane, dict)}
    require(len(by_id) == len(lanes), "lane IDs must be unique")
    require(set(by_id) == EXPECTED_LANES, "application lane set changed")

    selected = []
    for lane_id, lane in by_id.items():
        status = lane.get("status")
        require(status in ALLOWED_STATUSES, f"{lane_id}: invalid status")
        if status == "next_fixture":
            selected.append(lane_id)
        for field in (
            "name",
            "source_object",
            "local_obligation",
            "excluded_inference",
            "first_fixture",
            "switch_condition",
        ):
            require(nonempty(lane.get(field)), f"{lane_id}: {field} is required")
        route = lane.get("certificate_route")
        require(
            isinstance(route, list)
            and len(route) >= 3
            and all(nonempty(step) for step in route),
            f"{lane_id}: certificate_route requires at least three nonempty steps",
        )
        require(
            lane["local_obligation"] != lane["excluded_inference"],
            f"{lane_id}: obligation and excluded inference must be distinct",
        )
        try:
            validate_lane(lane, path.as_posix())
        except SymbolicBudgetError as exc:
            raise ManifestError(str(exc)) from exc

    require(len(selected) == 1, "exactly one lane must be selected as next_fixture")
    require(
        manifest.get("next_fixture_lane") == selected[0] == "APP-GEO-02",
        "automated geometry must remain the selected next fixture",
    )


def main() -> int:
    try:
        validate()
        validate_symbolic_budgets()
    except (ManifestError, SymbolicBudgetError) as exc:
        print(f"application manifest rejected: {exc}", file=sys.stderr)
        return 1
    print("application manifest checked: six bounded lanes, one selected next fixture")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
