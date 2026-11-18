#!/usr/bin/env python3
"""Read-only exact Project #2 lifecycle integrity audit.

GitHub Project Status is a workflow projection. GCL State is an organization
Issue Field and gcl-state:* labels are discovery signals, not execution authority.
The empty duplicate Project field is explicitly NOT the canonical Issue Field.
"""
from __future__ import annotations
import json
import subprocess
import sys

PROJECT = "PVT_kwDOB9Ao_c4Blwur"
EXPECTED_STATUS = {"Todo", "In Progress", "Done", "RETURNED"}
AVAILABLE_FILTER = "is:open label:gcl-state:available"
QUERY = """query($after:String,$includeMetadata:Boolean!){
 organization(login:"grandchallenge"){projectV2(number:2){
 id fields(first:100) @include(if:$includeMetadata){nodes{... on ProjectV2SingleSelectField{name options{name}}}}
 views(first:100) @include(if:$includeMetadata){nodes{name filter}}
 items(first:100,after:$after){pageInfo{hasNextPage endCursor} nodes{
 id content{... on Issue{number state repository{nameWithOwner}
 labels(first:100){totalCount nodes{name}}}}
 fieldValueByName(name:"Status"){... on ProjectV2ItemFieldSingleSelectValue{name}}
 duplicate:fieldValueByName(name:"GCL State"){... on ProjectV2ItemFieldSingleSelectValue{name}}
 }}
 }}}
"""

def validate(fields, views, rows):
    errors, notices = [], []
    field_map = {f["name"]: f for f in fields if f and f.get("name")}
    status = field_map.get("Status")
    if status is None or {x["name"] for x in status.get("options", [])} != EXPECTED_STATUS:
        errors.append("STATUS_SCHEMA_DRIFT")
    duplicate = field_map.get("GCL State")
    if duplicate is None:
        notices.append("PROJECT_GCL_STATE_DUPLICATE_ABSENT")
    elif duplicate.get("options"):
        errors.append("PROJECT_GCL_STATE_DUPLICATE_CONFIGURED")
    if not any(v["name"] == "AVAILABLE" and v.get("filter") == AVAILABLE_FILTER for v in views):
        errors.append("AVAILABLE_VIEW_DRIFT")
    counts = {"items": len(rows), "available": 0, "closed": 0, "returned": 0}
    seen = set()
    for row in rows:
        c = row.get("content")
        if not c:
            notices.append("NON_ISSUE_PROJECT_ITEM")
            continue
        key = (c["repository"]["nameWithOwner"], c["number"])
        if key in seen:
            errors.append(f"DUPLICATE_ITEM:{key}")
        seen.add(key)
        s = (row.get("fieldValueByName") or {}).get("name")
        if s is not None and s not in EXPECTED_STATUS:
            errors.append(f"UNKNOWN_STATUS:{key}:{s}")
        if (row.get("duplicate") or {}).get("name") is not None:
            errors.append(f"PROJECT_GCL_STATE_DUPLICATE_POPULATED:{key}")
        labels_obj = c.get("labels") or {}
        labels = {n["name"] for n in labels_obj.get("nodes", [])}
        if labels_obj.get("totalCount", 0) > len(labels):
            errors.append(f"LABELS_TRUNCATED:{key}")
        available = "gcl-state:available" in labels
        returned = "gcl-state:returned" in labels
        if available: counts["available"] += 1
        if returned: counts["returned"] += 1
        if available and returned:
            errors.append(f"CONFLICTING_LIFECYCLE_LABELS:{key}")
        if c["state"] == "CLOSED":
            counts["closed"] += 1
            if available: errors.append(f"CLOSED_AVAILABLE:{key}")
            if s in ("Todo", "In Progress"): errors.append(f"CLOSED_ACTIVE_STATUS:{key}:{s}")
        # A returned worker dispatch may remain OPEN for intake while its
        # Project workflow is Done. Do not treat that as inconsistent.
        if c["state"] == "OPEN" and s == "Done" and not returned:
            notices.append(f"OPEN_DONE_REQUIRES_DISPOSITION_REVIEW:{key}")
        if available and c["state"] != "OPEN":
            errors.append(f"NONOPEN_AVAILABLE:{key}")
    return {"record_type": "GCL_PROJECT_LIFECYCLE_INTEGRITY/1",
            "counts": counts, "errors": sorted(set(errors)),
            "notices": sorted(set(notices)),
            "status": "FAIL" if errors else "PASS_WITH_NOTICES" if notices else "PASS"}

def main():
    cursor = None
    rows = []
    fields = views = None
    project_id = None
    while True:
        args = ["gh", "api", "graphql", "-f", "query=" + QUERY,
                "-F", "includeMetadata=" + ("true" if fields is None else "false")]
        if cursor:
            args += ["-f", "after=" + cursor]
        result = subprocess.run(args, capture_output=True, text=True, check=True)
        payload = json.loads(result.stdout)
        if payload.get("errors"):
            raise RuntimeError(payload["errors"])
        project = payload["data"]["organization"]["projectV2"]
        if project_id is not None and project["id"] != project_id:
            raise RuntimeError("project identity drift")
        project_id = project["id"]
        if fields is None:
            if "fields" not in project or "views" not in project:
                raise RuntimeError("first-page Project metadata absent")
            fields = project["fields"]["nodes"]
            views = project["views"]["nodes"]
        elif "fields" in project or "views" in project:
            raise RuntimeError("unexpected repeated Project metadata")
        page = project["items"]
        rows.extend(page["nodes"])
        if not page["pageInfo"]["hasNextPage"]:
            break
        cursor = page["pageInfo"]["endCursor"]
        if not cursor:
            raise RuntimeError("missing pagination cursor")
    if project_id != PROJECT:
        raise RuntimeError("unexpected project identity")
    report = validate(fields, views, rows)
    print(json.dumps(report, indent=2))
    return 1 if report["errors"] else 0

if __name__ == "__main__":
    sys.exit(main())
