#!/usr/bin/env python3
"""Erdős #561: restore fourth source-proved ORIGINAL core transfer to 3-blue proof trees.

This only composes existing, source-labeled sufficient theorems. It must not
turn UNKNOWN into a refutation, claim a full solution, or self-certify MATHCERT.
"""
import argparse
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import combinations_with_replacement, product
import json
import verify_recursive_three_blue_certificates as prior
import verify_recursive_red_matching_certificates as red

FOURTH = "OPPOSITE_PARITY_NONISOLATED_VERTEX_BUDGET"

def fourth_core_gate(n,m):
    """Fourth gate of source GENERAL_CORE_ORIGINAL_TRANSFER.md, Theorem A.

    Only the previously *unhandled* fourth sufficient criterion is returned.
    Source assumes BOTH leading arm sizes >=2 and opposite parity.
    """
    prior.validate(n,m)
    if prior.transfer(n,m) is not None:
        return None
    if n[0]<2 or m[0]<2:
        return None
    if (n[0]-m[0])%2!=1:
        return None
    D=n[0]+m[0]-2
    R=max(sum(n)+len(n),sum(m)+len(m))
    return FOURTH if 2*prior.W(n,m)<2*D*D+R else None

@lru_cache(None)
def original(n,m):
    prior.validate(n,m)
    old=red.original(n,m)
    if old is not None:return old
    if len(n)<=3:return None
    # An enhanced JOINT certificate can also activate one of the THREE
    # previously source-proved ORIGINAL transfer gates, even when the old
    # classifier could not previously reach that JOINT dependency.
    prior_gate=prior.transfer(n,m)
    fourth_gate=fourth_core_gate(n,m)
    if prior_gate is None and fourth_gate is None:return None
    child=joint(n,m)
    if child is None:return None
    if prior_gate is not None:
        return prior.leaf("ORIGINAL_TRANSFER_AFTER_ENHANCED_JOINT_"+prior_gate,n,m,{
            "source_theorem":"GENERAL_CORE_ORIGINAL_TRANSFER.md/Theorem A/conditions 1-3",
            "exact_joint_certificate":child
        })
    D=n[0]+m[0]-2
    R=max(sum(n)+len(n),sum(m)+len(m))
    return prior.leaf("ORIGINAL_TRANSFER_"+FOURTH,n,m,{
        "source_theorem":"GENERAL_CORE_ORIGINAL_TRANSFER.md/Theorem A/condition 4",
        "necessary_prior_joint_certificate":child,
        "leading_caps":[n[0]-1,m[0]-1],
        "degree_budget_D":D,"nonisolated_vertex_lower_R":R,
        "strict_budget_margin":2*D*D+R-2*prior.W(n,m)
    })

@lru_cache(None)
def joint(n,m):
    prior.validate(n,m)
    old=red.joint(n,m)
    if old is not None:return old
    if len(n)<=3:return None
    # R1 must be a previously or recursively proven exact ORIGINAL; its
    # arbitrary-host lower then matches the canonical JOINT upper.
    if prior.W(n[1:],m)==prior.J(n,m):
        child=original(n[1:],m)
        if child is not None:
            return prior.leaf("FIRST_RESIDUAL_SHARP_VIA_FOURTH_CORE",n,m,child)
    # A zero-deficit RED matching may recurse on STRICTLY SHORTER red lists.
    x=red.red_loss(n,m)
    if x is not None and x["loss"]==0:
        child=joint(x["shorter_red"],x["shorter_blue"])
        if child is not None:
            return prior.leaf("RED_MATCHING_VIA_FOURTH_CORE_RECURSION",n,m,{
                "normalized_red":list(x["normalized_red"]),
                "normalized_blue":list(x["normalized_blue"]),
                "shorter_red":list(x["shorter_red"]),
                "red_matching_loss":0,"minimum_matching_edges":x["matching_lower"],
                "shorter_joint_certificate":child
            })
    return None

