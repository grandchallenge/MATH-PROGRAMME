from __future__ import annotations

import json
import time
import urllib.parse
from pathlib import Path
from typing import Any, Callable

from autonomy_github import AutonomyError, json_content
from administrative_autonomy_receipt_stage import (
    STATE_PATH,
    completion_has_receipt,
    pending_closures as ordinary_pending_closures,
    receipt_for,
)
from administrative_autonomy_runtime_mirror_sync import authoritative_successful_run_id
from administrative_autonomy_runtime_queue_starvation import (
    pending_closures as nonblocking_pending_closures,
)
from administrative_autonomy_runtime_receipt_behind_resume import (
    stage_completion_receipt as resumable_stage_completion_receipt,
)
from administrative_autonomy_runtime_structural_0121_recovery import (
    wait_mirror_sync as structural_0121_hole_wait_mirror_sync,
)

ROOT = Path(__file__).resolve().parents[1]
CONTROL_PATH = (
    ROOT
    / "governance"
    / "administrative_post_receipt_closure_resume_control.json"
)

PendingFunction = Callable[
    [Any, str, dict[str, Any], str],
    list[dict[str, Any]],
]


def load_control() -> dict[str, Any]:
    return json.loads(CONTROL_PATH.read_text(encoding="utf-8"))


def _require_control(control: dict[str, Any]) -> None:
    if control.get("control_id") != "MP-ADMIN-POST-RECEIPT-CLOSURE-RESUME-001":
        raise AutonomyError("post-receipt closure-resume control identity drift")
    if control.get("status") != "ACTIVE_ON_PROTECTED_MERGE":
        raise AutonomyError("post-receipt closure-resume control is not active")
    correction = control.get("correction", {})
    required = {
        "receipt_complete_open_closure_only": True,
        "ordinary_receipt_missing_precedence_preserved": True,
        "descendant_synchronization_allowed_for_target_only": True,
        "receipt_introduction_ancestry_required": True,
        "all_configured_mirrors_required": True,
        "mirror_head_must_equal_successful_synchronization_head": True,
        "mirror_frontier_must_equal_protected_completion_frontier": True,
        "duplicate_receipt_allowed": False,
        "completion_frontier_change_allowed": False,
        "cadence_anchor_reset": False,
        "deadline_reset": False,
    }
    for key, expected in required.items():
        if correction.get(key) != expected:
            raise AutonomyError(f"post-receipt closure-resume control drift: {key}")


def _target_manifest(manifest: dict[str, Any], control: dict[str, Any]) -> bool:
    target = control["target"]
    return (
        str(manifest.get("occurrence_key") or "") == str(target["occurrence_key"])
        and str(manifest.get("procedure_id") or "") == str(target["procedure_id"])
        and str(manifest.get("scheduled_due_at") or "") == str(target["scheduled_due_at"])
        and int(manifest.get("issue_number") or 0) == int(target["candidate_issue"])
        and int(manifest.get("pull_request_number") or 0)
        == int(target["candidate_pull_request"])
        and str(manifest.get("branch") or "") == str(target["candidate_branch"])
    )


def _target_receipt_matches(
    receipt: dict[str, Any], control: dict[str, Any]
) -> bool:
    target = control["target"]
    return (
        str(receipt.get("procedure_id") or "") == str(target["procedure_id"])
        and str(receipt.get("scheduled_due_at") or "")
        == str(target["scheduled_due_at"])
        and str(receipt.get("record_path") or "") == str(target["record_path"])
        and str(receipt.get("merge_commit") or "")
        == str(target["record_merge_commit"])
        and str(receipt.get("reviewed_head") or "") == str(target["reviewed_head"])
        and int(receipt.get("pull_request") or 0)
        == int(target["candidate_pull_request"])
        and str(receipt.get("disposition") or "")
        == "REFEREE_AGENT_AUTHORIZED_EXACT_HEAD_PROTECTED_MERGE"
        and str(receipt.get("receipt_state") or "") == "PROTECTED_COMPLETE"
    )


def _target_closure(item: dict[str, Any], control: dict[str, Any]) -> bool:
    target = control["target"]
    manifest = item.get("manifest", {})
    return (
        _target_manifest(manifest, control)
        and int(item.get("issue_number") or 0) == int(target["candidate_issue"])
        and int(item.get("pull_request") or 0)
        == int(target["candidate_pull_request"])
        and str(item.get("record_id") or "") == str(target["record_id"])
        and str(item.get("record_path") or "") == str(target["record_path"])
        and str(item.get("exact_head") or "") == str(target["reviewed_head"])
        and str(item.get("record_merge_commit") or "")
        == str(target["record_merge_commit"])
        and item.get("receipt_present") is True
        and _target_receipt_matches(item.get("receipt", {}), control)
    )


