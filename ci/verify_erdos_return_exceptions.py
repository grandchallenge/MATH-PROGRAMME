#!/usr/bin/env python3
"""Check exact source-exception partition and authenticated per-issue dispositions."""
import argparse
import hashlib
import json
import os
from pathlib import Path

try:
    from ci import erdos_return_exceptions as ex
    from ci.erdos_catalogue_queue_projection import persist_projection_receipt
except ModuleNotFoundError:
    import erdos_return_exceptions as ex
    from erdos_catalogue_queue_projection import persist_projection_receipt


def verify(report, manifest, digest, root, run, attempt, head):
    expected=ex.manifest(report,16,digest)
    if expected!=manifest:
        raise ValueError("exception manifest and immutable report differ")
    if not (run.isdecimal() and attempt.isdecimal() and len(head)==40):
        raise ValueError("unbound GitHub provenance")
    prefix="gcl-return-exception-batch-"
    names={p.name:p for p in root.iterdir() if p.is_dir()} if root.is_dir() else {}
    expected_names={f"{prefix}{entry['index']}-{run}-{attempt}" for entry in expected["include"]}
    if set(names)!=expected_names:
        raise ValueError("missing, duplicate, or unexpected batch artifacts")
    seen=[]
    counters={"formatted":0,"source_review":0,"competing_review":0,"already_exists":0}
    evidence=[]
    for part in expected["include"]:
        path=names[f"{prefix}{part['index']}-{run}-{attempt}"]/"receipt.json"
        record=json.loads(path.read_text())
        rows=record.get("results")
        if (record.get("schema")!=ex.SCHEMA or record.get("status")!="VERIFIED_BATCH"
            or record.get("verified") is not True or record.get("applied") is not True
            or record.get("report_sha256")!=digest or record.get("protected_head")!=head
            or record.get("run_id")!=run or record.get("batch")!=part
            or record.get("blocker") is not None or record.get("in_flight_issue") is not None
            or not isinstance(rows,list) or [r.get("issue") for r in rows]!=part["issues"]):
            raise ValueError(f"batch {part['index']}: incomplete or unbound readback")
        for r in rows:
            kind=r.get("kind")
            effect=r.get("effect")
            if (kind not in {"MECHANICAL_REPAIR","SOURCE_INTEGRITY","MULTIPLE_VALID"}
                or effect not in {"POSTED","ALREADY_EXISTS"}
                or r.get("readback") is not True
                or type(r.get("posted_comment_id")) is not int
                or len(str(r.get("derived_sha256","")))!=64):
                raise ValueError(f"#{r.get('issue')}: unverified exception disposition")
            if effect=="ALREADY_EXISTS":
                counters["already_exists"]+=1
            if kind=="MECHANICAL_REPAIR":
                counters["formatted"]+=1
            elif kind=="MULTIPLE_VALID":
                counters["competing_review"]+=1
            else:
                counters["source_review"]+=1
        seen+=part["issues"]
        evidence.append({"batch":part["index"],"issue_count":len(rows),
                         "receipt_sha256":hashlib.sha256(path.read_bytes()).hexdigest()})
    if seen!=ex.exceptions(report):
        raise ValueError("exception partition incomplete")
    unresolved=counters["source_review"]+counters["competing_review"]
    return {"schema":"GCL-ERDOS-RETURN-EXCEPTION-AGGREGATE/1",
            "status":"VERIFIED_WITH_SOURCE_REVIEW_PENDING" if unresolved else "VERIFIED",
            "verified":True,"complete":True,"fully_remediated":unresolved==0,
            "claim_scope":"Exception routing and mechanical readbacks only; no mathematical adjudication",
            "report_sha256":digest,"protected_head":head,"run_id":run,
            "issue_count":len(seen),"batch_count":len(evidence),
            "unresolved_source_reviews":unresolved,**counters,"batch_evidence":evidence}


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--report",type=Path,required=True)
    p.add_argument("--manifest",type=Path,required=True)
    p.add_argument("--root",type=Path,required=True)
    p.add_argument("--receipt",type=Path,required=True)
    a=p.parse_args()
    result={"schema":"GCL-ERDOS-RETURN-EXCEPTION-AGGREGATE/1",
            "status":"BLOCKED","verified":False,"complete":False,
            "fully_remediated":False,"blocker":None}
    try:
        raw=a.report.read_bytes()
        result=verify(json.loads(raw),json.loads(a.manifest.read_text()),
                      ex.sha(raw),a.root,os.getenv("GITHUB_RUN_ID",""),
                      os.getenv("GITHUB_RUN_ATTEMPT",""),os.getenv("GITHUB_SHA",""))
    except (ValueError,KeyError,OSError,TypeError) as error:
        result["blocker"]=str(error)
    persist_projection_receipt(a.receipt,result)
    print(json.dumps({k:v for k,v in result.items() if k!="batch_evidence"},sort_keys=True))
    return 0 if result["verified"] else 1


if __name__=="__main__":
    raise SystemExit(main())
