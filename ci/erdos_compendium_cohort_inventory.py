#!/usr/bin/env python3
"""Read-only exact-registry, authenticated live GitHub queue inventory check."""
from __future__ import annotations

import argparse
import concurrent.futures
import datetime as dt
import hashlib
import json
import time
import urllib.error
import urllib.request
from pathlib import Path

from erdos_compendium_source_reconcile import token

REPO = "grandchallenge/MATH-PROGRAMME"
LABELS = {"gcl-job", "gcl-state:available", "gcl-role:source-audit", "gcl-pickup:direct-editorial"}


def read_issue(number: int, auth: str) -> dict:
    url = f"https://api.github.com/repos/{REPO}/issues/{number}"
    req = urllib.request.Request(url, headers={
        "Authorization": "Bearer " + auth,
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    })
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                return json.load(response)
        except (urllib.error.URLError, TimeoutError) as error:
            if isinstance(error, urllib.error.HTTPError) and error.code not in (500, 502, 503, 504):
                raise
            if attempt == 3:
                raise
            time.sleep(0.5 * 2 ** attempt)
    raise AssertionError("unreachable")


def audit(manifest: dict, auth: str, workers: int) -> dict:
    items = manifest["items"]
    if len(items) != 200 or len({i["problem_id"] for i in items}) != 200:
        raise ValueError("Expected 200 distinct registry problem records")
    def one(item: dict) -> dict:
        n, issue = item["problem_id"], item["audit_issue"]
        obj = read_issue(issue, auth)
        body = obj.get("body") or ""
        labels = {v["name"] for v in obj.get("labels", [])}
        errors = []
        if obj.get("number") != issue or obj.get("state") != "open":
            errors.append("ISSUE_ID_OR_OPEN_STATE")
        if item["assignment_id"] not in obj.get("title", "") or item["assignment_id"] not in body:
            errors.append("ASSIGNMENT_MISMATCH")
        if hashlib.sha256(body.encode()).hexdigest() != item["registry_issue_body_sha256"]:
            errors.append("ISSUE_BODY_DRIFT")
        if not LABELS.issubset(labels):
            errors.append("QUEUE_LABELS_MISMATCH")
        if f"https://www.erdosproblems.com/{n}" not in body:
            errors.append("ORIGINAL_SOURCE_URL_MISSING")
        if manifest["source"]["source_commit"] not in body:
            errors.append("SOURCE_COMMIT_MISMATCH")
        return {"problem_id": n, "issue_number": issue,
                "issue_url": obj.get("html_url"), "state": obj.get("state"),
                "issue_body_sha256": hashlib.sha256(body.encode()).hexdigest(),
                "labels": sorted(labels), "exceptions": errors}
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        records = sorted(pool.map(one, items), key=lambda z: z["problem_id"])
    return {
        "record_type": "ERDOS_COMPENDIUM_COHORT_INVENTORY/1",
        "cohort_id": manifest["cohort_id"],
        "registry_blob": manifest["source_registry_blob"],
        "observed_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "authenticated_live_issue_count": len(records),
        "issue_identity_valid": sum(not r["exceptions"] for r in records),
        "issues_with_exceptions": sum(bool(r["exceptions"]) for r in records),
        "scope": {"ids": [r["problem_id"] for r in records],
                  "issues": [r["issue_number"] for r in records]},
        "source_url_check": "STRUCTURAL_ONLY; NOT AN HTTP REACHABILITY OR PRIMARY_PAPER_VERIFICATION",
        "records": records,
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--manifest", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--workers", type=int, default=6)
    a = p.parse_args()
    if not 1 <= a.workers <= 8:
        p.error("workers must be within 1..8")
    result = audit(json.loads(a.manifest.read_text()), token(), a.workers)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({k: result[k] for k in ("authenticated_live_issue_count",
              "issue_identity_valid", "issues_with_exceptions", "observed_utc")}))
    if result["issues_with_exceptions"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
