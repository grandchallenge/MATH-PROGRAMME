#!/usr/bin/env python3
"""Bounded GCL Project #2 queue projection for ERDOS-ROLLING-024 source critics.

Never claims source approval, worker independence, Solve dispatch or certification.
Uses already-governed clerk token, not a new bot credential or pickup mechanism.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
ROSTER = ROOT / "governance/erdos_catalogue/ROLLING_RESEARCH_024.json"
OWNER, REPO, PROJECT = "grandchallenge", "MATH-PROGRAMME", 2
PROJECT_ID = "PVT_kwDOB9Ao_c4Blwur"
PROJECT_STATUS_FIELD_ID = "PVTSSF_lADOB9Ao_c4BlwurzhkcRPQ"
ISSUE_FIELD_IDS = {"GCL State":47953501, "GCL Campaign":47953502,
                   "GCL Role":47953503, "GCL Collaboration":47953504,
                   "GCL Phase":47953505, "GCL Cohort":47953514, "GCL Timebox":47953515}
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


def review_already_recorded(ident: int) -> str | None:
    """An existing SOURCE_ACCEPTED, REVISE or BLOCKED review must never be re-offered."""
    comments = gh("api", f"repos/{OWNER}/{REPO}/issues/{ident}/comments?per_page=100")
    if not isinstance(comments, list) or len(comments) == 100:
        raise ValueError("ambiguous critical review history or pagination")
    dispositions = []
    for comment in comments:
        body = comment.get("body") or ""
        if body.startswith("GCL-CRITICAL-REVIEW/1"):
            rows = [line.split(":", 1)[1].strip() for line in body.splitlines()
                    if line.startswith("DISPOSITION:")]
            if len(rows) != 1 or rows[0] not in {"SOURCE_ACCEPTED", "REVISE", "BLOCKED"}:
                raise ValueError("invalid existing critical-review disposition")
            dispositions.append(rows[0])
    if len(dispositions) > 1:
        raise ValueError("multiple critic dispositions; protected reconciliation required")
    return dispositions[0] if dispositions else None


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
    """Only Status is a Project V2 field; GCL State/Role/etc are organization Issue Fields."""
    data = gh("project", "field-list", str(PROJECT), "--owner", OWNER, "--format", "json")
    fields = data.get("fields") or []
    by_name = {field["name"]: field for field in fields}
    if len(fields) != len(by_name):
        raise ValueError("duplicate Project field")
    status = by_name.get("Status")
    if not status or status.get("id") != PROJECT_STATUS_FIELD_ID:
        raise ValueError("protected Project #2 Status field identity mismatch")
    # The live project Status option ID may be updated by GitHub owners.
    # Bind exact named option at the current verified Project field identity,
    # then re-fetch and match *that same ID* after the write. Reject unknowns.
    raw_options = status.get("options") or []
    matches = [op for op in raw_options if op.get("name") == "Todo"]
    if len(matches) != 1 or not re.fullmatch(r"[0-9a-f]{8}", str(matches[0].get("id", ""))):
        raise ValueError("no unique well-formed Todo option from live protected Project field")
    status["validated_todo_option_id"] = matches[0]["id"]
    return by_name


def add_issue_fields(ident: int) -> None:
    """POST additive Issue Field values; PUT would overwrite unrelated fields."""
    expected = {k: v for k, v in {**FIELD_EXPECTED, **TEXT_FIELDS}.items() if k != "Status"}
    expected["GCL Timebox"] = 35
    payload = {"issue_field_values": [
        {"field_id": ISSUE_FIELD_IDS[name], "value": value}
        for name, value in expected.items()
    ]}
    process = subprocess.run(
        ["gh", "api", f"repos/{OWNER}/{REPO}/issues/{ident}/issue-field-values",
         "--method", "POST", "--input", "-"],
        input=json.dumps(payload), capture_output=True, text=True, timeout=90)
    if process.returncode:
        raise RuntimeError(f"issue field POST failed for #{ident}: {process.stderr[:350]}")


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


def project_status(item_id: str) -> dict:
    """Read the exact Project V2 Status after write; no optimistic label projection."""
    query = """
