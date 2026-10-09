#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.parse
from pathlib import Path
from typing import Any

try:
    from ci.ns_ci_intake_pr_controller import (
        ControllerError,
        Github,
        find_open_pr,
        list_intake_branches,
        profile_for_dispatch,
        validate_candidate,
    )
except ModuleNotFoundError:
    from ns_ci_intake_pr_controller import (
        ControllerError,
        Github,
        find_open_pr,
        list_intake_branches,
        profile_for_dispatch,
        validate_candidate,
    )

OWNER = "grandchallenge"
REPO = "MATHSOLVE"
EXPECTED_AUTHOR = "gcl-release-trust[bot]"
EXPECTED_REVIEWER = "gcl-council-clerk[bot]"


def branch_head_sha(gh: Github, branch: str) -> str:
    encoded = urllib.parse.quote(branch, safe="/")
    ref = gh.request("GET", f"/repos/{OWNER}/{REPO}/git/ref/heads/{encoded}")
    sha = ref.get("object", {}).get("sha") if isinstance(ref, dict) else None
    if not isinstance(sha, str):
        raise ControllerError(f"{branch}: branch head SHA unavailable")
    return sha


def validate_pr_binding(
    gh: Github,
    item: dict[str, Any],
    pr: dict[str, Any],
) -> dict[str, Any]:
    dispatch_id = item["dispatch_id"]
    branch = item["branch"]
    profile = profile_for_dispatch(dispatch_id, gh)

    if pr.get("state") != "open":
        raise ControllerError(f"{dispatch_id}: evidence PR is not open")
    if pr.get("draft") is True:
        raise ControllerError(f"{dispatch_id}: evidence PR is draft")

    user = pr.get("user")
    author = user.get("login") if isinstance(user, dict) else None
    if author != EXPECTED_AUTHOR:
        raise ControllerError(
            f"{dispatch_id}: evidence PR author mismatch: {author!r}"
        )

    base = pr.get("base")
    head = pr.get("head")
    base_ref = base.get("ref") if isinstance(base, dict) else None
    head_ref = head.get("ref") if isinstance(head, dict) else None
    head_sha = head.get("sha") if isinstance(head, dict) else None

    if base_ref != "main":
        raise ControllerError(f"{dispatch_id}: evidence PR base is not main")
    if head_ref != branch:
        raise ControllerError(
            f"{dispatch_id}: evidence PR head branch mismatch: {head_ref!r}"
        )
    live_branch_sha = branch_head_sha(gh, branch)
    if head_sha != live_branch_sha:
        raise ControllerError(
            f"{dispatch_id}: evidence PR head moved relative to branch ref"
        )

    expected_title = f"{profile.pr_title_prefix}: {dispatch_id}"
    if pr.get("title") != expected_title:
        raise ControllerError(f"{dispatch_id}: evidence PR title mismatch")

    if pr.get("mergeable") is False:
        raise ControllerError(f"{dispatch_id}: evidence PR is not mergeable")

    return {
        "pr_number": pr.get("number"),
        "pr_node_id": pr.get("node_id"),
        "head_sha": head_sha,
        "base_ref": base_ref,
        "author": author,
    }



def exact_clerk_approval_exists(
    gh: Github,
    pr_number: int,
    head_sha: str,
) -> bool:
    reviews = gh.request(
        "GET",
        f"/repos/{OWNER}/{REPO}/pulls/{pr_number}/reviews?per_page=100",
    )
    if not isinstance(reviews, list):
        raise ControllerError("evidence PR review list response malformed")
    return any(
        isinstance(review, dict)
        and isinstance(review.get("user"), dict)
        and review["user"].get("login") == EXPECTED_REVIEWER
        and review.get("state") == "APPROVED"
        and review.get("commit_id") == head_sha
        for review in reviews
    )

