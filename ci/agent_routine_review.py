#!/usr/bin/env python3
"""Protected, deliberately narrow machine reviewer for a reversible MkDocs image removal.

This is a routine delegated mechanical disposition, NOT independent mathematical review.
Unknown changes fail closed. GitHub's review rule and native merge queue remain active.
"""
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from typing import Any

REPOSITORY = "grandchallenge/MATH-PROGRAMME"
APP_REVIEWER = "gcl-release-trust[bot]"
REMOVE_EXACTLY = (
    "## The GCL continuity fabric\n"
    "\n"
    "![GCL Agent Continuity fabric showing the relationship between the canonical governance layer, specialised repositories, and protected admission.](assets/gcl-agent-continuity-fabric.png)\n"
    "\n"
    "This public orientation diagram shows how the canonical policy and bounded-operation layers relate to the specialised MATHFORGE, MATHSOLVE, and MATHCERT repositories. The artwork is explanatory, not operative: repository-local policy, protected records, validators, and exact-head evidence remain authoritative. It does not grant authority, certify mathematics, or imply authority inheritance across repositories.\n"
    "\n"
)
REQUIRED_HEAD_CONTEXTS = frozenset({
    "validate-json", "formal-validation / formal-validation",
    "policy / policy", "security / action-policy", "routing-enforcement",
})


class RoutineReviewError(RuntimeError):
    pass


def api(method: str, path: str, *, token: str, payload: dict | None = None) -> Any:
    if not token:
        raise RoutineReviewError("missing authorized token")
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        "https://api.github.com" + path,
        data=data,
        method=method,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": "Bearer " + token,
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "gcl-routine-review-001",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=25) as response:
            return json.load(response)
    except urllib.error.HTTPError as exc:
        raise RoutineReviewError(
            f"GitHub {method} {path.split('?')[0]} returned HTTP {exc.code}"
        ) from exc


def removed_patch_text(patch: str) -> str:
    """Recover just deleted lines from a GitHub unified patch, excluding file headers."""
    lines = patch.splitlines(keepends=True)
    return "".join(line[1:] for line in lines if line.startswith("-") and not line.startswith("---"))


def eligible_image_removal(pr: dict, files: list[dict], pinned_head: str) -> None:
    if pr.get("state") != "open" or pr.get("draft"):
        raise RoutineReviewError("PR not open and ready")
    head = pr.get("head") or {}
    if head.get("sha") != pinned_head or not (len(pinned_head) == 40):
        raise RoutineReviewError("PR head changed from exact candidate")
    if (head.get("repo") or {}).get("full_name") != REPOSITORY:
        raise RoutineReviewError("candidate outside authorized repository")
    if (pr.get("base") or {}).get("ref") != "main":
        raise RoutineReviewError("PR does not target protected main")
    if (pr.get("user") or {}).get("login") == APP_REVIEWER:
        raise RoutineReviewError("reviewer App cannot approve its own change")
    if pr.get("changed_files") != 1 or len(files) != 1:
        raise RoutineReviewError("exactly one tracked documentation file required")
    f = files[0]
    if (f.get("filename"), f.get("status"), f.get("additions"), f.get("deletions")) != (
        "docs/index.md", "modified", 0, 6
    ):
        raise RoutineReviewError("file scope, addition, or deletion count drift")
    patch = f.get("patch") or ""
    if any(line.startswith("+") and not line.startswith("+++") for line in patch.splitlines()):
        raise RoutineReviewError("unexpected added line")
    if removed_patch_text(patch) != REMOVE_EXACTLY:
        raise RoutineReviewError("deletion content not precisely the admitted image section")


