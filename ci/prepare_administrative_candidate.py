from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from administrative_automation import (
    AutomationError,
    build_candidate_manifest,
    candidate_mutation_allowed,
    derive_completion_state,
    iso_z,
    load_json,
    preparation_occurrences,
    validate_candidate_manifest,
    validate_config,
)

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "governance" / "administrative_maintenance_automation.json"
REGISTRY_PATH = ROOT / "governance" / "administrative_maintenance_trigger_registry.json"
REPORT_PATH = ROOT / "administrative-maintenance-candidate.json"
UTC = timezone.utc


class GitHubClient:
    def __init__(self, token: str, api_url: str = "https://api.github.com") -> None:
        if not token:
            raise AutomationError("GITHUB_TOKEN is required in apply mode")
        self.token = token
        self.api_url = api_url.rstrip("/")

    def request(self, method: str, path: str, payload: dict[str, Any] | None = None) -> Any:
        data = None if payload is None else json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            f"{self.api_url}{path}",
            data=data,
            method=method,
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {self.token}",
                "X-GitHub-Api-Version": "2022-11-28",
                "User-Agent": "grandchallenge-maintenance-automation",
            },
        )
        try:
            with urllib.request.urlopen(request) as response:
                body = response.read()
                return json.loads(body) if body else None
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise AutomationError(f"GitHub API {method} {path} failed: {exc.code} {detail}") from exc

    def get(self, path: str) -> Any:
        return self.request("GET", path)

    def post(self, path: str, payload: dict[str, Any]) -> Any:
        return self.request("POST", path, payload)

    def put(self, path: str, payload: dict[str, Any]) -> Any:
        return self.request("PUT", path, payload)

    def patch(self, path: str, payload: dict[str, Any]) -> Any:
        return self.request("PATCH", path, payload)


def repository_state(client: GitHubClient, repositories: list[str]) -> list[dict[str, Any]]:
    state: list[dict[str, Any]] = []
    for repository in repositories:
        encoded = urllib.parse.quote(repository, safe="/")
        repo = client.get(f"/repos/{encoded}")
        default_branch = repo["default_branch"]
        branch = client.get(f"/repos/{encoded}/branches/{urllib.parse.quote(default_branch, safe='')}")
        pulls = client.get(f"/repos/{encoded}/pulls?state=open&per_page=100")
        state.append(
            {
                "repository": repository,
                "default_branch": default_branch,
                "protected_head": branch["commit"]["sha"],
                "open_pull_requests": [
                    {
                        "number": item["number"],
                        "head": item["head"]["sha"],
                        "base": item["base"]["sha"],
                        "draft": bool(item["draft"]),
                        "author": item["user"]["login"],
                    }
                    for item in pulls
                ],
            }
        )
    return state


def issue_marker(key: str) -> str:
    return f"<!-- administrative-candidate:{key} -->"


def find_issue(client: GitHubClient, repository: str, marker: str) -> dict[str, Any] | None:
    items = client.get(f"/repos/{repository}/issues?state=all&per_page=100&sort=updated&direction=desc")
    return next((item for item in items if "pull_request" not in item and marker in str(item.get("body") or "")), None)


def find_pull_request(client: GitHubClient, repository: str, branch: str) -> dict[str, Any] | None:
    owner = repository.split("/", 1)[0]
    query = urllib.parse.urlencode({"state": "all", "head": f"{owner}:{branch}", "per_page": 100})
    items = client.get(f"/repos/{repository}/pulls?{query}")
    return items[0] if items else None


def get_branch(client: GitHubClient, repository: str, branch: str) -> dict[str, Any] | None:
    try:
        return client.get(f"/repos/{repository}/branches/{urllib.parse.quote(branch, safe='')}")
    except AutomationError as exc:
        if " 404 " in str(exc):
            return None
        raise


def get_content(client: GitHubClient, repository: str, path: str, ref: str) -> dict[str, Any] | None:
    query = urllib.parse.urlencode({"ref": ref})
    try:
        return client.get(f"/repos/{repository}/contents/{path}?{query}")
    except AutomationError as exc:
        if " 404 " in str(exc):
            return None
        raise


