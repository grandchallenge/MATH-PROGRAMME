#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import urllib.parse
from pathlib import Path
from typing import Any

try:
    from ci.ns_ci_intake_pr_controller import (
        ControllerError,
        Github,
        OWNER,
        REPO,
        compare_files,
        fetch_text,
        find_open_pr,
        sha256_text,
    )
except ModuleNotFoundError:
    from ns_ci_intake_pr_controller import (
        ControllerError,
        Github,
        OWNER,
        REPO,
        compare_files,
        fetch_text,
        find_open_pr,
        sha256_text,
    )

BRANCH_PREFIX = "intake/openmath-"
DISPATCH_RE = re.compile(r"^OM26-H([2-7])-WP([0-9]{2})-IA-([0-9]{3})$")


def derive_dispatch_id(branch_name: str) -> str:
    if not branch_name.startswith(BRANCH_PREFIX):
        raise ControllerError("branch does not use OPENMATH intake prefix")
    dispatch_id = branch_name[len(BRANCH_PREFIX):].upper()
    if not DISPATCH_RE.fullmatch(dispatch_id):
        raise ControllerError(f"branch does not map to OPENMATH dispatch syntax: {branch_name}")
    return dispatch_id


def dispatch_base(dispatch_id: str) -> str:
    match = DISPATCH_RE.fullmatch(dispatch_id)
    if not match:
        raise ControllerError(f"invalid OPENMATH dispatch id: {dispatch_id}")
    hill, wp, _agent = match.groups()
    return f"contributions/OPENMATH-2026/OM26-H{hill}/WP{wp}"


def expected_paths(dispatch_id: str, comment_id: int) -> tuple[str, str]:
    base = dispatch_base(dispatch_id)
    raw = f"{base}/raw/{dispatch_id}/github-comment-{comment_id}.md"
    receipt = f"{base}/receipts/{dispatch_id}/github-comment-{comment_id}.json"
    return raw, receipt


def dispatch_path(dispatch_id: str) -> str:
    return f"{dispatch_base(dispatch_id)}/dispatches/{dispatch_id}.json"


def list_intake_branches(gh: Github) -> list[str]:
    prefix = urllib.parse.quote(f"heads/{BRANCH_PREFIX}", safe="/")
    refs = gh.get_optional(f"/repos/{OWNER}/{REPO}/git/matching-refs/{prefix}")
    if refs is None:
        return []
    if not isinstance(refs, list):
        raise ControllerError("matching-refs response is not a list")
    names: list[str] = []
    for item in refs:
        ref = item.get("ref") if isinstance(item, dict) else None
        if isinstance(ref, str) and ref.startswith("refs/heads/"):
            names.append(ref[len("refs/heads/"):])
    return sorted(set(names))


def main_has_any_raw(gh: Github, dispatch_id: str) -> bool:
    raw_dir = f"{dispatch_base(dispatch_id)}/raw/{dispatch_id}"
    encoded_dir = urllib.parse.quote(raw_dir, safe="/")
    items = gh.get_optional(f"/repos/{OWNER}/{REPO}/contents/{encoded_dir}?ref=main")
    if items is None:
        return False
    if not isinstance(items, list):
        raise ControllerError(f"{dispatch_id}: protected raw directory response is not a list")
    pattern = re.compile(r"^github-comment-[0-9]+\.md$")
    return any(
        isinstance(item, dict)
        and isinstance(item.get("name"), str)
        and pattern.fullmatch(item["name"])
        for item in items
    )


