#!/usr/bin/env python3
"""Validate exact MATHFORGE external-source imports and corpus conformance."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "governance" / "mathforge_external_source_imports.json"
SCHEMA_PATH = ROOT / "schemas" / "mathforge_external_source_import.schema.json"
EXPECTED_PROVIDER_COMMIT = "bab7ae57f54601b49ad9fc870051095ad487c64a"
EXPECTED_UPSTREAM_COMMIT = "f22d0f28b55e6e777acf82e722d97ae982dff02e"
EXPECTED_ARTIFACTS = {
    "governance/external_sources.json": "0b05cdc69a43e1f3c84b4fa4bff37e7cd250094f",
    "forge/intake/researchmath14k/RM-DIO-004/source_lock.json": "a465a003a28d3182ec2296dbe88fb51af63ce0ca",
    "forge/intake/researchmath14k/RM-DIO-004/reliability_register.json": "2bcd7cf431231b883eb92c302d72da5a139298a6",
    "forge/intake/researchmath14k/RM-DIO-004/source_row.json": "0ad6ee2599b59a8bd9cebb2a8e39974f1e968ef9",
    "forge/intake/researchmath14k/RM-DIO-004/problem_card.json": "a66b185460e57e975140b9a211394b7e8e9268d0",
    "forge/intake/researchmath14k/RM-DIO-004/mathsolve_handoff.json": "40f37c02db51ae48d02be7e43ca515bb9eddf2a8",
}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def import_errors(registry: dict[str, Any] | None = None) -> list[str]:
    instance = registry if registry is not None else load(REGISTRY_PATH)
    schema = load(SCHEMA_PATH)
    errors = [
        f"external source imports: {error.json_path}: {error.message}"
        for error in sorted(
            Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(instance),
            key=lambda item: list(item.path),
        )
    ]
    if instance.get("provider_commit") != EXPECTED_PROVIDER_COMMIT:
        errors.append("external source imports: protected MATHFORGE commit drift")
    sources = instance.get("sources", [])
    if not isinstance(sources, list) or len(sources) != 1:
        return errors + ["external source imports: expected exactly one governed corpus source"]
    source = sources[0]
    if source.get("source_id") != "RM-AMPHORA-001" or source.get("source_class") != "corpus_row":
        errors.append("external source imports: ResearchMath source identity or class drift")
    if source.get("upstream_commit") != EXPECTED_UPSTREAM_COMMIT:
        errors.append("external source imports: ResearchMath upstream commit drift")
    if source.get("programme_disposition") != "CONFORMANCE_FIXTURE_ONLY":
        errors.append("external source imports: corpus fixture may not grant admission")
    artifacts = source.get("artifacts", [])
    by_path = {item.get("path"): item.get("git_blob_sha1") for item in artifacts if isinstance(item, dict)}
    if by_path != EXPECTED_ARTIFACTS:
        errors.append("external source imports: canonical MATHFORGE artifact identities drift")
    return errors


def main() -> int:
    errors = import_errors()
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("MATHFORGE external corpus source is pinned to protected commit and retained as a conformance-only Programme fixture")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
