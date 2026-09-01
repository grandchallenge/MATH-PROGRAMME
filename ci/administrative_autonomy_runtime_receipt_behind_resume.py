from __future__ import annotations

import json
import time
import urllib.parse
from pathlib import Path
from typing import Any, Callable

from administrative_automation import canonical_digest, parse_datetime
from autonomy_github import AutonomyError, Client, delete_branch, json_content, required_contexts, wait_checks
from administrative_autonomy_receipt_stage import (
    STATE_PATH,
    advance_completion_state,
    branch_ref,
    completion_has_receipt,
    receipt_for,
    stage_completion_receipt as base_stage_completion_receipt,
    verify_receipt_scope,
    wait_completion_readback,
)
from administrative_autonomy_runtime_github import exact_head_merge, record_referee_disposition, wait_clean
from administrative_protected_receipt_adapters import UpdateBranchState
from administrative_protected_receipt_live import classify_receipt_pull_for_sync
from administrative_protected_receipt_model import BranchState, ConflictState

ROOT = Path(__file__).resolve().parents[1]
CONTROL_PATH = ROOT / "governance" / "administrative_autonomy_receipt_behind_resume_control.json"
RECEIPT_BRANCH_PREFIX = "automation/maintenance/receipt-"
CompletionLoader = Callable[[Client, str, str, str], dict[str, Any] | None]


def load_control() -> dict[str, Any]:
    return json.loads(CONTROL_PATH.read_text(encoding="utf-8"))


def validate_control(control: dict[str, Any]) -> None:
    if control.get("control_id") != "MP-ADMIN-RECEIPT-BEHIND-RESUME-001":
        raise AutonomyError("receipt BEHIND resume control identity drift")
    if control.get("status") != "ACTIVE_WHEN_PROTECTED":
        raise AutonomyError("receipt BEHIND resume control is not active")
    if control.get("repository") != "grandchallenge/MATH-PROGRAMME":
        raise AutonomyError("receipt BEHIND resume repository drift")
    sync = control.get("synchronization", {})
    required = {
        "branch_prefix": RECEIPT_BRANCH_PREFIX,
        "base_branch": "main",
        "state_path": STATE_PATH,
        "expected_head_required": True,
        "single_open_pull_required": True,
        "same_repository_required": True,
        "exact_payload_required_before_and_after_sync": True,
        "synchronize_only_when_behind": True,
        "clean_resume_allowed": True,
        "fresh_exact_head_checks_required": True,
        "fresh_referee_disposition_required": True,
        "ordinary_protected_merge_required": True,
    }
    for key, expected in required.items():
        if sync.get(key) != expected:
            raise AutonomyError(f"receipt BEHIND resume control drift: {key}")
    authority = control.get("authority_boundary", {})
    if authority.get("human_steward_identity_asserted") is not False:
        raise AutonomyError("receipt BEHIND resume asserts Human Steward identity")
    if authority.get("bypass_may_be_exercised") is not False:
        raise AutonomyError("receipt BEHIND resume permits bypass")
    if authority.get("direct_protected_push") is not False:
        raise AutonomyError("receipt BEHIND resume permits direct protected push")
    claims = control.get("claim_boundaries", {})
    if not claims or any(value is not False for value in claims.values()):
        raise AutonomyError("receipt BEHIND resume claim boundaries must remain false")


def _open_receipt_pulls(candidate: Client, repo: str, branch: str) -> list[dict[str, Any]]:
    owner = repo.split("/", 1)[0]
    query = urllib.parse.urlencode({"state": "open", "head": f"{owner}:{branch}", "per_page": 20})
    pulls = candidate.get(f"/repos/{repo}/pulls?{query}")
    if not isinstance(pulls, list):
        raise AutonomyError("receipt BEHIND resume pull query returned invalid data")
    return pulls


def _validate_receipt_pull(pull: dict[str, Any], repo: str, branch: str, base_branch: str) -> tuple[int, str]:
    if pull.get("state") != "open":
        raise AutonomyError("receipt BEHIND resume pull request is not open")
    if pull.get("draft") is True:
        raise AutonomyError("receipt BEHIND resume pull request is draft")
    head = pull.get("head", {})
    base = pull.get("base", {})
    if str(head.get("ref") or "") != branch:
        raise AutonomyError("receipt BEHIND resume branch identity drift")
    if str(base.get("ref") or "") != base_branch:
        raise AutonomyError("receipt BEHIND resume base branch drift")
    if str(head.get("repo", {}).get("full_name") or repo) != repo:
        raise AutonomyError("receipt BEHIND resume head repository drift")
    number = int(pull.get("number") or 0)
    head_sha = str(head.get("sha") or "")
    if not number or len(head_sha) != 40 or any(c not in "0123456789abcdef" for c in head_sha):
        raise AutonomyError("receipt BEHIND resume pull identity is invalid")
    return number, head_sha


