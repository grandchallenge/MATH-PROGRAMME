#!/usr/bin/env python3
"""Erdos #561 bilateral RED/BLUE vertex-support Gallai matching proof certificates.

Imports the source-admitted fifth-core engine UNCHANGED. A complete finite
integer profile audit is distinct from unbounded mathematical proof.
"""
import argparse
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import combinations_with_replacement
import json

import verify_recursive_fifth_core_certificates as previous

prior = previous.prior
red = previous.red
SOURCE = "RECURSIVE_BILATERAL_SUPPORT_BLUE_MATCHING_THEOREM.md/Theorems A-B"
BILATERAL = "BILATERAL_SUPPORT_SINGLE_BLUE_MATCHING_ZERO_DEFICIT"

def bilateral_rule(n,m):
    """Return sound theorem-premise data, or None (UNKNOWN).

    Number of RED components >= BLUE components, both at least three; the
    general supported public classifier has exactly three BLUE components.
    """
    prior.validate(n,m)
    s=len(n)
    if s<3 or len(m)!=3:
        return None
    a=prior.norm(n);b=prior.norm(m)
    U,V=b[:2]
    if V<2:
        return None
    red_vertices=sum(a)+s
    blue_vertices=sum(b)+3
    larger_support=max(red_vertices,blue_vertices)
    if larger_support<3*s-1:
        return None
    p=sum(max(0,a[i]-max(a[i+1]+V-1,
        a[i+2]+U-1 if i+2<s else -10**12)) for i in range(s-1))
    assert p>=0
    assert prior.J(n,m)-prior.J(a,b)==(s+1)*(n[-1]+m[-1]-2)
    assert prior.J(a,b)-(s+1)-prior.J(a,(U-1,V-1))==p
    return {
        "normalized_red":a,"normalized_blue":b,
        "red_vertex_support":red_vertices,"blue_vertex_support":blue_vertices,
        "max_original_support":larger_support,
        "min_matching_edges":s+1,
        "normalized_second_blue_arm":V,
        "blue_matching_loss":p,
        "source_theorem":SOURCE
    }

@lru_cache(None)
def joint(n,m):
    prior.validate(n,m)
    prior_proof=previous.joint(n,m)
    if prior_proof is not None:
        return prior_proof
    rule=bilateral_rule(n,m)
    if rule is not None and rule["blue_matching_loss"]==0:
        assert rule["max_original_support"]>=3*len(n)-1
        assert rule["normalized_second_blue_arm"]>=2
        return prior.leaf(BILATERAL,n,m,{
            **rule,
            "support_supplier":("RED" if rule["red_vertex_support"]>=3*len(n)-1
                                else "BLUE"),
            "source_import":"THREE_BY_THREE_JOINT_RECONSTRUCTION.md/Lemma 1 (two-arm residual)",
        })
    if len(n)<=3:
        return None
    if prior.W(n[1:],m)==prior.J(n,m):
        child=original(n[1:],m)
        if child is not None:
            return prior.leaf("FIRST_RESIDUAL_SHARP_VIA_BILATERAL_RECURSION",n,m,{
                "source_rule":"RECURSIVE_THREE_BLUE_CERTIFICATE_THEOREM.md/R1",
                "strictly_shorter_original":child,
            })
    rule=red.red_loss(n,m)
    if rule is not None and rule["loss"]==0:
        child=joint(rule["shorter_red"],rule["shorter_blue"])
        if child is not None:
            return prior.leaf("RED_MATCHING_VIA_BILATERAL_RECURSION",n,m,{
                "source_rule":"RECURSIVE_RED_MATCHING_CERTIFICATE_THEOREM.md",
                "normalized_red":list(rule["normalized_red"]),
                "normalized_blue":list(rule["normalized_blue"]),
                "shorter_red":list(rule["shorter_red"]),
                "shorter_blue":list(rule["shorter_blue"]),
                "red_matching_loss":0,
                "matching_edges_at_least":rule["matching_lower"],
                "strictly_shorter_joint":child
            })
    return None

