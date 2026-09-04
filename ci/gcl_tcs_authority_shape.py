from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

ROOT = Path(__file__).resolve().parents[1]
DECL_SCHEMA = Path("docs/council/submissions/GCL-TCS-00/schemas/gcl-tcs-conformance.schema.json")

CANDIDATE_STATUSES = {"candidate"}
AUTHORITATIVE_SOURCE_STATUSES = {"admitted", "authoritative"}
TERMINAL_SOURCE_STATUSES = {"superseded", "withdrawn"}
ALL_STATUSES = CANDIDATE_STATUSES | AUTHORITATIVE_SOURCE_STATUSES | TERMINAL_SOURCE_STATUSES
SHAPE_REFS = [
    "#/$defs/candidateRecordShape",
    "#/$defs/authoritativeSourceRecordShape",
    "#/$defs/terminalSourceRecordShape",
]


def status_shape(status: str) -> str | None:
    if status in CANDIDATE_STATUSES:
        return "candidateRecordShape"
    if status in AUTHORITATIVE_SOURCE_STATUSES:
        return "authoritativeSourceRecordShape"
    if status in TERMINAL_SOURCE_STATUSES:
        return "terminalSourceRecordShape"
    return None


def authority_shape_errors(schema: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    one_of = schema.get("oneOf")
    if one_of != [{"$ref": ref} for ref in SHAPE_REFS]:
        errors.append("authority-shape: top_level_oneOf_drift")

    properties = schema.get("properties")
    authority = properties.get("authority_status") if isinstance(properties, Mapping) else None
    declared_statuses = set(authority.get("enum", [])) if isinstance(authority, Mapping) else set()
    if declared_statuses != ALL_STATUSES:
        errors.append("authority-shape: authority_status_domain_drift")

    defs = schema.get("$defs")
    if not isinstance(defs, Mapping):
        return sorted(set(errors + ["authority-shape: missing_defs"]))

    candidate = _shape_statuses(defs.get("candidateRecordShape"))
    active = _shape_statuses(defs.get("authoritativeSourceRecordShape"))
    terminal = _shape_statuses(defs.get("terminalSourceRecordShape"))

    if candidate != CANDIDATE_STATUSES:
        errors.append("authority-shape: candidate_shape_drift")
    if active != AUTHORITATIVE_SOURCE_STATUSES:
        errors.append("authority-shape: authoritative_source_shape_drift")
    if terminal != TERMINAL_SOURCE_STATUSES:
        errors.append("authority-shape: terminal_source_shape_drift")
    if (candidate & active) or (candidate & terminal) or (active & terminal):
        errors.append("authority-shape: shapes_not_disjoint")
    if candidate | active | terminal != ALL_STATUSES:
        errors.append("authority-shape: shapes_do_not_cover_status_domain")
    return sorted(set(errors))


def _shape_statuses(shape: Any) -> set[str]:
    if not isinstance(shape, Mapping):
        return set()
    required = shape.get("required")
    properties = shape.get("properties")
    if not isinstance(required, list) or "authority_status" not in required or not isinstance(properties, Mapping):
        return set()
    authority = properties.get("authority_status")
    if not isinstance(authority, Mapping):
        return set()
    if isinstance(authority.get("const"), str):
        return {authority["const"]}
    values = authority.get("enum")
    return set(values) if isinstance(values, list) else set()


def load_schema(root: Path = ROOT) -> Mapping[str, Any]:
    return json.loads((root / DECL_SCHEMA).read_text(encoding="utf-8"))
