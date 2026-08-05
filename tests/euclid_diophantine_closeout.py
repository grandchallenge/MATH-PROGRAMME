#!/usr/bin/env python3
"""Fail-closed validator for the EUCLID-DIOPHANTINE-E2E-002 Programme closeout."""
from __future__ import annotations
import json
from pathlib import Path
from typing import Any
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "governance" / "euclid_diophantine_e2e_002_closeout.json"
SCHEMA = ROOT / "schemas" / "euclid_diophantine_e2e_002_closeout.schema.json"
PAGE = ROOT / "docs" / "EUCLID_DIOPHANTINE_E2E_002_PROOF_TRACE.md"

EXPECTED = {
"programme_base":"183ff2a0adfbe5bd0ffd5f2e638089b94b868c54",
"stage1_output":"36c62434dbd19719d990e71ddc23729f0614ace7",
"forge_merge":"af5398a05f17789a061ab0d23c2b47f0cc952fff",
"forge_package":"e89d5b7c611aaa4a7fdea716742e993eaa283da1",
"forge_manifest":"de9dae12cd578ee98b58e6fc1b39365f8c1e7109",
"solve_merge":"66d54d375ae4dfc148888325b6093818669e7c02",
"solve_candidate":"74703b449fa861b72be1eaf89fb1c39a943183ce",
"solve_producer":"5f4ffaf644da47cecd50fd3013a6412eb90ca555",
"solve_handoff":"80a4bf5082ac9ed9459a1dbd7dbb77166e84764e",
"solve_manifest":"d4c3ced7eb3bbf4c3d865a847f9b701cf677cdf4",
"solve_overlay":"2be21dc20a3bb8e39ed4302d4bff6ee7ebab0aa3",
"cert_merge":"cd69013cf55d4ee96539d28ee27eadef64cca06f",
"cert_output":"60bfb86980ef7c3b797b55c4932e469bfea767e5",
"cert_route":"5dbf98b0570f4c55b8cb6c30da168ac0cec18393",
"cert_checker":"25cb866b9d6f3202f4a01359a0a562645145999b",
"cert_tests":"55bf83c82f621d2aca8b6bb556e12ae5eae33a25",
"cert_lean":"bd33d96f851f4079560492364fa0dcadcc06ec3b"}
CLAIMS={f"EUCLID-DIOPHANTINE-E2E-002-C00{i}" for i in range(1,5)}
TOKENS=("21 = -2 * 252 + 5 * 105","84 = 4 * 21","84 = -8 * 252 + 20 * 105","20 = 0 * 21 + 20","0 < 20 < 21","linearDiophantine_iff_gcdDvdNatAbs","noDiophantine25210520","CERTIFIED_LINEAR_DIOPHANTINE_EQUIVALENCE_AND_BOUNDED_EXEMPLARS",EXPECTED["forge_merge"],EXPECTED["solve_merge"],EXPECTED["cert_merge"],"does **not** establish","Stage 3 still requires exact historical source acquisition")

def load_json(path:Path)->Any: return json.loads(path.read_text(encoding="utf-8"))

