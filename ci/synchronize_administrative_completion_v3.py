from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import administrative_automation as automation
import administrative_receipts as receipts

automation.derive_completion_state = receipts.derive_completion_state

import synchronize_administrative_completion as implementation

UTC = timezone.utc
REQUIRED = {"Programme policy checks", "GCL conformance"}


def report_path(argv: list[str]) -> Path:
    if "--report" in argv:
        index = argv.index("--report")
        if index + 1 >= len(argv):
            raise automation.AutomationError("--report requires a path")
        return Path(argv[index + 1])
    return implementation.REPORT_PATH


def successful_workflows(client: implementation.GitHubClient, repository: str, head: str) -> dict[str, int]:
    runs = client.get(f"/repos/{repository}/actions/runs?head_sha={head}&event=push&per_page=100")["workflow_runs"]
    successful: dict[str, int] = {}
    for run in runs:
        name = str(run.get("name") or "")
        if name in REQUIRED and run.get("status") == "completed" and run.get("conclusion") == "success":
            successful.setdefault(name, int(run["id"]))
    return successful


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if "--apply" in args:
        repository = os.environ.get("GITHUB_REPOSITORY", "")
        head = os.environ.get("WORKFLOW_RUN_HEAD_SHA") or os.environ.get("GITHUB_SHA") or implementation.subprocess_head()
        client = implementation.GitHubClient(
            os.environ.get("GITHUB_TOKEN", ""),
            os.environ.get("GITHUB_API_URL", "https://api.github.com"),
        )
        successful = successful_workflows(client, repository, head)
        missing = sorted(REQUIRED - set(successful))
        if missing:
            report = {
                "schema_version": "1.0.0",
                "state": "SYNCHRONIZATION_WAITING_FOR_REQUIRED_WORKFLOWS",
                "protected_head": head,
                "evaluated_at": datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
                "successful_workflows": successful,
                "missing_successful_workflows": missing,
                "protected_completion_advanced": False,
                "mirrors_changed": False,
                "authority_boundary": {
                    "approval_created": False,
                    "human_steward_disposition_created": False,
                    "merge_created": False,
                    "auto_merge_enabled": False,
                },
            }
            path = report_path(args)
            path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
            print(json.dumps(report, indent=2))
            return 0
    return implementation.main(args)


if __name__ == "__main__":
    raise SystemExit(main())
