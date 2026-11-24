#!/usr/bin/env python3
"""Provenance-safe ZERO cap / mixed vertex-budget transfer for GCL Erdős #561.

Imports prior all-s BLUE + RED recursive certificates unchanged.
This is an exact finite theorem-dependency audit, NOT independent MathCert.
"""
import argparse
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import combinations_with_replacement
import json
import verify_recursive_red_matching_certificates as red
import verify_recursive_three_blue_certificates as old

def original_guard(n,m):
    """Return a source-sufficient transfer label with EXACT source hypotheses."""
    old.validate(n,m)
    D=n[0]+m[0]-2
    W=old.W(n,m)
    if min(n[0],m[0])==1:
        return "ZERO_CAP_MONOCHROME"
    assert n[0]>=2 and m[0]>=2
    known=old.transfer(n,m)
    if known is not None:return known
    if (n[0]%2)!=(m[0]%2):
        R=max(sum(n)+len(n),sum(m)+len(m))
        if 2*W<2*D*D+R:
            return "OPPOSITE_PARITY_VERTEX_BUDGET"
    return None

@lru_cache(None)
def joint(n,m):
    old.validate(n,m)
    previous=red.joint(n,m)
    if previous is not None:return previous
    if len(n)<=3:return None
    v=old.J(n,m)
    if old.W(n[1:],m)==v:
        dependent=original(n[1:],m)
        if dependent is not None:
            return old.leaf("FIRST_RESIDUAL_SHARP_AFTER_CORE_AUDIT",n,m,dependent)
    info=red.red_loss(n,m)
    if info is not None and info["loss"]==0:
        dependent=joint(info["shorter_red"],info["shorter_blue"])
        if dependent is not None:
            return old.leaf("RED_MATCHING_AFTER_CORE_AUDIT",n,m,{
                "matching_lower":info["matching_lower"],
                "red_loss":0,
                "normalized_red":list(info["normalized_red"]),
                "normalized_blue":list(info["normalized_blue"]),
                "shorter_red":list(info["shorter_red"]),
                "shorter_joint_certificate":dependent})
    return None

@lru_cache(None)
def original(n,m):
    old.validate(n,m)
    if len(n)<=3:
        return old.original(n,m)
    if min(n[0],m[0])==1:
        # Prior original leaf could have used the degree-core theorem outside
        # its n1,m1>=2 hypothesis. Justify HERE by elementary monochromatic
        # argument, with explicit dependency on a sourced sharp joint proof.
        dep=joint(n,m)
        return old.leaf("ORIGINAL_TRANSFER_ZERO_CAP_MONOCHROME",n,m,dep) if dep else None
    previous=red.original(n,m)
    if previous is not None:return previous
    guard=original_guard(n,m)
    if guard is None:return None
    dep=joint(n,m)
    return old.leaf("ORIGINAL_TRANSFER_"+guard,n,m,dep) if dep else None

def audit():
    cnt=Counter();fingerprint=sha256();examples={}
    for s in range(3,9):
        for pre in combinations_with_replacement(range(1,9),s-1):
            n=tuple(reversed(pre))+(1,)
            for U in range(2,9):
                for V in range(2,U+1):
                    m=(U,V,1)
                    assert old.canon(n,m)==old.canon_alt(n,m)
                    jold,jnew=red.joint(n,m),joint(n,m)
                    oold,onew=red.original(n,m),original(n,m)
                    assert jold is None or jnew is not None
                    assert oold is None or onew is not None
                    assert len(n)<=3 or onew is None or jnew is not None
                    category=jnew["proof"] if jnew else "UNKNOWN"
                    cnt['total']+=1
                    cnt['old_joint']+=jold is not None
                    cnt['new_joint']+=jnew is not None
                    cnt['old_original']+=oold is not None
                    cnt['new_original']+=onew is not None
                    cnt['extra_joint']+=jold is None and jnew is not None
                    cnt['extra_original']+=oold is None and onew is not None
                    cnt['joint_unknown']+=jnew is None
                    cnt['proof_'+category]+=1
                    if onew and 'ZERO_CAP_MONOCHROME' in onew['proof']:
                        cnt['explicit_zero_cap_original_proof']+=1
                    if onew and 'OPPOSITE_PARITY_VERTEX_BUDGET' in onew['proof']:
                        cnt['explicit_opposite_core_original_proof']+=1
                    if category not in examples:examples[category]=[list(n),list(m)]
                    fingerprint.update(('%d|%s|%s|%s|%s\n'%(
                        s,','.join(map(str,n)),','.join(map(str,m)),category,
                        onew["proof"] if onew else "UNKNOWN")).encode())
    assert cnt['total']==179928
    assert (cnt['old_joint'],cnt['old_original'])==(165677,131052)
    assert (cnt['new_joint'],cnt['new_original'])==(165851,132487)
    assert (cnt['extra_joint'],cnt['extra_original'])==(174,1435)
    assert cnt['joint_unknown']==14077
    return {"counts":dict(sorted(cnt.items())),"classification_sha256":fingerprint.hexdigest(),
            "first_examples_by_method":examples}

def guards():
    n,m=(2,1,1,1,1),(5,4,1)
    assert original_guard(n,m)=="OPPOSITE_PARITY_VERTEX_BUDGET"
    D=n[0]+m[0]-2;R=max(sum(n)+len(n),sum(m)+len(m))
    assert D==5 and R==13 and old.W(n,m)==31
    assert old.W(n,m)>D*(D+1) and 2*old.W(n,m)<2*D*D+R
    assert joint(n,m) is not None and original(n,m) is not None
    assert original(n,m)["proof"]=="ORIGINAL_TRANSFER_OPPOSITE_PARITY_VERTEX_BUDGET"
    zz,bb=(1,1,1,1),(6,6,1)
    assert original_guard(zz,bb)=="ZERO_CAP_MONOCHROME"
    assert joint(zz,bb) is not None
    o=original(zz,bb)
    assert o is not None and o["proof"]=="ORIGINAL_TRANSFER_ZERO_CAP_MONOCHROME"
    # Guard is not allowed to apply Lovasz factor transfer to leading-one
    # pairs; test explicitly for both zero-cap orientations.
    for u in range(1,11):
        for s in range(4,8):
            a=(1,)*s;b=(u,u,1)
            assert original_guard(a,b)=="ZERO_CAP_MONOCHROME"
    return "MONOCHROME_AND_OPPOSITE_PARITY_GUARDS_PASS"

def main():
    pa=argparse.ArgumentParser()
    pa.add_argument("--red")
    pa.add_argument("--blue")
    pa.add_argument("--grid",action="store_true")
    a=pa.parse_args()
    print(guards())
    if a.red or a.blue:
        if not(a.red and a.blue):pa.error("provide both red/blue")
        n=tuple(map(int,a.red.split(',')))
        m=tuple(map(int,a.blue.split(',')))
        old.validate(n,m)
        print(json.dumps({"red":n,"blue":m,"transfer_guard":original_guard(n,m),
                          "joint":joint(n,m),"original":original(n,m)},
                         indent=2,sort_keys=True))
    if a.grid or not a.red:
        print(json.dumps(audit(),sort_keys=True))
        print("ERDOS561_RECURSIVE_VERTEX_BUDGET_FINITE_PASS")
if __name__=="__main__":main()
