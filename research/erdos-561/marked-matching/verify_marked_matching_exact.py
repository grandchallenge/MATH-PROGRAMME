#!/usr/bin/env python3
"""Independent exact verification of designated-vertex Tutte/Berge deficiency
and floor(k4/5) matching coverage bound for maximum-degree-four graphs.
Brute exponential DP (no NetworkX matching algorithm) vs exhaustive
S-subset odd-component deficiency and explicit matching reconstruction.
"""
from functools import lru_cache
from random import Random
from collections import Counter
import networkx as nx

def graph_data(G):
    vertices=list(G.nodes)
    z={v:i for i,v in enumerate(vertices)}
    N=len(vertices)
    nbr=[0]*N
    for a,b in G.edges:
        i,j=z[a],z[b]
        assert i!=j
        nbr[i]|=1<<j;nbr[j]|=1<<i
    U=sum(1<<i for i in range(N) if nbr[i].bit_count()==4)
    assert max((m.bit_count() for m in nbr),default=0)<=4
    return nbr,U

def matching_exact(nbr,U):
    n=len(nbr);full=(1<<n)-1
    @lru_cache(None)
    def match(mask):
        if not mask:return (0,())
        bit=mask&-mask;i=bit.bit_length()-1
        score,ex=match(mask^bit)
        eligible=nbr[i] & (mask^bit)
        while eligible:
            nextbit=eligible&-eligible;j=nextbit.bit_length()-1
            value,old=match(mask^bit^nextbit)
            value+=((U>>i)&1)+((U>>j)&1)
            if value>score:score,ex=value,old+((i,j),)
            eligible^=nextbit
        return score,ex
    score,edges=match(full)
    used=set()
    for i,j in edges:
        assert i!=j and (nbr[i]>>j)&1
        assert i not in used and j not in used
        used.update((i,j))
    assert score==sum((U>>i)&1 for i in used)
    return score,edges

def components(nbr,remaining):
    comps=[]
    while remaining:
        start=remaining&-remaining
        block=start
        frontier=start
        while frontier:
            i=(frontier&-frontier).bit_length()-1
            frontier &= frontier-1
            extra=nbr[i]&remaining&~block
            block|=extra
            frontier|=extra
        comps.append(block)
        remaining &=~block
    return comps

def deficiency_exact(nbr,U):
    n=len(nbr);full=(1<<n)-1
    value=0;witness=0
    for S in range(1<<n):
        odd=sum(1 for comp in components(nbr,full^S)
                if (comp&~U)==0 and comp.bit_count()%2==1)
        deficit=odd-S.bit_count()
        if deficit>value:value,witness=deficit,S
    return value,witness

def check(G):
    nbr,U=graph_data(G)
    k=U.bit_count()
    covered,M=matching_exact(nbr,U)
    deficient,wit=deficiency_exact(nbr,U)
    assert k-covered==deficient,(len(nbr),k,covered,deficient)
    assert deficient<=k//5,(len(nbr),k,deficient)
    assert k-covered<=k//5
    # Direct red=M, blue=E\M coloring. Blue degree4 only at
    # uncovered originally degree4 vertices; red has no 2-edge star.
    matching={tuple(sorted((u,v))) for u,v in M}
    blue_degree=Counter()
    for u,adj in enumerate(nbr):
        for v in range(u+1,len(nbr)):
            if (adj>>v)&1 and (u,v) not in matching:
                blue_degree[u]+=1;blue_degree[v]+=1
    four=sum(blue_degree[u]==4 for u in range(len(nbr)))
    assert four==k-covered
    return k,deficient

if __name__=='__main__':
    results=Counter()
    atlas=0
    for G in nx.graph_atlas_g():
        if max((d for _,d in G.degree),default=0)>4:continue
        check(G);atlas+=1
    rng=Random(561)
    random_tests=0
    for n in range(8,12):
        for trial in range(65):
            G=nx.Graph();G.add_nodes_from(range(n))
            edgelist=[(u,v) for u in range(n) for v in range(u+1,n)]
            rng.shuffle(edgelist)
            for u,v in edgelist:
                if G.degree[u]<4 and G.degree[v]<4 and rng.random()<0.6:G.add_edge(u,v)
            k,deficit=check(G)
            results[(k,deficit)]+=1
            random_tests+=1
    for copies in (1,2,3,4):
        G=nx.disjoint_union_all([nx.complete_graph(5) for _ in range(copies)])
        k,deficit=check(G)
        assert (k,deficit)==(5*copies,copies)
    print('MARKED_MATCHING_EXACT_PASS',{
       'atlas_graphs':atlas,'random_graphs':random_tests,
       'disjoint_K5_sharpness_instances':4,'matching_coverage_equals_odd_component_max_deficiency':True,
       'deficiency_bound':'unmatched_degree4 <= floor(count_degree4/5)',
       'max_tested_order':20})
