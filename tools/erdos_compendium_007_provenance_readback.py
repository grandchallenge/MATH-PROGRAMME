#!/usr/bin/env python3
"""Live read-only provenance census. Do not equate issue returns with source criticism."""
from __future__ import annotations
from concurrent.futures import ThreadPoolExecutor
import datetime as dt
import hashlib
import json
import re
import subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
COHORT=ROOT/"governance/erdos_compendium/batches/EC-BULK-007.json"
OUT=ROOT/"governance/erdos_compendium/batches/EC-BULK-007_LIVE_PROVENANCE_READBACK_20261017.json"
HOST="repos/grandchallenge/MATH-PROGRAMME/"
def api(path):
    p=subprocess.run(["gh","api",HOST+path],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,timeout=27)
    if p.returncode:raise RuntimeError(f"GH_HTTP {path} ({p.returncode}) {p.stderr[:90]}")
    return json.loads(p.stdout)
def one(item):
    n=item["problem_id"]; issue_id=item["audit_issue"];expect_url=item["source_return"]
    c_id=int(re.search(r"#issuecomment-(\d+)$",expect_url).group(1))
    issue=api("issues/"+str(issue_id));comment=api("issues/comments/"+str(c_id))
    body=issue.get("body") or "";cbody=comment.get("body") or ""
    hashes={"issue_sha256":hashlib.sha256(body.encode()).hexdigest(),
      "comment_sha256":hashlib.sha256(cbody.encode()).hexdigest()}
    conditions={
      "issue_identity":issue.get("number")==issue_id,
      "issue_open":issue.get("state")=="open",
      "issue_body_hash_locked":hashes["issue_sha256"]==item["original_issue_body_sha256"],
      "comment_url_locked":comment.get("html_url")==expect_url,
      "comment_issue_binding":str(comment.get("issue_url","")).endswith("/issues/"+str(issue_id)),
      "valid_assignment":("ASSIGNMENT_ID: ERDOS-CATALOGUE-"+str(n).zfill(4)+"-S01") in cbody,
      "valid_problem":("PROBLEM_ID: "+str(n)) in cbody,
      "result_marker":cbody.startswith("RESULT/1\n"),
      "original_source_link":f"www.erdosproblems.com/{n}" in body,
    }
    return {"problem_id":n,"issue":issue_id,"comment_id":c_id,"author":comment.get("user",{}).get("login"),
    "comment_created_at":comment.get("created_at"),**hashes,"checks":conditions,
    "all_provenance_checks_pass":all(conditions.values()),
    "claim_scope":"ORIGINAL_ISSUE_RETURN_PRESENT__SOURCE_AND_MATH_JUDGMENT_NOT_PERFORMED"}
def main():
    j=json.loads(COHORT.read_text());items=j["items"]
    assert len(items)==168 and len(set(x["problem_id"] for x in items))==168
    with ThreadPoolExecutor(max_workers=8) as executor:
        rows=list(executor.map(one,items))
    passed=sum(r["all_provenance_checks_pass"] for r in rows)
    doc={
      "record_type":"EC_BULK_007_LIVE_PROVENANCE_READBACK/1",
      "observed_utc":dt.datetime.now(dt.timezone.utc).isoformat(),
      "cohort_id":"EC-BULK-007","recorded_manuscripts":len(rows),
      "source_return_provenance_checks_passed":passed,
      "source_return_provenance_checks_failed":len(rows)-passed,
      "qualification":"Does not verify citations, primary source pages, proof statuses or claims; does not count as independent critic approval or protected editorial admission.",
      "records":rows}
    OUT.write_text(json.dumps(doc,indent=2,ensure_ascii=False)+"\n")
    print(json.dumps({"observed_utc":doc["observed_utc"],"passed":passed,
       "failed":[r["problem_id"] for r in rows if not r["all_provenance_checks_pass"]]}))
    if passed !=len(rows):raise SystemExit(3)
if __name__=="__main__":main()
