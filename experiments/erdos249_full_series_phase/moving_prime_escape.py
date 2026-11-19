"""Erdos 249 WP08-B: exact moving-prime totient pulse and overlog phase.

This module verifies finite arithmetic implications of the manuscript
MOVING_PRIME_ESCAPE_008B.md. The uniform prime-number-theorem asymptotic
is established in that manuscript, not by finite test extrapolation.

Original binary totient series irrationality: OPEN / MATHCERT NOT_SUBMITTED.
"""
from math import isqrt

from experiments.erdos249_full_series_phase.overlog_phase_separation import (
    totients, overlog_depth, rolling_numerators, centered,
)


def primes_to(n: int) -> tuple[int, ...]:
    """Exact small prime list (no conjectural primality input)."""
    if n < 2:
        return ()
    sieve = bytearray(b"\x01") * (n + 1)
    sieve[0:2] = b"\x00\x00"
    for p in range(2, isqrt(n) + 1):
        if sieve[p]:
            for m in range(p*p, n+1, p):
                sieve[m] = 0
    return tuple(p for p in range(2, n+1) if sieve[p])


def finite_prime_euler_sieve(limit: int, y: int) -> list[int]:
    """Compute exact g_y, without enumerating enormous rational divisors."""
    if limit < 1 or y < 2:
        raise ValueError("limit>=1 and y>=2 required")
    a = list(range(limit + 1))
    for p in primes_to(min(y, limit)):
        for n in range(p, limit + 1, p):
            a[n] -= a[n] // p
    return a


def unique_large_prime_sieve(limit: int, y: int) -> list[int]:
    """Exact unique p>y divisor on n<=limit, requiring y*y>limit.

    Every n in this range has at most one distinct or repeated p>y.
    """
    if limit < 1 or y < 2 or y*y <= limit:
        raise ValueError("requires 1<=limit<y*y and y>=2")
    factor = [0] * (limit + 1)
    for p in primes_to(limit):
        if p > y:
            for n in range(p, limit + 1, p):
                if factor[n]:
                    raise AssertionError("two large prime factors in regime")
                factor[n] = p
    return factor


def moving_prime_receipt(X: int, y: int) -> dict[str, object]:
    """Exact finite pulse, gap, and hostile consistency certificate.

    Theorem range: X>=64, integer y>=2, y*y>3X.
    No test or receipt asserts the prime number theorem from sampling.
    """
    if X < 64 or y < 2 or y*y <= 3*X:
        raise ValueError("X>=64, y>=2 and y*y>3X are mandatory")
    L = overlog_depth(X)
    Q = 1 << L
    limit = 2*X + L + 1
    if limit >= 3*X:
        raise AssertionError("internal endpoint inequality violated")
    phi = totients(limit)
    gy = finite_prime_euler_sieve(limit, y)
    large = unique_large_prime_sieve(limit, y)

    for n in range(1, limit+1):
        p = large[n]
        difference = gy[n] - phi[n]
        if p:
            m = n // p
            if m >= y or n % p:
                raise AssertionError("large-prime quotient not small")
            if difference != phi[m]:
                raise AssertionError("exact sparse prime-pulse identity failed")
        elif difference:
            raise AssertionError("unexpected missing-prime residue")
        if difference < 0 or gy[n] > n:
            raise AssertionError("finite Euler approximation contract failed")

    delta = [phi[n] - gy[n] for n in range(limit+1)]
    numerators = rolling_numerators(X, delta)
    residues = [centered(v, Q) for v in numerators]

    selected = []
    all_endpoints = []
    missing_primes = tuple(p for p in primes_to(2*y) if p > y)
    previous_endpoints = set()
    for p in missing_primes:
        low = X + L + 1
        high = 2*X + L - 1
        for n in range(((low+p-1)//p)*p, high+1, p):
            if n in previous_endpoints:
                raise AssertionError("omitted-prime endpoint counted twice")
            previous_endpoints.add(n)
            all_endpoints.append(n)
            m = n // p
            if not (large[n] == p and gy[n] - phi[n] == phi[m]):
                raise AssertionError("omitted-prime residual decomposition")
            if 2*phi[m] >= m:
                selected.append((n, p, m))
                N = n - L - 1
                if not (
                    12*y*abs(residues[N-X]) >= X
                    or 12*y*abs(residues[N-X+1]) >= X
                ):
                    raise AssertionError("good pulse lacks strong adjacent gap")
    strong = tuple(
        N for N in range(X, 2*X)
        if 12*y*abs(residues[N-X]) >= X
    )
    weak = tuple(
        N for N in range(X, 2*X)
        if 192*y*abs(residues[N-X]) >= Q
    )
    if not set(strong).issubset(set(weak)):
        raise AssertionError("strong gap did not imply theorem phase gap")
    if 2*len(strong) < len(selected):
        raise AssertionError("effective all-prime counting theorem failed")

    return {
        "X": X, "y": y, "L": L, "modulus": Q,
        "all_missing_primes_in_y_2y": missing_primes,
        "all_prime_endpoints": tuple(sorted(all_endpoints)),
        "good_prime_endpoints": tuple(selected),
        "strong_gap_starts": strong,
        "theorem_gap_starts": weak,
        "theorem_gap_threshold": f"1/{192*y}",
        "proven_finite_lower_count_twice": len(selected),
        "noncertifying_source": "WP08_B_EXACT_INTEGER_ARITHMETIC",
        "full_series_irrationality": "OPEN",
    }


def rational_finite_patch(X: int, y: int) -> tuple[list[int], list[int]]:
    """Finite-block hostile: patch rational g_y to equal phi in the window.

    The infinite patch series is rational since it differs from the
    known rational complete g_y series in finitely many coefficients.
    This routine does not attempt huge exact rational S_y evaluation.
    """
    if X < 64 or y < 2 or y*y <= 3*X:
        raise ValueError("invalid finite patch theorem regime")
    L = overlog_depth(X)
    limit = 3*X - 1
    phi = totients(limit)
    gy = finite_prime_euler_sieve(limit, y)
    patch = list(gy)
    for n in range(X+1, 2*X+L+1):
        patch[n] = phi[n]
    return patch, phi
