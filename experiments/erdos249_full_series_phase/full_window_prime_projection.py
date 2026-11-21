"""Erdos #249 WP09-E: fixed-prime projection across the full Cook window.

Implements exact rational finite CRT aliases, exact dyadic residue weights,
the explicit integer sufficient condition for full-window L2 energy, and
the genuine Cook numerator by an independent exact rolling recurrence.

PROOF is in FULL_WINDOW_PRIME_PROJECTION_009E.md. Numerical diagnostics do
not constitute a Cook first-harmonic cancellation theorem or MATHCERT.
"""
from __future__ import annotations

from fractions import Fraction
from math import isqrt, prod

from experiments.erdos249_full_series_phase.fourier_probe import totients
from experiments.erdos249_full_series_phase.joint_local_prime_law import (
    primes_through,
)


def _positive(value: int, name: str) -> None:
    if type(value) is not int or value < 1:
        raise ValueError(f"{name} must be a positive ordinary integer")


def fixed_separating_prime(h: int) -> int:
    """First prime p NOT dividing the fixed shift h (p need not exceed L+h)."""
    _positive(h, "h")
    p = 2
    while True:
        if h % p and all(p % d for d in range(2, isqrt(p) + 1)):
            return p
        p += 1


def cook_minimal_depth(X: int, h: int) -> int:
    """Least L>=h satisfying Cook's exact 16(2X+h+L+2)<=2**L."""
    _positive(X, "X")
    _positive(h, "h")
    L = h
    while (1 << L) < 16 * (2 * X + h + L + 2):
        L += 1
    return L


def dyadic_residue_weights(h: int, L: int, p: int | None = None
                           ) -> dict[str, object]:
    """Return exact Q-weighted q_r and t_r = q_(r-h) - q_r.

    q_r= sum_{1<=j<=L,j congruent r mod p} 2**(-j);
    values returned are integer numerators of denominator Q=2**L.
    """
    _positive(h, "h")
    _positive(L, "L")
    if p is None:
        p = fixed_separating_prime(h)
    if type(p) is not int or p < 2 or h % p == 0:
        raise ValueError("p must be a prime not dividing h")
    if any(p % d == 0 for d in range(2, isqrt(p) + 1)):
        raise ValueError("p is not prime")
    Q = 1 << L
    q = [0] * p
    for j in range(1, L + 1):
        q[j % p] += 1 << (L - j)
    t = tuple(q[(r - h) % p] - q[r] for r in range(p))
    if sum(t) != 0 or 6 * t[(h + 1) % p] < Q or 6 * (-t[1 % p]) < Q:
        raise AssertionError("two uniform dyadic separating coordinates failed")
    return {
        "h": h, "L": L, "p": p, "Q": Q,
        "q_numerators": tuple(q), "t_numerators": t,
        "positive_class": (h + 1) % p, "negative_class": 1 % p,
        "alias_l2_numerator": sum(v * v for v in t),
    }


