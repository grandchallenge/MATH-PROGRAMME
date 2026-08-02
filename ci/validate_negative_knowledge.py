#!/usr/bin/env python3
"""Validate the GCL negative-knowledge pilot registry."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = ROOT / "negative_knowledge" / "pilot_registry.json"
DEFAULT_SCHEMA = ROOT / "schemas" / "negative_knowledge_registry.schema.json"

REOPENABLE_STATUSES = {
    "blocked",
    "inconclusive",
    "computationally_exhausted",
    "reopen_on_new_theorem",
    "reopen_on_new_evidence",
}
PILOT_TYPES = {"mathematical", "computational", "systems"}


def canonical_digest(value: Any) -> str:
    payload = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def validate(
    registry_path: Path = DEFAULT_REGISTRY,
    schema_path: Path = DEFAULT_SCHEMA,
) -> list[str]:
    errors: list[str] = []
    try:
        registry = load_json(registry_path)
    except (OSError, json.JSONDecodeError) as exc:
        return [f"registry load failed: {exc}"]
    try:
        schema = load_json(schema_path)
    except (OSError, json.JSONDecodeError) as exc:
        return [f"schema load failed: {exc}"]

    validator = Draft202012Validator(schema)
    for error in sorted(validator.iter_errors(registry), key=lambda item: list(item.path)):
        location = "/".join(str(part) for part in error.path) or "<root>"
        errors.append(f"schema {location}: {error.message}")
    if errors:
        return errors

    records = registry["records"]
    record_ids = [record["negative_record_id"] for record in records]
    if len(records) != 3:
        errors.append("pilot registry must contain exactly three records")
    if len(record_ids) != len(set(record_ids)):
        errors.append("negative_record_id values must be unique")

    record_types = {record["record_type"] for record in records}
    if record_types != PILOT_TYPES:
        errors.append(
            "pilot registry must contain exactly the mathematical, computational, and systems record types"
        )

    scope_digests: set[str] = set()
    evidence_digests: set[str] = set()
    evidence_subjects: set[tuple[str, str, str, str]] = set()

    for record in records:
        record_id = record["negative_record_id"]
        expected_scope_digest = canonical_digest(record["scope"])
        if record["scope_digest"] != expected_scope_digest:
            errors.append(f"{record_id}: scope_digest does not match canonical scope bytes")
        expected_evidence_digest = canonical_digest(record["evidence"])
        if record["evidence_digest"] != expected_evidence_digest:
            errors.append(f"{record_id}: evidence_digest does not match canonical evidence bytes")

        if record["scope_digest"] in scope_digests:
            errors.append(f"{record_id}: duplicate scope_digest")
        scope_digests.add(record["scope_digest"])
        if record["evidence_digest"] in evidence_digests:
            errors.append(f"{record_id}: duplicate evidence_digest")
        evidence_digests.add(record["evidence_digest"])

        for artifact in record["evidence"]:
            subject = (
                artifact["repository"],
                artifact["commit_sha"],
                artifact["path"],
                artifact["git_blob_sha1"],
            )
            if subject in evidence_subjects:
                errors.append(f"{record_id}: duplicate evidence subject {subject}")
            evidence_subjects.add(subject)

        status = record["status"]
        failure_kind = record["failure_kind"]
        reopening = record["reopening"]
        if status in REOPENABLE_STATUSES and reopening is None:
            errors.append(f"{record_id}: reopenable status requires a structured reopening trigger")
        if status not in REOPENABLE_STATUSES and status != "superseded" and reopening is not None:
            errors.append(f"{record_id}: terminal status must not contain reopening instructions")
        if status == "reopen_on_new_theorem" and reopening is not None:
            if reopening["trigger_type"] != "new_theorem":
                errors.append(f"{record_id}: reopen_on_new_theorem requires new_theorem trigger")
        if status == "reopen_on_new_evidence" and reopening is not None:
            if reopening["trigger_type"] != "new_evidence":
                errors.append(f"{record_id}: reopen_on_new_evidence requires new_evidence trigger")

        if status == "refuted" and failure_kind != "theorem_refutation":
            errors.append(f"{record_id}: refuted status requires theorem_refutation evidence")
        if failure_kind == "theorem_refutation" and status != "refuted":
            errors.append(f"{record_id}: theorem_refutation must use refuted status")
        if failure_kind == "estimate_obstruction" and status not in {
            "blocked",
            "inconclusive",
            "invalid_under_assumptions",
            "reopen_on_new_theorem",
            "reopen_on_new_evidence",
        }:
            errors.append(f"{record_id}: estimate obstruction has incompatible status {status}")
        if failure_kind == "bounded_search_exhaustion" and status not in {
            "computationally_exhausted",
            "reopen_on_new_evidence",
        }:
            errors.append(f"{record_id}: bounded search exhaustion has incompatible status {status}")
        if status == "computationally_exhausted" and failure_kind not in {
            "bounded_search_exhaustion",
            "resource_exhaustion",
        }:
            errors.append(
                f"{record_id}: computationally_exhausted requires bounded-search or resource exhaustion"
            )

        superseded_by = record["lineage"]["superseded_by"]
        if status == "superseded" and superseded_by is None:
            errors.append(f"{record_id}: superseded status requires superseded_by identity")
        if status != "superseded" and superseded_by is not None:
            errors.append(f"{record_id}: non-superseded status must not set superseded_by")

        if failure_kind == "theorem_refutation":
            if record["scope"]["conclusion_strength"] != "exact_scope_only":
                errors.append(f"{record_id}: theorem refutation must be exact_scope_only")
            if record["review"]["required_office"] != "Referee":
                errors.append(f"{record_id}: theorem refutation requires Referee review")

        if failure_kind == "bounded_search_exhaustion":
            if record["record_type"] != "computational":
                errors.append(f"{record_id}: bounded search exhaustion must be computational")
            if record["scope"]["conclusion_strength"] != "finite_search_only":
                errors.append(f"{record_id}: bounded search exhaustion must be finite_search_only")

        if failure_kind == "implementation_failure":
            if record["record_type"] != "systems":
                errors.append(f"{record_id}: implementation failure must be systems")
            if status not in {"superseded", "blocked", "inconclusive"}:
                errors.append(f"{record_id}: implementation failure has invalid disposition")

        if record["disposition"]["route_state"] != "inactive":
            errors.append(f"{record_id}: negative records cannot activate a route")
        if not record["disposition"]["non_excluded_variants"]:
            errors.append(f"{record_id}: non_excluded_variants must remain explicit")
        if record["review"]["satisfaction_mode"] != "external_exact_head_review":
            errors.append(f"{record_id}: review satisfaction must remain external and exact-head bound")
        if record["review"]["may_promote_claim"]:
            errors.append(f"{record_id}: review cannot promote a claim")

        for predecessor in record["lineage"]["predecessor_record_ids"]:
            if predecessor not in record_ids:
                errors.append(f"{record_id}: unknown predecessor {predecessor}")
            if predecessor == record_id:
                errors.append(f"{record_id}: record cannot supersede itself")

        if any(record["claim_boundaries"].values()):
            errors.append(f"{record_id}: claim boundary inflation is prohibited")

    predecessor_graph = {
        record["negative_record_id"]: set(record["lineage"]["predecessor_record_ids"])
        for record in records
    }
    for start in record_ids:
        stack: list[tuple[str, tuple[str, ...]]] = [(start, ())]
        while stack:
            current, path = stack.pop()
            if current in path:
                cycle = " -> ".join((*path, current))
                errors.append(f"lineage cycle detected: {cycle}")
                break
            stack.extend(
                (predecessor, (*path, current))
                for predecessor in predecessor_graph.get(current, set())
            )

    if any(registry["claim_boundaries"].values()):
        errors.append("registry claim boundary inflation is prohibited")

    return errors


def main() -> int:
    errors = validate()
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        print(f"negative-knowledge validation failed with {len(errors)} error(s)", file=sys.stderr)
        return 1
    print("negative-knowledge pilot registry is valid: 3 bounded records")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
