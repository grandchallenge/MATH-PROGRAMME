from __future__ import annotations

import re
from typing import Any, Mapping

from autonomy_github import AutonomyError

SYNC_EVENT_PREFIX = "LOW_FRICTION_SYNC_EVENT — MP-ADMIN-LOW-FRICTION-001"
_SYNC_PREVIOUS_RE = re.compile(r"^- previous head: `([0-9a-f]{40})`;$", re.MULTILINE)
_SYNC_NEW_RE = re.compile(r"^- synchronized head: `([0-9a-f]{40})`;$", re.MULTILINE)


def _comment_events(low, referee, pr: int) -> list[dict[str, Any]]:
    comments = referee.get(
        f"/repos/{low.EXPECTED_REPOSITORY}/issues/{pr}/comments?per_page=100"
    )
    if not isinstance(comments, list):
        raise AutonomyError("low-friction synchronization comments are malformed")
    if len(comments) >= 100:
        raise AutonomyError(
            "low-friction synchronization evidence exceeds one bounded comment page"
        )
    events: list[dict[str, Any]] = []
    for item in comments:
        body = str(item.get("body") or "")
        if not body.startswith(SYNC_EVENT_PREFIX):
            continue
        if item.get("user", {}).get("login") != low.EXPECTED_REFEREE_LOGIN:
            raise AutonomyError("low-friction synchronization evidence actor drift")
        previous_match = _SYNC_PREVIOUS_RE.search(body)
        new_match = _SYNC_NEW_RE.search(body)
        if (
            previous_match is None
            or new_match is None
            or "- expected-head update: `true`;" not in body
        ):
            raise AutonomyError("low-friction synchronization evidence is malformed")
        previous = previous_match.group(1)
        synchronized = new_match.group(1)
        if previous == synchronized:
            raise AutonomyError("low-friction synchronization evidence has no head change")
        events.append(
            {
                "previous_head": previous,
                "synchronized_head": synchronized,
                "expected_head_used": True,
                "evidence_source": "referee_comment",
                "evidence_comment_id": int(item.get("id") or 0),
            }
        )
    return events


def _history_events(low, referee, pr: int, branch: str) -> list[dict[str, Any]]:
    commits = referee.get(
        f"/repos/{low.EXPECTED_REPOSITORY}/pulls/{pr}/commits?per_page=100"
    )
    if not isinstance(commits, list):
        raise AutonomyError("low-friction synchronization commit history is malformed")
    if len(commits) >= 100:
        raise AutonomyError(
            "low-friction synchronization history exceeds one bounded commit page"
        )
    expected_message = f"Merge branch '{low.EXPECTED_BASE}' into {branch}"
    events: list[dict[str, Any]] = []
    for commit in commits:
        if commit.get("author", {}).get("login") != low.EXPECTED_CANDIDATE_LOGIN:
            continue
        message = str(commit.get("commit", {}).get("message") or "").splitlines()[0]
        if message != expected_message:
            continue
        synchronized = str(commit.get("sha") or "")
        parents = [str(item.get("sha") or "") for item in commit.get("parents", [])]
        if not low.SHA_RE.fullmatch(synchronized) or len(parents) != 2:
            raise AutonomyError("low-friction synchronization commit identity is malformed")
        previous, protected_base = parents
        if not low.SHA_RE.fullmatch(previous) or not low.SHA_RE.fullmatch(protected_base):
            raise AutonomyError("low-friction synchronization commit parents are malformed")
        events.append(
            {
                "previous_head": previous,
                "synchronized_head": synchronized,
                "expected_head_used": True,
                "evidence_source": "candidate_merge_commit",
                "protected_base_parent": protected_base,
            }
        )
    return events


def persistent_sync_events(low, referee, pr: int, branch: str) -> list[dict[str, Any]]:
    combined: dict[tuple[str, str], dict[str, Any]] = {}
    for event in _history_events(low, referee, pr, branch):
        key = (str(event["previous_head"]), str(event["synchronized_head"]))
        combined[key] = event
    for event in _comment_events(low, referee, pr):
        key = (str(event["previous_head"]), str(event["synchronized_head"]))
        existing = combined.get(key, {})
        combined[key] = {**existing, **event}
    return list(combined.values())


