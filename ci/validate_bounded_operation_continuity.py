#!/usr/bin/env python3
"""Validate durable bounded-operation continuity for governed MATH work."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_REL = "governance/bounded_operation_checkpoint_registry.json"
REGISTRY_SCHEMA_REL = "schemas/bounded_operation_checkpoint_registry.schema.json"
CHECKPOINT_SCHEMA_REL = "schemas/bounded_operation_checkpoint.schema.json"
CHECKPOINT_ROOT_REL = "governance/bounded_operation_checkpoints"

LIVE_STATES = {"AUTHORIZED_READY", "IN_PROGRESS", "AWAITING_EXTERNAL_EVIDENCE"}
BLOCKED_STATE = "BLOCKED_GENUINE_BOUNDARY"
TERMINAL_STATE = "TERMINAL"
RECOGNIZED_BOUNDARIES = {
    "governance",
    "authority",
    "authentication",
    "safety",
    "protected-state",
    "materially-changed-state",
    "substantive-evidentiary",
    "recovery-exhaustion",
}
REQUIRED_INSTRUCTION_BINDINGS = {
    "AGENTS.md": (
        "Durable bounded-operation continuity",
        REGISTRY_REL,
        "ci/validate_bounded_operation_continuity.py",
    ),
    "docs/governance/EXECUTION_RECOVERY_OPERATING_GUIDE.md": (
        "Durable checkpoint and session restart",
        REGISTRY_REL,
        "requires_chat_history",
    ),
    "docs/AGENT_COUNCIL_WORK_PACKAGE_CHECKLIST.md": (
        "Bounded-operation continuity gate",
        REGISTRY_REL,
        "fresh_session_safe",
    ),
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def schema_errors(instance: Any, schema_path: Path) -> list[str]:
    validator = Draft202012Validator(load_json(schema_path))
    return [
        f"{error.json_path}: {error.message}"
        for error in sorted(validator.iter_errors(instance), key=lambda item: list(item.path))
    ]


def safe_repo_path(relative: str, root: Path = ROOT) -> Path | None:
    path = Path(relative)
    if path.is_absolute() or ".." in path.parts:
        return None
    return root / path


def discovered_checkpoints(root: Path = ROOT) -> set[str]:
    checkpoint_root = root / CHECKPOINT_ROOT_REL
    if not checkpoint_root.is_dir():
        return set()
    return {
        path.relative_to(root).as_posix()
        for path in checkpoint_root.glob("*.json")
        if path.is_file()
    }


def checkpoint_semantic_errors(checkpoint: dict[str, Any], label: str) -> list[str]:
    errors: list[str] = []
    state = checkpoint["state"]
    actions = checkpoint["permitted_next_actions"]
    action_ids = [item["id"] for item in actions]
    next_action = checkpoint["next_action"]
    external = checkpoint["external_evidence"]
    boundary = checkpoint["blocking_boundary"]
    terminal_evidence = checkpoint["terminal_evidence"]

    if len(action_ids) != len(set(action_ids)):
        errors.append(f"{label}: permitted_next_actions contains duplicate action IDs")

    if state == TERMINAL_STATE:
        if next_action is not None:
            errors.append(f"{label}: TERMINAL checkpoint must not have next_action")
        if actions:
            errors.append(f"{label}: TERMINAL checkpoint must not have permitted_next_actions")
        if not terminal_evidence:
            errors.append(f"{label}: TERMINAL checkpoint requires terminal_evidence")
        if external["waiting"]:
            errors.append(f"{label}: TERMINAL checkpoint cannot wait for external evidence")
        if boundary is not None:
            errors.append(f"{label}: TERMINAL checkpoint cannot carry a blocking boundary")
    else:
        if next_action is None:
            errors.append(f"{label}: nonterminal checkpoint requires one deterministic next_action")
        elif next_action["id"] not in action_ids:
            errors.append(f"{label}: next_action must be one of permitted_next_actions")
        if not actions:
            errors.append(f"{label}: nonterminal checkpoint requires permitted_next_actions")
        if terminal_evidence:
            errors.append(f"{label}: nonterminal checkpoint must not claim terminal_evidence")

    if state == "AWAITING_EXTERNAL_EVIDENCE":
        if not external["waiting"]:
            errors.append(f"{label}: AWAITING_EXTERNAL_EVIDENCE requires external_evidence.waiting=true")
        if not external["objects"]:
            errors.append(f"{label}: AWAITING_EXTERNAL_EVIDENCE requires exact external evidence objects")
    elif external["waiting"]:
        errors.append(f"{label}: only AWAITING_EXTERNAL_EVIDENCE may set external_evidence.waiting=true")

    if state == BLOCKED_STATE:
        if boundary is None:
            errors.append(f"{label}: BLOCKED_GENUINE_BOUNDARY requires a named blocking_boundary")
        elif boundary["category"] not in RECOGNIZED_BOUNDARIES:
            errors.append(f"{label}: unrecognized blocking boundary {boundary['category']!r}")
    elif boundary is not None:
        errors.append(f"{label}: blocking_boundary is only valid for BLOCKED_GENUINE_BOUNDARY")

    if state in LIVE_STATES and checkpoint["resume"]["requires_chat_history"]:
        errors.append(f"{label}: live checkpoint cannot require chat history")
    if state in LIVE_STATES and not checkpoint["resume"]["fresh_session_safe"]:
        errors.append(f"{label}: live checkpoint must be fresh-session safe")

    if next_action is not None:
        normalized = f"{next_action['id']} {next_action['description']}".lower().strip()
        vague_waits = {"wait", "wait for ci", "wait for review", "wait for checks"}
        if normalized in vague_waits or next_action["description"].strip().lower() in vague_waits:
            errors.append(f"{label}: vague wait is not a deterministic next action")

    identities = checkpoint["identities"]
    if identities["pr_number"] is not None and identities["candidate_head_sha"] is None:
        errors.append(f"{label}: PR-bound checkpoint requires candidate_head_sha")
    if identities["workflow_runs"] and identities["candidate_head_sha"] is None:
        errors.append(f"{label}: workflow-bound checkpoint requires candidate_head_sha")

    claim_boundaries = checkpoint["claim_boundaries"]
    if any(claim_boundaries.values()):
        errors.append(f"{label}: checkpoint is continuity state only and cannot authorize claims or protected actions")

    return errors


def registry_errors(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    registry_path = root / REGISTRY_REL
    if not registry_path.is_file():
        return [f"bounded-operation checkpoint registry is missing: {REGISTRY_REL}"]

    registry = load_json(registry_path)
    errors.extend(
        f"{REGISTRY_REL}: {error}"
        for error in schema_errors(registry, root / REGISTRY_SCHEMA_REL)
    )
    if errors:
        return errors

    registered = set(registry["checkpoints"])
    discovered = discovered_checkpoints(root)
    for relative in sorted(discovered - registered):
        errors.append(f"bounded-operation continuity: discovered checkpoint is unregistered: {relative}")
    for relative in sorted(registered - discovered):
        errors.append(f"bounded-operation continuity: registered checkpoint is missing: {relative}")

    checkpoint_ids: list[str] = []
    work_ids: list[str] = []
    for relative in registry["checkpoints"]:
        path = safe_repo_path(relative, root)
        if path is None or not path.is_file():
            continue
        checkpoint = load_json(path)
        shape_errors = schema_errors(checkpoint, root / CHECKPOINT_SCHEMA_REL)
        errors.extend(f"{relative}: {error}" for error in shape_errors)
        if shape_errors:
            continue
        checkpoint_ids.append(checkpoint["checkpoint_id"])
        work_ids.append(checkpoint["governed_work_id"])
        errors.extend(checkpoint_semantic_errors(checkpoint, relative))

    for value in sorted({x for x in checkpoint_ids if checkpoint_ids.count(x) > 1}):
        errors.append(f"bounded-operation continuity: duplicate checkpoint_id {value}")
    for value in sorted({x for x in work_ids if work_ids.count(x) > 1}):
        errors.append(f"bounded-operation continuity: duplicate governed_work_id {value}")
    return errors


def instruction_binding_errors(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    for relative, fragments in REQUIRED_INSTRUCTION_BINDINGS.items():
        path = root / relative
        if not path.is_file():
            errors.append(f"bounded-operation continuity instruction binding is missing: {relative}")
            continue
        text = path.read_text(encoding="utf-8")
        for fragment in fragments:
            if fragment not in text:
                errors.append(f"{relative}: bounded-operation continuity binding missing {fragment!r}")
    return errors


def main() -> int:
    errors = instruction_binding_errors() + registry_errors()
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        print(f"bounded-operation continuity validation failed with {len(errors)} error(s)", file=sys.stderr)
        return 1

    print(
        "bounded-operation continuity is valid: registered checkpoints are fresh-session resumable, "
        "deterministic, exact-identity bound, and fail closed only at named genuine boundaries"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
