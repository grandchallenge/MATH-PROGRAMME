#!/usr/bin/env python3
"""Exact star-host upper corroboration of the 322/3111 paper theorem.
Does NOT verify the unbounded Lovasz-factor dependency or arbitrary hosts.
"""
from itertools import product

N = (3, 2, 2)
M = (3, 1, 1, 1)
HOST = (4, 4, 3, 2, 2)

def diagonal(a, b):
    return tuple(
        max(a[i] + b[j] - 1 for i in range(len(a)) for j in range(len(b)) if i + j == k)
        for k in range(len(a) + len(b) - 1)
    )

def diagonal_independent(a, b):
    return tuple(
        max(a[i-1] + b[z-i-1] - 1 for i in range(1, len(a)+1) if 1 <= z-i <= len(b))
        for z in range(2, len(a)+len(b)+1)
    )

def contains(arms, target):
    arms = sorted((x for x in arms if x), reverse=True)
    target = sorted(target, reverse=True)
    return len(arms) >= len(target) and all(a >= b for a,b in zip(arms,target))

assert diagonal(N,M) == diagonal_independent(N,M) == (5,4,4,3,2,2)
assert diagonal(N[1:],M) == diagonal_independent(N[1:],M) == (4,4,2,2,2)
assert diagonal(N,M[1:]) == diagonal_independent(N,M[1:]) == (3,3,3,2,2)
assert HOST == diagonal(N,M)[1:] and sum(HOST) == 15
assert sum(diagonal(N[1:],M)) == 14 and sum(diagonal(N,M[1:])) == 13

count=0
for red in product(*(range(h+1) for h in HOST)):
    blue = tuple(h-r for h,r in zip(HOST,red))
    assert contains(red,N[1:]) or contains(blue,M), ("A",red,blue)
    assert contains(red,N) or contains(blue,M[1:]), ("B",red,blue)
    count += 1
assert count == 900
for k in range(8,15):
    for v in range(12,29):
        if v+2*k <= 28:
            assert k==8 and v==12
print("ERDOS561_322_3111_ANTIDIAGONAL_PASS")
print("ERDOS561_322_3111_ALL_900_HOST_COLOUR_CLASSES_PASS")
print("ERDOS561_322_3111_HANDSHAKE_ARITHMETIC_PASS")