def merge_protected(
    gh: Github,
    pr_number: int,
    expected_head_sha: str,
    dispatch_id: str,
) -> dict[str, Any]:
    if not isinstance(pr_number, int):
        raise ControllerError(f"{dispatch_id}: evidence PR number unavailable")
    result = gh.request(
        "PUT",
        f"/repos/{OWNER}/{REPO}/pulls/{pr_number}/merge",
        {
            "sha": expected_head_sha,
            "merge_method": "squash",
            "commit_title": f"Protect intake evidence: {dispatch_id} (#{pr_number})",
            "commit_message": (
                "Mechanical preservation of one validated RESULT/1 raw snapshot "
                "and receipt. No mathematical adjudication, certification, "
                "claim promotion, or campaign advancement."
            ),
        },
    )
    if not isinstance(result, dict) or result.get("merged") is not True:
        raise ControllerError(
            f"{dispatch_id}: protected merge did not complete: {result!r}"
        )
    return result


def run(apply: bool) -> dict[str, Any]:
    read_token = os.environ.get("MATHSOLVE_INTAKE_PR_TOKEN", "")
    merge_token = os.environ.get("MATHSOLVE_EVIDENCE_MERGE_TOKEN", "")
    if not read_token:
        raise ControllerError("MATHSOLVE_INTAKE_PR_TOKEN is empty")
    if not merge_token:
        raise ControllerError("MATHSOLVE_EVIDENCE_MERGE_TOKEN is empty")
    gh = Github(read_token)
    merge_gh = Github(merge_token)

    report: dict[str, Any] = {
        "schema_version": "1.0.0",
        "controller": "GCL_RELEASE_TRUST_EXTERNAL_INTAKE_EVIDENCE_ADMISSION",
        "target_repository": f"{OWNER}/{REPO}",
        "apply": apply,
        "authority": {
            "validation_token": {"contents": "read", "pull_requests": "write"},
            "merge_token": {"contents": "write", "pull_requests": "write"},
            "protected_merge": True,
            "admin_bypass": False,
            "campaign_mutation": False,
            "mathematical_adjudication": False,
        },
        "candidates": [],
        "protected_merges": [],
        "errors": [],
    }

    for branch in list_intake_branches(gh):
        pr = find_open_pr(gh, branch)
        if pr is None:
            continue
        try:
            item = validate_candidate(gh, branch)
            if item.get("state") != "OPEN_PR_EXISTS":
                raise ControllerError(
                    f"{item['dispatch_id']}: unexpected intake state "
                    f"{item.get('state')}"
                )
            live = gh.request(
                "GET", f"/repos/{OWNER}/{REPO}/pulls/{pr['number']}"
            )
            if not isinstance(live, dict):
                raise ControllerError(
                    f"{item['dispatch_id']}: evidence PR response malformed"
                )
            binding = validate_pr_binding(gh, item, live)
            approved = exact_clerk_approval_exists(
                gh,
                int(binding["pr_number"]),
                str(binding["head_sha"] or ""),
            )
            candidate = {
                "campaign": item["campaign"],
                "dispatch_id": item["dispatch_id"],
                "branch": branch,
                **binding,
                "clerk_exact_head_approval": approved,
                "state": (
                    "VALIDATED_FOR_PROTECTED_MERGE"
                    if approved
                    else "AWAITING_COUNCIL_CLERK_DOCUMENTARY_REVIEW"
                ),
            }
            report["candidates"].append(candidate)
            if not approved:
                continue
            if apply:
                merged = merge_protected(
                    merge_gh,
                    int(binding["pr_number"]),
                    str(binding["head_sha"] or ""),
                    item["dispatch_id"],
                )
                report["protected_merges"].append(
                    {
                        "dispatch_id": item["dispatch_id"],
                        "pr_number": binding["pr_number"],
                        "head_sha": binding["head_sha"],
                        "merge_commit_sha": merged.get("sha"),
                    }
                )
        except ControllerError as exc:
            report["errors"].append({"branch": branch, "error": str(exc)})

    report["authority_created"] = False
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    try:
        report = run(args.apply)
    except ControllerError as exc:
        report = {
            "schema_version": "1.0.0",
            "controller": "GCL_RELEASE_TRUST_EXTERNAL_INTAKE_EVIDENCE_ADMISSION",
            "apply": args.apply,
            "fatal_error": str(exc),
            "authority_created": False,
        }
        args.report.write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        print(str(exc), file=sys.stderr)
        return 2

    args.report.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