def _is_ancestor(client: Any, repo: str, ancestor: str, descendant: str) -> bool:
    if ancestor == descendant:
        return True
    compare = client.get(
        f"/repos/{repo}/compare/{urllib.parse.quote(ancestor, safe='')}..."
        f"{urllib.parse.quote(descendant, safe='')}"
    )
    return str(compare.get("status") or "") == "ahead"


def _current_main(client: Any, repo: str) -> str:
    branch = client.get(f"/repos/{repo}/branches/main")
    return str(branch.get("commit", {}).get("sha") or "")


def _require_target_receipt_in_completion(
    completion: dict[str, Any], control: dict[str, Any]
) -> dict[str, Any]:
    target = control["target"]
    procedure = completion.get("procedures", {}).get(str(target["procedure_id"]))
    if not isinstance(procedure, dict):
        raise AutonomyError("post-receipt target procedure is absent")
    if (
        str(procedure.get("completed_through_utc") or "")
        != str(target["preserved_completed_through_utc"])
    ):
        raise AutonomyError("post-receipt protected completion frontier drift")
    if (
        str(completion.get("derived_from_protected_head") or "")
        != str(target["record_merge_commit"])
    ):
        raise AutonomyError("post-receipt completion derivation head drift")
    due = str(target["scheduled_due_at"])
    same_due = [
        item
        for item in procedure.get("receipts", [])
        if str(item.get("scheduled_due_at") or "") == due
    ]
    if len(same_due) != 1 or not _target_receipt_matches(same_due[0], control):
        raise AutonomyError(
            "post-receipt exact protected receipt is absent, conflicting, or ambiguous"
        )
    return same_due[0]


def _require_receipt_introduction(
    candidate: Any,
    repo: str,
    receipt: dict[str, Any],
    control: dict[str, Any],
) -> None:
    target = control["target"]
    introduction = str(target["receipt_introduction_commit"])
    at_commit = json_content(candidate, repo, STATE_PATH, introduction)
    if at_commit is None or not completion_has_receipt(at_commit, receipt):
        raise AutonomyError("post-receipt introduction commit does not contain receipt")
    commit = candidate.get(f"/repos/{repo}/commits/{introduction}")
    parents = commit.get("parents", [])
    if not parents:
        raise AutonomyError("post-receipt introduction commit has no protected parent")
    protected_parent = str(parents[0].get("sha") or "")
    before = json_content(candidate, repo, STATE_PATH, protected_parent)
    if before is not None and completion_has_receipt(before, receipt):
        raise AutonomyError(
            "post-receipt declared introduction commit is not the protected introduction"
        )
    main = _current_main(candidate, repo)
    if not main or not _is_ancestor(candidate, repo, introduction, main):
        raise AutonomyError(
            "post-receipt introduction commit is not ancestral to protected main"
        )


def pending_closures(
    candidate: Any,
    repo: str,
    runtime: dict[str, Any],
    referee_login: str,
    base: PendingFunction = nonblocking_pending_closures,
    all_base: PendingFunction = ordinary_pending_closures,
) -> list[dict[str, Any]]:
    """Restore exactly #515 terminal debt without re-blocking receipt-complete debt generally."""

    ordinary = base(candidate, repo, runtime, referee_login)
    if ordinary:
        return ordinary

    control = load_control()
    _require_control(control)
    candidates = [
        item
        for item in all_base(candidate, repo, runtime, referee_login)
        if _target_closure(item, control)
    ]
    if len(candidates) > 1:
        raise AutonomyError("duplicate exact post-receipt target closure")
    if not candidates:
        return []

    item = candidates[0]
    completion = json_content(candidate, repo, STATE_PATH, "main")
    if completion is None:
        raise AutonomyError("post-receipt protected completion ledger is absent")
    receipt = _require_target_receipt_in_completion(completion, control)
    _require_receipt_introduction(candidate, repo, receipt, control)
    return [item]


