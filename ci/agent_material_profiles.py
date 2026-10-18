#!/usr/bin/env python3
"""Fail-closed, content-addressed classification of routine material closures.

No candidate-supplied label, reviewer text, workflow or profile is executable
authority. This module must be loaded only from protected main.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parents[1]
REGISTRY = HERE / "governance/agent_delegated_admission_profiles.json"
PATH_RE = re.compile(r"^docs/[A-Za-z0-9][A-Za-z0-9_-]*\.md$")
PROFILE_OPERATIONS = {
    "DOC-FINAL-NEWLINE-001": "append_one_missing_final_newline",
    "DOC-TRAILING-SPACE-001": "remove_single_nonsemantic_trailing_space",
    "DOC-REDUNDANT-BLANKS-001": "collapse_runs_of_three_or_more_empty_lines",
}
MAX_BYTES = 250000


class MaterialAdmissionError(ValueError):
    pass


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def validate_registry(record: dict[str, Any]) -> None:
    if (record.get("schema_version"), record.get("control_id"),
        record.get("repository"), record.get("base_branch"),
        record.get("status")) != (
        "1.0.0", "GCL-DELEGATED-MATERIAL-ADMISSION-001",
        "grandchallenge/MATH-PROGRAMME", "main",
        "BOUNDED_ROUTINE_PROFILES_ONLY",
    ):
        raise MaterialAdmissionError("delegated profile registry identity drift")
    paths = record.get("paths") or {}
    if paths != {
        "kind": "TOP_LEVEL_DOCS_MARKDOWN",
        "regex": r"^docs/[A-Za-z0-9][A-Za-z0-9_-]*\.md$",
        "max_files": 1,
        "max_file_bytes": 250000,
    }:
        raise MaterialAdmissionError("scope, size or path contract drift")
    profiles = record.get("profiles")
    if not isinstance(profiles, list) or len(profiles) != len(PROFILE_OPERATIONS):
        raise MaterialAdmissionError("unexpected number of delegated profiles")
    found = set()
    for item in profiles:
        if not isinstance(item, dict):
            raise MaterialAdmissionError("invalid profile")
        ident = item.get("id")
        if ident in found or item.get("operation") != PROFILE_OPERATIONS.get(ident):
            raise MaterialAdmissionError("unknown or duplicate operation")
        if item.get("max_changed_lines") != (1 if ident == "DOC-FINAL-NEWLINE-001" else 12):
            raise MaterialAdmissionError("unreviewed maximum change scope")
        if item.get("review_roles") != ["Verifier", "Adversary"] or item.get("review_mode") != "non_authoring_read_only":
            raise MaterialAdmissionError("delegated functional audit was weakened")
        found.add(ident)
    if found != set(PROFILE_OPERATIONS):
        raise MaterialAdmissionError("profile omissions")
    if record.get("issue") != 1247 or record.get("successor") != "GCL-AGENT-ADMISSION-SPECIALIST-001":
        raise MaterialAdmissionError("successor control identity drift")
    bounds = record.get("boundaries") or {}
    for key in ("claims_promoted", "mathematical_certification",
                "substantive_specialist_review_substituted", "protected_bypass",
                "merge_queue_bypass", "security_policy_change"):
        if bounds.get(key) is not False:
            raise MaterialAdmissionError("authority-boundary expansion")
    if bounds.get("unknown_or_mixed_effect") != "REJECT" or bounds.get("unmodelled_operation") != "REJECT":
        raise MaterialAdmissionError("ambiguous effect not fail-closed")


def load_registry(path: Path = REGISTRY) -> dict[str, Any]:
    record = json.loads(path.read_text(encoding="utf-8"))
    validate_registry(record)
    return record


def plain_markdown(data: bytes) -> str:
    if len(data) > MAX_BYTES or not data or b"\x00" in data:
        raise MaterialAdmissionError("invalid or oversized file")
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise MaterialAdmissionError("not UTF-8") from exc
    if "\r" in text or "\t" in text or not text.strip():
        raise MaterialAdmissionError("noncanonical line endings or empty document")
    # Conservative safeguard: do not normalize within code, math display,
    # embedded HTML or YAML front matter without a specialist parser.
    forbidden = ("\x60\x60\x60", "~~~", "$$", "\\[", "\\begin{", "<!--",
                 "<script", "<style")
    if any(token in text for token in forbidden) or text.startswith("---\n"):
        raise MaterialAdmissionError("document contains semantic syntax")
    return text


def classify_text(path: str, before: bytes, after: bytes,
                  registry: dict[str, Any]) -> dict[str, Any]:
    validate_registry(registry)
    if not PATH_RE.fullmatch(path):
        raise MaterialAdmissionError("unadmitted file or path class")
    old, new = plain_markdown(before), plain_markdown(after)
    if old == new:
        raise MaterialAdmissionError("no material change")
    candidates: list[tuple[str, int]] = []
    if not old.endswith("\n") and new == old + "\n":
        candidates.append(("DOC-FINAL-NEWLINE-001", 1))
    old_lines = old.splitlines(keepends=True)
    new_lines = new.splitlines(keepends=True)
    if len(old_lines) == len(new_lines):
        changed = [(o, n) for o, n in zip(old_lines, new_lines) if o != n]
        if 0 < len(changed) <= 12 and all(
            o.endswith(" \n") and not o.endswith("  \n") and
            n == o[:-2] + "\n" and
            not o.lstrip().startswith((">", "#", "-", "*", "+", "|", "<")) and
            "$" not in o and "\x60" not in o and "\\" not in o
            for o, n in changed
        ):
            candidates.append(("DOC-TRAILING-SPACE-001", len(changed)))
    # Collapse surplus vertical whitespace only. Four newlines correspond
    # to three empty lines; keeping three newlines preserves two empty lines.
    collapsed = re.sub(r"\n{4,}", "\n\n\n", old)
    if collapsed != old and collapsed == new:
        removed = old.count("\n") - new.count("\n")
        if 0 < removed <= 12:
            candidates.append(("DOC-REDUNDANT-BLANKS-001", removed))
    if len(candidates) != 1:
        raise MaterialAdmissionError("unproved or mixed content transformation")
    profile, changed_lines = candidates[0]
    return {
        "control_id": registry["control_id"],
        "disposition": "ROUTINE_BOUNDED",
        "profile_id": profile,
        "changed_lines": changed_lines,
        "path": path,
        "before_sha256": sha256(before),
        "after_sha256": sha256(after),
        "reviewer_system_id": "gcl-release-trust-protected-controller",
        "logical_passes": [
            {"role": "Verifier", "logical_pass_id": profile + "-VERIFY",
             "mode": "non_authoring_read_only", "finding": "PASS"},
            {"role": "Adversary", "logical_pass_id": profile + "-ADVERSARY",
             "mode": "non_authoring_read_only", "finding": "PASS"},
        ],
        "authority": {
            "github_mechanical_approval": True,
            "scientific_certification": False,
            "substantive_review_satisfied": False,
            "protected_bypass": False,
        },
    }


if __name__ == "__main__":
    load_registry()
    print("delegated routine material profile registry valid")
