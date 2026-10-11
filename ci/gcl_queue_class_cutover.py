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
ROLLING_ROSTER = Path(__file__).resolve().parents[1] / "governance/erdos_catalogue/ROLLING_RESEARCH_024.json"

def protected_rolling_critics() -> dict[int,int]:
    """Exact protected source-semantic critic docket mapping: issue -> Erdős ID."""
    data=json.loads(ROLLING_ROSTER.read_text(encoding="utf-8"))
    if (data.get("record_type")!="GCL_ERDOS_ROLLING_RESEARCH_COHORT"
        or data.get("cohort_id")!="ERDOS-ROLLING-024-001"
        or len(data.get("items") or [])!=24):
        raise ValueError("protected Erdős rolling-24 roster identity/size drift")
    result={}
    for row in data["items"]:
        issue=row.get("source_critical_review_issue")
        problem=row.get("problem_id")
        if not isinstance(issue,int) or not isinstance(problem,int) or issue<=0 or problem<=0 or issue in result:
            raise ValueError("protected source critic docket identity/uniqueness drift")
        result[issue]=problem
    return result


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
    # Exact protected editorial typography inventories, despite source role.
    editorial_source_dockets={1262:"MP-MATH-TYPO-ED07 — ",
                              1264:"MP-MATH-TYPO-ED09 — "}
    if repo=="grandchallenge/MATH-PROGRAMME" and number in editorial_source_dockets:
        if not title.startswith(editorial_source_dockets[number]) or not source:
            raise ValueError(f"{repo}#{number}: editorial typography identity drift")
        return "Editorial",mode
    # Protected ERDOS-ROLLING-024 source-semantic critics are *mathematics*
    # even though they execute by direct issue pickup rather than Solve /claim.
    # The issue number is bound to a problem in the protected cohort registry;
    # both title and SOURCE role must agree with that immutable identity.
    if repo=="grandchallenge/MATH-PROGRAMME":
        roster=protected_rolling_critics()
        if number in roster:
            prefix=f"ERDOS {roster[number]} — critical source and lemma review of "
            if not source or not title.startswith(prefix):
                raise ValueError(f"{repo}#{number}: protected Erdős rolling critic identity drift")
            return "Mathematics",mode
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
    conflicts=[]
    for item in items:
        try:
            cls,mode=classify(item)
        except (ValueError,TypeError,KeyError) as exc:
            conflicts.append(str(exc))
            continue
        expected[cls]+=1
        current=(item.get("fieldValueByName") or {}).get("name")
        if current not in (None,"Editorial","Mathematics"):
            raise ValueError("unrecognized existing Queue Class option")
        if current!=cls:
            corrections.append({"item_id":item["id"],"repo":item["content"]["repository"]["nameWithOwner"],
                                "issue":item["content"]["number"],"was":current,
                                "class":cls,"mode":mode,"option":opts[cls]})
    if conflicts:
        raise ValueError(f"{len(conflicts)} Project item(s) have ambiguous class: " +
                         " | ".join(conflicts[:30]) +
                         (f" (+{len(conflicts)-30} more)" if len(conflicts)>30 else ""))
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



BATCH_SIZE = 10


def update_class_batch(rows: list[dict]) -> None:
    """Use small GraphQL alias groups; verify exact ID for every mutation."""
    if not rows or len(rows) > BATCH_SIZE:
        raise ValueError("invalid Queue Class batch size")
    variables = {"project":PROJECT_ID,"field":QUEUE_FIELD_ID}
    definitions = ["$project:ID!","$field:ID!"]
    fields = []
    seen = set()
    for i, row in enumerate(rows):
        item, option = row["item_id"], row["option"]
        if not isinstance(item,str) or not item.startswith("PVTI_") or item in seen:
            raise ValueError("invalid or duplicate Project item in Queue Class batch")
        if not isinstance(option,str) or not option:
            raise ValueError("missing Queue Class option ID")
        seen.add(item)
        definitions.extend((f"$item{i}:ID!",f"$option{i}:String!"))
        variables[f"item{i}"] = item
        variables[f"option{i}"] = option
        fields.append(
            f"m{i}:updateProjectV2ItemFieldValue(input:{{"
            f"projectId:$project,itemId:$item{i},fieldId:$field,"
            f"value:{{singleSelectOptionId:$option{i}}}"
            "}){projectV2Item{id}}"
        )
    mutation = "mutation("+",".join(definitions)+"){"+ " ".join(fields) +"}"
    result = graphql(mutation,**variables)
    for i, row in enumerate(rows):
        if (result.get(f"m{i}") or {}).get("projectV2Item",{}).get("id") != row["item_id"]:
            raise RuntimeError("Queue Class batch mutation returned incorrect item ID")


