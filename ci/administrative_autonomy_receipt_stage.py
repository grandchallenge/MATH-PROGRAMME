from __future__ import annotations

import base64
import copy
import hashlib
import json
import time
import urllib.parse
from typing import Any

from administrative_automation import canonical_digest, iso_z, parse_datetime, validate_completion_state
from autonomy_github import AutonomyError, Client, delete_branch, json_content, required_contexts, wait_checks
from administrative_autonomy_runtime_github import (
    exact_head_merge,
    mark_ready,
    record_referee_disposition,
    wait_clean,
)

STATE_PATH = "governance/administrative_maintenance_completion_state.json"
DISPOSITION = "REFEREE_AGENT_AUTHORIZED_EXACT_HEAD_PROTECTED_MERGE"


def record_payload(record: dict[str, Any]) -> bytes:
    return (json.dumps(record, indent=2) + "\n").encode("utf-8")


def receipt_for(
    procedure_id: str,
    due: str,
    record_path: str,
    record: dict[str, Any],
    merge_sha: str,
    reviewed_head: str,
    pull_request: int,
) -> dict[str, Any]:
    return {
        "procedure_id": procedure_id,
        "scheduled_due_at": iso_z(parse_datetime(due)),
        "record_path": record_path,
        "record_sha256": hashlib.sha256(record_payload(record)).hexdigest(),
        "merge_commit": merge_sha,
        "reviewed_head": reviewed_head,
        "pull_request": int(pull_request),
        "disposition": DISPOSITION,
        "receipt_state": "PROTECTED_COMPLETE",
    }


def same_receipt(left: dict[str, Any], right: dict[str, Any]) -> bool:
    keys = (
        "procedure_id",
        "scheduled_due_at",
        "record_path",
        "merge_commit",
        "reviewed_head",
        "pull_request",
        "disposition",
    )
    return all(left.get(key) == right.get(key) for key in keys)


def completion_has_receipt(completion: dict[str, Any], receipt: dict[str, Any]) -> bool:
    procedure = completion.get("procedures", {}).get(receipt["procedure_id"], {})
    return any(same_receipt(item, receipt) for item in procedure.get("receipts", []))


def advance_completion_state(
    current: dict[str, Any],
    receipt: dict[str, Any],
    protected_record_merge: str,
) -> dict[str, Any]:
    completion = copy.deepcopy(current)
    if completion_has_receipt(completion, receipt):
        return completion
    procedure = completion.get("procedures", {}).get(receipt["procedure_id"])
    if not isinstance(procedure, dict):
        raise AutonomyError("completion ledger procedure is absent")
    due = parse_datetime(receipt["scheduled_due_at"])
    completed_raw = procedure.get("completed_through_utc")
    if completed_raw and due <= parse_datetime(str(completed_raw)):
        raise AutonomyError("completion receipt would not advance the protected ledger")
    receipts = list(procedure.get("receipts", []))
    receipts.append(copy.deepcopy(receipt))
    receipts.sort(key=lambda item: (item["scheduled_due_at"], item["record_path"]))
    procedure["receipts"] = receipts
    procedure["receipt_count"] = len(receipts)
    procedure["completed_through_utc"] = iso_z(due)
    completion["derived_from_protected_head"] = protected_record_merge
    errors = validate_completion_state(completion, current)
    if errors:
        raise AutonomyError("; ".join(errors))
    return completion


def wait_pull_head(
    client: Client,
    repo: str,
    pull_request: int,
    expected_head: str,
    timeout: int,
    poll: int,
) -> dict[str, Any]:
    deadline = time.monotonic() + timeout
    last = ""
    while time.monotonic() < deadline:
        pull = client.get(f"/repos/{repo}/pulls/{pull_request}")
        last = str(pull.get("head", {}).get("sha") or "")
        if last == expected_head:
            return pull
        time.sleep(poll)
    raise AutonomyError(
        f"finalized maintenance head readback timed out: expected {expected_head}, observed {last}"
    )


