"""Exact sparse-binary orbit bounds; a no-go control, never a proof of Erdős #249."""
from __future__ import annotations

import math


def exponent(m: int) -> int:
    """Protected source: Erdos249Bounded.exponent m = 2^(m+1) - m."""
    if m < 0:
        raise ValueError("m must be nonnegative")
    return (1 << (m + 1)) - m


def support_through(y: int) -> tuple[int, ...]:
    """Enumerate exponents e_m <= y without truncating their exact integers."""
    ans = []
    m = 0
    while exponent(m) <= y:
        ans.append(exponent(m))
        m += 1
    return tuple(ans)


def dyadic_residue(N: int, L: int) -> int:
    """Exact floor(2^L frac(2^N T)), with sparse binary support."""
    if N < 0 or L < 1:
        raise ValueError("N>=0 and L>=1 required")
    return sum(1 << (N + L - e) for e in support_through(N + L) if e > N)


def exceptional_count(X: int, K: int) -> int:
    """Count N in [X,2X) with support at some position N+1,...,N+K."""
    if X < 1 or K < 1:
        raise ValueError("positive X and K required")
    bad = set()
    for e in support_through(2 * X + K):
        lo, hi = max(X, e - K), min(2 * X - 1, e - 1)
        if hi >= lo:
            bad.update(range(lo, hi + 1))
    return len(bad)


def universal_phase_bound(X: int, K: int, H: int) -> float:
    """Rigorous analytic |mean_N e(h*2^N*T)-1| bound, all integer |h|<=H.

    Uses e_m>=2^m, so B(y)<=1+floor(log2 y), and covers at most K bad
    N per supported binary digit. No transcendental numerical certification
    is implied by the floating-point evaluation of the bound.
    """
    if X < 1 or K < 1 or H < 0:
        raise ValueError("X>=1, K>=1, H>=0 required")
    # bit_length(2X+K) = 1+floor(log2(2X+K)), exactly.
    return (2 * math.pi * H * 2 ** (-K)
            + 2 * K * (2 * X + K).bit_length() / X)


def sharpened_phase_bound(X: int, K: int, H: int) -> float:
    """Same rigorous estimate using the exact finite exceptional count."""
    return 2 * math.pi * H * 2 ** (-K) + 2 * exceptional_count(X, K) / X


def phase_mean(X: int, L: int, h: int) -> complex:
    """Finite approximation to the actual sparse irrational's doubling orbit.

    The difference from the true mean is <=2*pi*|h|*2^(-L) analytically.
    Trigonometric arithmetic here is not interval-certified.
    """
    if X < 1 or L < 1:
        raise ValueError("X>=1 and L>=1 required")
    modulus = 1 << L
    real = imag = 0.0
    for N in range(X, 2 * X):
        r = dyadic_residue(N, L)
        q = (h * r) % modulus
        theta = 2 * math.pi * (q / modulus)
        real += math.cos(theta)
        imag += math.sin(theta)
    return complex(real / X, imag / X)


def polynomial_harmonic_bound(X: int, degree: int) -> dict:
    """Quantitative uniform theorem for all integer |h| <= X^degree."""
    if X < 2 or degree < 0 or degree > 8:
        raise ValueError("X>=2 and 0<=degree<=8 required")
    K = (degree + 2) * (X - 1).bit_length()
    H = X ** degree
    # Since X<=2^ceil(log2 X), we have 2^-K <= X^(-degree-2).
    return {
        "X": X,
        "degree": degree,
        "H": H,
        "K": K,
        "support_count": len(support_through(2 * X + K)),
        "exceptional_count": exceptional_count(X, K),
        "universal_bound": universal_phase_bound(X, K, H),
        "exact_exception_bound": sharpened_phase_bound(X, K, H),
    }
