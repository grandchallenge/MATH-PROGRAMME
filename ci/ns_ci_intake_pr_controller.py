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


class ControllerError(RuntimeError):
    pass


@dataclass(frozen=True)
class IntakeProfile:
    campaign: str
    branch_prefix: str
    dispatch_re: re.Pattern[str]
    base: str
    receipt_schema_version: str
    pr_title_prefix: str


PROFILES = (
    IntakeProfile(
        campaign="NS-CI-001",
        branch_prefix="intake/nsci-",
        dispatch_re=re.compile(r"^NSCI-C2-[A-E]-(?:BLIND|COOP|ADV)-[0-9]{3}$"),
        base="contributions/NS-CI-001/C2_MIX_DIRECTION_COMPRESSION_LEDGER_CHARGE",
        receipt_schema_version="0.2-pilot",
        pr_title_prefix="NS-CI intake",
    ),
    IntakeProfile(
        campaign="UC-001",
        branch_prefix="intake/uc-",
        dispatch_re=re.compile(r"^UC-WP08-D004-WP0[1-5]-IA-001$"),
        base="contributions/UC-001/WP08_D004_INCIDENCE_INTERFACE",
        receipt_schema_version="1.0.0",
        pr_title_prefix="UC-001 intake",
    ),
    IntakeProfile(
        campaign="ERDOS-OPEN-RECON",
        branch_prefix="intake/erdos-",
        dispatch_re=re.compile(
            r"^ERDOS-(?:593|595|241|470|1052|99|101|138)-(?:R1|S1|A1)-IA-001$"
        ),
        base="contributions/ERDOS-OPEN-001/RECON_TRANCHE_001",
        receipt_schema_version="1.0.0",
        pr_title_prefix="ERDOS-OPEN intake",
    ),
    IntakeProfile(
        campaign="GCL-E2E-CANARY-001",
        branch_prefix="intake/gcl-e2e-canary-",
        dispatch_re=re.compile(r"^GCL-E2E-CANARY-001-IA-001$"),
        base="contributions/GCL-E2E-CANARY-001",
        receipt_schema_version="1.0.0",
        pr_title_prefix="GCL E2E canary intake",
    ),
    IntakeProfile(
        campaign="GCL-E2E-CANARY-002",
        branch_prefix="intake/gcl-e2e-canary-",
        dispatch_re=re.compile(r"^GCL-E2E-CANARY-002-IA-001$"),
        base="contributions/GCL-E2E-CANARY-002",
        receipt_schema_version="1.0.0",
        pr_title_prefix="GCL E2E canary intake",
    ),
    IntakeProfile(
        campaign="GCL-E2E-CANARY-003",
        branch_prefix="intake/gcl-e2e-canary-",
        dispatch_re=re.compile(r"^GCL-E2E-CANARY-003-IA-001$"),
        base="contributions/GCL-E2E-CANARY-003",
        receipt_schema_version="1.0.0",
        pr_title_prefix="GCL E2E canary intake",
    ),
)


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
            "User-Agent": "gcl-external-intake-pr-controller",
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


def profile_for_branch(branch_name: str) -> tuple[IntakeProfile, str]:
    for profile in PROFILES:
        if branch_name.startswith(profile.branch_prefix):
            slug = branch_name[len("intake/"):].upper()
            if profile.dispatch_re.fullmatch(slug):
                return profile, slug
    raise ControllerError("branch does not map to a registered external-intake dispatch")


def profile_for_dispatch(dispatch_id: str) -> IntakeProfile:
    for profile in PROFILES:
        if profile.dispatch_re.fullmatch(dispatch_id):
            return profile
    raise ControllerError(f"dispatch is not registered with the external intake controller: {dispatch_id}")


def derive_dispatch_id(branch_name: str) -> str:
    return profile_for_branch(branch_name)[1]


