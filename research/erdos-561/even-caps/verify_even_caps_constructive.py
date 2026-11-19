#!/usr/bin/env python3
"""Constructive (2,2) edge partition for EVERY simple graph Delta<=4.
Uses a 4-regular multigraph completion, Euler orientation and a perfect
matching in the associated bipartite 2-regular multigraph. Dummy edges
are dropped at the end. All atlas graphs n<=7 checked; deterministic
random larger graphs included as smoke tests. Math proof separate.
"""
import networkx as nx
from collections import Counter
from random import Random

def split_even_caps(G):
    V=list(G.nodes)
    assert all(d<=4 for _,d in G.degree)
    H=nx.MultiGraph()
    H.add_nodes_from(V)
    physical=[]
    for u,v in G.edges:
        physical.append((u,v,True))
    stubs=[]
    for v in V:stubs += [v]*(4-G.degree[v])
    assert len(stubs)%2==0
    for i in range(0,len(stubs),2):
        physical.append((stubs[i],stubs[i+1],False))
    for eid,(u,v,_) in enumerate(physical):H.add_edge(u,v,key=eid)
    assert all(d==4 for _,d in H.degree)
    oriented=[]
    for component in nx.connected_components(H):
        q=next(iter(component))
        oriented.extend(nx.eulerian_circuit(H.subgraph(component),source=q,keys=True))
    assert len(oriented)==len(physical)
    B=nx.Graph()
    left={('out',v) for v in V};right={('in',v) for v in V}
    B.add_nodes_from(left,bipartite=0)
    B.add_nodes_from(right,bipartite=1)
    for u,v,eid in oriented:B.add_edge(('out',u),('in',v))
    mate=nx.algorithms.bipartite.maximum_matching(B,top_nodes=left)
    assert all(x in mate for x in left)
    colors={}
    used_left=set()
    for u,v,eid in oriented:
        # One matching edge outgoing from each u; graph pair mate may
        # be represented by multiple physical edges, choose first.
        if mate[('out',u)]==('in',v) and u not in used_left:
            colors[eid]=0;used_left.add(u)
        else:colors[eid]=1
    assert len(colors)==len(physical)
    red=[];blue=[]
    for eid,(u,v,orig) in enumerate(physical):
        if not orig:continue
        (red if colors[eid]==0 else blue).append((u,v))
    assert len(red)+len(blue)==G.number_of_edges()
    for edges in (red,blue):
        deg=Counter()
        for u,v in edges:
            deg[u]+=1;deg[v]+=1
        assert max(deg.values(),default=0)<=2
    return len(red),len(blue)

if __name__=='__main__':
    tested=0;active=0
    for G in nx.graph_atlas_g():
        if len(G)>7:continue
        if max((d for _,d in G.degree),default=0)>4:continue
        tested+=1
        if G.number_of_edges():active+=1
        split_even_caps(G)
    rand=Random(561)
    random_done=0
    for n in (8,10,12,16,24):
        for trial in range(40):
            G=nx.Graph();G.add_nodes_from(range(n))
            order=list(range(n));rand.shuffle(order)
            for u in order:
                for v in order:
                    if u>=v:continue
                    if G.degree[u]>=4 or G.degree[v]>=4:continue
                    if rand.random()<0.35:G.add_edge(u,v)
            split_even_caps(G);random_done+=1
    print('EVEN_CAPS_CONSTRUCTIVE_PASS',{'all_atlas_graphs_maxdegree_at_most_4':tested,
                                     'with_edges':active,'larger_random_graphs':random_done})