def stage_completion_receipt(
    candidate: Any,
    referee: Any,
    administrator: Any,
    repo: str,
    runtime: dict[str, Any],
    record_id: str,
    procedure_id: str,
    due: str,
    record_path: str,
    record: dict[str, Any],
    source_pull_request: int,
    source_head: str,
    source_merge_sha: str,
    referee_login: str,
    candidate_login: str,
    base: Callable[..., dict[str, Any]] = resumable_stage_completion_receipt,
) -> dict[str, Any]:
    """For the exact target, bind the already-protected receipt to its true introduction."""

    control = load_control()
    _require_control(control)
    target = control["target"]
    is_target = (
        record_id == str(target["record_id"])
        and procedure_id == str(target["procedure_id"])
        and due == str(target["scheduled_due_at"])
        and record_path == str(target["record_path"])
        and int(source_pull_request) == int(target["candidate_pull_request"])
        and source_head == str(target["reviewed_head"])
        and source_merge_sha == str(target["record_merge_commit"])
    )
    if not is_target:
        return base(
            candidate,
            referee,
            administrator,
            repo,
            runtime,
            record_id,
            procedure_id,
            due,
            record_path,
            record,
            source_pull_request,
            source_head,
            source_merge_sha,
            referee_login,
            candidate_login,
        )

    current = json_content(candidate, repo, STATE_PATH, "main")
    if current is None:
        raise AutonomyError("post-receipt protected completion ledger is absent")
    receipt = receipt_for(
        procedure_id,
        due,
        record_path,
        record,
        source_merge_sha,
        source_head,
        source_pull_request,
    )
    protected = _require_target_receipt_in_completion(current, control)
    if not completion_has_receipt(current, receipt) or not _target_receipt_matches(
        protected, control
    ):
        raise AutonomyError("post-receipt target receipt content drift")
    _require_receipt_introduction(candidate, repo, receipt, control)

    return {
        "receipt": receipt,
        "completion": current,
        "receipt_pull_request": int(target["receipt_pull_request"]),
        "receipt_head": str(target["receipt_head"]),
        "receipt_disposition_comment_id": int(
            target["receipt_disposition_comment_id"]
        ),
        "receipt_merge_commit": str(target["receipt_introduction_commit"]),
        "receipt_recovered": True,
    }


def _successful_sync_run(observability: Any, repo: str, head: str) -> int:
    payload = observability.get(
        f"/repos/{repo}/actions/workflows/"
        "administrative-maintenance-synchronization.yml/runs?"
        f"head_sha={urllib.parse.quote(head, safe='')}&per_page=20"
    )
    runs = payload.get("workflow_runs", [])
    if not isinstance(runs, list):
        raise AutonomyError("post-receipt synchronization workflow-run payload drift")
    normalized = [run for run in runs if isinstance(run, dict)]
    return authoritative_successful_run_id(normalized)


def _mirrors_current(
    evidence: Any,
    runtime: dict[str, Any],
    head: str,
    frontier: str,
) -> bool:
    head_marker = f"- protected MATH-PROGRAMME head: `{head}`"
    frontier_marker = f"- `structural_sweep` completed through: `{frontier}`"
    for mirror in runtime["mirrors"]:
        issue = evidence.get(
            f"/repos/{mirror['repository']}/issues/{int(mirror['issue'])}"
        )
        body = str(issue.get("body") or "")
        if head_marker not in body or frontier_marker not in body:
            return False
    return True


def wait_mirror_sync(
    observability: Any,
    evidence: Any,
    repo: str,
    merge_sha: str,
    procedure: str,
    due: str,
    runtime: dict[str, Any],
    base: Callable[..., int] = structural_0121_hole_wait_mirror_sync,
) -> int:
    """For #515, accept only a synchronized protected descendant of the receipt merge."""

    control = load_control()
    _require_control(control)
    target = control["target"]
    is_target = (
        merge_sha == str(target["receipt_introduction_commit"])
        and procedure == str(target["procedure_id"])
        and due == str(target["scheduled_due_at"])
    )
    if not is_target:
        return base(
            observability,
            evidence,
            repo,
            merge_sha,
            procedure,
            due,
            runtime,
        )

    completion = json_content(evidence, repo, STATE_PATH, "main")
    if completion is None:
        raise AutonomyError("post-receipt protected completion ledger is absent")
    _require_target_receipt_in_completion(completion, control)
    frontier = str(target["preserved_completed_through_utc"])
    timeout = int(runtime["merge_control"]["maximum_protected_readback_wait_seconds"])
    poll = int(runtime["merge_control"]["poll_interval_seconds"])
    deadline = time.monotonic() + timeout
    stable_run = 0
    stable_reads = 0

    while time.monotonic() < deadline:
        head = _current_main(observability, repo)
        if not head or not _is_ancestor(
            observability,
            repo,
            str(target["receipt_introduction_commit"]),
            head,
        ):
            raise AutonomyError(
                "post-receipt protected main is not descended from receipt introduction"
            )
        run_id = _successful_sync_run(observability, repo, head)
        current = run_id > 0 and _mirrors_current(evidence, runtime, head, frontier)
        if current:
            if run_id == stable_run:
                stable_reads += 1
            else:
                stable_run = run_id
                stable_reads = 1
            if stable_reads >= 2:
                return run_id
        else:
            stable_run = 0
            stable_reads = 0
        time.sleep(poll)

    raise AutonomyError(
        "post-receipt descendant protected mirror synchronization timed out"
    )