def expected_paths(dispatch_id: str, comment_id: int) -> tuple[str, str]:
    profile = profile_for_dispatch(dispatch_id)
    raw = f"{profile.base}/raw/{dispatch_id}/github-comment-{comment_id}.md"
    receipt = f"{profile.base}/receipts/{dispatch_id}/github-comment-{comment_id}.json"
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
    # Find un-PR'd evidence branches using the repository branches API.
    # An open-PR-only discovery loop cannot create the first PR for a branch.
    # Branch listing requires only the same bounded contents:read token.
    # Retain open-PR discovery for backward compatibility and deduplicate.
    names: set[str] = set()
    for source in ("branches", "pulls"):
        page = 1
        while True:
            if source == "branches":
                path = f"/repos/{OWNER}/{REPO}/branches?per_page=100&page={page}"
            else:
                path = (
                    f"/repos/{OWNER}/{REPO}/pulls?"
                    f"state=open&base=main&per_page=100&page={page}"
                )
            items = gh.request("GET", path)
            if not isinstance(items, list):
                raise ControllerError(f"{source} discovery response is not a list")
            for item in items:
                if not isinstance(item, dict):
                    continue
                if source == "branches":
                    ref = item.get("name")
                else:
                    head = item.get("head")
                    ref = head.get("ref") if isinstance(head, dict) else None
                if not isinstance(ref, str):
                    continue
                try:
                    profile_for_branch(ref)
                except ControllerError:
                    continue
                names.add(ref)
            if len(items) < 100:
                break
            page += 1
    return sorted(names)


def main_has_any_raw(gh: Github, dispatch_id: str) -> bool:
    profile = profile_for_dispatch(dispatch_id)
    raw_dir = f"{profile.base}/raw/{dispatch_id}"
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
    profile, dispatch_id = profile_for_branch(branch)
    dispatch_dir = f"{profile.base}/dispatches"
    dispatch_text, dispatch_blob = fetch_text(
        gh, f"{dispatch_dir}/{dispatch_id}.json", "main"
    )
    try:
        dispatch = json.loads(dispatch_text)
    except json.JSONDecodeError as exc:
        raise ControllerError(f"{dispatch_id}: protected dispatch JSON invalid") from exc

    if dispatch.get("dispatch_id") != dispatch_id:
        raise ControllerError(f"{dispatch_id}: protected dispatch identity mismatch")
    if dispatch.get("campaign") != profile.campaign:
        raise ControllerError(f"{dispatch_id}: protected campaign identity mismatch")
    if dispatch.get("dispatch_status") != "READY_FOR_GITHUB_COMMENT":
        raise ControllerError(f"{dispatch_id}: dispatch is not ready for intake")
    if dispatch.get("return_protocol") != "GCL-CONTRIBUTION-RESULT/1":
        raise ControllerError(f"{dispatch_id}: return protocol mismatch")
    if dispatch.get("canonical_mutation_authorized") is not False:
        raise ControllerError(f"{dispatch_id}: canonical mutation unexpectedly authorized")

    changed = compare_files(gh, branch)
    receipt_dir = f"{profile.base}/receipts"
    receipt_prefix = f"{receipt_dir}/{dispatch_id}/github-comment-"
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
        "schema_version": receipt.get("schema_version") == profile.receipt_schema_version,
        "dispatch_id": receipt.get("dispatch_id") == dispatch_id,
        "assignment_id": receipt.get("assignment_id") == dispatch.get("assignment_id"),
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

    if main_has_any_raw(gh, dispatch_id):
        state = "ALREADY_PROTECTED"
    else:
        existing = find_open_pr(gh, branch)
        state = "OPEN_PR_EXISTS" if existing else "PR_REQUIRED"

    return {
        "campaign": profile.campaign,
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
    profile = profile_for_dispatch(dispatch_id)
    title = f"{profile.pr_title_prefix}: {dispatch_id}"
    body = (
        f"Trusted intake snapshot for {profile.campaign} dispatch {dispatch_id}, GitHub comment {comment_id}. "
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


def run(apply: bool) -> dict[str, Any]:
    token = os.environ.get("MATHSOLVE_INTAKE_PR_TOKEN", "")
    if not token:
        raise ControllerError("MATHSOLVE_INTAKE_PR_TOKEN is empty")
    gh = Github(token)

    report: dict[str, Any] = {
        "schema_version": "1.1.0",
        "controller": "GCL_RELEASE_TRUST_BOUNDED_EXTERNAL_INTAKE_PR_CONTROLLER",
        "target_repository": f"{OWNER}/{REPO}",
        "registered_campaigns": [p.campaign for p in PROFILES],
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
                "campaign": item["campaign"],
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
            "schema_version": "1.1.0",
            "controller": "GCL_RELEASE_TRUST_BOUNDED_EXTERNAL_INTAKE_PR_CONTROLLER",
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
