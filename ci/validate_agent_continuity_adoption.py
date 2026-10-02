#!/usr/bin/env python3
"""Validate MATH-PROGRAMME adoption of GCL-AGENT-CONTINUITY-001."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
ADOPTION_REL = ".gcl/agent-continuity.json"
AGENTS_REL = "AGENTS.md"
SCHEMA_REL = "schemas/agent_continuity_adoption.schema.json"
CHECKPOINT_REGISTRY_REL = "governance/bounded_operation_checkpoint_registry.json"
CHECKPOINT_VALIDATOR_REL = "ci/validate_bounded_operation_continuity.py"

SCHEMA_AUTHORITY_COMMIT = "7e6b61ddf77e2d73309657d089a98cae84cc735f"
SCHEMA_BLOB_SHA = "b019881a54763a949613c8116260b729742867bd"
LOCAL_VALIDATOR = "ci/validate_agent_continuity_adoption.py"

EXPECTED = {
    "repository": "grandchallenge/MATH-PROGRAMME",
    "specialization": "MATH-PROGRAMME-BOUNDED-OPERATION-CONTINUITY-001",
    "local_validator": LOCAL_VALIDATOR,
}
EXPECTED_SCHEMA_BINDING = {
    "authority_commit": SCHEMA_AUTHORITY_COMMIT,
    "schema_blob_sha": SCHEMA_BLOB_SHA,
    "local_snapshot": SCHEMA_REL,
    "local_snapshot_authoritative": False,
    "mutable_remote_fetch_allowed": False,
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def git_blob_sha(path: Path) -> str:
    payload = path.read_bytes()
    header = f"blob {len(payload)}\0".encode("utf-8")
    return hashlib.sha1(header + payload).hexdigest()


def common_schema_errors(record: dict[str, Any], root: Path = ROOT) -> list[str]:
    schema_path = root / SCHEMA_REL
    if not schema_path.is_file():
        return [f"missing pinned common adoption schema: {SCHEMA_REL}"]

    observed_blob = git_blob_sha(schema_path)
    if observed_blob != SCHEMA_BLOB_SHA:
        return [
            f"pinned schema blob mismatch: expected {SCHEMA_BLOB_SHA}, found {observed_blob}"
        ]

    try:
        schema = load_json(schema_path)
        Draft202012Validator.check_schema(schema)
    except Exception as exc:
        return [f"invalid pinned common adoption schema: {exc}"]

    validator = Draft202012Validator(schema)
    return [
        f"common schema {error.json_path}: {error.message}"
        for error in sorted(validator.iter_errors(record), key=lambda item: list(item.path))
    ]


def adoption_errors(record: dict[str, Any], agents_text: str, root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    errors.extend(common_schema_errors(record, root))

    for key, value in EXPECTED.items():
        if record.get(key) != value:
            errors.append(f"{key}: expected {value!r}, found {record.get(key)!r}")

    specialization_data = record.get("specialization_data", {})
    if not isinstance(specialization_data, dict):
        errors.append("specialization_data must be an object")
        specialization_data = {}

    binding = specialization_data.get("schema_binding", {})
    if not isinstance(binding, dict):
        errors.append("specialization_data.schema_binding must be an object")
        binding = {}
    for key, value in EXPECTED_SCHEMA_BINDING.items():
        if binding.get(key) != value:
            errors.append(
                f"specialization_data.schema_binding.{key}: expected {value!r}, "
                f"found {binding.get(key)!r}"
            )

    impl = specialization_data.get("implementation", {})
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
    if not isinstance(impl, dict):
        errors.append("specialization_data.implementation must be an object")
        impl = {}
    for key, value in expected_impl.items():
        if impl.get(key) != value:
            errors.append(f"implementation.{key}: expected {value!r}, found {impl.get(key)!r}")

    applicability = specialization_data.get("applicability", {})
    if not isinstance(applicability, dict):
        errors.append("specialization_data.applicability must be an object")
        applicability = {}
    if applicability.get("long_horizon_or_explicitly_admitted_operations") is not True:
        errors.append("continuity applicability must include long-horizon/admitted operations")
    if applicability.get("routine_bounded_work_excluded") is not True:
        errors.append("routine bounded work must remain excluded")

    unexpected_specialization = set(specialization_data) - {
        "schema_binding",
        "implementation",
        "applicability",
    }
    if unexpected_specialization:
        errors.append(
            "unexpected Programme specialization_data fields: "
            + ", ".join(sorted(unexpected_specialization))
        )

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
    print(
        "MATH-PROGRAMME GCL-AGENT-CONTINUITY-001 adoption: PASS "
        f"(INTELLECT schema {SCHEMA_AUTHORITY_COMMIT}:{SCHEMA_BLOB_SHA})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
