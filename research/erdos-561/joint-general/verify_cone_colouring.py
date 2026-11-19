#!/usr/bin/env python3
"""A constructive witness against at least one joint residual arrowing
condition for EVERY finite simple G with e(G)<2*m1+sum(n), when
len(n)>=3, len(m)>=4. Independently verify via explicit star embeddings.
"""
from collections import Counter
from random import Random
import networkx as nx
from exact_arbitrary_host import forest_masks

CASES=[((1,1,1),(1,1,1,1)),((2,1,1),(3,1,1,1)),
       ((3,1,1),(4,2,1,1)),((3,2,1),(3,2,2,1)),
       ((2,2,2,2),(3,1,1,1)),((4,2,1),(5,2,1,1)),
       ((1,1,1),(4,1,1,1,1)),((4,1,1,1),(4,1,1,1))]

def construct(G,n,m):
    N=sum(n);b=m[0];E=G.number_of_edges()
    assert len(n)>=3 and len(m)>=4 and E<2*b+N and b>=1
    edges={frozenset(e) for e in G.edges}
    if not edges:return 'A',set(),edges,'no_edges'
    v=max(G.nodes,key=lambda u:G.degree[u]);dv=G.degree[v]
    if dv<b:return 'A',set(),edges,'no_blue_leading_star'
    for u in G.nodes:
        if u==v:continue
        dq=G.degree[u]-int(G.has_edge(v,u))
        if E-dv-dq<N:
            blue={e for e in edges if u in e or v in e}
            red=edges-blue
            assert len(red)<N
            return 'B',red,blue,'two_blue_centers'
    high={u for u in G.nodes if u!=v and G.degree[u]>=b}
    assert all(G.has_edge(v,u) for u in high)
    incident=[e for e in edges if v in e]
    red={frozenset((v,u)) for u in high}
    for e in incident:
        if len(red)>=dv-b+1:break
        red.add(e)
    assert len(red)>=dv-b+1
    assert all(v in e for e in red)
    blue=edges-red
    assert max((sum(u in e for e in blue) for u in G.nodes),default=0)<b
    return 'A',red,blue,'one_red_center'

def verify(G,n,m):
    label,red,blue,reason=construct(G,n,m)
    assert len(red)+len(blue)==G.number_of_edges() and not(red&blue)
    # Verify actual ordinary non-induced disjoint star-forest containment.
    if label=='A':
        target_red=n[1:];target_blue=m
    else:
        target_red=n;target_blue=m[1:]
    def contains(colour,target):
        return bool(forest_masks(sorted(tuple(sorted(e)) for e in colour),target))
    assert not contains(red,target_red),(label,'RED_TARGET',n,m,G.edges)
    assert not contains(blue,target_blue),(label,'BLUE_TARGET',n,m,G.edges)
    return reason

if __name__=='__main__':
    rng=Random(5613490);stats=Counter()
    for n,m in CASES:
        limit=2*m[0]+sum(n)
        for z in range(160):
            v=rng.randint(8,18)
            G=nx.Graph();G.add_nodes_from(range(v))
            options=[(a,b) for a in range(v) for b in range(a+1,v)]
            rng.shuffle(options)
            take=rng.randint(0,limit-1)
            G.add_edges_from(options[:take])
            stats[verify(G,n,m)]+=1
    # Deliberately exercise all three distinct construction branches.
    n,m=(2,1,1),(3,1,1,1)
    GA=nx.Graph();GA.add_edges_from([(0,i) for i in range(1,4)]+[(4+2*i,5+2*i) for i in range(6)])
    GB=nx.Graph();GB.add_edges_from([(0,i) for i in range(1,4)]+[(4,i) for i in range(5,8)]+[(8,9),(10,11),(12,13)])
    GC=nx.path_graph(10)
    for graph in (GA,GB,GC):
        assert graph.number_of_edges()<2*m[0]+sum(n)
        stats[verify(graph,n,m)]+=1
    assert stats['one_red_center']>0 and stats['two_blue_centers']>0 and stats['no_blue_leading_star']>0,stats
    print('GENERAL_TWO_CENTER_BOUND_WITNESS_PASS',{'random_graph_parameter_checks':len(CASES)*160,
           'engineered_cases':3,'branches':dict(stats),
           'all_target_avoidance_checked_by_explicit_vertex_disjoint_embeddings':True})
