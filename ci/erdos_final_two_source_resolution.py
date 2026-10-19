#!/usr/bin/env python3
"""Council Clerk source-only resolution of Erdős #14/#41 after protected replay."""
import argparse,hashlib,json,os
from pathlib import Path
from ci import erdos_three_source_resolution as c
ROOT=Path(__file__).resolve().parents[1]
PREFIX="GCL-CRITICAL-SOURCE-RESOLUTION/FINAL-TWO/1"
AXIOMS={"propext","Quot.sound","Classical.choice"}
T={
 2522:dict(problem=14,child=2702,review=6142586862,result=6248804789,readback=6248985841,
           pr=2760,merge="ab14758464acb18d8ff9dcaf427831ed29c8a45e",
           file="Erdos14HistoricalTaskTargetParity.lean",receipt="ERDOS_014_KERNEL_REPLAY_RECEIPT.json",
           sha="2dc6778835adb8c2052d183f7ce98b79a93630e42dfdb968d9435bbfcce7d47d"),
 2536:dict(problem=41,child=2703,review=6123841627,result=6248565053,readback=6248985537,
           pr=2759,merge="65b85aa7e8ddff98f6af38c8f04542f582bf8370",
           file="Erdos41HistoricalMathlibBridge.lean",receipt="ERDOS41_HISTORICAL_MATHLIB_BRIDGE.json",
           sha="66f82861886a78102e49e02a2092dcc48729317acfdd0977a2cd42504bd0ec49")
}
class GateError(c.CouncilError):pass
def demand(ok,why):
 if not ok:raise GateError(why)
def check_material(n,data,src):
 s=T[n]
 demand(hashlib.sha256(src).hexdigest()==s["sha"],"source bytes drift")
 demand(data.get("assignment_issue")==s["child"] and data.get("parent_review_issue")==n and
        data.get("catalogue_issue")==1269+s["problem"] and data.get("programme_issue")==2503,"issue linkage drift")
 if n==2522:
  demand(data.get("record_type")=="GCL_ERDOS_014_EXACT_LEAN_REPLAY_V1","wrong replay receipt")
  demand(data.get("credited_external_solver")=="JenW1N" and data.get("gcl_discovered_proof") is False,"solver credit drift")
  demand(data.get("reconstructed_source_repository",{}).get("derived_commit_sha1")=="8432eac998110a563e03df65a28c117e97c8c142","historical task drift")
  rows=data.get("replayed_submissions",[])
  expect={"i":("01f4b21faa141073550ace4791e41bb283bad80fb700e8965387588dc9238029","496840684dd5dc4f0747bf4732ee4fe246340353f8a11aae00bde325fa100ca5"),
          "ii":("92676249a3598e8a654641b6d8078ed91bb3b00db116143e5a586cd63e1e6b20","188ebf8bdf3a04694155ddf3e2d87c64f53d545781cfda7b63e21d6b1434cd74")}
  demand(len(rows)==2 and {r.get("part") for r in rows}=={"i","ii"},"part inventory drift")
  for r in rows:
   typ,src_hash=expect[r["part"]]
   demand(r.get("source_type_sha256_expected")==r.get("source_type_sha256_recomputed")==typ and
          r.get("submission_sha256")==src_hash,"task/submission hash drift")
   demand(r.get("kernel_exit_code")==0 and r.get("kernel_trust_level")==0 and
          set(r.get("transitive_axioms",[]))<=AXIOMS,"untrusted replay")
   for key in ("independent_gcl_kernel_replay","defeq_intended_challenge_target","static_policy_valid"):
    demand(r.get(key) is True,"unverified "+key)
   for key in ("depends_on_sorryAx","value_has_sorry","type_has_sorry",
               "depends_on_forbidden_source_theorem","defeq_hostile_altered_target"):
    demand(r.get(key) is False,"forbidden "+key)
  demand(data.get("authority_effects",{}).get("gcl_math_certification") is False and
         data.get("authority_effects",{}).get("revision_clearance_authorized") is False,"illicit child authority")
 else:
  demand(data.get("record_type")=="GCL_ERDOS_041_HISTORICAL_MATHLIB_BRIDGE_V1","wrong predicate receipt")
  demand(data.get("source_sha256")==s["sha"] and data.get("sorry_count")==0 and data.get("exit_code")==0,"bridge replay mismatch")
  demand(data.get("frozen_provider_blob_sha1")=="5e9eeb26586d087f4b2ab3d82734ea5ed87ddf50" and
         data.get("refreshed_provider_blob_sha1")=="2a1bd1f521325e36aaaf50a3a3feffc9c426aaf6","provider drift")
  demand(data.get("primary_1980_survey_pdf_sha256")=="e2280c6cbba6bfecedb5c5134ce827c59695dccd7f3377d42658cbc30b8db3cf","primary source drift")
  demand(data.get("imported_mathlib_finset_multiset_comparison_complete") is True and
         data.get("historical_theorem_specification",{}).get("historical_variant_name")=="erdos_41.variants.historical_b3","predicate comparison absent")
  theorems=data.get("kernel_proved_theorems",{})
  for name in ("historical_implies_fixed","modern_implies_fixed",
               "exists_infinite_historicalB3_not_modernB3","exists_infinite_modernB3_not_historicalB3"):
   demand(name in theorems and set(theorems[name].get("axioms",[]))<=AXIOMS,"nonstandard or missing "+name)
  demand(all(data.get(k) is False for k in
         ("mathematical_conjecture_solved","mathcert_claimed","solve_dispatch","revision_clearance_authorized")),"illicit source claim")
 return {"issue":n,"sha":s["sha"],"source_only":True}
