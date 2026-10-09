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
    queue_binding: dict[str, Any] | None = None


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


QUEUE_BINDINGS_PATH = ".gcl/worker_queue/INTAKE_BINDINGS.json"


def protected_queue_bindings(gh: Github) -> list[dict[str, Any]]:
    """Fetch only protected-main queue producer contracts, never branch data."""
    path = f"/repos/{OWNER}/{REPO}/contents/{QUEUE_BINDINGS_PATH}?ref=main"
    item = gh.get_optional(path)
    if item is None:
        return []  # New intake contract is not yet admitted on protected main.
    if not isinstance(item, dict):
        raise ControllerError("protected queue intake manifest response is malformed")
    document = json.loads(content_text(item))
    if document.get("record_type") != "GCL_QUEUE_INTAKE_BINDINGS" or document.get("schema_version") != "1.0.0":
        raise ControllerError("protected queue intake binding schema mismatch")
    auth = document.get("authority_effect")
    if auth != {"queue_operation_only":True,"mathematical":False,"certification":False}:
        raise ControllerError("protected queue intake authority boundary mismatch")
    entries = document.get("bindings")
    if not isinstance(entries, list):
        raise ControllerError("protected queue intake bindings are not a list")
    ids = [x.get("dispatch_id") for x in entries]
    if any(not isinstance(x,str) for x in ids) or len(set(ids)) != len(ids):
        raise ControllerError("protected queue intake dispatch identities are malformed or duplicated")
    return entries


def profile_for_queue_binding(binding: dict[str, Any]) -> IntakeProfile:
    did = binding["dispatch_id"]
    path = str(binding.get("dispatch_path") or "")
    parts = Path(path)
    if parts.is_absolute() or ".." in parts.parts or parts.name != did + ".json":
        raise ControllerError("protected queue dispatch path is unsafe or unbound")
    campaign = binding.get("campaign")
    if campaign not in {"RH-001","ERDOS-OPEN"}:
        raise ControllerError("queue intake campaign unregistered")
    return IntakeProfile(
        campaign=campaign,
        branch_prefix="intake/" + did.lower(),
        dispatch_re=re.compile("^" + re.escape(did) + "$"),
        base=parts.parent.parent.as_posix(),
        receipt_schema_version="1.0.0",
        pr_title_prefix="GCL queue intake",
        queue_binding=binding,
    )


def profile_for_branch(branch_name: str, gh: Github | None = None) -> tuple[IntakeProfile, str]:
    for profile in PROFILES:
        if branch_name.startswith(profile.branch_prefix):
            slug = branch_name[len("intake/"):].upper()
            if profile.dispatch_re.fullmatch(slug):
                return profile, slug
    if gh is not None:
        for binding in protected_queue_bindings(gh):
            profile = profile_for_queue_binding(binding)
            if branch_name == profile.branch_prefix:
                return profile, binding["dispatch_id"]
    raise ControllerError("branch does not map to a registered external-intake dispatch")


def profile_for_dispatch(dispatch_id: str, gh: Github | None = None) -> IntakeProfile:
    for profile in PROFILES:
        if profile.dispatch_re.fullmatch(dispatch_id):
            return profile
    if gh is not None:
        for binding in protected_queue_bindings(gh):
            if binding.get("dispatch_id") == dispatch_id:
                return profile_for_queue_binding(binding)
    raise ControllerError(f"dispatch is not registered with the external intake controller: {dispatch_id}")


def derive_dispatch_id(branch_name: str) -> str:
    return profile_for_branch(branch_name)[1]


