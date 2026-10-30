#!/usr/bin/env python3
"""One-issue, source-locked return projection. No mathematical admission."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

try:
    from ci import erdos_catalogue_programme_intake as intake
    from ci import erdos_catalogue_queue_projection as project
except ModuleNotFoundError:
    import erdos_catalogue_programme_intake as intake
    import erdos_catalogue_queue_projection as project

SCHEMA = "GCL-ERDOS-RETURN-FASTPATH/1"
REPO = "grandchallenge/MATH-PROGRAMME"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def api(url):
    """Bounded retry of read-only source queries on transport timeout only.

    Never retry explicit nonzero responses (including permission/policy denial).
    No mutations occur in this helper; source identities are checked by capture.
    """
    for attempt in range(2):
        try:
            p = subprocess.run(["gh", "api", url], capture_output=True,
                               text=True, timeout=60)
        except subprocess.TimeoutExpired:
            if attempt == 0:
                continue
            raise
        if p.returncode:
            raise RuntimeError(f"GitHub source read {url}: {p.stderr[-900:]}")
        return json.loads(p.stdout)
    raise AssertionError("unreachable read retry state")


def source_event(path):
    event = json.loads(path.read_text())
    if (os.getenv("GITHUB_ACTIONS") != "true"
        or os.getenv("GITHUB_REPOSITORY") != REPO
        or os.getenv("GITHUB_REF") != "refs/heads/main"
        or os.getenv("GITHUB_EVENT_NAME") != "issue_comment"
        or event.get("repository", {}).get("full_name") != REPO
        or event.get("action") not in ("created", "edited")):
        raise ValueError("not a protected source-return event")
    issue = event.get("issue") or {}
    comment = event.get("comment") or {}
    n, cid = issue.get("number"), comment.get("id")
    if (type(n) is not int or n < 1 or type(cid) is not int or cid < 1
        or issue.get("pull_request")
        or not isinstance(comment.get("body"), str)
        or not comment["body"].startswith("RESULT/1\n")):
        raise ValueError("invalid RESULT/1 event binding")
    return event, n, cid


def capture(event_path, out):
    event, n, cid = source_event(event_path)
    registry = intake.load_registry()
    rows = [r for r in registry["issues"] if r["issue_number"] == n]
    if len(rows) != 1:
        raise ValueError("source issue absent or duplicate")
    issue = api(f"repos/{REPO}/issues/{n}")
    current = api(f"repos/{REPO}/issues/comments/{cid}")
    if (current.get("issue_url") != f"https://api.github.com/repos/{REPO}/issues/{n}"
        or current.get("body") != event["comment"]["body"]):
        raise ValueError("source event superseded or comment misbound")
    comments = api(f"repos/{REPO}/issues/{n}/comments?per_page=100")
    if not isinstance(comments, list) or len(comments) >= 100:
        raise ValueError("comment census incomplete")
    if sum(x.get("id") == cid for x in comments) != 1:
        raise ValueError("event comment absent from live census")
    receipts = []
    for comment in comments:
        if not str(comment.get("body") or "").startswith("RESULT/1"):
            continue
        row, _ = intake.capture({"repository": {"full_name": REPO},
                                 "issue": issue, "comment": comment,
                                 "action": "snapshot"}, registry)
        receipts.append(row)
    evidence = [r for r in receipts if r["comment_id"] == cid]
    if len(evidence) != 1 or evidence[0]["validation"] != "STRUCTURALLY_VALID_UNADJUDICATED":
        raise ValueError(f"invalid incoming return: {[x.get('errors') for x in evidence]}")
    problem = rows[0]["problem_id"]
    report = {"record_type": "ERDOS_CATALOGUE_INTAKE_REPORT",
              "schema_version": "1.0.0", "registry_id": registry["registry_id"],
              "authority_effects": intake.NO_AUTHORITY,
              "source_semantic_adjudication": "NOT_PERFORMED",
              "custody": "BOUND_ONE_ISSUE_LIVE_GITHUB_SNAPSHOT",
              "tasks": [{"issue_number": n, "problem_id": problem,
                         "task_id": intake.assignment(problem),
                         "structurally_valid_returns": sum(
                             x["validation"] == "STRUCTURALLY_VALID_UNADJUDICATED"
                             for x in receipts)}],
              "receipts": receipts}
    selected = project.validate_receipt(report, n)
    if selected["comment_id"] != cid:
        raise ValueError("newly submitted source not selected; review required")
    out.mkdir(parents=True, exist_ok=True)
    raw = json.dumps(report, sort_keys=True, indent=2).encode() + b"\n"
    (out / "REPORT.json").write_bytes(raw)
    bound = {"schema": SCHEMA, "issue": n, "comment_id": cid,
             "comment_sha256": selected["comment_body_sha256"],
             "report_sha256": sha(raw), "head": os.getenv("GITHUB_SHA", ""),
             "run": os.getenv("GITHUB_RUN_ID", ""),
             "mathematical_certification": False}
    (out / "BINDING.json").write_text(json.dumps(bound, indent=2) + "\n")
    return bound


def apply(event_path, out):
    event, n, cid = source_event(event_path)
    bound = json.loads((out / "BINDING.json").read_text())
    raw = (out / "REPORT.json").read_bytes()
    if (bound.get("schema") != SCHEMA or bound.get("issue") != n
        or bound.get("comment_id") != cid
        or bound.get("report_sha256") != sha(raw)
        or bound.get("head") != os.getenv("GITHUB_SHA", "")
        or bound.get("run") != os.getenv("GITHUB_RUN_ID", "")
        or os.getenv("GCL_RETURN_FASTPATH_CONTROL") != "protected-main"
        or not os.getenv("GH_TOKEN")):
        raise ValueError("protected source/report binding failed")
    report = json.loads(raw)
    row = project.validate_receipt(report, n)
    if (row["comment_id"] != cid
        or row["comment_body_sha256"] != bound["comment_sha256"]):
        raise ValueError("selected comment changed")
    receipt, code = project.project_source_returns(
        report, [n], dry_run=False,
        receipt_path=out / "PROJECTION.json",
        report_digest=bound["report_sha256"])
    if code or not receipt.get("verified") or not receipt.get("complete"):
        raise ValueError(f"single-issue projector failed: {receipt.get('blocker')}")
    result = receipt["results"][0]
    if result["target"] == "RETURNED":
        if (result.get("verified_status") != "RETURNED"
            or result.get("verified_gcl_state") != "RETURNED"
            or result.get("available_removed") is not True):
            raise ValueError("incomplete Project, Issue Field, or label readback")
    elif result["target"] == "PRESERVE_DONE":
        if result.get("verified_status") != "Done":
            raise ValueError("historic Done custody not preserved")
    else:
        raise ValueError("unexpected projection target")
    return {"issue": n, "status": "VERIFIED", "source_comment_id": cid,
            "target": result["target"], "source_semantics_accepted": False}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["capture", "apply"])
    parser.add_argument("--event", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    try:
        result = (capture(args.event, args.out) if args.mode == "capture"
                  else apply(args.event, args.out))
    except (RuntimeError, ValueError, KeyError, TypeError, OSError,
            subprocess.CalledProcessError, subprocess.TimeoutExpired) as error:
        blocker = {"schema": SCHEMA, "status": "BLOCKED", "verified": False,
                   "error": f"{type(error).__name__}: {error}"}
        (args.out / "BLOCKER.json").write_text(json.dumps(blocker, indent=2) + "\n")
        print(json.dumps(blocker), file=sys.stderr, flush=True)
        return 1
    print(json.dumps(result, sort_keys=True), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
