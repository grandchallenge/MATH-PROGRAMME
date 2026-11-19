#!/usr/bin/env python3
"""Independent direct colouring audit for both universal Δ4 schemes.
Builds matchings with a DIFFERENT algorithm (NetworkX Edmonds blossom)
than the preceding exact vertex-mask DP, checks every original edge
is assigned exactly once, and recognizes disjoint P3 packing explicitly.
"""
from collections import Counter
from itertools import combinations
from random import Random
import json,os
from pathlib import Path
import networkx as nx

root=Path(__file__).resolve().parent
cert=json.loads((root/'FINAL_22_CASE_CERTIFICATE.json').read_text())
assert len(cert['closed_pairs'])==22

def p3_packing_at_least_three(edges):
    adj={}
    for a,b in edges:
        adj.setdefault(a,set()).add(b)
        adj.setdefault(b,set()).add(a)
    p3=set()
    for center,nbr in adj.items():
        for a,b in combinations(nbr,2):
            p3.add(frozenset((a,b,center)))
    paths=list(p3)
    for i,p in enumerate(paths):
        for j in range(i+1,len(paths)):
            q=paths[j]
            if p.isdisjoint(q):
                for k in range(j+1,len(paths)):
                    if paths[k].isdisjoint(p|q):return True
    return False

def check_graph(G,which):
    assert not G.is_multigraph()
    e=G.number_of_edges()
    assert max((d for _,d in G.degree),default=0)<=4
    assert e<=29
    marked={v for v,d in G.degree if d==4}
    H=G.copy()
    nx.set_edge_attributes(H,{(a,b):int(a in marked)+int(b in marked) for a,b in G.edges},'weight')
    matching=nx.algorithms.matching.max_weight_matching(H,weight='weight')
    M={frozenset(e) for e in matching}
    used=set(v for edge in M for v in edge)
    unmatched=marked-used
    assert len(unmatched)<=len(marked)//5,(G.number_of_nodes(),e,marked,unmatched)
    assert len(unmatched)<=2
    reds=set(M)
    if which=='B':
        reds|={frozenset((a,b)) for a,b in G.edges if a in unmatched or b in unmatched}
    all_edges={frozenset((a,b)) for a,b in G.edges}
    assert len(all_edges)==e
    blue=all_edges-reds
    assert len(blue)+len(reds)==e and reds.isdisjoint(blue)
    red_deg=Counter(v for edge in reds for v in edge)
    blue_deg=Counter(v for edge in blue for v in edge)
    if which=='A':
        assert max(red_deg.values(),default=0)<=1
        assert sum(d==4 for d in blue_deg.values())<=2
    else:
        assert max(blue_deg.values(),default=0)<=3
        assert not p3_packing_at_least_three(reds)
    return len(unmatched)

if __name__=='__main__':
    atlas=0
    for G in nx.graph_atlas_g():
        if max((d for _,d in G.degree),default=0)>4:continue
        check_graph(G,'A')
        check_graph(G,'B')
        atlas+=1
    rng=Random(1561)
    count=0
    for rec in cert['closed_pairs']:
        E=rec['E'];strategy=rec['construction'][0]
        for j in range(15):
            n=max(5,(E+1)//2)+j%4
            G=nx.random_regular_graph(4,n,seed=rng.randint(0,1<<30))
            edges=list(G.edges)
            rng.shuffle(edges)
            for u,v in edges[:2*n-E]:G.remove_edge(u,v)
            assert G.number_of_edges()==E
            check_graph(G,strategy)
            count+=1
    for copies in (1,2):
        G=nx.disjoint_union_all([nx.complete_graph(5) for _ in range(copies)])
        for which in ('A','B'):check_graph(G,which)
    print('TWO_CONSTRUCTIVE_COLORINGS_PASS',{
       'atlas_graph_types':atlas,'atlas_scheme_runs':2*atlas,
       'original_22_pairs_each_tested_on_15_exact_edgecount_hosts':count,
       'separate_K5_obstructions':2,'direct_disjoint_P3_packing_test':True})
