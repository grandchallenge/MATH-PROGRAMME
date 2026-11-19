#!/usr/bin/env python3
"""Independent bounded degree-core corroboration on NetworkX graph atlas; not an unbounded proof."""
from collections import Counter
import networkx as nx
stats=Counter()
def split(G,a,b):
    V=G.number_of_nodes()
    edges=list(G.edges())
    red=[0]*V
    blue=[0]*V
    def dfs(i):
        if i==len(edges):return True
        u,v=edges[i]
        if red[u]<a and red[v]<a:
            red[u]+=1;red[v]+=1
            if dfs(i+1):return True
            red[u]-=1;red[v]-=1
        if blue[u]<b and blue[v]<b:
            blue[u]+=1;blue[v]+=1
            if dfs(i+1):return True
            blue[u]-=1;blue[v]-=1
        return False
    return dfs(0)
for G in nx.graph_atlas_g():
    if G.number_of_nodes()<3 or G.number_of_edges()>18:continue
    D=max((d for _,d in G.degree()),default=0)
    if D<2:continue
    C={v for v,d in G.degree() if d==D}
    vmax=sum(d>0 for _,d in G.degree())
    ncore=max(map(len,nx.connected_components(G.subgraph(C))),default=0)
    for a in range(1,D):
        stats["tested"]+=1
        if split(G,a,D-a):continue
        stats["obstructions"]+=1
        assert ncore>=D+1
        assert 2*G.number_of_edges()>=D*(D+1)
        assert vmax<=2*G.number_of_edges()-D*D+1
assert stats["tested"]==4115 and stats["obstructions"]==32,stats
print(dict(stats))
