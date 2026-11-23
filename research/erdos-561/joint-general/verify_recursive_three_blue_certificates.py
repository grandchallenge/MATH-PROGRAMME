#!/usr/bin/env python3
"""Erdős #561: executable sufficient theorem-composition for 3 BLUE stars.

An exact certificate here is a *proof dependency trace* whose correctness
depends on the named paper-level GCL/public source theorems. It is NOT a
machine-checked proof of those source theorems, independent review, or MATHCERT.

Uses the source-proved all-s single-blue-matching lower, pinned two-BLUE
ORIGINAL size theorem, full 3x3 ORIGINAL/JOIN theorem, and three protected
degree-core transfer criteria. No SAT solver, machine learning or sampling.
"""
import argparse
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import combinations_with_replacement
import json

def canon(n,m):
    return tuple(max(n[i]+m[j]-1 for i in range(len(n)) for j in range(len(m))
                     if i+j==k) for k in range(len(n)+len(m)-1))
def canon_alt(n,m):
    return tuple(max(n[i-1]+m[k-i-1]-1 for i in range(1,len(n)+1)
                     if 1<=k-i<=len(m)) for k in range(2,len(n)+len(m)+1))
def W(n,m): return sum(canon(n,m))
def J(n,m): return sum(canon(n,m)[1:])
def sorted_positive(a):
    return bool(a) and all(isinstance(x,int) and x>=1 for x in a) and tuple(sorted(a,reverse=True))==a
def validate(n,m):
    if not sorted_positive(n) or not sorted_positive(m) or len(m)!=3 or len(n)<2:
        raise ValueError("Require sorted positive RED length >=2 and BLUE length exactly three.")
def red_support(n):
    return sum(n)+len(n)>=3*len(n)-1
def norm(n):
    return tuple(x-n[-1]+1 for x in n)
def blue_loss(n,m):
    assert n[-1]==1 and m[-1]==1 and len(m)==3 and m[1]>=2
    return sum(max(0,n[i]-max(n[i+1]+m[1]-1,
                n[i+2]+m[0]-1 if i+2<len(n) else -10**30))
               for i in range(len(n)-1))
def transfer(n,m):
    """Exact source-proved sufficient ORIGINAL transfer condition; one label."""
    D=n[0]+m[0]-2
    w=W(n,m)
    if w<=D*(D+1)//2:return "CORE_HANDSHAKE_HALF"
    if n[0]%2 and m[0]%2:return "EVEN_CAP_SPLIT_BOTH_LEADERS_ODD"
    if (n[0]%2 or m[0]%2) and w<=D*(D+1):
        return "SATURATED_CORE_UNIQUENESS_ONE_ODD"
    return None
def leaf(kind,n,m,dependency=None):
    return {"proof":kind,"red":list(n),"blue":list(m),
            "joint_canonical":J(n,m),"original_canonical":W(n,m),
            **({"depends_on":dependency} if dependency else {})}

@lru_cache(None)
def original(n,m):
    validate(n,m)
    if len(n)==2:
        return leaf("PINNED_TWO_COMPONENT_ORIGINAL",n,m)
    if len(n)==3:
        return leaf("SOURCE_RECONSTRUCTED_COMPLETE_3X3_ORIGINAL",n,m)
    j=joint(n,m)
    method=transfer(n,m)
    if j is None or method is None:return None
    return leaf("ORIGINAL_TRANSFER_"+method,n,m,j)

@lru_cache(None)
def joint(n,m):
    validate(n,m)
    if len(n)==2:
        # Two-RED-component residual bridge after swapping colours.
        return leaf("SOURCE_TWO_COMPONENT_JOINT_BRIDGE",n,m)
    if len(n)==3:
        return leaf("SOURCE_RECONSTRUCTED_COMPLETE_3X3_JOINT",n,m)
    j=J(n,m)
    a,b=norm(n),norm(m)
    if b[1]>=2 and red_support(a) and blue_loss(a,b)==0:
        return leaf("ALL_S_SINGLE_BLUE_MATCHING_ZERO_DEFICIT",n,m,{
            "normalized_red":list(a),"normalized_blue":list(b),
            "normalized_red_support":sum(a)+len(a),"blue_matching_loss":0})
    if W(n,m[1:])==j:
        return leaf("SECOND_RESIDUAL_PINNED_TWO_BLUE_ORIGINAL",n,m,{
            "second_residual_value":W(n,m[1:])})
    first=original(n[1:],m)
    if first is not None and W(n[1:],m)==j:
        return leaf("FIRST_RESIDUAL_RECURSIVELY_SHARP_ORIGINAL",n,m,first)
    return None

