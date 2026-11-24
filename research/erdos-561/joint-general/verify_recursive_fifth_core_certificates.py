#!/usr/bin/env python3
"""Erdős #561: fifth all-parity ORIGINAL core-vertex-support transfer.

Only composes SOURCE-PROVED (paper UNDER_REVIEW) sufficient theorems.
Do not claim MATHCERT or the complete unrestricted conjecture.
"""
import argparse
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import combinations_with_replacement
import json

import verify_recursive_vertex_budget_certificates as previous

prior = previous.prior
red = previous.red
FIFTH = "ANY_PARITY_NONISOLATED_MAXIMUM_DEGREE_CORE"

def fifth_core_gate(n,m):
    """New sufficient ORIGINAL gate; no unproved sharp JOINT is assumed."""
    prior.validate(n,m)
    if n[0]<2 or m[0]<2:
        return None
    D=n[0]+m[0]-2
    R=max(sum(n)+len(n),sum(m)+len(m))
    W=prior.W(n,m)
    return FIFTH if 2*W<=D*D+R else None

@lru_cache(None)
def joint(n,m):
    prior.validate(n,m)
    old=previous.joint(n,m)
    if old is not None:
        return old
    if len(n)<=3:
        return None
    if prior.W(n[1:],m)==prior.J(n,m):
        child=original(n[1:],m)
        if child is not None:
            return prior.leaf("FIRST_RESIDUAL_SHARP_VIA_FIFTH_CORE",n,m,{
                "source_rule":"RECURSIVE_THREE_BLUE_CERTIFICATE_THEOREM.md/R1",
                "strictly_shorter_red_original":child})
    rule=red.red_loss(n,m)
    if rule is not None and rule["loss"]==0:
        child=joint(rule["shorter_red"],rule["shorter_blue"])
        if child is not None:
            return prior.leaf("RED_MATCHING_VIA_FIFTH_CORE_RECURSION",n,m,{
                "source_rule":"RECURSIVE_RED_MATCHING_CERTIFICATE_THEOREM.md",
                "normalized_red":list(rule["normalized_red"]),
                "normalized_blue":list(rule["normalized_blue"]),
                "shorter_red":list(rule["shorter_red"]),
                "shorter_blue":list(rule["shorter_blue"]),
                "matching_edges_at_least":rule["matching_lower"],
                "matching_deficit":0,
                "strictly_shorter_joint":child})
    return None

@lru_cache(None)
def original(n,m):
    prior.validate(n,m)
    old=previous.original(n,m)
    if old is not None:
        return old
    if len(n)<=3:
        return None
    previous_gate=prior.transfer(n,m)
    fourth_gate=previous.fourth_core_gate(n,m)
    fifth_gate=fifth_core_gate(n,m)
    if previous_gate is None and fourth_gate is None and fifth_gate is None:
        return None
    child=joint(n,m)
    if child is None:
        return None
    if previous_gate is not None:
        return prior.leaf("ORIGINAL_TRANSFER_AFTER_FIFTH_ENHANCED_JOINT_"+previous_gate,n,m,{
            "source_theorem":"GENERAL_CORE_ORIGINAL_TRANSFER.md/Theorem A/conditions 1-3",
            "individually_proved_sharp_joint":child})
    if fourth_gate is not None:
        return prior.leaf("ORIGINAL_TRANSFER_AFTER_FIFTH_ENHANCED_JOINT_"+fourth_gate,n,m,{
            "source_theorem":"GENERAL_CORE_ORIGINAL_TRANSFER.md/Theorem A/condition 4",
            "individually_proved_sharp_joint":child})
    assert fifth_gate==FIFTH
    D=n[0]+m[0]-2
    R=max(sum(n)+len(n),sum(m)+len(m))
    W=prior.W(n,m)
    assert min(n[0],m[0])>=2 and 2*W<=D*D+R
    return prior.leaf("ORIGINAL_TRANSFER_"+FIFTH,n,m,{
        "source_theorem":"RECURSIVE_FIFTH_CORE_VERTEX_SUPPORT_THEOREM.md/Theorem F",
        "individually_proved_sharp_joint":child,
        "degree_caps":[n[0]-1,m[0]-1],
        "maximum_degree_D":D,"minimum_nonisolated_vertices_R":R,
        "original_canonical_W":W,
        "core_vertex_budget_margin":D*D+R-2*W,
        "necessary_number_of_degree_D_vertices":D+1,
        "handshake_twice_edges_at_least":D*D+R-1,
        "counterexample_twice_edges_at_most":2*W-2})

