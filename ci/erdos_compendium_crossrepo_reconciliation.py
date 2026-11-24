#!/usr/bin/env python3
"""Read-only protected-tree reconciliation; no theorem or publication promotion.

Cross-repository evidence is retained by exact Git object identity. Path matches
are discovery leads, not theorem evidence. Reviewed scope decisions are separately
bound to the exact source blobs and manuscript state.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path

REPOS=("MATH-PROGRAMME","MATHSOLVE","MATHCERT")
IDS=set(range(1,1222))
SHA=re.compile(r"[0-9a-f]{40}")
NAMED=re.compile(r"erd[oőö]s",re.I)
ID_RE=re.compile(r"(?i)erd[oőö]s[-_ ]*#?([0-9]{1,4})(?![0-9])|/E([0-9]{1,4})(?=[A-Z])")
PROGRAMME_PREFIX=re.compile(r"^(?:research/erdos-(\d{1,4})/|experiments/erdos(\d{1,4})[_/-]|governance/erdos_proof_verification/(?:evidence/|manifests/|admissions/|adjudications/|reviews/)(\d{4})(?:/|[_.])|docs/erdos/proof-verification-(\d{4})\.md$|docs/handoffs/ERDOS-(\d{1,4})-)")

def require(ok, why):
    if not ok: raise ValueError(why)

def load_trees(directory):
    result={}
    heads={}
    for repo in REPOS:
        h=json.loads((directory/f"{repo}-head.json").read_text())
        d=json.loads((directory/f"{repo}-tree.json").read_text())
        sha=h["commit"]["sha"]
        require(h.get("protected") is True and SHA.fullmatch(sha),f"{repo}: unprotected/unbound source")
        # REST trees are returned with the actual tree SHA, not the commit SHA.
        require(d.get("sha")==h["commit"]["commit"]["tree"]["sha"],f"{repo}: tree not bound to protected commit")
        require(d.get("truncated") is False and isinstance(d.get("tree"),list),f"{repo}: incomplete tree")
        blobs={}
        for item in d["tree"]:
            if item["type"]!="blob":continue
            p,s=item["path"],item["sha"]
            require(isinstance(p,str) and p not in blobs and SHA.fullmatch(s),f"{repo}: invalid blob")
            blobs[p]=s
        result[repo]=blobs
        heads[repo]=sha
    return heads,result

def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(",",":")).encode()).hexdigest()

def problem_ids(repo,path):
    if repo=="MATH-PROGRAMME":
        m=PROGRAMME_PREFIX.match(path)
        return sorted({int(x) for x in m.groups() if x and int(x) in IDS}) if m else []
    if not NAMED.search(path):return []
    return sorted({int(x) for m in ID_RE.finditer(path) for x in m.groups() if x and int(x) in IDS})

def snapshot(trees):
    by_id={}
    unassigned={}
    counts={}
    for repo in REPOS:
        paths=trees[repo]
        if repo!="MATH-PROGRAMME":
            selected={p:s for p,s in paths.items() if NAMED.search(p)}
            counts[repo]=len(selected)
            unassigned[repo]=[{"path":p,"blob":s} for p,s in sorted(selected.items()) if not problem_ids(repo,p)]
        else:
            selected=paths
        for p,s in sorted(selected.items()):
            for n in problem_ids(repo,p):
                by_id.setdefault(str(n),[]).append({"repository":repo,"path":p,"blob":s})
    return {"named_crossrepo_file_counts":counts,"evidence_by_problem":by_id,"unassigned_named_crossrepo_files":unassigned}

def reconcile(heads,trees,baseline,admissions):
    require(baseline.get("record_type")=="ERDOS_CROSSREPO_RECONCILIATION_BASELINE/1","wrong baseline type")
    now=snapshot(trees)
    old=baseline["inventory"]
    rows=baseline["assessments"]
    reviewed={r["problem_id"]:r for r in rows}
    require(len(reviewed)==len(rows) and set(reviewed)<=IDS,"duplicate/invalid assessments")
    admitted={r["problem_id"] for r in admissions.get("admissions",[])}
    admitted.update(r["problem_id"] for b in admissions.get("batches",[]) for r in b["entries"])
    require(admitted<=IDS,"unexpected editorial ID")
    candidates=[]
    ids=set(map(int,now["evidence_by_problem"]))|set(map(int,old["evidence_by_problem"]))|set(reviewed)
    for n in sorted(ids):
        k=str(n)
        prior=old["evidence_by_problem"].get(k,[])
        current=now["evidence_by_problem"].get(k,[])
        row=reviewed.get(n)
        manuscript=trees["MATH-PROGRAMME"].get(f"governance/erdos_compendium/editorial/{n:04d}.md")
        changed=prior!=current
        anchor_drift=[]
        if row:
            for a in row["anchors"]:
                repo,p=a["repository"],a["path"]
                require(repo in REPOS and SHA.fullmatch(a["blob"]),"invalid baseline anchor")
                if trees[repo].get(p)!=a["blob"]:anchor_drift.append(a)
            editorial_drift=(manuscript!=row["manuscript_blob"] or (n in admitted)!=row["editorially_admitted"])
            state="REASSESS_SOURCE_OR_EDITORIAL_CHANGE" if changed or anchor_drift or editorial_drift else row["editorial_disposition"]
        else:
            editorial_drift=False
            state="UNASSESSED_EVIDENCE_DISCOVERY"
        candidates.append({"problem_id":n,"current_evidence_file_count":len(current),
          "evidence_inventory_changed":changed,"anchor_drift":anchor_drift,
          "editorial_identity_changed":editorial_drift,"editorially_admitted":n in admitted,
          "manuscript_blob":manuscript,"evidence_fingerprint":digest(current),
          "state":state,"publication_authorized":False,"theorem_status_inferred":False})
    return {"record_type":"ERDOS_CROSSREPO_RECONCILIATION/1","protected_heads":heads,
      "named_crossrepo_file_counts":now["named_crossrepo_file_counts"],
      "distinct_path_mapped_problems":len(ids),
      "unassigned_named_crossrepo_counts":{r:len(v) for r,v in now["unassigned_named_crossrepo_files"].items()},
      "shared_or_unassigned_inventory_changed":old["unassigned_named_crossrepo_files"]!=now["unassigned_named_crossrepo_files"],
      "assessed_problem_count":len(reviewed),"review_candidates":candidates,
      "inventory":now,"authority":"READ_ONLY_PATH_IDENTITY_AND_REVIEW_ANCHOR_RECONCILIATION",
      "history_exhaustive":False,"semantic_assessment_automatic":False,"publication_authorized":False}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--trees",type=Path,required=True)
    p.add_argument("--baseline",type=Path,required=True)
    p.add_argument("--admissions",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    heads,trees=load_trees(a.trees)
    d=reconcile(heads,trees,json.loads(a.baseline.read_text()),json.loads(a.admissions.read_text()))
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n")
    print("Cross-repository evidence:",d["named_crossrepo_file_counts"],"assessed",d["assessed_problem_count"])
    for r in d["review_candidates"]:
        if r["state"]!="RECONCILED_EXACT_CERTIFIED_ARTICLE":
            print(f"#{r['problem_id']}: {r['state']}")
if __name__=="__main__":
    main()
