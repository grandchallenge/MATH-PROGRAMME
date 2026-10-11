#!/usr/bin/env python3
"""Authenticated, fail-closed Erdős 41 queue preflight and evidence manifest.

Usage: GH_TOKEN=... python ci/erdos_41_queue_bridge.py preflight --evidence runs/erdos-41/finite-replay.json
No writes by default. 'publish' creates an unadjudicated issue comment only.
"""
import argparse, hashlib, json, os, subprocess
from pathlib import Path
REPO="grandchallenge/MATH-PROGRAMME"
ISSUE=2536
LABELS={"gcl-job","gcl-state:available","gcl-role:source-audit","gcl-pickup:direct-editorial"}
def github(endpoint, *, method="GET", body=None):
    if not os.getenv("GH_TOKEN"):
        raise RuntimeError("GH_TOKEN not configured: authenticated operator required")
    argv=["gh","api","--method",method,endpoint]
    if body is not None: argv+=["--input","-"]
    p=subprocess.run(argv,input=json.dumps(body) if body is not None else None,
                     text=True,capture_output=True,check=False,timeout=60)
    if p.returncode: raise RuntimeError("GitHub API failure: "+p.stderr[:400])
    return json.loads(p.stdout)
def preflight():
    issue=github(f"repos/{REPO}/issues/{ISSUE}")
    labels={x["name"] for x in issue["labels"]}
    if issue["state"]!="open" or not LABELS.issubset(labels):
        raise RuntimeError("queue issue not AVAILABLE with required labels")
    fields=github(f"repos/{REPO}/issues/{ISSUE}/issue-field-values")
    vals=[(f.get("single_select_option") or {}).get("name") for f in fields
          if f.get("issue_field_name")=="GCL State"]
    if vals!=["AVAILABLE"]: raise RuntimeError("live GCL State Issue Field is not AVAILABLE")
    comments=github(f"repos/{REPO}/issues/{ISSUE}/comments?per_page=100")
    if len(comments)>=100: raise RuntimeError("pagination needed; fail closed")
    if any((c.get("body") or "").startswith("GCL-FORGE-CRITIQUE-CANDIDATE/1\n") for c in comments):
        raise RuntimeError("candidate evidence already submitted")
    return {"issue":ISSUE,"state":"AVAILABLE","labels":sorted(labels)}
def validate(path):
    raw=Path(path).read_bytes(); d=json.loads(raw)
    if d.get("schema")!="GCL-ERDOS-041-DETERMINISTIC-REPLAY/1" or d.get("issue")!=ISSUE or d.get("problem_id")!=41:
        raise ValueError("wrong replay schema/issue")
    if d.get("status")!="PASS_FINITE_SEMANTIC_DIFFERENCE_ONLY": raise ValueError("replay failed")
    if d.get("multisets_with_sum_five") is None or [1,1,3] not in d["multisets_with_sum_five"] or [1,2,2] not in d["multisets_with_sum_five"]:
        raise ValueError("missing finite witness")
    if not all(v is False for v in d.get("authority_effects",{}).values()) or len(d.get("authority_effects",{}))!=4:
        raise ValueError("authority effect attempted")
    return hashlib.sha256(raw).hexdigest(),d
def main():
    p=argparse.ArgumentParser()
    p.add_argument("action",choices=["preflight","publish"])
    p.add_argument("--evidence",required=True)
    p.add_argument("--allow-publication",action="store_true")
    args=p.parse_args()
    digest,d=validate(args.evidence)
    queue=preflight()
    if args.action=="publish":
        if not args.allow_publication: raise RuntimeError("explicit publication flag required")
        body="GCL-FORGE-CRITIQUE-CANDIDATE/1\nSTATUS: UNADJUDICATED\nPROBLEM_ID: 41\nREVIEW_ISSUE: 2536\nEVIDENCE_SHA256: "+digest+"\nFINITE_RESULT: "+d["status"]+"\nAUTHORITY_EFFECT: NONE\n"
        # This is an unadjudicated, authenticated comment, not a claim or acceptance.
        result=github(f"repos/{REPO}/issues/{ISSUE}/comments",method="POST",body={"body":body})
        print(json.dumps({"published":result.get("html_url"),"evidence_sha256":digest}))
    else:
        print(json.dumps({"preflight":"PASS","queue":queue,"evidence_sha256":digest}))
if __name__=="__main__": main()
