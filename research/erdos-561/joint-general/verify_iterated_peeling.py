#!/usr/bin/env python3
"""Independent constructive proof auditor. For arbitrary finite SIMPLE
G with e<2*m1+sum(n)+(t-4)*n1, len(n)>=3,len(m)>=4,
return an explicit 2-edge-colouring avoiding ONE of the two residual
Ramsey conditions. Verify via actual vertex-disjoint star embeddings.
"""
from collections import Counter
from random import Random
import networkx as nx
from exact_arbitrary_host import forest_masks

CASES=[((1,1,1),(1,1,1,1)),((2,1,1),(3,1,1,1)),
       ((3,1,1),(4,2,1,1)),((3,2,1),(3,2,2,1)),
       ((2,2,2,2),(3,1,1,1)),((2,1,1),(4,1,1,1,1)),
       ((3,1,1),(4,1,1,1,1,1)),((4,1,1,1),(4,1,1,1,1))]

def certificate(G,n,m):
  assert len(n)>=3 and len(m)>=4
  n=tuple(sorted(n,reverse=True));m=tuple(sorted(m,reverse=True))
  a,b,N,t=n[0],m[0],sum(n),len(m)
  bound=2*b+N+(t-4)*a;E=G.number_of_edges()
  assert E<bound and nx.number_of_selfloops(G)==0
  edges={frozenset(e) for e in G.edges}
  if not edges:return 'A',set(),edges,'no_edges',0
  v=max(G.nodes,key=lambda v:G.degree[v]);dv=G.degree[v]
  if dv<b:return 'A',set(),edges,'max_degree_below_b',0
  Q={e for e in edges if v not in e}
  dq=Counter(x for e in Q for x in e)
  heavy=next((u for u in G.nodes if u!=v and dq[u]>=b),None)
  if heavy is not None:
    H={v,heavy}
    steps=0
    for j in range(t-4):
      red={e for e in edges if e.isdisjoint(H)}
      rd=Counter(x for e in red for x in e)
      center=next((u for u in G.nodes if u not in H and rd[u]>=a),None)
      if center is None:
        blue=edges-red
        assert len(H)<=t-2
        return 'B',red,blue,'no_next_red_leading_star',steps
      H.add(center);steps+=1
    red={e for e in edges if e.isdisjoint(H)}
    blue=edges-red
    assert len(H)==t-2
    assert len(red)<N,(E,b,N,t,len(red),n,m)
    return 'B',red,blue,'iterated_blue_hubs',steps
  # No degree >=b outside v after removing its incident edges.
  high={u for u in G.nodes if u!=v and G.degree[u]>=b}
  assert all(G.has_edge(u,v) for u in high)
  red={frozenset((u,v)) for u in high}
  for e in edges:
    if len(red)>=dv-b+1:break
    if v in e:red.add(e)
  assert len(red)>=dv-b+1 and all(v in e for e in red)
  blue=edges-red
  bd=Counter(u for e in blue for u in e)
  assert max(bd.values(),default=0)<b
  return 'A',red,blue,'one_red_hub',0

def audit(G,n,m):
  label,red,blue,reason,steps=certificate(G,n,m)
  assert len(red)+len(blue)==G.number_of_edges() and red.isdisjoint(blue)
  targets=(n[1:],m) if label=='A' else (n,m[1:])
  def contains(E,target):
    return bool(forest_masks(sorted(tuple(sorted(e)) for e in E),target))
  assert not contains(red,targets[0]),('RED_CONTAINMENT',reason,n,m)
  assert not contains(blue,targets[1]),('BLUE_CONTAINMENT',reason,n,m)
  return reason,steps

if __name__=='__main__':
  rng=Random(5613490);stats=Counter();total=0
  for n,m in CASES:
    a,b=n[0],m[0];L=2*b+sum(n)+(len(m)-4)*a
    for i in range(145):
      N=rng.randint(8,19)
      G=nx.Graph();G.add_nodes_from(range(N))
      options=[(u,v) for u in range(N) for v in range(u+1,N)]
      rng.shuffle(options);E=rng.randrange(L)
      G.add_edges_from(options[:E]);reason,steps=audit(G,n,m)
      stats[reason]+=1;total+=1
      if steps:stats['peeled_centres']+=steps
  # Engineered graphs for all relevant branches and t>=5 peeling.
  H=nx.Graph();H.add_edges_from([(0,i) for i in range(1,5)]+[(5,i) for i in range(6,10)]+[(10,11),(12,13),(14,15)])
  for n,m in [((2,1,1),(4,1,1,1,1)),((3,1,1),(4,1,1,1,1,1))]:
    assert H.number_of_edges()<2*m[0]+sum(n)+(len(m)-4)*n[0]
    reason,steps=audit(H,n,m);stats[reason]+=1;total+=1
  assert stats['one_red_hub'] and stats['iterated_blue_hubs'] and stats['max_degree_below_b'],stats
  print('ITERATED_PEELING_CONSTRUCTIVE_PASS',{'graphs_and_parameter_pairs':total,
    'branch_counts':dict(stats),'all_avoiding_colourings_explicitly_checked':True})
