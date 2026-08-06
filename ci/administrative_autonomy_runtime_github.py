from __future__ import annotations

import base64
import json
import time
import urllib.parse
from datetime import datetime, timedelta
from typing import Any

from administrative_automation import canonical_digest, parse_datetime
from autonomy_github import AutonomyError, Client, content, json_content


def gql(client: Client, query: str, variables: dict[str, Any]) -> dict[str, Any]:
    result = client.post("/graphql", {"query": query, "variables": variables})
    if result.get("errors"):
        raise AutonomyError(f"GraphQL operation failed: {result['errors']}")
    return result


def mark_ready(client: Client, node_id: str) -> None:
    result = gql(
        client,
        "mutation($id:ID!){markPullRequestReadyForReview(input:{pullRequestId:$id}){pullRequest{number isDraft headRefOid}}}",
        {"id": node_id},
    )
    value = result.get("data", {}).get("markPullRequestReadyForReview", {}).get("pullRequest", {})
    if value.get("isDraft") is not False:
        raise AutonomyError("candidate pull request did not become review-ready")


def pull_snapshot(client: Client, node_id: str) -> dict[str, Any]:
    result = gql(
        client,
        "query($id:ID!){node(id:$id){... on PullRequest{number state isDraft headRefOid mergeStateStatus}}}",
        {"id": node_id},
    )
    value = result.get("data", {}).get("node")
    if not isinstance(value, dict):
        raise AutonomyError("pull-request state query returned no pull request")
    return value


def put_record(client: Client, repo: str, branch: str, path: str, record: dict[str, Any]) -> str:
    old = content(client, repo, path, branch)
    payload: dict[str, Any] = {
        "message": f"Finalize autonomous administrative record {record['record_id']}",
        "content": base64.b64encode((json.dumps(record, indent=2) + "\n").encode("utf-8")).decode("ascii"),
        "branch": branch,
    }
    if old:
        payload["sha"] = old["sha"]
    result = client.put(f"/repos/{repo}/contents/{path}", payload)
    return result["commit"]["sha"]


def verify_scope(client: Client, repo: str, pr: int, manifest_path: str, record_path: str, scope: dict[str, Any]) -> None:
    files = client.get(f"/repos/{repo}/pulls/{pr}/files?per_page=100")
    names = [item["filename"] for item in files]
    if names != sorted([manifest_path, record_path]):
        raise AutonomyError(f"autonomous maintenance path drift: {names}")
    if len(files) > int(scope["maximum_changed_files"]):
        raise AutonomyError("autonomous maintenance changed-file limit exceeded")
    additions = sum(int(item.get("additions") or 0) for item in files)
    deletions = sum(int(item.get("deletions") or 0) for item in files)
    if additions > int(scope["maximum_additions"]) or deletions > int(scope["maximum_deletions"]):
        raise AutonomyError("autonomous maintenance line-change limit exceeded")


def update_execution_issue(
    candidate: Client,
    repo: str,
    issue: int,
    manifest: dict[str, Any],
    record_id: str,
    exact_head: str,
) -> None:
    marker = f"<!-- administrative-candidate:{manifest['occurrence_key']} -->"
    body = (
        f"{marker}\n# Autonomous bounded administrative execution\n\n"
        "## State\n\n`AUTONOMOUS_FINALIZATION_IN_PROGRESS`\n\n"
        "This issue is a navigation and execution mirror. Protected records, merge receipts, and Referee readback remain authoritative.\n\n"
        f"- record: `{record_id}`;\n"
        f"- procedure: `{manifest['procedure_id']}`;\n"
        f"- occurrence: `{manifest['occurrence_key']}`;\n"
        f"- scheduled due: `{manifest['scheduled_due_at']}`;\n"
        f"- exact finalized head: `{exact_head}`;\n"
        "- Candidate and merge executor: `gcl-release-trust[bot]`;\n"
        "- Referee: `github-actions[bot]`;\n"
        "- Human Steward disposition: not required and not asserted;\n"
        "- bypass exercise: prohibited;\n"
        "- mathematical, source, certification, and external-claim authority: excluded.\n\n"
        "The operation remains fail closed until successful exact-head checks, Referee disposition, clean-state merge, protected record readback, and mirror synchronization complete.\n"
    )
    updated = candidate.patch(
        f"/repos/{repo}/issues/{issue}",
        {"body": body},
    )
    if marker not in str(updated.get("body") or ""):
        raise AutonomyError("execution issue update readback failed")