def put_completion_state(
    candidate: Client,
    repo: str,
    branch: str,
    completion: dict[str, Any],
) -> str:
    old = candidate.get(
        f"/repos/{repo}/contents/{STATE_PATH}?ref={urllib.parse.quote(branch, safe='')}"
    )
    payload = {
        "message": (
            "Bind autonomous protected completion receipt "
            f"{completion['derived_from_protected_head'][:12]}"
        ),
        "content": base64.b64encode(
            (json.dumps(completion, indent=2) + "\n").encode("utf-8")
        ).decode("ascii"),
        "branch": branch,
        "sha": old["sha"],
    }
    result = candidate.put(f"/repos/{repo}/contents/{STATE_PATH}", payload)
    return str(result["commit"]["sha"])


def branch_ref(candidate: Client, repo: str, branch: str) -> dict[str, Any] | None:
    encoded = urllib.parse.quote(branch, safe="")
    try:
        return candidate.get(f"/repos/{repo}/git/ref/heads/{encoded}")
    except AutonomyError as exc:
        if " 404 " in str(exc):
            return None
        raise


def ensure_branch(
    candidate: Client,
    repo: str,
    branch: str,
    base_sha: str,
) -> None:
    existing = branch_ref(candidate, repo, branch)
    if existing is None:
        candidate.post(
            f"/repos/{repo}/git/refs",
            {"ref": f"refs/heads/{branch}", "sha": base_sha},
        )
        return
    actual = str(existing.get("object", {}).get("sha") or "")
    if actual != base_sha:
        raise AutonomyError("receipt branch exists at an unexpected head")


def find_open_pull(candidate: Client, repo: str, branch: str) -> dict[str, Any] | None:
    owner = repo.split("/", 1)[0]
    query = urllib.parse.urlencode(
        {"state": "open", "head": f"{owner}:{branch}", "per_page": 20}
    )
    pulls = candidate.get(f"/repos/{repo}/pulls?{query}")
    return pulls[0] if pulls else None


def create_receipt_pull(
    candidate: Client,
    repo: str,
    branch: str,
    record_id: str,
    source_pull_request: int,
    source_merge_sha: str,
    receipt_head: str,
) -> dict[str, Any]:
    pull = find_open_pull(candidate, repo, branch)
    if pull is None:
        pull = candidate.post(
            f"/repos/{repo}/pulls",
            {
                "title": f"[maintenance-receipt] {record_id}",
                "head": branch,
                "base": "main",
                "draft": True,
                "maintainer_can_modify": False,
                "body": (
                    f"Binds the protected completion receipt for autonomous maintenance PR #{source_pull_request}.\n\n"
                    f"- protected record merge: `{source_merge_sha}`;\n"
                    f"- receipt head: `{receipt_head}`;\n"
                    "- changed path: `governance/administrative_maintenance_completion_state.json`;\n"
                    "- Candidate and merge executor: `gcl-release-trust[bot]`;\n"
                    "- Referee: `github-actions[bot]`;\n"
                    "- Human Steward disposition: not required and not asserted;\n"
                    "- bypass exercise: prohibited;\n"
                    "- substantive claim authority: excluded."
                ),
            },
        )
    if pull.get("draft") is True:
        mark_ready(candidate, str(pull["node_id"]))
    return candidate.get(f"/repos/{repo}/pulls/{int(pull['number'])}")


def verify_receipt_scope(
    candidate: Client,
    repo: str,
    pull_request: int,
) -> None:
    files = candidate.get(f"/repos/{repo}/pulls/{pull_request}/files?per_page=100")
    names = [str(item.get("filename") or "") for item in files]
    if names != [STATE_PATH]:
        raise AutonomyError(f"completion receipt path drift: {names}")
    if sum(int(item.get("additions") or 0) for item in files) > 5000:
        raise AutonomyError("completion receipt additions exceed bounded scope")
    if sum(int(item.get("deletions") or 0) for item in files) > 5000:
        raise AutonomyError("completion receipt deletions exceed bounded scope")


