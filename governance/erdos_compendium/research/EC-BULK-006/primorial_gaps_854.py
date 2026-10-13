"""Finite primorial-totative gap fixture, not an asymptotic proof."""
from math import gcd, prod
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19]
for k in range(2, 9):
    n = prod(PRIMES[:k])
    sieve = bytearray([1]) * n
    for p in PRIMES[:k]:
        sieve[0::p] = bytes(len(sieve[0::p]))
    totatives = [i for i in range(1, n) if sieve[i]]
    gaps = [b - a for a, b in zip(totatives, totatives[1:])]
    observed = set(gaps)
    maximum = max(gaps)
    missing = [t for t in range(2, maximum + 1, 2) if t not in observed]
    assert len(totatives) == prod(p - 1 for p in PRIMES[:k])
    assert sum(gaps) == n - 2 and all(g % 2 == 0 for g in gaps)
    if n <= 30030:
        assert all(gcd(a, n) == 1 for a in totatives)
    print(k, n, len(totatives), maximum, len(observed), missing, gaps.count(maximum))
