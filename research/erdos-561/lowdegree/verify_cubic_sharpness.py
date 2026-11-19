#!/usr/bin/env python3
"""Exact sharpness witness for (1,2) subcubic cap partition bound.
A single degree-2 separator touches two odd five-vertex cubic cores,
so no matching can saturate all ten degree-3 vertices.
"""
from itertools import combinations
from collections import Counter

# Each five-vertex block is K5 minus edges (0,1),(0,2),(3,4),
# and has degrees (2,3,3,3,3). Link both block 0s to central 10.
removed={(0,1),(0,2),(3,4)}
edges=[]
for start in (0,5):
 for i,j in combinations(range(5),2):
  if (i,j) not in removed:
   edges.append((start+i,start+j))
edges.extend([(0,10),(5,10)])
assert len(edges)==16
D=Counter(v for e in edges for v in e)
assert len(D)==11
assert sorted(D.values())==[2]+[3]*10
saturated={v for v,d in D.items() if d==3}
assert len(saturated)==10

matching_cover_exists=False
for mask in range(1<<len(edges)):
 used=set();ok=True
 for i,(u,v) in enumerate(edges):
  if (mask>>i)&1:
   if u in used or v in used:
    ok=False;break
   used.add(u);used.add(v)
 if ok and saturated<=used:
  matching_cover_exists=True;break
assert not matching_cover_exists

# Factor obstruction witness: S={10}, T=empty. G-S has two
# five-vertex tight components, both with odd alpha*|C|=5.
assert D[10]==2
assert sum(1 for start in (0,5) if all(D[start+i]==3 for i in range(5)))==2
A=min(D[10],1)
q=2
assert A==1 and q==2 and A<q
print('SHARP_SUBCUBIC_PASS: edges=16 max_degree=3 saturated=10 matching_cover=False Lovasz_A=1 q=2')