def guard_project_api_budget(corrections: int) -> dict:
    """Fail before the first write when the shared Clerk API quota is insufficient."""
    proc = subprocess.run(["gh","api","rate_limit"],capture_output=True,
                          text=True,timeout=40,check=False)
    if proc.returncode:
        raise RuntimeError("Clerk rate-limit preflight unavailable: "+proc.stderr[:280])
    rate = json.loads(proc.stdout).get("resources") or {}
    if not isinstance(rate,dict):
        raise RuntimeError("Clerk rate-limit preflight malformed")
    graphql_budget = (rate.get("graphql") or {}).get("remaining")
    core_budget = (rate.get("core") or {}).get("remaining")
    required_graphql = max(200, ((corrections + BATCH_SIZE-1)//BATCH_SIZE)*2+100)
    if not isinstance(graphql_budget,int) or not isinstance(core_budget,int):
        raise RuntimeError("Clerk API budget unknown: refusal before mutations")
    if graphql_budget < required_graphql or core_budget < 25:
        raise RuntimeError(
            f"Clerk rate budget insufficient before mutations: "
            f"GraphQL {graphql_budget}/{required_graphql} needed, REST {core_budget}/25 needed; "
            "retry after GitHub installation limit resets"
        )
    return {"graphql_remaining":graphql_budget,
            "graphql_minimum":required_graphql,"rest_remaining":core_budget}



def execute(apply:bool, report:Path) -> int:
    if apply and not os.environ.get("GH_TOKEN"):
        raise RuntimeError("--apply requires authenticated short-lived GH_TOKEN")
    # Rate inspection must precede the first full-Project GraphQL query.
    # Once the shared Clerk installation is exhausted, even the read-only
    # 1,000+ item snapshot cannot complete. Do not spend/retry graph reads
    # or partly mutate fields until the installation quota recovers.
    if apply:
        initial_budget = guard_project_api_budget(0)
        print("INITIAL_API_BUDGET",json.dumps(initial_budget,sort_keys=True),flush=True)
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
    # Protect the independent cutover against the shared Clerk installation
    # quota, then use bounded aliases and exact response identity checks.
    budget = guard_project_api_budget(len(changes))
    print("API_BUDGET",json.dumps(budget,sort_keys=True),flush=True)
    for start in range(0,len(changes),BATCH_SIZE):
        update_class_batch(changes[start:start+BATCH_SIZE])
        done=min(start+BATCH_SIZE,len(changes))
        if done%100==0 or done==len(changes):
            print(f"CLASSIFIED {done}/{len(changes)}",flush=True)
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



RECEIPT_MARKER = "<!-- GCL-QUEUE-CLASS-CUTOVER-READBACK/1 -->"


def receipt_message(receipt: dict | None, *, run_url: str, protected_sha: str) -> str:
    """Render a deliberately non-authoritative snapshot, never inferred success."""
    complete = (isinstance(receipt, dict)
                and receipt.get("record_type") == "GCL_QUEUE_CLASS_CUTOVER_RECEIPT"
                and receipt.get("applied") is True
                and receipt.get("dry_run") is False
                and receipt.get("global_available_view_unchanged") is True
                and receipt.get("queue_field") == QUEUE_FIELD_ID
                and isinstance(receipt.get("items"), int)
                and receipt["items"] > 0
                and isinstance(receipt.get("post_readback"), dict)
                and receipt["post_readback"].get("items") == receipt["items"]
                and isinstance(receipt.get("saved_view_ids"), dict)
                and all(receipt["saved_view_ids"].get(k) for k in VIEW_FILTERS)
                and isinstance(receipt.get("classes_expected"), dict)
                and set(receipt["classes_expected"]) == {"Editorial", "Mathematics"}
                and sum(receipt["classes_expected"].values()) == receipt["items"])
    lines = [RECEIPT_MARKER, "# Protected GCL queue-class readback",
             "", "**Project classification:** " + ("VERIFIED" if complete else "BLOCKED / UNVERIFIED"),
             "", "- Protected source SHA: `" + protected_sha + "`",
             "- GitHub Actions run: " + run_url,
             "- Project: https://github.com/orgs/grandchallenge/projects/2"]
    if complete:
        lines.extend([
            "- Project items fully re-read: **" + str(receipt["items"]) + "**",
            "- Classified Editorial: **" + str(receipt["classes_expected"]["Editorial"]) + "**",
            "- Classified Mathematics: **" + str(receipt["classes_expected"]["Mathematics"]) + "**",
            "- Queue Class field: `" + QUEUE_FIELD_ID + "`",
            "- EDITORIAL saved view: `" + str(receipt["saved_view_ids"]["EDITORIAL"]) + "`",
            "- MATHEMATICS saved view: `" + str(receipt["saved_view_ids"]["MATHEMATICS"]) + "`",
            "- Global AVAILABLE view identity preserved: `" + AVAILABLE_VIEW_ID + "`",
            "- Correction candidates at start of this run: " + str(receipt.get("corrections")),
        ])
    else:
        lines.append("- No complete and verified applied Project receipt was available. Inspect the linked run's logs and archived receipt; **do not assert cutover success**.")
        if isinstance(receipt, dict) and receipt.get("blocker"):
            lines.append("- Exact controller blocker: `" + str(receipt["blocker"])[:3000].replace("`", "'") + "`")
    lines.extend(["",
      "This readback does not establish class-specific active-worker capacity enforcement, live two-lane pickup/RESULT/1 replay, chapter acceptance, mathematical certification, or overall cutover closure.",
      "",
      "Cutover authority: https://github.com/grandchallenge/MATHSOLVE/issues/1049"])
    return "\n".join(lines) + "\n"


def publish_readback(report: Path, issue: int) -> int:
    """Upsert one evidence-only comment using the scoped Council Clerk App token."""
    if not os.environ.get("GH_TOKEN"):
        raise RuntimeError("short-lived Council Clerk GH_TOKEN absent")
    if issue != 2563:
        raise ValueError("unexpected queue cutover receipt target")
    receipt = None
    if report.exists():
        receipt = json.loads(report.read_text(encoding="utf-8"))
    run_id = os.environ.get("GITHUB_RUN_ID", "")
    sha = os.environ.get("GITHUB_SHA", "")
    if not run_id.isdecimal() or not re.fullmatch(r"[0-9a-f]{40}", sha):
        raise RuntimeError("GitHub run identity or protected SHA missing")
    body = receipt_message(receipt,
                           run_url=f"https://github.com/{OWNER}/MATH-PROGRAMME/actions/runs/{run_id}",
                           protected_sha=sha)

    def api(*args: str, stdin: str | None = None) -> object:
        result = subprocess.run(["gh", "api", *args], text=True, input=stdin,
                                capture_output=True, timeout=75, check=False)
        if result.returncode:
            raise RuntimeError("receipt GitHub API error: " + result.stderr[:350])
        return json.loads(result.stdout)

    issue_data = api(f"repos/{OWNER}/MATH-PROGRAMME/issues/{issue}")
    if issue_data.get("state") != "open" or issue_data.get("comments", 0) >= 100:
        raise RuntimeError("receipt issue closed or comment list pagination unsafe")
    comments = api(f"repos/{OWNER}/MATH-PROGRAMME/issues/{issue}/comments?per_page=100")
    matches = [entry for entry in comments
               if RECEIPT_MARKER in str(entry.get("body", ""))]
    if len(matches) > 1:
        raise RuntimeError("duplicate controller receipts; refuse overwrite")
    payload = json.dumps({"body":body})
    if matches:
        posted = api("--method", "PATCH",
            f"repos/{OWNER}/MATH-PROGRAMME/issues/comments/{matches[0]['id']}",
            "--input", "-", stdin=payload)
    else:
        posted = api("--method", "POST",
            f"repos/{OWNER}/MATH-PROGRAMME/issues/{issue}/comments",
            "--input", "-", stdin=payload)
    if posted.get("body") != body:
        raise RuntimeError("receipt comment readback mismatch")
    print("RECEIPT_PUBLISHED", "VERIFIED" if "**Project classification:** VERIFIED" in body else "BLOCKED", flush=True)
    return 0


def main() -> int:
    parser=argparse.ArgumentParser()
    parser.add_argument("--apply",action="store_true")
    parser.add_argument("--receipt",type=Path,required=True)
    parser.add_argument("--publish-issue",type=int)
    args=parser.parse_args()
    try:
        if args.publish_issue is not None:
            if args.apply:
                raise ValueError("--publish-issue cannot run with --apply")
            return publish_readback(args.receipt, args.publish_issue)
        return execute(args.apply,args.receipt)
    except (ValueError,RuntimeError,KeyError,TypeError,subprocess.SubprocessError, OSError) as error:
        print("CUTOVER_BLOCKED",str(error),file=sys.stderr,flush=True)
        if args.apply and args.publish_issue is None:
            args.receipt.parent.mkdir(parents=True,exist_ok=True)
            args.receipt.write_text(json.dumps({
                "record_type":"GCL_QUEUE_CLASS_CUTOVER_RECEIPT",
                "applied":False,"dry_run":False,"blocker":str(error),
                "queue_field":QUEUE_FIELD_ID,
                "boundary":"controller failure; no completion asserted"
            },sort_keys=True,indent=2)+"\n",encoding="utf-8")
        return 2


if __name__=="__main__":
    raise SystemExit(main())
