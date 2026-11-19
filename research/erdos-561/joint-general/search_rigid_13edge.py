#!/usr/bin/env python3
"""Complete rigid E=13 candidate search for the smallest unresolved
3×4 strict-switch pair n=(3,1,1),m=(4,3,1,1).
Conditional on hypothetical joint arrowing and exact degree-center
peeling equality, hosts are precisely F311 plus two nonadjacent degree4
hubs and their 8 attachment edges (plus isolates). Enumerate ALL such
simple graphs up to symmetry of freshly introduced leaf labels.
"""
import sys,json,time,hashlib
from itertools import combinations
from collections import Counter
from exact_arbitrary_host import forest_masks,arrow

n=(3,1,1);m=(4,3,1,1);J=14;E=13
base=((0,1),(0,2),(0,3),(4,5),(6,7))
old=tuple(range(8));hub=(8,9)
subsets=[frozenset(z) for q in range(5) for z in combinations(old,q)]

def build(A,B,shared):
 edges=list(base)
 edges.extend((8,x) for x in sorted(A));edges.extend((9,x) for x in sorted(B))
 v=10
 for _ in range(shared):
  edges.extend(((8,v),(9,v)));v+=1
 for _ in range(4-len(A)-shared):edges.append((8,v));v+=1
 for _ in range(4-len(B)-shared):edges.append((9,v));v+=1
 assert len(edges)==13 and len(set(tuple(sorted(e)) for e in edges))==13
 return edges

def star_red_masks(edges):
 inc={}
 for k,(a,b) in enumerate(edges):
  inc.setdefault(a,[]).append(k);inc.setdefault(b,[]).append(k)
 patterns={0}
 for eids in inc.values():
  for j in range(1<<len(eids)):
   patterns.add(sum(1<<eid for k,eid in enumerate(eids) if j>>k&1))
 Eindex={tuple(sorted(e)):i for i,e in enumerate(edges)}
 for a,b,c in combinations(sorted(inc),3):
  x=[tuple(sorted(e)) for e in ((a,b),(b,c),(a,c))]
  if all(e in Eindex for e in x):patterns.add(sum(1<<Eindex[e] for e in x))
 return patterns

def arrow_first_fast(edges):
 # A red target F(1,1) (matching2); red graphs that avoid it
 # are a star or 3-cycle. Every such coloring must contain full blue m.
 embeddings=forest_masks(edges,m)
 if not embeddings:return False,'no_all_blue_full_target'
 for rm in star_red_masks(edges):
  if not any(emb&rm==0 for emb in embeddings):
   return False,'explicit_red_star_or_triangle_avoids_blue'
 return True,'A_ARROW'

start=int(sys.argv[1]) if len(sys.argv)>1 else 0
stop=int(sys.argv[2]) if len(sys.argv)>2 else len(subsets)
count=Counter();border=[];t0=time.monotonic()
for A in subsets[start:stop]:
 for B in subsets:
  if 0 in A and 0 in B:continue
  for shared in range(min(4-len(A),4-len(B))+1):
   count['all_admissible_attachments']+=1
   # Even all-blue A condition forces >=13 distinct nonisolated
   # vertices to host F(4,3,1,1) with 13 vertices.
   if len(A)+len(B)+shared>5:
    count['too_few_vertices_for_blue_full_target']+=1
    continue
   G=build(A,B,shared)
   count['potential_full_blue_vertex_budget']+=1
   a,reason=arrow_first_fast(G)
   if not a:
    count[reason]+=1
    continue
   count['arrows_A']+=1
   b,avoid=arrow(G,n,m[1:])
   if b:
    result={'n':n,'m':m,'J':J,'host_edges':13,'edges':G,'A':True,'B':True,'oldA':sorted(A),'oldB':sorted(B),'shared':shared}
    print('JOINT_RESIDUAL_REFUTED_WITH_WITNESS',json.dumps(result),flush=True)
    raise SystemExit(2)
   count['fails_B']+=1
   if len(border)<3:border.append({'edges':G,'A':True,'B':False,'B_bad_coloring_masks':avoid})
 count['first_subsets_processed']+=1
print('RIGID13_SEARCH_PARTITION',json.dumps({'start':start,'stop':stop,'total_subsets':len(subsets),'counts':dict(count),'border_examples':border,'seconds':round(time.monotonic()-t0,2)}),flush=True)
