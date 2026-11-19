#!/usr/bin/env python3
"""Fast independent exact test of G -> (2K2, K1,b + qK2)
for arbitrary SIMPLE graph. All red graphs avoiding 2K2 are stars or
triangles; test each without relying on exhaustive 2^E coloring table.
"""
from itertools import combinations
from functools import lru_cache

def blue_contains(blue,b,q):
  # Return an explicit blue (b,1,...,1) witness as original edges.
  adj={}
  for x,y in blue:
    adj.setdefault(x,set()).add(y)
    adj.setdefault(y,set()).add(x)
  def has_matching(edges,need,used=0):
    if need==0:return ()
    if len(edges)<need:return None
    for i,(x,y) in enumerate(edges):
      if x in used or y in used:continue
      out=has_matching(edges[i+1:],need-1,used|{x,y})
      if out is not None:return ((x,y),)+out
    return None
  for v,neigh in adj.items():
    if len(neigh)<b:continue
    for subset in combinations(sorted(neigh),b):
      exclude=set(subset)|{v}
      rem=[edge for edge in blue if not set(edge)&exclude]
      found=has_matching(rem,q,set())
      if found is not None:return tuple((v,u) for u in subset)+found
  return None

def arrow_A(edges,b,q):
  edges=tuple(tuple(sorted(e)) for e in edges)
  assert len(edges)==len(set(edges))
  incident={}
  for i,(u,v) in enumerate(edges):
    incident.setdefault(u,[]).append(i)
    incident.setdefault(v,[]).append(i)
  candidates={0}
  for ids in incident.values():
    for p in range(1<<len(ids)):
      candidates.add(sum(1<<ids[j] for j in range(len(ids)) if p>>j&1))
  E=len(edges)
  for u,v,w in combinations(sorted(incident),3):
    pair={tuple(sorted((u,v))),tuple(sorted((u,w))),tuple(sorted((v,w)))}
    if pair.issubset(edges):
      candidates.add(sum(1<<edges.index(e) for e in pair))
  full=(1<<E)-1
  for redmask in candidates:
    blue=[edges[i] for i in range(E) if not redmask>>i&1]
    if blue_contains(blue,b,q) is None:
      return False,redmask
  return True,None

if __name__=='__main__':
  from exact_arbitrary_host import stars,arrow
  for host in ((4,4,1,1,1,1),(4,4,2,1,1,1),(4,3,2,2,1,1)):
    E=stars(host)
    a,_=arrow(E,(1,1),(4,1,1,1,1))
    b,_=arrow_A(E,4,4)
    print(host,a,b)
    assert a==b
