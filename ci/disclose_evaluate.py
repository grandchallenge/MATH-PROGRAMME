"""Bounded offline disclosure evaluator for GCL-DISCLOSE-PR-001."""
from __future__ import annotations
import hashlib,json
from datetime import date
from collections import Counter,defaultdict
from pathlib import Path
from typing import Any


def load(path:Path)->Any:return json.loads(path.read_text(encoding="utf-8"))
def canonical(data:Any)->str:return json.dumps(data,indent=2,sort_keys=True)+"\n"
def digest(path:Path)->str:return hashlib.sha256(path.read_bytes()).hexdigest()
def git_blob(path:Path)->str:
    content=path.read_bytes();return hashlib.sha1(f"blob {len(content)}\0".encode()+content).hexdigest()
def finding(fid:str,status:str,reason:str,subject:str,detail:str)->dict[str,str]:return {"finding_id":fid,"disposition":status,"reason_code":reason,"subject":subject,"detail":detail}

def cyclic(edges:list[dict[str,str]])->bool:
    graph:dict[str,list[str]]=defaultdict(list);nodes:set[str]=set()
    for edge in edges:graph[edge["source"]].append(edge["target"]);nodes.update((edge["source"],edge["target"]))
    state={node:0 for node in nodes}
    def visit(node:str)->bool:
        if state[node]==1:return True
        if state[node]==2:return False
        state[node]=1
        if any(visit(child) for child in graph.get(node,[])):return True
        state[node]=2;return False
    return any(visit(node) for node in sorted(nodes) if state[node]==0)