def algebra_guards():
    checked=0;guardable=0;prior_covered=0;invalid=0
    for s in range(3,8):
        for p in combinations_with_replacement(range(1,9),s-1):
            n=tuple(reversed(p))+(1,)
            for U in range(1,9):
                for V in range(1,U+1):
                    m=(U,V,1)
                    if prior.canon(n,m)!=prior.canon_alt(n,m):
                        raise AssertionError("mismatched antidiagonal indexes")
                    label=fourth_core_gate(n,m)
                    checked+=1
                    if label:
                        guardable+=1
                        D=n[0]+m[0]-2;R=max(sum(n)+len(n),sum(m)+len(m))
                        assert n[0]>=2 and m[0]>=2
                        assert (n[0]-m[0])%2 and 2*prior.W(n,m)<2*D*D+R
                        assert prior.transfer(n,m) is None
                        assert 2*D*D+R-2*prior.W(n,m)>=1
                    if prior.transfer(n,m) is not None:prior_covered+=1
                    if min(n[0],m[0])<2 and label:invalid+=1
    assert invalid==0
    # Boundary equality and parity/leading-cap exclusions: fail CLOSED.
    for n,m in [((1,1,1,1),(6,6,1)),((2,1,1),(2,1,1)),((2,2,1),(4,3,1))]:
        assert fourth_core_gate(n,m) is None
    return {"guard_cells":checked,"new_criterion_guardable":guardable,
            "prior_transfer_covered":prior_covered,
            "leading_cap_exclusion":invalid}

def audit():
    counts=Counter();classification=sha256();examples={}
    for s in range(3,9):
        for prefix in combinations_with_replacement(range(1,9),s-1):
            n=tuple(reversed(prefix))+(1,)
            for U in range(2,9):
                for V in range(2,U+1):
                    m=(U,V,1)
                    oldJ,oldO=red.joint(n,m),red.original(n,m)
                    newJ,newO=joint(n,m),original(n,m)
                    assert oldJ is None or newJ is not None
                    assert oldO is None or newO is not None
                    assert newO is None or newJ is not None or len(n)<=3
                    cat=newJ["proof"] if newJ else "UNKNOWN"
                    counts["total"]+=1
                    counts["old_joint"]+=oldJ is not None
                    counts["new_joint"]+=newJ is not None
                    counts["old_original"]+=oldO is not None
                    counts["new_original"]+=newO is not None
                    counts["added_joint"]+=oldJ is None and newJ is not None
                    counts["added_original"]+=oldO is None and newO is not None
                    counts["remaining_joint_unknown"]+=newJ is None
                    counts["new_joint_by_"+cat]+=1
                    if oldJ is None and newJ is not None and "new_joint" not in examples:
                        examples["new_joint"]={"n":list(n),"m":list(m),"proof":newJ}
                    if oldO is None and newO is not None and "new_original" not in examples:
                        examples["new_original"]={"n":list(n),"m":list(m),"proof":newO}
                    classification.update(("%d|%s|%s|%s|%s\n"%(
                        s,",".join(map(str,n)),",".join(map(str,m)),cat,
                        newO["proof"] if newO else "UNKNOWN")).encode())
    assert counts["total"]==179928
    assert (counts["old_joint"],counts["old_original"])==(165677,131052)
    assert (counts["new_joint"],counts["new_original"])==(165741,132393)
    assert (counts["added_joint"],counts["added_original"])==(64,1341)
    assert counts["remaining_joint_unknown"]==14187
    assert counts["old_joint"]+counts["added_joint"]==counts["new_joint"]
    assert counts["old_original"]+counts["added_original"]==counts["new_original"]
    return {"counts":dict(sorted(counts.items())),
            "classification_sha256":classification.hexdigest(),
            "first_new_examples":examples}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--red")
    parser.add_argument("--blue")
    parser.add_argument("--grid",action="store_true")
    args=parser.parse_args()
    print("ERDOS561_FOURTH_CORE_GUARDS",json.dumps(algebra_guards(),sort_keys=True))
    if args.red or args.blue:
        if not (args.red and args.blue):parser.error("both original lists required")
        n=tuple(map(int,args.red.split(",")))
        m=tuple(map(int,args.blue.split(",")))
        prior.validate(n,m)
        print(json.dumps({"red":n,"blue":m,
            "fourth_condition":fourth_core_gate(n,m),
            "joint_certificate":joint(n,m),
            "original_certificate":original(n,m)},sort_keys=True,indent=2))
    if args.grid or not args.red:
        result=audit()
        print("ERDOS561_FOURTH_CORE_CLASSIFICATION",json.dumps(result,sort_keys=True))
        print("ERDOS561_FOURTH_CORE_RECURSIVE_CERTIFICATES_FINITE_PASS")

if __name__=="__main__":
    main()