def _require_exact_completion(candidate: Client, repo: str, ref: str, expected: dict[str, Any], completion_loader: CompletionLoader = json_content) -> None:
    actual = completion_loader(candidate, repo, STATE_PATH, ref)
    if actual is None or canonical_digest(actual) != canonical_digest(expected):
        raise AutonomyError("receipt BEHIND resume completion payload drift")


def _wait_head_change(candidate: Client, repo: str, pull_request: int, branch: str, base_branch: str, previous_head: str, timeout: int, poll: int) -> dict[str, Any]:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        pull = candidate.get(f"/repos/{repo}/pulls/{pull_request}")
        _, head = _validate_receipt_pull(pull, repo, branch, base_branch)
        if head != previous_head:
            return pull
        time.sleep(poll)
    raise AutonomyError("receipt BEHIND head-change readback timed out")


def _wait_typed_sync_facts(candidate: Client, repo: str, pull_request: int, declared_base: str, timeout: int, poll: int):
    deadline = time.monotonic() + timeout
    last = None
    while time.monotonic() < deadline:
        last = classify_receipt_pull_for_sync(
            candidate,
            repo,
            pull_request,
            declared_base,
            update_control_permitted=True,
        )
        if last.branch_state != BranchState.UNKNOWN and last.conflict_state != ConflictState.UNKNOWN:
            return last
        time.sleep(poll)
    raise AutonomyError(f"receipt typed-state readback timed out: {last}")


def resume_existing_receipt(
    candidate: Client,
    repo: str,
    branch: str,
    completion: dict[str, Any],
    control: dict[str, Any],
    completion_loader: CompletionLoader = json_content,
) -> tuple[dict[str, Any], str, dict[str, Any]] | None:
    validate_control(control)
    sync = control["synchronization"]
    if not branch.startswith(str(sync["branch_prefix"])):
        raise AutonomyError("receipt BEHIND resume branch is outside bounded namespace")
    ref = branch_ref(candidate, repo, branch)
    if ref is None:
        return None
    observed_ref = str(ref.get("object", {}).get("sha") or "")
    pulls = _open_receipt_pulls(candidate, repo, branch)
    if len(pulls) != 1:
        raise AutonomyError("receipt BEHIND resume requires exactly one open pull request")
    pull = pulls[0]
    receipt_pr, observed_head = _validate_receipt_pull(pull, repo, branch, str(sync["base_branch"]))
    if observed_ref != observed_head:
        raise AutonomyError("receipt BEHIND resume branch/pull head mismatch")
    _require_exact_completion(candidate, repo, observed_head, completion, completion_loader)
    verify_receipt_scope(candidate, repo, receipt_pr)

    declared_base = str(completion.get("derived_from_protected_head") or "")
    if len(declared_base) != 40:
        raise AutonomyError("receipt BEHIND resume declared base snapshot is absent")
    facts = _wait_typed_sync_facts(
        candidate,
        repo,
        receipt_pr,
        declared_base,
        int(sync["merge_state_wait_seconds"]),
        int(sync["poll_interval_seconds"]),
    )
    pull = candidate.get(f"/repos/{repo}/pulls/{receipt_pr}")
    _, observed_head = _validate_receipt_pull(pull, repo, branch, str(sync["base_branch"]))
    event: dict[str, Any] = {
        "control_id": control["control_id"],
        "pull_request": receipt_pr,
        "branch": branch,
        "previous_head": observed_head,
        "trigger": facts.branch_state.value,
        "branch_state": facts.branch_state.value,
        "conflict_state": facts.conflict_state.value,
        "raw_advisory": facts.raw_advisory,
        "expected_head_used": False,
    }
    if facts.conflict_state == ConflictState.CONFLICTED:
        raise AutonomyError("receipt synchronization rejected true content conflict")
    if facts.branch_state == BranchState.BEHIND_CURRENT_BASE:
        if facts.update_branch_state != UpdateBranchState.PERMITTED_TO_ATTEMPT:
            raise AutonomyError("receipt synchronization is not permitted by typed state")
        candidate.put(
            f"/repos/{repo}/pulls/{receipt_pr}/update-branch",
            {"expected_head_sha": observed_head},
        )
        pull = _wait_head_change(
            candidate,
            repo,
            receipt_pr,
            branch,
            str(sync["base_branch"]),
            observed_head,
            int(sync["head_change_wait_seconds"]),
            int(sync["poll_interval_seconds"]),
        )
        _, receipt_head = _validate_receipt_pull(pull, repo, branch, str(sync["base_branch"]))
        event |= {"synchronized_head": receipt_head, "expected_head_used": True}
    elif facts.branch_state == BranchState.AT_CURRENT_BASE and sync.get("clean_resume_allowed") is True:
        receipt_head = observed_head
        event["synchronized_head"] = receipt_head
    else:
        raise AutonomyError(f"receipt synchronization rejected typed branch state: {facts.branch_state.value}")

    _require_exact_completion(candidate, repo, receipt_head, completion, completion_loader)
    verify_receipt_scope(candidate, repo, receipt_pr)
    return pull, receipt_head, event


