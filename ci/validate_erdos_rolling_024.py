#!/usr/bin/env python3
"""Static fail-closed check of the governed 24-problem rolling Erdős selection."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(p): return json.loads((ROOT/p).read_text(encoding="utf-8"))
def check():
 m=load("governance/erdos_catalogue/ROLLING_RESEARCH_024.json")
 t=load("governance/erdos_open_triage.json")
 b=load("governance/erdos_catalogue/BATCH-001.json")
 r=load("governance/erdos_catalogue/REGISTRY.json")
 items=m["items"]; ids=[e["problem_id"] for e in items]
 expected=b["selection"]["existing_recon_reuse"]+b["selection"]["protected_source_open"]
 assert m["cohort_id"]=="ERDOS-ROLLING-024-001"
 assert m["state"]=="SELECTED_FOR_PREPARATION_NOT_SOLVE_DISPATCHED"
 assert m["size_limit"]==24 and len(items)==len(set(ids))==24 and ids==expected
 assert len([x for x in items if x["worker_result_comment_id"]])==24
 assert len([x for x in items if not x["worker_result_comment_id"]])==0
 assert len([x for x in items if x["source_critical_review_issue"]])==24
 assert not any(m["authority_effects"].values())
 tt={int(x["problem_id"]):x for x in t["entries"]}
 rr={x["problem_id"]:x for x in r["issues"]}
 for pos,x in enumerate(items,1):
  n=x["problem_id"]; tr=tt[n]; reg=rr[n]
  assert x["slot"]==pos and x["catalogue_issue"]==reg["issue_number"]
  assert x["triage_class"]==tr["triage_class"]
  assert tr["registry_status"]["state"]=="open" and tr["protected_fc"]["present"] is True
  assert x["protected_statement"]["path"]==tr["protected_fc"]["path"]
  assert x["protected_statement"]["git_blob_sha1"]==tr["protected_fc"]["git_blob_sha1"]
  assert not any(x["launch_gates"].values())
  assert x["solve_execution_authorized"] is False and x["claimable"] is False
  assert x["certification_authorized"] is False
  assert (x["stage"]=="RETURNED_AWAITING_CRITICAL_SOURCE_REVIEW")==bool(x["worker_result_comment_id"])
  assert not x["source_critical_review_issue"] or x["worker_result_comment_id"]
  assert not x["proposed_target"] or x["worker_result_comment_id"]
 print("ERDOS-ROLLING-024: 24 selected; 24 worker-returned pending review; 0 source-design pending; zero Solve authority")
if __name__=="__main__": check()
