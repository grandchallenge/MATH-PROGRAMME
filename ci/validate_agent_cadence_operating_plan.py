from __future__ import annotations

import hashlib
import json
import re
import subprocess
from decimal import Decimal
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "governance" / "agent_cadence_operating_plan_transform.json"
DURATION_RE = re.compile(r"^P(?:(?P<days>\d+)D)?(?:T(?:(?P<hours>\d+)H)?(?:(?P<minutes>\d+)M)?)?$")
REQUIRED_NONCOMPRESSED = {
    "exact_head_review",
    "independent_review",
    "required_checks",
    "protected_merge",
    "protected_main_readback",
    "adverse_evidence_retention",
    "claim_boundaries",
    "reserved_human_authority",
}
ACTIVATION_FIELDS = {
    "plan_candidate_head",
    "plan_file_sha256",
    "transform_file_sha256",
    "council_matter_sha256",
    "council_disposition_sha256",
    "human_steward_evidence",
    "protected_merge_sha",
    "protected_main_plan_blob",
    "protected_main_plan_sha256",
    "protected_main_transform_sha256",
    "readback_run",
    "readback_completed_at_utc",
    "t0_utc",
}


def duration_seconds(label: str) -> int:
    match = DURATION_RE.fullmatch(label)
    if not match or not any(match.groupdict().values()):
        raise ValueError(f"invalid supported ISO-8601 duration: {label}")
    days = int(match.group("days") or 0)
    hours = int(match.group("hours") or 0)
    minutes = int(match.group("minutes") or 0)
    if hours >= 24 or minutes >= 60:
        raise ValueError(f"non-canonical duration: {label}")
    return days * 86400 + hours * 3600 + minutes * 60


