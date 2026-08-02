#!/usr/bin/env python3
"""Offline GCL work-package tooling candidate.

This tranche validates candidate manifests against repository-local schemas and
checks exact local file identities. It cannot authorize promotion.
"""
from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TRUTH_SPINE = ROOT / "governance" / "gcl_truth_spine_registry.json"
DEFAULT_CONTRACT = ROOT / "governance" / "gcl_tooling_command_contract.json"
DEFAULT_CONTRACT_SCHEMA = ROOT / "schemas" / "gcl_tooling_command_contract.schema.json"
DEFAULT_IDENTITY_SCHEMA = ROOT / "schemas" / "gcl_local_identity_manifest.schema.json"
DEFAULT_FIXTURE_MANIFEST = ROOT / "governance" / "governed_campaign_registry.json"
DEFAULT_FIXTURE_SCHEMA = ROOT / "schemas" / "governed_campaign_registry.schema.json"
DEFAULT_FIXTURE_IDENTITIES = ROOT / "fixtures" / "gcl_tooling" / "governed_campaign_registry.identity.json"

IMPLEMENTED_COMMANDS = {"validate-manifest", "check-identities"}
PLANNED_COMMANDS = {"init-work-package", "build-review-packet", "verify-promotion"}
EXPECTED_COMMANDS = IMPLEMENTED_COMMANDS | PLANNED_COMMANDS
DYNAMIC_AUTHORITY_CLASSES = {"producing repository", "producing research repository"}


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def schema_errors(instance: dict[str, Any], schema: dict[str, Any], label: str) -> list[str]:
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    return [
        f"{label} schema: {'/'.join(map(str, error.absolute_path)) or '<root>'}: {error.message}"
        for error in sorted(validator.iter_errors(instance), key=lambda item: list(item.absolute_path))
    ]


def safe_repository_path(root: Path, relative: str) -> Path:
    candidate = Path(relative)
    if candidate.is_absolute() or ".." in candidate.parts:
        raise ValueError(f"unsafe repository path: {relative}")
    resolved = (root / candidate).resolve()
    if resolved != root.resolve() and root.resolve() not in resolved.parents:
        raise ValueError(f"path escapes repository root: {relative}")
    return resolved


def resolve_input_path(path: Path, root: Path = ROOT) -> Path:
    return path if path.is_absolute() else root / path


def git_blob_sha(payload: bytes) -> str:
    header = f"blob {len(payload)}\0".encode("utf-8")
    return hashlib.sha1(header + payload).hexdigest()


def record_class(truth_spine: dict[str, Any], record_class_id: str) -> dict[str, Any] | None:
    matches = [
        item
        for item in truth_spine.get("record_classes", [])
        if item.get("record_class_id") == record_class_id
    ]
    return matches[0] if len(matches) == 1 else None


def repository_is_authorized(expected: str, actual: str) -> bool:
    if expected in DYNAMIC_AUTHORITY_CLASSES:
        return actual.startswith("grandchallenge/") and len(actual.split("/", 1)[1]) > 0
    return expected == actual


def path_is_authorized(patterns: list[str], relative_path: str) -> bool:
    return any(fnmatch.fnmatchcase(relative_path, pattern) for pattern in patterns)