def validate_candidate(gh: Github, branch: str) -> dict[str, Any]:
    dispatch_id = derive_dispatch_id(branch)
    dpath = dispatch_path(dispatch_id)
    dispatch_text, dispatch_blob = fetch_text(gh, dpath, "main")
    try:
        dispatch = json.loads(dispatch_text)
    except json.JSONDecodeError as exc:
        raise ControllerError(f"{dispatch_id}: protected dispatch JSON invalid") from exc

    checks = {
        "dispatch_id": dispatch.get("dispatch_id") == dispatch_id,
        "campaign": dispatch.get("campaign") == "OPENMATH-2026",
        "dispatch_status": dispatch.get("dispatch_status") == "READY_FOR_GITHUB_COMMENT",
        "return_protocol": dispatch.get("return_protocol") == "GCL-CONTRIBUTION-RESULT/1",
        "canonical_mutation_authorized": dispatch.get("canonical_mutation_authorized") is False,
    }
    failed = sorted(name for name, ok in checks.items() if not ok)
    if failed:
        raise ControllerError(f"{dispatch_id}: protected dispatch validation failed: {', '.join(failed)}")

    changed = compare_files(gh, branch)
    receipt_prefix = f"{dispatch_base(dispatch_id)}/receipts/{dispatch_id}/github-comment-"
    receipts = [p for p in changed if p.startswith(receipt_prefix) and p.endswith(".json")]
    if len(receipts) != 1:
        raise ControllerError(f"{dispatch_id}: branch must contain exactly one changed receipt")
    receipt_path = receipts[0]
    match = re.search(r"github-comment-([0-9]+)\.json$", receipt_path)
    if not match:
        raise ControllerError(f"{dispatch_id}: receipt comment identity malformed")
    comment_id = int(match.group(1))
    raw_path, expected_receipt = expected_paths(dispatch_id, comment_id)
    if receipt_path != expected_receipt:
        raise ControllerError(f"{dispatch_id}: receipt path mismatch")
    if changed != sorted([raw_path, receipt_path]):
        raise ControllerError(
            f"{dispatch_id}: evidence branch changed-file set is not exactly raw+receipt: {changed}"
        )

    raw_text, raw_blob = fetch_text(gh, raw_path, branch)
    receipt_text, receipt_blob = fetch_text(gh, receipt_path, branch)
    try:
        receipt = json.loads(receipt_text)
    except json.JSONDecodeError as exc:
        raise ControllerError(f"{dispatch_id}: receipt JSON invalid") from exc

    receipt_checks = {
        "schema_version": receipt.get("schema_version") == "1.0.0",
        "dispatch_id": receipt.get("dispatch_id") == dispatch_id,
        "assignment_id": receipt.get("assignment_id") == dispatch.get("assignment_id"),
        "agent_ref": receipt.get("agent_ref") == dispatch.get("agent_ref"),
        "result_protocol": receipt.get("result_protocol") == "GCL-CONTRIBUTION-RESULT/1",
        "github_issue_number": receipt.get("github_issue_number") == dispatch.get("github_issue_number"),
        "github_comment_id": receipt.get("github_comment_id") == comment_id,
        "raw_artifact_path": receipt.get("raw_artifact_path") == raw_path,
        "bootstrap_path": receipt.get("bootstrap_path") == dispatch.get("bootstrap_path"),
        "bootstrap_blob_sha1": receipt.get("bootstrap_blob_sha1") == dispatch.get("bootstrap_blob_sha1"),
        "source_handoff_commit_sha": receipt.get("source_handoff_commit_sha") == dispatch.get("source_handoff_commit_sha"),
        "operation_contract": receipt.get("operation_contract") == dispatch.get("operation_contract"),
        "schema_result": receipt.get("schema_result") == "valid",
        "freshness": receipt.get("freshness") == "current_for_dispatch",
        "handling_state": receipt.get("handling_state") == "received_unadjudicated",
        "mathematical_correctness_adjudicated": receipt.get("mathematical_correctness_adjudicated") is False,
        "independence_strength_adjudicated": receipt.get("independence_strength_adjudicated") is False,
        "canonical_claim_effect": receipt.get("canonical_claim_effect") is False,
    }
    failed = sorted(name for name, ok in receipt_checks.items() if not ok)
    if failed:
        raise ControllerError(f"{dispatch_id}: receipt validation failed: {', '.join(failed)}")

    if main_has_any_raw(gh, dispatch_id):
        state = "ALREADY_PROTECTED"
    else:
        existing = find_open_pr(gh, branch)
        state = "OPEN_PR_EXISTS" if existing else "PR_REQUIRED"

    return {
        "dispatch_id": dispatch_id,
        "branch": branch,
        "dispatch_blob_sha": dispatch_blob,
        "raw_path": raw_path,
        "raw_blob_sha": raw_blob,
        "raw_sha256": sha256_text(raw_text),
        "receipt_path": receipt_path,
        "receipt_blob_sha": receipt_blob,
        "github_issue_number": dispatch.get("github_issue_number"),
        "github_comment_id": comment_id,
        "state": state,
    }


def open_pr(gh: Github, item: dict[str, Any]) -> dict[str, Any]:
    dispatch_id = item["dispatch_id"]
    comment_id = item["github_comment_id"]
    body = (
        f"Trusted OPENMATH intake snapshot for dispatch {dispatch_id}, GitHub comment {comment_id}. "
        "This PR preserves raw contributor evidence and a machine receipt only. "
        "It does not adjudicate mathematics, infer independence, certify a claim, "
        "authorize competition submission, or alter campaign state."
    )
    pr = gh.request(
        "POST",
        f"/repos/{OWNER}/{REPO}/pulls",
        {
            "title": f"OPENMATH intake: {dispatch_id}",
            "head": item["branch"],
            "base": "main",
            "body": body,
        },
    )
    if not isinstance(pr, dict) or not isinstance(pr.get("number"), int):
        raise ControllerError(f"{dispatch_id}: pull request creation returned malformed response")
    return pr


def run(apply: bool) -> dict[str, Any]:
    token = os.environ.get("MATHSOLVE_INTAKE_PR_TOKEN", "")
    if not token:
        raise ControllerError("MATHSOLVE_INTAKE_PR_TOKEN is empty")
    gh = Github(token)
    report: dict[str, Any] = {
        "schema_version": "1.0.0",
        "controller": "GCL_RELEASE_TRUST_BOUNDED_OPENMATH_INTAKE_PR_CONTROLLER",
        "target_repository": f"{OWNER}/{REPO}",
        "apply": apply,
        "authority": {
            "contents": "read",
            "pull_requests": "write",
            "merge": False,
            "review": False,
            "campaign_mutation": False,
            "mathematical_adjudication": False,
        },
        "branches": [],
        "opened_prs": [],
        "errors": [],
    }
    for branch in list_intake_branches(gh):
        try:
            item = validate_candidate(gh, branch)
            report["branches"].append(item)
            if item["state"] != "PR_REQUIRED" or not apply:
                continue
            pr = open_pr(gh, item)
            report["opened_prs"].append({
                "dispatch_id": item["dispatch_id"],
                "branch": branch,
                "pr_number": pr["number"],
                "pr_url": pr.get("html_url"),
            })
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
            "controller": "GCL_RELEASE_TRUST_BOUNDED_OPENMATH_INTAKE_PR_CONTROLLER",
            "apply": args.apply,
            "fatal_error": str(exc),
            "authority_created": False,
        }
        args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(str(exc), file=os.sys.stderr)
        return 2
    args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
