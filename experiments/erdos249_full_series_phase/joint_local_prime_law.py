"""ERDOS249 WP09-C: finite-prime model for local shifted-totient joint phases.

Exact CRT profiles and a rigorously derived numerical error envelope.
Only fixed finite shifted DIFFERENCES scaled by Q are covered.
The exponentially weighted Cook window D_h(N,L)/Q is NOT covered.

The theorem, quantifiers, and mathematical proof appear in
JOINT_LOCAL_PRIME_LAW_009C.md. No originality, MATHCERT, or
original-series irrationality certification is claimed.
"""
from cmath import exp
from fractions import Fraction
from math import isqrt, log, pi, prod, sin

Term = tuple[int, int, int]  # (integer weight, plus offset, minus offset)


def _validated(terms: tuple[Term, ...]) -> tuple[int, int]:
    if not isinstance(terms, tuple) or not terms:
        raise ValueError("nonempty tuple of (weight, plus, minus) required")
    W = 0
    H = 0
    for entry in terms:
        if (not isinstance(entry, tuple) or len(entry) != 3
                or any(type(v) is not int for v in entry)):
            raise ValueError("each term must be three actual integers")
        w, a, b = entry
        if a < 0 or b < 0:
            raise ValueError("offsets must be nonnegative")
        W += abs(w)
        H = max(H, a, b)
    if W == 0:
        raise ValueError("at least one nonzero weight required")
    return W, H


def primes_through(y: int) -> tuple[int, ...]:
    if type(y) is not int or y < 2:
        raise ValueError("integer cutoff y>=2 required")
    flags = bytearray(b"\x01") * (y + 1)
    flags[:2] = b"\x00\x00"
    for p in range(2, isqrt(y) + 1):
        if flags[p]:
            flags[p * p:y + 1:p] = b"\x00" * ((y - p * p) // p + 1)
    return tuple(p for p in range(2, y + 1) if flags[p])


def profile(y: int, terms: tuple[Term, ...], max_period: int = 100_000
            ) -> tuple[int, tuple[Fraction, ...]]:
    """Exact CRT period P_y and Delta_y(a) on every residue a modulo P_y.

    Delta_y(a) = sum_w w*(f_y(a+plus)-f_y(a+minus)).
    Returns rational values: no floating-point arithmetic in the CRT engine.
    """
    _validated(terms)
    ps = primes_through(y)
    P = prod(ps)
    if type(max_period) is not int or max_period < 1 or P > max_period:
        raise ValueError("prime-period resource cap exceeded")
    values = [Fraction(1)] * P
    for p in ps:
        factor = Fraction(p - 1, p)
        for a in range(0, P, p):
            values[a] *= factor
    deltas = tuple(sum(
        (w * (values[(a + plus) % P] - values[(a + minus) % P])
         for w, plus, minus in terms), Fraction(0))
        for a in range(P))
    return P, deltas


def exact_moment(y: int, terms: tuple[Term, ...], degree: int,
                 max_period: int = 100_000) -> Fraction:
    """Exact rational CRT average of Delta_y^degree."""
    if type(degree) is not int or degree < 0:
        raise ValueError("degree must be nonnegative integer")
    P, ds = profile(y, terms, max_period)
    return sum((d ** degree for d in ds), Fraction(0)) / P


def characteristic(y: int, terms: tuple[Term, ...], rho: float,
                   max_period: int = 100_000) -> complex:
    """Finite-prime joint characteristic integrated over 1<=t<=2.

    Numerical evaluation of an exactly defined finite integral:
    C_y(rho)= P^-1 sum_a integral_1^2 exp(2*pi*i*t*Delta_y(a)/rho) dt.
    Integral equals exp(3*pi*i*Delta/rho)*sinc(pi*Delta/rho).
    """
    if not isinstance(rho, (float, int)) or not 32 <= rho < float("inf"):
        raise ValueError("rho must be finite and >=32")
    P, ds = profile(y, terms, max_period)
    total = 0j
    for d in ds:
        angle = pi * float(d) / rho
        sinc = sin(angle) / angle if angle else 1.0
        total += exp(3j * angle) * sinc
    return total / P


def effective_error(X: int, Q: int, y: int, terms: tuple[Term, ...],
                    max_period: int = 100_000) -> float:
    """Rigorous upper bound |actual local phase mean - C_y(Q/X)|.

    The theorem uses only |exp(2*pi*i*u)-exp(2*pi*i*v)|<=2*pi*|u-v|,
    count of multiples in an X-block, and a periodic Riemann-sum bound.
    The returned FLOAT is a conservative representation of an analytic
    bound, not a machine-certified interval-arithmetic upper bound.
    """
    W, H = _validated(terms)
    if type(X) is not int or type(Q) is not int or X < 64 or Q < 32 * X:
        raise ValueError("integer X>=64, Q>=32X required")
    ps = primes_through(y)
    P = prod(ps)
    if type(max_period) is not int or max_period < 1 or P > max_period:
        raise ValueError("prime-period resource cap exceeded")
    rho = Q / X
    harmonic_bound = 1 + log(2 * X + H)
    return (4 * pi * H * W / Q
            + 8 * pi * W / rho * (1 / y + harmonic_bound / X)
            + P / X * (2 + 4 * pi * W / rho))


def infinite_model_truncation_bound(y: int, terms: tuple[Term, ...],
                                    rho: float) -> float:
    """Bound |C_y(rho)-C_infinity(rho)| uniformly for rho>=32."""
    W, _ = _validated(terms)
    if not isinstance(rho, (float, int)) or not 32 <= rho < float("inf"):
        raise ValueError("rho must be finite and >=32")
    primes_through(y)
    return 8 * pi * W / (rho * y)


def actual_local_characteristic(X: int, Q: int, terms: tuple[Term, ...],
                                phi: list[int]) -> complex:
    """Finite check ONLY; the analytic theorem does not rely on samples."""
    _, H = _validated(terms)
    if type(X) is not int or type(Q) is not int or X < 64 or Q < 32 * X:
        raise ValueError("integer X>=64, Q>=32X required")
    if len(phi) <= 2 * X + H:
        raise ValueError("totient oracle does not cover all shifted indices")
    total = 0j
    for n in range(X, 2 * X):
        d = sum(w * (phi[n + a] - phi[n + b])
                for w, a, b in terms)
        total += exp(2j * pi * d / Q)
    return total / X
