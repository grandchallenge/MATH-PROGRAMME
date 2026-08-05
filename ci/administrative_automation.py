from __future__ import annotations

import hashlib
import json
import re
import subprocess
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable, Iterable

UTC = timezone.utc
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
PROCEDURE_RE = re.compile(r"^[a-z][a-z0-9_]*$")
SAFE_REPOSITORY_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")


class AutomationError(ValueError):
    pass


@dataclass(frozen=True)
class Occurrence:
    procedure_id: str
    due_at: datetime
    prepare_at: datetime
    freeze_at: datetime
    occurrence_key: str
    branch_name: str
    manifest_path: str


def parse_datetime(value: str) -> datetime:
    normalized = value.strip()
    if normalized.endswith("Z"):
        normalized = normalized[:-1] + "+00:00"
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        raise AutomationError(f"time must include an offset: {value}")
    return parsed.astimezone(UTC)


def iso_z(value: datetime) -> str:
    return value.astimezone(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_digest(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def occurrence_key(procedure_id: str, due_at: datetime) -> str:
    if not PROCEDURE_RE.fullmatch(procedure_id):
        raise AutomationError(f"unsafe procedure id: {procedure_id}")
    return f"{procedure_id}:{iso_z(due_at)}"


def occurrence_slug(procedure_id: str, due_at: datetime) -> str:
    due_slug = due_at.astimezone(UTC).strftime("%Y%m%dT%H%M%SZ")
    return f"{procedure_id}-{due_slug}"


def validate_config(config: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if config.get("schema_version") != "1.0.0":
        errors.append("automation schema_version must be 1.0.0")
    if config.get("control_id") != "MP-ADMIN-MAINT-001":
        errors.append("control_id drift")
    repositories = config.get("evidence_repositories")
    if not isinstance(repositories, list) or len(repositories) != 5:
        errors.append("exactly five evidence repositories are required")
    elif len(set(repositories)) != 5 or any(not SAFE_REPOSITORY_RE.fullmatch(item) for item in repositories):
        errors.append("evidence repositories are duplicated or unsafe")
    procedures = config.get("procedures")
    if not isinstance(procedures, dict) or not procedures:
        errors.append("procedures must be a non-empty object")
    else:
        for procedure_id, procedure in procedures.items():
            if not PROCEDURE_RE.fullmatch(procedure_id):
                errors.append(f"unsafe procedure id: {procedure_id}")
                continue
            lead = procedure.get("lead_minutes")
            freeze = procedure.get("freeze_minutes")
            if not isinstance(lead, int) or lead <= 0:
                errors.append(f"{procedure_id}: lead_minutes must be positive")
            if not isinstance(freeze, int) or freeze <= 0:
                errors.append(f"{procedure_id}: freeze_minutes must be positive")
            if isinstance(lead, int) and isinstance(freeze, int) and freeze >= lead:
                errors.append(f"{procedure_id}: freeze must occur after preparation and before due")
            globs = procedure.get("record_globs")
            if not isinstance(globs, list) or not globs or any(".." in item or item.startswith("/") for item in globs):
                errors.append(f"{procedure_id}: unsafe record_globs")
    authority = config.get("authority_boundary", {})
    forbidden = (
        "automated_approval",
        "automated_human_steward_disposition",
        "automated_merge",
        "automated_auto_merge",
        "branch_protection_bypass",
    )
    for field in forbidden:
        if authority.get(field) is not False:
            errors.append(f"authority boundary must set {field}=false")
    return errors


def completion_by_procedure(completion: dict[str, Any]) -> dict[str, datetime | None]:
    result: dict[str, datetime | None] = {}
    for procedure_id, state in completion.get("procedures", {}).items():
        raw = state.get("completed_through_utc")
        result[procedure_id] = parse_datetime(raw) if raw else None
    return result


def iter_due_occurrences(procedure: dict[str, Any], completed_through: datetime | None) -> Iterable[datetime]:
    first_due = parse_datetime(procedure["first_due_utc"])
    active_through = parse_datetime(procedure["active_through_utc"])
    interval_minutes = procedure.get("interval_minutes")
    if interval_minutes is None:
        candidates = [first_due]
    else:
        if not isinstance(interval_minutes, int) or interval_minutes <= 0:
            raise AutomationError("interval_minutes must be null or positive")
        interval = timedelta(minutes=interval_minutes)
        count = int((active_through - first_due) // interval)
        candidates = [first_due + index * interval for index in range(count + 1)]
    for due in candidates:
        if due <= active_through and (completed_through is None or due > completed_through):
            yield due


def build_occurrence(config: dict[str, Any], procedure_id: str, due_at: datetime) -> Occurrence:
    procedure = config["procedures"][procedure_id]
    lead = timedelta(minutes=procedure["lead_minutes"])
    freeze = timedelta(minutes=procedure["freeze_minutes"])
    slug = occurrence_slug(procedure_id, due_at)
    return Occurrence(
        procedure_id=procedure_id,
        due_at=due_at,
        prepare_at=due_at - lead,
        freeze_at=due_at - freeze,
        occurrence_key=occurrence_key(procedure_id, due_at),
        branch_name=f"automation/maintenance/{slug}",
        manifest_path=f"governance/administrative_candidates/{slug}.json",
    )


def preparation_occurrences(
    config: dict[str, Any],
    registry: dict[str, Any],
    completion: dict[str, Any],
    now: datetime,
) -> list[Occurrence]:
    completed = completion_by_procedure(completion)
    registry_by_id = {item["id"]: item for item in registry["procedures"]}
    result: list[Occurrence] = []
    for procedure_id in config["procedures"]:
        if procedure_id not in registry_by_id:
            raise AutomationError(f"procedure missing from protected trigger registry: {procedure_id}")
        for due in iter_due_occurrences(registry_by_id[procedure_id], completed.get(procedure_id)):
            occurrence = build_occurrence(config, procedure_id, due)
            if occurrence.prepare_at <= now <= occurrence.due_at:
                result.append(occurrence)
    return sorted(result, key=lambda item: (item.due_at, item.procedure_id))


def candidate_mutation_allowed(occurrence: Occurrence, now: datetime) -> bool:
    return now < occurrence.freeze_at


def build_candidate_manifest(
    occurrence: Occurrence,
    generated_at: datetime,
    source_head: str,
    repository_state: list[dict[str, Any]],
    issue_number: int | None = None,
    pull_request_number: int | None = None,
) -> dict[str, Any]:
    if not SHA_RE.fullmatch(source_head):
        raise AutomationError("invalid source protected head")
    normalized_state = sorted(repository_state, key=lambda item: item["repository"])
    evidence_digest = canonical_digest(normalized_state)
    return {
        "schema_version": "1.0.0",
        "state": "CANDIDATE_PREPARED",
        "control_id": "MP-ADMIN-MAINT-001",
        "occurrence_key": occurrence.occurrence_key,
        "procedure_id": occurrence.procedure_id,
        "scheduled_due_at": iso_z(occurrence.due_at),
        "prepare_at": iso_z(occurrence.prepare_at),
        "freeze_at": iso_z(occurrence.freeze_at),
        "generated_at": iso_z(generated_at),
        "source_protected_head": source_head,
        "branch": occurrence.branch_name,
        "manifest_path": occurrence.manifest_path,
        "issue_number": issue_number,
        "pull_request_number": pull_request_number,
        "evidence_digest": evidence_digest,
        "repository_state": normalized_state,
        "authority_boundary": {
            "protected_authority_created": False,
            "independent_approval_created": False,
            "human_steward_disposition_created": False,
            "merge_authorized": False,
            "merge_performed": False,
            "candidate_is_final_record": False,
        },
        "claim_boundaries": {
            "mathematical_target_proved": False,
            "campaign_admitted": False,
            "source_verified": False,
            "cert_route_registered": False,
            "adjudication_authorized": False,
            "certificate_issued": False,
            "external_claim_authorized": False,
        },
    }


def validate_candidate_manifest(manifest: dict[str, Any], occurrence: Occurrence | None = None) -> list[str]:
    errors: list[str] = []
    if manifest.get("state") != "CANDIDATE_PREPARED":
        errors.append("candidate state drift")
    if occurrence:
        expected = {
            "occurrence_key": occurrence.occurrence_key,
            "procedure_id": occurrence.procedure_id,
            "scheduled_due_at": iso_z(occurrence.due_at),
            "prepare_at": iso_z(occurrence.prepare_at),
            "freeze_at": iso_z(occurrence.freeze_at),
            "branch": occurrence.branch_name,
            "manifest_path": occurrence.manifest_path,
        }
        for field, value in expected.items():
            if manifest.get(field) != value:
                errors.append(f"candidate {field} drift")
    if not SHA_RE.fullmatch(str(manifest.get("source_protected_head", ""))):
        errors.append("candidate source head invalid")
    repositories = manifest.get("repository_state")
    if not isinstance(repositories, list) or len(repositories) != 5:
        errors.append("candidate repository evidence incomplete")
    elif canonical_digest(sorted(repositories, key=lambda item: item["repository"])) != manifest.get("evidence_digest"):
        errors.append("candidate evidence digest mismatch")
    authority = manifest.get("authority_boundary", {})
    if not authority or any(value is not False for value in authority.values()):
        errors.append("candidate authority inflation")
    boundaries = manifest.get("claim_boundaries", {})
    if not boundaries or any(value is not False for value in boundaries.values()):
        errors.append("candidate claim inflation")
    return errors


GitRunner = Callable[[list[str]], str]


def default_git_runner(args: list[str]) -> str:
    completed = subprocess.run(["git", *args], check=True, text=True, capture_output=True)
    return completed.stdout.strip()


def record_due(record: dict[str, Any], due_fields: list[str]) -> str | None:
    for field in due_fields:
        value = record.get(field)
        if isinstance(value, str) and value:
            return iso_z(parse_datetime(value))
    return None


def receipt_for_record(
    root: Path,
    path: Path,
    procedure_id: str,
    due_fields: list[str],
    head_sha: str,
    git_runner: GitRunner,
) -> dict[str, Any] | None:
    record = load_json(path)
    status = str(record.get("status", ""))
    if not (status.startswith("COMPLETE") or status.startswith("PROTECTED_")):
        return None
    due = record_due(record, due_fields)
    if not due:
        return None
    relative = path.relative_to(root).as_posix()
    merge_commit = git_runner(["log", "--diff-filter=A", "--format=%H", "-1", "--", relative])
    if not SHA_RE.fullmatch(merge_commit):
        raise AutomationError(f"{relative}: no protected introduction commit")
    ancestry = subprocess.run(["git", "merge-base", "--is-ancestor", merge_commit, head_sha], cwd=root, check=False)
    if ancestry.returncode != 0:
        raise AutomationError(f"{relative}: introduction commit is not ancestral to protected head")
    parents = git_runner(["show", "-s", "--format=%P", merge_commit]).split()
    message = git_runner(["show", "-s", "--format=%B", merge_commit])
    if len(parents) < 2:
        raise AutomationError(f"{relative}: protected receipt is not a merge commit")
    pr_match = re.search(r"Merge PR #(\d+)", message)
    head_match = re.search(r"exact head ([0-9a-f]{40})", message)
    disposition_match = re.search(r"Disposition:\s*([A-Z0-9_]+)", message)
    if not (pr_match and head_match and disposition_match):
        raise AutomationError(f"{relative}: merge receipt lacks PR, exact head, or disposition")
    return {
        "procedure_id": procedure_id,
        "scheduled_due_at": due,
        "record_path": relative,
        "record_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "merge_commit": merge_commit,
        "reviewed_head": head_match.group(1),
        "pull_request": int(pr_match.group(1)),
        "disposition": disposition_match.group(1),
        "receipt_state": "PROTECTED_COMPLETE",
    }


def derive_completion_state(
    root: Path,
    config: dict[str, Any],
    head_sha: str,
    git_runner: GitRunner = default_git_runner,
) -> dict[str, Any]:
    if not SHA_RE.fullmatch(head_sha):
        raise AutomationError("protected head SHA is invalid")
    receipts: list[dict[str, Any]] = []
    receipts.extend(config.get("bootstrap_receipts", []))
    for procedure_id, procedure in config["procedures"].items():
        for pattern in procedure["record_globs"]:
            for path in sorted(root.glob(pattern)):
                receipt = receipt_for_record(root, path, procedure_id, procedure.get("due_fields", ["scheduled_due_at"]), head_sha, git_runner)
                if receipt:
                    floor_raw = procedure.get("receipt_floor_utc")
                    if floor_raw and parse_datetime(receipt["scheduled_due_at"]) < parse_datetime(floor_raw):
                        continue
                    receipts.append(receipt)

    for receipt in config.get("bootstrap_receipts", []):
        merge_commit = str(receipt.get("merge_commit", ""))
        if not SHA_RE.fullmatch(merge_commit):
            raise AutomationError("bootstrap receipt merge commit invalid")
        ancestry = subprocess.run(["git", "merge-base", "--is-ancestor", merge_commit, head_sha], cwd=root, check=False)
        if ancestry.returncode != 0:
            raise AutomationError("bootstrap receipt is not ancestral to protected head")

    seen: dict[tuple[str, str], dict[str, Any]] = {}
    for receipt in receipts:
        if receipt.get("receipt_state") != "PROTECTED_COMPLETE":
            raise AutomationError("non-protected receipt cannot advance completion")
        if not SHA_RE.fullmatch(str(receipt.get("merge_commit", ""))):
            raise AutomationError("receipt merge commit invalid")
        key = (receipt["procedure_id"], iso_z(parse_datetime(receipt["scheduled_due_at"])))
        normalized = {**receipt, "scheduled_due_at": key[1]}
        previous = seen.get(key)
        if previous and canonical_digest(previous) != canonical_digest(normalized):
            raise AutomationError(f"conflicting protected receipts for {key[0]} {key[1]}")
        seen[key] = normalized

    procedures: dict[str, Any] = {}
    for procedure_id in config["procedures"]:
        matching = [receipt for (kind, _), receipt in seen.items() if kind == procedure_id]
        matching.sort(key=lambda item: parse_datetime(item["scheduled_due_at"]))
        procedures[procedure_id] = {
            "completed_through_utc": matching[-1]["scheduled_due_at"] if matching else None,
            "receipt_count": len(matching),
            "receipts": matching,
        }
    return {
        "schema_version": "1.0.0",
        "control_id": "MP-ADMIN-MAINT-001",
        "derived_from_protected_head": head_sha,
        "state": "PROTECTED_RECEIPT_DERIVED",
        "procedures": procedures,
        "authority_boundary": {
            "issues_are_authority": False,
            "workflow_artifacts_are_authority": False,
            "draft_pull_requests_are_authority": False,
            "unmerged_branches_are_authority": False,
            "protected_merge_receipts_required": True,
        },
    }


def validate_completion_state(state: dict[str, Any], previous: dict[str, Any] | None = None) -> list[str]:
    errors: list[str] = []
    if state.get("state") != "PROTECTED_RECEIPT_DERIVED":
        errors.append("completion state must be receipt-derived")
    if not SHA_RE.fullmatch(str(state.get("derived_from_protected_head", ""))):
        errors.append("completion state protected head invalid")
    authority = state.get("authority_boundary", {})
    if authority.get("protected_merge_receipts_required") is not True:
        errors.append("protected merge receipts must be required")
    for field in ("issues_are_authority", "workflow_artifacts_are_authority", "draft_pull_requests_are_authority", "unmerged_branches_are_authority"):
        if authority.get(field) is not False:
            errors.append(f"completion authority inflation: {field}")
    procedures = state.get("procedures", {})
    for procedure_id, procedure in procedures.items():
        receipts = procedure.get("receipts", [])
        dates = [parse_datetime(item["scheduled_due_at"]) for item in receipts]
        if dates != sorted(dates) or len(dates) != len(set(dates)):
            errors.append(f"{procedure_id}: receipts are duplicate or unordered")
        expected = iso_z(dates[-1]) if dates else None
        if procedure.get("completed_through_utc") != expected:
            errors.append(f"{procedure_id}: completed_through mismatch")
        if procedure.get("receipt_count") != len(receipts):
            errors.append(f"{procedure_id}: receipt_count mismatch")
        for receipt in receipts:
            if receipt.get("receipt_state") != "PROTECTED_COMPLETE":
                errors.append(f"{procedure_id}: non-protected receipt")
    if previous:
        for procedure_id, old in previous.get("procedures", {}).items():
            old_raw = old.get("completed_through_utc")
            new_raw = procedures.get(procedure_id, {}).get("completed_through_utc")
            if old_raw and (not new_raw or parse_datetime(new_raw) < parse_datetime(old_raw)):
                errors.append(f"{procedure_id}: completion state regression")
    return errors


def apply_completion_to_registry(registry: dict[str, Any], completion: dict[str, Any]) -> dict[str, Any]:
    patched = json.loads(json.dumps(registry))
    by_id = completion.get("procedures", {})
    for procedure in patched["procedures"]:
        state = by_id.get(procedure["id"], {})
        procedure["completed_through_utc"] = state.get("completed_through_utc")
        procedure["completion_source"] = "protected_receipt_derivation"
    return patched