def close_execution_issue(
    candidate: Client,
    repo: str,
    issue: int,
    manifest: dict[str, Any],
    record_id: str,
    exact_head: str,
    merge_sha: str,
    disposition_id: int,
    readback_id: int,
    synchronization_run: int,
) -> None:
    marker = f"<!-- administrative-candidate:{manifest['occurrence_key']} -->"
    body = (
        f"{marker}\n# Autonomous bounded administrative execution\n\n"
        "## State\n\n`PROTECTED_COMPLETE`\n\n"
        "This issue is a navigation mirror. The protected record and merge receipt are authoritative.\n\n"
        f"- record: `{record_id}`;\n"
        f"- occurrence: `{manifest['occurrence_key']}`;\n"
        f"- exact approved head: `{exact_head}`;\n"
        f"- Referee disposition comment: `{disposition_id}`;\n"
        f"- protected merge: `{merge_sha}`;\n"
        f"- protected readback comment: `{readback_id}`;\n"
        f"- mirror synchronization run: `{synchronization_run}`;\n"
        "- Candidate/Referee/merge-executor separation: verified;\n"
        "- bypass used: `false`;\n"
        "- Human Steward identity asserted: `false`;\n"
        "- mathematical or certification authority asserted: `false`.\n"
    )
    updated = candidate.patch(
        f"/repos/{repo}/issues/{issue}",
        {"body": body, "state": "closed", "state_reason": "completed"},
    )
    if updated.get("state") != "closed" or marker not in str(updated.get("body") or ""):
        raise AutonomyError("execution issue closure readback failed")


def record_referee_disposition(
    referee: Client,
    repo: str,
    pr: int,
    sha: str,
    record_id: str,
    checks: dict[str, str],
    referee_login: str,
) -> dict[str, Any]:
    check_lines = "\n".join(f"- `{name}`: `{result}`;" for name, result in sorted(checks.items()))
    body = (
        "REFEREE_AGENT_APPROVED_EXACT_HEAD_ADMINISTRATIVE_MAINTENANCE\n\n"
        f"- record: `{record_id}`;\n"
        f"- exact head: `{sha}`;\n"
        "- approval record: `issue_comment`;\n"
        "- Human Steward disposition: `false`;\n"
        "- identity separation: verified;\n"
        "- changed-path scope: verified;\n"
        "- claim boundaries: all `false`;\n"
        "- live required checks:\n"
        f"{check_lines}\n\n"
        "Disposition: `REFEREE_AGENT_AUTHORIZED_EXACT_HEAD_PROTECTED_MERGE`."
    )
    comment = referee.post(f"/repos/{repo}/issues/{pr}/comments", {"body": body})
    if comment.get("user", {}).get("login") != referee_login:
        raise AutonomyError("Referee disposition actor readback failed")
    return comment


def disposition_present(referee: Client, repo: str, pr: int, sha: str, referee_login: str) -> bool:
    expected = f"- exact head: `{sha}`;"
    comments = referee.get(f"/repos/{repo}/issues/{pr}/comments?per_page=100")
    return any(
        item.get("user", {}).get("login") == referee_login
        and str(item.get("body") or "").startswith("REFEREE_AGENT_APPROVED_EXACT_HEAD_ADMINISTRATIVE_MAINTENANCE")
        and expected in str(item.get("body") or "")
        and "REFEREE_AGENT_AUTHORIZED_EXACT_HEAD_PROTECTED_MERGE" in str(item.get("body") or "")
        for item in comments
    )


