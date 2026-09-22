#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any

OWNER = "grandchallenge"
REPO = "MATHSOLVE"
API = "https://api.github.com"
BRANCH_PREFIX = "intake/nsci-"
DISPATCH_RE = re.compile(r"^NSCI-C2-[A-E]-(?:BLIND|COOP|ADV)-[0-9]{3}$")
BASE = "contributions/NS-CI-001/C2_MIX_DIRECTION_COMPRESSION_LEDGER_CHARGE"
DISPATCH_DIR = f"{BASE}/dispatches"
RAW_DIR = f"{BASE}/raw"
RECEIPT_DIR = f"{BASE}/receipts"

class ControllerError(RuntimeError):
    pass

@dataclass
class Github:
    token: str

    def request(self, method: str, path: str, payload: dict[str, Any] | None = None) -> Any:
        url = API + path
        data = None
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {self.token}",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "gcl-ns-ci-intake-pr-controller",
        }
        if payload is not None:
            data = json.dumps(payload).encode("utf-8")
            headers["Content-Type"] = "application/json"
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                raw = response.read()
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", "replace")
            raise ControllerError(f"{method} {path} failed: HTTP {exc.code}: {body}") from exc
        except urllib.error.URLError as exc:
            raise ControllerError(f"{method} {path} failed: {exc}") from exc
        if not raw:
            return None
        return json.loads(raw.decode("utf-8"))

    def get_optional(self, path: str) -> Any | None:
        try:
            return self.request("GET", path)
        except ControllerError as exc:
            if "HTTP 404" in str(exc):
                return None
            raise


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def content_text(item: dict[str, Any]) -> str:
    encoded = item.get("content")
    encoding = item.get("encoding")
    if encoding != "base64" or not isinstance(encoded, str):
        raise ControllerError("GitHub contents response is not base64 text")
    return base64.b64decode(encoded).decode("utf-8")


def derive_dispatch_id(branch_name: str) -> str:
    if not branch_name.startswith(BRANCH_PREFIX):
        raise ControllerError("branch does not use NS-CI intake prefix")
    slug = branch_name[len("intake/"):].upper()
    if not DISPATCH_RE.fullmatch(slug):
        raise ControllerError(f"branch does not map to registered dispatch syntax: {branch_name}")
    return slug


def expected_paths(dispatch_id: str, comment_id: int) -> tuple[str, str]:
    raw = f"{RAW_DIR}/{dispatch_id}/github-comment-{comment_id}.md"
    receipt = f"{RECEIPT_DIR}/{dispatch_id}/github-comment-{comment_id}.json"
    return raw, receipt


def fetch_text(gh: Github, path: str, ref: str) -> tuple[str, str]:
    encoded_path = urllib.parse.quote(path, safe="/")
    encoded_ref = urllib.parse.quote(ref, safe="")
    item = gh.request("GET", f"/repos/{OWNER}/{REPO}/contents/{encoded_path}?ref={encoded_ref}")
    if not isinstance(item, dict):
        raise ControllerError(f"unexpected contents response for {path}")
    sha = item.get("sha")
    if not isinstance(sha, str):
        raise ControllerError(f"missing blob sha for {path}")
    return content_text(item), sha


def list_intake_branches(gh: Github) -> list[str]:
    prefix = urllib.parse.quote(f"heads/{BRANCH_PREFIX}", safe="/")
    refs = gh.get_optional(f"/repos/{OWNER}/{REPO}/git/matching-refs/{prefix}")
    if refs is None:
        return []
    if not isinstance(refs, list):
        raise ControllerError("matching-refs response is not a list")
    names = []
    for item in refs:
        ref = item.get("ref") if isinstance(item, dict) else None
        if isinstance(ref, str) and ref.startswith("refs/heads/"):
            names.append(ref[len("refs/heads/"):])
    return sorted(set(names))


def main_has_raw(gh: Github, raw_path: str) -> bool:
    encoded_path = urllib.parse.quote(raw_path, safe="/")
    return gh.get_optional(f"/repos/{OWNER}/{REPO}/contents/{encoded_path}?ref=main") is not None


def find_open_pr(gh: Github, branch: str) -> dict[str, Any] | None:
    head = urllib.parse.quote(f"{OWNER}:{branch}", safe="")
    pulls = gh.request("GET", f"/repos/{OWNER}/{REPO}/pulls?state=open&head={head}&per_page=10")
    if not isinstance(pulls, list):
        raise ControllerError("pull list response is not a list")
    return pulls[0] if pulls else None


def compare_files(gh: Github, branch: str) -> list[str]:
    encoded = urllib.parse.quote(f"main...{branch}", safe=".")
    comparison = gh.request("GET", f"/repos/{OWNER}/{REPO}/compare/{encoded}")
    files = comparison.get("files") if isinstance(comparison, dict) else None
    if not isinstance(files, list):
        raise ControllerError("compare response lacks files")
    result = []
    for item in files:
        filename = item.get("filename") if isinstance(item, dict) else None
        if isinstance(filename, str):
            result.append(filename)
    return sorted(result)


