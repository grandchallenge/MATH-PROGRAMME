#!/usr/bin/env python3
"""Exact conormal bookkeeping for R1; not a proof of normal-topology continuity."""
from itertools import combinations

def partitions(seq):
    if not seq:
        yield []
        return
    first, rest = seq[0], seq[1:]
    for p in partitions(rest):
        yield [(first,)] + p
        for i in range(len(p)):
            q = p.copy()
            q[i] = (first,) + q[i]
            yield q

seen = 0
for n in range(4, 9):
    remaining = tuple(range(2,n))
    for p in partitions(remaining):
        nontrivial = [b for b in p if len(b)>=2]
        if not nontrivial:
            continue
        for b in nontrivial:
            eta = [0]*n
            eta[b[0]]=3
            eta[b[1]]=-3
            # Every residual block has zero cotangent sum; pair conormal +/-7.
            for alpha in [-7,0,7]:
                xi=eta.copy()
                xi[0],xi[1]=alpha,-alpha
                assert sum(xi[:2])==0
                assert all(sum(xi[k] for k in block)==0 for block in p)
                assert any(v for v in xi)
                seen+=1
assert seen>=100
print(f"PASS: {seen} exact simultaneous-partition conormal witness checks")
print("NOTE: topological continuity derives from published normal-topology theorems.")
