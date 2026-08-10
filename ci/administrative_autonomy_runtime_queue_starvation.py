from __future__ import annotations

from typing import Any, Callable

from autonomy_github import AutonomyError
from administrative_autonomy_receipt_stage import (
    pending_closures as ordinary_pending_closures,
)

PendingFunction = Callable[[Any, str, dict[str, Any], str], list[dict[str, Any]]]


def filter_receipt_complete_closures(
    closures: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Keep only closures whose protected completion receipt is still absent.

    A receipt-complete item may retain an open navigation issue or unresolved
    mirror-cleanup debt.  That lifecycle debt remains visible in GitHub, but it
    is not missing protected completion and therefore must not monopolize later
    bounded maintenance execution.
    """

    blocking: list[dict[str, Any]] = []
    for item in closures:
        if "receipt_present" not in item:
            raise AutonomyError(
                "pending maintenance closure is missing receipt-presence evidence"
            )
        if item["receipt_present"] is True:
            continue
        if item["receipt_present"] is not False:
            raise AutonomyError(
                "pending maintenance closure receipt-presence evidence is invalid"
            )
        blocking.append(item)
    return blocking


def pending_closures(
    candidate: Any,
    repo: str,
    runtime: dict[str, Any],
    referee_login: str,
    base: PendingFunction = ordinary_pending_closures,
) -> list[dict[str, Any]]:
    return filter_receipt_complete_closures(
        base(candidate, repo, runtime, referee_login)
    )
