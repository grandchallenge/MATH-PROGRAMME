"""Exact rational prime-pulse negative control for Erdős #249 WP06.

The coefficient sequence a_n=4*floor(n/8)+2*b_(n-1)-b_n has
rational dyadic sum 8/255 for ANY bounded binary b with b_0=0.
The constructed b has sparse support at selected prime pulses.

Not a theorem about the Euler totient sequence or a solution to #249.
"""
from fractions import Fraction
from math import isqrt


def prime_3mod4_after(lower):
    """Finite witness generator; cofinal existence is a classical theorem."""
    if lower < 0:
        raise ValueError("lower bound must be nonnegative")
    n = max(3, lower + 1)
    n += (3 - n) % 4
    while True:
        if all(n % d for d in range(3, isqrt(n) + 1, 2)):
            return n
        n += 4


def separated_pulse_primes(shifts, count, lower=11):
    """Construct a finite initial segment of a cofinal sparse prime family."""
    hs = tuple(sorted(set(shifts)))
    if not hs or hs[0] < 1 or count < 1:
        raise ValueError("nonempty positive shifts and positive count required")
    pset = []
    threshold = max(10, lower - 1)
    for _ in range(count):
        p = prime_3mod4_after(threshold)
        pset.append(p)
        threshold = p + 4 * hs[-1] + 8
    return tuple(pset)


def pulse_support(shifts, primes):
    """A finite prefix of the infinite binary coboundary support."""
    hs = tuple(sorted(set(shifts)))
    ps = tuple(primes)
    if not hs or hs[0] < 1 or not ps:
        raise ValueError("nonempty positive shifts and nonempty prime family")
    if ps[0] < 11 or any(p % 4 != 3 for p in ps):
        raise ValueError("prime positions must be >=11 and 3 modulo 4")
    if any(prime_3mod4_after(p-1) != p for p in ps):
        raise ValueError("all prime positions must be prime")
    if any(p2 <= p1 + 4 * hs[-1] + 1 for p1, p2 in zip(ps, ps[1:])):
        raise ValueError("successive pulse windows must be disjoint")
    return frozenset(p + 4 * h - 1 for p in ps for h in hs)


def coefficient(n, support):
    if n < 1:
        raise ValueError("index must be positive")
    value = 4 * (n // 8) + 2 * int(n - 1 in support) - int(n in support)
    return value


def exact_value():
    """Sum_{n>=1} 4*floor(n/8)*2^-n, independent of support."""
    return Fraction(8, 255)


def partial_coboundary(N, support):
    """Exact identity Σ_{n<=N}(2b_(n-1)-b_n)2^-n=-b_N/2^N."""
    if N < 0:
        raise ValueError("depth must be nonnegative")
    return sum((Fraction(2 * int(n-1 in support) - int(n in support), 1 << n)
                for n in range(1, N + 1)), Fraction())


def partial_value(N, support):
    if N < 0:
        raise ValueError("depth must be nonnegative")
    return sum((Fraction(coefficient(n, support), 1 << n)
                for n in range(1, N + 1)), Fraction())


def verify_finite_pulses(shifts, primes, support):
    hs = tuple(sorted(set(shifts)))
    for p in primes:
        if (p-1) in support or p in support:
            raise AssertionError("pulse base contaminated")
        for h in hs:
            v = coefficient(p + 4*h, support) - coefficient(p, support)
            if v % 4 != 2:
                raise AssertionError("prime pulse congruence absent")
    return True


def discarded_difference_bound(N, H, L):
    """One-sided bound for 0<=a_n<=n, from the *original full difference*."""
    if N < 0 or H < 1 or L < 1:
        raise ValueError("invalid shift, start or depth")
    return Fraction(N + H + L + 2, 1 << L)


def depth_for_unit_tail_bound(N, H):
    """Smallest depth at which the *upper bound* is strictly below one."""
    if N < 0 or H < 1:
        raise ValueError("invalid start or shift")
    L = 1
    while (1 << L) <= N + H + L + 2:
        L += 1
    return L


def same_depth_obstruction(N, H, L, K, final_coeff):
    """Certified general necessary-depth obstruction (not a proof of S)."""
    if K < 1 or L < 1 or N < 0 or H < 1 or final_coeff <= 0:
        raise ValueError("positive coefficient, threshold and depth required")
    if final_coeff % (1 << K):
        raise ValueError("endpoint does not satisfy 2-adic premise")
    if final_coeff > N + L:
        raise ValueError("coefficient exceeds argument")
    if L > K:
        return False
    assert (N + L) >= (1 << K)
    assert discarded_difference_bound(N, H, L) > 1
    return True
