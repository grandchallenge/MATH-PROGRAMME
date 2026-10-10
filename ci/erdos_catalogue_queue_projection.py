#!/usr/bin/env python3
"""Project projection for structurally valid Erdős direct-editorial returns.

Uses gh's authenticated actor, not a mathematical or protected admission authority.
No shell session manipulation; fail closed on ambiguous Project configuration.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys

OWNER = "grandchallenge"
REPO = "MATH-PROGRAMME"
PROJECT = "2"
URL_PREFIX = f"https://github.com/{OWNER}/{REPO}/issues/"
STATES = ("RETURNED",)


def gh(*args: str) -> object:
    p = subprocess.run(["gh", *args], text=True, capture_output=True)
    if p.returncode:
        raise RuntimeError(f"gh {' '.join(args[:3])}: {p.stderr.strip()}")
    return json.loads(p.stdout)


def graph(query: str, **variables: object) -> dict:
    payload = json.dumps({"query": query, "variables": variables})
    result = subprocess.run(["gh", "api", "graphql", "--input", "-"],
                            input=payload, text=True, capture_output=True)
    if result.returncode:
        raise RuntimeError(f"targeted GraphQL query failed: {result.stderr.strip()}")
    response = json.loads(result.stdout)
    if response.get("errors"):
        raise RuntimeError(f"targeted GraphQL errors: {response['errors']}")
    return response["data"]


PROJECT_META_QUERY = """
query($owner: String!, $number: Int!) {
  organization(login: $owner) {
    projectV2(number: $number) {
      id
      fields(first: 100) {
        pageInfo { hasNextPage }
        nodes {
          ... on ProjectV2SingleSelectField {
            id
            name
            options { id name }
          }
        }
      }
    }
  }
}
"""

ISSUE_ITEM_QUERY = """
query($owner: String!, $repo: String!, $number: Int!) {
  repository(owner: $owner, name: $repo) {
    issue(number: $number) {
      projectItems(first: 100) {
        pageInfo { hasNextPage }
        nodes {
          id
          project { id number }
          fieldValueByName(name: "Status") {
            ... on ProjectV2ItemFieldSingleSelectValue { name }
          }
        }
      }
    }
  }
}
"""


def project_metadata() -> tuple[str, str, str]:
    project = graph(PROJECT_META_QUERY, owner=OWNER, number=int(PROJECT))[
        "organization"]["projectV2"]
    if not project or project["fields"]["pageInfo"]["hasNextPage"]:
        raise ValueError("Project fields missing or pagination incomplete")
    matches = [(field, option) for field in project["fields"]["nodes"]
               if field and field.get("name") == "Status"
               for option in field.get("options", [])
               if option["name"].upper() == "RETURNED"]
    if len(matches) != 1:
        raise ValueError("expected exactly one RETURNED option on Project Status")
    return project["id"], matches[0][0]["id"], matches[0][1]["id"]


def issue_project_item(issue: int, project_id: str) -> dict:
    data = graph(ISSUE_ITEM_QUERY, owner=OWNER, repo=REPO, number=issue)
    node = data["repository"]["issue"]
    if node is None or node["projectItems"]["pageInfo"]["hasNextPage"]:
        raise ValueError("Issue project membership missing or paginated")
    matches = [item for item in node["projectItems"]["nodes"]
               if item["project"]["id"] == project_id]
    if len(matches) != 1:
        raise ValueError(f"expected one Project item for #{issue}; got {len(matches)}")
    return {"id": matches[0]["id"],
            "status": (matches[0].get("fieldValueByName") or {}).get("name")}


def validate_receipt(report: dict, issue: int) -> dict:
    tasks = [t for t in report.get("tasks", []) if t.get("issue_number") == issue]
    if len(tasks) != 1:
        raise ValueError("issue missing or ambiguous in captured catalogue task registry")
    rows = [r for r in report.get("receipts", []) if r.get("issue_number") == issue
            and r.get("validation") == "STRUCTURALLY_VALID_UNADJUDICATED"
            and r.get("event_action") != "deleted"]
    if len(rows) != 1:
        raise ValueError(f"expected exactly one current structurally valid return, got {len(rows)}")
    row = rows[0]
    expected = f"ERDOS-CATALOGUE-{row['problem_id']:04d}-S01"
    if row.get("task_id") != expected or tasks[0].get("task_id") != expected or not row.get("comment_id"):
        raise ValueError("return binding mismatch")
    return row


def reconcile(report: dict, issue: int, dry_run: bool) -> dict:
    receipt = validate_receipt(report, issue)
    issue_json = gh("api", f"repos/{OWNER}/{REPO}/issues/{issue}")
    assert isinstance(issue_json, dict)
    labels = {l["name"] for l in issue_json.get("labels", [])}
    if issue_json.get("state") != "open" or not {"gcl-job", "gcl-pickup:direct-editorial", "gcl-role:source-audit"} <= labels:
        raise ValueError("issue state/pickup binding failed")
    comment = gh("api", f"repos/{OWNER}/{REPO}/issues/comments/{receipt['comment_id']}")
    if not isinstance(comment, dict) or comment.get("issue_url") != f"https://api.github.com/repos/{OWNER}/{REPO}/issues/{issue}":
        raise ValueError("comment-to-issue binding failed")
    if not comment.get("body", "").startswith("RESULT/1\n"):
        raise ValueError("return no longer exists or has been edited")
    # Never trust a historical event after a comment edit; verify exact body digest.
    import hashlib
    if hashlib.sha256(comment["body"].encode()).hexdigest() != receipt["comment_body_sha256"]:
        raise ValueError("comment changed since capture; recapture required")
    project_id, field_id, option_id = project_metadata()
    item = issue_project_item(issue, project_id)
    before = {"issue": issue, "comment_id": receipt["comment_id"], "project_item": item["id"],
              "status_before": item.get("status"), "target": "RETURNED", "dry_run": dry_run}
    if dry_run:
        return before
    if str(item.get("status", "")).upper() != "RETURNED":
        subprocess.run(["gh", "project", "item-edit", "--project-id", project_id,
                        "--id", item["id"], "--field-id", field_id,
                        "--single-select-option-id", option_id], check=True)
    if "gcl-state:available" in labels:
        subprocess.run(["gh", "api", "--method", "DELETE",
                        f"repos/{OWNER}/{REPO}/issues/{issue}/labels/gcl-state%3Aavailable"],
                       check=True, stdout=subprocess.DEVNULL)
    final = issue_project_item(issue, project_id)
    if final["id"] != item["id"] or str(final["status"]).upper() != "RETURNED":
        raise RuntimeError("Targeted Project readback does not confirm returned state")
    refreshed = gh("api", f"repos/{OWNER}/{REPO}/issues/{issue}")
    if "gcl-state:available" in {l["name"] for l in refreshed["labels"]}:
        raise RuntimeError("issue availability label persists")
    before["verified_status"] = final.get("status")
    before["available_removed"] = True
    return before


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--report", required=True)
    p.add_argument("--issue", type=int)
    p.add_argument("--all", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    try:
        with open(args.report, encoding="utf-8") as f:
            report = json.load(f)
        if (args.issue is None) == (not args.all):
            raise ValueError("specify exactly one of --issue or --all")
        issues = [args.issue] if args.issue is not None else [t["issue_number"] for t in report.get("tasks", []) if t.get("structurally_valid_returns") == 1]
        results = []
        for issue in issues:
            results.append(reconcile(report, issue, args.dry_run))
        print(json.dumps(results, sort_keys=True))
        return 0
    except (OSError, ValueError, RuntimeError, subprocess.CalledProcessError, KeyError) as exc:
        print(f"QUEUE_RECONCILIATION_BLOCKED: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
