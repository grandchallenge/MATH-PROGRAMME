#!/usr/bin/env python3
"""GCL Project #2 semantic Queue Class correction and saved-view readback.

Runs ONLY with a bounded, authenticated org-Projects-write Council Clerk token.
No repository or Issue Field lifecycle mutation; no claim/lease/release effect.
Dry-run by default. --apply verifies *every* Project item before the first write
and replays the complete 1,000+-item readback after changes.

Semantics: Erdős catalogue source/design audits are Mathematics with
direct_editorial pickup; proper expository writing/reviews are Editorial.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
import os
from pathlib import Path
import re
import subprocess
import sys

OWNER, NUMBER = "grandchallenge", 2
PROJECT_ID = "PVT_kwDOB9Ao_c4Blwur"
QUEUE_FIELD_ID = "PVTSSF_lADOB9Ao_c4BlwurzhlJkjI"
AVAILABLE_VIEW_ID = "PVTV_lADOB9Ao_c4BlwurzgL64bo"
DIRECT = "gcl-pickup:direct-editorial"
SOURCE_ROLE = "gcl-role:source-audit"
ERDOS = re.compile(r"^(?:\[GCL-ERDOS\]\s+)?ERDOS-CATALOGUE-\d{4}-S\d{2}\b")
REPOS = {
    "grandchallenge/MATHSOLVE": "reservation_controlled",
    "grandchallenge/MATH-PROGRAMME": "direct_editorial",
    "grandchallenge/ADAPTIVE-INTELLIGENCE-ATLAS": "direct_editorial",
    "grandchallenge/COMPUTATIONAL-DIFFICULTY-ATLAS": "direct_editorial",
}
VIEW_FILTERS = {
    "EDITORIAL": 'is:open "Queue Class":Editorial',
    "MATHEMATICS": 'is:open "Queue Class":Mathematics',
}

QUERY = """
query($owner:String!,$number:Int!,$after:String){
  organization(login:$owner){
    projectV2(number:$number){
      id
      fields(first:100){
        pageInfo{hasNextPage}
        nodes{... on ProjectV2SingleSelectField{id name options{id name}}}
      }
      views(first:100){
        pageInfo{hasNextPage}
        nodes{id name filter}
      }
      items(first:100,after:$after){
        totalCount
        pageInfo{hasNextPage endCursor}
        nodes{
          id
          content{
            ... on Issue{
              number title state
              repository{nameWithOwner}
              labels(first:100){totalCount nodes{name}}
            }
          }
          fieldValueByName(name:"Queue Class"){
            ... on ProjectV2ItemFieldSingleSelectValue{name optionId}
          }
        }
      }
    }
  }
}
"""

MUTATE_CLASS = """
mutation($project:ID!,$item:ID!,$field:ID!,$option:String!){
  updateProjectV2ItemFieldValue(input:{
    projectId:$project,itemId:$item,fieldId:$field,
    value:{singleSelectOptionId:$option}
  }){projectV2Item{id}}
}
"""
CREATE_VIEW = """
mutation($project:ID!,$name:String!){
  createProjectV2View(input:{projectId:$project,name:$name,layout:TABLE_LAYOUT}){
    projectV2View{id name filter}
  }
}
"""
UPDATE_VIEW = """
mutation($id:ID!,$filter:String!){
  updateProjectV2View(input:{viewId:$id,filter:$filter}){
    projectV2View{id name filter}
  }
}
"""


def graphql(query: str, **variables: object) -> dict:
    payload = json.dumps({"query":query, "variables":variables})
    proc = subprocess.run(["gh","api","graphql","--input","-"],input=payload,
                          capture_output=True,text=True,timeout=90,check=False)
    if proc.returncode:
        raise RuntimeError("Project GraphQL failed: "+proc.stderr[:500])
    response=json.loads(proc.stdout)
    if response.get("errors"):
        raise RuntimeError("Project GraphQL errors: "+str(response["errors"])[:500])
    return response["data"]


def read_full_project() -> tuple[dict,list[dict]]:
    after=None
    all_items=[]
    seen=set()
    total=None
    metadata=None
    while True:
        result=graphql(QUERY,owner=OWNER,number=NUMBER,after=after)
        project=(result.get("organization") or {}).get("projectV2")
        if not project or project.get("id") != PROJECT_ID:
            raise ValueError("Project #2 identity mismatch")
        for name in ("fields","views"):
            if project[name]["pageInfo"]["hasNextPage"]:
                raise ValueError(name+" pagination unsupported; refuse incomplete metadata")
        if metadata is None:
            metadata=project
        elif (project["fields"] != metadata["fields"] or project["views"] != metadata["views"]):
            raise ValueError("Project metadata changed while reading pages")
        block=project["items"]
        if total is None:
            total=block["totalCount"]
        elif total != block["totalCount"]:
            raise ValueError("Project inventory changed while paging")
        for item in block["nodes"]:
            if not item or not item.get("id") or item["id"] in seen:
                raise ValueError("duplicate or missing Project item ID")
            seen.add(item["id"])
            all_items.append(item)
        cursor=block["pageInfo"]["endCursor"]
        if not block["pageInfo"]["hasNextPage"]:
            break
        if not cursor or cursor==after:
            raise ValueError("non-progressing Project pagination")
        after=cursor
    if len(all_items) != total or not all_items:
        raise ValueError(f"incomplete Project inventory {len(all_items)}/{total}")
    return metadata, all_items


def classify(item: dict) -> tuple[str,str]:
    issue=item.get("content") or {}
    repo=(issue.get("repository") or {}).get("nameWithOwner")
    title=issue.get("title")
    number=issue.get("number")
    if repo not in REPOS or not isinstance(number,int) or not isinstance(title,str):
        raise ValueError(f"unrecognized Project content: {repo}#{number}")
    labels=issue.get("labels") or {}
    entries=labels.get("nodes") or []
    if labels.get("totalCount") != len(entries):
        raise ValueError(f"{repo}#{number}: issue labels were truncated")
    names={x.get("name") for x in entries}
    if "gcl-job" not in names:
        raise ValueError(f"{repo}#{number}: non-GCL job in classified Project inventory")
    pickup={x for x in names if isinstance(x,str) and x.startswith("gcl-pickup:")}
    mode=REPOS[repo]
    if mode=="reservation_controlled":
        if pickup:
            raise ValueError(f"{repo}#{number}: conflicting reservation/direct pickup")
        return "Mathematics",mode
    if pickup!={DIRECT}:
        raise ValueError(f"{repo}#{number}: missing/contradictory direct pickup label")
    source=SOURCE_ROLE in names
    tagged=bool(ERDOS.match(title))
    if repo=="grandchallenge/MATH-PROGRAMME" and (source or tagged):
        if not (source and tagged):
            raise ValueError(f"{repo}#{number}: ambiguous mathematics source-audit")
        return "Mathematics",mode
    if source:
        raise ValueError(f"{repo}#{number}: non-catalogue source audit requires adjudicated class")
    return "Editorial",mode


def prepare(project:dict, items:list[dict]) -> tuple[list[dict],dict]:
    fields=[f for f in project["fields"]["nodes"]
            if f and f.get("name")=="Queue Class" and f.get("id")==QUEUE_FIELD_ID]
    if len(fields)!=1:
        raise ValueError("Queue Class identity/field contract drift")
    opts={o["name"]:o["id"] for o in fields[0].get("options",[])}
    if set(opts)!={"Editorial","Mathematics"}:
        raise ValueError("Queue Class options do not match governed two-class contract")
    views={v["name"]:v for v in project["views"]["nodes"] if v}
    if "AVAILABLE" not in views or views["AVAILABLE"]["id"]!=AVAILABLE_VIEW_ID:
        raise ValueError("global AVAILABLE view changed; no mutation")
    if views["AVAILABLE"].get("filter")!='is:open "GCL State":AVAILABLE':
        raise ValueError("global AVAILABLE filter drift")
    for name in VIEW_FILTERS:
        if [v["name"] for v in project["views"]["nodes"] if v].count(name)>1:
            raise ValueError("duplicate "+name+" Project view")
    corrections=[]
    expected=Counter()
    for item in items:
        cls,mode=classify(item)
        expected[cls]+=1
        current=(item.get("fieldValueByName") or {}).get("name")
        if current not in (None,"Editorial","Mathematics"):
            raise ValueError("unrecognized existing Queue Class option")
        if current!=cls:
            corrections.append({"item_id":item["id"],"repo":item["content"]["repository"]["nameWithOwner"],
                                "issue":item["content"]["number"],"was":current,
                                "class":cls,"mode":mode,"option":opts[cls]})
    return corrections, {"items":len(items),"classes_expected":dict(expected),
                         "corrections":len(corrections),"views":views}


def reconcile_views(project:dict, *, apply:bool) -> None:
    views={v["name"]:v for v in project["views"]["nodes"] if v}
    for name, filt in VIEW_FILTERS.items():
        v=views.get(name)
        if not apply:
            print("VIEW",name,"existing" if v else "missing",
                  "filter",v.get("filter") if v else "MISSING",flush=True)
            continue
        if v is None:
            created=graphql(CREATE_VIEW,project=PROJECT_ID,name=name)
            v=created["createProjectV2View"]["projectV2View"]
        if v.get("filter")!=filt:
            result=graphql(UPDATE_VIEW,id=v["id"],filter=filt)
            updated=result["updateProjectV2View"]["projectV2View"]
            if updated["name"]!=name or updated["filter"]!=filt:
                raise RuntimeError("Project view mutation readback failed: "+name)


def execute(apply:bool, report:Path) -> int:
    if apply and not os.environ.get("GH_TOKEN"):
        raise RuntimeError("--apply requires authenticated short-lived GH_TOKEN")
    project,items=read_full_project()
    changes,summary=prepare(project,items)
    receipt={"record_type":"GCL_QUEUE_CLASS_CUTOVER_RECEIPT",
             "project":f"https://github.com/orgs/{OWNER}/projects/{NUMBER}",
             "queue_field":QUEUE_FIELD_ID,**summary,
             "dry_run":not apply,"applied":False,
             "sample_corrections":changes[:20],
             "boundary":"classification and view presentation only; no lease or mathematical authority"}
    report.parent.mkdir(parents=True,exist_ok=True)
    report.write_text(json.dumps(receipt,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("PRECHECK",json.dumps(summary,default=str),flush=True)
    if not apply:
        reconcile_views(project,apply=False)
        return 0
    # All items and both classes were checked before the first mutation.
    for i,c in enumerate(changes,1):
        result=graphql(MUTATE_CLASS,project=PROJECT_ID,item=c["item_id"],
                       field=QUEUE_FIELD_ID,option=c["option"])
        if result["updateProjectV2ItemFieldValue"]["projectV2Item"]["id"]!=c["item_id"]:
            raise RuntimeError("mutation identity mismatch")
        if i%100==0:
            print(f"CLASSIFIED {i}/{len(changes)}",flush=True)
    # Reread and refuse to claim success on stale or partial pagination.
    checked,rows=read_full_project()
    pending,recheck=prepare(checked,rows)
    if pending:
        raise RuntimeError(f"{len(pending)} Queue Class values failed complete readback")
    reconcile_views(checked,apply=True)
    final,rows=read_full_project()
    remaining,result=prepare(final,rows)
    if remaining:
        raise RuntimeError("post-view Project classification drift")
    view_map=result["views"]
    for name,filt in VIEW_FILTERS.items():
        view=view_map.get(name)
        if not view or view.get("filter")!=filt:
            raise RuntimeError("missing class view readback "+name)
    receipt.update({"applied":True,"dry_run":False,"post_readback":result,
                    "saved_view_ids":{name:view_map[name]["id"] for name in VIEW_FILTERS},
                    "global_available_view_unchanged":True})
    report.write_text(json.dumps(receipt,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("PASS",json.dumps({k:receipt[k] for k in ("applied","items","classes_expected","saved_view_ids")}),flush=True)
    return 0


def main() -> int:
    parser=argparse.ArgumentParser()
    parser.add_argument("--apply",action="store_true")
    parser.add_argument("--receipt",type=Path,required=True)
    args=parser.parse_args()
    try:
        return execute(args.apply,args.receipt)
    except (ValueError,RuntimeError,KeyError,TypeError,subprocess.SubprocessError, OSError) as error:
        print("CUTOVER_BLOCKED",str(error),file=sys.stderr,flush=True)
        return 2


if __name__=="__main__":
    raise SystemExit(main())
