#!/usr/bin/env python3
"""Necessary ordinary-Lovasz factor-cut profiles for D=3, e<=18.
Under an already-proved k>=10 saturated-core theorem, every failed
(1,2) degree-cap partition has at least two counted 'large' components
(size>=4). Enumerate all integer partitions of at most 12 saturated
vertices; every counted component must be tight degree 3 and parity odd.
A necessary bound is weighted_boundary<=3(q-1), AND unweighted boundary
<= total degree outside the counted components = 2e-3*sum sizes.
The latter is essential for excluding the apparent 5+7 and 5+5+1
possibilities. Numerics are exact, independent of earlier verifiers.
"""
from functools import lru_cache

@lru_cache(None)
def parity_boundaries(c):
    out=[]
    for edges_internal in range(c*(c-1)//2+1):
        boundary=3*c-2*edges_internal
        if boundary<0:continue
        for s in range(boundary+1):
            t=boundary-s
            if (c+t)%2==1:
                out.append((s+2*t,s+t,s,t,edges_internal))
    return tuple(out)

def partitions(N,minimum=1):
    if N==0:
        yield ()
        return
    for head in range(minimum,N+1):
        for rest in partitions(N-head,head):
            yield (head,)+rest

for edgecount in (16,17,18):
    candidates=[];examined=0
    for counted_size in range(8,13):
        for sizes in partitions(counted_size):
            if sum(c>=4 for c in sizes)<2:continue
            examined+=1
            q=len(sizes)
            weighted_min=sum(min(x[0] for x in parity_boundaries(c)) for c in sizes)
            unweighted_min=sum(min(x[1] for x in parity_boundaries(c)) for c in sizes)
            outdegree=2*edgecount-3*counted_size
            if weighted_min<=3*(q-1) and unweighted_min<=outdegree:
                candidates.append((sizes,weighted_min,unweighted_min))
    assert examined==34,examined
    assert candidates==[((5,5),2,2)],(edgecount,candidates)
    print('FACTOR_COMPONENT_BUDGET_PASS',{'edges':edgecount,'partitions_tested':examined,
                                      'only_feasible_counted_sizes':(5,5),'weighted_min':2,'boundary_min':2})
print('SUBCUBIC_16_18_CUT_PROFILES_PASS')