def validate_candidate(gh: Github, branch: str) -> dict[str, Any]:
    dispatch_id = derive_dispatch_id(branch)

    dispatch_text, dispatch_blob = fetch_text(
        gh, f"{DISPATCH_DIR}/{dispatch_id}.json", "main"
    )
    try:
        dispatch = json.loads(dispatch_text)
    except json.JSONDecodeError as exc:
        raise ControllerError(f"{dispatch_id}: protected dispatch JSON invalid") from exc

    if dispatch.get("dispatch_id") != dispatch_id:
        raise ControllerError(f"{dispatch_id}: protected dispatch identity mismatch")
    if dispatch.get("dispatch_status") != "READY_FOR_GITHUB_COMMENT":
        raise ControllerError(f"{dispatch_id}: dispatch is not ready for intake")
    if dispatch.get("return_protocol") != "GCL-CONTRIBUTION-RESULT/1":
        raise ControllerError(f"{dispatch_id}: return protocol mismatch")
    if dispatch.get("canonical_mutation_authorized") is not False:
        raise ControllerError(f"{dispatch_id}: canonical mutation unexpectedly authorized")

    changed = compare_files(gh, branch)
    receipt_prefix = f"{RECEIPT_DIR}/{dispatch_id}/github-comment-"
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

    expected_issue = dispatch.get("github_issue_number")
    checks = {
        "schema_version": receipt.get("schema_version") == "0.2-pilot",
        "dispatch_id": receipt.get("dispatch_id") == dispatch_id,
        "result_protocol": receipt.get("result_protocol") == "GCL-CONTRIBUTION-RESULT/1",
        "github_issue_number": receipt.get("github_issue_number") == expected_issue,
        "github_comment_id": receipt.get("github_comment_id") == comment_id,
        "raw_artifact_path": receipt.get("raw_artifact_path") == raw_path,
        "raw_sha256": receipt.get("raw_sha256") == sha256_text(raw_text),
        "bootstrap_sha256": receipt.get("bootstrap_sha256") == dispatch.get("bootstrap_sha256"),
        "source_handoff_commit_sha": receipt.get("source_handoff_commit_sha") == dispatch.get("source_handoff_commit_sha"),
        "source_handoff_blob_sha": receipt.get("source_handoff_blob_sha") == dispatch.get("source_handoff_blob_sha"),
        "source_handoff_sha256": receipt.get("source_handoff_sha256") == dispatch.get("source_handoff_sha256"),
        "schema_result": receipt.get("schema_result") == "valid",
        "freshness": receipt.get("freshness") == "current_for_dispatch",
        "handling_state": receipt.get("handling_state") == "received_unadjudicated",
        "mathematical_correctness_adjudicated": receipt.get("mathematical_correctness_adjudicated") is False,
        "independence_strength_adjudicated": receipt.get("independence_strength_adjudicated") is False,
        "canonical_claim_effect": receipt.get("canonical_claim_effect") is False,
    }
    failed = sorted(name for name, ok in checks.items() if not ok)
    if failed:
        raise ControllerError(f"{dispatch_id}: receipt validation failed: {', '.join(failed)}")

    if main_has_raw(gh, raw_path):
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
        "github_issue_number": expected_issue,
        "github_comment_id": comment_id,
        "state": state,
    }


def open_pr(gh: Github, item: dict[str, Any]) -> dict[str, Any]:
    dispatch_id = item["dispatch_id"]
    comment_id = item["github_comment_id"]
    title = f"NS-CI intake: {dispatch_id}"
    body = (
        f"Trusted intake snapshot for dispatch {dispatch_id}, GitHub comment {comment_id}. "
        "This PR preserves raw contributor evidence and a machine receipt only. "
        "It does not adjudicate mathematics, infer independence, certify a claim, "
        "or alter campaign state."
    )
    pr = gh.request(
        "POST",
        f"/repos/{OWNER}/{REPO}/pulls",
        {"title": title, "head": item["branch"], "base": "main", "body": body},
    )
    if not isinstance(pr, dict) or not isinstance(pr.get("number"), int):
        raise ControllerError(f"{dispatch_id}: pull request creation returned malformed response")
    return pr


def comment_issue(gh: Github, issue_number: int, body: str) -> None:
    gh.request(
        "POST",
        f"/repos/{OWNER}/{REPO}/issues/{issue_number}/comments",
        {"body": body},
    )


def run(apply: bool) -> dict[str, Any]:
    token = os.environ.get("MATHSOLVE_INTAKE_PR_TOKEN", "")
    if not token:
        raise ControllerError("MATHSOLVE_INTAKE_PR_TOKEN is empty")
    gh = Github(token)

    report: dict[str, Any] = {
        "schema_version": "1.0.0",
        "controller": "GCL_RELEASE_TRUST_BOUNDED_NS_CI_INTAKE_PR_CONTROLLER",
        "target_repository": f"{OWNER}/{REPO}",
        "apply": apply,
        "authority": {
            "contents": "read",
            "pull_requests": "write",
            "issues": "write",
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
            url = pr.get("html_url")
            number = pr["number"]
            report["opened_prs"].append({
                "dispatch_id": item["dispatch_id"],
                "branch": branch,
                "pr_number": number,
                "pr_url": url,
            })
            if isinstance(item.get("github_issue_number"), int):
                comment_issue(
                    gh,
                    item["github_issue_number"],
                    f"INTAKE CONTROLLER — raw-evidence PR created by bounded Release Trust controller: #{number}. "
                    "Mathematical status remains unadjudicated.",
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
            "controller": "GCL_RELEASE_TRUST_BOUNDED_NS_CI_INTAKE_PR_CONTROLLER",
            "apply": args.apply,
            "fatal_error": str(exc),
            "authority_created": False,
        }
        args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(str(exc), file=sys.stderr)
        return 2

    args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