def evaluate(fixture:Path)->dict[str,Any]:
    manifest=load(fixture/"manifest.json");reviews=load(fixture/manifest["evidence_files"]["reviews"]);head=manifest["candidate"]["head_sha"];evaluated=date.fromisoformat(manifest["evaluation_date"]);out=[]
    for artifact in manifest["artifacts"]:
        fid=f"F-{artifact['artifact_id']}";path=fixture/artifact["path"]
        if not path.is_file():out.append(finding(fid,"FAIL" if artifact["required"] else "ABSTAIN","REQUIRED_EVIDENCE_MISSING" if artifact["required"] else "OPTIONAL_EVIDENCE_MISSING",artifact["artifact_id"],artifact["path"]))
        elif artifact["repository"]!=manifest["candidate"]["repository"] or artifact["commit"]!=head or artifact["subject_head"]!=head:out.append(finding(fid,"FAIL","IDENTITY_DRIFT",artifact["artifact_id"],f"{artifact['repository']}@{artifact['commit']}:{artifact['path']}"))
        elif git_blob(path)!=artifact["blob"]:out.append(finding(fid,"FAIL","BLOB_DRIFT",artifact["artifact_id"],git_blob(path)))
        elif digest(path)!=artifact["expected_sha256"]:out.append(finding(fid,"FAIL","DIGEST_DRIFT",artifact["artifact_id"],digest(path)))
        else:out.append(finding(fid,"PASS","EXACT_ARTIFACT_MATCH",artifact["artifact_id"],digest(path)))
    for case in manifest["classification_cases"]:
        fid=f"F-{case['case_id']}"
        if case["status"]=="missing" or case["disposition"] is None:out.append(finding(fid,"ABSTAIN","CLASSIFICATION_ABSENT",case["case_id"],"no disposition"))
        elif case["subject_head"]!=head:out.append(finding(fid,"FAIL","CLASSIFICATION_HEAD_MISMATCH",case["case_id"],case["subject_head"]))
        elif case["expires_at"] is not None and date.fromisoformat(case["expires_at"])<evaluated:out.append(finding(fid,"FAIL","CLASSIFICATION_EXPIRED",case["case_id"],case["expires_at"]))
        elif case["status"]!="active" or case["superseded_by"] is not None:out.append(finding(fid,"FAIL","CLASSIFICATION_NOT_CURRENT",case["case_id"],case["status"]))
        else:out.append(finding(fid,"PASS","ACTIVE_CLASSIFICATION",case["case_id"],case["disposition"]))
    for case in manifest["hold_cases"]:
        fid=f"F-{case['case_id']}"
        if case["subject_head"]!=head:out.append(finding(fid,"FAIL","HOLD_HEAD_MISMATCH",case["case_id"],case["subject_head"]))
        elif case["status"]=="active" and date.fromisoformat(case["expires_at"])<evaluated:out.append(finding(fid,"FAIL","HOLD_STATUS_EXPIRY_CONTRADICTION",case["case_id"],case["expires_at"]))
        elif case["status"]=="active" and case["used_as_authority"]:out.append(finding(fid,"FAIL","ACTIVE_NO_RELEASE_HOLD",case["case_id"],case["hold_kind"]))
        elif case["status"] in {"expired","superseded"} and case["used_as_authority"]:out.append(finding(fid,"FAIL","STALE_HOLD_USED_AS_AUTHORITY",case["case_id"],case["status"]))
        else:out.append(finding(fid,"PASS","HOLD_NOT_BLOCKING",case["case_id"],case["status"]))
    for case in manifest["attributions"]:
        fid=f"F-{case['attribution_id']}";complete=bool(case["authors"] and case["contributors"]) and (not case["inventor_review_required"] or bool(case["inventors"])) and case["status"]=="complete"
        out.append(finding(fid,"PASS","ATTRIBUTION_COMPLETE",case["attribution_id"],"complete") if complete else finding(fid,"FAIL","ATTRIBUTION_INCOMPLETE",case["attribution_id"],case["status"]))
    for case in manifest["claim_cases"]:
        fid=f"F-{case['case_id']}";public=case["public_text"].lower();matched=sorted(term for term in case["prohibited_terms"] if term.lower() in public)
        if matched and not case["professional_review_present"]:out.append(finding(fid,"FAIL","UNSUPPORTED_IP_LANGUAGE",case["case_id"],",".join(matched)))
        elif case["public_text"]!=case["approved_language"]:out.append(finding(fid,"FAIL","CLAIM_EXCEEDS_APPROVED_LANGUAGE",case["case_id"],case["public_text"]))
        else:out.append(finding(fid,"PASS","APPROVED_CLAIM_EXACT",case["case_id"],case["approved_language"]))
    for case in manifest["confidentiality_cases"]:
        fid=f"F-{case['case_id']}";sensitive=any(case[key] for key in ("contains_confidential_material","contains_credentials","contains_customer_data","contains_unpublished_invention"))
        out.append(finding(fid,"FAIL","CONFIDENTIAL_EXPORT_LEAK",case["case_id"],case["export_surface"]) if sensitive else finding(fid,"PASS","SYNTHETIC_PUBLIC_EXPORT",case["case_id"],case["export_surface"]))
    by_review={r["review_id"]:r for r in reviews["reviews"]}
    exact=by_review["REV-DISCLOSURE-EXACT"]
    if exact["head_sha"]!=head:out.append(finding("F-REVIEW-EXACT","FAIL","REVIEW_HEAD_MISMATCH",exact["review_id"],exact["head_sha"]))
    elif date.fromisoformat(exact["expires_at"])<evaluated:out.append(finding("F-REVIEW-EXACT","FAIL","REVIEW_EXPIRED",exact["review_id"],exact["expires_at"]))
    elif exact["author_account"] or exact["state"]!="APPROVED" or exact["superseded"]:out.append(finding("F-REVIEW-EXACT","FAIL","REVIEW_NOT_CURRENT",exact["review_id"],exact["state"]))
    else:out.append(finding("F-REVIEW-EXACT","PASS","EXACT_NON_AUTHOR_REVIEW",exact["review_id"],exact["reviewer"]))
    mismatch=by_review["REV-DISCLOSURE-MISMATCH"]
    out.append(finding("F-REVIEW-MISMATCH","FAIL","REVIEW_HEAD_MISMATCH",mismatch["review_id"],mismatch["head_sha"]) if mismatch["head_sha"]!=head else finding("F-REVIEW-MISMATCH","PASS","EXACT_NON_AUTHOR_REVIEW",mismatch["review_id"],mismatch["reviewer"]))
    author=by_review["REV-RELEASE-AUTHOR"]
    out.append(finding("F-RELEASE-AUTHOR","FAIL","AUTHOR_ONLY_RELEASE_AUTHORITY",author["review_id"],author["reviewer"]) if author["author_account"] else finding("F-RELEASE-AUTHOR","PASS","NON_AUTHOR_RELEASE_AUTHORITY",author["review_id"],author["reviewer"]))
    out.append(finding("F-AUTHORITY-GRAPH","FAIL","CIRCULAR_RELEASE_AUTHORITY","authority graph","cycle detected") if cyclic(manifest["authority_edges"]) else finding("F-AUTHORITY-GRAPH","PASS","ACYCLIC_RELEASE_AUTHORITY","authority graph",str(len(manifest["authority_edges"]))))
    prior=fixture/manifest["prior_disclosure_evidence"]["path"]
    if not prior.is_file():out.append(finding("F-PRIOR-DISCLOSURE","FAIL" if manifest["prior_disclosure_evidence"]["required"] else "ABSTAIN","REQUIRED_PRIOR_DISCLOSURE_MISSING" if manifest["prior_disclosure_evidence"]["required"] else "PRIOR_DISCLOSURE_EVIDENCE_MISSING","prior disclosure",str(prior.relative_to(fixture))))
    else:out.append(finding("F-PRIOR-DISCLOSURE","PASS","PRIOR_DISCLOSURE_EVIDENCE_PRESENT","prior disclosure",digest(prior)))
    out.sort(key=lambda entry:entry["finding_id"]);counts=Counter(entry["disposition"] for entry in out)
    return {"schema_version":"1.0.0","control_id":"GCL-DISCLOSE-PR-001","fixture_id":manifest["fixture_id"],"candidate":manifest["candidate"],"overall_disposition":"FAIL" if counts["FAIL"] else "ABSTAIN" if counts["ABSTAIN"] else "PASS","summary":{key:counts.get(key,0) for key in ("PASS","FAIL","ABSTAIN")} ,"findings":out,"unresolved_holds":[x["case_id"] for x in manifest["hold_cases"] if x["status"]=="active"],"unsupported_conclusions":["novelty, priority, inventorship, patentability, or freedom to operate","legal validity, export eligibility, or confidentiality obligations","publication merit, customer suitability, or commercial value"],"authority_boundary":{"record_validation_only":True,"actual_release_authorized":False,"professional_review_required":True,"human_release_authority_required":True}}
