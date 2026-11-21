"""ERDOS249 WP09-D: exact positive-definite shifted-totient covariance.

Proves and tests the single-prime conditional projection for any
nonzero finite integer difference signature. Mathematical theorems and
infinite-limit arguments are in JOINT_COVARIANCE_GAP_009D.md.

This module supplies finite exact-rational checks and optional finite
real-phase diagnostics. No assertion of original irrationality or
independent mathematical certification.
"""
from __future__ import annotations

from cmath import exp
from fractions import Fraction
from math import pi, prod

from experiments.erdos249_full_series_phase.joint_local_prime_law import (
    profile, primes_through,
)
from experiments.erdos249_full_series_phase.overlog_phase_separation import (
    totients,
)


def signature(terms: tuple[tuple[int, int, int], ...]
              ) -> tuple[tuple[int, int], ...]:
    """Canonical nonzero zero-sum coefficient vector (offset, coefficient)."""
    if not isinstance(terms, tuple) or not terms:
        raise ValueError("nonempty tuple of triples required")
    c: dict[int, int] = {}
    for entry in terms:
        if (not isinstance(entry, tuple) or len(entry) != 3 or
                any(type(t) is not int for t in entry)):
            raise ValueError("each entry must contain three actual integers")
        w, a, b = entry
        if a < 0 or b < 0:
            raise ValueError("offsets must be nonnegative")
        c[a] = c.get(a, 0) + w
        c[b] = c.get(b, 0) - w
    sig = tuple((s, w) for s, w in sorted(c.items()) if w)
    if not sig or sum(w for _, w in sig) != 0:
        raise ValueError("nonzero zero-sum difference signature required")
    return sig


def signature_norms(terms: tuple[tuple[int, int, int], ...]
                    ) -> dict[str, int]:
    sig = signature(terms)
    return {
        "H": sig[-1][0],
        "B": sum(abs(w) for _, w in sig),
        "squared": sum(w * w for _, w in sig),
        "support": len(sig),
    }


def first_separating_prime(terms: tuple[tuple[int, int, int], ...]) -> int:
    """First prime strictly larger than the largest occupied offset."""
    H = signature_norms(terms)["H"]
    p = max(2, H + 1)
    while True:
        isprime = all(p % d for d in range(2, int(p**0.5) + 1))
        if isprime:
            return p
        p += 1


def conditional_projection(
    terms: tuple[tuple[int, int, int], ...],
    y: int,
    max_period: int = 100_000,
) -> dict[str, object]:
    """Exact finite CRT conditional variance for one separating prime.

    For P_y = product_{q<=y}q, f_y(a) = product_{q<=y,q|a}(1-1/q),
    Delta_y(a) = sum_s c_s f_y(a+s).

    E[Delta_y | a mod p =r] = -mu_(y,p) c_(-r mod p)/p,
    where mu_(y,p)=product_{q<=y,q!=p}(1-1/q^2).
    """
    sig = signature(terms)
    p = first_separating_prime(terms)
    if type(y) is not int or y < p:
        raise ValueError("cutoff must include the separating prime")
    P, ds = profile(y, terms, max_period=max_period)
    if P % p:
        raise AssertionError("CRT period is missing separating prime")
    ps = primes_through(y)
    mu_other = prod(
        (1 - Fraction(1, q*q) for q in ps if q != p),
        start=Fraction(1))
    c = dict(sig)
    theoretical = tuple(
        -mu_other * c.get((-r) % p, 0) / p
        for r in range(p))
    observed = tuple(
        sum((ds[a] for a in range(r, P, p)), Fraction()) / (P // p)
        for r in range(p))
    if observed != theoretical:
        raise AssertionError("exact conditional projection mismatch")
    if sum(observed, Fraction()) != 0:
        raise AssertionError("difference signature lost its zero mean")
    projection_energy = sum((z*z for z in observed), Fraction()) / p
    expected = mu_other**2 * sum(w*w for _, w in sig) / (p**3)
    if projection_energy != expected:
        raise AssertionError("single-prime L2 projection identity failed")
    total_energy = sum((z*z for z in ds), Fraction()) / P
    if total_energy < projection_energy:
        raise AssertionError("CRT conditional variance exceeds total")
    return {
        "cutoff": y,
        "period": P,
        "separating_prime": p,
        "signature": sig,
        "mu_other": mu_other,
        "conditional_means": observed,
        "conditional_energy": projection_energy,
        "exact_variance": total_energy,
        "simple_uniform_lower": Fraction(9,25*p**3) *
            sum(w*w for _, w in sig),
        "variance_at_least_projection": True,
        "original_series_status": "OPEN",
    }


def finite_product_covariance(
    terms: tuple[tuple[int, int, int], ...],
    y: int
) -> Fraction:
    """Independent Euler-product reconstruction of finite CRT covariance."""
    sig = signature(terms)
    ps = primes_through(y)
    def pair(s: int, t: int) -> Fraction:
        h = abs(s-t)
        value = Fraction(1)
        for p in ps:
            a = Fraction(1) - Fraction(2,p*p) + Fraction(1,p**3)
            b = a if h % p == 0 else Fraction(1) - Fraction(2,p*p)
            value *= b
        return value
    return sum(
        (w*v*pair(s,t) for s,w in sig for t,v in sig),
        Fraction())


def finite_cos_gap_bound(
    terms: tuple[tuple[int, int, int], ...],
    y: int, rho: int | Fraction,
) -> Fraction:
    """Exact rational analytic lower bound on 1-Re C_y(rho).

    Valid when rho >=4B, where B=sum_s |c_s|. Uses
    1-cos(2*pi*x) >= 8*x^2 for |x|<=1/2 and integral t²=7/3.
    """
    ns = signature_norms(terms)
    if not isinstance(rho, (int, Fraction)) or rho < 4*ns["B"]:
        raise ValueError("rho must be rational and >=4B")
    P, ds = profile(y, terms)
    v = sum((d*d for d in ds), Fraction()) / P
    return Fraction(56,3) * v / (rho*rho)


def actual_phase_energy(
    X: int, Q: int,
    terms: tuple[tuple[int, int, int], ...],
) -> dict[str, object]:
    """Finite actual totient-phase check with exact rational L2 bound.

    This verifies a deterministic inequality at finite X; it does not
    claim the asymptotic theorem from a finite computation.
    """
    ns = signature_norms(terms)
    if (type(X) is not int or type(Q) is not int or
            X < max(64,ns["H"]) or Q < 6*ns["B"]*X):
        raise ValueError("X>=max(64,H), Q>=6BX required")
    sig = signature(terms)
    phi = totients(2*X + ns["H"] + 1)
    ds = tuple(sum(c*phi[n+s] for s,c in sig)
               for n in range(X, 2*X))
    if max(abs(d) for d in ds)*2 > Q:
        raise AssertionError("phase escaped centered half interval")
    energy = sum(d*d for d in ds)
    gap_lower = Fraction(8*energy, X*Q*Q)
    numeric_gap = sum(1 - exp(2j*pi*d/Q).real for d in ds)/X
    if numeric_gap + 1e-12 < float(gap_lower):
        raise AssertionError("numeric phase violates exact analytic lower")
    return {
        "X": X, "Q": Q, "local_difference_energy": energy,
        "exact_phase_gap_lower": gap_lower,
        "numeric_actual_phase_gap": numeric_gap,
        "full_cook_harmonic": False,
        "irrationality_status": "OPEN",
    }
