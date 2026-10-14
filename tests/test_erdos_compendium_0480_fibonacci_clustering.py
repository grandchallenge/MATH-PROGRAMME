"""Source-bound finite checks for Erdős #480 and Chung–Graham's constant.

The paper's infinite-sequence inequality and Fibonacci-digit sharpness theorem
are NOT established by these finite checks or an unproved Lean declaration.
"""

from decimal import Decimal, localcontext
from fractions import Fraction


def fibonacci(n: int) -> int:
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def partial_denominator(k: int) -> Fraction:
    return Fraction(1) + sum(
        (Fraction(1, fibonacci(2 * j)) for j in range(1, k + 1)),
        Fraction(0),
    )


def test_480_fibonacci_even_terms_and_constant_direction() -> None:
    assert [fibonacci(2 * i) for i in range(1, 9)] == [
        1, 3, 8, 21, 55, 144, 377, 987,
    ]
    assert partial_denominator(1) == Fraction(2)
    assert partial_denominator(2) == Fraction(7, 3)
    assert partial_denominator(3) == Fraction(59, 24)
    # 7/3 > sqrt(5) because both terms positive and 49/9 > 5.
    assert partial_denominator(2) ** 2 > 5
    assert all(partial_denominator(k) < partial_denominator(k + 1)
               for k in range(1, 12))


def test_480_sharp_constant_certified_by_rational_tail_bounds() -> None:
    # Fibonacci even terms grow by a factor >2 at each step. Thus
    # sum_{j>k} 1/F_{2j} < 1/F_{2k}.
    c = partial_denominator(12)
    alpha_lower = 1 / (c + Fraction(1, fibonacci(24)))
    alpha_upper = 1 / c
    with localcontext() as context:
        context.prec = 40
        decimal_lower = Decimal(alpha_lower.numerator) / Decimal(alpha_lower.denominator)
        decimal_upper = Decimal(alpha_upper.numerator) / Decimal(alpha_upper.denominator)
        published_alpha = Decimal("0.39441967")
        assert decimal_lower < published_alpha < decimal_upper
        assert decimal_upper < Decimal(1) / Decimal(5).sqrt()


def test_480_periodic_examples_have_zero_clustering_at_positive_shift() -> None:
    for q in (2, 3, 5, 7):
        x = [Fraction(m % q, q - 1) for m in range(12 * q)]
        assert all(x[m + q] == x[m] for m in range(11 * q))
        assert all(q * abs(x[m + q] - x[m]) == 0 for m in range(11 * q))
    # This verifies examples, not a universal bound.


def test_480_golden_rotation_not_the_published_extremizer() -> None:
    with localcontext() as context:
        context.prec = 40
        tau = (Decimal(5).sqrt() - 1) / 2
        smaller_adjacent_rotation_step = 1 - tau
        assert abs(smaller_adjacent_rotation_step - Decimal("0.38196601125010515")) < Decimal("1e-15")
        # Any C(x) is <= the n=1 liminf. The historical 1980 p.107
        # golden-rotation parenthetical therefore cannot certify α-sharpness.
        alpha_lower_rational = 1 / (
            partial_denominator(12) + Fraction(1, fibonacci(24))
        )
        alpha_lower = (
            Decimal(alpha_lower_rational.numerator)
            / Decimal(alpha_lower_rational.denominator)
        )
        assert smaller_adjacent_rotation_step < alpha_lower


def test_480_zero_shift_is_not_allowed() -> None:
    # A repaired formal statement has n : ℕ+; n=0 would produce
    # 0 * abs(x_m - x_m)=0 for every sequence and every m.
    assert 0 * abs(Fraction(4, 5) - Fraction(4, 5)) == 0
    assert min((q for q in (1, 2, 3, 4) if q > 0)) == 1
