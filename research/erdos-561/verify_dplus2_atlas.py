#!/usr/bin/env python3
"""Independent atlas verification of the sharp D+2 saturated-vertex theorem.
Full two-colour degree-cap brute force on all n<=7 unlabeled graphs.
"""
import json
from collections import Counter
import networkx as nx

def capsplittable(G,alpha,beta):
 E=list(G.edges());D=alpha+beta
 rem=[0]*G.number_of_nodes();red=[0]*len(rem);blue=[0]*len(rem)
 for u,v in E:rem[u]+=1;rem[v]+=1
 # degree-based highest impact sorting
 E.sort(key=lambda e:-(G.degree(e[0])+G.degree(e[1])))
 def go(i):
  if i==len(E):return True
  u,v=E[i]
  if red[u]<alpha and red[v]<alpha:
   red[u]+=1;red[v]+=1
   if go(i+1):return True
   red[u]-=1;red[v]-=1
  if blue[u]<beta and blue[v]<beta:
   blue[u]+=1;blue[v]+=1
   if go(i+1):return True
   blue[u]-=1;blue[v]-=1
  return False
 return go(0)

def isolated_clique(G,D):
 for cc in nx.connected_components(G):
  if len(cc)==D+1 and G.subgraph(cc).number_of_edges()==D*(D+1)//2:
   return True
 return False

def run():
 stats=Counter();examples=[]
 for G in nx.graph_atlas_g():
  D=max((d for _,d in G.degree()),default=0)
  if D<2:continue
  nD=sum(d==D for _,d in G.degree())
  stats['graphs_atlas_with_D_ge2']+=1
  for a in range(1,D):
   stats['total_cap_graph_tests']+=1
   splittable=capsplittable(G,a,D-a)
   if nD<=D+2:
    stats['below_threshold_tests']+=1
    expected_failure=(D%2==0 and a%2==1 and isolated_clique(G,D))
    if splittable==expected_failure:
     examples.append((nx.to_graph6_bytes(G,header=False).decode().strip(),D,a,nD))
     raise AssertionError('Prediction failure '+str(examples[-1]))
    if not splittable:stats['below_threshold_obstructions']+=1
   else:
    stats['above_threshold_tests']+=1
    if not splittable:
     stats['above_threshold_obstructions']+=1
     if not isolated_clique(G,D):stats['nonclique_above_threshold_obstructions']+=1
 return dict(stats)
if __name__=='__main__':print(json.dumps(run(),indent=2))
