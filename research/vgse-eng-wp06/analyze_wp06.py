#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from fractions import Fraction
from pathlib import Path

HERE=Path(__file__).resolve().parent

def load(name):
    return json.loads((HERE/name).read_text(encoding="utf-8"))

def rank(M):
    a=[[Fraction(v) for v in row] for row in M]
    r=0
    for c in range(len(a[0])):
        p=next((i for i in range(r,len(a)) if a[i][c]),None)
        if p is None: continue
        a[r],a[p]=a[p],a[r]
        q=a[r][c]; a[r]=[v/q for v in a[r]]
        for i in range(len(a)):
            if i==r or not a[i][c]: continue
            f=a[i][c]; a[i]=[x-f*y for x,y in zip(a[i],a[r])]
        r+=1
        if r==len(a): break
    return r

def validate():
    errors=[]
    src=load("SOURCE_DEFINITION_AUDIT.json")
    te3=load("TE3_REPLAY.json")
    sym=load("BOUNDARY_SYMMETRY.json")
    act=load("QUOTIENT_ACTION.json")
    norm=load("NORMALIZATION_AUDIT.json")
    res=load("RESULTS.json")
    claims=load("CLAIM_LEDGER.json")

    if "TE3" not in src["primary_source"]["source_definition"]:
        errors.append("source TE3 definition missing")
    if src["current_c05"]["missing_source_definition_check"] is None:
        errors.append("C05 TE3 audit gap missing")

    if te3["aggregate"]["disposition"]!="TE3_FAILS_FOR_PROTECTED_C04_WEIGHT_CLASS_ON_ALL_FIVE_RETAINED_BRANCHES":
        errors.append("TE3 disposition drift")
    if len(te3["branch_replay"])!=5:
        errors.append("TE3 branch count drift")
    for b in te3["branch_replay"]:
        r=b["simple_P12_contradiction"]["ratio"]
        if not (0 < r < 0.03):
            errors.append(f"branch {b['branch']} no longer shows robust P12 contradiction")
        if max(abs(x-1) for x in b["target_ratios"][5:]) >= 1e-10:
            errors.append(f"branch {b['branch']} cycle replay drift")
    if te3["aggregate"]["maximum_closed_cycle_relative_error"]>=1e-10:
        errors.append("cycle tolerance exceeded")

    M=act["matrix"]
    if rank(M)!=5 or act["rank"]!=5 or act["kernel_dimension"]!=1:
        errors.append("boundary quotient action rank/kernel drift")
    k=act["kernel_generator"]
    if any(sum(row[j]*k[j] for j in range(6)) for row in M):
        errors.append("stored kernel generator invalid")
    if act["closed_cycle_action"]!="zero on all three WP05 closed-cycle coordinates":
        errors.append("cycle action drift")

    if res["source_defined_t_embedding"]["recovered_rank"]!=8:
        errors.append("true t-embedding must remain 8/8 geometry-identifiable")
    if res["broader_algebraic_realization_class"]["geometry_only_identifiable_rank"]!=3:
        errors.append("algebraic class geometry-only rank drift")
    if res["broader_algebraic_realization_class"]["boundary_ambiguity_rank"]!=5:
        errors.append("boundary ambiguity rank drift")
    if res["terminal_candidate"]!="BOUNDARY_CALIBRATION_FIVE_DIMENSIONAL_OBSTRUCTION":
        errors.append("terminal candidate drift")
    if any(res["claim_boundary"].values()):
        errors.append("claim boundary crossed")
    ids={c["id"] for c in claims["claims"]}
    if ids != {f"VGSE-ENG-WP06-C{i:02d}" for i in range(1,11)}:
        errors.append("claim ledger IDs drift")
    return errors

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--check",action="store_true"); a=ap.parse_args()
    errors=validate()
    if errors:
        print("\n".join(errors)); return 1
    if a.check: print("VGSE-ENG-WP06 deterministic replay: PASS")
    else: print(json.dumps({"status":"PASS","terminal_candidate":load("RESULTS.json")["terminal_candidate"]},indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
