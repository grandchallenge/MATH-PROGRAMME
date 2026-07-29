#!/usr/bin/env python3
"""Validate complete reusable cross-pillar lane packages."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import SchemaError

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = Path("governance/cross_pillar_lane_packages.json")
EXPECTED_IDS = {
    "LANE-EXACT-FINITE",
    "LANE-INTERVAL",
    "LANE-SAT-SMT",
    "LANE-LEAN-HANDOFF",
    "LANE-LITERATURE-STATUS",
}
REQUIRED_DOCTRINE_HEADINGS = (
    "## Obligation",
    "## MATHFORGE",
    "## MATHSOLVE",
    "## MATHCERT",
    "## Allowed statuses",
    "## Rejection policy",
    "## Claim boundary",
)


class LanePackageError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise LanePackageError(message)


def nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise LanePackageError(f"{path}: cannot load JSON: {exc}") from exc


def validate_schema(schema: Any, path: Path) -> Draft202012Validator:
    require(isinstance(schema, dict), f"{path}: schema must be an object")
    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError as exc:
        raise LanePackageError(f"{path}: invalid JSON Schema: {exc.message}") from exc
    return Draft202012Validator(schema, format_checker=FormatChecker())


def validate_instance(
    validator: Draft202012Validator,
    instance: Any,
    label: str,
) -> None:
    errors = sorted(validator.iter_errors(instance), key=lambda error: list(error.path))
    require(
        not errors,
        f"{label}: " + "; ".join(f"{error.json_path}: {error.message}" for error in errors),
    )


def validate_manifest(manifest: Any, lane_id: str, root: Path) -> tuple[Path, Path, Path]:
    require(isinstance(manifest, dict), f"{lane_id}: lane.json must be an object")
    require(manifest.get("schema_version") == "1.0.0", f"{lane_id}: unsupported lane schema version")
    require(manifest.get("lane_id") == lane_id, f"{lane_id}: lane manifest ID drift")
    for field in ("title", "obligation", "claim_boundary"):
        require(nonempty(manifest.get(field)), f"{lane_id}: {field} is required")

    artifacts = manifest.get("artifacts")
    require(isinstance(artifacts, dict), f"{lane_id}: artifacts must be an object")
    expected_artifacts = {
        "input_schema": "input.schema.json",
        "handoff_schema": "handoff.schema.json",
        "toy_fixture": "fixture.json",
    }
    require(artifacts == expected_artifacts, f"{lane_id}: artifact contract drift")

    statuses = manifest.get("allowed_statuses")
    require(
        isinstance(statuses, list)
        and len(statuses) >= 4
        and len(statuses) == len(set(statuses))
        and all(nonempty(status) for status in statuses),
        f"{lane_id}: allowed_statuses must be unique and nonempty",
    )
    require("rejected" in statuses, f"{lane_id}: rejected status is required")
    require("ready_for_mathcert" in statuses, f"{lane_id}: ready_for_mathcert status is required")

    rejection = manifest.get("rejection_policy")
    require(
        isinstance(rejection, list)
        and len(rejection) >= 3
        and all(nonempty(rule) for rule in rejection),
        f"{lane_id}: at least three rejection rules are required",
    )
    route = manifest.get("mathcert_route")
    require(
        isinstance(route, list)
        and len(route) >= 3
        and all(nonempty(step) for step in route),
        f"{lane_id}: MATHCERT route requires at least three steps",
    )

    input_path = root / artifacts["input_schema"]
    handoff_path = root / artifacts["handoff_schema"]
    fixture_path = root / artifacts["toy_fixture"]
    for path in (input_path, handoff_path, fixture_path):
        require(path.is_file(), f"{lane_id}: missing package artifact {path.name}")
    return input_path, handoff_path, fixture_path


def validate_doctrine(path: Path, lane_id: str) -> None:
    require(path.is_file(), f"{lane_id}: doctrine file is missing: {path}")
    text = path.read_text(encoding="utf-8")
    for heading in REQUIRED_DOCTRINE_HEADINGS:
        require(heading in text, f"{lane_id}: doctrine missing heading {heading}")
    require(lane_id.split("LANE-", 1)[-1].replace("-", " ").lower() or text, f"{lane_id}: invalid doctrine")


def validate(root: Path = ROOT) -> None:
    registry_path = root / REGISTRY_PATH
    registry = load_json(registry_path)
    require(isinstance(registry, dict), "lane registry must be an object")
    require(registry.get("schema_version") == "1.0.0", "unsupported lane registry schema version")
    require(registry.get("registry_id") == "CROSS-PILLAR-LANE-PACKAGES", "lane registry ID drift")

    required_ids = registry.get("required_lane_ids")
    require(
        isinstance(required_ids, list)
        and len(required_ids) == len(set(required_ids))
        and set(required_ids) == EXPECTED_IDS,
        "required cross-pillar lane set drift",
    )
    packages = registry.get("packages")
    require(isinstance(packages, list) and len(packages) == 5, "registry must contain exactly five packages")
    by_id = {item.get("lane_id"): item for item in packages if isinstance(item, dict)}
    require(len(by_id) == len(packages), "lane registry contains duplicate or malformed package records")
    require(set(by_id) == EXPECTED_IDS, "lane registry package set drift")

    registered_roots: set[str] = set()
    for lane_id in sorted(EXPECTED_IDS):
        record = by_id[lane_id]
        package_root_text = record.get("root")
        doctrine_text = record.get("doctrine")
        require(nonempty(package_root_text), f"{lane_id}: package root is required")
        require(nonempty(doctrine_text), f"{lane_id}: doctrine path is required")
        require(package_root_text not in registered_roots, f"{lane_id}: duplicate package root")
        registered_roots.add(package_root_text)

        package_root = root / package_root_text
        require(package_root.is_dir(), f"{lane_id}: package root is missing")
        manifest_path = package_root / "lane.json"
        require(manifest_path.is_file(), f"{lane_id}: lane.json is missing")
        manifest = load_json(manifest_path)
        input_path, handoff_path, fixture_path = validate_manifest(manifest, lane_id, package_root)
        validate_doctrine(root / doctrine_text, lane_id)

        input_schema = load_json(input_path)
        handoff_schema = load_json(handoff_path)
        input_validator = validate_schema(input_schema, input_path)
        handoff_validator = validate_schema(handoff_schema, handoff_path)
        fixture = load_json(fixture_path)
        require(isinstance(fixture, dict), f"{lane_id}: fixture must be an object")
        require(set(fixture) == {"input", "handoff"}, f"{lane_id}: fixture requires input and handoff only")
        validate_instance(input_validator, fixture["input"], f"{lane_id} fixture input")
        validate_instance(handoff_validator, fixture["handoff"], f"{lane_id} fixture handoff")
        require(
            fixture["handoff"].get("status") in manifest["allowed_statuses"],
            f"{lane_id}: fixture handoff status is not admitted by lane manifest",
        )
        require(
            fixture["handoff"].get("certification_state") == "not_certified",
            f"{lane_id}: toy fixture must remain not_certified",
        )

    discovered = {
        path.parent.relative_to(root).as_posix()
        for path in (root / "lanes").glob("*/lane.json")
        if path.is_file()
    }
    require(discovered == registered_roots, f"lane package registry mismatch: registered={sorted(registered_roots)}, discovered={sorted(discovered)}")


def main() -> int:
    try:
        validate()
    except LanePackageError as exc:
        print(f"cross-pillar lane package validation rejected: {exc}", file=sys.stderr)
        return 1
    print("cross-pillar lane packages checked: five complete doctrine, schema, fixture, rejection, and MATHCERT routes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