def required_contexts_green(check_runs: list[dict], statuses: list[dict]) -> None:
    succeeded: set[str] = set()
    failed: set[str] = set()
    for run in check_runs:
        name = str(run.get("name") or "")
        if name in REQUIRED_HEAD_CONTEXTS:
            if run.get("status") == "completed" and run.get("conclusion") == "success":
                succeeded.add(name)
            else:
                failed.add(name)
    for status in statuses:
        name = str(status.get("context") or "")
        if name in REQUIRED_HEAD_CONTEXTS:
            if status.get("state") == "success":
                succeeded.add(name)
            else:
                failed.add(name)
    missing = REQUIRED_HEAD_CONTEXTS - succeeded
    if failed or missing:
        raise RoutineReviewError(
            "required exact-head admission evidence incomplete: "
            + repr({"failed_or_pending": sorted(failed), "missing": sorted(missing)})
        )


def candidate_number(event: dict, event_name: str) -> tuple[int, str] | None:
    if event_name == "workflow_dispatch":
        value = (event.get("inputs") or {}).get("pr_number")
        if value is None or not str(value).isdigit():
            return None
        return int(value), ""
    if event_name == "workflow_run":
        run = event.get("workflow_run") or {}
        if run.get("event") != "pull_request" or run.get("conclusion") != "success":
            return None
        if (run.get("repository") or {}).get("full_name") != REPOSITORY:
            return None
        prs = run.get("pull_requests") or []
        if len(prs) != 1:
            return None
        return int(prs[0]["number"]), str(run.get("head_sha") or "")
    return None


def main() -> int:
    with open(os.environ["GITHUB_EVENT_PATH"], encoding="utf-8") as file:
        event = json.load(file)
    resolved = candidate_number(event, os.environ.get("GITHUB_EVENT_NAME", ""))
    if resolved is None:
        print("No single eligible pull request bound to trusted workflow event; no action")
        return 0
    number, event_sha = resolved
    read_token = os.environ.get("GITHUB_TOKEN", "")
    review_token = os.environ.get("REVIEW_APP_TOKEN", "")
    prefix = f"/repos/{REPOSITORY}"
    pr = api("GET", f"{prefix}/pulls/{number}", token=read_token)
    head = str((pr.get("head") or {}).get("sha") or "")
    if event_sha and head != event_sha:
        raise RoutineReviewError("event SHA not current PR head")
    files = api("GET", f"{prefix}/pulls/{number}/files?per_page=100", token=read_token)
    eligible_image_removal(pr, files, head)
    checks = api("GET", f"{prefix}/commits/{head}/check-runs?per_page=100", token=read_token)
    statuses = api("GET", f"{prefix}/commits/{head}/status", token=read_token)
    if checks.get("total_count", 0) > 100:
        raise RoutineReviewError("check run pagination unknown")
    required_contexts_green(checks.get("check_runs", []), statuses.get("statuses", []))
    reviews = api("GET", f"{prefix}/pulls/{number}/reviews?per_page=100", token=read_token)
    if any(
        (r.get("user") or {}).get("login") == APP_REVIEWER
        and r.get("state") == "APPROVED" and r.get("commit_id") == head
        for r in reviews
    ):
        print("Already reviewed at exact head; idempotent no-op")
        return 0
    fresh = api("GET", f"{prefix}/pulls/{number}", token=read_token)
    if (fresh.get("head") or {}).get("sha") != head or fresh.get("state") != "open":
        raise RoutineReviewError("PR mutated during admission preflight")
    response = api("POST", f"{prefix}/pulls/{number}/reviews", token=review_token, payload={
        "event": "APPROVE",
        "commit_id": head,
        "body": (
            "GCL-AGENT-STAFFING-001 / ROUTINE_BOUNDED / mechanical admission only. "
            "Verified exact docs/index.md image-section deletion, zero additions, "
            "same-repo candidate, non-author App identity and required exact-head "
            "checks including GH-OS pre-queue routing. No theorem, certification, "
            "claim, constitutional, or security disposition. Final admission "
            "remains exclusively GitHub native merge queue. "
            f"Head: {head}."
        ),
    })
    if response.get("state") != "APPROVED":
        raise RoutineReviewError("GitHub did not record an approved App review")
    print(f"Agent-driven bounded routine review recorded on PR #{number} at {head}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (RoutineReviewError, OSError, KeyError, ValueError) as error:
        print("Fail closed: " + str(error), file=sys.stderr)
        sys.exit(1)
