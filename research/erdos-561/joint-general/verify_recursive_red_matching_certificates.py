#!/usr/bin/env python3
"""Adds source-backed RED-matching recursion to admitted Erdős #561 proof trees.

No full all-host proof is inferred from finite tests; mathematical rules import
source-proved GCL/public results and retain paper UNDER_REVIEW statuses.
"""
import argparse
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import combinations_with_replacement
import json
import verify_recursive_three_blue_certificates as prior

def red_loss(n,m):
    """Exact normalized RED deletion deficit; None means illegal case."""
    prior.validate(n,m)
    s=len(n)
    if s<4:return None
    a=prior.norm(n)
    b=prior.norm(m)
    if a[-2]<2 or sum(a)+s<3*s-1:return None
    U,V=b[0],b[1]
    p=max(0,U-max(a[-3],a[-2]+V-1))+max(0,V-a[-2])
    q=tuple(x-1 for x in a[:-1])
    assert all(x>=1 for x in q)
    assert prior.J(a,b)-(s+1)-prior.J(q,b)==p
    assert prior.J(n,m)-prior.J(a,b)==(s+1)*(n[-1]+m[-1]-2)
    return {"loss":p,"normalized_red":a,"normalized_blue":b,
            "shorter_red":q,"shorter_blue":b,"matching_lower":s+1}

@lru_cache(None)
def original(n,m):
    prior.validate(n,m)
    previous=prior.original(n,m)
    if previous is not None:return previous
    if len(n)<=3:return None
    transfer=prior.transfer(n,m)
    if transfer is None:return None
    proof=joint(n,m)
    if proof is None:return None
    return prior.leaf("ORIGINAL_TRANSFER_AFTER_RED_MATCHING_"+transfer,n,m,proof)

@lru_cache(None)
def joint(n,m):
    prior.validate(n,m)
    previous=prior.joint(n,m)
    if previous is not None:return previous
    if len(n)<=3:return None
    j=prior.J(n,m)
    if prior.W(n[1:],m)==j:
        child=original(n[1:],m)
        if child is not None:
            return prior.leaf("FIRST_RESIDUAL_SHARP_VIA_ENHANCED_ORIGINAL",n,m,child)
    rule=red_loss(n,m)
    if rule is not None and rule["loss"]==0:
        child=joint(rule["shorter_red"],rule["shorter_blue"])
        if child is not None:
            return prior.leaf("RED_MATCHING_ZERO_DEFICIT_RECURSION",n,m,{
                "normalized_red":list(rule["normalized_red"]),
                "normalized_blue":list(rule["normalized_blue"]),
                "shorter_red":list(rule["shorter_red"]),
                "matching_edges_at_least":rule["matching_lower"],
                "red_loss":0,"shorter_joint_certificate":child
            })
    return None

def audit():
    ct=Counter();h=sha256();examples={}
    for s in range(3,9):
        for prefix in combinations_with_replacement(range(1,9),s-1):
            n=tuple(reversed(prefix))+(1,)
            for U in range(2,9):
                for V in range(2,U+1):
                    m=(U,V,1)
                    if prior.canon(n,m)!=prior.canon_alt(n,m):
                        raise AssertionError("independent antidiagonal mismatch")
                    baseJ,baseO=prior.joint(n,m),prior.original(n,m)
                    newJ,newO=joint(n,m),original(n,m)
                    if baseJ is not None:assert newJ is not None
                    if baseO is not None:assert newO is not None
                    if newO is not None:assert newJ is not None or len(n)<=3
                    cat=newJ["proof"] if newJ is not None else "UNKNOWN"
                    ct["total"]+=1
                    ct["old_joint"]+=baseJ is not None
                    ct["new_joint"]+=newJ is not None
                    ct["old_original"]+=baseO is not None
                    ct["new_original"]+=newO is not None
                    ct["new_joint_only"]+=(baseJ is None and newJ is not None)
                    ct["new_original_only"]+=(baseO is None and newO is not None)
                    ct["still_unknown"]+=newJ is None
                    ct["joint_"+cat]+=1
                    if cat not in examples:examples[cat]=[list(n),list(m)]
                    h.update(("%d|%s|%s|%s|%s\n"%(s,",".join(map(str,n)),
                        ",".join(map(str,m)),cat,
                        newO["proof"] if newO else "UNKNOWN")).encode())
    assert ct["total"]==179928
    assert ct["old_joint"]==162839 and ct["old_original"]==129885
    assert ct["new_joint"]==165599 and ct["new_original"]==131028
    assert ct["new_joint_only"]==2760 and ct["new_original_only"]==1143
    assert ct["still_unknown"]==14329
    return {"counts":dict(sorted(ct.items())),"classification_sha256":h.hexdigest(),
            "first_examples_by_method":examples}

def guards():
    example=((7,5,2,1),(5,2,1))
    n,m=example
    rule=red_loss(n,m)
    assert rule is not None and rule["loss"]==0
    assert rule["shorter_red"]==(6,4,1)
    assert prior.joint(n,m) is None
    p=joint(n,m)
    assert p and p["proof"]=="RED_MATCHING_ZERO_DEFICIT_RECURSION"
    assert p["depends_on"]["shorter_joint_certificate"]["proof"]=="SOURCE_RECONSTRUCTED_COMPLETE_3X3_JOINT"
    # Genuine positive red and blue normalized minima: the same identity
    # applies by removing prior RED/BLUE matchings before the final red one.
    for f in range(1,5):
        for g in range(1,5):
            x=tuple(a+f-1 for a in n)
            y=tuple(a+g-1 for a in m)
            r=red_loss(x,y)
            assert r and r["loss"]==0
            assert r["shorter_red"]==(6,4,1)
            assert prior.J(x,y)==prior.J(n,m)+(len(n)+1)*(f+g-2)
            assert joint(x,y) is not None
    # Broad direct algebra guard, independent of the grid's final RED=1.
    count=0
    for s in range(4,8):
        for f in range(1,4):
            for g in range(1,4):
                for U in range(2,8):
                    for V in range(1,U+1):
                        n=tuple((2*s-i)+f-1 for i in range(1,s))+(f,)
                        m=(U+g-1,V+g-1,g)
                        t=red_loss(n,m)
                        assert t is not None
                        count+=1
    return {"normalization_guard_cases":count,
            "new_example_joint":p,
            "note":"No host-census inference or MATHCERT"}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--red")
    ap.add_argument("--blue")
    ap.add_argument("--grid",action="store_true")
    args=ap.parse_args()
    g=guards()
    print("ERDOS561_RED_MATCHING_NORMALIZATION_GUARDS",g["normalization_guard_cases"])
    if args.red or args.blue:
        if not(args.red and args.blue):ap.error("Both RED and BLUE required")
        n=tuple(map(int,args.red.split(",")))
        m=tuple(map(int,args.blue.split(",")))
        prior.validate(n,m)
        print(json.dumps({"red":n,"blue":m,
            "red_transfer":red_loss(n,m),
            "joint_certificate":joint(n,m),
            "original_certificate":original(n,m)},indent=2,sort_keys=True))
    if args.grid or not args.red:
        result=audit()
        print(json.dumps(result,sort_keys=True))
        print("ERDOS561_RECURSIVE_RED_MATCHING_CERTIFICATES_FINITE_PASS")
if __name__=="__main__":main()
