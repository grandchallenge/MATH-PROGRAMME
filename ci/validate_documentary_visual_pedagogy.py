#!/usr/bin/env python3
"""Validate the bounded documentary visual-pedagogy pilot contract.

This validator checks identity, completeness, schema shape, provenance declarations,
and authority boundaries. It deliberately does not claim to validate mathematical
visual fidelity; that remains an independent domain-sensitive review obligation.
"""

from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
AUDIT_PATH = Path("governance/documentary_visual_pedagogy_pilot_audit.json")
CONTRACT_ROOT = Path("governance/visual_pedagogy/plates")
SCHEMA_PATH = Path("schemas/documentary_visual_plate.schema.json")
ASSET_ROOT = Path("docs/assets/documentaries")
VISUAL_SUFFIXES = {".svg", ".png", ".webp", ".jpg", ".jpeg", ".pdf", ".mp4", ".webm"}
DISPOSITIONS = {"KEEP", "REDRAW", "REPLACE", "RETIRE"}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def discovered_visual_assets(root: Path = ROOT) -> set[str]:
    base = root / ASSET_ROOT
    if not base.is_dir():
        return set()
    return {
        path.relative_to(root).as_posix()
        for path in base.rglob("*")
        if path.is_file() and path.suffix.lower() in VISUAL_SUFFIXES
    }


def discovered_contract_paths(root: Path = ROOT) -> list[Path]:
    base = root / CONTRACT_ROOT
    if not base.is_dir():
        return []
    return sorted(base.glob("*.json"))


def audit_inventory(audit: dict[str, Any]) -> list[dict[str, Any]]:
    return [asset for family in audit.get("families", []) for asset in family.get("assets", [])]


