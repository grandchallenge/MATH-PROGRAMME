#!/usr/bin/env python3
"""Validate the OZ-WP00 intake and source-lock manifest."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is required: python3 -m pip install PyYAML") from exc


ID_PATTERNS = {
    "manuscript_statements": re.compile(r"^OZ-MSS-S\d{3}$"),
    "recurrences": re.compile(r"^OZ-REC-R\d{3}$"),
    "harmonic_formulas": re.compile(r"^OZ-HAR-H\d{3}$"),
    "congruences": re.compile(r"^OZ-CON-C\d{3}$"),
    "lean_declarations": re.compile(r"^OZ-L4-T\d{3}$"),
    "certificates": re.compile(r"^OZ-CER-E\d{3}$"),
    "computations": re.compile(r"^OZ-CMP-X\d{3}$"),
    "literature_sources": re.compile(r"^OZ-LIT-B\d{3}$"),
    "irrationality_bridges": re.compile(r"^OZ-BRG-G\d{3}$"),
}

COMMON_FIELDS = {
    "id",
    "exact_statement_or_description",
    "source_lock_id",
    "exact_locator",
    "content_sha256",
    "mathematical_status",
    "novelty_status",
    "review_status",
    "assumptions",
    "scope",
    "dependencies",
    "supports",
    "conflicts",
}

EXTRA_FIELDS = {
    "lean_declarations": {
        "repository",
        "commit",
        "file",
        "declaration",
        "imported_axioms",
        "sorry_free",
        "build_result",
        "semantic_correspondence_id",
    },
    "certificates": {
        "certificate_type",
        "producer",
        "verifier",
        "replay_command",
        "bounded_domain",
    },
    "computations": {
        "code_commit",
        "environment_lock",
        "input_hashes",
        "output_hashes",
        "arithmetic_mode",
        "bounded_domain",
        "replay_command",
    },
    "literature_sources": {
        "bibliographic_identity",
        "persistent_locator",
        "audited_claims",
        "equivalence_findings",
    },
}


class ValidationError(Exception):
    """Raised when the manifest violates the intake contract."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def load_manifest(path: Path) -> dict[str, Any]:
    require(path.is_file(), f"manifest does not exist: {path}")
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    require(isinstance(payload, dict), "manifest root must be a mapping")
    return payload


def validate_sha256(value: Any, context: str) -> None:
    require(
        isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value) is not None,
        f"{context}: content_sha256 must be 64 lowercase hexadecimal characters",
    )


def validate_record(
    collection: str,
    record: Any,
    seen_ids: set[str],
    source_lock_ids: set[str],
) -> None:
    require(isinstance(record, dict), f"{collection}: every record must be a mapping")
    required = COMMON_FIELDS | EXTRA_FIELDS.get(collection, set())
    missing = sorted(required - record.keys())
    require(not missing, f"{collection}/{record.get('id', '<missing-id>')}: missing {missing}")

    record_id = record["id"]
    require(isinstance(record_id, str), f"{collection}: id must be a string")
    require(ID_PATTERNS[collection].fullmatch(record_id) is not None, f"invalid ID: {record_id}")
    require(record_id not in seen_ids, f"duplicate stable ID: {record_id}")
    seen_ids.add(record_id)

    require(
        record["source_lock_id"] in source_lock_ids,
        f"{record_id}: unknown source_lock_id {record['source_lock_id']!r}",
    )
    validate_sha256(record["content_sha256"], record_id)

    for field in ("assumptions", "dependencies", "supports", "conflicts"):
        require(isinstance(record[field], list), f"{record_id}: {field} must be a list")


def validate_manifest(payload: dict[str, Any], require_complete: bool) -> None:
    require(payload.get("manifest_contract") == "oz_wp00_intake_source_lock", "wrong manifest contract")
    require(payload.get("manifest_id") == "OZ-WP00-INTAKE-SOURCE-LOCK", "wrong manifest_id")
    require(payload.get("work_package_id") == "OZ-WP00", "wrong work_package_id")

    source_locks = payload.get("source_locks")
    require(isinstance(source_locks, list), "source_locks must be a list")
    source_lock_ids: set[str] = set()
    for lock in source_locks:
        require(isinstance(lock, dict), "each source lock must be a mapping")
        required = {"id", "kind", "version", "locator", "bytes", "sha256", "acquired_at"}
        missing = sorted(required - lock.keys())
        require(not missing, f"source lock missing fields: {missing}")
        lock_id = lock["id"]
        require(isinstance(lock_id, str) and lock_id.startswith("OZ-SRC-"), f"invalid source lock ID: {lock_id}")
        require(lock_id not in source_lock_ids, f"duplicate source lock ID: {lock_id}")
        source_lock_ids.add(lock_id)
        validate_sha256(lock["sha256"], lock_id)
        require(isinstance(lock["bytes"], int) and lock["bytes"] >= 0, f"{lock_id}: bytes must be nonnegative")

    objects = payload.get("objects")
    require(isinstance(objects, dict), "objects must be a mapping")
    require(set(objects) == set(ID_PATTERNS), "objects must contain exactly the governed collections")

    seen_ids: set[str] = set()
    for collection in ID_PATTERNS:
        records = objects[collection]
        require(isinstance(records, list), f"{collection} must be a list")
        for record in records:
            validate_record(collection, record, seen_ids, source_lock_ids)

    unresolved = payload.get("unresolved_intake")
    require(isinstance(unresolved, list), "unresolved_intake must be a list")

    declared_ready = payload.get("promotion_ready")
    computed_ready = (
        bool(source_locks)
        and all(bool(objects[name]) for name in ID_PATTERNS)
        and not unresolved
    )
    require(
        declared_ready is computed_ready,
        f"promotion_ready={declared_ready!r} disagrees with computed readiness {computed_ready!r}",
    )

    if require_complete:
        require(computed_ready, "OZ-WP00 intake is structurally valid but incomplete")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--require-complete", action="store_true")
    args = parser.parse_args()

    try:
        payload = load_manifest(args.manifest)
        validate_manifest(payload, args.require_complete)
    except ValidationError as exc:
        print(f"OZ-WP00 intake validation failed: {exc}", file=sys.stderr)
        return 1

    if payload["promotion_ready"]:
        print("OZ-WP00 intake manifest is complete and promotion-ready.")
    else:
        print("OZ-WP00 intake manifest is structurally valid; intake remains open.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