def counts_grid():
    cnt=Counter()
    # Fingerprint all classified cases and their theorem provenance in
    # deterministic order; independent auditors can compare exact source run.
    h=sha256()
    sample={}
    for s in range(3,9):
        for prefix in combinations_with_replacement(range(1,9),s-1):
            n=tuple(reversed(prefix))+(1,)
            for U in range(2,9):
                for V in range(2,U+1):
                    m=(U,V,1)
                    assert canon(n,m)==canon_alt(n,m)
                    j=joint(n,m)
                    o=original(n,m)
                    category=j["proof"] if j is not None else "OPEN"
                    cnt["profiles"]+=1
                    cnt["joint_"+category]+=1
                    cnt["joint_sharp_proved"]+=int(j is not None)
                    cnt["original_sharp_proved"]+=int(o is not None)
                    cnt["joint_unresolved"]+=int(j is None)
                    if category not in sample:
                        sample[category]={"red":n,"blue":m}
                    h.update((str(s)+"|"+",".join(map(str,n))+"|"+
                              ",".join(map(str,m))+"|"+category+"|"+
                              (o["proof"] if o else "OPEN")+"\n").encode())
    assert cnt["profiles"]==179928
    assert cnt["joint_sharp_proved"]==162839
    assert cnt["joint_unresolved"]==17089
    assert cnt["original_sharp_proved"]==129885
    assert cnt["joint_SOURCE_RECONSTRUCTED_COMPLETE_3X3_JOINT"]==1008
    assert cnt["joint_ALL_S_SINGLE_BLUE_MATCHING_ZERO_DEFICIT"]==133949
    assert cnt["joint_SECOND_RESIDUAL_PINNED_TWO_BLUE_ORIGINAL"]==13924
    assert cnt["joint_FIRST_RESIDUAL_RECURSIVELY_SHARP_ORIGINAL"]==13958
    return {"counts":dict(sorted(cnt.items())),"classification_sha256":h.hexdigest(),
            "first_examples_by_method":sample}

def independent_guard_tests():
    # Sources of the original bound are checked by BOTH canonical conventions.
    for n,m in [((4,3,2,1),(8,4,1)),((8,7,4,2,1),(9,4,1)),
                ((1,1,1,1),(3,2,1)),((2,2,1,1,1),(8,2,1))]:
        assert canon(n,m)==canon_alt(n,m)
        a,b=norm(n),norm(m)
        if b[1]>=2:
            p=blue_loss(a,b)
            assert J(a,b)-(len(a)+1)-J(a,(b[0]-1,b[1]-1))==p
        jj=joint(n,m)
        oo=original(n,m)
        if jj is not None:
            assert jj["joint_canonical"]==J(n,m)
        if oo is not None:
            assert oo["original_canonical"]==W(n,m)
    # An explicit smaller witness where no criterion applies must remain open:
    # found by the finite exact loop, not a statement that the conjecture fails.
    return "PROOF_DEPENDENCY_AND_CANONICAL_INDEX_GUARDS_PASS"

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--red",help="comma-separated nonincreasing positive sizes")
    ap.add_argument("--blue",help="comma-separated THREE nonincreasing positive sizes")
    ap.add_argument("--grid",action="store_true",help="enumerate declared full parameter grid")
    args=ap.parse_args()
    print(independent_guard_tests())
    if args.red or args.blue:
        if not (args.red and args.blue):ap.error("specify both --red and --blue")
        n=tuple(int(x) for x in args.red.split(","))
        m=tuple(int(x) for x in args.blue.split(","))
        validate(n,m)
        print(json.dumps({"red":n,"blue":m,
                          "joint_certificate":joint(n,m),
                          "original_certificate":original(n,m)},
                          indent=2,sort_keys=True))
    if args.grid or not args.red:
        print(json.dumps(counts_grid(),sort_keys=True))
        print("ERDOS561_RECURSIVE_THREE_BLUE_PROOF_CERTIFICATES_FINITE_PASS")
if __name__=="__main__": main()