def check_runs_state(client: Client, repo: str, sha: str, accepted: set[str], required: set[str]) -> tuple[bool, dict[str, str]]:
    runs = client.get(f"/repos/{repo}/commits/{sha}/check-runs?per_page=100").get("check_runs", [])
    latest: dict[str, dict[str, Any]] = {}
    for run in runs:
        name = str(run.get("name") or "unnamed")
        if name not in latest or str(run.get("started_at") or "") > str(latest[name].get("started_at") or ""):
            latest[name] = run
    observed: dict[str, str] = {}
    pending = False
    for name, run in latest.items():
        status = str(run.get("status") or "missing")
        conclusion = run.get("conclusion")
        observed[name] = status if status != "completed" else str(conclusion)
        if status != "completed":
            pending = True
        elif conclusion not in accepted:
            raise AutonomyError(f"post-disposition check run failed: {name}={conclusion}")
    for name in required:
        if name not in latest:
            observed[name] = "missing"
            pending = True
    return bool(latest) and not pending, observed


def wait_clean(
    candidate: Client,
    referee: Client,
    repo: str,
    node_id: str,
    sha: str,
    referee_login: str,
    required: list[str],
    control: dict[str, Any],
    disposition_at: float,
) -> dict[str, str]:
    deadline = time.monotonic() + int(control["maximum_stabilization_wait_seconds"])
    accepted = set(control["accepted_check_conclusions"])
    poll = int(control["poll_interval_seconds"])
    minimum = int(control["minimum_post_disposition_settle_seconds"])
    last: dict[str, Any] = {}
    stable_since: float | None = None
    stable_fingerprint = ""
    while time.monotonic() < deadline:
        snapshot = pull_snapshot(candidate, node_id)
        if snapshot.get("state") != "OPEN" or snapshot.get("isDraft") is not False or snapshot.get("headRefOid") != sha:
            raise AutonomyError("maintenance pull request changed before merge")
        if not disposition_present(referee, repo, int(snapshot["number"]), sha, referee_login):
            raise AutonomyError("exact-head Referee disposition disappeared")
        settled, checks = check_runs_state(referee, repo, sha, accepted, set(required))
        merge_state = snapshot.get("mergeStateStatus")
        last = {"merge_state": merge_state, "checks": checks}
        fingerprint = canonical_digest({"merge_state": merge_state, "checks": checks})
        clean = settled and merge_state == control["required_pre_merge_state"]
        if clean and fingerprint == stable_fingerprint:
            if stable_since is None:
                stable_since = time.monotonic()
        elif clean:
            stable_fingerprint = fingerprint
            stable_since = time.monotonic()
        else:
            stable_fingerprint = fingerprint
            stable_since = None
        if (
            stable_since is not None
            and time.monotonic() - disposition_at >= minimum
            and time.monotonic() - stable_since >= minimum
        ):
            return checks
        time.sleep(poll)
    raise AutonomyError(f"post-disposition stabilization timed out: {last}")


def exact_head_merge(candidate: Client, repo: str, pr: int, sha: str, record_id: str, candidate_login: str) -> dict[str, Any]:
    result = candidate.put(
        f"/repos/{repo}/pulls/{pr}/merge",
        {
            "sha": sha,
            "merge_method": "merge",
            "commit_title": f"Merge PR #{pr}: {record_id}",
            "commit_message": (
                f"Autonomous bounded administrative completion.\n\n"
                f"exact head {sha}\n\n"
                "Disposition: REFEREE_AGENT_AUTHORIZED_EXACT_HEAD_PROTECTED_MERGE"
            ),
        },
    )
    if result.get("merged") is not True:
        raise AutonomyError(f"Candidate exact-head merge failed: {result.get('message')}")
    readback = candidate.get(f"/repos/{repo}/pulls/{pr}")
    if (
        readback.get("merged") is not True
        or readback.get("head", {}).get("sha") != sha
        or readback.get("merged_by", {}).get("login") != candidate_login
    ):
        raise AutonomyError("Candidate exact-head merge actor readback failed")
    return readback


