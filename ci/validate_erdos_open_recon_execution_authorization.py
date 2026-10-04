#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/"governance"/"erdos_open_recon_execution_authorization.json"
PROBLEMS=["593","595","241","470","1052","99","101","138"]
LANES=["R1","S1","A1"]

def load():
    return json.loads(PATH.read_text(encoding="utf-8"))

def validate(d):
    e=[]
    if d.get("record_type")!="GCL_ERDOS_OPEN_RECON_EXECUTION_AUTHORIZATION":
        e.append("record type drift")
    if d.get("authorization_id")!="ERDOS-OPEN-RECON-AUTH-001":
        e.append("authorization id drift")
    t=d.get("programme_triage",{})
    if t.get("commit")!="fceda552485562bfb6210e520a10d3d62314a6f0" or t.get("triage_id")!="ERDOS-OPEN-TRIAGE-001":
        e.append("triage binding drift")
    p=d.get("protected_solve_pack_set",{})
    if p.get("commit")!="a9ab08f463740ca86fcc0efc082ce9ba5de72c04" or p.get("git_blob_sha1")!="4a594b8ed8f7972548ef5f60f580103062c77643":
        e.append("Solve pack binding drift")
    if d.get("selected_problem_ids")!=PROBLEMS:
        e.append("selected problem set drift")
    expected=[f"ERDOS-{problem}-{lane}" for problem in PROBLEMS for lane in LANES]
    if d.get("authorized_assignment_ids")!=expected:
        e.append("assignment set drift")
    scope=d.get("execution_scope",{})
    required_true=["contributor_execution_authorized_after_protected_solve_lease_binding","issue_binding_required","dispatch_id_required","agent_ref_required","lease_identity_required","immutable_launch_artifact_required"]
    for k in required_true:
        if scope.get(k) is not True: e.append(f"{k} must be true")
    if scope.get("state")!="ACTIVATION_TRANSACTION_AUTHORIZED": e.append("execution state drift")
    if scope.get("lane_timebox_minutes")!=35: e.append("timebox drift")
    if scope.get("return_protocol")!="GCL-CONTRIBUTION-RESULT/1": e.append("return protocol drift")
    s=d.get("synthesis_policy",{})
    if s.get("initial_synthesis_allowed") is not False or s.get("cross_disclosure_before_closure") is not False:
        e.append("blind synthesis boundary weakened")
    a=d.get("authority_boundary",{})
    for k in ["canonical_mathematical_mutation_authorized","theorem_claim_promotion_authorized","certification_authorized","publication_authorized","contributor_repository_mutation_authorized"]:
        if a.get(k) is not False: e.append(f"authority inflation: {k}")
    if a.get("issue_comment_return_only") is not True: e.append("return transport drift")
    return e

def main():
    errors=validate(load())
    if errors: raise SystemExit("\n".join(errors))
    print("ERDOS-OPEN reconnaissance execution authorization valid: 8 problems / 24 lanes")
if __name__=="__main__": main()
