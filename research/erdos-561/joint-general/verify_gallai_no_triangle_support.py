#!/usr/bin/env python3
"""GCL Erdős #561: no-triangle factor-critical support sharpening and finite proof traces.

Proof of the graph lemma is mathematical, in companion manuscript.
Code checks exact arithmetic, monotone recursive sufficient certificates, and
actual vertex-disjoint graph avoiding-colouring witnesses. Not MATHCERT.
"""
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, combinations_with_replacement
import json
import verify_recursive_fifth_core_certificates as old

prior=old.prior
red=old.red

def improved_support(n):
    s=len(n)
    return sum(n)+s >= 2*s+s//2

@lru_cache(None)
def joint(n,m):
    prior.validate(n,m)
    oldproof=old.joint(n,m)
    if oldproof is not None:
        return oldproof
    if len(n)<=3:
        return None
    a,b=prior.norm(n),prior.norm(m)
    if b[1]>=2 and improved_support(a) and prior.blue_loss(a,b)==0:
        assert not prior.red_support(a), "new leaf should not duplicate protected old blue rule"
        return prior.leaf("SHARPENED_GALLAI_NO_TRIANGLE_BLUE_ZERO_DEFICIT",n,m,{
            "source_theorem":"GALLAI_NO_TRIANGLE_SUPPORT_SHARPENING_THEOREM.md/Lemma T, Corollary U",
            "normalized_red":list(a),"normalized_blue":list(b),
            "normalized_red_vertex_support":sum(a)+len(a),
            "new_required_support":2*len(a)+len(a)//2,
            "old_required_support":3*len(a)-1,
            "blue_matching_deficit":0,
            "nontrivial_factorcritical_matching_at_least":2,
            "triangle_component_eliminated_by_explicit_avoiding_colouring":True})
    # Use this stronger oracle as input to source-proved well-founded R1 and
    # red-matching inferences. Both recurse to STRICTLY shorter red lists.
    if prior.W(n[1:],m)==prior.J(n,m):
        child=original(n[1:],m)
        if child is not None:
            return prior.leaf("SHARPENED_GALLAI_FIRST_RESIDUAL_ORIGINAL",n,m,{
                "source_rule":"RECURSIVE_THREE_BLUE_CERTIFICATE_THEOREM.md/R1",
                "strictly_shorter_original":child})
    rule=red.red_loss(n,m)
    if rule is not None and rule["loss"]==0:
        child=joint(rule["shorter_red"],rule["shorter_blue"])
        if child is not None:
            return prior.leaf("SHARPENED_GALLAI_RED_MATCHING_RECURSION",n,m,{
                "source_rule":"RECURSIVE_RED_MATCHING_CERTIFICATE_THEOREM.md",
                "loss":0,"shorter_red":list(rule["shorter_red"]),
                "shorter_blue":list(rule["shorter_blue"]),
                "strictly_shorter_joint":child})
    return None

@lru_cache(None)
def original(n,m):
    prior.validate(n,m)
    oldproof=old.original(n,m)
    if oldproof is not None:
        return oldproof
    if len(n)<=3:
        return None
    prior_gate=prior.transfer(n,m)
    fourth=old.previous.fourth_core_gate(n,m)
    fifth=old.fifth_core_gate(n,m)
    if prior_gate is None and fourth is None and fifth is None:
        return None
    child=joint(n,m)
    if child is None:
        return None
    source=("GENERAL_CORE_ORIGINAL_TRANSFER.md/Theorem A" if prior_gate or fourth
            else "RECURSIVE_FIFTH_CORE_VERTEX_SUPPORT_THEOREM.md/Theorem F")
    return prior.leaf("SHARPENED_GALLAI_ORIGINAL_TRANSFER_"+str(prior_gate or fourth or fifth),
            n,m,{"source_theorem":source,"joint_proof":child})

