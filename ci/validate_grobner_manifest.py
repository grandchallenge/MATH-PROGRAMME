#!/usr/bin/env python3
"""Validate the executable Groebner application portfolio."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

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
BUDGET_INTEGER_FIELDS = (
    "max_variables",
    "max_total_degree",
    "max_runtime_seconds",
    "max_basis_elements",
    "max_intermediate_terms",
)
BUDGET_TEXT_FIELDS = (
    "monomial_order",
    "backend",
    "backend_version",
    "fallback_route",
)
FAILURE_STATUSES = {
    "timeout",
    "degree_explosion",
    "basis_size_explosion",
    "memory_exhaustion",
    "unstable_modular_reconstruction",
    "unsuitable_monomial_order",
    "side_conditions_missing",
    "not_actually_algebraic",
    "cancelled_by_budget",
}


class ManifestError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ManifestError(message)


def nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_budget(lane_id: str, budget: Any) -> None:
    require(isinstance(budget, dict), f"{lane_id}: resource_budget must be an object")
    for field in BUDGET_INTEGER_FIELDS:
        value = budget.get(field)
        require(
            isinstance(value, int) and not isinstance(value, bool) and value > 0,
            f"{lane_id}: resource_budget.{field} must be a positive integer",
        )
    for field in BUDGET_TEXT_FIELDS:
        require(nonempty(budget.get(field)), f"{lane_id}: resource_budget.{field} is required")


def validate_ledger(lane_id: str, ledger: Any) -> None:
    require(isinstance(ledger, dict), f"{lane_id}: run_ledger must be an object")
    execution = ledger.get("execution_status")
    termination = ledger.get("termination_status")
    failure = ledger.get("failure_status")
    failure_record = ledger.get("failure_record")
    result_artifact = ledger.get("result_artifact")
    recorded_at = ledger.get("recorded_at")
    require(execution in {"not_started", "completed", "failed"}, f"{lane_id}: invalid execution_status")
    if execution == "not_started":
        require(termination == "not_started", f"{lane_id}: unstarted lane has invalid termination_status")
        require(failure is None and failure_record is None, f"{lane_id}: unstarted lane cannot carry failure evidence")
        require(result_artifact is None and recorded_at is None, f"{lane_id}: unstarted lane cannot carry execution evidence")
    elif execution == "completed":
        require(termination == "success", f"{lane_id}: completed lane must terminate with success")
        require(failure is None and failure_record is None, f"{lane_id}: completed lane cannot carry failure evidence")
        require(nonempty(result_artifact), f"{lane_id}: completed lane requires result_artifact")
        require(nonempty(recorded_at), f"{lane_id}: completed lane requires recorded_at")
    else:
        require(termination in FAILURE_STATUSES, f"{lane_id}: failed lane needs controlled termination_status")
        require(failure == termination, f"{lane_id}: failure_status must equal termination_status")
        require(nonempty(failure_record), f"{lane_id}: failed lane requires failure_record")
        require(result_artifact is None, f"{lane_id}: failed lane cannot claim result_artifact")
        require(nonempty(recorded_at), f"{lane_id}: failed lane requires recorded_at")


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
            isinstance(route, list) and len(route) >= 3 and all(nonempty(step) for step in route),
            f"{lane_id}: certificate_route requires at least three nonempty steps",
        )
        require(lane["local_obligation"] != lane["excluded_inference"], f"{lane_id}: obligation and excluded inference must be distinct")
        require(lane.get("lane_class") == "expensive_symbolic", f"{lane_id}: lane_class must be expensive_symbolic")
        validate_budget(lane_id, lane.get("resource_budget"))
        validate_ledger(lane_id, lane.get("run_ledger"))

    require(len(selected) == 1, "exactly one lane must be selected as next_fixture")
    require(
        manifest.get("next_fixture_lane") == selected[0] == "APP-GEO-02",
        "automated geometry must remain the selected next fixture",
    )


def main() -> int:
    try:
        validate()
    except ManifestError as exc:
        print(f"application manifest rejected: {exc}", file=sys.stderr)
        return 1
    print("application manifest checked: six bounded lanes, one selected next fixture")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
