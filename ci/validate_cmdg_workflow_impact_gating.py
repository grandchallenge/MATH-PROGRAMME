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
        if path.name != "cmdg-postmerge.yml"
    }


def load_dispatcher_text() -> str:
    return (WORKFLOW_DIR / "cmdg-postmerge.yml").read_text(encoding="utf-8")


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
    dispatcher_text: str | None = None,
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
        if "push" in trigger:
            errors.append(f"{name}: direct push trigger must be absent; protected pushes route through dispatcher")
        if "workflow_call" not in trigger:
            errors.append(f"{name}: workflow_call trigger missing")
        if "workflow_dispatch" not in trigger:
            errors.append(f"{name}: workflow_dispatch trigger missing")

    try:
        dispatcher_text = load_dispatcher_text() if dispatcher_text is None else dispatcher_text
        dispatcher = yaml.load(dispatcher_text, Loader=yaml.BaseLoader)
        trigger = dispatcher.get("on", {}) if isinstance(dispatcher, dict) else {}
        push = trigger.get("push", {}) if isinstance(trigger, dict) else {}
        if "main" not in _as_list(push.get("branches")) or push.get("paths") is not None:
            errors.append("dispatcher: every protected-main push must reach classifier without native paths")
        schedules = trigger.get("schedule", []) if isinstance(trigger, dict) else []
        crons = [item.get("cron") for item in schedules if isinstance(item, dict)]
        if crons != [control.get("scheduled_current_head_sentinel", {}).get("cron")]:
            errors.append("dispatcher: daily current-head sentinel cron drift")
        if "workflow_dispatch" not in trigger:
            errors.append("dispatcher: workflow_dispatch trigger missing")
        jobs = dispatcher.get("jobs", {}) if isinstance(dispatcher, dict) else {}
        calls = {
            str(job.get("uses", "")).removeprefix("./.github/workflows/")
            for job in jobs.values() if isinstance(job, dict) and "uses" in job
        }
        if calls != set(expected):
            errors.append(f"dispatcher: reusable-workflow roster drift: expected={expected} actual={sorted(calls)}")
        for job_id, job in jobs.items():
            if isinstance(job, dict) and "uses" in job:
                condition = str(job.get("if", ""))
                if "policy_shards" not in condition or "cmdg" not in condition:
                    errors.append(f"dispatcher: {job_id} is not gated by fail-closed CMDG classification")
        for marker in ("ci/policy_impact.py classify", "ci/cmdg_postmerge_readback.py", "Enforce downstream hold"):
            if marker not in dispatcher_text:
                errors.append(f"dispatcher: required marker missing: {marker}")
    except (OSError, yaml.YAMLError, AttributeError) as exc:
        errors.append(f"dispatcher invalid: {exc}")

    for path in control.get("negative_examples", []):
        if path_matches(str(path), paths):
            errors.append(f"negative example unexpectedly matches CMDG gate: {path}")
    for path in control.get("positive_examples", []):
        if not path_matches(str(path), paths):
            errors.append(f"positive example does not match CMDG gate: {path}")

    routing = control.get("routing_boundary", {})
    if routing.get("unrelated_pr_standalone_cmdg_instantiation") is not False:
        errors.append("unrelated PR standalone CMDG instantiation must remain false")
    if routing.get("unrelated_main_push_standalone_cmdg_instantiation") is not False:
        errors.append("unrelated main-push standalone CMDG instantiation must remain false")
    if routing.get("cmdg_relevant_pr_full_standalone_family") is not True:
        errors.append("CMDG-relevant PR full-family fanout must remain true")
    if routing.get("cmdg_relevant_main_push_full_standalone_family") is not True:
        errors.append("CMDG-relevant main-push full-family fanout must remain true")
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
        "CMDG workflow impact gating: exact reusable roster, conservative PR closure, "
        "always-classified protected pushes, exact-SHA readback, daily current-head sentinel, manual dispatch, and authority boundaries are valid"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
