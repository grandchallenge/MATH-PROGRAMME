from __future__ import annotations

from fractions import Fraction
from math import comb

from sympy import ZZ
from sympy.polys.matrices import DomainMatrix

SIZE = 24
DET_DEGREE_MAX = 144
EXPECTED_RESIDUAL_DEGREE = 94
EXPECTED_FACTORS = (
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


def _a_coefficients(n: int) -> list[int]:
    out = [0] * 6
    for i in range(3):
        left = comb(2, i) * (n + 7) ** (2 - i) * (-1) ** i
        for h in range(4):
            out[i + h] += left * comb(3, h) * (n + 1) ** (3 - h)
    return out


def _b_coefficients(n: int) -> list[int]:
    return [2 * (n + 7), 3 * n + 23, n + 10, 1]


def _coefficient_of_shifted_monomial(power: int, degree: int) -> int:
    if 0 <= degree <= power:
        return comb(power, degree)
    return 0


def _block_rows(n: int) -> list[list[int]]:
    a_coeff = _a_coefficients(n)
    b_coeff = _b_coefficients(n)
    rows = [[0] * SIZE for _ in range(SIZE)]
    for row in range(SIZE):
        for column in range(SIZE):
            first = 0
            for u, value in enumerate(a_coeff):
                first += value * _coefficient_of_shifted_monomial(column, row - u)
            q = row - column - 2
            second = b_coeff[q] if 0 <= q < len(b_coeff) else 0
            rows[row][column] = (n + 7) * (first - second)
    return rows


def _det(n: int) -> int:
    return int(DomainMatrix(_block_rows(n), (SIZE, SIZE), ZZ).det())


def _forward_differences(values: list[int]) -> list[int]:
    row = values[:]
    leading = []
    while row:
        leading.append(row[0])
        row = [row[i + 1] - row[i] for i in range(len(row) - 1)]
    return leading


def _power_coefficients(values: list[int]) -> list[int]:
    deltas = _forward_differences(values)
    polynomial = [Fraction(0)]
    falling = [Fraction(1)]
    factorial = 1
    for k, delta in enumerate(deltas):
        if k:
            factorial *= k
        scale = Fraction(delta, factorial)
        if len(polynomial) < len(falling):
            polynomial.extend([Fraction(0)] * (len(falling) - len(polynomial)))
        for i, value in enumerate(falling):
            polynomial[i] += scale * value
        next_falling = [Fraction(0)] * (len(falling) + 1)
        for i, value in enumerate(falling):
            next_falling[i] -= k * value
            next_falling[i + 1] += value
        falling = next_falling
    while polynomial and polynomial[-1] == 0:
        polynomial.pop()
    if any(value.denominator != 1 for value in polynomial):
        raise AssertionError("independent determinant reconstruction left Q\\Z")
    return [int(value) for value in polynomial]


def _eval(coefficients: list[int], n: int) -> int:
    out = 0
    for coefficient in reversed(coefficients):
        out = out * n + coefficient
    return out


def _divide_by_x_plus_shift(coefficients: list[int], shift: int) -> tuple[list[int], int]:
    if len(coefficients) < 2:
        return [0], coefficients[0] if coefficients else 0
    quotient = [0] * (len(coefficients) - 1)
    quotient[-1] = coefficients[-1]
    for degree in range(len(coefficients) - 2, 0, -1):
        quotient[degree - 1] = coefficients[degree] - shift * quotient[degree]
    remainder = coefficients[0] - shift * quotient[0]
    return quotient, remainder


def _shift_by_positive_integer(coefficients: list[int], shift: int) -> list[int]:
    out = [0] * len(coefficients)
    for degree, coefficient in enumerate(coefficients):
        for j in range(degree + 1):
            out[j] += coefficient * comb(degree, j) * shift ** (degree - j)
    return out


def verify_gauge_domain() -> dict:
    values = [_det(n) for n in range(DET_DEGREE_MAX + 1)]
    determinant = _power_coefficients(values)
    if len(determinant) - 1 != DET_DEGREE_MAX:
        raise AssertionError("independent determinant degree mismatch")
    if _eval(determinant, 145) != _det(145):
        raise AssertionError("independent determinant fresh-point mismatch")

    residual = determinant
    verified_multiplicities = {}
    for shift, multiplicity in EXPECTED_FACTORS:
        for _ in range(multiplicity):
            residual, remainder = _divide_by_x_plus_shift(residual, shift)
            if remainder != 0:
                raise AssertionError(f"missing exact factor (n+{shift})")
        verified_multiplicities[str(shift)] = multiplicity

    if len(residual) - 1 != EXPECTED_RESIDUAL_DEGREE:
        raise AssertionError("independent residual degree mismatch")
    if residual[-1] != 1:
        raise AssertionError("independent residual is not monic")

    shifted = _shift_by_positive_integer(residual, 9)
    if not all(coefficient > 0 for coefficient in shifted):
        raise AssertionError("independent shift-9 positivity replay failed")

    small = [_eval(residual, n) for n in range(1, 9)]
    if any(value == 0 for value in small):
        raise AssertionError("independent residual integer check failed")

    witness = _det(5) % 4194301
    if witness != 2300711:
        raise AssertionError("independent governed witness mismatch")

    return {
        "determinant_degree_bound_replayed": DET_DEGREE_MAX,
        "determinant_degree": len(determinant) - 1,
        "factor_multiplicities_verified": verified_multiplicities,
        "residual_degree": len(residual) - 1,
        "residual_shift9_positive": True,
        "residual_n_1_through_8_nonzero": True,
        "canonical_gauge_nonsingular_for_all_integer_n_gte_1": True,
        "only_nonnegative_integer_singular_fiber": 0,
        "governed_witness_replayed": witness,
        "finite_sampling_used_as_global_proof": False,
        "proof_basis": (
            "degree<=144 determinant reconstruction; exact factor division; "
            "R_94(n+9) coefficient positivity; exact n=1..8 checks"
        ),
        "proof_effect": "NONE",
        "promotion_effect": "NONE",
        "t3_proved": False,
        "global_certificate_constructed": False,
    }