def wait_record_readback(client: Client, repo: str, path: str, record: dict[str, Any], timeout: int, poll: int) -> None:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        actual = json_content(client, repo, path, "main")
        if actual is not None and canonical_digest(actual) == canonical_digest(record):
            return
        time.sleep(poll)
    raise AutonomyError("protected maintenance record readback timed out")


def wait_mirror_sync(
    observability: Client,
    evidence: Client,
    repo: str,
    merge_sha: str,
    procedure_id: str,
    due: str,
    runtime: dict[str, Any],
) -> int:
    timeout = int(runtime["merge_control"]["maximum_protected_readback_wait_seconds"])
    poll = int(runtime["merge_control"]["poll_interval_seconds"])
    deadline = time.monotonic() + timeout
    workflow = urllib.parse.quote("administrative-maintenance-synchronization.yml", safe="")
    run_id = 0
    while time.monotonic() < deadline:
        runs = observability.get(
            f"/repos/{repo}/actions/workflows/{workflow}/runs?head_sha={merge_sha}&per_page=20"
        ).get("workflow_runs", [])
        successful = [item for item in runs if item.get("status") == "completed" and item.get("conclusion") == "success"]
        if successful:
            run_id = int(successful[0]["id"])
            marker_head = f"- protected MATH-PROGRAMME head: `{merge_sha}`"
            marker_due = f"- `{procedure_id}` completed through: `{due}`"
            mirrors_current = True
            for mirror in runtime["mirrors"]:
                issue = evidence.get(f"/repos/{mirror['repository']}/issues/{mirror['issue']}")
                body = str(issue.get("body") or "")
                if marker_head not in body or marker_due not in body:
                    mirrors_current = False
                    break
            if mirrors_current:
                return run_id
        time.sleep(poll)
    raise AutonomyError("protected mirror synchronization readback timed out")


def list_directory_names(client: Client, repo: str, directory: str) -> list[str]:
    try:
        values = client.get(f"/repos/{repo}/contents/{directory}?ref=main")
    except AutonomyError as exc:
        if " 404 " in str(exc):
            return []
        raise
    return [str(item.get("name") or "") for item in values]


def eligible_candidates(candidate: Client, repo: str, runtime: dict[str, Any], now: datetime) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    pulls = candidate.get(f"/repos/{repo}/pulls?state=open&per_page=100")
    result: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for pull in pulls:
        branch = str(pull.get("head", {}).get("ref") or "")
        if not branch.startswith(runtime["scope"]["branch_prefix"]):
            continue
        if pull.get("user", {}).get("login") != runtime["candidate_identity"]["login"]:
            raise AutonomyError("maintenance branch is not authored by Candidate Agent")
        slug = branch.removeprefix(runtime["scope"]["branch_prefix"])
        manifest_path = f"{runtime['scope']['candidate_manifest_prefix']}{slug}.json"
        manifest = json_content(candidate, repo, manifest_path, branch)
        if not manifest:
            raise AutonomyError(f"candidate manifest missing: {manifest_path}")
        if manifest.get("state") != "CANDIDATE_PREPARED":
            raise AutonomyError("candidate state drift")
        if manifest.get("branch") != branch or manifest.get("manifest_path") != manifest_path:
            raise AutonomyError("candidate branch or manifest path drift")
        if int(manifest.get("pull_request_number") or 0) != int(pull["number"]):
            raise AutonomyError("candidate pull-request identity drift")
        if manifest.get("procedure_id") not in runtime["automated_procedures"]:
            continue
        if any(item is not False for item in manifest.get("claim_boundaries", {}).values()):
            raise AutonomyError("candidate claim inflation")
        if any(item is not False for item in manifest.get("authority_boundary", {}).values()):
            raise AutonomyError("candidate authority inflation")
        freeze = parse_datetime(manifest["freeze_at"])
        due = parse_datetime(manifest["scheduled_due_at"])
        recovery = timedelta(minutes=int(runtime["scope"]["recovery_window_minutes_after_due"]))
        if freeze <= now <= due + recovery:
            result.append((pull, manifest))
    return sorted(result, key=lambda item: parse_datetime(item[1]["scheduled_due_at"]))