def visual_pedagogy_errors(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    audit_file = root / AUDIT_PATH
    schema_file = root / SCHEMA_PATH

    if not audit_file.is_file():
        return [f"visual pedagogy: missing audit record {AUDIT_PATH.as_posix()}"]
    if not schema_file.is_file():
        return [f"visual pedagogy: missing plate schema {SCHEMA_PATH.as_posix()}"]

    audit = load_json(audit_file)
    schema = load_json(schema_file)
    validator = Draft202012Validator(schema)
    inventory = audit_inventory(audit)

    if not audit.get("full_inventory_audit_complete", False):
        errors.append("visual pedagogy: whole-library identity/disposition audit is not complete")

    asset_paths = [str(item.get("asset", "")) for item in inventory]
    if len(asset_paths) != len(set(asset_paths)):
        errors.append("visual pedagogy: duplicate asset path in audit inventory")

    dispositions = [str(item.get("disposition", "")) for item in inventory]
    for disposition in dispositions:
        if disposition not in DISPOSITIONS:
            errors.append(f"visual pedagogy: unknown audit disposition {disposition!r}")

    counts = audit.get("inventory_counts", {})
    if counts.get("assets") != len(inventory):
        errors.append(
            f"visual pedagogy: inventory count says {counts.get('assets')!r} assets, found {len(inventory)}"
        )
    if counts.get("documentary_families") != len(audit.get("families", [])):
        errors.append("visual pedagogy: documentary-family count does not match family inventory")
    role_counts = Counter(str(item.get("role", "")) for item in inventory)
    if counts.get("decorative_covers") != role_counts.get("cover", 0):
        errors.append("visual pedagogy: decorative-cover count does not match inventory")
    if counts.get("instructional_plates") != role_counts.get("plate", 0):
        errors.append("visual pedagogy: instructional-plate count does not match inventory")
    disposition_counts = Counter(dispositions)
    for disposition in sorted(DISPOSITIONS):
        if counts.get(disposition, 0) != disposition_counts.get(disposition, 0):
            errors.append(
                f"visual pedagogy: {disposition} count says {counts.get(disposition, 0)!r}, "
                f"found {disposition_counts.get(disposition, 0)}"
            )

    audited_assets = set(asset_paths)
    for item in inventory:
        relative = str(item.get("asset", ""))
        path = root / relative
        if not relative.startswith(f"{ASSET_ROOT.as_posix()}/"):
            errors.append(f"visual pedagogy: audited asset outside documentary asset root: {relative}")
            continue
        if not path.is_file():
            errors.append(f"visual pedagogy: audited predecessor asset missing: {relative}")
            continue
        expected_sha = str(item.get("blob_sha", ""))
        actual_sha = git_blob_sha(path)
        if expected_sha != actual_sha:
            errors.append(
                f"visual pedagogy: predecessor identity drift for {relative}: "
                f"audit {expected_sha!r}, current git blob {actual_sha}"
            )

    pilot = audit.get("reference_pilot", {})
    selected = pilot.get("selected", [])
    if not 6 <= len(selected) <= 10:
        errors.append(f"visual pedagogy: reference pilot must contain 6-10 cases, found {len(selected)}")
    selected_paths = [str(item.get("asset", "")) for item in selected]
    if len(selected_paths) != len(set(selected_paths)):
        errors.append("visual pedagogy: duplicate asset in reference-pilot selection")
    inventory_by_path = {str(item.get("asset", "")): item for item in inventory}
    for item in selected:
        relative = str(item.get("asset", ""))
        audited = inventory_by_path.get(relative)
        if audited is None:
            errors.append(f"visual pedagogy: pilot asset is absent from audit inventory: {relative}")
            continue
        if item.get("disposition") != audited.get("disposition"):
            errors.append(f"visual pedagogy: pilot disposition disagrees with audit for {relative}")
    if selected and not any(item.get("disposition") == "KEEP" for item in selected):
        errors.append("visual pedagogy: pilot lacks a KEEP positive control")
    if selected and not any(item.get("disposition") in {"REDRAW", "REPLACE"} for item in selected):
        errors.append("visual pedagogy: pilot lacks a corrective REDRAW/REPLACE case")

    contracts: list[tuple[Path, dict[str, Any]]] = []
    plate_ids: list[str] = []
    for path in discovered_contract_paths(root):
        try:
            contract = load_json(path)
        except json.JSONDecodeError as exc:
            errors.append(f"visual pedagogy: invalid JSON {path.relative_to(root)}: {exc}")
            continue
        contracts.append((path, contract))
        plate_ids.append(str(contract.get("plate_id", "")))
        for error in sorted(validator.iter_errors(contract), key=lambda value: list(value.path)):
            errors.append(
                f"visual pedagogy: {path.relative_to(root).as_posix()} {error.json_path}: {error.message}"
            )
        if contract.get("representation_class") in {"data-derived", "simulation-derived"}:
            if not contract.get("renderer", {}).get("reproducible", False):
                errors.append(
                    f"visual pedagogy: {path.name} data/simulation-derived contract must be reproducible"
                )
        review = contract.get("independent_review")
        if not isinstance(review, dict):
            errors.append(f"visual pedagogy: {path.name} must declare independent_review status")

    if len(plate_ids) != len(set(plate_ids)):
        errors.append("visual pedagogy: duplicate plate_id across pilot contracts")
    if len(contracts) != len(selected):
        errors.append(
            f"visual pedagogy: expected one visual contract per selected pilot case; "
            f"selected {len(selected)}, contracts {len(contracts)}"
        )

    accounted_contract_assets: set[str] = set()
    for path, contract in contracts:
        derivative_paths = {
            str(item.get("path", "")) for item in contract.get("derivatives", []) if item.get("path")
        }
        predecessor = contract.get("predecessor")
        if isinstance(predecessor, str) and predecessor:
            derivative_paths.add(predecessor)
        matched = derivative_paths & set(selected_paths)
        if len(matched) != 1:
            errors.append(
                f"visual pedagogy: {path.name} must bind exactly one selected predecessor asset; "
                f"matched {sorted(matched)}"
            )
            continue
        selected_asset = next(iter(matched))
        accounted_contract_assets.add(selected_asset)
        audited = inventory_by_path[selected_asset]
        if contract.get("documentary_id") != audited.get("documentary_id"):
            errors.append(f"visual pedagogy: {path.name} documentary_id disagrees with audit")
        if contract.get("audit_disposition") != audited.get("disposition"):
            errors.append(f"visual pedagogy: {path.name} audit_disposition disagrees with audit")

    for missing in sorted(set(selected_paths) - accounted_contract_assets):
        errors.append(f"visual pedagogy: selected pilot asset has no unique contract: {missing}")

    discovered_assets = discovered_visual_assets(root)
    contract_derivatives = {
        str(item.get("path", ""))
        for _, contract in contracts
        for item in contract.get("derivatives", [])
        if item.get("path")
    }
    unaccounted = discovered_assets - audited_assets - contract_derivatives
    for relative in sorted(unaccounted):
        errors.append(f"visual pedagogy: unaccounted documentary visual asset: {relative}")

    return errors


def main() -> int:
    errors = visual_pedagogy_errors()
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("documentary visual-pedagogy contracts valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