def wait_completion_readback(
    candidate: Client,
    repo: str,
    expected: dict[str, Any],
    timeout: int,
    poll: int,
) -> None:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        actual = json_content(candidate, repo, STATE_PATH, "main")
        if actual is not None and canonical_digest(actual) == canonical_digest(expected):
            return
        time.sleep(poll)
    raise AutonomyError("protected completion receipt readback timed out")


def find_referee_disposition(
    client: Client,
    repo: str,
    pull_request: int,
    exact_head: str,
    referee_login: str,
) -> dict[str, Any]:
    expected = f"- exact head: `{exact_head}`;"
    comments = client.get(f"/repos/{repo}/issues/{pull_request}/comments?per_page=100")
    matches = [
        item
        for item in comments
        if item.get("user", {}).get("login") == referee_login
        and str(item.get("body") or "").startswith(
            "REFEREE_AGENT_APPROVED_EXACT_HEAD_ADMINISTRATIVE_MAINTENANCE"
        )
        and expected in str(item.get("body") or "")
        and DISPOSITION in str(item.get("body") or "")
    ]
    if len(matches) != 1:
        raise AutonomyError("exact-head Referee disposition is absent or ambiguous")
    return matches[0]


def locate_receipt_protection_head(
    candidate: Client,
    repo: str,
    receipt: dict[str, Any],
) -> str:
    commits = candidate.get(
        f"/repos/{repo}/commits?path={urllib.parse.quote(STATE_PATH, safe='')}&per_page=100"
    )
    for commit in commits:
        sha = str(commit.get("sha") or "")
        if not sha:
            continue
        value = json_content(candidate, repo, STATE_PATH, sha)
        if value is not None and completion_has_receipt(value, receipt):
            return sha
    raise AutonomyError("protected completion receipt introduction commit is absent")


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
    current = json_content(candidate, repo, STATE_PATH, "main")
    if current is None:
        raise AutonomyError("protected completion ledger is absent")
    receipt = receipt_for(
        procedure_id,
        due,
        record_path,
        record,
        source_merge_sha,
        source_head,
        source_pull_request,
    )
    if completion_has_receipt(current, receipt):
        return {
            "receipt": receipt,
            "completion": current,
            "receipt_pull_request": None,
            "receipt_head": None,
            "receipt_disposition_comment_id": None,
            "receipt_merge_commit": locate_receipt_protection_head(
                candidate, repo, receipt
            ),
            "receipt_recovered": True,
        }

    completion = advance_completion_state(current, receipt, source_merge_sha)
    main = candidate.get(f"/repos/{repo}/branches/main")
    base_sha = str(main["commit"]["sha"])
    compact = parse_datetime(due).strftime("%Y%m%dT%H%M%SZ")
    branch = f"automation/maintenance/receipt-{procedure_id}-{compact}"
    ensure_branch(candidate, repo, branch, base_sha)
    receipt_head = put_completion_state(candidate, repo, branch, completion)
    pull = create_receipt_pull(
        candidate,
        repo,
        branch,
        record_id,
        source_pull_request,
        source_merge_sha,
        receipt_head,
    )
    receipt_pr = int(pull["number"])
    pull = wait_pull_head(
        candidate,
        repo,
        receipt_pr,
        receipt_head,
        int(runtime["merge_control"]["maximum_stabilization_wait_seconds"]),
        int(runtime["merge_control"]["poll_interval_seconds"]),
    )
    if pull.get("draft") is True:
        raise AutonomyError("completion receipt pull request remained draft")
    verify_receipt_scope(candidate, repo, receipt_pr)

    live_ruleset = administrator.get(
        f"/repos/{repo}/rulesets/{runtime['ruleset_id']}"
    )
    contexts = required_contexts(live_ruleset)
    checks = wait_checks(
        referee,
        repo,
        receipt_head,
        contexts,
        int(runtime["merge_control"]["maximum_check_wait_seconds"]),
    )
    disposition = record_referee_disposition(
        referee,
        repo,
        receipt_pr,
        receipt_head,
        f"{record_id}-RECEIPT",
        checks,
        referee_login,
    )
    post_checks = wait_clean(
        candidate,
        referee,
        repo,
        str(pull["node_id"]),
        receipt_head,
        referee_login,
        contexts,
        runtime["merge_control"],
        time.monotonic(),
    )
    merged = exact_head_merge(
        candidate,
        repo,
        receipt_pr,
        receipt_head,
        f"{record_id}-RECEIPT",
        candidate_login,
    )
    receipt_merge = str(merged["merge_commit_sha"])
    wait_completion_readback(
        candidate,
        repo,
        completion,
        int(runtime["merge_control"]["maximum_protected_readback_wait_seconds"]),
        int(runtime["merge_control"]["poll_interval_seconds"]),
    )
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
    }


