from __future__ import annotations

import hashlib
import re
import subprocess
from pathlib import Path
from typing import Any, Callable

import administrative_automation as aa

GitRunner = Callable[[list[str]], str]


def default_git_runner(args: list[str]) -> str:
    completed = subprocess.run(["git", *args], check=True, text=True, capture_output=True)
    return completed.stdout.strip()


def receipt_for_record(
    root: Path,
    path: Path,
    procedure_id: str,
    due_fields: list[str],
    head_sha: str,
    git_runner: GitRunner,
) -> dict[str, Any] | None:
    record = aa.load_json(path)
    status = str(record.get("status", ""))
    if not (status.startswith("COMPLETE") or status.startswith("PROTECTED_")):
        return None
    due = aa.record_due(record, due_fields)
    if not due:
        return None
    relative = path.relative_to(root).as_posix()
    merge_commit = git_runner(
        ["log", "--first-parent", "--diff-filter=A", "--format=%H", "-1", head_sha, "--", relative]
    )
    if not aa.SHA_RE.fullmatch(merge_commit):
        raise aa.AutomationError(f"{relative}: no protected first-parent introduction commit")
    ancestry = subprocess.run(
        ["git", "merge-base", "--is-ancestor", merge_commit, head_sha],
        cwd=root,
        check=False,
    )
    if ancestry.returncode != 0:
        raise aa.AutomationError(f"{relative}: introduction commit is not ancestral to protected head")
    parents = git_runner(["show", "-s", "--format=%P", merge_commit]).split()
    message = git_runner(["show", "-s", "--format=%B", merge_commit])
    if len(parents) < 2:
        raise aa.AutomationError(f"{relative}: protected receipt is not a merge commit")
    pr_match = re.search(r"Merge PR #(\d+)", message)
    head_match = re.search(r"exact head ([0-9a-f]{40})", message)
    disposition_match = re.search(r"Disposition:\s*([A-Z0-9_]+)", message)
    if not (pr_match and head_match and disposition_match):
        raise aa.AutomationError(f"{relative}: merge receipt lacks PR, exact head, or disposition")
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
    if not aa.SHA_RE.fullmatch(head_sha):
        raise aa.AutomationError("protected head SHA is invalid")
    receipts: list[dict[str, Any]] = list(config.get("bootstrap_receipts", []))

    for procedure_id, procedure in config["procedures"].items():
        due_fields = procedure.get("due_fields", ["scheduled_due_at"])
        floor_raw = procedure.get("receipt_floor_utc")
        floor = aa.parse_datetime(floor_raw) if floor_raw else None
        for pattern in procedure["record_globs"]:
            for path in sorted(root.glob(pattern)):
                record = aa.load_json(path)
                due_raw = aa.record_due(record, due_fields)
                if not due_raw:
                    continue
                if floor and aa.parse_datetime(due_raw) < floor:
                    continue
                receipt = receipt_for_record(
                    root,
                    path,
                    procedure_id,
                    due_fields,
                    head_sha,
                    git_runner,
                )
                if receipt:
                    receipts.append(receipt)

    for receipt in config.get("bootstrap_receipts", []):
        merge_commit = str(receipt.get("merge_commit", ""))
        if not aa.SHA_RE.fullmatch(merge_commit):
            raise aa.AutomationError("bootstrap receipt merge commit invalid")
        ancestry = subprocess.run(
            ["git", "merge-base", "--is-ancestor", merge_commit, head_sha],
            cwd=root,
            check=False,
        )
        if ancestry.returncode != 0:
            raise aa.AutomationError("bootstrap receipt is not ancestral to protected head")

    seen: dict[tuple[str, str], dict[str, Any]] = {}
    for receipt in receipts:
        if receipt.get("receipt_state") != "PROTECTED_COMPLETE":
            raise aa.AutomationError("non-protected receipt cannot advance completion")
        if not aa.SHA_RE.fullmatch(str(receipt.get("merge_commit", ""))):
            raise aa.AutomationError("receipt merge commit invalid")
        key = (
            receipt["procedure_id"],
            aa.iso_z(aa.parse_datetime(receipt["scheduled_due_at"])),
        )
        normalized = {**receipt, "scheduled_due_at": key[1]}
        previous = seen.get(key)
        if previous and aa.canonical_digest(previous) != aa.canonical_digest(normalized):
            raise aa.AutomationError(f"conflicting protected receipts for {key[0]} {key[1]}")
        seen[key] = normalized

    procedures: dict[str, Any] = {}
    for procedure_id in config["procedures"]:
        matching = [receipt for (kind, _), receipt in seen.items() if kind == procedure_id]
        matching.sort(key=lambda item: aa.parse_datetime(item["scheduled_due_at"]))
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
