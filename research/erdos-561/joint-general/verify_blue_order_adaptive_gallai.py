#!/usr/bin/env python3
"""Exact arithmetic and source-derived proof-tree replay of adaptive Gallai criterion.

Does not independently establish the factor-critical theorem or certify MATHCERT.
"""
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import combinations_with_replacement
import json
import verify_gallai_no_triangle_support as parent

old=parent.old
prior=parent.prior
red=parent.red

def adaptive_support(n,V):
    s=len(n)
    rho=(V+3)//2    # ceil((V+2)/2) for second BLUE target F(V,1)
    return sum(n)+s >= 2*s+s//rho

@lru_cache(None)
def joint(n,m):
    prior.validate(n,m)
    oldproof=parent.joint(n,m)
    if oldproof is not None:return oldproof
    if len(n)<=3:return None
    a,b=prior.norm(n),prior.norm(m)
    if b[1]>=2 and adaptive_support(a,b[1]) and prior.blue_loss(a,b)==0:
        assert not parent.improved_support(a)
        s=len(a);rho=(b[1]+3)//2
        return prior.leaf("BLUE_ORDER_ADAPTIVE_GALLAI_MATCHING_ZERO_DEFICIT",n,m,{
            "source_theorem":"BLUE_ORDER_ADAPTIVE_GALLAI_SUPPORT_THEOREM.md/Theorem V and Corollary W",
            "normalized_red":list(a),"normalized_blue":list(b),
            "matching_lower_bound":s+1,"blue_order_matching_factor_rho":rho,
            "adaptive_required_support":2*s+s//rho,
            "actual_normalized_red_support":sum(a)+s,
            "blue_matching_deficit":0})
    if prior.W(n[1:],m)==prior.J(n,m):
        child=original(n[1:],m)
        if child is not None:
            return prior.leaf("BLUE_ORDER_ADAPTIVE_FIRST_RESIDUAL_ORIGINAL",n,m,{
                "source_rule":"RECURSIVE_THREE_BLUE_CERTIFICATE_THEOREM.md/R1",
                "strictly_shorter_original":child})
    q=red.red_loss(n,m)
    if q is not None and q["loss"]==0:
        child=joint(q["shorter_red"],q["shorter_blue"])
        if child is not None:
            return prior.leaf("BLUE_ORDER_ADAPTIVE_RED_MATCHING_RECURSION",n,m,{
                "source_rule":"RECURSIVE_RED_MATCHING_CERTIFICATE_THEOREM.md",
                "loss":0,"strictly_shorter_joint":child})
    return None

@lru_cache(None)
def original(n,m):
    prior.validate(n,m)
    oldproof=parent.original(n,m)
    if oldproof is not None:return oldproof
    if len(n)<=3:return None
    t=prior.transfer(n,m)
    fourth=old.previous.fourth_core_gate(n,m)
    fifth=old.fifth_core_gate(n,m)
    if t is None and fourth is None and fifth is None:return None
    j=joint(n,m)
    if j is None:return None
    return prior.leaf("BLUE_ORDER_ADAPTIVE_ORIGINAL_TRANSFER_"+str(t or fourth or fifth),n,m,{
        "source_theorem":"GENERAL_CORE_ORIGINAL_TRANSFER.md or RECURSIVE_FIFTH_CORE_VERTEX_SUPPORT_THEOREM.md",
        "strict_dependency_sharp_joint":j})

def audit():
    c=Counter();digest=sha256();examples={}
    for s in range(3,9):
        for prefix in combinations_with_replacement(range(1,9),s-1):
            n=tuple(reversed(prefix))+(1,)
            for U in range(2,9):
                for V in range(2,U+1):
                    m=(U,V,1)
                    prior_support=parent.improved_support(n)
                    new_support=adaptive_support(n,V)
                    assert not prior_support or new_support
                    loss=prior.blue_loss(n,m)
                    assert prior.canon(n,m)==prior.canon_alt(n,m)
                    c["total"]+=1
                    c["parent_support"]+=prior_support
                    c["adaptive_support"]+=new_support
                    c["additional_support"]+=new_support and not prior_support
                    c["parent_zero_loss"]+=prior_support and loss==0
                    c["adaptive_zero_loss"]+=new_support and loss==0
                    c["additional_zero_loss"]+=new_support and not prior_support and loss==0
                    pj=parent.joint(n,m);po=parent.original(n,m)
                    nj=joint(n,m);no=original(n,m)
                    assert pj is None or nj is not None
                    assert po is None or no is not None
                    c["parent_joint"]+=pj is not None
                    c["parent_original"]+=po is not None
                    c["new_joint"]+=nj is not None
                    c["new_original"]+=no is not None
                    if nj is not None and pj is None:
                        c["new_joint_in_this_extension"]+=1
                        c["new_joint_"+nj["proof"]]+=1
                        if "joint" not in examples:examples["joint"]=nj
                    if no is not None and po is None:
                        c["new_original_in_this_extension"]+=1
                        if "original" not in examples:examples["original"]=no
                    digest.update((str((n,m))+"|"+(nj["proof"] if nj else "UNKNOWN")+"|"+
                                   (no["proof"] if no else "UNKNOWN")+"\n").encode())
    c["joint_unknown"]=c["total"]-c["new_joint"]
    c["original_unknown"]=c["total"]-c["new_original"]
    assert c["total"]==179928
    assert (c["parent_support"],c["adaptive_support"])==(179368,179635)
    assert (c["parent_zero_loss"],c["adaptive_zero_loss"])==(135852,136118)
    assert (c["additional_support"],c["additional_zero_loss"])==(267,266)
    assert c["parent_joint"]==167485 and c["parent_original"]==152446
    return {"counts":dict(sorted(c.items())),"fingerprint":digest.hexdigest(),
            "examples":examples}

if __name__=="__main__":
    z=audit()
    print("ERDOS561_BLUE_TARGET_ORDER_ADAPTIVE_FULL_GRID",json.dumps(z,sort_keys=True))
    print("ERDOS561_BLUE_TARGET_ORDER_ADAPTIVE_FINITE_PASS")
