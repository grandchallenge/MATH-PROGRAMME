#!/usr/bin/env python3
"""Bounded GCL Project #2 queue projection for ERDOS-ROLLING-024 source critics.

Never claims source approval, worker independence, Solve dispatch or certification.
Uses already-governed clerk token, not a new bot credential or pickup mechanism.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
ROSTER = ROOT / "governance/erdos_catalogue/ROLLING_RESEARCH_024.json"
OWNER, REPO, PROJECT = "grandchallenge", "MATH-PROGRAMME", 2
PROJECT_ID = "PVT_kwDOB9Ao_c4Blwur"
LABELS = {"gcl-job", "gcl-pickup:direct-editorial", "gcl-collab:cooperative",
          "gcl-role:source-audit", "gcl-state:available"}
FIELD_EXPECTED = {"GCL State": "AVAILABLE", "GCL Role": "SOURCE",
                  "GCL Collaboration": "COOPERATIVE",
                  "GCL Phase": "VERIFICATION", "Status": "Todo"}
TEXT_FIELDS = {"GCL Campaign": "ERDOS-ROLLING-024-001",
               "GCL Cohort": "ERDOS-ROLLING-024-001"}


def candidates(data: dict) -> list[dict]:
    """No other issues can be queued by this controller."""
    if data.get("cohort_id") != "ERDOS-ROLLING-024-001":
        raise ValueError("unknown cohort")
    slots = data.get("items")
    if not isinstance(slots, list) or len(slots) != 24:
        raise ValueError("cohort size drift")
    out, seen = [], set()
    for slot in slots:
        n, review, result = slot["problem_id"], slot["source_critical_review_issue"], slot["worker_result_comment_id"]
        if slot["solve_execution_authorized"] or slot["claimable"] or any(slot["launch_gates"].values()):
            raise ValueError("Solve authorization drift in preparatory cohort")
        if review is not None:
            if not isinstance(review, int) or review <= 0 or not isinstance(result, int) or result <= 0:
                raise ValueError("unbound critical issue or returned result")
            if review in seen:
                raise ValueError("duplicate critical issue")
            seen.add(review)
            out.append({"problem": n, "issue": review, "catalogue": slot["catalogue_issue"],
                        "result": result})
    returned = sum(1 for slot in slots if slot["worker_result_comment_id"] is not None)
    if len(out) != returned or len(seen) != returned:
        raise ValueError("one bound review docket required for each returned design; reconcile protected selection first")
    return out


def gh(*args: str) -> object:
    run = subprocess.run(["gh", *args], capture_output=True, text=True, timeout=90)
    if run.returncode:
        raise RuntimeError(f"gh {args[:3]} failed: {run.stderr[:350]}")
    return json.loads(run.stdout)


def gh_action(*args: str) -> None:
    run = subprocess.run(["gh", *args], capture_output=True, text=True, timeout=90)
    if run.returncode:
        raise RuntimeError(f"gh {args[:3]} failed: {run.stderr[:350]}")


def issue(ident: int) -> dict:
    data = gh("api", f"repos/{OWNER}/{REPO}/issues/{ident}")
    if not isinstance(data, dict):
        raise ValueError("invalid issue readback")
    return data


def review_is_already_accepted(ident: int) -> bool:
    comments = gh("api", f"repos/{OWNER}/{REPO}/issues/{ident}/comments?per_page=100")
    if not isinstance(comments, list) or len(comments) == 100:
        raise ValueError("ambiguous critical review history or pagination")
    for comment in comments:
        body = comment.get("body", "")
        if body.startswith("GCL-CRITICAL-REVIEW/1") and "\nDISPOSITION: SOURCE_ACCEPTED" in body:
            return True
    return False


def verified_source_issue(task: dict) -> dict:
    obj = issue(task["issue"])
    labels = {l["name"] for l in obj.get("labels", [])}
    if obj.get("state") != "open" or obj.get("pull_request"):
        raise ValueError("review docket is not an open issue")
    if not obj.get("title", "").startswith(f"ERDOS {task['problem']} "):
        raise ValueError("review docket title identity drift")
    body = obj.get("body") or ""
    if (f"issues/{task['catalogue']}" not in body or str(task["result"]) not in body):
        raise ValueError("review docket is not bound to exact original worker evidence")
    if any(label.startswith("gcl-state:") and label != "gcl-state:available" for label in labels):
        raise ValueError("review docket has a conflicting lifecycle label")
    return obj


def project_fields() -> dict:
    data = gh("project", "field-list", str(PROJECT), "--owner", OWNER, "--format", "json")
    fields = data.get("fields") or []
    by_name = {f["name"]: f for f in fields}
    if len(by_name) != len(fields):
        raise ValueError("duplicate Project field")
    for name in (*FIELD_EXPECTED, *TEXT_FIELDS):
        if name not in by_name:
            raise ValueError(f"missing Project field: {name}")
    for name, target in FIELD_EXPECTED.items():
        options = [opt for opt in by_name[name].get("options", []) if opt["name"] == target]
        if len(options) != 1:
            raise ValueError(f"Project option {name}/{target} missing or ambiguous")
    return by_name


def project_item_for_issue(ident: int) -> str | None:
    q = """
