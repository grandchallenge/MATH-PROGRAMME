#!/usr/bin/env python3
"""Validate documentary visual-pedagogy contracts across pilot and propagation phases.

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
PROPAGATION_MANIFEST_PATH = Path("governance/visual_pedagogy/propagation_manifest.json")
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
    inventory: list[dict[str, Any]] = []
    for family in audit.get("families", []):
        documentary_id = family.get("documentary_id")
        for asset in family.get("assets", []):
            item = dict(asset)
            item["documentary_id"] = documentary_id
            inventory.append(item)
    return inventory


def contract_asset_candidates(contract: dict[str, Any]) -> set[str]:
    """Return repository paths by which a contract can bind its audited visual."""
    paths = {
        str(item.get("path", ""))
        for item in contract.get("derivatives", [])
        if item.get("path")
    }
    predecessor = contract.get("predecessor")
    if isinstance(predecessor, str) and predecessor:
        paths.add(predecessor)
    return paths


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
    inventory_by_path = {str(item.get("asset", "")): item for item in inventory}
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
    selected_set = set(selected_paths)
    if len(selected_paths) != len(selected_set):
        errors.append("visual pedagogy: duplicate asset in reference-pilot selection")
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

    propagation_manifest: dict[str, Any] | None = None
    propagation_file = root / PROPAGATION_MANIFEST_PATH
    if propagation_file.is_file():
        try:
            loaded = load_json(propagation_file)
            if isinstance(loaded, dict):
                propagation_manifest = loaded
            else:
                errors.append("visual pedagogy: propagation manifest must be a JSON object")
        except json.JSONDecodeError as exc:
            errors.append(f"visual pedagogy: invalid propagation manifest JSON: {exc}")

    propagation_assets: set[str] = set()
    propagation_migration_assets: set[str] = set()
    if propagation_manifest is not None:
        assets = propagation_manifest.get("assets", {})
        migration = propagation_manifest.get("migration", {})
        if not isinstance(assets, dict):
            errors.append("visual pedagogy: propagation manifest assets must be an object")
        else:
            propagation_assets = set(map(str, assets))
        if not isinstance(migration, dict):
            errors.append("visual pedagogy: propagation manifest migration must be an object")
        else:
            propagation_migration_assets = set(map(str, migration))
        if propagation_assets and propagation_assets != audited_assets:
            errors.append("visual pedagogy: propagation manifest asset population disagrees with audited inventory")

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
        errors.append("visual pedagogy: duplicate plate_id across visual contracts")

    accounted_pilot_assets: set[str] = set()
    bound_assets: list[str] = []
    for path, contract in contracts:
        candidates = contract_asset_candidates(contract)
        matched_audit = candidates & audited_assets
        if len(matched_audit) != 1:
            errors.append(
                f"visual pedagogy: {path.name} must bind exactly one audited visual asset; "
                f"matched {sorted(matched_audit)}"
            )
            continue

        bound_asset = next(iter(matched_audit))
        bound_assets.append(bound_asset)
        audited = inventory_by_path[bound_asset]
        if contract.get("documentary_id") != audited.get("documentary_id"):
            errors.append(f"visual pedagogy: {path.name} documentary_id disagrees with audit")
        if contract.get("audit_disposition") != audited.get("disposition"):
            errors.append(f"visual pedagogy: {path.name} audit_disposition disagrees with audit")

        if bound_asset in selected_set:
            accounted_pilot_assets.add(bound_asset)
            continue

        # Contracts outside the original bounded pilot are valid only as governed
        # propagation contracts. They must bind an audited non-KEEP migration asset
        # admitted by the protected Stage-0 propagation manifest.
        if propagation_manifest is None:
            errors.append(
                f"visual pedagogy: {path.name} is outside the reference pilot but no protected propagation manifest exists"
            )
            continue
        if bound_asset not in propagation_assets or bound_asset not in propagation_migration_assets:
            errors.append(
                f"visual pedagogy: {path.name} binds non-pilot asset not admitted to staged migration: {bound_asset}"
            )
        if audited.get("disposition") == "KEEP":
            errors.append(
                f"visual pedagogy: {path.name} cannot create propagation contract for KEEP asset: {bound_asset}"
            )

    duplicate_bindings = duplicate_values(bound_assets)
    for duplicate in sorted(duplicate_bindings):
        errors.append(f"visual pedagogy: audited visual asset has multiple contracts: {duplicate}")

    for missing in sorted(selected_set - accounted_pilot_assets):
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


def duplicate_values(values: list[Any]) -> set[Any]:
    seen: set[Any] = set()
    duplicates: set[Any] = set()
    for value in values:
        if value in seen:
            duplicates.add(value)
        seen.add(value)
    return duplicates


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