def validate_manifest_record(
    *,
    root: Path,
    manifest_path: Path,
    schema_path: Path,
    record_class_id: str,
    repository: str,
    relative_path: str,
    truth_spine_path: Path = DEFAULT_TRUTH_SPINE,
) -> list[str]:
    errors: list[str] = []
    try:
        manifest = load_json(manifest_path)
        schema = load_json(schema_path)
        truth_spine = load_json(truth_spine_path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return [str(exc)]

    errors.extend(schema_errors(manifest, schema, "manifest"))
    entry = record_class(truth_spine, record_class_id)
    if entry is None:
        errors.append(f"truth spine: unknown or duplicate record class {record_class_id}")
        return errors

    expected_repository = str(entry.get("authoritative_repository", ""))
    if not repository_is_authorized(expected_repository, repository):
        errors.append(
            f"truth spine: {record_class_id} authority is {expected_repository}, not {repository}"
        )

    patterns = [str(item) for item in entry.get("authoritative_path_patterns", [])]
    if not path_is_authorized(patterns, relative_path):
        errors.append(
            f"truth spine: {relative_path} is outside the authoritative path class for "
            f"{record_class_id}"
        )

    try:
        expected_manifest_path = safe_repository_path(root, relative_path)
        if manifest_path.resolve() != expected_manifest_path:
            errors.append(
                f"manifest path mismatch: argument resolves to {manifest_path.resolve()}, "
                f"truth-spine path resolves to {expected_manifest_path}"
            )
    except ValueError as exc:
        errors.append(str(exc))
    return errors


def check_identity_manifest(
    *,
    root: Path,
    identity_manifest_path: Path,
    identity_schema_path: Path = DEFAULT_IDENTITY_SCHEMA,
) -> list[str]:
    errors: list[str] = []
    try:
        manifest = load_json(identity_manifest_path)
        schema = load_json(identity_schema_path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return [str(exc)]

    errors.extend(schema_errors(manifest, schema, "identity manifest"))
    files = manifest.get("files", [])
    paths = [str(item.get("path", "")) for item in files if isinstance(item, dict)]
    if len(paths) != len(set(paths)):
        errors.append("identity manifest: duplicate file path")

    for item in files:
        if not isinstance(item, dict):
            continue
        relative = str(item.get("path", ""))
        try:
            path = safe_repository_path(root, relative)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        if not path.is_file():
            errors.append(f"identity manifest: missing file {relative}")
            continue
        payload = path.read_bytes()
        observed_sha256 = hashlib.sha256(payload).hexdigest()
        observed_blob = git_blob_sha(payload)
        if item.get("bytes") != len(payload):
            errors.append(f"identity manifest: byte-length mismatch for {relative}")
        if item.get("sha256") != observed_sha256:
            errors.append(f"identity manifest: SHA-256 mismatch for {relative}")
        if item.get("git_blob_sha1") != observed_blob:
            errors.append(f"identity manifest: Git blob mismatch for {relative}")
    return errors


def tooling_contract_errors(
    contract_path: Path = DEFAULT_CONTRACT,
    contract_schema_path: Path = DEFAULT_CONTRACT_SCHEMA,
    truth_spine_path: Path = DEFAULT_TRUTH_SPINE,
) -> list[str]:
    errors: list[str] = []
    try:
        contract = load_json(contract_path)
        schema = load_json(contract_schema_path)
        truth_spine = load_json(truth_spine_path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return [str(exc)]

    errors.extend(schema_errors(contract, schema, "tooling contract"))
    commands = contract.get("commands", [])
    names = [item.get("name") for item in commands if isinstance(item, dict)]
    if len(names) != len(set(names)) or set(names) != EXPECTED_COMMANDS:
        errors.append("tooling contract: exact five-command set required")

    states = {
        str(item.get("name")): str(item.get("implementation_state"))
        for item in commands
        if isinstance(item, dict)
    }
    for name in IMPLEMENTED_COMMANDS:
        if states.get(name) != "implemented_candidate":
            errors.append(f"tooling contract: {name} must be implemented_candidate")
    for name in PLANNED_COMMANDS:
        if states.get(name) != "planned_not_executable":
            errors.append(f"tooling contract: {name} must fail closed as planned_not_executable")

    authority = contract.get("authority", {})
    if authority.get("truth_spine_registry_id") != truth_spine.get("registry_id"):
        errors.append("tooling contract: truth-spine registry identity mismatch")
    if authority.get("truth_spine_registry_blob") != "c4b30773be2f3151b3e975131ab6510245a3810b":
        errors.append("tooling contract: protected truth-spine registry blob drift")
    if any(value is not False for value in contract.get("claim_boundaries", {}).values()):
        errors.append("tooling contract: claim boundary inflated")
    if any(value is not True for value in contract.get("invariants", {}).values()):
        errors.append("tooling contract: invariant weakened")
    return errors


def validate_tooling(root: Path = ROOT) -> list[str]:
    errors = tooling_contract_errors(
        root / "governance/gcl_tooling_command_contract.json",
        root / "schemas/gcl_tooling_command_contract.schema.json",
        root / "governance/gcl_truth_spine_registry.json",
    )
    errors.extend(
        f"fixture manifest: {error}"
        for error in validate_manifest_record(
            root=root,
            manifest_path=root / "governance/governed_campaign_registry.json",
            schema_path=root / "schemas/governed_campaign_registry.schema.json",
            record_class_id="campaign_manifest",
            repository="grandchallenge/MATH-PROGRAMME",
            relative_path="governance/governed_campaign_registry.json",
            truth_spine_path=root / "governance/gcl_truth_spine_registry.json",
        )
    )
    errors.extend(
        f"fixture identity: {error}"
        for error in check_identity_manifest(
            root=root,
            identity_manifest_path=(
                root / "fixtures/gcl_tooling/governed_campaign_registry.identity.json"
            ),
            identity_schema_path=root / "schemas/gcl_local_identity_manifest.schema.json",
        )
    )
    return errors


def emit_report(command: str, errors: list[str], report_path: Path | None = None) -> int:
    report = {
        "schema_version": "1.0.0",
        "command": command,
        "valid": not errors,
        "errors": errors,
        "authority_boundary": {
            "candidate_output_only": True,
            "may_modify_protected_records": False,
            "may_authorize_promotion": False,
            "aether_required": False,
        },
    }
    text = json.dumps(report, indent=2) + "\n"
    if report_path is not None:
        report_path.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0 if not errors else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="gcl", description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser("validate-manifest")
    validate_parser.add_argument("--manifest", type=Path, required=True)
    validate_parser.add_argument("--schema", type=Path, required=True)
    validate_parser.add_argument("--record-class", required=True)
    validate_parser.add_argument("--repository", required=True)
    validate_parser.add_argument("--relative-path", required=True)
    validate_parser.add_argument("--truth-spine", type=Path, default=DEFAULT_TRUTH_SPINE)
    validate_parser.add_argument("--report", type=Path)

    identity_parser = subparsers.add_parser("check-identities")
    identity_parser.add_argument("--identity-manifest", type=Path, required=True)
    identity_parser.add_argument("--identity-schema", type=Path, default=DEFAULT_IDENTITY_SCHEMA)
    identity_parser.add_argument("--report", type=Path)

    for command in sorted(PLANNED_COMMANDS):
        subparsers.add_parser(command)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command in PLANNED_COMMANDS:
        return emit_report(
            args.command,
            [f"{args.command}: planned command is not executable in tooling tranche 1"],
        )
    if args.command == "validate-manifest":
        errors = validate_manifest_record(
            root=ROOT,
            manifest_path=resolve_input_path(args.manifest),
            schema_path=resolve_input_path(args.schema),
            record_class_id=args.record_class,
            repository=args.repository,
            relative_path=args.relative_path,
            truth_spine_path=resolve_input_path(args.truth_spine),
        )
        return emit_report(
            args.command,
            errors,
            resolve_input_path(args.report) if args.report else None,
        )
    if args.command == "check-identities":
        errors = check_identity_manifest(
            root=ROOT,
            identity_manifest_path=resolve_input_path(args.identity_manifest),
            identity_schema_path=resolve_input_path(args.identity_schema),
        )
        return emit_report(
            args.command,
            errors,
            resolve_input_path(args.report) if args.report else None,
        )
    raise AssertionError(f"unreachable command {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
