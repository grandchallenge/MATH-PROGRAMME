#!/usr/bin/env python3
"""Validate the repository-wide CI coverage audit and its explicit release blockers."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
AUDIT_PATH = ROOT / "governance/workflow_coverage_audit.json"
SCHEMA_PATH = ROOT / "schemas/workflow_coverage_audit.schema.json"
EXPECTED_AREAS = {
    "GLOBAL-POLICY",
    "CAMPAIGN-REPLAY-DISCOVERY",
    "CI-REACHABILITY",
    "REPOSITORY-TESTS",
    "EXPERIMENT-REACHABILITY",
    "SYMBOLIC-BUDGETS",
    "CROSS-PILLAR-LANES",
    "MATHFORGE-PROVIDER-IMPORTS",
    "MATHSOLVE-ROUTING",
    "FORMAL-REPLAYS",
    "EXTERNAL-MATHCERT-EVIDENCE",
    "STRICT-DOCUMENTATION-BUILD",
    "PAGES-PUBLICATION-CONTRACT",
    "FAST-PATH-WORKFLOWS",
}
EXPECTED_BLOCKERS = {
    "PAGES-CURRENT-MAIN-DEPLOYMENT",
    "PAGES-HOMEPAGE-METADATA",
}


class WorkflowCoverageAuditError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise WorkflowCoverageAuditError(message)


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def validate(root: Path = ROOT) -> None:
    audit = load(root / "governance/workflow_coverage_audit.json")
    schema = load(root / "schemas/workflow_coverage_audit.schema.json")
    errors = sorted(
        Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(audit),
        key=lambda error: list(error.path),
    )
    require(not errors, "; ".join(f"{error.json_path}: {error.message}" for error in errors))

    areas = audit["coverage_areas"]
    area_ids = [area["area_id"] for area in areas]
    require(len(area_ids) == len(set(area_ids)), "workflow coverage audit has duplicate area IDs")
    require(set(area_ids) == EXPECTED_AREAS, "workflow coverage area set drift")

    blockers = audit["remaining_blockers"]
    blocker_ids = [blocker["blocker_id"] for blocker in blockers]
    require(len(blocker_ids) == len(set(blocker_ids)), "workflow coverage audit has duplicate blockers")
    require(set(blocker_ids) == EXPECTED_BLOCKERS, "Pages blocker set drift")
    require(all(blocker["issue"] == 7 for blocker in blockers), "all remaining blockers must be scoped to issue #7")
    require(audit["umbrella_issue_disposition"] == "KEEP_OPEN", "issue #6 must remain open while Pages blockers exist")

    for required in (
        ".github/workflows/ci.yml",
        ".github/workflows/pages.yml",
        "ci/validate_workflow_semantics.py",
        "ci/validate_policy_reachability.py",
        "ci/validate_repository_execution.py",
        "ci/validate_symbolic_resource_budgets.py",
        "ci/validate_cross_pillar_lane_packages.py",
    ):
        require((root / required).is_file(), f"audited workflow control is missing: {required}")


def main() -> int:
    try:
        validate()
    except (WorkflowCoverageAuditError, OSError, json.JSONDecodeError) as exc:
        print(f"workflow coverage audit rejected: {exc}", file=sys.stderr)
        return 1
    print("workflow coverage audit checked: CI contracts complete; Pages operational blockers explicit")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
