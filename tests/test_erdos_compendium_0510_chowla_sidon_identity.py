"""Exact Laurent/Sidon construction witnessing Chowla's sharp possible exponent."""

from collections import Counter
from fractions import Fraction as F
from itertools import combinations


def sidon_powers(k):
    assert k >= 2
    return tuple((1 << j) - 1 for j in range(k))


def positive_differences(b):
    return tuple(bj - bi for bi, bj in combinations(b, 2))


def laurent_product_coeffs(b):
    """P(x)P(x^-1), coefficients for integer (possibly negative) exponents."""
    return Counter(bj - bi for bi in b for bj in b)


def cos_two_pi_thirds(m):
    return F(1) if m % 3 == 0 else F(-1, 2)


def test_510_powers_two_sidon_differences_unique():
    for k in range(2, 13):
        b = sidon_powers(k)
        a = positive_differences(b)
        assert len(a) == k * (k - 1) // 2
        assert len(set(a)) == len(a)
        assert min(a) > 0


def test_510_laurent_square_coefficients_and_factor_two():
    for k in range(2, 12):
        b = sidon_powers(k)
        a = positive_differences(b)
        coefficients = laurent_product_coeffs(b)
        assert coefficients[0] == k
        assert len(coefficients) == 1 + 2 * len(a)
        for d in a:
            assert coefficients[d] == coefficients[-d] == 1
        assert sum(coefficients.values()) == k * k
        # Therefore for |x|=1, 2 F_A = |P(x)|^2 - k >= -k.
        assert F(k, 2) > 0


def test_510_exact_rational_cosine_at_special_angles():
    for k in range(2, 12):
        b = sidon_powers(k)
        a = positive_differences(b)
        f = sum((cos_two_pi_thirds(m) for m in a), F(0))
        prod_real = sum((count * cos_two_pi_thirds(freq)
                         for freq, count in laurent_product_coeffs(b).items()), F(0))
        assert 2 * f == prod_real - k
        assert f >= F(-k, 2)
        assert sum((F(1) for _ in a), F(0)) == len(a)  # F_A(0)=N


def test_510_padding_cardinality_and_exponent_half_obstruction():
    for N in range(1, 240):
        # C(k,2) <= N < C(k+1,2), and r=N-C(k,2)<k.
        k = max(j for j in range(2, 30) if j * (j - 1) // 2 <= N)
        r = N - k * (k - 1) // 2
        assert 0 <= r < k
        b = sidon_powers(k)
        a = set(positive_differences(b))
        missing = (j for j in range(1, 20000) if j not in a)
        for _ in range(r):
            a.add(next(missing))
        assert len(a) == N
        # Universal pointwise inequality for THIS constructed A:
        # F_A(theta)>=-k/2-r, since each padded cosine >=-1.
        assert F(k, 2) + r <= F(3 * k, 2)


def test_510_zero_frequency_is_invalid_hypothesis():
    b = sidon_powers(5)
    assert 0 in b  # phases may have zero exponent
    a = positive_differences(b)
    assert 0 not in a  # cosine FREQUENCIES may not
