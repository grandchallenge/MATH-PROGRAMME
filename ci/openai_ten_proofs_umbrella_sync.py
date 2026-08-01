#!/usr/bin/env python3
"""Validate OTP-UMBRELLA-SYNC-001 current-state overlay."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
RECORD_PATH = ROOT / "governance" / "openai_ten_proofs_umbrella_sync.json"
SCHEMA_PATH = ROOT / "schemas" / "openai_ten_proofs_umbrella_sync.schema.json"
DOCUMENT_PATH = ROOT / "work_packages" / "OTP_UMBRELLA_SYNC_001.md"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def validation_errors(record: dict[str, Any] | None = None, document: str | None = None) -> list[str]:
    if record is None:
        record = load_json(RECORD_PATH)
    if document is None:
        document = DOCUMENT_PATH.read_text(encoding="utf-8")

    schema = load_json(SCHEMA_PATH)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = [
        f"OTP-UMBRELLA-SYNC-001: {error.json_path}: {error.message}"
        for error in sorted(validator.iter_errors(record), key=lambda item: list(item.path))
    ]

    replay = record.get("trusted_replay", {})
    if replay.get("kernel_clear_count") != replay.get("kernel_result_family_count"):
        errors.append("OTP-UMBRELLA-SYNC-001: kernel replay count mismatch")
    if replay.get("comparator_pass_count") != replay.get("comparator_configuration_count"):
        errors.append("OTP-UMBRELLA-SYNC-001: Comparator pass count mismatch")
    if replay.get("required_nanoda_accept_count") != replay.get("required_nanoda_count"):
        errors.append("OTP-UMBRELLA-SYNC-001: Nanoda pass count mismatch")

    aggregate = record.get("aggregate_integration", {})
    if aggregate.get("all_lean_state", "").startswith("failed") and aggregate.get("reopens_kernel_gate") is not False:
        errors.append("OTP-UMBRELLA-SYNC-001: aggregate import failure reopened kernel gate")

    semantic = record.get("semantic_gate", {})
    routes = record.get("route_state", {})
    if semantic.get("clear_count") == 0:
        for field in ("may_emit_result_family_handoff", "may_emit_aggregate_handoff", "may_adjudicate", "may_promote_result"):
            if routes.get(field) is not False:
                errors.append(f"OTP-UMBRELLA-SYNC-001: {field} must remain false while semantic clear count is zero")
        if routes.get("solve_handoff_count") != 0:
            errors.append("OTP-UMBRELLA-SYNC-001: Solve handoff count must remain zero")
        if routes.get("cert_output") is not None:
            errors.append("OTP-UMBRELLA-SYNC-001: Cert output must remain null")

    current = record.get("source_identity", {}).get("current_official", {})
    historical = record.get("source_identity", {}).get("historical_disconnected", {})
    if current.get("commit") == historical.get("commit"):
        errors.append("OTP-UMBRELLA-SYNC-001: current and historical roots must remain distinct")
    if historical.get("role") != "historical_intake_evidence":
        errors.append("OTP-UMBRELLA-SYNC-001: disconnected root role drift")

    required_tokens = (
        "72452f4579749448169cacf9f2ab22a4df2bb182",
        "e62211d28e3a9131950c89caa6542cfe5eff3bca",
        "bffb7d63476d79e86665ec5a74d554794e24357e",
        "12/12",
        "0/12",
        "All.lean",
        "No result-family handoff",
        "No aggregate certification",
    )
    for token in required_tokens:
        if token not in document:
            errors.append(f"OTP-UMBRELLA-SYNC-001 document: missing token {token}")

    boundary = str(record.get("claim_boundary", ""))
    for phrase in (
        "does not establish source-to-Lean equivalence",
        "MATHCERT route or output",
        "aggregate ten-proofs certification",
    ):
        if phrase not in boundary:
            errors.append("OTP-UMBRELLA-SYNC-001: claim boundary weakened")
            break
    return errors


def main() -> int:
    errors = validation_errors()
    if errors:
        print("\n".join(errors))
        return 1
    print("validated OTP-UMBRELLA-SYNC-001 identities, replay state, semantic gate, integration debt, and route prohibitions")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
