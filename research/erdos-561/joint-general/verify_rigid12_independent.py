#!/usr/bin/env python3
"""Independently enumerate every E=12 two-cubic-hub extension of F321.
Second graph/forest oracle builds distinct star embeddings from adjacency
combinations and an independent subset-monotonicity DP. Does not import
search_rigid_12edge or exact_arbitrary_host.
"""
from itertools import combinations
from collections import Counter
import json
from pathlib import Path

root=Path(__file__).resolve().parent
base={(0,1),(0,2),(0,3),(4,5),(4,6),(7,8)}
old={1,2,3,4,5,6,7,8}

def build(A,B,shared):
    edges=set(base)
    for z in A:edges.add((9,z))
    for z in B:edges.add((10,z))
    nextv=11
    for _ in range(shared):edges.update(((9,nextv),(10,nextv)));nextv+=1
    for _ in range(3-len(A)-shared):edges.add((9,nextv));nextv+=1
    for _ in range(3-len(B)-shared):edges.add((10,nextv));nextv+=1
    assert len(edges)==12
    return tuple(sorted(edges))

def is_exact_F321(after):
    if len(after)!=6:return False
    vertices={v for e in after for v in e}
    adj={v:set() for v in vertices}
    for a,b in after:adj[a].add(b);adj[b].add(a)
    counts=[]
    while vertices:
        v=next(iter(vertices));component={v};active=[v]
        for a in active:
            for b in adj[a]:
                if b not in component:component.add(b);active.append(b)
        vertices-=component
        e=sum(len(adj[x]) for x in component)//2
        if e<1 or len(component)!=e+1 or max(len(adj[x]) for x in component)!=e:return False
        counts.append(e)
    return sorted(counts)==[1,2,3]

def embeddings(edges,profile):
    allV={v for edge in edges for v in edge}
    adj={v:[] for v in allV}
    for k,(u,v) in enumerate(edges):adj[u].append((v,k));adj[v].append((u,k))
    options={}
    for star in set(profile):
        options[star]=[]
        for hub in adj:
            for leaves in combinations(adj[hub],star):
                used=frozenset([hub]+[u for u,_ in leaves]);mask=0
                for _,idx in leaves:mask|=1<<idx
                options[star].append((used,mask))
    results=set()
    def rec(j,occupied,mask):
        if j==len(profile):results.add(mask);return
        for v,edgesMask in options[profile[j]]:
            if occupied.isdisjoint(v):rec(j+1,occupied|v,mask|edgesMask)
    rec(0,frozenset(),0)
    return results

def arrow(edges,red,blue):
    E=len(edges);size=1<<E;full=size-1
    R=bytearray(size);B=bytearray(size)
    for mask in embeddings(edges,red):R[mask]=1
    for mask in embeddings(edges,blue):B[mask]=1
    for bit in (1<<j for j in range(E)):
        for mask in range(size):
            if mask&bit:
                R[mask]|=R[mask^bit]
                B[mask]|=B[mask^bit]
    for m in range(size):
        if not R[m] and not B[full^m]:return False,{'red_mask':m,'blue_mask':full^m}
    return True,None

counts=Counter();border=[]
subsets=[frozenset(x) for k in range(4) for x in combinations(sorted(old),k)]
for A in subsets:
  for B in subsets:
    if 4 in A and 4 in B:continue
    for shared in range(min(3-len(A),3-len(B))+1):
      edges=build(A,B,shared)
      counts['generated']+=1
      # A/B both forbid a 3-edge-blue-matching under full-incident
      # colouring from {v9,center0} or {u10,center0}, so remainder
      # must equal the entire edge forest 321.
      residual9=[edge for edge in edges if not({9,0}&set(edge))]
      if not is_exact_F321(residual9):
        counts['fails_residual9']+=1;continue
      residual10=[edge for edge in edges if not({10,0}&set(edge))]
      if not is_exact_F321(residual10):
        counts['fails_residual10']+=1;continue
      counts['passes_rigid_gate']+=1
      # A: red 2,1 vs blue 3,1,1,1
      # B: red 3,2,1 vs blue 1,1,1
      b,_=arrow(edges,(3,2,1),(1,1,1))
      if not b:
        counts['fails_B']+=1;continue
      counts['arrows_B']+=1
      a,bad=arrow(edges,(2,1),(3,1,1,1))
      if a:
        raise AssertionError(('JOINT_COUNTEREXAMPLE',edges))
      border.append({'edges':edges,'A_failure_colouring':bad})
      counts['fails_A']+=1
assert counts=={'generated':9194,'fails_residual9':8154,
 'fails_residual10':910,'passes_rigid_gate':130,
 'fails_B':129,'arrows_B':1,'fails_A':1},counts
orig=json.loads((root/'RIGID_12EDGE_CERTIFICATE.json').read_text())
assert len(border)==1
assert {tuple(e) for e in border[0]['edges']}=={tuple(e) for e in orig['remaining_borderline_graphs'][0]['edges']}
assert orig['remaining_joint_counterexamples']==0
print('RIGID12_DOUBLE_INDEPENDENT_ENUMERATION_PASS',dict(counts),
 'B_positive_A_negative_graph_edges',border[0]['edges'])
