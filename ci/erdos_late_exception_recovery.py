#!/usr/bin/env python3
"""Issue-scoped Council Clerk exception custody; never source or math acceptance."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
from ci import erdos_catalogue_programme_intake as intake
from ci import erdos_catalogue_queue_projection as project

REPO = "grandchallenge/MATH-PROGRAMME"
BOT = "gcl-council-clerk[bot]"
SCHEMA = "GCL-ERDOS-LATE-EXCEPTION-CUSTODY/1"


def bound_event(path):
    e = json.loads(path.read_text())
    issue, c = e.get("issue") or {}, e.get("comment") or {}
    n, cid, body = issue.get("number"), c.get("id"), c.get("body")
    if not (os.getenv("GITHUB_ACTIONS") == "true"
            and os.getenv("GITHUB_REPOSITORY") == REPO
            and os.getenv("GITHUB_REF") == "refs/heads/main"
            and os.getenv("GITHUB_EVENT_NAME") == "issue_comment"
            and e.get("repository", {}).get("full_name") == REPO
            and e.get("action") in ("created", "edited")
            and type(n) is int and n > 0 and type(cid) is int and cid > 0
            and not issue.get("pull_request")
            and c.get("user", {}).get("login") == BOT
            and isinstance(body, str) and body.startswith("GCL-RETURN-EXCEPTION/1\n")
            and f"\nISSUE: {n}\n" in body
            and "\nREVIEW: REQUIRED, NO SOURCE ACCEPTANCE\n" in body):
        raise ValueError("untrusted or misbound source exception event")
    rows = [x for x in intake.load_registry()["issues"] if x["issue_number"] == n]
    if len(rows) != 1 or f"\nPROBLEM: {rows[0]['problem_id']}\n" not in body:
        raise ValueError("source exception problem identity drift")
    live = project.gh("api", f"repos/{REPO}/issues/comments/{cid}")
    if live.get("issue_url") != f"https://api.github.com/repos/{REPO}/issues/{n}" or live.get("body") != body or live.get("user",{}).get("login") != BOT:
        raise ValueError("live Council Clerk exception mismatch")
    return n, cid, hashlib.sha256(body.encode()).hexdigest()


def run(command, event, out):
    n, cid, digest = bound_event(event)
    out.mkdir(parents=True, exist_ok=True)
    binding = {"schema": SCHEMA, "issue": n, "comment_id": cid,
               "body_sha256": digest, "source_semantics_accepted": False}
    if command == "capture":
        (out/"EXCEPTION_BINDING.json").write_text(json.dumps(binding,indent=2)+"\n")
        return binding
    if json.loads((out/"EXCEPTION_BINDING.json").read_text()) != binding:
        raise ValueError("capture/apply identity drift")
    if os.getenv("GCL_RETURN_FASTPATH_CONTROL") != "protected-main":
        raise ValueError("protected Council Clerk control missing")
    issue = project.gh("api", f"repos/{REPO}/issues/{n}")
    labels = {x["name"] for x in issue["labels"]}
    if not {"gcl-job","gcl-pickup:direct-editorial","gcl-role:source-audit"} <= labels:
        raise ValueError("source issue role or label drift")
    pid,fid,oid = project.project_metadata()
    item = project.issue_project_item(n,pid)
    if issue["state"] == "closed":
        if item["status"] != "Done":
            raise ValueError("closed issue Project state not Done")
        try:
            subprocess.run(["gh","api","--method","PATCH",f"repos/{REPO}/issues/{n}","-f","state=open"],
                           check=True,capture_output=True,text=True,timeout=60)
        except (subprocess.CalledProcessError,subprocess.TimeoutExpired):
            if project.gh("api",f"repos/{REPO}/issues/{n}")["state"] != "open":
                raise
    elif issue["state"] != "open":
        raise ValueError("unrecognized issue state")
    project.apply_returned_project_status(n,pid,item,fid,oid)
    state = project.source_issue_gcl_state(n)
    project.apply_returned_issue_field(n,state)
    project.remove_available_label(n,labels)
    done_issue = project.gh("api",f"repos/{REPO}/issues/{n}")
    done_item = project.issue_project_item(n,pid)
    if (done_issue["state"] != "open" or done_item["status"] != "RETURNED"
            or project.source_issue_gcl_state(n) != "RETURNED"
            or "gcl-state:available" in {x["name"] for x in done_issue["labels"]}):
        raise RuntimeError("exception custody readback not verified")
    receipt = {**binding,"status":"VERIFIED_SOURCE_REVIEW_PENDING",
               "project_status":"RETURNED","issue_state":"open","source_review_complete":False}
    (out/"EXCEPTION_CUSTODY.json").write_text(json.dumps(receipt,indent=2)+"\n")
    return receipt


if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("command",choices=("capture","restore"))
    parser.add_argument("--event",type=Path,required=True)
    parser.add_argument("--out",type=Path,required=True)
    args=parser.parse_args()
    print(json.dumps(run(args.command,args.event,args.out),sort_keys=True))