def semantic_errors(data:Any,page:str)->list[str]:
    e=[]
    if not isinstance(data,dict): return ["closeout record must be an object"]
    p=data.get("programme",{})
    if p.get("protected_base")!=EXPECTED["programme_base"]: e.append("Programme protected-base identity drift")
    if p.get("authority_state")!="candidate_programme_closeout_pending_exact_head_review_and_protected_merge": e.append("candidate closeout authority state drift")
    s1=data.get("protected_stage1",{})
    if s1.get("certification_output",{}).get("git_blob_sha1")!=EXPECTED["stage1_output"]: e.append("protected Stage 1 output identity drift")
    b=s1.get("bezout_spine",{})
    if (b.get("a"),b.get("b"),b.get("d"),b.get("x"),b.get("y"))!=(252,105,21,-2,5): e.append("protected Stage 1 Bézout spine drift")
    if s1.get("reuse_only_no_competing_gcd_definition") is not True: e.append("Stage 1 reuse-only boundary drift")
    for k,expected in (("forge",EXPECTED["forge_merge"]),("solve",EXPECTED["solve_merge"]),("cert",EXPECTED["cert_merge"])):
        s=data.get(k,{})
        if s.get("merge_commit")!=expected: e.append(f"{k} merge identity drift")
        if s.get("merge_parents")!=[s.get("protected_base"),s.get("reviewed_head")]: e.append(f"{k} merge-parent binding drift")
        r=s.get("independent_review",{})
        if r.get("reviewer")!="jimsteeg" or r.get("state")!="APPROVED": e.append(f"{k} independent review boundary drift")
        if not s.get("human_steward",{}).get("disposition","").startswith("HUMAN_STEWARD_AUTHORIZED_EXACT_HEAD_"): e.append(f"{k} Human Steward disposition drift")
        if any(not isinstance(v,int) or v<=0 for v in s.get("exact_head_workflows",{}).values()): e.append(f"{k} exact-head workflow identity invalid")
        if any(not isinstance(v,int) or v<=0 for v in s.get("protected_main_workflows",{}).values()): e.append(f"{k} protected-main workflow identity invalid")
    solve=data.get("solve",{}); cert=data.get("cert",{})
    if solve.get("disposition")!="SOLUTION_WITNESS_AND_DIVISIBILITY_OBSTRUCTION_READY_FOR_CERTIFICATION": e.append("Solve disposition drift")
    if cert.get("disposition")!="CERTIFIED_LINEAR_DIOPHANTINE_EQUIVALENCE_AND_BOUNDED_EXEMPLARS": e.append("Cert disposition drift")
    actual={
      "forge_package":data.get("forge",{}).get("artifacts",{}).get("forge_package",{}).get("git_blob_sha1"),
      "forge_manifest":data.get("forge",{}).get("artifacts",{}).get("provider_manifest",{}).get("git_blob_sha1"),
      "solve_candidate":solve.get("artifacts",{}).get("candidate",{}).get("git_blob_sha1"),
      "solve_producer":solve.get("artifacts",{}).get("producer",{}).get("git_blob_sha1"),
      "solve_handoff":solve.get("artifacts",{}).get("handoff",{}).get("git_blob_sha1"),
      "solve_manifest":solve.get("artifacts",{}).get("campaign_manifest",{}).get("git_blob_sha1"),
      "solve_overlay":solve.get("artifacts",{}).get("route_overlay",{}).get("git_blob_sha1"),
      "cert_output":cert.get("artifacts",{}).get("certification_output",{}).get("git_blob_sha1"),
      "cert_route":cert.get("artifacts",{}).get("route_overlay",{}).get("git_blob_sha1"),
      "cert_checker":cert.get("artifacts",{}).get("independent_checker",{}).get("git_blob_sha1"),
      "cert_tests":cert.get("artifacts",{}).get("adversarial_tests",{}).get("git_blob_sha1"),
      "cert_lean":cert.get("artifacts",{}).get("lean_theorem",{}).get("git_blob_sha1")}
    for k,v in actual.items():
        if v!=EXPECTED[k]: e.append(f"{k} artifact identity drift")
    ids=[x.get("claim_id") for x in data.get("certified_claims",[]) if isinstance(x,dict)]
    if set(ids)!=CLAIMS or len(ids)!=len(CLAIMS): e.append("certified claim membership drift")
    pos=data.get("canonical_instances",{}).get("positive",{}); w=pos.get("witness",{})
    if (pos.get("a"),pos.get("b"),pos.get("c"),pos.get("d"),pos.get("scale"))!=(252,105,84,21,4): e.append("positive instance drift")
    if w.get("x")*252+w.get("y")*105!=84: e.append("constructive witness equation is false")
    if pos.get("scale")*pos.get("d")!=pos.get("c"): e.append("constructive scale factor is false")
    neg=data.get("canonical_instances",{}).get("negative",{}); div=neg.get("division",{})
    q,r,d,c=div.get("quotient"),div.get("remainder"),neg.get("d"),neg.get("c")
    if (neg.get("a"),neg.get("b"),c,d,q,r)!=(252,105,20,21,0,20): e.append("negative instance drift")
    elif c!=q*d+r or not (0<r<d): e.append("divisibility obstruction is malformed")
    if any(v is not False for v in data.get("boundaries",{}).values()): e.append("one or more non-inflation boundaries became active")
    expected_gate="blocked_until_this_closeout_is_independently_approved_human_steward_authorized_protected_merged_read_back_and_exact_historical_source_lock_is_completed"
    if data.get("successor_gates",{}).get("book_vii_microcampaign")!=expected_gate: e.append("Book VII source-lock gate drift")
    if data.get("protected_effect")!="none_until_exact_head_review_human_steward_disposition_protected_merge_post_merge_checks_and_publication": e.append("protected-effect boundary drift")
    for t in TOKENS:
        if t not in page: e.append(f"public proof trace is missing required token: {t}")
    return e

def validate(record_path:Path=RECORD,schema_path:Path=SCHEMA,page_path:Path=PAGE)->list[str]:
    data=load_json(record_path); schema=load_json(schema_path)
    e=[f"{x.json_path}: {x.message}" for x in sorted(Draft202012Validator(schema).iter_errors(data),key=lambda x:list(x.path))]
    if not page_path.is_file(): return e+["public proof trace file is missing"]
    return e+semantic_errors(data,page_path.read_text(encoding="utf-8"))

def main()->int:
    e=validate()
    if e:
        print("\n".join(e)); print(f"EUCLID-DIOPHANTINE-E2E-002 Programme closeout failed with {len(e)} error(s)"); return 1
    print("validated Stage 1 reuse, exact cross-pillar receipts, constructive witness, divisibility obstruction, and Stage 3 source-lock gate"); return 0
if __name__=="__main__": raise SystemExit(main())