query($id:ID!){
 node(id:$id){
  ... on ProjectV2Item {
   fieldValueByName(name:"Status") {
    ... on ProjectV2ItemFieldSingleSelectValue {name optionId}
   }
  }
 }
}"""
    response = gh("api", "graphql", "-f", f"query={query}", "-F", f"id={item_id}")
    value = ((response.get("data") or {}).get("node") or {}).get("fieldValueByName") or {}
    if not value.get("name") or not value.get("optionId"):
        raise ValueError("Project Status readback is missing/ambiguous")
    return value


def issue_fields(ident: int) -> dict:
    records = gh("api", f"repos/{OWNER}/{REPO}/issues/{ident}/issue-field-values")
    if not isinstance(records, list):
        raise ValueError("invalid Issue Field response")
    return {r["issue_field_name"]: ((r.get("single_select_option") or {}).get("name") or r.get("value"))
            for r in records}


def apply_one(task: dict, fields: dict, dry_run: bool) -> dict:
    ident = task["issue"]
    obj = verified_source_issue(task)
    disposition = review_already_recorded(ident)
    if disposition is not None:
        return {"issue": ident, "state": "REVIEW_ALREADY_RECORDED",
                "disposition": disposition}
    item = project_item_for_issue(ident)
    if dry_run:
        return {"issue": ident, "state": "DRY_RUN", "project_item": item}
    if item is None:
        added = gh("project", "item-add", str(PROJECT), "--owner", OWNER,
                   "--url", obj["html_url"], "--format", "json")
        item = added["id"]
        if project_item_for_issue(ident) != item:
            raise RuntimeError("Project item-add readback failed")
    add_issue_fields(ident)
    expected = {k: v for k, v in {**FIELD_EXPECTED, **TEXT_FIELDS}.items()
                if k != "Status"}
    expected["GCL Timebox"] = 35
    actual = issue_fields(ident)
    missing = {k: v for k, v in expected.items() if actual.get(k) != v}
    if missing:
        raise RuntimeError(f"Issue Field readback failed #{ident}: {missing}")
    status_field = fields["Status"]
    live_todo_id = status_field["validated_todo_option_id"]
    gh_action("project", "item-edit", "--id", item, "--project-id", PROJECT_ID,
              "--field-id", status_field["id"],
              "--single-select-option-id", live_todo_id)
    actual_status = project_status(item)
    if actual_status != {"name": "Todo", "optionId": live_todo_id}:
        raise RuntimeError(f"Project Status write/readback drift #{ident}: {actual_status}")
    if review_already_recorded(ident) is not None:
        return {"issue": ident, "state": "REVIEW_RETURNED_DURING_PROJECT_UPDATE"}
    obj = issue(ident)
    existing = {label["name"] for label in obj.get("labels", [])}
    if any(label.startswith("gcl-state:") and label != "gcl-state:available"
           for label in existing):
        raise RuntimeError("lifecycle label changed during projection")
    additions = sorted(LABELS - existing)
    if additions:
        proc = subprocess.run(
            ["gh", "api", f"repos/{OWNER}/{REPO}/issues/{ident}/labels",
             "--method", "POST", "--input", "-"],
            input=json.dumps({"labels": additions}),
            capture_output=True, text=True, timeout=90)
        if proc.returncode:
            raise RuntimeError(f"labels POST failed #{ident}: {proc.stderr[:350]}")
    final = issue(ident)
    if not LABELS.issubset({label["name"] for label in final["labels"]}):
        raise RuntimeError("final queue label readback failed")
    if project_item_for_issue(ident) != item:
        raise RuntimeError("final Project membership readback failed")
    if any(issue_fields(ident).get(k) != v for k, v in expected.items()):
        raise RuntimeError("final Issue Field readback failed")
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
