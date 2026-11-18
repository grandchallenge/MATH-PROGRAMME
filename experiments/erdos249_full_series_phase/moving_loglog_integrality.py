"""ERDOS-249 WP07-A: finite exact checks behind moving-depth arithmetic collapse.

The asymptotic Selberg–Delange input is a classical external theorem.
This module tests only finite arithmetic premises and inequalities. It
neither numerically proves the asymptotic nor solves the original problem.
"""
from fractions import Fraction
from math import gcd


def totient_sieve(limit: int) -> list[int]:
    if limit < 1:
        raise ValueError("limit must be positive")
    vals = list(range(limit + 1))
    for p in range(2, limit + 1):
        if vals[p] == p:
            for n in range(p, limit + 1, p):
                vals[n] -= vals[n] // p
    return vals


def distinct_prime_factor_sieve(limit: int) -> list[int]:
    if limit < 1:
        raise ValueError("limit must be positive")
    vals = [0] * (limit + 1)
    for p in range(2, limit + 1):
        if vals[p] == 0:
            for n in range(p, limit + 1, p):
                vals[n] += 1
    return vals


def totient_independent(n: int) -> int:
    if n < 1:
        raise ValueError("positive integer required")
    return sum(gcd(k, n) == 1 for k in range(1, n + 1))


def v2(n: int) -> int:
    if n == 0:
        raise ValueError("v2 zero undefined")
    n = abs(n)
    return (n & -n).bit_length() - 1


def termwise_bad_positions(X: int, L: int, phi: list[int] | None = None) -> list[int]:
    if X < 2 or not 1 <= L <= X:
        raise ValueError("X>=2 and 1<=L<=X required")
    vals = phi if phi is not None else totient_sieve(2 * X + L)
    if len(vals) <= 2 * X - 1 + L:
        raise ValueError("totient list too short")
    return [N for N in range(X, 2 * X)
            if any(vals[N + j] % (1 << j) for j in range(1, L + 1))]


def finite_tail_numerator(N: int, L: int, phi: list[int]) -> int:
    if N < 1 or L < 1 or len(phi) <= N + L:
        raise ValueError("invalid finite tail source")
    return sum(phi[N + j] << (L - j) for j in range(1, L + 1))


def finite_markov_envelope(X: int, L: int, z: Fraction,
                           omega: list[int] | None = None) -> Fraction:
    """Exact finite inequality: #bad <= L*z^-L Σ_{n<=3X} z^omega(n).

    This can be (and is) extremely loose for computational X; no claim of
    finite useful numerical saving is made.
    """
    if X < 2 or not 1 <= L <= X or not (0 < z < 1):
        raise ValueError("invalid X, L or rational z")
    vals = omega if omega is not None else distinct_prime_factor_sieve(3 * X)
    if len(vals) <= 3 * X:
        raise ValueError("prime-factor sieve too short")
    return L * z**(-L) * sum((z**vals[n] for n in range(1, 3 * X + 1)),
                            Fraction())


def finite_explicit_bad_count_bound(X: int, L: int) -> dict:
    """Material receipt for z=1/2, independent of external asymptotics."""
    phi = totient_sieve(2 * X + L)
    omega = distinct_prime_factor_sieve(3 * X)
    bad = termwise_bad_positions(X, L, phi)
    bound = finite_markov_envelope(X, L, Fraction(1, 2), omega)
    if len(bad) > bound:
        raise AssertionError("finite Markov/union inequality disproved")
    nonintegral = [
        N for N in range(X, 2 * X)
        if finite_tail_numerator(N, L, phi) % (1 << L)
    ]
    if not set(nonintegral).issubset(set(bad)):
        raise AssertionError("a nonintegral finite sum has integral terms")
    return {
        "X": X, "L": L, "bad_count": len(bad),
        "nonintegral_sum_count": len(nonintegral),
        "markov_bound_numerator": str(bound.numerator),
        "markov_bound_denominator": str(bound.denominator),
        "boundary": "FINITE_CHECK_ONLY__SELBERG_DELANGE_EXTERNAL__FULL_S_OPEN",
    }


def first_omitted_term(N: int, L: int, phi: list[int] | None = None) -> Fraction:
    if N < 1 or L < 1:
        raise ValueError("positive N,L required")
    vals = phi if phi is not None else totient_sieve(N + L + 1)
    if len(vals) <= N + L + 1:
        raise ValueError("totient data too short")
    return Fraction(vals[N + L + 1], 1 << (L + 1))


def verify_totient_square_bound(limit: int) -> bool:
    phi = totient_sieve(limit)
    return all(2 * phi[n] * phi[n] >= n for n in range(1, limit + 1))
