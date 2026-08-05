from __future__ import annotations

import argparse
import base64
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from administrative_automation import (
    AutomationError,
    completion_by_procedure,
    derive_completion_state,
    iso_z,
    iter_due_occurrences,
    load_json,
    validate_completion_state,
    validate_config,
)
from prepare_administrative_candidate import GitHubClient, find_pull_request, get_branch, get_content

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "governance" / "administrative_maintenance_automation.json"
REGISTRY_PATH = ROOT / "governance" / "administrative_maintenance_trigger_registry.json"
STATE_PATH = ROOT / "governance" / "administrative_maintenance_completion_state.json"
REPORT_PATH = ROOT / "administrative-maintenance-synchronization.json"
PATCH_PATH = ROOT / "administrative-maintenance-cross-repository-mirror.md"
START = "<!-- administrative-automation-state:start -->"
END = "<!-- administrative-automation-state:end -->"
UTC = timezone.utc


def managed_section(completion: dict[str, Any], registry: dict[str, Any], head: str) -> str:
    completed = completion_by_procedure(completion)
    next_items: list[tuple[datetime, str]] = []
    for procedure in registry["procedures"]:
        pending = list(iter_due_occurrences(procedure, completed.get(procedure["id"])))
        if pending:
            next_items.append((pending[0], procedure["id"]))
    next_items.sort()
    lines = [
        START,
        "## Automated maintenance state mirror",
        "",
        "This section is navigation only. Protected repository records and merge receipts remain authoritative.",
        "",
        f"- protected MATH-PROGRAMME head: `{head}`",
        f"- completion-state mode: `{completion['state']}`",
    ]
    for procedure_id, state in completion["procedures"].items():
        lines.append(f"- `{procedure_id}` completed through: `{state['completed_through_utc'] or 'none'}`")
    lines.extend(["", "### Next controlled obligations", ""])
    for due, procedure_id in next_items:
        lines.append(f"- `{procedure_id}`: `{iso_z(due)}`")
    lines.extend(["", "Independent approval, Human Steward exact-head disposition, and protected merge remain manual.", END])
    return "\n".join(lines)


def replace_managed_section(body: str, section: str) -> str:
    if START in body or END in body:
        if body.count(START) != 1 or body.count(END) != 1 or body.index(START) > body.index(END):
            raise AutomationError("mirror body has malformed automation markers")
        before = body[: body.index(START)].rstrip()
        after = body[body.index(END) + len(END) :].lstrip()
        return f"{before}\n\n{section}\n\n{after}".rstrip() + "\n"
    return body.rstrip() + "\n\n" + section + "\n"


def update_issue_mirror(client: GitHubClient, repository: str, number: int, section: str) -> bool:
    issue = client.get(f"/repos/{repository}/issues/{number}")
    current = str(issue.get("body") or "")
    updated = replace_managed_section(current, section)
    if updated == current:
        return False
    client.patch(f"/repos/{repository}/issues/{number}", {"body": updated})
    return True


def put_state_file(client: GitHubClient, repository: str, branch: str, completion: dict[str, Any]) -> str:
    path = STATE_PATH.relative_to(ROOT).as_posix()
    existing = get_content(client, repository, path, branch)
    encoded = base64.b64encode((json.dumps(completion, indent=2) + "\n").encode("utf-8")).decode("ascii")
    payload: dict[str, Any] = {
        "message": f"Synchronize administrative completion state at {completion['derived_from_protected_head'][:12]}",
        "content": encoded,
        "branch": branch,
    }
    if existing:
        payload["sha"] = existing["sha"]
    response = client.put(f"/repos/{repository}/contents/{path}", payload)
    return response["commit"]["sha"]


def create_completion_sync_pr(client: GitHubClient, repository: str, completion: dict[str, Any], head: str) -> dict[str, Any] | None:
    current = load_json(STATE_PATH) if STATE_PATH.exists() else None
    if current == completion:
        return None
    branch = f"automation/maintenance-completion-sync/{head[:12]}"
    if not get_branch(client, repository, branch):
        client.post(f"/repos/{repository}/git/refs", {"ref": f"refs/heads/{branch}", "sha": head})
    commit = put_state_file(client, repository, branch, completion)
    pull = find_pull_request(client, repository, branch)
    if not pull:
        pull = client.post(
            f"/repos/{repository}/pulls",
            {
                "title": f"[maintenance-sync] protected completion state at {head[:12]}",
                "head": branch,
                "base": "main",
                "draft": True,
                "maintainer_can_modify": True,
                "body": f"""Synchronizes the machine-readable completion state derived from protected merge receipts at `{head}`.

This draft PR creates no approval, Human Steward disposition, merge authority, or completion beyond the receipts already present on protected `main`.
""",
            },
        )
    if pull.get("draft") is not True:
        raise AutomationError("completion synchronization PR must remain draft")
    return {"branch": branch, "commit": commit, "pull_request_number": pull["number"]}