@lru_cache(None)
def original(n,m):
    prior.validate(n,m)
    old=previous.original(n,m)
    if old is not None:
        return old
    if len(n)<=3:
        return None
    gate1=prior.transfer(n,m)
    gate4=previous.previous.fourth_core_gate(n,m)
    gate5=previous.fifth_core_gate(n,m)
    if gate1 is None and gate4 is None and gate5 is None:
        return None
    child=joint(n,m)
    if child is None:
        return None
    if gate1 is not None:
        return prior.leaf("ORIGINAL_AFTER_BILATERAL_JOINT_"+gate1,n,m,{
            "source_rule":"GENERAL_CORE_ORIGINAL_TRANSFER.md/Theorem A/conditions1-3",
            "individually_proved_sharp_joint":child,
        })
    if gate4 is not None:
        D=n[0]+m[0]-2
        R=max(sum(n)+len(n),sum(m)+3)
        assert (n[0]-m[0])%2 and 2*prior.W(n,m)<2*D*D+R
        return prior.leaf("ORIGINAL_AFTER_BILATERAL_JOINT_"+gate4,n,m,{
            "source_rule":"GENERAL_CORE_ORIGINAL_TRANSFER.md/Theorem A/condition4",
            "individually_proved_sharp_joint":child,
        })
    D=n[0]+m[0]-2
    R=max(sum(n)+len(n),sum(m)+3)
    W=prior.W(n,m)
    assert gate5==previous.FIFTH and min(n[0],m[0])>=2 and 2*W<=D*D+R
    return prior.leaf("ORIGINAL_AFTER_BILATERAL_JOINT_"+gate5,n,m,{
        "source_rule":"RECURSIVE_FIFTH_CORE_VERTEX_SUPPORT_THEOREM.md/Theorem F",
        "individually_proved_sharp_joint":child,
        "degree_budget":D,"nonisolated_support":R,
        "inclusive_core_margin":D*D+R-2*W
    })

def guard_examples():
    n,m=(3,1,1,1),(4,3,1)
    rule=bilateral_rule(n,m)
    assert rule is not None
    assert rule["red_vertex_support"]==10 and rule["blue_vertex_support"]==11
    assert rule["max_original_support"]==11 and rule["blue_matching_loss"]==0
    assert previous.joint(n,m) is None
    j=joint(n,m)
    assert j is not None and j["proof"]==BILATERAL
    assert prior.J(n,m)==17 and prior.W(n,m)==23
    assert original(n,m) is not None
    # Genuine normalized f,g positive and preservation of both supports.
    for f in range(1,5):
        for g in range(1,5):
            nn=tuple(x+f-1 for x in n)
            mm=tuple(x+g-1 for x in m)
            z=bilateral_rule(nn,mm)
            assert z is not None and z["blue_matching_loss"]==0
            assert z["red_vertex_support"]==10 and z["blue_vertex_support"]==11
            assert prior.J(nn,mm)==17+(len(n)+1)*(f+g-2)
            assert joint(nn,mm) is not None
    # Explicit no-premise examples: support missing on both, V=1, positive loss.
    assert bilateral_rule((1,1,1,1),(2,2,1)) is None
    assert bilateral_rule((3,1,1,1),(4,1,1)) is None
    q=bilateral_rule((8,2,1,1),(4,3,1))
    assert q is not None and q["blue_matching_loss"]>0
    return {"new_joint_example":list(n),"blue_example":list(m),
            "sharp_joint":prior.J(n,m),"sharp_original":prior.W(n,m),
            "positive_terminal_shifts_checked":16}