query($o:String!, $r:String!, $n:Int!){
 repository(owner:$o,name:$r){
  issue(number:$n){projectItems(first:100){
   pageInfo{hasNextPage}
   nodes{id project{id}}
  }}
 }
}"""
    graph = gh("api", "graphql", "-f", f"query={q}", "-F", f"o={OWNER}", "-F", f"r={REPO}", "-F", f"n={ident}")
    items = graph["data"]["repository"]["issue"]["projectItems"]
    if items["pageInfo"]["hasNextPage"]:
        raise ValueError("project membership paginated")
    found = [i["id"] for i in items["nodes"] if i["project"]["id"] == PROJECT_ID]
    if len(found) > 1:
        raise ValueError("duplicate Project #2 items")
    return found[0] if found else None


def issue_fields(ident: int) -> dict:
    records = gh("api", f"repos/{OWNER}/{REPO}/issues/{ident}/issue-field-values")
    if not isinstance(records, list):
        raise ValueError("invalid Issue Field response")
    return {r["issue_field_name"]: ((r.get("single_select_option") or {}).get("name") or r.get("value"))
            for r in records}


def apply_one(task: dict, fields: dict, dry_run: bool) -> dict:
    ident = task["issue"]
    obj = verified_source_issue(task)
    if review_is_already_accepted(ident):
        return {"issue": ident, "state": "SOURCE_ACCEPTED_REQUIRES_PROTECTED_ADJUDICATION"}
    item = project_item_for_issue(ident)
    if dry_run:
        return {"issue": ident, "state": "DRY_RUN", "project_item": item}
    if item is None:
        added = gh("project", "item-add", str(PROJECT), "--owner", OWNER,
                   "--url", obj["html_url"], "--format", "json")
        item = added["id"]
        if project_item_for_issue(ident) != item:
            raise RuntimeError("Project add missing on readback")
    for name, target in FIELD_EXPECTED.items():
        f = fields[name]
        option = next(o["id"] for o in f["options"] if o["name"] == target)
        gh_action("project", "item-edit", "--id", item, "--project-id", PROJECT_ID,
                  "--field-id", f["id"], "--single-select-option-id", option)
    for name, value in TEXT_FIELDS.items():
        gh_action("project", "item-edit", "--id", item, "--project-id", PROJECT_ID,
                  "--field-id", fields[name]["id"], "--text", value)
    actual = issue_fields(ident)
    missing = {k: v for k, v in {**FIELD_EXPECTED, **TEXT_FIELDS}.items() if k != "Status" and actual.get(k) != v}
    if missing:
        raise RuntimeError(f"Issue Field readback failed for {ident}: {missing}; do not label AVAILABLE")
    obj = issue(ident)
    existing = {l["name"] for l in obj.get("labels", [])}
    if any(s.startswith("gcl-state:") and s != "gcl-state:available" for s in existing):
        raise RuntimeError("lifecycle changed during projection")
    additions = sorted(LABELS - existing)
    if additions:
        gh_action("api", f"repos/{OWNER}/{REPO}/issues/{ident}/labels",
                  "--method", "POST", "-f", "labels[]=" + additions[0],
                  *sum([["-f", "labels[]=" + name] for name in additions[1:]], []))
    final = issue(ident)
    final_labels = {l["name"] for l in final["labels"]}
    if not LABELS.issubset(final_labels) or project_item_for_issue(ident) != item:
        raise RuntimeError("availability/project final readback incomplete")
    return {"issue": ident, "state": "AVAILABLE_REVIEW_ONLY", "item": item}


def main() -> int:
    p = argparse.ArgumentParser()
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument("--apply", action="store_true")
    group.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    try:
        tasks = candidates(json.loads(ROSTER.read_text(encoding="utf-8")))
        fields = project_fields()
        results = []
        for task in tasks:
            # Failure must be visible, not falsely count later dockets as complete.
            results.append(apply_one(task, fields, args.dry_run))
        print(json.dumps({"cohort": "ERDOS-ROLLING-024-001", "reviews": results}, sort_keys=True))
        return 0
    except (OSError, KeyError, TypeError, ValueError, RuntimeError, subprocess.TimeoutExpired) as exc:
        print(f"ERDOS_REVIEW_QUEUE_BLOCKED: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
