#!/usr/bin/env python3
"""Stage and verify AETHER repository controls with the Release Trust App."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from github_http import build_github_opener


API_ROOT = "https://api.github.com"
REPOSITORY = "grandchallenge/AETHER"
BRANCH = "main"
POLICY_PATH = ".github/repository-controls.json"
REQUIRED_JOBS = {
    "Required CI gate",
    "Required Supply Chain gate",
    "policy / policy",
    "security / action-policy",
}
BRANCH_RULESET_NAME = "Provider profile - main"
TAG_RULESET_NAME = "Immutable release tags"


class AetherControlsError(RuntimeError):
    pass


class GitHubClient:
    def __init__(self, token: str):
        if not token:
            raise AetherControlsError("administration token is empty")
        self.headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "grandchallenge-aether-controls-admin",
        }
        self.opener = build_github_opener()

    def request(
        self,
        method: str,
        path: str,
        data: Any | None = None,
        *,
        allow_404: bool = False,
    ) -> Any:
        body = None if data is None else json.dumps(data).encode("utf-8")
        request = urllib.request.Request(
            f"{API_ROOT}{path}", data=body, headers=self.headers, method=method
        )
        try:
            with self.opener.open(request, timeout=90) as response:
                raw = response.read()
                return json.loads(raw) if raw else None
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            if allow_404 and exc.code == 404:
                return {"_status": 404, "message": detail}
            raise AetherControlsError(
                f"GitHub API {method} {path} failed with {exc.code}: {detail}"
            ) from exc


def canonical_sha256(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def branch_ruleset_payload(policy: dict[str, Any]) -> dict[str, Any]:
    branch = policy["protected_branch"]
    return {
        "name": BRANCH_RULESET_NAME,
        "target": "branch",
        "enforcement": "active",
        "bypass_actors": [],
        "conditions": {"ref_name": {"include": ["~DEFAULT_BRANCH"], "exclude": []}},
        "rules": [
            {"type": "deletion"},
            {"type": "non_fast_forward"},
            {
                "type": "pull_request",
                "parameters": {
                    "allowed_merge_methods": ["merge", "squash"],
                    "dismiss_stale_reviews_on_push": branch["dismiss_stale_reviews"],
                    "require_code_owner_review": branch["require_code_owner_reviews"],
                    "require_last_push_approval": branch["require_last_push_approval"],
                    "required_approving_review_count": branch["minimum_approvals"],
                    "required_review_thread_resolution": branch[
                        "required_conversation_resolution"
                    ],
                    "required_reviewers": [],
                    "dismissal_restriction": {"enabled": False, "allowed_actors": []},
                },
            },
            {
                "type": "required_status_checks",
                "parameters": {
                    "do_not_enforce_on_create": False,
                    "strict_required_status_checks_policy": branch["strict"],
                    "required_status_checks": [
                        {"context": context}
                        for context in branch["required_status_checks"]
                    ],
                },
            },
        ],
    }


def tag_ruleset_payload() -> dict[str, Any]:
    return {
        "name": TAG_RULESET_NAME,
        "target": "tag",
        "enforcement": "active",
        "bypass_actors": [],
        "conditions": {"ref_name": {"include": ["refs/tags/*"], "exclude": []}},
        "rules": [{"type": "deletion"}, {"type": "non_fast_forward"}],
    }


def classic_payload(policy: dict[str, Any], *, locked: bool) -> dict[str, Any]:
    branch = policy["protected_branch"]
    return {
        "required_status_checks": {
            "strict": branch["strict"],
            "contexts": branch["required_status_checks"],
        },
        "enforce_admins": branch["enforce_admins"],
        "required_pull_request_reviews": {
            "dismiss_stale_reviews": branch["dismiss_stale_reviews"],
            "require_code_owner_reviews": branch["require_code_owner_reviews"],
            "require_last_push_approval": branch["require_last_push_approval"],
            "required_approving_review_count": branch["minimum_approvals"],
        },
        "restrictions": None,
        "required_linear_history": False,
        "allow_force_pushes": branch["allow_force_pushes"],
        "allow_deletions": branch["allow_deletions"],
        "block_creations": False,
        "required_conversation_resolution": branch[
            "required_conversation_resolution"
        ],
        "lock_branch": locked,
        "allow_fork_syncing": False,
    }


def load_policy_at(client: GitHubClient, ref: str) -> tuple[dict[str, Any], str]:
    encoded = urllib.parse.quote(POLICY_PATH, safe="/")
    content = client.request(
        "GET", f"/repos/{REPOSITORY}/contents/{encoded}?ref={urllib.parse.quote(ref)}"
    )
    if content.get("encoding") != "base64" or not content.get("content"):
        raise AetherControlsError("AETHER control policy is not canonical base64 content")
    raw = base64.b64decode(content["content"])
    policy = json.loads(raw.decode("utf-8"))
    validate_policy(policy)
    return policy, str(content.get("sha") or "")


def validate_policy(policy: dict[str, Any]) -> None:
    if policy.get("schema_version") != "aether.repository-controls.v1":
        raise AetherControlsError("AETHER policy schema drift")
    if policy.get("repository") != REPOSITORY:
        raise AetherControlsError("AETHER policy repository drift")
    branch = policy.get("protected_branch", {})
    if branch.get("name") != BRANCH:
        raise AetherControlsError("AETHER protected branch drift")
    if set(branch.get("required_status_checks", [])) != REQUIRED_JOBS:
        raise AetherControlsError("AETHER required job set drift")
    fixed = {
        "strict": True,
        "minimum_approvals": 0,
        "dismiss_stale_reviews": True,
        "require_code_owner_reviews": False,
        "require_last_push_approval": False,
        "required_conversation_resolution": True,
        "enforce_admins": True,
        "lock_branch": True,
        "allow_force_pushes": False,
        "allow_deletions": False,
    }
    for key, expected in fixed.items():
        if branch.get(key) is not expected:
            raise AetherControlsError(f"AETHER branch policy drift: {key}")
    model = policy.get("protection_model", {})
    if model.get("default_branch_ruleset", {}).get("name") != BRANCH_RULESET_NAME:
        raise AetherControlsError("AETHER branch ruleset identity drift")
    if model.get("release_tag_ruleset", {}).get("name") != TAG_RULESET_NAME:
        raise AetherControlsError("AETHER tag ruleset identity drift")


def successful_pr_jobs(client: GitHubClient, head_sha: str) -> set[str]:
    query = urllib.parse.urlencode(
        {"head_sha": head_sha, "event": "pull_request", "per_page": 100}
    )
    runs = client.request("GET", f"/repos/{REPOSITORY}/actions/runs?{query}")
    names: set[str] = set()
    for run in runs.get("workflow_runs", []):
        if run.get("head_sha") != head_sha or run.get("conclusion") != "success":
            continue
        jobs = client.request(
            "GET", f"/repos/{REPOSITORY}/actions/runs/{run['id']}/jobs?per_page=100"
        )
        names.update(
            str(job.get("name"))
            for job in jobs.get("jobs", [])
            if job.get("conclusion") == "success"
        )
    return names


def upsert_ruleset(client: GitHubClient, payload: dict[str, Any]) -> int:
    listing = client.request("GET", f"/repos/{REPOSITORY}/rulesets")
    matches = [item for item in listing if item.get("name") == payload["name"]]
    if len(matches) > 1:
        raise AetherControlsError(f"duplicate ruleset identity: {payload['name']}")
    if matches:
        ruleset_id = int(matches[0]["id"])
        client.request("PUT", f"/repos/{REPOSITORY}/rulesets/{ruleset_id}", payload)
        return ruleset_id
    created = client.request("POST", f"/repos/{REPOSITORY}/rulesets", payload)
    return int(created["id"])


def verify_rulesets(client: GitHubClient, policy: dict[str, Any]) -> list[dict[str, Any]]:
    expected = {
        BRANCH_RULESET_NAME: branch_ruleset_payload(policy),
        TAG_RULESET_NAME: tag_ruleset_payload(),
    }
    listing = client.request("GET", f"/repos/{REPOSITORY}/rulesets")
    snapshots = []
    for name, wanted in expected.items():
        matches = [item for item in listing if item.get("name") == name]
        if len(matches) != 1:
            raise AetherControlsError(f"expected one {name!r} ruleset, found {len(matches)}")
        detail = client.request(
            "GET", f"/repos/{REPOSITORY}/rulesets/{matches[0]['id']}"
        )
        observed = {key: detail.get(key) for key in wanted}
        if observed != wanted:
            raise AetherControlsError(f"ruleset readback differs: {name}")
        snapshots.append(detail)
    return snapshots


def stage(client: GitHubClient, pr_number: int, expected_head: str) -> dict[str, Any]:
    pull = client.request("GET", f"/repos/{REPOSITORY}/pulls/{pr_number}")
    actual_head = str(pull.get("head", {}).get("sha") or "")
    if pull.get("state") != "open" or actual_head != expected_head:
        raise AetherControlsError(
            f"AETHER PR identity drift: open/{expected_head} != {pull.get('state')}/{actual_head}"
        )
    policy, policy_blob = load_policy_at(client, expected_head)
    successful = successful_pr_jobs(client, expected_head)
    missing = REQUIRED_JOBS - successful
    if missing:
        raise AetherControlsError(f"AETHER PR jobs are incomplete: {sorted(missing)}")
    classic_before = client.request(
        "GET", f"/repos/{REPOSITORY}/branches/{BRANCH}/protection"
    )
    if classic_before.get("lock_branch", {}).get("enabled") is not True:
        raise AetherControlsError("classic protection was not locked before staging")
    upsert_ruleset(client, branch_ruleset_payload(policy))
    upsert_ruleset(client, tag_ruleset_payload())
    staged_rulesets = verify_rulesets(client, policy)
    client.request(
        "PUT",
        f"/repos/{REPOSITORY}/branches/{BRANCH}/protection",
        classic_payload(policy, locked=False),
    )
    classic_after = client.request(
        "GET", f"/repos/{REPOSITORY}/branches/{BRANCH}/protection"
    )
    if classic_after.get("lock_branch", {}).get("enabled") is not False:
        raise AetherControlsError("classic lock remained enabled after ruleset verification")
    return evidence(
        "staged",
        expected_head,
        policy_blob,
        staged_rulesets,
        classic_before,
        classic_after,
        sorted(successful),
    )


def retire(client: GitHubClient, expected_main: str) -> dict[str, Any]:
    branch = client.request("GET", f"/repos/{REPOSITORY}/branches/{BRANCH}")
    actual_main = str(branch.get("commit", {}).get("sha") or "")
    if actual_main != expected_main:
        raise AetherControlsError(
            f"AETHER protected main drift: {expected_main} != {actual_main}"
        )
    policy, policy_blob = load_policy_at(client, expected_main)
    snapshots = verify_rulesets(client, policy)
    classic_before = client.request(
        "GET", f"/repos/{REPOSITORY}/branches/{BRANCH}/protection"
    )
    client.request("DELETE", f"/repos/{REPOSITORY}/branches/{BRANCH}/protection")
    classic_after = client.request(
        "GET",
        f"/repos/{REPOSITORY}/branches/{BRANCH}/protection",
        allow_404=True,
    )
    if classic_after.get("_status") != 404:
        raise AetherControlsError("classic protection remained after retirement")
    verify_rulesets(client, policy)
    return evidence(
        "retired_classic",
        expected_main,
        policy_blob,
        snapshots,
        classic_before,
        classic_after,
        [],
    )


def evidence(
    state: str,
    subject_sha: str,
    policy_blob: str,
    rulesets: list[dict[str, Any]],
    classic_before: dict[str, Any],
    classic_after: dict[str, Any],
    successful_jobs: list[str],
) -> dict[str, Any]:
    value = {
        "schema_version": "gcl.aether-controls-admin-evidence.v1",
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "repository": REPOSITORY,
        "state": state,
        "subject_sha": subject_sha,
        "policy_path": POLICY_PATH,
        "policy_git_blob_sha1": policy_blob,
        "successful_pr_jobs": successful_jobs,
        "rulesets": rulesets,
        "classic_before": classic_before,
        "classic_after": classic_after,
        "verified": True,
    }
    value["evidence_sha256"] = canonical_sha256(value)
    return value


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("validate", "stage", "retire"), required=True)
    parser.add_argument("--pr-number", type=int, default=59)
    parser.add_argument("--expected-sha", default="")
    parser.add_argument("--token-env", default="GCL_REPOSITORY_ADMIN_TOKEN")
    parser.add_argument("--evidence", type=Path, default=Path("aether-controls-evidence.json"))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        if args.mode == "validate":
            validate_policy(
                {
                    "schema_version": "aether.repository-controls.v1",
                    "repository": REPOSITORY,
                    "protected_branch": {
                        "name": BRANCH,
                        "required_status_checks": sorted(REQUIRED_JOBS),
                        "strict": True,
                        "minimum_approvals": 0,
                        "dismiss_stale_reviews": True,
                        "require_code_owner_reviews": False,
                        "require_last_push_approval": False,
                        "required_conversation_resolution": True,
                        "enforce_admins": True,
                        "lock_branch": True,
                        "allow_force_pushes": False,
                        "allow_deletions": False,
                    },
                    "protection_model": {
                        "default_branch_ruleset": {"name": BRANCH_RULESET_NAME},
                        "release_tag_ruleset": {"name": TAG_RULESET_NAME},
                    },
                }
            )
            print("AETHER control administration contract is valid")
            return 0
        if len(args.expected_sha) != 40:
            raise AetherControlsError("--expected-sha must be one exact commit identity")
        client = GitHubClient(os.environ.get(args.token_env, ""))
        result = (
            stage(client, args.pr_number, args.expected_sha)
            if args.mode == "stage"
            else retire(client, args.expected_sha)
        )
        args.evidence.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"state": result["state"], "evidence_sha256": result["evidence_sha256"]}))
        return 0
    except (AetherControlsError, OSError, json.JSONDecodeError) as exc:
        print(f"AETHER controls administration failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
