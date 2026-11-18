"""Exact arithmetic for Erdős #249 WP04, without an irrationality verdict.

This module examines only rational truncations of the existing signed
Möbius/squared-Lambert representation of the *full* totient series.
It never estimates whether that full series is rational.
"""
from fractions import Fraction
from math import isqrt, prod


def mobius_values(limit: int) -> list[int]:
    """Return mu(0),...,mu(limit) by a standard prime/square sieve."""
    if limit < 1:
        raise ValueError("limit must be positive")
    mu = [1] * (limit + 1)
    mu[0] = 0
    prime = [True] * (limit + 1)
    prime[0:2] = [False, False]
    for p in range(2, limit + 1):
        if not prime[p]:
            continue
        for n in range(p, limit + 1, p):
            mu[n] *= -1
        for n in range(p * p, limit + 1, p * p):
            mu[n] = 0
        for n in range(p * p, limit + 1, p):
            prime[n] = False
    return mu


def mobius_one(n: int) -> int:
    """Independent trial-division oracle for small adversarial fixtures."""
    if n < 1:
        raise ValueError("n must be positive")
    left = n
    sign = 1
    for p in range(2, isqrt(n) + 1):
        if left % p == 0:
            left //= p
            sign = -sign
            if left % p == 0:
                return 0
            while left % p == 0:
                left //= p
    if left > 1:
        sign = -sign
    return sign


def weight(n: int) -> Fraction:
    if n < 1:
        raise ValueError("n must be positive")
    power = 1 << n
    return Fraction(power, (power - 1) ** 2)


def truncation(D: int) -> Fraction:
    if D < 1:
        raise ValueError("D must be positive")
    mu = mobius_values(D)
    return sum((mu[d] * weight(d) for d in range(1, D + 1)), Fraction())


def first_squarefree_after(D: int) -> int:
    if D < 0:
        raise ValueError("D must be nonnegative")
    n = D + 1
    while mobius_one(n) == 0:
        n += 1
    return n


def sign_of_exact_tail(D: int) -> int:
    """Proved analytic sign, *not* a finite-tail numerical inference."""
    return mobius_one(first_squarefree_after(D))


def strict_gap_lower(m: int) -> Fraction:
    """Strict lower bound Delta_m > 4/(3*4**m), proved in WP04."""
    if m < 1:
        raise ValueError("m must be positive")
    return Fraction(4, 3 * (4 ** m))


def absolute_tail_upper(D: int) -> Fraction:
    """For sum over d>D of mu(d)*weight(d), a valid strict upper bound."""
    if D < 0:
        raise ValueError("D must be nonnegative")
    m = D + 1
    x = 1 << m
    # Sum_{d>=m} 2^-d = 2^(1-m); factor (1-2^-m)^-2.
    return Fraction(2 * x, (x - 1) ** 2)


def primes_in_terminal_half(D: int) -> tuple[int, ...]:
    if D < 2:
        return ()
    result = []
    for p in range(2, D + 1):
        if 2 * p <= D:
            continue
        if all(p % d for d in range(2, isqrt(p) + 1)):
            result.append(p)
    return tuple(result)


def prime_window_forced_factor(D: int) -> int:
    """Proved divisor of the reduced denominator of truncation(D)."""
    return prod(((1 << p) - 1) ** 2 for p in primes_in_terminal_half(D))


def reduced_denominator_receipt(D: int) -> dict[str, object]:
    rational = truncation(D)
    factor = prime_window_forced_factor(D)
    if rational.denominator % factor:
        raise AssertionError("denominator isolation falsified")
    return {
        "depth": D,
        "numerator": str(rational.numerator),
        "denominator": str(rational.denominator),
        "denominator_decimal_digits": len(str(rational.denominator)),
        "prime_window": list(primes_in_terminal_half(D)),
        "forced_factor": str(factor),
        "forced_factor_decimal_digits": len(str(factor)),
        "verified_divides": True,
        "next_squarefree": first_squarefree_after(D),
        "exact_tail_sign": sign_of_exact_tail(D),
        "strict_gap_lower_num": str(strict_gap_lower(first_squarefree_after(D)).numerator),
        "strict_gap_lower_den": str(strict_gap_lower(first_squarefree_after(D)).denominator),
        "absolute_tail_upper_num": str(absolute_tail_upper(D).numerator),
        "absolute_tail_upper_den": str(absolute_tail_upper(D).denominator),
        "claim_boundary": "FULL_S_OPEN__FINITE_ARITHMETIC_ONLY",
    }
