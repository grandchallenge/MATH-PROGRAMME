#!/usr/bin/env python3
from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any, Iterable, Mapping

import yaml

ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "docs/council/submissions/GCL-TCS-00/GCL-TCS-00.policy.yaml"

EXPECTED_STANDARD_ID = "GCL-TCS-00"
EXPECTED_STANDARD_VERSION = "0.1.0"
EXPECTED_STANDARD_STATUS = "candidate"

REQUIRED_FIELDS = (
    "exception_id",
    "rule_id",
    "artifact_scope",
    "affected_content",
    "justification",
    "risk_assessment",
    "compensating_controls",
    "requested_by",
    "approved_by",
    "issued_date",
    "status",
)
DATE_FIELDS = ("review_date", "expiry_date")
INVALID_CONTROL_TOKENS = {"", "none", "n/a", "na", "tbd", "todo", "unknown"}


class ExceptionControlError(RuntimeError):
    pass


def _load_policy(root: Path = ROOT) -> dict[str, Any]:
    path = root / POLICY_PATH.relative_to(ROOT)
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ExceptionControlError("GCL-TCS policy must be a mapping")
    standard = raw.get("standard")
    if not isinstance(standard, dict):
        raise ExceptionControlError("GCL-TCS policy standard block missing")
    if (
        standard.get("id") != EXPECTED_STANDARD_ID
        or standard.get("version") != EXPECTED_STANDARD_VERSION
        or standard.get("status") != EXPECTED_STANDARD_STATUS
    ):
        raise ExceptionControlError("GCL-TCS candidate policy identity drift")
    model = raw.get("exception_model")
    if not isinstance(model, dict):
        raise ExceptionControlError("GCL-TCS exception_model missing")
    for key in ("non_waivable", "statuses"):
        values = model.get(key)
        if not isinstance(values, list) or not values or not all(isinstance(v, str) and v for v in values):
            raise ExceptionControlError(f"GCL-TCS exception_model.{key} invalid")
    return raw


def _parse_date(value: Any, field: str, errors: list[str]) -> date | None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{field}: missing_or_invalid_date")
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        errors.append(f"{field}: invalid_iso_date")
        return None


def _nonempty_text(record: Mapping[str, Any], field: str, errors: list[str]) -> str | None:
    value = record.get(field)
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{field}: missing_or_empty")
        return None
    return value.strip()


def _controls_valid(value: Any) -> bool:
    if not isinstance(value, list) or not value:
        return False
    for item in value:
        if not isinstance(item, str):
            return False
        if item.strip().lower() in INVALID_CONTROL_TOKENS:
            return False
    return True


def validate_exception_record(
    record: Any,
    *,
    authorized_approvers: Iterable[str] | None,
    as_of: date | None = None,
    root: Path = ROOT,
) -> list[str]:
    """Validate one artifact-exception record against GCL-TCS-00 candidate semantics.

    The caller supplies the governing authorized-approver set. The candidate standard
    does not yet define a complete profile owner/reviewer authority map, so this
    control refuses to invent one.
    """
    errors: list[str] = []
    if not isinstance(record, Mapping):
        return ["record: malformed_non_mapping"]

    policy = _load_policy(root)
    model = policy["exception_model"]
    statuses = set(model["statuses"])
    non_waivable = set(model["non_waivable"])

    for field in REQUIRED_FIELDS:
        if field not in record:
            errors.append(f"{field}: missing")

    for field in (
        "exception_id",
        "rule_id",
        "artifact_scope",
        "affected_content",
        "justification",
        "risk_assessment",
        "requested_by",
    ):
        _nonempty_text(record, field, errors)

    status = record.get("status")
    if not isinstance(status, str) or status not in statuses:
        errors.append("status: invalid")
        status = None

    issued = _parse_date(record.get("issued_date"), "issued_date", errors)

    rule_id = record.get("rule_id")
    if isinstance(rule_id, str) and rule_id in non_waivable:
        errors.append("rule_id: non_waivable_requirement")

    if not _controls_valid(record.get("compensating_controls")):
        errors.append("compensating_controls: missing_or_insufficient")

    approvers = (
        {item.strip() for item in authorized_approvers if isinstance(item, str) and item.strip()}
        if authorized_approvers is not None
        else set()
    )

    approved_by = record.get("approved_by")
    if status == "approved":
        if not approvers:
            errors.append("approved_by: approval_authority_unresolved")
        if not isinstance(approved_by, str) or not approved_by.strip():
            errors.append("approved_by: missing_or_invalid")
        elif approved_by.strip() not in approvers:
            errors.append("approved_by: unauthorized")

        review_present = isinstance(record.get("review_date"), str) and bool(record.get("review_date").strip())
        expiry_present = isinstance(record.get("expiry_date"), str) and bool(record.get("expiry_date").strip())
        if not (review_present or expiry_present):
            errors.append("lifecycle: approved_requires_review_or_expiry")
        review = _parse_date(record.get("review_date"), "review_date", errors) if review_present else None
        expiry = _parse_date(record.get("expiry_date"), "expiry_date", errors) if expiry_present else None

        if as_of is not None:
            if expiry is not None and expiry < as_of:
                errors.append("lifecycle: exception_expired")
            if review is not None and review < as_of:
                errors.append("lifecycle: review_overdue")
        if issued is not None:
            if review is not None and review < issued:
                errors.append("review_date: before_issued_date")
            if expiry is not None and expiry < issued:
                errors.append("expiry_date: before_issued_date")
    else:
        if "approved_by" in record and approved_by is not None and not isinstance(approved_by, str):
            errors.append("approved_by: invalid_type")

    return sorted(set(errors))


def evaluate_required_exceptions_for_promotion(
    *,
    required_exception_ids: Iterable[str],
    exception_records: Mapping[str, Any],
    authorized_approvers: Iterable[str] | None,
    as_of: date,
    root: Path = ROOT,
) -> list[str]:
    """Fail closed when a required exception is absent or not valid for promotion."""
    errors: list[str] = []
    required = {item for item in required_exception_ids if isinstance(item, str) and item}
    if not required:
        return errors

    for exception_id in sorted(required):
        if exception_id not in exception_records:
            errors.append(f"{exception_id}: required_exception_missing")
            continue
        record = exception_records[exception_id]
        record_errors = validate_exception_record(
            record,
            authorized_approvers=authorized_approvers,
            as_of=as_of,
            root=root,
        )
        if not isinstance(record, Mapping):
            errors.append(f"{exception_id}: required_exception_malformed")
            continue
        status = record.get("status")
        if status in {"expired", "revoked"}:
            errors.append(f"{exception_id}: required_exception_{status}")
        elif status != "approved":
            errors.append(f"{exception_id}: required_exception_not_approved")
        errors.extend(f"{exception_id}: {item}" for item in record_errors)

    return sorted(set(errors))


def main() -> int:
    policy = _load_policy(ROOT)
    print(
        f"{policy['standard']['id']} {policy['standard']['version']} "
        "exception control: candidate validator loaded"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
