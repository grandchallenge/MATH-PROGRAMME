#!/usr/bin/env python3
"""Exact-scope, authority-neutral Compendium direct RESULT/1 operational projector.

Reads authenticated issue/comment + organization Issue Fields. This does not
claim worker independence, verify proof/source claims, accept an article, or
permit publication. No /claim or MATHSOLVE reservation is needed.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re

DOCKETS = {
    2556: ("EC-ED02",7,1276),
    2557: ("EC-ED03",9,1278),
    2558: ("EC-ED04",10,1279),
}
REPO = "grandchallenge/MATH-PROGRAMME"
CAMPAIGN = "ERDOS-COMPENDIUM-EDITORIAL-001"
ASSIGNMENT_LABELS = {"gcl-job","gcl-role:constructive","gcl-collab:cooperative",
                     "gcl-pickup:direct-editorial"}
RETURN_FIELDS = {
    "ASSIGNMENT_ID","PROBLEM_ID","DISPOSITION","SOURCE_AUDIT","SOURCE_CLAIMS",
    "EXAMPLE_CHECK","PR_OR_REVIEW","CRITICAL_PASS","GITHUB_RENDER",
    "MKDOCS_RENDER","PUBLIC_HTML","BLOCKERS"
}
DISPOSITIONS = {"DRAFT_PR","REVIEWED","REVISION_REQUIRED","PARTIAL","BLOCKED"}
RENDER = {"PASS","FAIL","UNVERIFIED"}
PUBLIC = {"VERIFIED","PENDING","FAIL"}
AUTH_LOGIN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9-]{0,38}$")
PR_URL = re.compile(r"https://github[.]com/grandchallenge/MATH-PROGRAMME/pull/\d+")
SHA = re.compile(r"\b[0-9a-f]{40}\b")
FIELDS = {"GCL State","GCL Campaign","GCL Role","GCL Collaboration","GCL Phase",
          "GCL Cohort"}


def skip(reason: str) -> dict:
    return {"project":False,"reason":reason,"mathematical_effect":False,
            "editorial_accepted":False,"publication_authorized":False}


def parse_result(body: str) -> dict | None:
    if not isinstance(body,str) or not body.startswith("RESULT/1\n"):
        return None
    values={}
    for line in body.splitlines()[1:]:
        # Source text and explanatory blocks are permitted; required fields
        # must be unambiguous single-line uppercase header entries.
        m=re.match(r"^([A-Z0-9_]+):[ \t]*(.*)$",line)
        if m and m.group(1) in RETURN_FIELDS | {"GITHUB_ACTOR"}:
            if m.group(1) in values:
                return None
            values[m.group(1)] = m.group(2).strip()
    if not RETURN_FIELDS.issubset(values):
        return None
    if any(not values[k] or values[k].startswith("<") for k in RETURN_FIELDS):
        return None
    if values["DISPOSITION"] not in DISPOSITIONS:
        return None
    if values["GITHUB_RENDER"] not in RENDER or values["MKDOCS_RENDER"] not in RENDER:
        return None
    if values["PUBLIC_HTML"] not in PUBLIC:
        return None
    if values["DISPOSITION"] in {"DRAFT_PR","REVIEWED"} and (
        not PR_URL.search(values["PR_OR_REVIEW"]) or
        not SHA.search(values["PR_OR_REVIEW"])):
        return None
    return values


def evaluate(issue: dict, fields: list[dict], comments: list[dict]) -> dict:
    n=issue.get("number")
    if n not in DOCKETS:
        return skip("not_bound_compendium_editorial_issue")
    assignment,problem,source=DOCKETS[n]
    if issue.get("state")!="open" or issue.get("pull_request"):
        return skip("not_open_issue")
    if not str(issue.get("title") or "").startswith(
        f"{assignment} — Erdős #{problem} — "):
        return skip("title_identity_mismatch")
    body=issue.get("body") or ""
    if (f"issues/{source}" not in body or f"issues/2552" not in body):
        return skip("issue_source_or_parent_unbound")
    labels=[x.get("name") for x in issue.get("labels",[]) if isinstance(x,dict)]
    labelset=set(labels)
    if len(labels)!=len(labelset) or not ASSIGNMENT_LABELS.issubset(labelset):
        return skip("missing_or_duplicate_pickup_labels")
    if {x for x in labelset if x.startswith("gcl-pickup:")}!={"gcl-pickup:direct-editorial"}:
        return skip("pickup_mode_mismatch")
    lifecycle={x for x in labelset if x.startswith("gcl-state:")}
    if not lifecycle or not lifecycle.issubset({"gcl-state:available","gcl-state:returned"}):
        return skip("blocked_unknown_or_missing_lifecycle")
    if not isinstance(fields,list) or not isinstance(comments,list) or len(comments)>500:
        return skip("incomplete_issue_fields_or_comment_history")
    actual={}
    for row in fields:
        if not isinstance(row,dict) or row.get("issue_field_name") in actual:
            return skip("duplicate_or_invalid_issue_field")
        option=row.get("single_select_option") or {}
        actual[row.get("issue_field_name")]=option.get("name") or row.get("value")
    expected={"GCL Campaign":CAMPAIGN,"GCL Role":"CONSTRUCTIVE",
              "GCL Collaboration":"COOPERATIVE","GCL Phase":"SHARED",
              "GCL Cohort":"ERDOS-COMPENDIUM-EDITORIAL-TRANCHE-001"}
    if any(actual.get(k)!=v for k,v in expected.items()):
        return skip("protected_campaign_or_role_fields_drift")
    state=actual.get("GCL State")
    if state not in {"AVAILABLE","RETURNED"}:
        return skip("unavailable_or_invalid_state")
    if state=="AVAILABLE" and lifecycle!={"gcl-state:available"}:
        return skip("state_label_disagreement")
    # A prior worker-result event may have written the authoritative RETURNED
    # field and added the RETURNED label before the old AVAILABLE label was
    # removed. Only this exact partial transition is replayable.
    if state=="RETURNED" and lifecycle not in (
        {"gcl-state:available"}, {"gcl-state:returned"},
        {"gcl-state:available","gcl-state:returned"}
    ):
        return skip("returned_state_label_disagreement")
    ids=set()
    valid=[]
    for comment in comments:
        if not isinstance(comment,dict) or not isinstance(comment.get("id"),int):
            return skip("missing_authenticated_comment_id")
        if comment["id"] in ids:
            return skip("duplicate_comment_identity")
        ids.add(comment["id"])
        returned=parse_result(comment.get("body") or "")
        if returned is None:
            continue
        actor=(comment.get("user") or {}).get("login")
        if not isinstance(actor,str) or not AUTH_LOGIN.fullmatch(actor):
            continue
        if (returned["ASSIGNMENT_ID"]!=assignment or
            returned["PROBLEM_ID"]!=str(problem) or
            returned["SOURCE_AUDIT"]!=f"https://github.com/{REPO}/issues/{source}"):
            continue
        if "GITHUB_ACTOR" in returned and returned["GITHUB_ACTOR"].casefold()!=actor.casefold():
            continue
        valid.append((comment["id"],actor,returned))
    if not valid:
        return skip("no_valid_authenticated_bound_RESULT_1")
    valid.sort(key=lambda x:x[0])
    ident,actor,values=valid[0]
    if state=="RETURNED" and lifecycle=={"gcl-state:returned"}:
        return skip("already_returned")
    return {"project":True,"issue_number":n,"comment_id":ident,
            "authenticated_actor":actor,"assignment_id":assignment,
            "self_reported_disposition":values["DISPOSITION"],
            "state_to_write":"RETURNED","repair_incomplete_transition":state=="RETURNED",
            "mathematical_effect":False,"editorial_accepted":False,
            "independent_critic_accepted":False,"publication_authorized":False,
            "requires_solve_reservation":False}


def main() -> None:
    parser=argparse.ArgumentParser()
    parser.add_argument("--issue",type=Path,required=True)
    parser.add_argument("--fields",type=Path,required=True)
    parser.add_argument("--comments",type=Path,required=True)
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()
    result=evaluate(json.loads(args.issue.read_text()),
                    json.loads(args.fields.read_text()),
                    json.loads(args.comments.read_text()))
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n")
    print("COMPENDIUM_DIRECT_RETURN",json.dumps(result,sort_keys=True))


if __name__=="__main__":
    main()