def actual_graph_contains(edges,profile):
    adj={}
    for x,y in edges:
        adj.setdefault(x,set()).add(y);adj.setdefault(y,set()).add(x)
    choices=[]
    for arm in sorted(profile,reverse=True):
        triples=set()
        for centre,near in adj.items():
            for leaves in combinations(sorted(near),arm):
                triples.add(frozenset((centre,)+leaves))
        choices.append(tuple(triples))
    if any(not z for z in choices):return False
    @lru_cache(None)
    def search(pos,used):
        if pos==len(choices):return True
        return any(used.isdisjoint(v) and search(pos+1,used|v) for v in choices[pos])
    return search(0,frozenset())

def audit():
    counts=Counter();fingerprint=sha256();examples={}
    for s in range(3,9):
        for prefix in combinations_with_replacement(range(1,9),s-1):
            n=tuple(reversed(prefix))+(1,)
            oldsupport=prior.red_support(n)
            newsupport=improved_support(n)
            assert not oldsupport or newsupport
            for U in range(2,9):
                for V in range(2,U+1):
                    m=(U,V,1);loss=prior.blue_loss(n,m)
                    assert prior.canon(n,m)==prior.canon_alt(n,m)
                    counts["total"]+=1
                    counts["old_support"]+=oldsupport
                    counts["improved_support"]+=newsupport
                    counts["new_support_only"]+=newsupport and not oldsupport
                    counts["old_support_zero_loss"]+=oldsupport and loss==0
                    counts["improved_support_zero_loss"]+=newsupport and loss==0
                    counts["new_support_zero_loss_only"]+=newsupport and not oldsupport and loss==0
                    oldj=old.joint(n,m);oldo=old.original(n,m)
                    newj=joint(n,m);newo=original(n,m)
                    assert oldj is None or newj is not None
                    assert oldo is None or newo is not None
                    counts["old_joint"]+=oldj is not None
                    counts["old_original"]+=oldo is not None
                    counts["new_joint"]+=newj is not None
                    counts["new_original"]+=newo is not None
                    if newj is not None and oldj is None:
                        counts["newly_joint"]+=1
                        kind=newj["proof"]
                        counts["new_joint_"+kind]+=1
                        if "first_new_joint" not in examples:examples["first_new_joint"]=newj
                    if newo is not None and oldo is None:
                        counts["newly_original"]+=1
                        if "first_new_original" not in examples:examples["first_new_original"]=newo
                    state=(newj["proof"] if newj else "UNKNOWN",
                           newo["proof"] if newo else "UNKNOWN")
                    fingerprint.update((str((n,m))+repr(state)+"\\n").encode())
    counts["remaining_joint_unknown"]=counts["total"]-counts["new_joint"]
    counts["remaining_original_unknown"]=counts["total"]-counts["new_original"]
    # Elimination of the K3 factor-critical component: graph witness for each s.
    # In a graph with sK3, colour one whole component BLUE and s-1 RED.
    for s in range(3,10):
        edges=[(3*i+j,3*i+(j+1)%3) for i in range(s) for j in range(3)]
        red_edges=tuple(e for e in edges if e[0]//3<s-1)
        blue_edges=tuple(e for e in edges if e[0]//3==s-1)
        assert not actual_graph_contains(red_edges,(2,)*(s-1)+(1,))
        assert not actual_graph_contains(blue_edges,(1,1))
        counts["K3_factorcritical_component_avoiding_witnesses"]+=1
    return {"counts":dict(sorted(counts.items())),
            "fingerprint":fingerprint.hexdigest(),"examples":examples}

if __name__=="__main__":
    result=audit()
    c=result["counts"]
    assert c["total"]==179928
    assert (c["old_support"],c["improved_support"])==(177856,179368)
    assert (c["old_support_zero_loss"],c["improved_support_zero_loss"])==(134447,135852)
    assert c["new_support_only"]==1512
    assert c["new_support_zero_loss_only"]==1405
    assert c["new_joint"]>=c["old_joint"]==166589
    assert c["new_original"]>=c["old_original"]==151885
    print("ERDOS561_GALLAI_NO_TRIANGLE_SUPPORT_FULL_GRID",json.dumps(result,sort_keys=True))
    print("ERDOS561_GALLAI_NO_TRIANGLE_SUPPORT_FINITE_PASS")
