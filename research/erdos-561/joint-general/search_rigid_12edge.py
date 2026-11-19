#!/usr/bin/env python3
"""Exhaustive finite SUPERCLASS of any E=12 3+4 joint residual
counterexample for n=(3,2,1),m=(3,1,1,1).
From peeling equality: choose two nonadjacent degree-3 vertices v,u;
G - {v,u} has exactly six edges and MUST be F(3,2,1).
Enumerate all ways to connect v,u to that forest plus any new leaves
or common neighbours without loops/multiple edges, enforcing Δ<=3.
"""
from itertools import product
from collections import Counter
import json,hashlib
from pathlib import Path
from exact_arbitrary_host import arrow

base=[(0,1),(0,2),(0,3),(4,5),(4,6),(7,8)]
choices=(1,2,3,4,5,6,7,8)
n=(3,2,1);m=(3,1,1,1)

def graph_components_are_F321(E):
 if len(E)!=6:return False
 verts={v for e in E for v in e}
 adj={v:set() for v in verts}
 for a,b in E:adj[a].add(b);adj[b].add(a)
 rem=set(verts);profile=[]
 while rem:
  v=next(iter(rem));seen={v};todo=[v]
  for w in todo:
   for z in adj[w]:
    if z not in seen:seen.add(z);todo.append(z)
  rem-=seen
  edge_count=sum(len(adj[x]) for x in seen)//2
  assert edge_count>0
  if len(seen)!=edge_count+1 or max(len(adj[x]) for x in seen)!=edge_count:return False
  profile.append(edge_count)
 return sorted(profile,reverse=True)==[3,2,1]

def remaining(E,u,v):return [e for e in E if u not in e and v not in e]

count=Counter();witness=None;borderline=[];digest=hashlib.sha256()
for flags in product(range(4),repeat=len(choices)):
  if flags[3]==3:continue # core K1,2 centre degree 2 cannot take both
  av=sum(z&1!=0 for z in flags);au=sum(z&2!=0 for z in flags)
  if av>3 or au>3:continue
  first=base.copy()
  for x,z in zip(choices,flags):
   if z&1:first.append((9,x))
   if z&2:first.append((10,x))
  for shared in range(min(3-av,3-au)+1):
   E=first.copy();next_vertex=11
   for z in range(shared):
    E.extend([(9,next_vertex),(10,next_vertex)]);next_vertex+=1
   for _ in range(3-av-shared):E.append((9,next_vertex));next_vertex+=1
   for _ in range(3-au-shared):E.append((10,next_vertex));next_vertex+=1
   assert len(E)==12 and max((sum(v in ed for ed in E) for v in {k for ed in E for k in ed}))<=3
   count['candidates']+=1
   digest.update(json.dumps(E,separators=(',',':')).encode()+b'\n')
   if not graph_components_are_F321(remaining(E,9,0)):
    count['fails_rigid_v_centre']+=1;continue
   if not graph_components_are_F321(remaining(E,10,0)):
    count['fails_rigid_u_centre']+=1;continue
   count['passes_two_extra_rigid_pairs']+=1
   b,redblue=arrow(E,n,m[1:])
   if not b:
    count['fails_B_exact']+=1;continue
   count['arrows_B_exact']+=1
   a,redblue=arrow(E,n[1:],m)
   borderline.append({'edges':E,'arrows_B':b,'arrows_A':a,'A_bad_coloring_masks':redblue,'flags':list(flags),'shared_new_neighbours':shared})
   if a:
    witness=E;print('FOUND_UNRESTRICTED_JOINT_COUNTEREXAMPLE',E,flush=True)
    raise SystemExit(2)
   count['fails_A_exact']+=1
expected={'candidates':9194,'passes_two_extra_rigid_pairs':130,'arrows_B_exact':1,
'fails_A_exact':1,'fails_B_exact':129,'fails_rigid_u_centre':910,'fails_rigid_v_centre':8154}
assert dict(count)==expected,(count,expected)
assert len(borderline)==1 and not borderline[0]['arrows_A']
assert witness is None
record={'record_type':'ERDOS561_3X4_RIGID_12_EDGE_FINITE_CERTIFICATE/1',
 'n':[3,2,1],'m':[3,1,1,1], 'conjectured_minimum_edges':13,
 'strict_boundary_12_edge_candidates':count['candidates'],
 'candidate_enumeration_order_sha256':digest.hexdigest(),
 'finite_classification_counts':dict(count),'remaining_borderline_graphs':borderline,
 'remaining_joint_counterexamples':0,
 'claim':'J=13 is proved by unbounded peeling reduction plus complete finite attachment case verification; not the full s,t>=3 theorem'}
Path(__file__).with_name('RIGID_12EDGE_CERTIFICATE.json').write_text(json.dumps(record,indent=2)+'\n')
print('RIGID_12EDGE_COMPLETE_ENUMERATION',dict(count),'REFUTATION',witness,flush=True)
print('BORDERLINE_GRAPH',borderline[0],flush=True)
