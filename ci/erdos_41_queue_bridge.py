#!/usr/bin/env python3
"""Fail-closed, authenticated Erdős #41 queue preflight and evidence handoff.

No issue-write pathway. The existing protected GCL intake/controller alone decides
whether a RESULT/1 or provisional Forge evidence return is admissible.
"""
import argparse, hashlib, json, os, subprocess
from pathlib import Path

REPO="grandchallenge/MATH-PROGRAMME"
ISSUE=2536
LABELS={"gcl-job","gcl-state:available","gcl-role:source-audit","gcl-pickup:direct-editorial"}
AUTHORITY_KEYS={"source_acceptance","solve_dispatch","mathcert_certification","publication"}
PROVIDER_COMMIT="85f863718beeec7b58a3a1926ee92e3472bc2020"
SOURCE_BLOB="5e9eeb26586d087f4b2ab3d82734ea5ed87ddf50"

def github(endpoint):
    if not os.getenv("GH_TOKEN"):
        raise RuntimeError("GH_TOKEN not configured: authenticated operator required")
    p=subprocess.run(["gh","api","--method","GET",endpoint],text=True,
                     capture_output=True,check=False,timeout=60)
    if p.returncode: raise RuntimeError("GitHub read failed: "+p.stderr[:300])
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
    if not isinstance(comments,list) or len(comments)>=100:
        raise RuntimeError("comment history incomplete: fail closed")
    if any((c.get("body") or "").startswith(("GCL-FORGE-CRITIQUE-CANDIDATE/1\n","GCL-CRITICAL-REVIEW/1\n"))
           for c in comments):
        raise RuntimeError("critical evidence already submitted")
    return {"issue":ISSUE,"state":"AVAILABLE","labels":sorted(labels)}

def validate(path):
    raw=Path(path).read_bytes()
    d=json.loads(raw)
    if d.get("schema")!="GCL-ERDOS-041-DETERMINISTIC-REPLAY/1" or d.get("issue")!=ISSUE or d.get("problem_id")!=41:
        raise ValueError("wrong replay schema/issue")
    if d.get("status")!="PASS_FINITE_SEMANTIC_DIFFERENCE_ONLY":
        raise ValueError("replay failed")
    if (d.get("source_provider_commit")!=PROVIDER_COMMIT or
        d.get("source_provider_git_blob_sha1")!=SOURCE_BLOB or
        d.get("worker_result_comment_id")!=6104193801 or
        d.get("cohort")!="ERDOS-ROLLING-024-001" or
        not isinstance(d.get("roster_sha256"),str) or len(d["roster_sha256"])!=64):
        raise ValueError("source provenance mismatch")
    if (d.get("finite_set")!=[1,2,3] or
        d.get("three_element_subsets")!=[[1,2,3]] or
        [1,1,3] not in d.get("multisets_with_sum_five",[]) or
        [1,2,2] not in d.get("multisets_with_sum_five",[])):
        raise ValueError("missing finite witness")
    if d.get("authority_effects")!={k:False for k in AUTHORITY_KEYS}:
        raise ValueError("authority effect attempted")
    return hashlib.sha256(raw).hexdigest(),d

def main():
    p=argparse.ArgumentParser()
    p.add_argument("action",choices=["preflight"])
    p.add_argument("--evidence",required=True)
    p.add_argument("--out",default="runs/erdos-41/intake-handoff.json")
    args=p.parse_args()
    digest,d=validate(args.evidence)
    queue=preflight()
    handoff={
        "schema":"GCL-ERDOS-041-UNADJUDICATED-HANDOFF/1",
        "queue":queue,"evidence_sha256":digest,
        "roster_sha256":d["roster_sha256"],
        "source_provider_commit":PROVIDER_COMMIT,
        "source_provider_git_blob_sha1":SOURCE_BLOB,
        "worker_result_comment_id":6104193801,
        "candidate_status":"AWAITING_TRUSTED_INTAKE",
        "authority_effects":{k:False for k in AUTHORITY_KEYS}
    }
    target=Path(args.out);target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(handoff,sort_keys=True,indent=2)+"\n")
    print(json.dumps({"preflight":"PASS","handoff":str(target),"evidence_sha256":digest}))
if __name__=="__main__":main()
