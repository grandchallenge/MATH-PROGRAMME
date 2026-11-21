#!/usr/bin/env python3
"""Exact upper-host finite checks for two original size-Ramsey #561 cases.
The arbitrary-host lower theorem is analytical, not proved by this test.
"""
from itertools import product

RED = (3,2,2)
BLUES = ((3,1,1,1),(3,2,1,1))
HOST = (5,4,4,3,2,2)

def diagonal(a,b):
    return tuple(max(a[i]+b[j]-1 for i in range(len(a)) for j in range(len(b)) if i+j==k) for k in range(len(a)+len(b)-1))

def diagonal_independent(a,b):
    return tuple(max(a[i-1]+b[z-i-1]-1 for i in range(1,len(a)+1) if 1<=z-i<=len(b)) for z in range(2,len(a)+len(b)+1))

def contains(arms,target):
    arms=sorted((x for x in arms if x),reverse=True)
    target=sorted(target,reverse=True)
    return len(arms)>=len(target) and all(a>=b for a,b in zip(arms,target))

assert sum(HOST)==20 and len(HOST)==6
classes=0
for red_arms in product(*(range(x+1) for x in HOST)):
    blue_arms=tuple(h-r for h,r in zip(HOST,red_arms))
    for blue_target in BLUES:
        assert contains(red_arms,RED) or contains(blue_arms,blue_target), (red_arms,blue_arms,blue_target)
    classes+=1
assert classes==6*5*5*4*3*3==5400
for m in BLUES:
    assert diagonal(RED,m)==diagonal_independent(RED,m)==HOST
    assert diagonal(RED,m)[1:]==(4,4,3,2,2)
print("ERDOS561_ORIGINAL_322_VS_3111_3211_BOTH_J20_PASS")
print("ERDOS561_ORIGINAL_322_BOTH_ALL_5400_HOST_COLOUR_CLASSES_PASS")