def gate_guards():
    ct=Counter()
    for s in range(3,8):
        for prefix in combinations_with_replacement(range(1,9),s-1):
            n=tuple(reversed(prefix))+(1,)
            for U in range(1,9):
                for V in range(1,U+1):
                    m=(U,V,1)
                    if prior.canon(n,m)!=prior.canon_alt(n,m):
                        raise AssertionError("independent canonical indexing mismatch")
                    label=fifth_core_gate(n,m)
                    ct["checked"]+=1
                    if label is None:continue
                    ct["guard_legal"]+=1
                    D=n[0]+U-2
                    R=max(sum(n)+len(n),sum(m)+3)
                    W=prior.W(n,m)
                    assert min(n[0],U)>=2
                    assert 2*W<=R+D*D
                    assert 2*(W-1)<R+D*D-1
                    assert D>=2 and D+1<=R or D+1<=sum(n)+len(n)+sum(m)+3
                    ct["inclusive_margin_zero"]+=(2*W==R+D*D)
                    ct["margin_positive"]+=(2*W<R+D*D)
    for n,m in [((1,1,1,1),(8,2,1)),((2,2,1),(2,2,1))]:
        assert fifth_core_gate(n,m) is None
    assert fifth_core_gate((4,1,1,1),(4,2,1))==FIFTH
    assert fifth_core_gate((2,2,1,1),(8,6,1))==FIFTH
    return dict(sorted(ct.items()))

def audit():
    ct=Counter()
    fingerprint=sha256()
    examples={}
    for s in range(3,9):
        for prefix in combinations_with_replacement(range(1,9),s-1):
            n=tuple(reversed(prefix))+(1,)
            for U in range(2,9):
                for V in range(2,U+1):
                    m=(U,V,1)
                    oldj=previous.joint(n,m)
                    oldo=previous.original(n,m)
                    newj=joint(n,m)
                    newo=original(n,m)
                    assert oldj is None or newj is not None
                    assert oldo is None or newo is not None
                    assert newo is None or newj is not None or len(n)<=3
                    if newj is not None:
                        assert newj["red"]==list(n) or tuple(newj["red"])==n
                    ct["total"]+=1
                    ct["prior_joint"]+=(oldj is not None)
                    ct["new_joint"]+=(newj is not None)
                    ct["prior_original"]+=(oldo is not None)
                    ct["new_original"]+=(newo is not None)
                    ct["newly_joint"]+=(oldj is None and newj is not None)
                    ct["newly_original"]+=(oldo is None and newo is not None)
                    ct["remaining_joint_unknown"]+=(newj is None)
                    ct["remaining_original_unknown"]+=(newo is None)
                    if oldj is not None and oldo is None and fifth_core_gate(n,m):
                        ct["fifth_direct_prior_joint_recovery"]+=1
                    catj=newj["proof"] if newj is not None else "UNKNOWN"
                    cato=newo["proof"] if newo is not None else "UNKNOWN"
                    ct["joint_method_"+catj]+=1
                    ct["original_method_"+cato]+=1
                    if oldj is None and newj is not None and "new_joint" not in examples:
                        examples["new_joint"]={"red":list(n),"blue":list(m),"proof":newj}
                    if oldo is None and newo is not None and "new_original" not in examples:
                        examples["new_original"]={"red":list(n),"blue":list(m),"proof":newo}
                    fingerprint.update(("%d|%s|%s|%s|%s\n"%(
                        s,",".join(map(str,n)),",".join(map(str,m)),catj,cato)).encode())
    assert ct["total"]==179928
    assert ct["prior_joint"]==165741
    assert ct["prior_original"]==132393
    assert ct["fifth_direct_prior_joint_recovery"]==18863
    assert ct["new_joint"]>=ct["prior_joint"]
    assert ct["new_original"]>=ct["prior_original"]+18863
    return {"counts":dict(sorted(ct.items())),
            "classification_sha256":fingerprint.hexdigest(),
            "first_new_examples":examples}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--red");p.add_argument("--blue")
    p.add_argument("--grid",action="store_true")
    p.add_argument("--guard-only",action="store_true")
    args=p.parse_args()
    print("ERDOS561_FIFTH_CORE_NUMERICAL_GUARDS",json.dumps(gate_guards(),sort_keys=True))
    if args.red or args.blue:
        if not (args.red and args.blue):p.error("both --red and --blue required")
        n=tuple(map(int,args.red.split(",")))
        m=tuple(map(int,args.blue.split(",")))
        prior.validate(n,m)
        print(json.dumps({"red":n,"blue":m,"fifth_condition":fifth_core_gate(n,m),
                          "joint_certificate":joint(n,m),
                          "original_certificate":original(n,m)},sort_keys=True,indent=2))
    if args.grid or (not args.guard_only and not args.red):
        out=audit()
        print("ERDOS561_FIFTH_CORE_FULL_GRID",json.dumps(out,sort_keys=True))
        print("ERDOS561_FIFTH_CORE_RECURSIVE_CERTIFICATES_FINITE_PASS")

if __name__=="__main__":
    main()
