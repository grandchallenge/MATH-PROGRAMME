#!/usr/bin/env python3
"""Direct bounded cap-partition search; no Lovasz calls. Requires networkx."""
import networkx as nx
from collections import Counter
def split(G,a,b):
 es=sorted(G.edges(),key=lambda z:-(G.degree(z[0])+G.degree(z[1])))
 red={v:0 for v in G};blue={v:0 for v in G}
 def solve(i):
  if i==len(es):return True
  u,v=es[i]
  for d,cap in ((red,a),(blue,b)):
   if d[u]<cap and d[v]<cap:
    d[u]+=1;d[v]+=1
    if solve(i+1):return True
    d[u]-=1;d[v]-=1
  return False
 return solve(0)
count=Counter()
for G in nx.graph_atlas_g():
 if not G.number_of_edges():continue
 D=max(dict(G.degree()).values())
 if D<2 or sum(G.degree(v)==D for v in G)!=D+1:continue
 count['graph_classes']+=1
 isolated=any(len(C)==D+1 and all(G.degree(v)==D for v in C) for C in nx.connected_components(G))
 for a in range(1,D):
  yes=split(G,a,D-a)
  assert (not yes)==(isolated and D%2==0 and a%2==1)
  count['cases']+=1
  count['obstructions']+=not yes
assert (count['graph_classes'],count['cases'],count['obstructions'])==(77,172,20),count
print(dict(count))