def audit():
    ct=Counter();digest=sha256();samples={}
    for s in range(3,9):
        for seq in combinations_with_replacement(range(1,9),s-1):
            n=tuple(reversed(seq))+(1,)
            for U in range(2,9):
                for V in range(2,U+1):
                    m=(U,V,1)
                    if prior.canon(n,m)!=prior.canon_alt(n,m):
                        raise AssertionError("independent canonical-index mismatch")
                    oldj=previous.joint(n,m)
                    oldo=previous.original(n,m)
                    nj=joint(n,m)
                    no=original(n,m)
                    assert oldj is None or nj is not None
                    assert oldo is None or no is not None
                    assert no is None or nj is not None or len(n)<=3
                    ct["total"]+=1
                    ct["prior_joint"]+=oldj is not None
                    ct["new_joint"]+=nj is not None
                    ct["prior_original"]+=oldo is not None
                    ct["new_original"]+=no is not None
                    ct["newly_joint"]+=oldj is None and nj is not None
                    ct["newly_original"]+=oldo is None and no is not None
                    ct["joint_unknown"]+=nj is None
                    ct["original_unknown"]+=no is None
                    rule=bilateral_rule(n,m)
                    if (rule is not None and rule["red_vertex_support"]<3*s-1
                            and rule["blue_matching_loss"]==0):
                        ct["bilateral_rescued_zero_loss"]+=1
                        if oldj is None:
                            ct["bilateral_new_direct_joint"]+=1
                        else:
                            ct["bilateral_prior_joint"]+=1
                    catj=nj["proof"] if nj else "UNKNOWN"
                    cato=no["proof"] if no else "UNKNOWN"
                    ct["joint_route_"+catj]+=1
                    ct["original_route_"+cato]+=1
                    if oldj is None and nj is not None and "new_joint" not in samples:
                        samples["new_joint"]={"red":list(n),"blue":list(m),"proof":nj}
                    if oldo is None and no is not None and "new_original" not in samples:
                        samples["new_original"]={"red":list(n),"blue":list(m),"proof":no}
                    digest.update(("%d|%s|%s|%s|%s\n" % (
                        s,",".join(map(str,n)),",".join(map(str,m)),catj,cato)).encode())
    assert ct["total"]==179928
    assert (ct["prior_joint"],ct["prior_original"])==(166589,151885)
    assert (ct["new_joint"],ct["new_original"])==(166663,151940)
    assert (ct["newly_joint"],ct["newly_original"])==(74,55)
    assert ct["bilateral_rescued_zero_loss"]==355
    assert ct["bilateral_prior_joint"]==304
    assert ct["bilateral_new_direct_joint"]==51
    assert (ct["joint_unknown"],ct["original_unknown"])==(13265,27988)
    return {"counts":dict(sorted(ct.items())),
            "classification_sha256":digest.hexdigest(),
            "first_new_examples":samples}

def main():
    a=argparse.ArgumentParser()
    a.add_argument("--red");a.add_argument("--blue")
    a.add_argument("--guard-only",action="store_true")
    a.add_argument("--grid",action="store_true")
    args=a.parse_args()
    print("ERDOS561_BILATERAL_MATCHING_GUARDS",json.dumps(guard_examples(),sort_keys=True))
    if args.red or args.blue:
        if not (args.red and args.blue):a.error("Both red and blue lists required")
        n=tuple(map(int,args.red.split(",")))
        m=tuple(map(int,args.blue.split(",")))
        prior.validate(n,m)
        print("ERDOS561_BILATERAL_EXACT_PROFILE",json.dumps({
            "red":n,"blue":m,"bilateral_rule":bilateral_rule(n,m),
            "joint_certificate":joint(n,m),"original_certificate":original(n,m)
        },sort_keys=True,indent=2))
    if args.grid or not args.guard_only and not args.red:
        r=audit()
        print("ERDOS561_BILATERAL_FULL_GRID",json.dumps(r,sort_keys=True))
        print("ERDOS561_BILATERAL_RECURSIVE_CERTIFICATES_FINITE_PASS")

if __name__=="__main__":
    main()
