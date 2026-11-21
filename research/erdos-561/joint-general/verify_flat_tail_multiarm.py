#!/usr/bin/env python3
"""Deterministic exact arithmetic and finite star-host colouring checks.

The general arbitrary-host lower bound is mathematical (see
FLAT_TAIL_MULTIARM_RECOLOURING_THEOREM.md), not extrapolated from this test.
"""
from collections import Counter
from itertools import product

def diag0(n,m):
    return tuple(max(n[i]+m[j]-1 for i in range(len(n)) for j in range(len(m))
                     if i+j==k) for k in range(len(n)+len(m)-1))

def diag1(n,m):
    return tuple(max(n[i-1]+m[k-i-1]-1 for i in range(1,len(n)+1)
                     if 1<=k-i<=len(m)) for k in range(2,len(n)+len(m)+1))

def embeds(arms,target):
    arms=sorted((v for v in arms if v>0),reverse=True)
    target=sorted(target,reverse=True)
    return len(arms)>=len(target) and all(x>=y for x,y in zip(arms,target))

counts=Counter()
for t in range(4,10):
    for a in range(2,9):
        for c in range(a-1,a+5):
            for b in range(a+c-1,a+c+10):
                n=(a,1,1);m=(b,)+(c,)*(t-1)
                a1=diag0(n[1:],m);b1=diag0(n,m[1:]);full=diag0(n,m)
                assert (a1,b1,full)==(diag1(n[1:],m),diag1(n,m[1:]),diag1(n,m))
                assert a1==(b,b)+(c,)*(t-1)
                assert b1==(a+c-1,)*(t-1)+(c,c)
                upper=(b,b)+(a+c-1,)*(t-3)+(c,c)
                J=sum(upper)
                assert tuple(max(x,y) for x,y in zip(a1,b1))==upper
                assert J==2*b+(t-3)*(a+c-1)+2*c
                assert J==2*b+(t-1)*c+(t-3)*(a-1)
                assert sum(full)==J+a+b-1
                qmax=(t-3)*(a-1)-1
                assert 2+qmax//(a-1)==t-2 < t-1
                counts['exact_family']+=1

for t in range(4,10):
    for a in range(4,11):
        for c in range(1,a-1):
            for b in range(c,c+9):
                n=(a,1,1);m=(b,)+(c,)*(t-1)
                A=diag0(n[1:],m);B=diag0(n,m[1:])
                assert A==diag1(n[1:],m) and B==diag1(n,m[1:])
                r=min(a-1,c)
                lower=2*b+(t-1)*c+(t-3)*r
                assert lower<=sum(max(x,y) for x,y in zip(A,B))
                assert (2+(r*(t-3)-1)//r)==t-2
                counts['lower_only']+=1

sample=[
    (2,4,1,2),
    (2,5,2,3),
    (3,4,2,4),
    (3,5,2,4),
    (4,4,3,6),
    (4,5,3,6),
    (3,6,3,5),
]
for a,t,c,b in sample:
    n=(a,1,1);m=(b,)+(c,)*(t-1)
    h=(b,b)+(a+c-1,)*(t-3)+(c,c)
    assert len(h)==t+1
    for red in product(*(range(arm+1) for arm in h)):
        blue=tuple(arm-x for arm,x in zip(h,red))
        assert embeds(red,n[1:]) or embeds(blue,m),('R1',a,t,c,b,red)
        assert embeds(red,n) or embeds(blue,m[1:]),('R2',a,t,c,b,red)
        counts['complete_upper_arm_colourings']+=1
    counts['complete_upper_hosts']+=1

assert counts==Counter({'exact_family':2772,'lower_only':1890,
                       'complete_upper_arm_colourings':177482,
                       'complete_upper_hosts':7}),counts
print('ERDOS561_MULTIARM_EXACT_PARAMETER_GRID_2772_PASS')
print('ERDOS561_MULTIARM_LOWER_ONLY_GRID_1890_PASS')
print('ERDOS561_MULTIARM_COMPLETE_STAR_HOSTS_7_PASS')
print('ERDOS561_MULTIARM_COMPLETE_ARM_COLOURINGS_177482_PASS')