def material(n):
 s=T[n]; p=ROOT/"governance/source_erdos_critical_005"
 return check_material(n,json.loads((p/s["receipt"]).read_text()),(p/s["file"]).read_bytes())
def snapshot(n):
 s=T[n]; state=c.issue_snapshot(n)
 cm=c.comments(n)
 original=[x for x in cm if x.get("id")==s["review"] and
           (x.get("body") or "").startswith("GCL-CRITICAL-REVIEW/1\n") and
           "DISPOSITION: REVISE" in (x.get("body") or "")]
 demand(len(original)==1,"original REVISE review changed")
 children=c.comments(s["child"])
 demand(any(x.get("id")==s["result"] and (x.get("body") or "").startswith("RESULT/1") for x in children),"authenticated child RESULT missing")
 demand(any(x.get("id")==s["readback"] and (x.get("body") or "").startswith("EVIDENCE_REVIEW/1") for x in children),"terminal child readback missing")
 notes=[x for x in cm if (x.get("body") or "").startswith(PREFIX+"\n")]
 demand(len(notes)<=1,"duplicated Council Clerk resolution")
 if notes:
  note=notes[0]
  demand((note.get("user") or {}).get("login")=="gcl-council-clerk[bot]" and
         s["sha"] in note.get("body","") and s["merge"] in note.get("body",""),"resolution absent App provenance or material identity")
  demand(state["corrected"] or state["revise"],"invalid label state")
 else:
  demand(state["revise"] and not state["corrected"],"unapproved label transition")
 return {"issue":n,"problem":s["problem"],"already_resolved":bool(notes),"state":state}
def preflight():
 rows=[]
 for n,s in T.items():
  material(n)
  pr=json.loads(c.execute("pr","view",str(s["pr"]),"-R",c.REPO,"--json","state,mergeCommit"))
  demand(pr.get("state")=="MERGED" and (pr.get("mergeCommit") or {}).get("oid")==s["merge"],"protected PR merge mismatch")
  rows.append(snapshot(n))
 demand(len(rows)==2,"unexpected Council source scope")
 return rows
def apply(rows):
 demand(os.environ.get("GITHUB_ACTIONS")=="true" and
        os.environ.get("GITHUB_REF")=="refs/heads/main" and
        os.environ.get("GCL_CONTROLLER_ID")=="erdos-final-two-source-resolution" and
        bool(os.environ.get("GH_TOKEN")),"protected main restricted Council Clerk required")
 c.verify_installation_scope()
 for row in rows:
  n=row["issue"];s=T[n]
  if not row["already_resolved"]:
   body=(PREFIX+"\nERDOS_PROBLEM: "+str(s["problem"])+
         "\nREVIEW_ISSUE: #"+str(n)+"\nDISPOSITION: SOURCE_CORRECTION_ACCEPTED"+
         "\nPROTECTED_SOURCE_LOCK_PR: https://github.com/grandchallenge/MATH-PROGRAMME/pull/"+str(s["pr"])+
         "\nPROTECTED_MERGE_COMMIT: "+s["merge"]+"\nLEAN_SOURCE_SHA256: "+s["sha"]+
         "\nSOURCE_ROLE_ONLY: TRUE\nMATHEMATICAL_CERTIFICATION: FALSE"+
         "\nOPEN_PROBLEM_STATUS: UNCHANGED\nORIGINAL_RESULT_CUSTODY: RETURNED"+
         "\nISSUE_STATE: OPEN\nORIGINAL_EXTERNAL_PROVER_CREDIT_PRESERVED: TRUE"+
         "\nThe protected controller checked the exact child return and review, immutable source bytes, previously reported Lean replay receipt and exact protected merge; it did not perform a new kernel run.\n")
   path=ROOT/"artifacts/erdos-final-two-source-resolution"/f"issue-{n}.md"
   path.parent.mkdir(parents=True,exist_ok=True);path.write_text(body)
   c.execute("issue","comment",str(n),"-R",c.REPO,"--body-file",str(path))
  fresh=snapshot(n)
  demand(fresh["already_resolved"],"no protected App note")
  if fresh["state"]["revise"]:
   c.execute("issue","edit",str(n),"-R",c.REPO,"--add-label",c.CORRECTED,"--remove-label",c.REVISE)
  final=snapshot(n)
  demand(final["state"]["corrected"] and not final["state"]["revise"] and final["state"]["state"]=="OPEN","terminal readback failed")
 return True
def main():
 p=argparse.ArgumentParser();p.add_argument("--apply",action="store_true");p.add_argument("--receipt",required=True)
 a=p.parse_args()
 dest=ROOT/a.receipt;dest.parent.mkdir(parents=True,exist_ok=True)
 report={"record_type":"GCL_ERDOS_FINAL_TWO_COUNCIL/1","source_only":True,
         "mathematical_certification":False,"applied":False,"results":[],"error":None}
 try:
  rows=preflight();report["results"]=rows
  if a.apply:
   apply(rows);report["results"]=preflight()
   demand(all(x["already_resolved"] and x["state"]["corrected"] and not x["state"]["revise"]
              for x in report["results"]),"not terminal")
   report["applied"]=True
 except Exception as exc:
  report["error"]=str(exc);dest.write_text(json.dumps(report,indent=2)+"\n");raise
 dest.write_text(json.dumps(report,indent=2)+"\n")
 print(json.dumps({"applied":report["applied"],"items":[x["issue"] for x in report["results"]]}))
if __name__=="__main__":main()