def record_sync_event(low, referee, pr: int, branch: str, event: Mapping[str, Any]) -> dict[str, Any]:
    previous = str(event.get("previous_head") or "")
    synchronized = str(event.get("synchronized_head") or "")
    if not low.SHA_RE.fullmatch(previous) or not low.SHA_RE.fullmatch(synchronized):
        raise AutonomyError("low-friction synchronization event has invalid SHA")
    if previous == synchronized:
        raise AutonomyError("low-friction synchronization event did not change the head")

    for existing in persistent_sync_events(low, referee, pr, branch):
        if (
            existing.get("previous_head") == previous
            and existing.get("synchronized_head") == synchronized
            and existing.get("evidence_comment_id")
        ):
            return existing

    body = (
        f"{SYNC_EVENT_PREFIX}\n\n"
        f"- previous head: `{previous}`;\n"
        f"- synchronized head: `{synchronized}`;\n"
        "- expected-head update: `true`;\n"
        "- Candidate/Referee separation: `verified`;\n"
        "- Human Steward checkpoint: `false`.\n\n"
        "Disposition: `LOW_FRICTION_INTERNAL_HEAD_SYNCHRONIZATION_RECORDED`."
    )
    comment = referee.post(
        f"/repos/{low.EXPECTED_REPOSITORY}/issues/{pr}/comments",
        {"body": body},
    )
    if comment.get("user", {}).get("login") != low.EXPECTED_REFEREE_LOGIN:
        raise AutonomyError("low-friction synchronization evidence actor readback failed")
    value = dict(event)
    value["evidence_source"] = "referee_comment"
    value["evidence_comment_id"] = int(comment.get("id") or 0)
    return value


def _merge_events(*groups: list[dict[str, Any]]) -> list[dict[str, Any]]:
    combined: dict[tuple[str, str], dict[str, Any]] = {}
    for group in groups:
        for event in group:
            key = (
                str(event.get("previous_head") or ""),
                str(event.get("synchronized_head") or ""),
            )
            if not all(key):
                continue
            combined[key] = {**combined.get(key, {}), **event}
    return list(combined.values())


def install(low) -> None:
    existing_sync = low.synchronize_behind
    if getattr(existing_sync, "_mp_persistent_sync", False):
        original_sync = getattr(existing_sync, "_mp_original")
    else:
        original_sync = existing_sync

    existing_receipt = low.record_terminal_receipt
    if getattr(existing_receipt, "_mp_persistent_sync", False):
        original_receipt = getattr(existing_receipt, "_mp_original")
    else:
        original_receipt = existing_receipt

    if not getattr(existing_sync, "_mp_persistent_sync", False):
        def durable_synchronize(candidate, observer, pull, control):
            event = original_sync(candidate, observer, pull, control)
            pr = int(pull["number"])
            branch = str(pull.get("head", {}).get("ref") or "")
            return record_sync_event(low, observer, pr, branch, event)

        durable_synchronize._mp_persistent_sync = True
        durable_synchronize._mp_original = original_sync
        low.synchronize_behind = durable_synchronize

    if not getattr(existing_receipt, "_mp_persistent_sync", False):
        def durable_terminal_receipt(
            referee,
            classification,
            disposition_id,
            checks,
            sync_events,
            readback,
            trace,
        ):
            persisted = persistent_sync_events(
                low,
                referee,
                int(classification.pr),
                str(classification.branch),
            )
            merged = _merge_events(list(sync_events), persisted)
            return original_receipt(
                referee,
                classification,
                disposition_id,
                checks,
                merged,
                readback,
                trace,
            )

        durable_terminal_receipt._mp_persistent_sync = True
        durable_terminal_receipt._mp_original = original_receipt
        low.record_terminal_receipt = durable_terminal_receipt
