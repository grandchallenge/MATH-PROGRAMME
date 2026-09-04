from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Mapping

import yaml

ROOT = Path(__file__).resolve().parents[1]
DECL_SCHEMA = Path("docs/council/submissions/GCL-TCS-00/schemas/gcl-tcs-conformance.schema.json")
RECORD_SCHEMA = Path("docs/council/submissions/GCL-TCS-00/schemas/gcl-tcs-record-contracts.schema.json")
IMMUTABLE_REVISION_PATTERN = r"^(?:git-(?:blob|commit|tree):[0-9a-f]{40}|sha256:[0-9a-f]{64}|[0-9a-f]{40})$"
IMMUTABLE_REVISION_RE = re.compile(IMMUTABLE_REVISION_PATTERN)

GOVERNED_REVISION_ROOTS = (
    Path("governance/gcl_tcs_pilots"),
    Path("governance/rebuild_evidence/GHOS-ESTATE-ROLLOUT-001/gcl-tcs"),
    Path("docs/council/submissions/GCL-POS-01"),
)


def is_immutable_revision(value: Any) -> bool:
    return isinstance(value, str) and IMMUTABLE_REVISION_RE.fullmatch(value) is not None


def binding_errors(
    declaration: Mapping[str, Any],
    gate_record: Mapping[str, Any],
    review_record: Mapping[str, Any],
) -> list[str]:
    errors: list[str] = []
    source_revision = declaration.get("source_revision")
    gate_revision = gate_record.get("reviewed_revision")
    review_revision = review_record.get("reviewed_revision")

    if not is_immutable_revision(source_revision):
        errors.append("binding: declaration_revision_not_immutable")
    if not is_immutable_revision(gate_revision):
        errors.append("binding: gate_revision_not_immutable")
    if not is_immutable_revision(review_revision):
        errors.append("binding: review_revision_not_immutable")

    if gate_record.get("artifact_id") != declaration.get("artifact_id"):
        errors.append("binding: artifact_id_mismatch")
    if gate_record.get("gate_id") != review_record.get("gate_id"):
        errors.append("binding: gate_id_mismatch")
    if source_revision != gate_revision or gate_revision != review_revision:
        errors.append("binding: revision_mismatch")
    return sorted(set(errors))


def schema_binding_errors(
    declaration_schema: Mapping[str, Any], record_schema: Mapping[str, Any]
) -> list[str]:
    errors: list[str] = []
    decl_defs = declaration_schema.get("$defs")
    record_defs = record_schema.get("$defs")
    if not isinstance(decl_defs, Mapping) or not isinstance(record_defs, Mapping):
        return ["schema: missing_defs"]

    for name, defs in (("declaration", decl_defs), ("record", record_defs)):
        immutable = defs.get("immutableRevision")
        if not isinstance(immutable, Mapping) or immutable.get("pattern") != IMMUTABLE_REVISION_PATTERN:
            errors.append(f"schema: {name}_immutable_revision_contract_drift")

    decl_props = declaration_schema.get("properties")
    if not isinstance(decl_props, Mapping) or decl_props.get("source_revision") != {"$ref": "#/$defs/immutableRevision"}:
        errors.append("schema: declaration_source_revision_not_bound")

    expected_inline = {"type": "string", "pattern": IMMUTABLE_REVISION_PATTERN}
    declaration_review = decl_defs.get("reviewReference")
    declaration_review_props = declaration_review.get("properties") if isinstance(declaration_review, Mapping) else None
    if not isinstance(declaration_review_props, Mapping) or declaration_review_props.get("reviewed_revision") != expected_inline:
        errors.append("schema: declaration_review_reference_revision_not_bound")

    review = record_defs.get("reviewRecord")
    gate = record_defs.get("gateRecord")
    review_props = review.get("properties") if isinstance(review, Mapping) else None
    gate_props = gate.get("properties") if isinstance(gate, Mapping) else None
    if not isinstance(review_props, Mapping) or review_props.get("reviewed_revision") != expected_inline:
        errors.append("schema: review_revision_not_bound")
    if not isinstance(gate_props, Mapping) or gate_props.get("reviewed_revision") != expected_inline:
        errors.append("schema: gate_revision_not_bound")
    return sorted(set(errors))


def _load(path: Path) -> Any:
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".json":
        return json.loads(text)
    return yaml.safe_load(text)


def _walk_revision_values(value: Any, path: str = "") -> list[tuple[str, Any]]:
    found: list[tuple[str, Any]] = []
    if isinstance(value, Mapping):
        for key, child in value.items():
            child_path = f"{path}.{key}" if path else str(key)
            if key in {"source_revision", "reviewed_revision"}:
                found.append((child_path, child))
            found.extend(_walk_revision_values(child, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            found.extend(_walk_revision_values(child, f"{path}[{index}]"))
    return found


def governed_revision_errors(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    observed = 0
    for relative_root in GOVERNED_REVISION_ROOTS:
        absolute_root = root / relative_root
        if not absolute_root.exists():
            continue
        for path in sorted(absolute_root.rglob("*")):
            if not path.is_file() or path.suffix not in {".yaml", ".yml", ".json"}:
                continue
            try:
                payload = _load(path)
            except Exception:
                continue
            for field_path, value in _walk_revision_values(payload):
                observed += 1
                if not is_immutable_revision(value):
                    errors.append(f"{path.relative_to(root)}:{field_path}:mutable_or_malformed_revision:{value}")
    if observed == 0:
        errors.append("governed_records: no_revision_values_observed")
    return sorted(set(errors))