def pending_closures(
    candidate: Client,
    repo: str,
    runtime: dict[str, Any],
    referee_login: str,
) -> list[dict[str, Any]]:
    directory = str(runtime["scope"]["candidate_manifest_prefix"]).rstrip("/")
    entries = candidate.get(f"/repos/{repo}/contents/{directory}?ref=main")
    completion = json_content(candidate, repo, STATE_PATH, "main")
    if completion is None:
        raise AutonomyError("protected completion ledger is absent")
    pending: list[dict[str, Any]] = []
    record_directories = {
        str(value["directory"]).rstrip("/")
        for value in runtime["record_layout"].values()
    }
    for entry in entries:
        if str(entry.get("name") or "").endswith(".json") is False:
            continue
        manifest = json_content(candidate, repo, str(entry["path"]), "main")
        if not manifest or manifest.get("procedure_id") not in runtime["automated_procedures"]:
            continue
        issue_number = int(manifest.get("issue_number") or 0)
        pull_request = int(manifest.get("pull_request_number") or 0)
        if not issue_number or not pull_request:
            continue
        issue = candidate.get(f"/repos/{repo}/issues/{issue_number}")
        if issue.get("state") != "open":
            continue
        pull = candidate.get(f"/repos/{repo}/pulls/{pull_request}")
        if pull.get("merged") is not True:
            continue
        files = candidate.get(f"/repos/{repo}/pulls/{pull_request}/files?per_page=100")
        paths = [
            str(item.get("filename") or "")
            for item in files
            if any(
                str(item.get("filename") or "").startswith(f"{directory}/")
                for directory in record_directories
            )
        ]
        if len(paths) != 1:
            raise AutonomyError("merged maintenance record path is absent or ambiguous")
        record_path = paths[0]
        record = json_content(candidate, repo, record_path, "main")
        if not record or record.get("status") != "COMPLETE_AUTONOMOUS":
            raise AutonomyError("merged maintenance record is absent or not autonomous-complete")
        exact_head = str(pull.get("head", {}).get("sha") or "")
        disposition = find_referee_disposition(
            candidate, repo, pull_request, exact_head, referee_login
        )
        receipt = receipt_for(
            str(manifest["procedure_id"]),
            str(manifest["scheduled_due_at"]),
            record_path,
            record,
            str(pull["merge_commit_sha"]),
            exact_head,
            pull_request,
        )
        pending.append(
            {
                "manifest": manifest,
                "record": record,
                "record_id": str(record["record_id"]),
                "record_path": record_path,
                "issue_number": issue_number,
                "pull_request": pull_request,
                "exact_head": exact_head,
                "record_merge_commit": str(pull["merge_commit_sha"]),
                "record_disposition_comment_id": int(disposition["id"]),
                "receipt_present": completion_has_receipt(completion, receipt),
                "receipt": receipt,
            }
        )
    return pending