def put_manifest(client: GitHubClient, repository: str, branch: str, path: str, manifest: dict[str, Any], existing: dict[str, Any] | None) -> str:
    content = base64.b64encode((json.dumps(manifest, indent=2) + "\n").encode("utf-8")).decode("ascii")
    payload: dict[str, Any] = {
        "message": f"Prepare administrative candidate {manifest['occurrence_key']}",
        "content": content,
        "branch": branch,
    }
    if existing:
        payload["sha"] = existing["sha"]
    result = client.put(f"/repos/{repository}/contents/{path}", payload)
    return result["commit"]["sha"]


def issue_body(occurrence: Any, source_head: str) -> str:
    marker = issue_marker(occurrence.occurrence_key)
    return f"""{marker}
# Automated administrative candidate

## State

`CANDIDATE_PREPARED`

This issue was created by bounded preparation automation. It is navigation and execution coordination only. It creates no protected authority.

- control: `MP-ADMIN-MAINT-001`
- procedure: `{occurrence.procedure_id}`
- occurrence key: `{occurrence.occurrence_key}`
- scheduled due time: `{iso_z(occurrence.due_at)}`
- preparation time: `{iso_z(occurrence.prepare_at)}`
- automated mutation freeze: `{iso_z(occurrence.freeze_at)}`
- source protected head: `{source_head}`
- candidate branch: `{occurrence.branch_name}`
- candidate manifest: `{occurrence.manifest_path}`

## Manual authority gates

The candidate cannot become protected complete without:

1. an unchanged exact-head non-author `APPROVED` review;
2. an explicit Human Steward exact-head disposition;
3. a deliberate protected expected-head merge;
4. protected-main readback.

Automation may not create or impersonate any of those gates.
"""


def pull_request_body(occurrence: Any, issue_number: int, source_head: str) -> str:
    return f"""Prepares the non-authoritative candidate for #{issue_number}.

- state: `CANDIDATE_PREPARED`;
- occurrence key: `{occurrence.occurrence_key}`;
- scheduled due time: `{iso_z(occurrence.due_at)}`;
- source protected head: `{source_head}`;
- automated mutation freeze: `{iso_z(occurrence.freeze_at)}`.

This pull request is created as a draft. Automation must not mark it ready, approve it, create a Human Steward disposition, enable auto-merge, or merge it.

The exact-state manifest is a preparation artifact, not the final protected procedure record. A human-controlled review-ready head must contain the final record, validation evidence, and claim boundaries required by the procedure.
"""


def parse_generated_at(manifest: dict[str, Any]) -> datetime:
    from administrative_automation import parse_datetime

    return parse_datetime(str(manifest["generated_at"]))


