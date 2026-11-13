#!/usr/bin/env python3
"""Validate scoped RESULT/1 receipts for individual Erdős proof-verification tasks.

This is a fail-closed, read-only verifier. A GitHub comment, this validator,
and an operational reservation do not themselves confer execution authority,
mathematical acceptance, or protected admission.
"""
from __future__ import annotations

import re
from typing import Iterable

TASK = re.compile(r"ERDOS-PV-(\d{4})-([ABCD])\Z")
SHA256 = re.compile(r"[0-9a-f]{64}\Z")
FIELDS = ("ASSIGNMENT_ID", "PROBLEM_ID", "PHASE", "COHORT_ISSUE",
          "SOURCE_ISSUE", "SOURCE_BODY_SHA256", "DISPOSITION",
          "EVIDENCE_REF", "CLAIM_REF")
ALLOWED_DISPOSITIONS = {"SOURCE_SCOPE_RECONCILED_CANDIDATE",
                        "BOUNDED_RESULT_RETURNED", "EVIDENCE_BLOCKED"}


def parse_result(body: str) -> dict:
    if not isinstance(body, str) or not body.startswith("RESULT/1\n"):
        raise ValueError("missing exact RESULT/1 header")
    data = {}
    for line in body.splitlines()[1:]:
        if line.startswith("## "):
            break
        if not line.strip():
            continue
        m = re.fullmatch(r"([A-Z_]+): (.+)", line)
        if not m or m.group(1) not in FIELDS or m.group(1) in data:
            raise ValueError("malformed, duplicate or unrecognized RESULT/1 field")
        data[m.group(1)] = m.group(2)
    if set(data) != set(FIELDS):
        raise ValueError("missing or unexpected RESULT/1 fields")
    m = TASK.fullmatch(data["ASSIGNMENT_ID"])
    if not m or int(data["PROBLEM_ID"]) != int(m.group(1)) or data["PHASE"] != m.group(2):
        raise ValueError("assignment, problem and phase disagree")
    if not SHA256.fullmatch(data["SOURCE_BODY_SHA256"]):
        raise ValueError("source SHA256 malformed")
    for field in ("COHORT_ISSUE", "SOURCE_ISSUE"):
        if not data[field].isdigit() or int(data[field]) < 1:
            raise ValueError("invalid issue identifier")
    if data["DISPOSITION"] not in ALLOWED_DISPOSITIONS:
        raise ValueError("unsupported disposition or false acceptance claim")
    if not data["EVIDENCE_REF"].startswith(
        "governance/erdos_proof_verification/evidence/"
    ):
        raise ValueError("return evidence is not in protected proof-verification lane")
    if data["CLAIM_REF"] != "refs/heads/gcl-pv-claims/" + data["ASSIGNMENT_ID"]:
        raise ValueError("wrong per-task claim-ref binding")
    return data


def validate_return(row: dict, stage: str, body: str, existing_comments: Iterable[str] = ()) -> dict:
    data = parse_result(body)
    n = row["problem_id"]
    task = row["stage_work_items"][stage]
    if (data["ASSIGNMENT_ID"] != task["task_id"]
        or int(data["PROBLEM_ID"]) != n
        or data["PHASE"] != stage
        or int(data["COHORT_ISSUE"]) != task["cohort_issue_number"]
        or int(data["SOURCE_ISSUE"]) != row["source_audit_issue"]
        or data["SOURCE_BODY_SHA256"] != row["source_issue_body_sha256"]):
        raise ValueError("source-locked task or issue identity mismatch")
    matches = []
    for text in existing_comments:
        if not isinstance(text, str) or not text.startswith("RESULT/1\n"):
            continue
        try:
            previous = parse_result(text)
        except ValueError:
            continue
        if previous["ASSIGNMENT_ID"] == task["task_id"]:
            matches.append(previous)
    if matches:
        raise ValueError("duplicate RESULT/1 for exact task: fail closed")
    return data


def can_release_after_readback(row: dict, stage: str, protected_receipt_ref: str) -> bool:
    item = row["stage_work_items"][stage]
    return (item["work_status"] in ("PROTECTED_ADMITTED", "REUSED_SCOPE_VERIFIED",
                                    "VERIFIED_BOUNDED")
            and item["review_status"] not in ("NOT_REVIEWED", "PENDING", "")
            and bool(item["evidence_refs"])
            and bool(item.get("protected_admission_ref"))
            and item["protected_admission_ref"] == protected_receipt_ref
            and protected_receipt_ref.startswith("grandchallenge/MATH-PROGRAMME@"))


if __name__ == "__main__":
    raise SystemExit("Import as a validator; do not use it to dispatch or reserve workers.")
