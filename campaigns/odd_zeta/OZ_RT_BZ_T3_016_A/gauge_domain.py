from __future__ import annotations

from fractions import Fraction
from math import comb

from sympy import ZZ
from sympy.polys.matrices import DomainMatrix

DIMENSION = 24
DETERMINANT_DEGREE_BOUND = 144
RESIDUAL_DEGREE = 94
WITNESS_N = 5
WITNESS_PRIME = 4194301
WITNESS_BLOCK_DETERMINANT = 2300711

# Exact forced factors of the canonical 24x24 diagonal gauge block.
LINEAR_FACTOR_MULTIPLICITIES = (
    (0, 1),
    (1, 7),
    (2, 2),
    (3, 2),
    (4, 2),
    (5, 2),
    (6, 2),
    (7, 31),
    (8, 1),
)


def _convolve(left: list[int], right: list[int]) -> list[int]:
    out = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            out[i + j] += a * b
    return out


def _linear_product(factors: list[tuple[int, int]]) -> list[int]:
    out = [1]
    for constant, slope in factors:
        out = _convolve(out, [constant, slope])
    return out


def _matrix_rows(n: int) -> list[list[int]]:
    """Exact canonical 24x24 diagonal block, rows/columns l^0,...,l^23."""
    # A(l)=(n+7-l)^2 (n+l+1)^3.
    a_poly = _linear_product([(n + 7, -1)] * 2 + [(n + 1, 1)] * 3)
    # B(l)=(l+1)(l+2)(n+l+7).
    b_poly = _linear_product([(1, 1), (2, 1), (n + 7, 1)])

    rows = [[0] * DIMENSION for _ in range(DIMENSION)]
    for b in range(DIMENSION):
        shifted_monomial = [comb(b, t) for t in range(b + 1)]
        first = _convolve(a_poly, shifted_monomial)
        for j in range(DIMENSION):
            value = first[j] if j < len(first) else 0
            q = j - (b + 2)
            if 0 <= q < len(b_poly):
                value -= b_poly[q]
            rows[j][b] = (n + 7) * value
    return rows


def _determinant_at(n: int) -> int:
    matrix = DomainMatrix(_matrix_rows(n), (DIMENSION, DIMENSION), ZZ)
    return int(matrix.det())


def _interpolate_consecutive_integer_values(values: list[int]) -> list[int]:
    """Return power-basis coefficients, constant first, from f(0),...,f(d)."""
    differences = [Fraction(value) for value in values]
    newton = []
    while differences:
        newton.append(differences[0])
        differences = [
            differences[i + 1] - differences[i] for i in range(len(differences) - 1)
        ]

    coefficients = [Fraction(0)]
    binomial_basis = [Fraction(1)]
    for k, delta in enumerate(newton):
        if len(coefficients) < len(binomial_basis):
            coefficients.extend([Fraction(0)] * (len(binomial_basis) - len(coefficients)))
        for i, value in enumerate(binomial_basis):
            coefficients[i] += delta * value

        next_basis = [Fraction(0)] * (len(binomial_basis) + 1)
        for i, value in enumerate(binomial_basis):
            next_basis[i] -= Fraction(k, k + 1) * value
            next_basis[i + 1] += Fraction(1, k + 1) * value
        binomial_basis = next_basis

    while coefficients and coefficients[-1] == 0:
        coefficients.pop()
    if any(value.denominator != 1 for value in coefficients):
        raise AssertionError("determinant interpolation did not reconstruct Z[n]")
    return [int(value) for value in coefficients]


def _multiply_linear_power(coefficients: list[int], shift: int, multiplicity: int) -> list[int]:
    out = coefficients
    for _ in range(multiplicity):
        out = _convolve(out, [shift, 1])
    return out


def _forced_factor() -> list[int]:
    out = [1]
    for shift, multiplicity in LINEAR_FACTOR_MULTIPLICITIES:
        out = _multiply_linear_power(out, shift, multiplicity)
    return out


def _divide_exact(dividend: list[int], divisor: list[int]) -> tuple[list[int], list[int]]:
    if not divisor or divisor[-1] == 0:
        raise ZeroDivisionError("invalid polynomial divisor")
    work = dividend[:]
    quotient = [0] * max(1, len(dividend) - len(divisor) + 1)
    while len(work) >= len(divisor):
        lead = work[-1]
        divisor_lead = divisor[-1]
        if lead % divisor_lead:
            raise AssertionError("non-exact polynomial division")
        coefficient = lead // divisor_lead
        degree = len(work) - len(divisor)
        quotient[degree] = coefficient
        for i, value in enumerate(divisor):
            work[degree + i] -= coefficient * value
        while work and work[-1] == 0:
            work.pop()
    while quotient and quotient[-1] == 0:
        quotient.pop()
    return quotient or [0], work


def _shift(coefficients: list[int], amount: int) -> list[int]:
    out = [0] * len(coefficients)
    for degree, coefficient in enumerate(coefficients):
        for j in range(degree + 1):
            out[j] += coefficient * comb(degree, j) * amount ** (degree - j)
    return out


def _evaluate(coefficients: list[int], value: int) -> int:
    result = 0
    for coefficient in reversed(coefficients):
        result = result * value + coefficient
    return result


def build_gauge_domain() -> dict:
    samples = [_determinant_at(n) for n in range(DETERMINANT_DEGREE_BOUND + 1)]
    determinant = _interpolate_consecutive_integer_values(samples)
    if len(determinant) - 1 != DETERMINANT_DEGREE_BOUND:
        raise AssertionError("canonical block determinant degree drift")

    # One out-of-sample exact determinant evaluation closes the interpolation replay.
    if _evaluate(determinant, DETERMINANT_DEGREE_BOUND + 1) != _determinant_at(
        DETERMINANT_DEGREE_BOUND + 1
    ):
        raise AssertionError("determinant interpolation fresh-point failure")

    forced = _forced_factor()
    residual, remainder = _divide_exact(determinant, forced)
    if remainder:
        raise AssertionError("forced gauge determinant factorization failed")
    if len(residual) - 1 != RESIDUAL_DEGREE or residual[-1] != 1:
        raise AssertionError("residual factor degree/normalization drift")

    shifted = _shift(residual, 9)
    if not shifted or not all(value > 0 for value in shifted):
        raise AssertionError("R_94(n+9) positivity certificate failed")

    residual_small = [_evaluate(residual, n) for n in range(1, 9)]
    if any(value == 0 for value in residual_small):
        raise AssertionError("R_94 vanishes at an integer in 1..8")

    witness = _determinant_at(WITNESS_N) % WITNESS_PRIME
    if witness != WITNESS_BLOCK_DETERMINANT:
        raise AssertionError("governed modular witness drift")

    return {
        "matrix_dimension": DIMENSION,
        "determinant_degree": len(determinant) - 1,
        "forced_factor_degree": len(forced) - 1,
        "residual_degree": len(residual) - 1,
        "residual_monic": residual[-1] == 1,
        "residual_shift": 9,
        "residual_shift9_all_coefficients_positive": True,
        "residual_values_n_1_through_8": residual_small,
        "singular_nonnegative_integer_fibers": [0],
        "canonical_gauge_nonsingular_for_all_integers_n_gte": 1,
        "witness": {
            "n": WITNESS_N,
            "prime": WITNESS_PRIME,
            "block_determinant_mod_prime": witness,
        },
        "full_gauge_dimension": DIMENSION * DIMENSION,
        "full_gauge_block_count": DIMENSION,
        "proof_effect": "NONE",
        "promotion_effect": "NONE",
        "t3_proved": False,
        "global_certificate_constructed": False,
    }
