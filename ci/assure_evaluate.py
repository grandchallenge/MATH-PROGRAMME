"""Bounded offline evidence evaluator for GCL-ASSURE-PR-001."""
from __future__ import annotations
import hashlib,json
from collections import Counter,defaultdict
from pathlib import Path
from typing import Any

PROHIBITED={"scientific_truth","novelty","commercial_readiness"}
PRIVATE={"grandchallenge/","MATH-PROGRAMME","MATHFORGE","MATHSOLVE","MATHCERT","AETHER"}

def load(path:Path)->Any:return json.loads(path.read_text(encoding="utf-8"))
def canonical(data:Any)->str:return json.dumps(data,indent=2,sort_keys=True)+"\n"
def digest(path:Path)->str:return hashlib.sha256(path.read_bytes()).hexdigest()
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
    manifest=load(fixture/"manifest.json");workflows=load(fixture/manifest["evidence_files"]["workflows"]);reviews=load(fixture/manifest["evidence_files"]["reviews"]);head=manifest["candidate"]["head_sha"];out=[]
    for artifact in manifest["artifacts"]:
        fid=f"F-{artifact['artifact_id']}";path=fixture/artifact["path"]
        if not path.is_file():out.append(finding(fid,"FAIL" if artifact["required"] else "ABSTAIN","REQUIRED_EVIDENCE_MISSING" if artifact["required"] else "OPTIONAL_EVIDENCE_MISSING",artifact["artifact_id"],artifact["path"]))
        elif artifact["subject_head"]!=head:out.append(finding(fid,"FAIL","HEAD_DRIFT",artifact["artifact_id"],artifact["subject_head"]))
        elif digest(path)!=artifact["expected_sha256"]:out.append(finding(fid,"FAIL","DIGEST_DRIFT",artifact["artifact_id"],digest(path)))
        else:out.append(finding(fid,"PASS","EXACT_ARTIFACT_MATCH",artifact["artifact_id"],digest(path)))
    for run in workflows["runs"]:
        fid=f"F-{run['run_id']}"
        if run["head_sha"]!=head:out.append(finding(fid,"FAIL","HEAD_DRIFT",run["run_id"],run["head_sha"]))
        elif run["conclusion"]!="success":out.append(finding(fid,"FAIL","WORKFLOW_NOT_SUCCESSFUL",run["run_id"],run["conclusion"]))
        elif not run["source_exported"] or not run["jobs"]:out.append(finding(fid,"FAIL","FABRICATED_WORKFLOW_SUCCESS",run["run_id"],"success lacks exported job evidence"))
        elif any(job["conclusion"]!="success" for job in run["jobs"]):out.append(finding(fid,"FAIL","WORKFLOW_JOB_FAILED",run["run_id"],"one or more jobs failed"))
        else:out.append(finding(fid,"PASS","EXPORTED_WORKFLOW_SUCCESS",run["run_id"],str(len(run["jobs"]))))
    mismatched=[r for r in reviews["reviews"] if r["head_sha"]!=head];unresolved=[r for r in reviews["reviews"] if r["state"]=="CHANGES_REQUESTED" and not r["resolved"]];approvals=[r for r in reviews["reviews"] if r["state"]=="APPROVED" and not r["author_account"] and r["head_sha"]==head]
    if mismatched:out.append(finding("F-REVIEW-STATE","FAIL","REVIEW_HEAD_MISMATCH","reviews",str(len(mismatched))))
    elif unresolved:out.append(finding("F-REVIEW-STATE","FAIL","UNRESOLVED_CHANGES_REQUESTED","reviews",str(len(unresolved))))
    elif not approvals:out.append(finding("F-REVIEW-STATE","ABSTAIN","MISSING_NON_AUTHOR_APPROVAL","reviews","0"))
    else:out.append(finding("F-REVIEW-STATE","PASS","NON_AUTHOR_APPROVAL_PRESENT","reviews",str(len(approvals))))
    out.append(finding("F-AUTHORITY-GRAPH","FAIL","CIRCULAR_AUTHORITY","authority graph","cycle detected") if cyclic(manifest["authority_edges"]) else finding("F-AUTHORITY-GRAPH","PASS","ACYCLIC_AUTHORITY_GRAPH","authority graph",str(len(manifest["authority_edges"]))))
    policy=json.dumps(manifest["policy_profile"],sort_keys=True).lower();leaked=sorted(token for token in PRIVATE if token.lower() in policy)
    out.append(finding("F-POLICY-BOUNDARY","FAIL","PRIVATE_POLICY_LEAKAGE","policy profile",",".join(leaked)) if manifest["policy_profile"]["embedded_private_policy"] or leaked else finding("F-POLICY-BOUNDARY","PASS","GENERIC_POLICY_ONLY","policy profile",manifest["policy_profile"]["origin"]))
    out.append(finding("F-PRIVACY-BOUNDARY","FAIL","DISALLOWED_DATA_CLASSIFICATION","privacy",manifest["data_classification"]) if manifest["data_classification"]!="synthetic_public" or any(manifest["privacy"].values()) else finding("F-PRIVACY-BOUNDARY","PASS","SYNTHETIC_PUBLIC_ONLY","privacy",manifest["data_classification"]))
    by_id={entry["finding_id"]:entry for entry in out}
    for claim in manifest["claims"]:
        fid=f"F-CLAIM-{claim['claim_id']}";refs=[by_id.get(ref) for ref in claim["evidence_refs"]]
        if claim["category"] in PROHIBITED:out.append(finding(fid,"ABSTAIN","UNSUPPORTED_CONCLUSION",claim["claim_id"],claim["category"]))
        elif any(ref is None for ref in refs):out.append(finding(fid,"ABSTAIN","UNKNOWN_EVIDENCE_REFERENCE",claim["claim_id"],"missing reference"))
        elif any(ref["disposition"]=="FAIL" for ref in refs):out.append(finding(fid,"FAIL","SUPPORTING_EVIDENCE_FAILED",claim["claim_id"],",".join(claim["evidence_refs"])))
        elif not refs or any(ref["disposition"]=="ABSTAIN" for ref in refs):out.append(finding(fid,"ABSTAIN","SUPPORTING_EVIDENCE_INCOMPLETE",claim["claim_id"],",".join(claim["evidence_refs"])))
        else:out.append(finding(fid,"PASS","EVIDENCE_SUPPORTS_BOUNDED_CLAIM",claim["claim_id"],",".join(claim["evidence_refs"])))
    out.sort(key=lambda entry:entry["finding_id"]);counts=Counter(entry["disposition"] for entry in out)
    return {"schema_version":"1.0.0","control_id":"GCL-ASSURE-PR-001","fixture_id":manifest["fixture_id"],"candidate":manifest["candidate"],"overall_disposition":"FAIL" if counts["FAIL"] else "ABSTAIN" if counts["ABSTAIN"] else "PASS","summary":{key:counts.get(key,0) for key in ("PASS","FAIL","ABSTAIN")},"findings":out,"unsupported_conclusions":["mathematical or scientific truth","novelty, priority, patentability, or freedom to operate","legal or security certification","product-market fit or commercial readiness"],"authority_boundary":{"advisory_dossier_only":True,"certificate_issued":False,"external_use_authorized":False,"expert_review_required":True}}
