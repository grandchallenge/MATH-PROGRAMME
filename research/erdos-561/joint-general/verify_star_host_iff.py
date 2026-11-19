#!/usr/bin/env python3
"""Independent brute verification of the paper star-host iff criterion.
Enumerates EVERY red-arm count on EVERY tested star component; no reuse
of star_host_falsifier.py / exact_arbitrary_host.py.
"""
from itertools import product,combinations_with_replacement
from functools import lru_cache

@lru_cache(None)
def parts(E,cap):
 if E==0:return ((),)
 out=[]
 for h in range(min(E,cap),0,-1):
  for tail in parts(E-h,h):out.append((h,)+tail)
 return tuple(out)

def target(counts,forest):
 counts=sorted(counts,reverse=True)
 return len(counts)>=len(forest) and all(counts[i]>=v for i,v in enumerate(forest))

def brute_arrow(H,n,m):
 for reds in product(*(range(h+1) for h in H)):
  blues=[h-r for h,r in zip(H,reds)]
  if not target(reds,n) and not target(blues,m):return False
 return True

def diagonal(n,m):
 return tuple(max(n[i]+m[j]-1 for i in range(len(n)) for j in range(len(m)) if i+j==z)
              for z in range(len(n)+len(m)-1))

def predicted(H,n,m):
 W=diagonal(n,m);L=len(W)
 return len(H)>=L and all(H[i]>=W[i] for i in range(L))

def seq(p):return [t[::-1] for t in combinations_with_replacement(range(1,3),p)]

single=0;joint=0
for s,t in ((2,2),(2,3),(3,3),(3,4),(4,4)):
 for n in seq(s):
  for m in seq(t):
   for E in range(10):
    for H in parts(E,E):
     predictedA=predicted(H,n,m)
     actualA=brute_arrow(H,n,m)
     assert actualA==predictedA,('SINGLE',H,n,m,actualA,predictedA)
     single+=1
     if s>=3 and t>=3:
      J=sum(diagonal(n,m)[1:]);
      expected=len(H)>=s+t-2 and all(H[i]>=diagonal(n,m)[i+1] for i in range(s+t-2))
      actual=brute_arrow(H,n[1:],m) and brute_arrow(H,n,m[1:])
      assert actual==expected,('JOINT',H,n,m,actual,expected,J)
      joint+=1
print('STAR_HOST_IF_AND_ONLY_IF_BRUTE_PASS',{'single_pair_host_tests':single,'joint_residual_host_tests':joint,'all_edge_colours_enumerated':True,'max_host_edges':9})
