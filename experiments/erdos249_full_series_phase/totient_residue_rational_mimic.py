"""WP07-E: rational binary series with the *same* nearlog totient residues.

This is an exact adversarial mathematical control, not Euler's totient and
not a proof/refutation of the irrationality of its binary series.

a_n = floor(n/2) + 2*b_(n-1) - b_n
b_n = (floor(n/2)+2*b_(n-1)-phi(n)) mod M_n
M_n = 2^max(0,floor(log2 n)-2).

The full series sum a_n/2^n is exactly 2/3, yet a_n=phi(n) mod M_n at
EVERY n. At depth floor(log2 N)-2, the *whole* finite tail fractional
part and every integral Fourier harmonic are exactly identical to the
actual totient tail at each N>=8.
"""
from fractions import Fraction
from math import gcd


def phi_sieve(limit: int) -> list[int]:
    if limit < 1:
        raise ValueError("limit must be positive")
    v = list(range(limit + 1))
    for p in range(2, limit + 1):
        if v[p] == p:
            for n in range(p, limit + 1, p):
                v[n] -= v[n] // p
    return v


def phi_independent(n: int) -> int:
    if n < 1:
        raise ValueError("positive n required")
    return sum(gcd(n, k) == 1 for k in range(1, n + 1))


def power2_modulus(n: int) -> int:
    if n < 1:
        raise ValueError("positive n required")
    return 1 << max(0, n.bit_length() - 3)


def v2_positive(n: int) -> int:
    if n <= 0:
        raise ValueError("positive integer required")
    return (n & -n).bit_length() - 1


def rational_totient_residue_mimic(limit: int,
                                  phi: list[int] | None = None
                                  ) -> tuple[list[int], list[int]]:
    """Build a,b through 'limit'; b_0=0; phi may be independent input."""
    if limit < 1:
        raise ValueError("positive limit required")
    values = phi if phi is not None else phi_sieve(limit)
    if len(values) <= limit:
        raise ValueError("totient source too short")
    a, b = [0] * (limit + 1), [0] * (limit + 1)
    for n in range(1, limit + 1):
        c = n // 2
        q = c + 2 * b[n-1]
        b[n] = (q - values[n]) % power2_modulus(n)
        a[n] = q - b[n]
        if (a[n] - values[n]) % power2_modulus(n):
            raise AssertionError("residue matching violated")
        if n >= 2 and not (4*a[n] >= n and a[n] <= n):
            raise AssertionError("linear coefficient envelope violated")
    return a, b


def finite_scaled_numerator(N: int, L: int, coefficients: list[int]) -> int:
    if N < 1 or L < 1 or len(coefficients) <= N + L:
        raise ValueError("invalid N, L, or source")
    return sum(coefficients[N+j] << (L-j) for j in range(1, L+1))


def nearlog_depth(N: int) -> int:
    if N < 8:
        raise ValueError("N>=8 required")
    return N.bit_length() - 3


def finite_tail_integer_difference(N: int, coefficients: list[int],
                                   phi: list[int]) -> int:
    L = nearlog_depth(N)
    difference = (finite_scaled_numerator(N, L, coefficients)
                  - finite_scaled_numerator(N, L, phi))
    if difference % (1 << L):
        raise AssertionError("the two finite tails have unequal fractional parts")
    return difference >> L


def exact_rational_sum() -> Fraction:
    """Analytical value: Σ floor(n/2)2^-n = 2/3."""
    return Fraction(2, 3)


def exact_scaled_infinite_tail(N: int, coefficients: list[int]) -> Fraction:
    if N < 1 or len(coefficients) <= N:
        raise ValueError("N must have an exact finite prefix")
    integer_prefix = sum(coefficients[j] << (N-j) for j in range(1, N+1))
    return (1 << N) * exact_rational_sum() - integer_prefix


def frac(x: Fraction) -> Fraction:
    return x - (x.numerator // x.denominator)


def finite_receipt(X: int) -> dict[str, object]:
    if X < 8:
        raise ValueError("X>=8 required")
    phi = phi_sieve(2*X + X.bit_length())
    a, b = rational_totient_residue_mimic(2*X + X.bit_length(), phi)
    L = nearlog_depth(X)
    errors = []
    for N in range(X, 2*X):
        q_a = finite_scaled_numerator(N, L, a)
        q_phi = finite_scaled_numerator(N, L, phi)
        if (q_a-q_phi) % (1 << L):
            errors.append(N)
    mismatches = [
        n for n in range(2, 2*X)
        if v2_positive(a[n]) != v2_positive(phi[n])
    ]
    nearmax2 = [
        n for n in range(2, 2*X)
        if v2_positive(phi[n]) >= max(0, n.bit_length()-3)
    ]
    if not set(mismatches).issubset(set(nearmax2)):
        raise AssertionError("valuation exceptional set not contained in E_2")
    if errors:
        raise AssertionError("some nearlog finite fractional parts disagree")
    return {
        "X": X, "L": L, "all_starts_identical_residue": True,
        "starts_checked": X, "valuation_mismatches": len(mismatches),
        "nearmax2_candidates": len(nearmax2),
        "rational_full_series": "2/3",
        "claim_boundary": "EXACT_FINITE_CONTROL_ONLY__ACTUAL_TOTIENT_S_OPEN",
    }
