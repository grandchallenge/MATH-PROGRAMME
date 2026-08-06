from __future__ import annotations

from datetime import datetime
from typing import Any

import synchronize_administrative_completion_v3 as v3

implementation = v3.implementation


def active_runtime() -> bool:
    try:
        runtime = implementation.load_json(
            implementation.ROOT
            / "governance"
            / "administrative_autonomy_runtime_integration.json"
        )
        activation = implementation.load_json(
            implementation.ROOT
            / str(runtime["activation_record"])
        )
    except (FileNotFoundError, KeyError, ValueError):
        return False
    return (
        runtime.get("status") == "ACTIVE_WHEN_PROTECTED"
        and activation.get("state") == "ACTIVE"
        and activation.get("activation_id") == runtime.get("activation_id")
    )


def managed_section(
    completion: dict[str, Any],
    registry: dict[str, Any],
    head: str,
) -> str:
    completed = implementation.completion_by_procedure(completion)
    next_items: list[tuple[datetime, str]] = []
    for procedure in registry["procedures"]:
        pending = list(
            implementation.iter_due_occurrences(
                procedure,
                completed.get(procedure["id"]),
            )
        )
        if pending:
            next_items.append((pending[0], procedure["id"]))
    next_items.sort()
    lines = [
        implementation.START,
        "## Automated maintenance state mirror",
        "",
        "This section is navigation only. Protected repository records and merge receipts remain authoritative.",
        "",
        f"- protected MATH-PROGRAMME head: `{head}`",
        f"- completion-state mode: `{completion['state']}`",
    ]
    for procedure_id, state in completion["procedures"].items():
        lines.append(
            f"- `{procedure_id}` completed through: "
            f"`{state['completed_through_utc'] or 'none'}`"
        )
    lines.extend(["", "### Next controlled obligations", ""])
    for due, procedure_id in next_items:
        lines.append(f"- `{procedure_id}`: `{implementation.iso_z(due)}`")
    if active_runtime():
        lines.extend(
            [
                "",
                "Routine bounded structural-sweep, administrative-review, and deep-conformance completion is delegated under protected `ACTIVE` authority. Candidate, Referee, and merge-executor identities remain separated; exact-head checks and protected readback remain mandatory.",
                "",
                "Human Steward disposition remains required for control-plane changes, delegated-scope expansion, pilot or constitutional review, and mathematical, source, certification, external-claim, waiver, or emergency authority.",
            ]
        )
    else:
        lines.extend(
            [
                "",
                "Independent approval, Human Steward exact-head disposition, and protected merge remain manual.",
            ]
        )
    lines.append(implementation.END)
    return "\n".join(lines)


def create_completion_sync_pr(
    client: Any,
    repository: str,
    completion: dict[str, Any],
    head: str,
) -> dict[str, Any] | None:
    if active_runtime():
        return None
    return _original_create_completion_sync_pr(
        client,
        repository,
        completion,
        head,
    )


_original_create_completion_sync_pr = implementation.create_completion_sync_pr
implementation.managed_section = managed_section
implementation.create_completion_sync_pr = create_completion_sync_pr


if __name__ == "__main__":
    raise SystemExit(v3.main())
