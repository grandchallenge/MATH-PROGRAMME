from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any, Callable

import administrative_autonomy_runtime_post_receipt_closure_resume as predecessor
from administrative_automation import parse_datetime, validate_completion_state
from administrative_autonomy_receipt_stage import (
    STATE_PATH,
    completion_has_receipt,
    receipt_for,
)
from autonomy_github import AutonomyError, json_content

ROOT = Path(__file__).resolve().parents[1]
CONTROL_PATH = (
    ROOT
    / "governance"
    / "administrative_post_receipt_current_frontier_control.json"
)

PendingFunction = Callable[
    [Any, str, dict[str, Any], str],
    list[dict[str, Any]],
]


def load_control() -> dict[str, Any]:
    return json.loads(CONTROL_PATH.read_text(encoding="utf-8"))


def _require_control(control: dict[str, Any]) -> None:
    if control.get("control_id") != "MP-ADMIN-POST-RECEIPT-CURRENT-FRONTIER-001":
        raise AutonomyError("post-receipt current-frontier control identity drift")
    if control.get("issue") != 544:
        raise AutonomyError("post-receipt current-frontier issue identity drift")
    if control.get("status") != "ACTIVE_ON_PROTECTED_MERGE":
        raise AutonomyError("post-receipt current-frontier control is not active")
    predecessor_control = control.get("predecessor_control", {})
    if predecessor_control != {
        "control_id": "MP-ADMIN-POST-RECEIPT-CLOSURE-RESUME-001",
        "issue": 541,
        "protected_merge": "a7f7499aca55b184311d16f7d6fcc6e892bb9adc",
        "mutation_prohibited": True,
    }:
        raise AutonomyError("post-receipt predecessor-control binding drift")
    required = {
        "exact_target_only": True,
        "current_frontier_read_from_protected_ledger": True,
        "ordinary_completion_validator_required": True,
        "exact_historical_receipt_must_remain_unique": True,
        "current_frontier_must_equal_latest_structural_receipt_due": True,
        "derived_head_must_equal_latest_structural_receipt_record_merge": True,
        "current_frontier_must_not_precede_target_due": True,
        "receipt_introduction_ancestry_required": True,
        "descendant_synchronization_required": True,
        "all_configured_mirrors_required": True,
        "stable_mirror_observations_required": 2,
        "duplicate_receipt_allowed": False,
        "completion_ledger_mutation_allowed": False,
        "completion_frontier_change_allowed": False,
        "record_mutation_allowed": False,
        "cadence_anchor_reset": False,
        "deadline_reset": False,
    }
    correction = control.get("correction", {})
    for key, expected in required.items():
        if correction.get(key) != expected:
            raise AutonomyError(f"post-receipt current-frontier control drift: {key}")


def _predecessor_control(control: dict[str, Any]) -> dict[str, Any]:
    base = predecessor.load_control()
    predecessor._require_control(base)
    target = control["target"]
    predecessor_target = base["target"]
    identity_fields = (
        "candidate_issue",
        "candidate_pull_request",
        "occurrence_key",
        "procedure_id",
        "scheduled_due_at",
        "candidate_branch",
        "record_id",
        "record_path",
        "reviewed_head",
        "record_merge_commit",
        "receipt_pull_request",
        "receipt_head",
        "receipt_disposition_comment_id",
        "receipt_introduction_commit",
    )
    if any(target.get(field) != predecessor_target.get(field) for field in identity_fields):
        raise AutonomyError("post-receipt current-frontier target drift from predecessor")
    return base


def _require_predecessor_merge_ancestry(
    client: Any, repo: str, control: dict[str, Any]
) -> str:
    main = predecessor._current_main(client, repo)
    protected_merge = str(control["predecessor_control"]["protected_merge"])
    if not main or not predecessor._is_ancestor(client, repo, protected_merge, main):
        raise AutonomyError(
            "post-receipt current-frontier predecessor merge is not ancestral to protected main"
        )
    return main


def _validated_current_frontier(
    completion: dict[str, Any],
    control: dict[str, Any],
    predecessor_control: dict[str, Any] | None = None,
) -> tuple[str, dict[str, Any]]:
    _require_control(control)
    predecessor_control = predecessor_control or _predecessor_control(control)
    errors = validate_completion_state(completion)
    if errors:
        raise AutonomyError(
            "post-receipt protected completion ledger invalid: " + "; ".join(errors)
        )

    target = control["target"]
    procedure = completion.get("procedures", {}).get(str(target["procedure_id"]))
    if not isinstance(procedure, dict):
        raise AutonomyError("post-receipt target procedure is absent")
    receipts = procedure.get("receipts", [])
    if not isinstance(receipts, list) or not receipts:
        raise AutonomyError("post-receipt protected structural receipt set is empty")

    target_due = str(target["scheduled_due_at"])
    exact = [
        item
        for item in receipts
        if str(item.get("scheduled_due_at") or "") == target_due
    ]
    if (
        len(exact) != 1
        or not predecessor._target_receipt_matches(exact[0], predecessor_control)
    ):
        raise AutonomyError(
            "post-receipt exact protected receipt is absent, conflicting, or ambiguous"
        )

    latest = receipts[-1]
    frontier = str(procedure.get("completed_through_utc") or "")
    latest_due = str(latest.get("scheduled_due_at") or "")
    if frontier != latest_due:
        raise AutonomyError(
            "post-receipt current frontier is not the latest protected structural receipt"
        )
    if parse_datetime(frontier) < parse_datetime(target_due):
        raise AutonomyError("post-receipt current frontier precedes exact target due")
    discovery_frontier = str(target["discovery_frontier"])
    if parse_datetime(frontier) < parse_datetime(discovery_frontier):
        raise AutonomyError("post-receipt current frontier regressed below protected discovery")

    derived = str(completion.get("derived_from_protected_head") or "")
    latest_merge = str(latest.get("merge_commit") or "")
    if not latest_merge or derived != latest_merge:
        raise AutonomyError(
            "post-receipt current frontier derivation head does not match latest protected receipt"
        )
    return frontier, exact[0]


