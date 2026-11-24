#!/usr/bin/env python3
"""New source-backed factorcritical component-size rule for Erdős #561.

Imports 52-claim protected recursive certificates without modifying them.
Paper-level theorem is UNDER_REVIEW; this finite proof trace is only CHECKED.
UNKNOWN is neither a counterexample nor a certification of conjecture failure.
"""
import argparse
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, combinations_with_replacement
import json

import verify_recursive_vertex_budget_certificates as prior
import verify_recursive_red_matching_certificates as red
import verify_recursive_three_blue_certificates as base

PROOF="SMALL_FACTORCRITICAL_COMPONENT_BLUE_MATCHING"

def guard(n,m):
    """Exact sufficient condition and quantitative residual lower from new paper."""
    base.validate(n,m)
    a,b=base.norm(n),base.norm(m)
    s=len(a)
    if b[1]<2:
        return None
    E=sum(z-1 for z in a)
    gamma=2*(s//(E+1))
    interference=base.blue_loss(a,b)
    # Counts and the gap are independent of the host topology.
    assert base.J(a,b)-(s+1)-base.J(a,(b[0]-1,b[1]-1))==interference
    return {"normalized_red":a,"normalized_blue":b,
            "red_component_count":s,"red_excess_E":E,
            "red_vertex_support":2*s+E,
            "factorcritical_small_component_2floor":gamma,
            "blue_two_star_edge_sum":b[1]+1,
            "matching_s_plus_one_proved":gamma<=b[1]+1,
            "interference_P":interference,
            "unconditional_deficit":interference+n[-1]+m[-1]-1}

@lru_cache(None)
def joint(n,m):
    base.validate(n,m)
    old=prior.joint(n,m)
    if old is not None:return old
    q=guard(n,m)
    if q and q["matching_s_plus_one_proved"] and q["interference_P"]==0:
        return base.leaf(PROOF,n,m,{
            "source_theorem":"FACTORCRITICAL_COMPONENT_ORDER_MATCHING_THEOREM.md/Theorems A-B",
            "normalized_red":list(q["normalized_red"]),
            "normalized_blue":list(q["normalized_blue"]),
            "E":q["red_excess_E"],
            "two_floor_s_over_E_plus_one":q["factorcritical_small_component_2floor"],
            "blue_two_star_size_sum":q["blue_two_star_edge_sum"],
            "minimum_matching_edges":len(n)+1,
            "blue_interference_P":0})
    if len(n)<=3:return None
    if base.W(n[1:],m)==base.J(n,m):
        child=original(n[1:],m)
        if child is not None:
            return base.leaf("FIRST_RESIDUAL_SHARP_VIA_COMPONENT_ORDER_RECURSION",n,m,{
                "source_theorem":"RECURSIVE_THREE_BLUE_CERTIFICATE_THEOREM.md/R1",
                "shorter_red_original_certificate":child})
    r=red.red_loss(n,m)
    if r and r["loss"]==0:
        child=joint(r["shorter_red"],r["shorter_blue"])
        if child is not None:
            return base.leaf("RED_MATCHING_VIA_COMPONENT_ORDER_RECURSION",n,m,{
                "source_theorem":"RECURSIVE_RED_MATCHING_CERTIFICATE_THEOREM.md/Theorem A",
                "shorter_red":list(r["shorter_red"]),
                "shorter_blue":list(r["shorter_blue"]),
                "zero_matching_loss":True,
                "shorter_joint_certificate":child})
    return None

@lru_cache(None)
def original(n,m):
    base.validate(n,m)
    old=prior.original(n,m)
    if old is not None:return old
    if len(n)<=3:return None
    transfer=base.transfer(n,m)
    fourth=prior.fourth_core_gate(n,m)
    if transfer is None and fourth is None:return None
    child=joint(n,m)
    if child is None:return None
    if transfer is not None:
        source="GENERAL_CORE_ORIGINAL_TRANSFER.md/Theorem A/conditions 1-3"
        label="ORIGINAL_TRANSFER_AFTER_COMPONENT_ORDER_"+transfer
    else:
        source="GENERAL_CORE_ORIGINAL_TRANSFER.md/Theorem A/condition 4"
        label="ORIGINAL_TRANSFER_AFTER_COMPONENT_ORDER_"+fourth
    return base.leaf(label,n,m,{
        "source_theorem":source,
        "same_profile_joint_certificate":child,
        "D":n[0]+m[0]-2,"W":base.W(n,m)})

def positive_compositions(s):
    for k in range(1,s+1):
        def recurse(rem,count):
            if count==0:
                if rem==0:yield ()
                return
            for a in range(1,rem-count+2):
                for tail in recurse(rem-a,count-1):
                    yield (a,)+tail
        yield from recurse(s,k)

def nontriangular_factorcritical_graph_witness():
    """Actual 2K7 witness: BOTH factorcritical components have matching number 3.

    Each deletion retains full RED (2,1,1,1,1,1). Yet the entire two-component
    graph has a colouring avoiding that RED target and BLUE (5,1).
    Demonstrates why the old all-triangle proof cannot establish this case.
    """
    C0=tuple(range(7))
    C1=tuple(range(7,14))
    edges=frozenset(frozenset((x,y)) for C in (C0,C1)
                    for x,y in combinations(C,2))
    assert len(edges)==42
    def valid_star(support,centre,leaves):
        assert centre in support and all(z in support for z in leaves)
        assert len(leaves)==len(set(leaves)) and centre not in leaves
        return all(frozenset((centre,l)) in edges for l in leaves)
    # Every Q-x retains an ordinary (not necessarily induced) RED target,
    # with star supports occupying ALL thirteen surviving vertices:
    # intact K7 holds P3+2K2; six-vertex remainder holds 3K2.
    for t in range(14):
        intact=C1 if t in C0 else C0
        rem=tuple(x for x in (C0 if t in C0 else C1) if x!=t)
        assert len(intact)==7 and len(rem)==6
        assert valid_star(intact,intact[0],intact[1:3])
        stars=[(intact[0],intact[1:3])]
        stars.extend((intact[j],(intact[j+1],)) for j in (3,5))
        stars.extend((rem[j],(rem[j+1],)) for j in (0,2,4))
        assert tuple(len(x[1]) for x in stars)==(2,1,1,1,1,1)
        supports=[]
        for centre,leaves in stars:
            assert valid_star(tuple(range(14)),centre,leaves)
            supports.extend((centre,)+tuple(leaves))
        assert len(supports)==13 and len(set(supports))==13
    # Colour C0 RED and C1 BLUE. Each monochromatic graph only has
    # seven supported vertices, whereas RED target needs 13 and BLUE
    # (5,1) requires eight. The colouring is an ordinary graph witness.
    red=tuple(e for e in edges if e.issubset(C0))
    blue=tuple(e for e in edges if e.issubset(C1))
    assert len(red)==len(blue)==21
    red_support=set().union(*red)
    blue_support=set().union(*blue)
    assert len(red_support)==7<13
    assert len(blue_support)==7<8
    assert 2*(6//(1+1))==6<=5+1
    return {"checked_vertex_deletions":14,
            "nontriangular_factorcritical_components":2,
            "actual_edges":42}

def independent_matching_lemma_audit():
    ct=Counter()
    # Exhaustively enumerate all factorcritical matching number partitions
    # in the declared range, including large components not just triangles.
    for s in range(2,11):
        for E in range(0,s+2):
            gamma=2*(s//(E+1))
            for B in range(2,2*s+4):  # v+g sum, both positive
                if gamma>B:continue
                for p in positive_compositions(s):
                    c=len(p)
                    if c<E+1:continue
                    assert min(p)*2<=B,(s,E,B,p)
                    assert 2*s+c-1>=2*s+E
                    ct["factorcritical_component_order_inequalities"]+=1
    # Source and independent exact antidiagonals, including nonterminal shifts.
    for n,m in [
        ((3,1,1,1),(3,2,1)),
        ((3,3,2,2,1),(6,4,1)),
        ((6,4,2,2),(8,5,3)),
        ((5,3,2,1,1,1),(7,4,2)),
        ((1,1,1,1),(5,4,1)),
    ]:
        assert base.canon(n,m)==base.canon_alt(n,m)
        x=guard(n,m)
        if x is None:continue
        assert x["unconditional_deficit"]>=x["interference_P"]+1
        assert x["red_vertex_support"]==sum(x["normalized_red"])+len(n)
        assert x["factorcritical_small_component_2floor"]==2*(len(n)//(x["red_excess_E"]+1))
        ct["explicit_guard_examples"]+=1
    n,m=(3,1,1,1),(3,2,1)
    assert prior.joint(n,m) is None
    x=guard(n,m)
    assert x and x["red_vertex_support"]<3*len(n)-1
    assert x["matching_s_plus_one_proved"] and x["interference_P"]==0
    assert base.J(n,m)==13 and base.W(n,m)==18
    p=joint(n,m);o=original(n,m)
    assert p and p["proof"]==PROOF
    assert o and o["original_canonical"]==18
    ct["concrete_new_joint_and_original_graph_theorem"]+=1
    witness=nontriangular_factorcritical_graph_witness()
    assert witness["checked_vertex_deletions"]==14
    ct["nontriangular_all_vertex_deletion_witnesses"]+=14
    ct["nontriangular_actual_avoiding_graph_colouring"]+=1
    return ct

def full_grid_audit():
    ct=Counter();fingerprint=sha256();examples={}
    for s in range(3,9):
        for pref in combinations_with_replacement(range(1,9),s-1):
            n=tuple(reversed(pref))+(1,)
            for U in range(2,9):
                for V in range(2,U+1):
                    m=(U,V,1)
                    assert base.canon(n,m)==base.canon_alt(n,m)
                    oldJ,oldO=prior.joint(n,m),prior.original(n,m)
                    newJ,newO=joint(n,m),original(n,m)
                    assert oldJ is None or newJ is not None
                    assert oldO is None or newO is not None
                    assert newO is None or newJ is not None or len(n)<=3
                    x=guard(n,m)
                    supported_old=base.red_support(base.norm(n))
                    if not supported_old and x and x["interference_P"]==0:
                        ct["low_support_zero_P"]+=1
                        if x["matching_s_plus_one_proved"]:
                            ct["new_guard_low_support"]+=1
                            if oldJ is None:ct["new_guard_old_engine_unknown"]+=1
                    ct["total"]+=1
                    ct["old_joint"]+=oldJ is not None
                    ct["new_joint"]+=newJ is not None
                    ct["old_original"]+=oldO is not None
                    ct["new_original"]+=newO is not None
                    ct["new_joint_over_old"]+=(oldJ is None and newJ is not None)
                    ct["new_original_over_old"]+=(oldO is None and newO is not None)
                    ct["remaining_joint_unknown"]+=newJ is None
                    key=newJ["proof"] if newJ else "UNKNOWN"
                    ct["joint_"+key]+=1
                    if oldJ is None and newJ is not None and "new_joint" not in examples:
                        examples["new_joint"]={"n":list(n),"m":list(m),"proof":newJ}
                    if oldO is None and newO is not None and "new_original" not in examples:
                        examples["new_original"]={"n":list(n),"m":list(m),"proof":newO}
                    fingerprint.update(("%d|%s|%s|%s|%s\n"%(
                        s,",".join(map(str,n)),",".join(map(str,m)),
                        key,newO["proof"] if newO else "UNKNOWN")).encode())
    assert ct["total"]==179928
    assert (ct["old_joint"],ct["old_original"])==(165741,132393)
    assert ct["low_support_zero_P"]==1959
    assert ct["new_guard_low_support"]==1671
    assert ct["new_guard_old_engine_unknown"]==826
    assert ct["new_joint"]==ct["old_joint"]+ct["new_joint_over_old"]
    assert ct["new_original"]==ct["old_original"]+ct["new_original_over_old"]
    return {"counts":dict(sorted(ct.items())),
            "classification_sha256":fingerprint.hexdigest(),
            "examples":examples}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--red");ap.add_argument("--blue")
    ap.add_argument("--grid",action="store_true")
    z=ap.parse_args()
    print("ERDOS561_FACTORCRITICAL_ORDER_GUARDS",json.dumps(dict(independent_matching_lemma_audit()),sort_keys=True))
    if z.red or z.blue:
        if not(z.red and z.blue):ap.error("both red and blue are required")
        n=tuple(int(t) for t in z.red.split(","))
        m=tuple(int(t) for t in z.blue.split(","))
        base.validate(n,m)
        print("ERDOS561_FACTORCRITICAL_ORDER_CERTIFICATE",json.dumps({
            "red":n,"blue":m,"guard":guard(n,m),
            "joint":joint(n,m),"original":original(n,m)},sort_keys=True,indent=2))
    if z.grid or not z.red:
        result=full_grid_audit()
        print("ERDOS561_FACTORCRITICAL_ORDER_CLASSIFICATION",json.dumps(result,sort_keys=True))
    print("ERDOS561_FACTORCRITICAL_COMPONENT_ORDER_FINITE_PASS")

if __name__=="__main__":
    main()
