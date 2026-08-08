from __future__ import annotations

import copy
from datetime import datetime, timezone
from typing import Any, Callable

from administrative_automation import parse_datetime
from autonomy_github import AutonomyError
from administrative_autonomy_runtime_github import (
    eligible_candidates as ordinary_eligible_candidates,
)

UTC = timezone.utc

LATE_RECOVERY_OCCURRENCE_KEY = "structural_sweep:2026-08-08T18:09:00Z"
LATE_RECOVERY_DUE_AT = parse_datetime("2026-08-08T18:09:00Z")
LATE_RECOVERY_ISSUE_NUMBER = 312
LATE_RECOVERY_PULL_REQUEST_NUMBER = 313
LATE_RECOVERY_EXPIRES_AT = parse_datetime("2026-08-10T01:21:00Z")

EligibleFunction = Callable[
    [Any, str, dict[str, Any], datetime],
    list[tuple[dict[str, Any], dict[str, Any]]],
]


def _widened_recovery_minutes(runtime: dict[str, Any]) -> int:
    ordinary = int(runtime["scope"]["recovery_window_minutes_after_due"])
    bounded = int(
        (LATE_RECOVERY_EXPIRES_AT - LATE_RECOVERY_DUE_AT).total_seconds()
        // 60
    )
    return max(ordinary, bounded)


def eligible_candidates(
    candidate: Any,
    repo: str,
    runtime: dict[str, Any],
    now: datetime,
    base: EligibleFunction = ordinary_eligible_candidates,
) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    """Admit exactly one expired candidate without relaxing the global window.

    The ordinary runtime remains authoritative.  This wrapper only replays the
    existing eligibility checks with a temporary in-memory recovery horizon for
    the exact August 8 occurrence after its ordinary window has expired.  The
    protected runtime configuration is never mutated, and the exception expires
    at the accelerated pilot/deep-conformance boundary.
    """

    ordinary = base(candidate, repo, runtime, now)
    if ordinary:
        return ordinary

    if now.tzinfo is None:
        raise AutonomyError("late-recovery evaluation time must include an offset")
    observed = now.astimezone(UTC)
    if observed > LATE_RECOVERY_EXPIRES_AT:
        return []

    widened = copy.deepcopy(runtime)
    widened["scope"]["recovery_window_minutes_after_due"] = (
        _widened_recovery_minutes(runtime)
    )
    replayed = base(candidate, repo, widened, observed)

    matches: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for pull, manifest in replayed:
        if manifest.get("occurrence_key") != LATE_RECOVERY_OCCURRENCE_KEY:
            continue
        if int(manifest.get("issue_number") or 0) != LATE_RECOVERY_ISSUE_NUMBER:
            raise AutonomyError("late-recovery issue identity drift")
        if int(manifest.get("pull_request_number") or 0) != LATE_RECOVERY_PULL_REQUEST_NUMBER:
            raise AutonomyError("late-recovery manifest pull-request identity drift")
        if int(pull.get("number") or 0) != LATE_RECOVERY_PULL_REQUEST_NUMBER:
            raise AutonomyError("late-recovery pull-request identity drift")
        matches.append((pull, manifest))

    if len(matches) > 1:
        raise AutonomyError("duplicate exact-occurrence late-recovery candidate")
    return matches
