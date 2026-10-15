#!/usr/bin/env python3
"""Read-only, authenticated full issue identity/label check for EC-BULK-007.

Does not change Issues or Projects. Uses the original source manifest as the
authority and checks all 168 frozen body hashes and task IDs. Never infer that
an Issue label certifies Projects, source-fidelity, or publication status.
"""
import argparse
import concurrent.futures
import datetime
import hashlib
import json
import subprocess
import time
import urllib.error
import urllib.request
from pathlib import Path


def auth_token():
    return subprocess.check_output(["gh","auth","token"],text=True).strip()


def issue_readback(item, token):
    repo = "grandchallenge/MATH-PROGRAMME"
    url = f"https://api.github.com/repos/{repo}/issues/{item['audit_issue']}"
    headers = {"Authorization":f"Bearer {token}","Accept":"application/vnd.github+json",
               "User-Agent":"gcl-ec-bulk-007-source-identity-audit"}
    last = None
    for attempt in range(5):
        try:
            with urllib.request.urlopen(urllib.request.Request(url,headers=headers),timeout=20) as response:
                j = json.load(response)
            break
        except (urllib.error.URLError, TimeoutError) as exc:
            last = exc
            if attempt == 4:
                raise
            time.sleep(0.4 * 2**attempt)
    labels = sorted(x["name"] for x in j["labels"])
    errors = []
    if j["number"] != item["audit_issue"]:
        errors.append("ISSUE_ID_MISMATCH")
    if j["state"] != "open":
        errors.append("NOT_OPEN")
    if f"ERDOS-CATALOGUE-{item['problem_id']:04d}-S01" not in j["title"]:
        errors.append("TITLE_OR_TASK_ID_MISMATCH")
    if hashlib.sha256((j.get("body") or "").encode()).hexdigest() != item["original_issue_body_sha256"]:
        errors.append("FROZEN_ORIGINAL_BODY_DIGEST_CHANGED")
    if not {"gcl-job","gcl-pickup:direct-editorial","gcl-role:source-audit"} <= set(labels):
        errors.append("SOURCE_AUDIT_ROLE_LABELS_MISSING")
    if j["assignees"]:
        errors.append("ASSIGNEES_PRESENT_VERIFY_LEASE")
    return {"problem_id":item["problem_id"],"audit_issue":item["audit_issue"],
            "title":j["title"],"state":j["state"],"labels":labels,
            "assignees":[a["login"] for a in j["assignees"]],
            "comments":j["comments"],"result_link":item["source_return"],
            "issues":errors}



def verify_saved_snapshot(manifest: dict, snapshot: dict) -> dict:
    """Validate an already captured authenticated readback, WITHOUT live GitHub calls.

    This deliberately cannot renew identity evidence, determine Projects status,
    certify source fidelity, or change the Issue label lifecycle. A live controller
    must repeat the authenticated scan for fresh custody claims.
    """
    items = manifest.get("items")
    rows = snapshot.get("issues")
    if (not isinstance(items, list) or len(items) != 168
            or not isinstance(rows, list) or len(rows) != 168
            or snapshot.get("total_issues_checked") != 168
            or snapshot.get("issues_with_identity_flags") != 0
            or snapshot.get("record_type") != "EC_BULK_007_SOURCE_ISSUE_READBACK/1"):
        raise ValueError("incomplete or invalid saved cohort identity readback")
    expected = {x["problem_id"]: x for x in items}
    actual = {x["problem_id"]: x for x in rows}
    if len(expected) != 168 or len(actual) != 168 or set(expected) != set(actual):
        raise ValueError("saved readback has missing or duplicate problem identities")
    for n, item in expected.items():
        row = actual[n]
        if (row.get("audit_issue") != item["audit_issue"]
                or row.get("state") != "open" or row.get("issues") != []
                or row.get("result_link") != item["source_return"]
                or not row.get("result_link")
                or not {"gcl-job", "gcl-pickup:direct-editorial", "gcl-role:source-audit"}.issubset(set(row.get("labels", [])))):
            raise ValueError(f"saved original issue or return binding inconsistent for #{n}")
    if snapshot.get("source_return_count_in_manifest") != 168:
        raise ValueError("saved source return count inconsistent")
    return {"record_type": "EC_BULK_007_SAVED_SOURCE_IDENTITY_REPLAY/1",
            "source_issues": 168, "issue_identity_flags": 0,
            "live_identity_freshness": "HISTORICAL_SNAPSHOT_ONLY",
            "source_fidelity_certified": False,
            "projects_state_confirmed": False}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--manifest",default="governance/erdos_compendium/batches/EC-BULK-007.json")
    p.add_argument("--output",default="governance/erdos_compendium/batches/EC-BULK-007_QUEUE_READBACK.json")
    p.add_argument("--workers",type=int,default=10)
    args=p.parse_args()
    assert 1<=args.workers<=16
    m=json.loads(Path(args.manifest).read_text())
    items=m["items"]
    assert len(items)==168 and len({x["problem_id"] for x in items})==168
    token = auth_token()
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as ex:
        rows = list(ex.map(lambda x: issue_readback(x,token),items))
    assert len(rows)==168
    bad=[r for r in rows if r["issues"]]
    result={"record_type":"EC_BULK_007_SOURCE_ISSUE_READBACK/1",
            "cohort_id":"EC-BULK-007",
            "checked_at_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "verified_authentication":"fyremael",
            "registry_blob":m["source_registry_blob"],
            "total_issues_checked":len(rows),
            "open_issue_count":sum(r["state"]=="open" for r in rows),
            "issue_label_available_count":sum("gcl-state:available" in r["labels"] for r in rows),
            "issues_with_identity_flags":len(bad),
            "issue_metadata_flags":{"bad_problems":[r["problem_id"] for r in bad]},
            "project_state_note":"GitHub Issue labels are NOT authoritative Projects #2 status; Project readback separate.",
            "source_return_count_in_manifest":sum(bool(x["source_return"]) for x in items),
            "issues":rows}
    Path(args.output).write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n")
    print(json.dumps({k:v for k,v in result.items() if k in
          ("total_issues_checked","open_issue_count","issue_label_available_count",
           "issues_with_identity_flags","source_return_count_in_manifest")}))
    if bad:
        raise SystemExit("ISSUE_IDENTITY_MISMATCH")


if __name__=="__main__":
    main()
