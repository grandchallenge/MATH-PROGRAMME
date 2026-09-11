#!/usr/bin/env python3
"""Fail-closed validator for CMDG material-closure workflow routing."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import jsonschema
import yaml

import formal_validation as formal

ROOT = Path(__file__).resolve().parents[1]
CONTROL = ROOT / "governance/cmdg_workflow_impact_gating.json"
SCHEMA = ROOT / "schemas/cmdg_workflow_impact_gating.schema.json"
WORKFLOW_DIR = ROOT / ".github/workflows"


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected object: {path}")
    return value


def load_control() -> dict[str, Any]:
    return load_json(CONTROL)


def wrapper_mapping(control: dict[str, Any] | None = None) -> dict[str, str]:
    control = load_control() if control is None else control
    value = control.get("promotion", {}).get("standalone_workflows", {})
    return {str(name): str(lane) for name, lane in value.items()} if isinstance(value, dict) else {}


def load_workflow_texts(control: dict[str, Any] | None = None) -> dict[str, str]:
    return {
        name: (WORKFLOW_DIR / name).read_text(encoding="utf-8")
        for name in sorted(wrapper_mapping(control))
        if (WORKFLOW_DIR / name).is_file()
    }


def load_dispatcher_text() -> str:
    return (WORKFLOW_DIR / "cmdg-postmerge.yml").read_text(encoding="utf-8")


def _trigger(workflow: dict[str, Any]) -> dict[str, Any]:
    value = workflow.get("on", {}) if isinstance(workflow, dict) else {}
    return value if isinstance(value, dict) else {}


def validation_errors(
    control: dict[str, Any] | None = None,
    workflow_texts: dict[str, str] | None = None,
    dispatcher_text: str | None = None,
) -> list[str]:
    errors: list[str] = []
    try:
        control = load_control() if control is None else control
        jsonschema.validate(control, load_json(SCHEMA))
        registry = formal.load_registry(ROOT)
    except (OSError, ValueError, json.JSONDecodeError, jsonschema.ValidationError, formal.FormalValidationError) as exc:
        return [f"control/schema/registry invalid: {exc}"]

    if control["formal_router"]["required_context"] != registry["required_context"]:
        errors.append("formal required context disagrees with lane registry")

    expected = wrapper_mapping(control)
    texts = load_workflow_texts(control) if workflow_texts is None else workflow_texts
    actual_wrapper_files = {
        path.name
        for path in WORKFLOW_DIR.glob("cmdg-*.yml")
        if path.name not in {"cmdg-postmerge.yml", "cmdg-formal-lane-replay.yml"}
    }
    if set(expected) != actual_wrapper_files:
        errors.append(
            f"standalone CMDG workflow roster drift: expected={sorted(expected)} actual={sorted(actual_wrapper_files)}"
        )
    if set(texts) != set(expected):
        errors.append("provided CMDG workflow text roster drift")

    registry_cmdg = {
        lane["promotion_workflow"].removeprefix(".github/workflows/"): lane["id"]
        for lane in registry["lanes"]
        if lane["family"] == "CMDG"
    }
    if expected != registry_cmdg:
        errors.append("CMDG wrapper-to-lane map disagrees with formal lane registry")

    for name, lane in expected.items():
        text = texts.get(name)
        if text is None:
            continue
        try:
            workflow = yaml.load(text, Loader=yaml.BaseLoader)
        except yaml.YAMLError as exc:
            errors.append(f"{name}: invalid YAML: {exc}")
            continue
        trigger = _trigger(workflow)
        if set(trigger) != {"workflow_call", "workflow_dispatch"}:
            errors.append(f"{name}: wrapper triggers must be exactly workflow_call plus workflow_dispatch")
        jobs = workflow.get("jobs", {}) if isinstance(workflow, dict) else {}
        replay = jobs.get("replay", {}) if isinstance(jobs, dict) else {}
        if replay.get("uses") != "./.github/workflows/cmdg-formal-lane-replay.yml":
            errors.append(f"{name}: wrapper must delegate to the shared promotion executor")
        if replay.get("with", {}).get("lane") != lane:
            errors.append(f"{name}: governed lane binding drift")
        for forbidden in ("pull_request:", "push:", "schedule:", "Revalidate protected"):
            if forbidden in text:
                errors.append(f"{name}: forbidden feature-PR/chronological replay marker {forbidden}")

    shared = (WORKFLOW_DIR / "cmdg-formal-lane-replay.yml").read_text(encoding="utf-8")
    if "workflow_call:" not in shared:
        errors.append("shared CMDG executor must be reusable")
    for forbidden in ("pull_request:", "push:", "schedule:"):
        if forbidden in shared:
            errors.append(f"shared CMDG executor has forbidden direct trigger {forbidden}")
    for marker in (
        "ci/formal_validation.py run",
        "--mode promotion",
        "grandchallenge/lean-action@138a564e38a62ce545e8d47d86a97628463aced4",
    ):
        if marker not in shared:
            errors.append(f"shared CMDG executor missing marker: {marker}")

    generic = (WORKFLOW_DIR / "formal-validation.yml").read_text(encoding="utf-8")
    try:
        generic_yaml = yaml.load(generic, Loader=yaml.BaseLoader)
        trigger = _trigger(generic_yaml)
        if not {"pull_request", "merge_group", "schedule", "workflow_dispatch"}.issubset(trigger):
            errors.append("generic formal router trigger set incomplete")
    except yaml.YAMLError as exc:
        errors.append(f"generic formal router invalid YAML: {exc}")
    for marker in (
        "fromJSON(needs.impact.outputs.formal_matrix)",
        "ci/formal_validation.py classify",
        "ci/formal_validation.py run",
        "formal-validation:\n    name: formal-validation",
        "Require exactly the selected substantive lane set",
    ):
        if marker not in generic:
            errors.append(f"generic formal router missing required marker: {marker}")
    for retired_marker in (
        "Bridge legacy required context",
        "Replay LOG-GCD-001 in Lean",
        "Replay PC-WP04 bounded certificate",
        "Replay pinned Union-Closed MATHCERT evidence",
    ):
        if retired_marker in generic:
            errors.append(f"generic formal router retains retired migration marker: {retired_marker}")

    p3 = control["acceptance_examples"]["p3_only"]
    try:
        planned = formal.classify_paths(p3["paths"], registry)
        if planned["lanes"] != p3["expected_lanes"]:
            errors.append(f"P3-only acceptance route drift: {planned['lanes']}")
        unrelated = control["acceptance_examples"]["unrelated"]
        planned = formal.classify_paths(unrelated["paths"], registry)
        if planned["lanes"] != unrelated["expected_lanes"]:
            errors.append(f"unrelated acceptance route drift: {planned['lanes']}")
    except formal.FormalValidationError as exc:
        errors.append(f"acceptance routing failed: {exc}")

    try:
        dispatcher_text = load_dispatcher_text() if dispatcher_text is None else dispatcher_text
        dispatcher = yaml.load(dispatcher_text, Loader=yaml.BaseLoader)
        trigger = _trigger(dispatcher)
        if set(trigger) != {"schedule", "workflow_dispatch"}:
            errors.append("CMDG sentinel triggers must be exactly schedule plus workflow_dispatch")
        crons = [item.get("cron") for item in trigger.get("schedule", []) if isinstance(item, dict)]
        if crons != [control["sentinel"]["cron"]]:
            errors.append("CMDG current-head sentinel cron drift")
        for marker in (
            "family'] == 'CMDG'",
            "ci/formal_validation.py run",
            "--mode sentinel",
            "CMDG_PROTECTED_MAIN_SENTINEL_SUCCEEDED",
        ):
            if marker not in dispatcher_text:
                errors.append(f"CMDG sentinel missing marker: {marker}")
        for forbidden in ("ci/policy_impact.py", "formal_replay_gate.py", "formal_replay_attestation.py"):
            if forbidden in dispatcher_text:
                errors.append(f"CMDG sentinel retains superseded router/attestation marker: {forbidden}")
    except (OSError, yaml.YAMLError, AttributeError) as exc:
        errors.append(f"CMDG sentinel invalid: {exc}")

    routing = control["routing_boundary"]
    if routing != {
        "unrelated_pr_substantive_cmdg_instantiation": False,
        "cmdg_relevant_pr_full_standalone_family": False,
        "within_cmdg_lane_reduction": True,
        "standalone_cmdg_pr_triggers": False,
        "promotion_full_declared_lane_replay_preserved": True,
        "daily_full_cmdg_sentinel_preserved": True,
    }:
        errors.append("CMDG material routing boundary drift")
    if any(value is not False for value in control["authority_boundary"].values()):
        errors.append("authority boundary weakened")
    return errors


def main() -> int:
    errors = validation_errors()
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        print(f"CMDG material routing validation failed with {len(errors)} error(s)", file=sys.stderr)
        return 1
    print(
        "CMDG material routing: feature PRs instantiate only material lanes; standalone workflows are promotion-only; complete protected-main sentinel replay and authority boundaries are preserved"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
