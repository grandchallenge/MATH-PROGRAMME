#!/usr/bin/env python3
"""Second independent enumeration of EVERY E=13 candidate forced by
peeling equality for (3,1,1) vs (4,3,1,1). Independent disjoint forest
embedding masks and independent all-colouring oracle on A-positive set.
"""
from itertools import product,combinations
from collections import Counter
import json
from pathlib import Path

base=((0,1),(0,2),(0,3),(4,5),(6,7))
old=tuple(range(8));flags=range(4)

def embeddings(edges,target):
  vertices=set(v for edge in edges for v in edge)
  adj={v:[] for v in vertices}
  for i,(u,v) in enumerate(edges):adj[u].append((v,i));adj[v].append((u,i))
  options={}
  for d in set(target):
    options[d]=[]
    for centre in vertices:
      for group in combinations(adj[centre],d):
        vert={centre};mask=0
        for v,idx in group:vert.add(v);mask|=1<<idx
        options[d].append((frozenset(vert),mask))
  found=set()
  def recurse(j,used,mask):
    if j==len(target):found.add(mask);return
    for used2,m in options[target[j]]:
      if not used2&used:recurse(j+1,used|used2,mask|m)
  recurse(0,frozenset(),0)
  return found

def arrow(edges,R,B):
  E=len(edges);size=1<<E;allmask=size-1
  red=bytearray(size);blue=bytearray(size)
  for x in embeddings(edges,R):red[x]=1
  for x in embeddings(edges,B):blue[x]=1
  for k in range(E):
    bit=1<<k
    for x in range(size):
      if x&bit:
        red[x]|=red[x^bit];blue[x]|=blue[x^bit]
  for mask in range(size):
    if not red[mask] and not blue[allmask^mask]:return False,(mask,allmask^mask)
  return True,None

def red_mask_options(edges):
  incident={}
  for k,(u,v) in enumerate(edges):
    incident.setdefault(u,[]).append(k);incident.setdefault(v,[]).append(k)
  options={0}
  for ids in incident.values():
    for bits in range(1<<len(ids)):
      options.add(sum((1<<eid) for i,eid in enumerate(ids) if bits>>i&1))
  index={tuple(sorted(e)):k for k,e in enumerate(edges)}
  for x,y,z in combinations(sorted(incident),3):
    e=[tuple(sorted(xy)) for xy in ((x,y),(x,z),(y,z))]
    if all(xy in index for xy in e):options.add(sum(1<<index[xy] for xy in e))
  return options

def first_condition(edges):
  # Red two disjoint edges is a matching2. Red avoids it iff a star
  # or triangle, so we enumerate all such red edge subsets.
  blue_emb=embeddings(edges,(4,3,1,1))
  if not blue_emb:return False
  for R in red_mask_options(edges):
    if not any((mask&R)==0 for mask in blue_emb):return False
  return True

stats=Counter();border=[]
for pattern in product(flags,repeat=8):
  if pattern[0]==3:continue # 3-star centre can take only 1 more edge
  A=[x for x,c in enumerate(pattern) if c&1]
  B=[x for x,c in enumerate(pattern) if c&2]
  if len(A)>4 or len(B)>4:continue
  first=list(base)+[(8,x) for x in A]+[(9,x) for x in B]
  for shared in range(min(4-len(A),4-len(B))+1):
    stats['generated']+=1
    if len(A)+len(B)+shared>5:
      stats['too_few_vertices']+=1;continue
    edges=first.copy();v=10
    for j in range(shared):edges.extend(((8,v),(9,v)));v+=1
    for j in range(4-len(A)-shared):edges.append((8,v));v+=1
    for j in range(4-len(B)-shared):edges.append((9,v));v+=1
    assert len(edges)==13 and len(set(tuple(sorted(e)) for e in edges))==13
    stats['vertex_budget_feasible']+=1
    if not first_condition(edges):
      stats['fails_A']+=1;continue
    stats['passes_A']+=1
    Acheck,Aavoid=arrow(edges,(1,1),(4,3,1,1))
    assert Acheck
    Bcheck,Bavoid=arrow(edges,(3,1,1),(3,1,1))
    if Bcheck:raise AssertionError(('JOINT_COUNTEREXAMPLE',edges))
    stats['fails_B']+=1
    border.append({'edges':edges,'B_bad_coloring':Bavoid})
expected={'generated':31667,'too_few_vertices':22442,'vertex_budget_feasible':9225,'fails_A':9224,'passes_A':1,'fails_B':1}
assert stats==expected,(stats,expected)
assert len(border)==1
print('RIGID13_SECOND_INDEPENDENT_EXACT_PASS',dict(stats),'A_positive_B_negative_edges',border[0]['edges'])
Path(__file__).with_name('RIGID_13EDGE_CERTIFICATE.json').write_text(json.dumps({'record_type':'ERDOS561_3X4_RIGID_13EDGE_CERTIFICATE/1','n':[3,1,1],'m':[4,3,1,1],'conjectured_joint_min_edges':14,'residual_individual_weight_sums':[13,13],'candidate_generation_complete_under_two_hub_equality':True,'counts':dict(stats),'remaining_A_positive_B_negative':border,'joint_counterexamples':0},indent=2)+'\n')
