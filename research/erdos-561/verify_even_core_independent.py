#!/usr/bin/env python3
"""Separate exhaustive feasibility checker: does NOT construct Hamilton cycles."""
from itertools import combinations
import json

def possible(D, a, missing):
    n=D+1;missing=set(missing)
    edges=[e for e in combinations(range(n),2) if e not in missing]
    stubs=[0]*n
    for u,v in missing:stubs[u]+=1;stubs[v]+=1
    targets_low=[max(0,a-s) for s in stubs]
    targets_high=[min(a,D-s) for s in stubs]
    deg=[0]*n
    # Independent exhaustive core-edge partition, deciding pendant colours from feasibility intervals.
    rem=[0]*n
    for u,v in edges:rem[u]+=1;rem[v]+=1
    def dfs(i):
        if i==len(edges):return all(targets_low[v]<=deg[v]<=targets_high[v] for v in range(n))
        u,v=edges[i];rem[u]-=1;rem[v]-=1
        for color in (0,1):
            deg[u]+=color;deg[v]+=color
            if all(deg[z]<=targets_high[z] and deg[z]+rem[z]>=targets_low[z] for z in (u,v)):
                if dfs(i+1):return True
            deg[u]-=color;deg[v]-=color
        rem[u]+=1;rem[v]+=1
        return False
    return dfs(0)

def run():
    totals={'checked':0,'positive':0,'negative':0}
    for D in (2,4):
        E=list(combinations(range(D+1),2))
        for mask in range(1<<len(E)):
            missing=[E[i] for i in range(len(E)) if mask>>i&1]
            for a in range(1,D):
                got=possible(D,a,missing)
                exp=not (D%2==0 and a%2==1 and not missing)
                assert got==exp,(D,a,missing,got,exp)
                totals['checked']+=1
                totals['positive' if got else 'negative']+=1
    for D in (3,5):
        E=list(combinations(range(D+1),2))
        # Keep D5 test bounded: all subsets with up to 2 missing edges.
        cases=[tuple()] + [c for k in (1,2) for c in combinations(E,k)]
        for missing in cases:
            for a in range(1,D):
                got=possible(D,a,missing)
                assert got,(D,a,missing)
                totals['checked']+=1;totals['positive']+=1
    return totals

if __name__=='__main__':print(json.dumps(run(),indent=2))