def verify_required_workflows(client: GitHubClient, repository: str, head: str) -> dict[str, int]:
    runs = client.get(f"/repos/{repository}/actions/runs?head_sha={head}&event=push&per_page=100")["workflow_runs"]
    required = {"Programme policy checks", "GCL conformance"}
    successful: dict[str, int] = {}
    for run in runs:
        name = str(run.get("name") or "")
        if name in required and run.get("status") == "completed" and run.get("conclusion") == "success":
            successful.setdefault(name, int(run["id"]))
    missing = required - set(successful)
    if missing:
        raise AutomationError(f"protected-main workflows not yet successful: {sorted(missing)}")
    return successful


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--report", type=Path, default=REPORT_PATH)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    config = load_json(CONFIG_PATH)
    errors = validate_config(config)
    if errors:
        raise AutomationError("; ".join(errors))
    registry = load_json(REGISTRY_PATH)
    head = os.environ.get("WORKFLOW_RUN_HEAD_SHA") or os.environ.get("GITHUB_SHA") or subprocess_head()
    completion = derive_completion_state(ROOT, config, head)
    previous = load_json(STATE_PATH) if STATE_PATH.exists() else None
    errors = validate_completion_state(completion, previous)
    if errors:
        raise AutomationError("; ".join(errors))
    section = managed_section(completion, registry, head)
    result: dict[str, Any] = {
        "schema_version": "1.0.0",
        "state": "SYNCHRONIZATION_EVALUATED",
        "protected_head": head,
        "evaluated_at": iso_z(datetime.now(UTC)),
        "completion_digest": completion,
        "same_repository_mirrors": [],
        "cross_repository_mirror": {"state": "NOT_APPLIED"},
        "completion_state_pull_request": None,
        "authority_boundary": {
            "approval_created": False,
            "human_steward_disposition_created": False,
            "merge_created": False,
            "auto_merge_enabled": False,
        },
    }

    if args.apply:
        repository = os.environ.get("GITHUB_REPOSITORY", "")
        if repository != config["repository"]:
            raise AutomationError("synchronizer repository mismatch")
        client = GitHubClient(os.environ.get("GITHUB_TOKEN", ""), os.environ.get("GITHUB_API_URL", "https://api.github.com"))
        result["protected_main_workflows"] = verify_required_workflows(client, repository, head)
        result["completion_state_pull_request"] = create_completion_sync_pr(client, repository, completion, head)
        for mirror in config["mirrors"]:
            if mirror["repository"] == repository:
                changed = update_issue_mirror(client, repository, mirror["issue"], section)
                result["same_repository_mirrors"].append({**mirror, "changed": changed})

        cross = next(item for item in config["mirrors"] if item["repository"] != repository)
        cross_token = os.environ.get("CROSS_REPOSITORY_MAINTENANCE_TOKEN", "")
        if cross_token:
            cross_client = GitHubClient(cross_token, os.environ.get("GITHUB_API_URL", "https://api.github.com"))
            changed = update_issue_mirror(cross_client, cross["repository"], cross["issue"], section)
            result["cross_repository_mirror"] = {**cross, "state": "CURRENT", "changed": changed}
        else:
            PATCH_PATH.write_text(
                f"# Cross-repository mirror patch required\n\nRepository: `{cross['repository']}`\n\nIssue: `#{cross['issue']}`\n\n{section}\n",
                encoding="utf-8",
            )
            result["cross_repository_mirror"] = {
                **cross,
                "state": "CREDENTIAL_MISSING_PATCH_RETAINED",
                "patch": PATCH_PATH.name,
            }
    else:
        result["cross_repository_mirror"] = {"state": "DRY_RUN"}

    args.report.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


def subprocess_head() -> str:
    import subprocess

    return subprocess.run(["git", "rev-parse", "HEAD"], check=True, text=True, capture_output=True).stdout.strip()


if __name__ == "__main__":
    raise SystemExit(main())
