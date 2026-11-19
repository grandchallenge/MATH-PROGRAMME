#!/usr/bin/env python3
"""Independent exact integer audit of ordinary-Lovasz tight-component
boundary profiles for D=3, red cap=1, blue cap=2 and k<=10.
Test necessary numerical conditions, not a substitute for the paper proof.
"""
from functools import lru_cache
from collections import Counter
D=3
ALPHA=1
BETA=2
@lru_cache(None)
def possibilities(c):
    values=[]
    for internal in range(c*(c-1)//2+1):
        boundary=D*c-2*internal
        if boundary<0:continue
        for to_S in range(boundary+1):
            to_T=boundary-to_S
            if (ALPHA*c+to_T)%2==1:
                values.append((to_S+BETA*to_T,to_S,to_T,internal))
    return tuple(sorted(values))

def partitions(n,minimum=1):
    if n==0:
        yield ()
    for j in range(minimum,n+1):
        for tail in partitions(n-j,j):
            yield (j,)+tail

survivors=[]
examined=0
for k in range(1,11):
    for sizes in partitions(k):
        q=len(sizes)
        if not q or max(sizes)<=3:continue
        examined+=1
        w=sum(min(p[0] for p in possibilities(c)) for c in sizes)
        if w<=D*(q-1):
            survivors.append((sizes,w,q))
assert survivors==[((5,5),2,2)],survivors
assert min(possibilities(5))==(1,1,0,7)
assert min(possibilities(4))[0]==3
assert min(possibilities(1))[0]==3
print('EXACT_LOVASZ_CUT_PROFILE_PASS',{'tested_profiles':examined,'only_profile':survivors[0],
    'unique_large_core_size_pair':[5,5],'each_weighted_boundary':1})
