#!/usr/bin/env python3
"""Independent two-colouring correctness crosscheck for 160 nonstar hosts.
Compares structural red-2K2-star/triangle method with full 2^13
subset enumeration and exact vertex-disjoint star forest embeddings.
"""
from random import Random
from star_host_falsifier import partitions
from exact_arbitrary_host import stars,identify,arrow
from fast_A import arrow_A
rng=Random(561)
cases=[]
for H in (x for x in partitions(13) if len(x)>=5 and max(x)>=4):
 edges=stars(H);verts=sorted({v for e in edges for v in e})
 for _ in range(10):
  u,v=rng.sample(verts,2);G=identify(edges,u,v)
  if G is not None:cases.append((H,G))
rng.shuffle(cases)
assert len(cases)>=160
for H,G in cases[:160]:
 structural=arrow_A(G,4,4)[0]
 exhaustive=arrow(G,(1,1),(4,1,1,1,1))[0]
 assert structural==exhaustive,(H,structural,exhaustive)
print('INDEPENDENT_STRUCTURAL_VS_EXHAUSTIVE_COLORING_PASS',len(cases[:160]))
