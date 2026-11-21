#!/usr/bin/env python3
"""Deterministic exact parameter and nonuniform star-host audit."""
from itertools import combinations_with_replacement, product
from collections import Counter

def diag0(n,m):
    return tuple(max(n[i]+m[j]-1 for i in range(len(n)) for j in range(len(m)) if i+j==z)
                 for z in range(len(n)+len(m)-1))
def diag1(n,m):
    return tuple(max(n[i-1]+m[z-i-1]-1 for i in range(1,len(n)+1) if 1<=z-i<=len(m))
                 for z in range(2,len(n)+len(m)+1))
def contains(arms,target):
    arm=sorted((x for x in arms if x>0),reverse=True)
    tar=sorted(target,reverse=True)
    return len(arm)>=len(tar) and all(x>=y for x,y in zip(arm,tar))
counts=Counter()
for k in range(3,8):
  for a in range(2,7):
    for q in combinations_with_replacement(range(1,a+3),k):
      c=q[::-1]
      for exact in (True,False):
        if (c[k-3]>=a-1)!=exact: continue
        lo=a+c[0]-1 if exact else c[0]
        for b in range(lo,lo+4 if exact else lo+3):
          n=(a,1,1);m=(b,)+c
          A=diag0(n[1:],m);B=diag0(n,m[1:]);W=diag0(n,m)
          assert A==diag1(n[1:],m) and B==diag1(n,m[1:]) and W==diag1(n,m)
          d=[max(0,x-a+1) for x in c]
          lower=2*b+sum(c)+sum(max(0,c[i+2]-d[i]) for i in range(k-2))
          U=tuple(max(x,y) for x,y in zip(A,B))
          assert lower<=sum(U)
          if exact:
            expected=(b,b)+tuple(max(c[i],a+c[i+2]-1) for i in range(k-2))+(c[-2],c[-1])
            assert U==expected and lower==sum(U)
            assert sum(W)==sum(U)+a+b-1
            counts['exact']+=1
          else:counts['lower_only']+=1
samples=[
 (3,(3,2,1),5),(3,(3,2,1,1),5),
 (4,(5,4,3,2,1),8),(3,(4,3,2,1,1),6),
 (2,(3,2,2,1,1),4),(4,(5,3,3,1),8)
]
for a,c,b in samples:
  n=(a,1,1);m=(b,)+c;k=len(c)
  U=(b,b)+tuple(max(c[i],a+c[i+2]-1) for i in range(k-2))+(c[-2],c[-1])
  for red in product(*(range(x+1) for x in U)):
    blue=tuple(x-y for x,y in zip(U,red))
    assert contains(red,n[1:]) or contains(blue,m),('R1',n,m,red)
    assert contains(red,n) or contains(blue,m[1:]),('R2',n,m,red)
    counts['complete_allocations']+=1
  counts['hosts']+=1
assert counts==Counter({'exact':24500,'lower_only':19305,'complete_allocations':147188,'hosts':6}),counts
print('ERDOS561_VARIABLE_TAIL_EXACT_GRID_24500_PASS')
print('ERDOS561_VARIABLE_TAIL_LOWER_ONLY_19305_PASS')
print('ERDOS561_VARIABLE_TAIL_SIX_HOSTS_147188_ARM_COLOURS_PASS')
