#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "governance/external_execution_plane_profile.json"
PROFILE_SCHEMA = ROOT / "schemas/external_execution_plane_profile.schema.json"
MANIFEST_SCHEMA = ROOT / "schemas/external_execution_manifest.schema.json"
RECEIPT_SCHEMA = ROOT / "schemas/external_execution_receipt.schema.json"
ADOPTION = ROOT / "governance/GCL-CEX-01-ADOPTION.json"

class ExternalExecutionProfileError(ValueError):
    pass

def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ExternalExecutionProfileError(f"expected object: {path}")
    return value

def validate_profile_object(profile: dict[str, Any]) -> None:
    schema = load(PROFILE_SCHEMA)
    jsonschema.Draft202012Validator.check_schema(schema)
    jsonschema.validate(profile, schema, cls=jsonschema.Draft202012Validator)

    adoption = load(ADOPTION)
    authority = profile["authority"]
    expected = {
        "standard": adoption["standard"],
        "standard_version": adoption["standard_version"],
        "standard_commit": adoption["standard_commit"],
    }
    for key, value in expected.items():
        if authority.get(key) != value:
            raise ExternalExecutionProfileError(f"GCL-CEX adoption drift: {key}")
    if adoption.get("status") != "effective":
        raise ExternalExecutionProfileError("GCL-CEX adoption is not effective")
    if profile["github_control_plane"]["large_scientific_batch_primary_execution"]:
        raise ExternalExecutionProfileError("GitHub may not be the large-batch scientific compute plane")
    if profile["external_execution"]["repository_write_credentials_allowed"]:
        raise ExternalExecutionProfileError("external executor may not receive repository write credentials")
    if any(bool(value) for value in profile["claim_boundaries"].values()):
        raise ExternalExecutionProfileError("execution topology may not widen claim authority")

def validate_schema_contracts() -> None:
    for path in (MANIFEST_SCHEMA, RECEIPT_SCHEMA):
        jsonschema.Draft202012Validator.check_schema(load(path))

def validate() -> None:
    validate_schema_contracts()
    validate_profile_object(load(PROFILE))

if __name__ == "__main__":
    validate()
    print("external execution plane profile: valid")