def git_blob_sha(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def _check_duration(item: dict[str, Any], label_key: str, seconds_key: str, errors: list[str], identity: str) -> None:
    try:
        parsed = duration_seconds(str(item.get(label_key, "")))
    except ValueError as exc:
        errors.append(f"{identity}: {exc}")
        return
    if parsed != int(item.get(seconds_key, -1)):
        errors.append(f"{identity}: {label_key} does not match {seconds_key}")


def _load_bound_source(value: dict[str, Any], errors: list[str]) -> dict[str, Any] | None:
    evidence = value.get("source_evidence", {})
    required = {"repository", "commit", "path", "git_blob", "sha256", "source_schedule_id"}
    if not isinstance(evidence, dict) or not required.issubset(evidence):
        errors.append("source_evidence is incomplete")
        return None
    try:
        result = subprocess.run(
            ["git", "show", f"{evidence['commit']}:{evidence['path']}"],
            cwd=ROOT,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except (OSError, subprocess.CalledProcessError):
        errors.append("immutable predecessor cannot be read from its bound commit and path")
        return None
    data = result.stdout
    if hashlib.sha256(data).hexdigest() != evidence["sha256"]:
        errors.append("immutable predecessor SHA-256 mismatch")
    if git_blob_sha(data) != evidence["git_blob"]:
        errors.append("immutable predecessor Git blob mismatch")
    try:
        source = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        errors.append("immutable predecessor is not valid UTF-8 JSON")
        return None
    if source.get("source_schedule_id") != evidence["source_schedule_id"]:
        errors.append("immutable predecessor schedule identity mismatch")
    return source


def _check_source_correspondence(value: dict[str, Any], source: dict[str, Any], errors: list[str]) -> None:
    if value.get("source_plan_id") != source.get("source_plan_id"):
        errors.append("source plan identity does not match immutable predecessor")
    if value.get("source_total") != source.get("total"):
        errors.append("source total does not match immutable predecessor")
    mappings = (
        ("phase_durations", "phase", "source_duration", "source_seconds"),
        ("milestone_offsets", "gate", "source_duration", "source_seconds"),
        ("cadence_offsets", "name", "source_duration", "source_seconds"),
    )
    for collection, identity_key, duration_key, seconds_key in mappings:
        source_items = {item[identity_key]: item for item in source.get(collection, [])}
        for item in value.get(collection, []):
            identity = item.get(identity_key)
            expected = source_items.get(identity)
            if expected is None:
                errors.append(f"{collection} {identity} absent from immutable predecessor")
                continue
            if item.get(duration_key) != expected.get("duration") or item.get(seconds_key) != expected.get("seconds"):
                errors.append(f"{collection} {identity} differs from immutable predecessor")
    if set(source.get("requirements_not_subject_to_time_compression", [])) != set(value.get("noncompressed_requirements", [])):
        errors.append("noncompressed requirements differ from immutable predecessor")


def validate(path: Path = DEFAULT_MANIFEST) -> list[str]:
    errors: list[str] = []
    value: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
    factor = Decimal(str(value.get("factor")))
    if factor != Decimal("0.1"):
        errors.append("factor must be exactly 0.1")

    source = _load_bound_source(value, errors)
    if source is not None:
        _check_source_correspondence(value, source, errors)

    source_total_object = value.get("source_total", {})
    target_total_object = value.get("target_total", {})
    _check_duration(source_total_object, "duration", "seconds", errors, "source total")
    _check_duration(target_total_object, "duration", "seconds", errors, "target total")
    source_total = int(source_total_object.get("seconds", -1))
    target_total = int(target_total_object.get("seconds", -1))
    if Decimal(source_total) * factor != Decimal(target_total):
        errors.append("total duration is not an exact 0.1 transform")

    phases = value.get("phase_durations", [])
    if not isinstance(phases, list) or len(phases) != 4:
        errors.append("exactly four phase durations are required")
        phases = []
    cumulative = 0
    source_phase_total = 0
    for phase in phases:
        identity = str(phase.get("phase"))
        _check_duration(phase, "source_duration", "source_seconds", errors, f"phase {identity} source")
        _check_duration(phase, "target_duration", "target_seconds", errors, f"phase {identity} target")
        _check_duration(phase, "target_cumulative_duration", "target_cumulative_seconds", errors, f"phase {identity} cumulative")
        source_seconds = int(phase.get("source_seconds", -1))
        target_seconds = int(phase.get("target_seconds", -1))
        cumulative += target_seconds
        source_phase_total += source_seconds
        if Decimal(source_seconds) * factor != Decimal(target_seconds):
            errors.append(f"phase {identity} is not an exact 0.1 transform")
        if int(phase.get("target_cumulative_seconds", -1)) != cumulative:
            errors.append(f"phase {identity} cumulative offset is incorrect")
    if source_phase_total != source_total or cumulative != target_total:
        errors.append("phase totals do not match plan totals")

    for collection_name in ("milestone_offsets", "cadence_offsets"):
        collection = value.get(collection_name, [])
        if not isinstance(collection, list) or not collection:
            errors.append(f"{collection_name} must be a non-empty array")
            continue
        for item in collection:
            identity = str(item.get("gate", item.get("name", "unknown")))
            _check_duration(item, "source_duration", "source_seconds", errors, f"{collection_name} {identity} source")
            _check_duration(item, "target_duration", "target_seconds", errors, f"{collection_name} {identity} target")
            source_seconds = int(item.get("source_seconds", -1))
            target_seconds = int(item.get("target_seconds", -1))
            if Decimal(source_seconds) * factor != Decimal(target_seconds):
                errors.append(f"{collection_name} {identity} is not an exact transform")

    dependency = value.get("dependency_contract", {})
    hard_predecessor = dependency.get("hard_predecessor")
    execution_gates = dependency.get("execution_gates", [])
    dependencies = dependency.get("dependencies", {})
    if hard_predecessor != "OPS-A" or set(execution_gates) != set(dependencies):
        errors.append("dependency contract gate set or hard predecessor is invalid")
    for gate in execution_gates:
        if hard_predecessor not in dependencies.get(gate, []):
            errors.append(f"execution gate {gate} does not depend on OPS-A")

    sequence = value.get("terminal_sequence", [])
    sequence_seconds: list[int] = []
    for item in sequence:
        _check_duration(item, "offset", "seconds", errors, f"terminal sequence {item.get('state')}")
        sequence_seconds.append(int(item.get("seconds", -1)))
    if [item.get("state") for item in sequence] != ["observation_cutoff", "ADM-B", "ADM-03", "terminal_packet"]:
        errors.append("terminal sequence state order is invalid")
    if sequence_seconds != sorted(set(sequence_seconds)) or not sequence_seconds or sequence_seconds[-1] != target_total:
        errors.append("terminal sequence offsets are not strictly ordered through P9D")

    noncompressed = set(value.get("noncompressed_requirements", []))
    missing = sorted(REQUIRED_NONCOMPRESSED - noncompressed)
    if missing:
        errors.append("missing noncompressed requirements: " + ", ".join(missing))

    schema_path = ROOT / str(value.get("activation_receipt_schema", ""))
    if not schema_path.is_file():
        errors.append("activation receipt schema is missing")
    else:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        if schema.get("additionalProperties") is not False or not ACTIVATION_FIELDS.issubset(schema.get("required", [])):
            errors.append("activation receipt schema does not bind the required identities")

    plan_path = ROOT / str(value.get("plan_path", ""))
    if not plan_path.is_file():
        errors.append("target plan path is missing")
    else:
        plan = plan_path.read_text(encoding="utf-8")
        required_tokens = {
            str(value.get("target_plan_id")),
            "PT4H48M",
            "P2DT12H",
            "P5DT9H36M",
            "P8DT4H48M",
            "P9D",
            "schemas/agent_cadence_operating_plan_activation.schema.json",
            "`OPS-A` is a hard predecessor",
            "PENDING_AT_CUTOFF",
            "FAILED_AT_CUTOFF",
        }
        for token in sorted(required_tokens):
            if token not in plan:
                errors.append(f"target plan is missing contract token: {token}")
        for stale in ("90-day result", "named human sponsor", "weekly review"):
            if stale in plan.lower():
                errors.append(f"target plan retains stale terminology: {stale}")
    return errors


def main() -> int:
    errors = validate()
    if errors:
        for error in errors:
            print(f"agent cadence operating plan: {error}")
        return 1
    print("agent cadence operating plan deadline transform and execution contract valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
