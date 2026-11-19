#!/usr/bin/env python3
"""Exact finite-simple-graph arrow checker for small edge sets.
Enumerates ordinary (non-induced) vertex-disjoint star-forest embeddings;
performs exhaustive upward-closure subset DP over EVERY 2-edge-coloring.
Never treats a failed sampling experiment as a proof.
"""
from itertools import combinations
from functools import lru_cache


def forest_masks(edges,target):
 V=sorted({v for e in edges for v in e}); ix={v:i for i,v in enumerate(V)}
 adj={v:[] for v in V}
 for i,(u,v) in enumerate(edges):
  assert u!=v
  adj[u].append((v,i));adj[v].append((u,i))
 possible={}
 for d in set(target):
  a=[]
  for center in V:
   for subset in combinations(adj[center],d):
    mask=(1<<ix[center]);em=0
    for v,i in subset:mask|=1<<ix[v];em|=1<<i
    a.append((mask,em))
  possible[d]=a
 target=tuple(sorted(target,reverse=True))
 if any(not possible[x] for x in target):return []
 patterns=set()
 def rec(pos,vbits,ebits):
  if pos==len(target):
   patterns.add(ebits);return
  for v,e in possible[target[pos]]:
   if not(vbits&v):rec(pos+1,vbits|v,ebits|e)
 rec(0,0,0)
 return patterns


def upward_table(E,emb):
 size=1<<E;mask=bytearray(size)
 for k in emb:mask[k]=1
 for i in range(E):
  bit=1<<i
  for j in range(size):
   if j&bit:mask[j]|=mask[j^bit]
 return mask

def arrow(edges,red,blue):
 E=len(edges);assert E<=20
 red_masks=forest_masks(edges,red)
 if not red_masks:return False,(0,(1<<E)-1)
 blue_masks=forest_masks(edges,blue)
 if not blue_masks:return False,((1<<E)-1,0)
 R=upward_table(E,red_masks);B=upward_table(E,blue_masks)
 allmask=(1<<E)-1
 for r in range(1<<E):
  if not R[r] and not B[allmask^r]:return False,(r,allmask^r)
 return True,None


def joint(edges,n,m):
 a,wa=arrow(edges,n[1:],m)
 if not a:return False,'red_deleted',wa
 b,wb=arrow(edges,n,m[1:])
 if not b:return False,'blue_deleted',wb
 return True,None,None


def stars(host):
 edges=[];at=0
 for h in host:
  for j in range(h):edges.append((at,at+j+1))
  at+=h+1
 return edges

def identify(edges,source,destination):
 res=[]
 for u,v in edges:
  if u==source:u=destination
  if v==source:v=destination
  if u==v:return None
  e=tuple(sorted((u,v)))
  if e in res:return None
  res.append(e)
 return res

if __name__=='__main__':
 n=(3,1,1);m=(4,1,1,1)
 for h in ((4,4,3,1,1),(4,4,2,1,1),(4,3,3,1,1)):
  E=stars(h)
  print('STAR',h,len(E),joint(E,n,m)[0],flush=True)
