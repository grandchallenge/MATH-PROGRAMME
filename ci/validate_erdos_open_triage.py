#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/"governance"/"erdos_open_triage.json"
EXPECTED={
    "ACTIVE_EXISTING_CAMPAIGN":1,
    "HOLD_STATUS_RECONCILIATION":4,
    "FIRST_RECONNAISSANCE_TRANCHE":8,
    "CROSS_CAMPAIGN_SYNERGY_ONLY":1,
    "DEFER_UNTIL_NEW_MECHANISM":6,
    "PROTECTED_READY_BACKLOG":280,
    "FORMAL_SOURCE_REFRESH_REQUIRED":58,
    "STATEMENT_CAPTURE_REQUIRED":235,
}
FIRST={"593","595","241","470","1052","99","101","138"}
HELD={"390","522","550","1112"}
PARK={"20","28","52","89","564","1135"}

def load():
    return json.loads(PATH.read_text(encoding="utf-8"))

def validate(data):
    errors=[]
    if data.get("record_type")!="GCL_ERDOS_OPEN_PROGRAMME_TRIAGE":
        errors.append("record type drift")
    src=data.get("source_intake",{})
    if src.get("commit")!="ec80b855c988e8dc7ddff40cb892b67263d5c86e":
        errors.append("Forge source commit drift")
    if src.get("git_blob_sha1")!="0a71491313ffad6ba2d02a3bdc3fc5a5a8cf65d8":
        errors.append("Forge manifest blob drift")
    entries=data.get("entries",[])
    if len(entries)!=593:
        errors.append("triage must cover exactly 593 strict-open rows")
    ids=[str(x.get("problem_id")) for x in entries]
    if len(ids)!=len(set(ids)):
        errors.append("duplicate problem ids")
    counts={}
    for row in entries:
        cls=row.get("triage_class")
        counts[cls]=counts.get(cls,0)+1
        if row.get("solve_authorized") is not False or row.get("certification_authorized") is not False:
            errors.append(f"authority inflation for {row.get('problem_id')}")
    if counts!=EXPECTED:
        errors.append(f"class counts drift: {counts}")
    by={str(x["problem_id"]):x for x in entries}
    if {i for i,r in by.items() if r["triage_class"]=="FIRST_RECONNAISSANCE_TRANCHE"}!=FIRST:
        errors.append("first tranche identity drift")
    if {i for i,r in by.items() if r["triage_class"]=="HOLD_STATUS_RECONCILIATION"}!=HELD:
        errors.append("status hold identity drift")
    if {i for i,r in by.items() if r["triage_class"]=="DEFER_UNTIL_NEW_MECHANISM"}!=PARK:
        errors.append("mechanism hold identity drift")
    if by["3"]["triage_class"]!="ACTIVE_EXISTING_CAMPAIGN":
        errors.append("Problem 3 must remain bound to existing campaign")
    if by["142"]["triage_class"]!="CROSS_CAMPAIGN_SYNERGY_ONLY":
        errors.append("Problem 142 must route to cross-campaign synergy")
    if data.get("policy",{}).get("no_auto_launch") is not True:
        errors.append("no-auto-launch boundary weakened")
    return errors

def main():
    errors=validate(load())
    if errors:
        raise SystemExit("\n".join(errors))
    print("ERDOS-OPEN triage valid: 593 rows; 8 first-tranche; no Solve authority")
if __name__=="__main__":
    main()
