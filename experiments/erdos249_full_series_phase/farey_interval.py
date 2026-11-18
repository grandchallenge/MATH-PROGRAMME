"""Exact minimum rational denominator in the positive full-totient-series tail interval.

Every rational p/q inside the *open* enclosure (A/2^N,(A+N+2)/2^N)
has q >= min_q, exactly. No asymptotic irrationality claim.
"""
from __future__ import annotations
import sys
sys.set_int_max_str_digits(100000)

import hashlib
import json
from fractions import Fraction


def phi_sieve(N: int) -> list[int]:
    a = list(range(N + 1))
    for p in range(2, N + 1):
        if a[p] == p:
            for k in range(p, N + 1, p):
                a[k] -= a[k] // p
    return a


def prefix_integer(phi: list[int], N: int) -> int:
    z = 0
    for n in range(1, N + 1):
        z = 2*z + phi[n]
    return z


def interval_neighbors(A: int, Q: int, D: int) -> tuple[tuple[int, int], tuple[int, int], tuple[int, int], int]:
    """Return adjacent Farey sides and first mediant strictly in (A/Q,(A+D)/Q).

    Invariants: a/b <= A/Q < (A+D)/Q <= c/d, bc-ad=1.
    Work with 1/0 as +infinity. Zero integer cases supported.
    """
    assert A >= 0 and Q >= 1 and 0 < D < Q
    xnum, ynum = A, A + D
    a, b, c, d = 0, 1, 1, 0
    steps = 0
    while True:
        steps += 1
        p, q = a + c, b + d
        if p * Q <= xnum * q:
            numer = xnum * b - a * Q
            denom = c * Q - xnum * d
            assert denom > 0 and numer >= denom
            k = numer // denom
            a += k*c
            b += k*d
        elif p * Q >= ynum * q:
            numer = c * Q - ynum * d
            denom = ynum * b - a * Q
            assert denom > 0 and numer >= denom
            k = numer // denom
            c += k*a
            d += k*b
        else:
            assert p*Q > xnum*q and p*Q < ynum*q
            assert b*c-a*d == 1
            assert a*Q <= xnum*b
            assert c*Q >= ynum*d
            assert q == b+d
            return (a,b),(c,d),(p,q),steps


def compute(N: int) -> dict:
    if N < 8:
        raise ValueError("N>=8 needed")
    phi=phi_sieve(N)
    A=prefix_integer(phi,N)
    Q=1<<N
    D=N+2
    assert 0 < D < Q
    lo,hi,mid,steps=interval_neighbors(A,Q,D)
    a,b=lo
    c,d=hi
    p,q=mid
    # Three independent exact integer inequalities; these suffice to verify certificate
    assert (a*Q <= A*b and c*Q >= (A+D)*d and b*c-a*d==1)
    assert A*q < p*Q < (A+D)*q
    assert q==b+d
    return {
       "N":N, "tail_bound":D, "denominator_power":N,
       "numerator_prefix":str(A),
       "farey_left":[str(a),str(b)],"farey_right":[str(c),str(d)],
       "first_interior_fraction":[str(p),str(q)],"minimal_denominator":str(q),
       "minimal_denominator_digits":len(str(q)),
       "stern_brocot_steps":steps,
       "prefix_sha256":hashlib.sha256(str(A).encode()).hexdigest(),
       "status":"FINITE_EXCLUSION_ONLY_S_IRRATIONALITY_OPEN"}


def validate_receipt(rec: dict) -> None:
    N=int(rec["N"])
    A=int(rec["numerator_prefix"])
    Q=1<<N
    D=int(rec["tail_bound"])
    a,b=map(int,rec["farey_left"])
    c,d=map(int,rec["farey_right"])
    p,q=map(int,rec["first_interior_fraction"])
    assert D==N+2
    assert b>=1 and d>=0 and q>=1
    assert b*c-a*d==1
    assert a*Q <= A*b
    assert (A+D)*d <= c*Q
    assert p==a+c and q==b+d
    assert A*q < p*Q < (A+D)*q
    assert str(q)==rec["minimal_denominator"]
    assert rec["minimal_denominator_digits"]==len(str(q))
    assert hashlib.sha256(str(A).encode()).hexdigest()==rec["prefix_sha256"]