def _existing_exact_disposition(referee: Client, repo: str, pull_request: int, exact_head: str, referee_login: str) -> dict[str, Any] | None:
    expected = f"- exact head: `{exact_head}`;"
    comments = referee.get(f"/repos/{repo}/issues/{pull_request}/comments?per_page=100")
    matches = [
        item for item in comments
        if item.get("user", {}).get("login") == referee_login
        and str(item.get("body") or "").startswith("REFEREE_AGENT_APPROVED_EXACT_HEAD_ADMINISTRATIVE_MAINTENANCE")
        and expected in str(item.get("body") or "")
        and "REFEREE_AGENT_AUTHORIZED_EXACT_HEAD_PROTECTED_MERGE" in str(item.get("body") or "")
    ]
    if len(matches) > 1:
        raise AutonomyError("duplicate exact-head receipt Referee disposition")
    return matches[0] if matches else None


def stage_completion_receipt(
    candidate: Client,
    referee: Client,
    administrator: Client,
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
) -> dict[str, Any]:
    control = load_control()
    validate_control(control)
    if repo != control["repository"]:
        raise AutonomyError("receipt BEHIND resume runtime repository drift")
    current = json_content(candidate, repo, STATE_PATH, "main")
    if current is None:
        raise AutonomyError("protected completion ledger is absent")
    receipt = receipt_for(procedure_id, due, record_path, record, source_merge_sha, source_head, source_pull_request)
    if completion_has_receipt(current, receipt):
        return base_stage_completion_receipt(candidate, referee, administrator, repo, runtime, record_id, procedure_id, due, record_path, record, source_pull_request, source_head, source_merge_sha, referee_login, candidate_login)
    completion = advance_completion_state(current, receipt, source_merge_sha)
    compact = parse_datetime(due).strftime("%Y%m%dT%H%M%SZ")
    branch = f"automation/maintenance/receipt-{procedure_id}-{compact}"
    resumed = resume_existing_receipt(candidate, repo, branch, completion, control)
    if resumed is None:
        return base_stage_completion_receipt(candidate, referee, administrator, repo, runtime, record_id, procedure_id, due, record_path, record, source_pull_request, source_head, source_merge_sha, referee_login, candidate_login)
    pull, receipt_head, synchronization = resumed
    receipt_pr = int(pull["number"])
    live_ruleset = administrator.get(f"/repos/{repo}/rulesets/{runtime['ruleset_id']}")
    contexts = required_contexts(live_ruleset)
    checks = wait_checks(referee, repo, receipt_head, contexts, int(runtime["merge_control"]["maximum_check_wait_seconds"]))
    disposition = _existing_exact_disposition(referee, repo, receipt_pr, receipt_head, referee_login)
    if disposition is None:
        disposition = record_referee_disposition(referee, repo, receipt_pr, receipt_head, f"{record_id}-RECEIPT", checks, referee_login)
    post_checks = wait_clean(candidate, referee, repo, str(pull["node_id"]), receipt_head, referee_login, contexts, runtime["merge_control"], time.monotonic())
    merged = exact_head_merge(candidate, repo, receipt_pr, receipt_head, f"{record_id}-RECEIPT", candidate_login)
    receipt_merge = str(merged["merge_commit_sha"])
    wait_completion_readback(candidate, repo, completion, int(runtime["merge_control"]["maximum_protected_readback_wait_seconds"]), int(runtime["merge_control"]["poll_interval_seconds"]))
    delete_branch(candidate, repo, branch)
    return {
        "receipt": receipt,
        "completion": completion,
        "receipt_pull_request": receipt_pr,
        "receipt_head": receipt_head,
        "receipt_checks": checks,
        "receipt_post_disposition_checks": post_checks,
        "receipt_disposition_comment_id": int(disposition["id"]),
        "receipt_merge_commit": receipt_merge,
        "receipt_recovered": False,
        "receipt_behind_synchronization": synchronization,
    }
