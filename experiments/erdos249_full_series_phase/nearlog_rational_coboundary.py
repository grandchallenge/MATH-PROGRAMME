"""WP07-B exact rational near-analytic-depth integer-tail comparator.

This is a counterexample to generic implications from high 2-adic
coefficient valuations and linear growth to irrationality or infinite
phase control. It is *not* Euler's totient and does not refute Cook's
totient-specific sufficient conditions.
"""
from fractions import Fraction


def modulus(n: int) -> int:
    if n < 1:
        raise ValueError("n must be positive")
    return 1 << max(0, n.bit_length() - 6)


def build_control(limit: int) -> tuple[list[int], list[int]]:
    """Return a_n, b_n through limit using a bounded variable carry.

    b_0=0; c_n=floor(n/2); M_n=2^max(0,floor(log2 n)-5).
    b_n=(c_n+2*b_(n-1)) mod M_n; a_n=c_n+2*b_(n-1)-b_n.
    """
    if limit < 1:
        raise ValueError("positive depth required")
    a = [0] * (limit + 1)
    b = [0] * (limit + 1)
    for n in range(1, limit + 1):
        raw = (n // 2) + 2 * b[n - 1]
        b[n] = raw % modulus(n)
        a[n] = raw - b[n]
    return a, b


def exact_value() -> Fraction:
    """Σ floor(n/2)*2^-n, by its rational generating function."""
    return Fraction(2, 3)


def finite_scaled_tail(N: int, L: int, a: list[int]) -> Fraction:
    if N < 1 or L < 1 or len(a) <= N + L:
        raise ValueError("invalid source/depth")
    return sum((Fraction(a[N + j], 1 << j)
                for j in range(1, L + 1)), Fraction())


def logarithmic_integer_depth(N: int) -> int:
    """For N>=64, this depth gives termwise integrality at every start."""
    if N < 64:
        raise ValueError("N>=64 required")
    return N.bit_length() - 6


def first_omitted_term(N: int, L: int, a: list[int]) -> Fraction:
    if N < 1 or L < 1 or len(a) <= N + L + 1:
        raise ValueError("invalid source/depth")
    return Fraction(a[N + L + 1], 1 << (L + 1))


def exact_full_scaled_tail(N: int, a: list[int]) -> Fraction:
    """U_N=2^N*(2/3)-integer-prefix for the infinite comparator."""
    if N < 1 or len(a) <= N:
        raise ValueError("invalid source/depth")
    prefix = sum(a[n] << (N - n) for n in range(1, N + 1))
    return (1 << N) * exact_value() - prefix


def fractional_part(x: Fraction) -> Fraction:
    return x - x.numerator // x.denominator


def receipt(N: int, a: list[int], b: list[int]) -> dict[str, object]:
    L = logarithmic_integer_depth(N)
    if len(a) <= N + L + 1 or len(b) <= N:
        raise ValueError("finite material too short")
    finite = finite_scaled_tail(N, L, a)
    lower = first_omitted_term(N, L, a)
    full = exact_full_scaled_tail(N, a)
    if finite.denominator != 1 or lower < 4:
        raise AssertionError("near-log integer or tail bound falsified")
    expected_fraction = Fraction(2 if N % 2 == 0 else 1, 3)
    if fractional_part(full - finite) != expected_fraction:
        raise AssertionError("rational infinite-tail fraction mismatch")
    return {
        "N": N, "L": L,
        "finite_integer": str(finite.numerator),
        "first_omitted_term": str(lower),
        "full_tail_fraction_numerator": expected_fraction.numerator,
        "full_tail_fraction_denominator": expected_fraction.denominator,
        "bound_ratio": "n/4<=a_n<=n for n>=2",
        "series_value": "2/3",
        "boundary": "RATIONAL_CONTROL_ONLY__ORIGINAL_ERDOS_249_OPEN",
    }