def expected_paths(dispatch_id: str, comment_id: int, gh: Github | None = None) -> tuple[str, str]:
    profile = profile_for_dispatch(dispatch_id, gh)
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
    # Discover candidate heads from open PRs rather than Git matching-refs.
    # Council Clerk/Release Trust app tokens have bounded pull-request access,
    # while matching-refs can legitimately return no visible refs for those
    # installations. Validation below still requires a registered branch
    # prefix, exact dispatch syntax, exact protected dispatch, and exact diff.
    names: list[str] = []
    page = 1
    while True:
        pulls = gh.request(
            "GET",
            f"/repos/{OWNER}/{REPO}/pulls?state=open&base=main&per_page=100&page={page}",
        )
        if not isinstance(pulls, list):
            raise ControllerError("open pull-request list response is not a list")
        for item in pulls:
            if not isinstance(item, dict):
                continue
            head = item.get("head")
            ref = head.get("ref") if isinstance(head, dict) else None
            if not isinstance(ref, str):
                continue
            if any(ref.startswith(profile.branch_prefix) for profile in PROFILES):
                names.append(ref)
        if len(pulls) < 100:
            break
        page += 1
    # Previously this controller only inspected open PRs, which cannot
    # discover a freshly captured evidence branch that has no PR yet.
    # The queue manifest provides a bounded exact list of permitted heads.
    for binding in protected_queue_bindings(gh):
        profile = profile_for_queue_binding(binding)
        branch = profile.branch_prefix
        if branch in names:
            continue
        receipt_directory = f"{profile.base}/receipts/{binding['dispatch_id']}"
        encoded = urllib.parse.quote(receipt_directory, safe="/")
        ref = urllib.parse.quote(branch, safe="")
        if gh.get_optional(f"/repos/{OWNER}/{REPO}/contents/{encoded}?ref={ref}") is not None:
            names.append(branch)
    return sorted(set(names))


def main_has_any_raw(gh: Github, dispatch_id: str) -> bool:
    profile = profile_for_dispatch(dispatch_id, gh)
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
    profile, dispatch_id = profile_for_branch(branch, gh)
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
    raw_path, expected_receipt = expected_paths(dispatch_id, comment_id, gh)
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
        "source_handoff_commit_sha": receipt.get("source_handoff_commit_sha") == dispatch.get("source_handoff_commit_sha"),
        "schema_result": receipt.get("schema_result") == "valid",
        "freshness": receipt.get("freshness") == "current_for_dispatch",
        "handling_state": receipt.get("handling_state") == "received_unadjudicated",
        "mathematical_correctness_adjudicated": receipt.get("mathematical_correctness_adjudicated") is False,
        "independence_strength_adjudicated": receipt.get("independence_strength_adjudicated") is False,
        "canonical_claim_effect": receipt.get("canonical_claim_effect") is False,
    }
    if profile.queue_binding is not None:
        b = profile.queue_binding
        task, _ = fetch_text(gh, b["task_path"], "main")
        checks.update({
            "queue_dispatch_identity": dispatch.get("dispatch_id") == b["dispatch_id"],
            "queue_dispatch_issue": dispatch.get("github_issue_number") == b["github_issue_number"],
            "queue_dispatch_task": dispatch.get("task_path") == b["task_path"],
            "queue_dispatch_commit": dispatch.get("task_commit") == b["task_commit"],
            "queue_task_digest": sha256_text(task) == b["task_sha256"],
            "queue_binding_kind": receipt.get("intake_binding_kind") == "PROTECTED_QUEUE_TASK_AND_ISSUE_DIGEST",
            "queue_receipt_task": receipt.get("task_path") == b["task_path"],
            "queue_receipt_commit": receipt.get("task_commit") == b["task_commit"],
            "queue_receipt_digest": receipt.get("task_sha256") == b["task_sha256"],
            "queue_receipt_issue_digest": receipt.get("issue_body_sha256") == b["issue_body_sha256"],
            "queue_certification_effect": receipt.get("certification_effect") is False,
            "queue_managed": receipt.get("queue_managed") is True,
            "queue_reservation_enforced": receipt.get("worker_reservation_enforced") is True,
            "queue_receipt_actor": isinstance(receipt.get("authenticated_github_actor"), str) and bool(receipt["authenticated_github_actor"]),
            "queue_reservation_owner": receipt.get("worker_reservation_owner") == receipt.get("authenticated_github_actor"),
            "queue_agent_ref": receipt.get("agent_ref") == dispatch.get("agent_ref"),
            "queue_no_legacy_bootstrap": "bootstrap_path" not in receipt,
        })
    else:
        checks.update({
            "bootstrap_sha256": receipt.get("bootstrap_sha256") == dispatch.get("bootstrap_sha256"),
            "source_handoff_blob_sha": receipt.get("source_handoff_blob_sha") == dispatch.get("source_handoff_blob_sha"),
            "source_handoff_sha256": receipt.get("source_handoff_sha256") == dispatch.get("source_handoff_sha256"),
        })
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
    profile = profile_for_dispatch(dispatch_id, gh)
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