def exact_finite_crt_projection(
    h: int, L: int, y: int, max_period: int = 10_000
) -> dict[str, object]:
    """Exact finite-prime CRT verification with overlapping shifts modulo p.

    Computes independent residue averages and matches the conditional
    projection -mu_(y,p) * t_(-r) / p, where t is already Q-normalized.
    """
    _positive(y, "y")
    w = dyadic_residue_weights(h, L)
    p = w["p"]
    if y < p:
        raise ValueError("the cutoff must include the fixed separating prime")
    ps = primes_through(y)
    P = prod(ps)
    if P > max_period:
        raise ValueError("finite CRT period exceeds the explicit cap")
    Q = w["Q"]
    mu = prod((1 - Fraction(1, q*q) for q in ps if q != p),
              start=Fraction(1))
    vals = []
    for a in range(P):
        v = Fraction()
        for j in range(1, L + 1):
            weight = Fraction(1, 1 << j)
            def fy(m: int) -> Fraction:
                return prod((Fraction(q-1, q) for q in ps if m % q == 0),
                            start=Fraction(1))
            v += weight * (fy(a+h+j) - fy(a+j))
        vals.append(v)
    observed = tuple(
        sum((vals[a] for a in range(r, P, p)), Fraction()) / (P // p)
        for r in range(p)
    )
    predicted = tuple(
        -mu * w["t_numerators"][(-r) % p] / (p*Q)
        for r in range(p)
    )
    if observed != predicted:
        raise AssertionError("actual finite CRT overlapping-shift oracle fails")
    if sum(observed, Fraction()) != 0:
        raise AssertionError("conditional means should sum to zero")
    return {
        "period": P, "p": p, "mu_other": mu, "observed": observed,
        "predicted": predicted, "l2_mean_projection":
            sum((z*z for z in observed), Fraction()) / p,
        "fixed_prime_alias_vector": w["t_numerators"],
    }


def projection_certificate(X: int, h: int, L: int | None = None
                           ) -> dict[str, object]:
    """Exact integer prerequisites for a certified all-Cook-window L2 bound.

    If eligible, proven:
      (1/X) sum G(N)**2 >= 1/(400 p**3)
      sum (D(N)/Q)**2 >= X**3/(1600 p**3)
    Here G is the full *normalized-totient* weighted window, whereas
    D/Q is the original *unwrapped* Cook phase argument. Neither is
    a modulo-one bound.
    """
    _positive(X, "X")
    _positive(h, "h")
    if L is None:
        L = cook_minimal_depth(X, h)
    w = dyadic_residue_weights(h, L)
    p, Q = w["p"], w["Q"]
    H = L + h
    E = 3 + (3*X).bit_length()
    requirement = 40*p*p*max(E, h+4)
    eligible = H <= X and X >= requirement
    return {
        "X": X, "h": h, "L": L, "H": H, "p": p, "Q": Q,
        "integer_discrepancy_majorant": E,
        "required_min_X": requirement,
        "window_fits_interval": H <= X,
        "eligible": eligible,
        "normalized_ratio_mean_square_lower":
            Fraction(1, 400*p**3) if eligible else None,
        "unwrapped_phase_sum_square_lower":
            Fraction(X**3, 1600*p**3) if eligible else None,
        "weighted_first_harmonic_tenth_saving": False,
        "original_irrationality": "OPEN",
    }


def cook_numerator_direct(phi: list[int], N: int, h: int, L: int) -> int:
    """Direct exact sum for an independent oracle; phi must be long enough."""
    return sum((1 << (L-j)) * (phi[N+h+j] - phi[N+j])
               for j in range(1, L+1))


def cook_numerators_rolling(phi: list[int], X: int, h: int, L: int
                            ) -> tuple[int, ...]:
    """Compute every actual D_h,N,L using the exact dyadic cocycle."""
    _positive(X, "X")
    _positive(h, "h")
    _positive(L, "L")
    if len(phi) <= 2*X+h+L:
        raise ValueError("totient buffer too short for the block")
    Q = 1 << L
    D = cook_numerator_direct(phi, X, h, L)
    result = [D]
    for N in range(X, 2*X-1):
        D = (2*D
             - Q*(phi[N+h+1]-phi[N+1])
             + (phi[N+h+L+1]-phi[N+L+1]))
        result.append(D)
    return tuple(result)


def exact_actual_window_energy(X: int, h: int, L: int | None = None,
                               max_X: int = 100_000
                               ) -> dict[str, object]:
    """Finite exact integer true-Cook numerator test, no floating dependence."""
    c = projection_certificate(X, h, L)
    if X > max_X:
        raise ValueError("finite execution exceeds bounded smoke-test budget")
    vals = cook_numerators_rolling(
        totients(2*X+c["H"]+1), X, h, c["L"])
    energy = sum(z*z for z in vals)
    if c["eligible"]:
        # Exact integer comparison: sum D² / Q² >= X³/(1600*p³).
        if 1600*c["p"]**3*energy < X**3*c["Q"]**2:
            raise AssertionError("actual arithmetic violates proved energy")
    return {
        **c,
        "sum_D_squared": energy,
        "energy_bound_passed": c["eligible"] and
            (1600*c["p"]**3*energy >= X**3*c["Q"]**2),
        "source": "actual Euler totient, exact integer rolling",
    }
