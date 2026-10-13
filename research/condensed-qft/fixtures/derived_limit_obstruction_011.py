#!/usr/bin/env python3
"""QFT-COND-005/DLI-011 finite rational Roos regression; not an infinite proof."""
from fractions import Fraction as Q

def shift(v):
    return (Q(0),) + v[:-1]

def add(a,b):
    return tuple(x+y for x,y in zip(a,b))

def sub(a,b):
    return tuple(x-y for x,y in zip(a,b))

def solve(xs, n, N):
    acc = tuple(Q(0) for _ in range(N))
    v = xs[n]
    for j in range(N):
        term = xs[n+j]
        for _ in range(j):
            term = shift(term)
        acc = add(acc, term)
    return acc

for N in range(1,25):
    xs = [tuple(Q((n+1)*(k+2)-3*k, 7) for k in range(N)) for n in range(3*N+3)]
    for n in range(N+1):
        y = solve(xs, n, N)
        ynext = solve(xs, n+1, N)
        assert sub(y, shift(ynext)) == xs[n], (N,n)
    zero = tuple(Q(0) for _ in range(N))
    v = xs[0]
    for _ in range(N):
        v = shift(v)
    assert v == zero
print("DLI-011 finite Roos truncation regression: PASS (N=1..24)")
