#!/usr/bin/env python3
"""Validate MATH-PROGRAMME adoption of GCL-AGENT-CONTINUITY-001."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ADOPTION_REL = ".gcl/agent-continuity.json"
AGENTS_REL = "AGENTS.md"
CHECKPOINT_REGISTRY_REL = "governance/bounded_operation_checkpoint_registry.json"
CHECKPOINT_VALIDATOR_REL = "ci/validate_bounded_operation_continuity.py"

EXPECTED = {
    "policy_id": "GCL-AGENT-CONTINUITY-001",
    "version": "1.0.0",
    "repository": "grandchallenge/MATH-PROGRAMME",
    "specialization": "MATH-PROGRAMME-BOUNDED-OPERATION-CONTINUITY-001",
}

def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))

def adoption_errors(record: dict[str, Any], agents_text: str, root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    for key, value in EXPECTED.items():
        if record.get(key) != value:
            errors.append(f"{key}: expected {value!r}, found {record.get(key)!r}")
    if record.get("required") is not True:
        errors.append("required must be true")

    impl = record.get("implementation", {})
    expected_impl = {
        "authoritative_checkpoint_registry": CHECKPOINT_REGISTRY_REL,
        "validator": CHECKPOINT_VALIDATOR_REL,
        "exact_head_preflight": "freshness.verification_command",
        "durable_checkpoint": "bounded_operation_checkpoint_registry_and_WORKSET_STATE",
        "alternate_agent_live_rebind": "resume.fresh_session_safe=true;resume.requires_chat_history=false",
        "deterministic_resume": "exactly_one_next_action",
        "named_terminal_boundary": "recognized_blocking_boundary_categories",
        "duplicate_checkpoint_registry_forbidden": True,
    }
    for key, value in expected_impl.items():
        if impl.get(key) != value:
            errors.append(f"implementation.{key}: expected {value!r}, found {impl.get(key)!r}")

    applicability = record.get("applicability", {})
    if applicability.get("long_horizon_or_explicitly_admitted_operations") is not True:
        errors.append("continuity applicability must include long-horizon/admitted operations")
    if applicability.get("routine_bounded_work_excluded") is not True:
        errors.append("routine bounded work must remain excluded")

    authority = record.get("authority_preservation", {})
    for key in (
        "authority_changed",
        "mathematical_certification_changed",
        "publication_authority_changed",
        "protected_bypass_changed",
    ):
        if authority.get(key) is not False:
            errors.append(f"authority_preservation.{key} must be false")

    for relative in (CHECKPOINT_REGISTRY_REL, CHECKPOINT_VALIDATOR_REL):
        if not (root / relative).is_file():
            errors.append(f"missing mapped Programme continuity surface: {relative}")

    required_agent_tokens = (
        "GCL-AGENT-CONTINUITY-001@1.0.0",
        CHECKPOINT_REGISTRY_REL,
        CHECKPOINT_VALIDATOR_REL,
        "single operational continuity source of truth",
    )
    for token in required_agent_tokens:
        if token not in agents_text:
            errors.append(f"AGENTS.md missing canonical continuity binding token: {token}")

    return errors

def main() -> int:
    adoption_path = ROOT / ADOPTION_REL
    agents_path = ROOT / AGENTS_REL
    errors: list[str] = []
    if not adoption_path.is_file():
        errors.append(f"missing required adoption record: {ADOPTION_REL}")
    if not agents_path.is_file():
        errors.append(f"missing required agent instructions: {AGENTS_REL}")

    if not errors:
        try:
            record = load_json(adoption_path)
        except Exception as exc:
            errors.append(f"invalid adoption JSON: {exc}")
            record = {}
        if not isinstance(record, dict):
            errors.append("adoption record must be an object")
            record = {}
        agents_text = agents_path.read_text(encoding="utf-8")
        errors.extend(adoption_errors(record, agents_text))

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("MATH-PROGRAMME GCL-AGENT-CONTINUITY-001 adoption: PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
