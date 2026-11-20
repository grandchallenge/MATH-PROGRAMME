#!/usr/bin/env python3
"""Exact finite audits of antidiagonal plateau transfers. Does not prove parent cases."""
import itertools, json
from pathlib import Path

def W(n,m):
    assert all(a >= b >= 1 for a,b in zip(n,n[1:]))
    assert all(a >= b >= 1 for a,b in zip(m,m[1:]))
    return tuple(max(n[i]+m[j]-1 for i in range(len(n)) for j in range(len(m)) if i+j==k)
                 for k in range(len(n)+len(m)-1))

def J(n,m):return sum(W(n,m)[1:])

def J_independent(n,m):
    z={k:[] for k in range(3,len(n)+len(m)+1)}
    for i,x in enumerate(n,1):
        for j,y in enumerate(m,1):
            if i+j>=3:z[i+j].append(x+y-1)
    return sum(max(z[k]) for k in sorted(z))

def lift(n0,m0,n,m,j):
    assert len(n0)==len(n) and len(m0)==len(m)
    assert all(x>=y for x,y in zip(n,n0)) and all(x>=y for x,y in zip(m,m0))
    assert J(n0,m0)==j==J(n,m)==J_independent(n,m)

n=(3,2,1)
case15=[(4,c,d,1) for c in range(1,4) for d in range(1,min(c,2)+1)]
assert case15==[(4,1,1,1),(4,2,1,1),(4,2,2,1),(4,3,1,1),(4,3,2,1)]
for m in case15:
    lift(n,(4,1,1,1),n,m,15)
    assert W(n,m)[1:]==(5,4,3,2,1)
for c in (1,2):
    lift(n,(3,1,1,1),n,(3,c,1,1),13)
    assert W(n,(3,c,1,1))[1:]==(4,3,3,2,1)
for a in range(4,25):
    n=(a,2,1)
    for c in (1,2):
        lift(n,(a,1,1,1),n,(a,c,1,1),3*a+4)
        assert W(n,(a,c,1,1))[1:]==(a+1,a,a,2,1)
for b in range(5,25):
    n=(3,1,1)
    for c in (2,3):
        lift(n,(b,2,2,1),n,(b,c,2,1),2*b+6)
        assert W(n,(b,c,2,1))[1:]==(b,b,3,2,1)
# Check exact plateau boundaries in finite parameter ranges.
for a in range(4,25):
    n=(a,2,1);base=J(n,(a,1,1,1))
    found=[(c,d,e) for c in range(1,a+1) for d in range(1,c+1)
           for e in range(1,d+1) if J(n,(a,c,d,e))==base]
    assert found==[(1,1,1),(2,1,1)]
for b in range(5,25):
    n=(3,1,1);base=J(n,(b,2,2,1))
    found=[(c,d,e) for c in range(2,b+1) for d in range(2,c+1)
           for e in range(1,d+1) if J(n,(b,c,d,e))==base]
    assert found==[(2,2,1),(3,2,1)]
print("PLATEAU_TRANSFER_VERIFIED",{"J15_cases":len(case15),
     "J13_cases":2,"a_samples":21,"b_samples":20,
     "new_infinite_families":2})
