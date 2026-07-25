#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
import sys
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
    ]
    for path in required:
        if not path.is_file():
            fail(f"missing required file {path}")

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
