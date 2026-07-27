#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
import sys
import tomllib
from pathlib import Path

REQUIRED_DECLARATIONS = {
    "eventContract_noComponentLoss",
    "stepBack_covers",
    "stepBack_none_outside",
    "stepBack_exactSupport",
    "stepBack_correct",
    "runBackward_covers",
    "runBackward_correct",
    "buildCertificate_sources",
    "all_s3_of_simplyConnectedCompatible",
}
REQUIRED_SOURCES = {
    ("Morgan-Tian", "Theorem 0.3"),
    ("Morgan-Tian", "Proposition 15.3"),
    ("Morgan-Tian", "Corollary 15.4"),
    ("PC-WP02", "PC02-T013/PC02-T014/PC02-T016"),
}
PROHIBITED_PATTERN = re.compile(r"(^|[^A-Za-z])(sorry|axiom)([^A-Za-z]|$)")
LEAN_NAME = re.compile(r"^[A-Za-z_][A-Za-z0-9_']*(?:\.[A-Za-z_][A-Za-z0-9_']*)*$")
GIT_REVISION = re.compile(r"^[0-9a-f]{40}$")


def fail(message: str) -> None:
    raise SystemExit(f"PC-WP04 policy failure: {message}")


def git_blob(path: Path) -> str:
    result = subprocess.run(
        ["git", "hash-object", str(path)],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def validate_lake_metadata(fixture: Path) -> None:
    lakefile_path = fixture / "lakefile.toml"
    lake_manifest_path = fixture / "lake-manifest.json"
    toolchain_path = fixture / "lean-toolchain"
    if not lake_manifest_path.is_file():
        fail("missing pinned lake-manifest.json")

    lakefile = tomllib.loads(lakefile_path.read_text(encoding="utf-8"))
    lake_manifest = json.loads(lake_manifest_path.read_text(encoding="utf-8"))
    project_name = lakefile.get("name")
    if not isinstance(project_name, str) or not LEAN_NAME.fullmatch(project_name):
        fail(f"Lake package name is not a valid Lean Name: {project_name!r}")
    if lake_manifest.get("name") != project_name:
        fail("lakefile.toml and lake-manifest.json package names disagree")

    requirements = lakefile.get("require", [])
    mathlib_requirements = [entry for entry in requirements if entry.get("name") == "mathlib"]
    if len(mathlib_requirements) != 1:
        fail("lakefile.toml must contain exactly one mathlib requirement")
    mathlib_input = mathlib_requirements[0].get("rev")
    expected_toolchain = f"leanprover/lean4:{mathlib_input}"
    if toolchain_path.read_text(encoding="utf-8").strip() != expected_toolchain:
        fail("lean-toolchain must match the lakefile mathlib release")

    packages = lake_manifest.get("packages", [])
    mathlib_packages = [entry for entry in packages if entry.get("name") == "mathlib"]
    if len(mathlib_packages) != 1:
        fail("lake-manifest.json must contain exactly one mathlib package")
    if mathlib_packages[0].get("inputRev") != mathlib_input:
        fail("mathlib inputRev does not match lakefile.toml")
    for package in packages:
        revision = package.get("rev")
        if not isinstance(revision, str) or not GIT_REVISION.fullmatch(revision):
            fail(f"dependency {package.get('name', '<unknown>')} is not pinned to a full Git revision")


def main() -> None:
    fixture = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("fixtures/formal/PC-WP04")
    root = Path.cwd()
    manifest_path = fixture / "certificate_manifest.json"
    lean_path = fixture / "PCWP04" / "History.lean"
    required = [
        manifest_path,
        lean_path,
        fixture / "README.md",
        fixture / "lakefile.toml",
        fixture / "lean-toolchain",
        fixture / "lake-manifest.json",
    ]
    for path in required:
        if not path.is_file():
            fail(f"missing required file {path}")

    validate_lake_metadata(fixture)

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("artifact_id") != "PC-WP04":
        fail("incorrect artifact_id")
    if manifest.get("imported_boundary", {}).get("declaration") != "ImportedEventRelation":
        fail("imported boundary must remain explicit")

    declarations = set(manifest.get("formal_declarations", []))
    if declarations != REQUIRED_DECLARATIONS:
        fail(f"formal declaration set drift: {sorted(declarations ^ REQUIRED_DECLARATIONS)}")

    lean_text = lean_path.read_text(encoding="utf-8")
    for declaration in REQUIRED_DECLARATIONS | {"ImportedEventRelation"}:
        if declaration not in lean_text:
            fail(f"Lean source omits {declaration}")
    for line_no, line in enumerate(lean_text.splitlines(), start=1):
        if PROHIBITED_PATTERN.search(line):
            fail(f"prohibited proof placeholder or local axiom at line {line_no}")

    sources = {
        (entry.get("provider"), entry.get("theorem_id"))
        for entry in manifest.get("governing_sources", [])
    }
    if sources != REQUIRED_SOURCES:
        fail(f"source-binding set drift: {sorted(sources ^ REQUIRED_SOURCES)}")

    replay = manifest.get("fixture_replay", {})
    for key in ("schema", "fixtures", "validator"):
        path = root / replay.get(key, "")
        if not path.is_file():
            fail(f"missing replay input {key}: {path}")
        digest_key = f"{key}_git_blob"
        if git_blob(path) != replay.get(digest_key):
            fail(f"Git blob mismatch for {key}")

    if replay.get("expected_total") != 14 or replay.get("expected_valid") != 2 or replay.get("expected_invalid") != 12:
        fail("fixture cardinality contract drift")

    validator = root / replay["validator"]
    subprocess.run([sys.executable, str(validator)], check=True)
    print("PC-WP04 policy validation passed")


if __name__ == "__main__":
    main()
