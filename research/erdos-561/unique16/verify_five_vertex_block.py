#!/usr/bin/env python3
"""Exhaustively classify each possible seven-edge five-vertex induced block.
All five vertices' *full* graph degree is 3, while one has exactly one
external edge. Therefore internal degree multiset (2,3,3,3,3).
Verify every such labelled internal graph is isomorphic to the canonical
K5 minus a two-edge path and a disjoint edge. Pure Python stdlib.
"""
from itertools import combinations,permutations

n=5
all_edges=list(combinations(range(n),2))
deleted={(0,1),(0,2),(3,4)}
canonical=frozenset(e for e in all_edges if e not in deleted)
assert len(canonical)==7

def isomorphic_to_canonical(edges):
    for p in permutations(range(n)):
        transformed=frozenset(tuple(sorted((p[u],p[v]))) for u,v in edges)
        if transformed==canonical:return True
    return False

found=0
for chosen in combinations(all_edges,7):
    deg=[0]*n
    for u,v in chosen:
        deg[u]+=1;deg[v]+=1
    if sorted(deg)!=[2,3,3,3,3]:continue
    found+=1
    if not isomorphic_to_canonical(chosen):
        raise AssertionError(('NONCANONICAL_5BLOCK',chosen))
assert found==30,found
print('UNIQUE_FIVE_VERTEX_BLOCK_PASS: 1024 labelled graphs checked, 30 with degree profile (2,3,3,3,3), all isomorphic')