def apply_occurrence(client: GitHubClient, repository: str, occurrence: Any, now: datetime, state: list[dict[str, Any]]) -> dict[str, Any]:
    repo_info = client.get(f"/repos/{repository}")
    default_branch = repo_info["default_branch"]
    default = client.get(f"/repos/{repository}/branches/{default_branch}")
    source_head = default["commit"]["sha"]
    marker = issue_marker(occurrence.occurrence_key)
    issue = find_issue(client, repository, marker)
    branch = get_branch(client, repository, occurrence.branch_name)
    pull_request = find_pull_request(client, repository, occurrence.branch_name)
    frozen = not candidate_mutation_allowed(occurrence, now)

    if frozen and not (issue and branch and pull_request):
        raise AutomationError(f"{occurrence.occurrence_key}: candidate missing after automated mutation freeze")

    if not issue:
        issue = client.post(
            f"/repos/{repository}/issues",
            {
                "title": f"[maintenance-candidate] {occurrence.procedure_id} due {iso_z(occurrence.due_at)}",
                "body": issue_body(occurrence, source_head),
                "labels": ["governance"],
            },
        )

    if not branch:
        client.post(f"/repos/{repository}/git/refs", {"ref": f"refs/heads/{occurrence.branch_name}", "sha": source_head})
        branch = get_branch(client, repository, occurrence.branch_name)

    existing = get_content(client, repository, occurrence.manifest_path, occurrence.branch_name)
    existing_manifest = None
    if existing:
        existing_manifest = json.loads(base64.b64decode(existing["content"]).decode("utf-8"))
        source_head = str(existing_manifest["source_protected_head"])

    manifest = build_candidate_manifest(
        occurrence,
        generated_at=parse_generated_at(existing_manifest) if existing_manifest else now,
        source_head=source_head,
        repository_state=state,
        issue_number=issue["number"],
        pull_request_number=pull_request["number"] if pull_request else None,
    )
    errors = validate_candidate_manifest(manifest, occurrence)
    if errors:
        raise AutomationError("; ".join(errors))

    changed = existing_manifest != manifest
    if changed and frozen:
        raise AutomationError(f"{occurrence.occurrence_key}: evidence changed after automated mutation freeze")
    if changed:
        put_manifest(client, repository, occurrence.branch_name, occurrence.manifest_path, manifest, existing)

    if not pull_request:
        pull_request = client.post(
            f"/repos/{repository}/pulls",
            {
                "title": f"[maintenance-candidate] {occurrence.procedure_id} due {iso_z(occurrence.due_at)}",
                "head": occurrence.branch_name,
                "base": default_branch,
                "body": pull_request_body(occurrence, issue["number"], source_head),
                "draft": True,
                "maintainer_can_modify": True,
            },
        )
        refreshed = build_candidate_manifest(
            occurrence,
            generated_at=parse_generated_at(manifest),
            source_head=source_head,
            repository_state=state,
            issue_number=issue["number"],
            pull_request_number=pull_request["number"],
        )
        current = get_content(client, repository, occurrence.manifest_path, occurrence.branch_name)
        put_manifest(client, repository, occurrence.branch_name, occurrence.manifest_path, refreshed, current)
        manifest = refreshed

    if pull_request.get("draft") is not True:
        raise AutomationError(f"{occurrence.occurrence_key}: automated candidate PR is not draft")

    return {
        "occurrence_key": occurrence.occurrence_key,
        "issue_number": issue["number"],
        "branch": occurrence.branch_name,
        "pull_request_number": pull_request["number"],
        "manifest_path": occurrence.manifest_path,
        "source_protected_head": source_head,
        "frozen": frozen,
        "manifest_changed": changed,
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--now", default="")
    parser.add_argument("--report", type=Path, default=REPORT_PATH)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    config = load_json(CONFIG_PATH)
    config_errors = validate_config(config)
    if config_errors:
        raise AutomationError("; ".join(config_errors))
    registry = load_json(REGISTRY_PATH)
    head = os.environ.get("GITHUB_SHA") or subprocess_head()
    completion = derive_completion_state(ROOT, config, head)
    now = datetime.fromisoformat(args.now.replace("Z", "+00:00")) if args.now else datetime.now(UTC)
    if now.tzinfo is None:
        raise AutomationError("--now must include an offset")
    now = now.astimezone(UTC)
    occurrences = preparation_occurrences(config, registry, completion, now)

    results: list[dict[str, Any]] = []
    if args.apply:
        repository = os.environ.get("GITHUB_REPOSITORY", "")
        if repository != config["repository"]:
            raise AutomationError("candidate workflow repository mismatch")
        client = GitHubClient(os.environ.get("GITHUB_TOKEN", ""), os.environ.get("GITHUB_API_URL", "https://api.github.com"))
        state = repository_state(client, config["evidence_repositories"])
        for occurrence in occurrences:
            results.append(apply_occurrence(client, repository, occurrence, now, state))
    else:
        results = [
            {
                "occurrence_key": item.occurrence_key,
                "procedure_id": item.procedure_id,
                "scheduled_due_at": iso_z(item.due_at),
                "prepare_at": iso_z(item.prepare_at),
                "freeze_at": iso_z(item.freeze_at),
                "branch": item.branch_name,
                "manifest_path": item.manifest_path,
                "mutation_allowed": candidate_mutation_allowed(item, now),
            }
            for item in occurrences
        ]

    report = {
        "schema_version": "1.0.0",
        "state": "CANDIDATE_PREPARATION_EVALUATED",
        "evaluated_at": iso_z(now),
        "apply": args.apply,
        "occurrence_count": len(results),
        "results": results,
        "authority_boundary": {
            "approval_created": False,
            "human_steward_disposition_created": False,
            "merge_created": False,
            "auto_merge_enabled": False,
        },
    }
    args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0


def subprocess_head() -> str:
    import subprocess

    return subprocess.run(["git", "rev-parse", "HEAD"], check=True, text=True, capture_output=True).stdout.strip()


if __name__ == "__main__":
    raise SystemExit(main())
