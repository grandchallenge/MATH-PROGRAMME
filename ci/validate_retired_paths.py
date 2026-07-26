#!/usr/bin/env python3
"""Validate retired repository paths and their bounded historical references."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RETIRED_PATH = "DOMAIN_04_POINCARE_RECONSTRUCTION_MASTER_PLAN.md"
CANONICAL_PATH = "DOMAIN_05_POINCARE_RECONSTRUCTION_MASTER_PLAN.md"
REFERENCE_MARKERS = {
    "FILE_MANIFEST.md": "was removed in PR #96",
    "docs/REPOSITORY_DOCS.md": "was removed in PR #96",
    "docs/decisions/ADR-0006_POINCARE_RECONSTRUCTION_ARCHIVE.md": (
        "retired from the current tree"
    ),
}
SCAN_SUFFIXES = {".md", ".yaml", ".yml", ".json", ".py", ".toml"}
SELF_PATHS = {
    "ci/validate_retired_paths.py",
    "ci/test_retired_paths.py",
}


def repository_texts(root: Path) -> dict[str, str]:
    texts: dict[str, str] = {}
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix not in SCAN_SUFFIXES:
            continue
        relative = path.relative_to(root).as_posix()
        if relative in SELF_PATHS or any(part.startswith(".") for part in path.relative_to(root).parts):
            continue
        texts[relative] = path.read_text(encoding="utf-8")
    return texts


def retired_path_errors(
    root: Path = ROOT,
    texts: dict[str, str] | None = None,
) -> list[str]:
    errors: list[str] = []
    texts = repository_texts(root) if texts is None else texts

    if (root / RETIRED_PATH).exists():
        errors.append(f"retired path must not exist in current tree: {RETIRED_PATH}")
    if not (root / CANONICAL_PATH).is_file():
        errors.append(f"canonical replacement is missing: {CANONICAL_PATH}")

    permitted = set(REFERENCE_MARKERS)
    for relative, text in sorted(texts.items()):
        if RETIRED_PATH in text and relative not in permitted:
            errors.append(f"{relative}: ungoverned reference to retired path {RETIRED_PATH}")

    for relative, marker in REFERENCE_MARKERS.items():
        text = texts.get(relative)
        if text is None:
            errors.append(f"retired-path reference record is missing: {relative}")
            continue
        if RETIRED_PATH not in text:
            errors.append(f"{relative}: missing retired path identity {RETIRED_PATH}")
        if marker not in text:
            errors.append(f"{relative}: missing retirement marker {marker!r}")

    return errors


def main() -> int:
    errors = retired_path_errors()
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        print(f"retired-path validation failed with {len(errors)} error(s)", file=sys.stderr)
        return 1
    print("retired path, canonical replacement, and historical-reference boundaries are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
