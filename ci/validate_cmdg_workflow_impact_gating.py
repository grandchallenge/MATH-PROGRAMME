#!/usr/bin/env python3
"""Fail-closed validator for MP-CMDG-WORKFLOW-IMPACT-GATING-001."""
from __future__ import annotations

import fnmatch
import json
import sys
from pathlib import Path
from typing import Any

import jsonschema
import yaml

ROOT = Path(__file__).resolve().parents[1]
CONTROL = ROOT / "governance/cmdg_workflow_impact_gating.json"
SCHEMA = ROOT / "schemas/cmdg_workflow_impact_gating.schema.json"
WORKFLOW_DIR = ROOT / ".github/workflows"


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected object: {path}")
    return value


def load_workflow_texts() -> dict[str, str]:
    return {
        path.name: path.read_text(encoding="utf-8")
        for path in sorted(WORKFLOW_DIR.glob("cmdg-*.yml"))
    }


def path_matches(path: str, patterns: list[str]) -> bool:
    return any(fnmatch.fnmatchcase(path, pattern) for pattern in patterns)


def _as_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value]
    if value is None:
        return []
    return [str(value)]


def validation_errors(
    control: dict[str, Any] | None = None,
    workflow_texts: dict[str, str] | None = None,
) -> list[str]:
    errors: list[str] = []
    try:
        control = load_json(CONTROL) if control is None else control
        jsonschema.validate(control, load_json(SCHEMA))
    except (OSError, ValueError, json.JSONDecodeError, jsonschema.ValidationError) as exc:
        return [f"control/schema invalid: {exc}"]

    if control.get("control_id") != "MP-CMDG-WORKFLOW-IMPACT-GATING-001":
        errors.append("control identity drift")
    if control.get("status") != "ACTIVE_ON_PROTECTED_MERGE":
        errors.append("control status drift")

    paths = control.get("pull_request_paths")
    if not isinstance(paths, list) or not paths or not all(isinstance(x, str) and x for x in paths):
        errors.append("pull_request_paths must be a nonempty string list")
        paths = []

    texts = load_workflow_texts() if workflow_texts is None else workflow_texts
    expected = sorted(str(x) for x in control.get("workflow_roster", []))
    actual = sorted(texts)
    if actual != expected:
        errors.append(f"standalone CMDG workflow roster drift: expected={expected} actual={actual}")

    for name in expected:
        text = texts.get(name)
        if text is None:
            continue
        try:
            workflow = yaml.load(text, Loader=yaml.BaseLoader)
        except yaml.YAMLError as exc:
            errors.append(f"{name}: invalid YAML: {exc}")
            continue
        if not isinstance(workflow, dict):
            errors.append(f"{name}: workflow root must be a mapping")
            continue
        trigger = workflow.get("on")
        if not isinstance(trigger, dict):
            errors.append(f"{name}: on trigger must be a mapping")
            continue
        pr = trigger.get("pull_request")
        if not isinstance(pr, dict) or _as_list(pr.get("paths")) != paths:
            errors.append(f"{name}: pull_request paths must equal the governed shared closure")
        push = trigger.get("push")
        if not isinstance(push, dict) or "main" not in _as_list(push.get("branches")):
            errors.append(f"{name}: push trigger must preserve main")
        if "workflow_dispatch" not in trigger:
            errors.append(f"{name}: workflow_dispatch trigger missing")

    for path in control.get("negative_examples", []):
        if path_matches(str(path), paths):
            errors.append(f"negative example unexpectedly matches CMDG gate: {path}")
    for path in control.get("positive_examples", []):
        if not path_matches(str(path), paths):
            errors.append(f"positive example does not match CMDG gate: {path}")

    routing = control.get("routing_boundary", {})
    if routing.get("unrelated_pr_standalone_cmdg_instantiation") is not False:
        errors.append("unrelated PR standalone CMDG instantiation must remain false")
    if routing.get("cmdg_relevant_pr_full_standalone_family") is not True:
        errors.append("CMDG-relevant PR full-family fanout must remain true")
    if routing.get("within_cmdg_lane_reduction") is not False:
        errors.append("Phase 1 may not reduce within-CMDG lane fanout")
    if routing.get("protected_required_check_identity_changed") is not False:
        errors.append("protected required check identity may not change")

    authority = control.get("authority_boundary", {})
    if any(value is not False for value in authority.values()):
        errors.append("authority boundary weakened")
    return errors


def main() -> int:
    errors = validation_errors()
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        print(f"CMDG workflow impact gating failed with {len(errors)} error(s)", file=sys.stderr)
        return 1
    print(
        "CMDG workflow impact gating: exact roster, shared conservative PR closure, "
        "unconditional protected-main push, manual dispatch, and authority boundaries are valid"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
