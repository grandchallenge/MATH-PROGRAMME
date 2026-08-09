from __future__ import annotations

import time
import urllib.parse
from typing import Any

from autonomy_github import AutonomyError, Client


def _run_order(run: dict[str, Any]) -> tuple[str, int]:
    return (
        str(run.get("created_at") or ""),
        int(run.get("id") or 0),
    )


def authoritative_successful_run_id(runs: list[dict[str, Any]]) -> int:
    """Return the newest settled synchronization attestation, or zero.

    Completed `skipped` workflow-run triggers are non-executions and do not
    displace an earlier successful synchronization.  Every other newer run is
    authoritative for ordering: while it is pending, or if it terminates
    without success, an older success may not be paired with mirror state that
    the newer run could have produced.
    """

    relevant = [
        run
        for run in runs
        if not (
            run.get("status") == "completed"
            and run.get("conclusion") == "skipped"
        )
    ]
    if not relevant:
        return 0
    newest = max(relevant, key=_run_order)
    if (
        newest.get("status") != "completed"
        or newest.get("conclusion") != "success"
    ):
        return 0
    return int(newest.get("id") or 0)


def _workflow_runs(
    observability: Client,
    repo: str,
    workflow: str,
    merge_sha: str,
) -> list[dict[str, Any]]:
    payload = observability.get(
        f"/repos/{repo}/actions/workflows/{workflow}/runs?head_sha={merge_sha}&per_page=20"
    )
    runs = payload.get("workflow_runs", [])
    if not isinstance(runs, list):
        raise AutonomyError("mirror synchronization workflow-run payload drift")
    return [run for run in runs if isinstance(run, dict)]


def _mirrors_current(
    evidence: Client,
    merge_sha: str,
    procedure_id: str,
    due: str,
    runtime: dict[str, Any],
) -> bool:
    marker_head = f"- protected MATH-PROGRAMME head: `{merge_sha}`"
    marker_due = f"- `{procedure_id}` completed through: `{due}`"
    for mirror in runtime["mirrors"]:
        issue = evidence.get(
            f"/repos/{mirror['repository']}/issues/{mirror['issue']}"
        )
        body = str(issue.get("body") or "")
        if marker_head not in body or marker_due not in body:
            return False
    return True


def wait_mirror_sync(
    observability: Client,
    evidence: Client,
    repo: str,
    merge_sha: str,
    procedure_id: str,
    due: str,
    runtime: dict[str, Any],
) -> int:
    """Bind terminal readback to the newest stable synchronization attestation.

    A previous successful no-op may not be combined with mirror state produced
    by a newer synchronization that is still running.  The selected run must be
    the newest non-skipped run for the exact protected head, must itself be
    terminally successful, and must remain that run across two observations of
    current mirrors plus a final workflow-run readback.
    """

    timeout = int(
        runtime["merge_control"]["maximum_protected_readback_wait_seconds"]
    )
    poll = int(runtime["merge_control"]["poll_interval_seconds"])
    deadline = time.monotonic() + timeout
    workflow = urllib.parse.quote(
        "administrative-maintenance-synchronization.yml",
        safe="",
    )
    stable_run_id = 0

    while time.monotonic() < deadline:
        runs = _workflow_runs(observability, repo, workflow, merge_sha)
        run_id = authoritative_successful_run_id(runs)
        if not run_id or not _mirrors_current(
            evidence,
            merge_sha,
            procedure_id,
            due,
            runtime,
        ):
            stable_run_id = 0
            time.sleep(poll)
            continue

        if stable_run_id != run_id:
            stable_run_id = run_id
            time.sleep(poll)
            continue

        confirm_runs = _workflow_runs(
            observability,
            repo,
            workflow,
            merge_sha,
        )
        if authoritative_successful_run_id(confirm_runs) != run_id:
            stable_run_id = 0
            time.sleep(poll)
            continue
        if not _mirrors_current(
            evidence,
            merge_sha,
            procedure_id,
            due,
            runtime,
        ):
            stable_run_id = 0
            time.sleep(poll)
            continue

        final_runs = _workflow_runs(
            observability,
            repo,
            workflow,
            merge_sha,
        )
        if authoritative_successful_run_id(final_runs) == run_id:
            return run_id

        stable_run_id = 0
        time.sleep(poll)

    raise AutonomyError(
        "protected mirror synchronization producer readback timed out"
    )
