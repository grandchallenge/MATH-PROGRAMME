#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path.cwd()
VALIDATOR = ROOT / "ci" / "validate_pc_wp04_fixture.py"
SOURCE_FIXTURE = ROOT / "fixtures" / "formal" / "PC-WP04"


def run(fixture: Path) -> int:
    return subprocess.run(
        [sys.executable, str(VALIDATOR), str(fixture)],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode


def mutate_manifest(fixture: Path) -> None:
    path = fixture / "certificate_manifest.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["governing_sources"] = data["governing_sources"][1:]
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def mutate_declaration(fixture: Path) -> None:
    path = fixture / "PCWP04" / "History.lean"
    path.write_text(
        path.read_text(encoding="utf-8").replace("stepBack_correct", "stepBack_corrupted"),
        encoding="utf-8",
    )


def mutate_placeholder(fixture: Path) -> None:
    path = fixture / "PCWP04" / "History.lean"
    path.write_text(
        path.read_text(encoding="utf-8") + "\ntheorem forbidden : True := by sorry\n",
        encoding="utf-8",
    )


def mutate_invalid_package_name(fixture: Path) -> None:
    path = fixture / "lakefile.toml"
    path.write_text(
        path.read_text(encoding="utf-8").replace('name = "pc_wp04"', 'name = "pc-wp04"', 1),
        encoding="utf-8",
    )


def mutate_manifest_name(fixture: Path) -> None:
    path = fixture / "lake-manifest.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["name"] = "other_package"
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def mutate_unpinned_dependency(fixture: Path) -> None:
    path = fixture / "lake-manifest.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["packages"][0]["rev"] = "main"
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    if run(SOURCE_FIXTURE) != 0:
        raise SystemExit("baseline PC-WP04 fixture failed")

    for name, mutation in [
        ("missing-source", mutate_manifest),
        ("missing-declaration", mutate_declaration),
        ("proof-placeholder", mutate_placeholder),
        ("invalid-package-name", mutate_invalid_package_name),
        ("manifest-name-drift", mutate_manifest_name),
        ("unpinned-dependency", mutate_unpinned_dependency),
    ]:
        with tempfile.TemporaryDirectory(prefix=f"pc-wp04-{name}-") as tmp:
            fixture = Path(tmp) / "PC-WP04"
            shutil.copytree(SOURCE_FIXTURE, fixture)
            mutation(fixture)
            if run(fixture) == 0:
                raise SystemExit(f"adversarial mutation unexpectedly passed: {name}")
            print(f"PASS mutation rejected: {name}")

    print("PC-WP04 adversarial policy tests passed")


if __name__ == "__main__":
    main()