def pending_closures(
    candidate: Any,
    repo: str,
    runtime: dict[str, Any],
    referee_login: str,
    base: PendingFunction = predecessor.nonblocking_pending_closures,
    all_base: PendingFunction = predecessor.ordinary_pending_closures,
) -> list[dict[str, Any]]:
    ordinary = base(candidate, repo, runtime, referee_login)
    if ordinary:
        return ordinary

    control = load_control()
    _require_control(control)
    predecessor_control = _predecessor_control(control)
    _require_predecessor_merge_ancestry(candidate, repo, control)
    candidates = [
        item
        for item in all_base(candidate, repo, runtime, referee_login)
        if predecessor._target_closure(item, predecessor_control)
    ]
    if len(candidates) > 1:
        raise AutonomyError("duplicate exact post-receipt current-frontier target closure")
    if not candidates:
        return []

    completion = json_content(candidate, repo, STATE_PATH, "main")
    if completion is None:
        raise AutonomyError("post-receipt protected completion ledger is absent")
    _, receipt = _validated_current_frontier(
        completion, control, predecessor_control
    )
    predecessor._require_receipt_introduction(
        candidate, repo, receipt, predecessor_control
    )
    return [candidates[0]]


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
    base: Callable[..., dict[str, Any]] = predecessor.stage_completion_receipt,
) -> dict[str, Any]:
    control = load_control()
    _require_control(control)
    predecessor_control = _predecessor_control(control)
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

    _require_predecessor_merge_ancestry(candidate, repo, control)
    current = json_content(candidate, repo, STATE_PATH, "main")
    if current is None:
        raise AutonomyError("post-receipt protected completion ledger is absent")
    frontier, protected_receipt = _validated_current_frontier(
        current, control, predecessor_control
    )
    receipt = receipt_for(
        procedure_id,
        due,
        record_path,
        record,
        source_merge_sha,
        source_head,
        source_pull_request,
    )
    if (
        not completion_has_receipt(current, receipt)
        or not predecessor._target_receipt_matches(
            protected_receipt, predecessor_control
        )
    ):
        raise AutonomyError("post-receipt target receipt content drift")
    predecessor._require_receipt_introduction(
        candidate, repo, receipt, predecessor_control
    )
    return {
        "receipt": receipt,
        "completion": current,
        "receipt_pull_request": int(target["receipt_pull_request"]),
        "receipt_head": str(target["receipt_head"]),
        "receipt_disposition_comment_id": int(target["receipt_disposition_comment_id"]),
        "receipt_merge_commit": str(target["receipt_introduction_commit"]),
        "receipt_recovered": True,
        "protected_current_frontier": frontier,
    }


def wait_mirror_sync(
    observability: Any,
    evidence: Any,
    repo: str,
    merge_sha: str,
    procedure: str,
    due: str,
    runtime: dict[str, Any],
    base: Callable[..., int] = predecessor.wait_mirror_sync,
) -> int:
    control = load_control()
    _require_control(control)
    predecessor_control = _predecessor_control(control)
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

    _require_predecessor_merge_ancestry(observability, repo, control)
    completion = json_content(evidence, repo, STATE_PATH, "main")
    if completion is None:
        raise AutonomyError("post-receipt protected completion ledger is absent")
    frontier, _ = _validated_current_frontier(
        completion, control, predecessor_control
    )
    timeout = int(runtime["merge_control"]["maximum_protected_readback_wait_seconds"])
    poll = int(runtime["merge_control"]["poll_interval_seconds"])
    deadline = time.monotonic() + timeout
    stable_run = 0
    stable_reads = 0

    while time.monotonic() < deadline:
        head = predecessor._current_main(observability, repo)
        if not head or not predecessor._is_ancestor(
            observability,
            repo,
            str(target["receipt_introduction_commit"]),
            head,
        ):
            raise AutonomyError(
                "post-receipt protected main is not descended from receipt introduction"
            )
        run_id = predecessor._successful_sync_run(observability, repo, head)
        current = run_id > 0 and predecessor._mirrors_current(
            evidence, runtime, head, frontier
        )
        if current:
            if run_id == stable_run:
                stable_reads += 1
            else:
                stable_run = run_id
                stable_reads = 1
            if stable_reads >= int(control["correction"]["stable_mirror_observations_required"]):
                return run_id
        else:
            stable_run = 0
            stable_reads = 0
        time.sleep(poll)

    raise AutonomyError(
        "post-receipt validated-current-frontier mirror synchronization timed out"
    )
