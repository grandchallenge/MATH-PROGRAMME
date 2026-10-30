"""Independent 097 controls: correlated Gaussians and actual Schwartz tests.

No producer, earlier fixture, or recurrence state is imported. The moment
calculation is compared with the differential equation for a 2x2 determinant.
These finite identities do not test Borel lifting or mixed-corner descent.
"""
from fractions import Fraction as Q
from math import comb, factorial


def moment(a, b, covariance):
    c11, c12, c22 = covariance
    total = Q(0)
    for cross in range(min(a, b) + 1):
        if (a - cross) % 2 or (b - cross) % 2:
            continue
        left, right = (a - cross) // 2, (b - cross) // 2
        total += (Q(factorial(a) * factorial(b),
                    2 ** (left + right) * factorial(left)
                    * factorial(cross) * factorial(right))
                  * c11 ** left * c12 ** cross * c22 ** right)
    return total


def test_coefficient(power, covariance, t, monomial=(0, 0)):
    # Pair u^monomial f_C with exp(-t epsilon^2 |u|^2/2).
    if power < 0 or power % 2:
        return Q(0)
    k = power // 2
    radial = sum((comb(k, a) * moment(monomial[0] + 2 * a,
                                    monomial[1] + 2 * (k - a), covariance)
                  for a in range(k + 1)), Q(0))
    return (-t / 2) ** k * radial / factorial(k)


def physical_ct(coefficients, h, covariance, t, monomial=(0, 0)):
    return sum((c * test_coefficient(h - j, covariance, t, monomial)
                for j, c in enumerate(coefficients)), Q(0))


def determinant_coefficients(covariance, t, count):
    # q(x)=(1+a*x+b*x^2)^(-1/2), from 2*D*q'+D'*q=0.
    c11, c12, c22 = covariance
    a, b = t * (c11 + c22), t * t * (c11 * c22 - c12 * c12)
    out = [Q(1)]
    for n in range(count):
        previous = out[n - 1] if n else Q(0)
        out.append(-(a * (2 * n + 1) * out[n] + 2 * b * n * previous)
                   / (2 * (n + 1)))
    return out


def main():
    covariances = [(Q(2), Q(1), Q(3)), (Q(1), Q(0), Q(4)),
                   (Q(3), Q(-1), Q(2))]
    pairings = derivatives = regulator_derivatives = stages = scales = 0
    for covariance in covariances:
        c11, c12, c22 = covariance
        determinant = c11 * c22 - c12 * c12
        inv11, inv12, inv22 = c22 / determinant, -c12 / determinant, c11 / determinant
        for t in (Q(1, 2), Q(1), Q(3)):
            exact = determinant_coefficients(covariance, t, 8)
            for seed in range(12):
                coefficients = [Q((-1) ** (seed + j) * (seed + 2 * j + 1), j + 1)
                                for j in range(7)]
                for h in range(12):
                    ct = physical_ct(coefficients, h, covariance, t)
                    expected = sum((c * exact[(h - j) // 2]
                                    for j, c in enumerate(coefficients)
                                    if h >= j and (h - j) % 2 == 0), Q(0))
                    assert ct == expected
                    pairings += 1
                    # d_u1(u1*f_C) = (1-u1*(C^-1*u)_1)*f_C.
                    derivative_ct = (physical_ct(coefficients, h + 1, covariance, t)
                                     - inv11 * physical_ct(coefficients, h + 1, covariance, t, (2, 0))
                                     - inv12 * physical_ct(coefficients, h + 1, covariance, t, (1, 1)))
                    assert derivative_ct == t * physical_ct(coefficients, h - 1, covariance, t, (2, 0))
                    derivatives += 1
                    # Fixed-y regulator derivative has all dimension/Euler terms.
                    scalar_part = [c * (j - 2 - h) for j, c in enumerate(coefficients)]
                    regulator_ct = (physical_ct(scalar_part, h + 1, covariance, t)
                                    + inv11 * physical_ct(coefficients, h + 1, covariance, t, (2, 0))
                                    + 2 * inv12 * physical_ct(coefficients, h + 1, covariance, t, (1, 1))
                                    + inv22 * physical_ct(coefficients, h + 1, covariance, t, (0, 2)))
                    assert regulator_ct == physical_ct(coefficients, h + 1, covariance, t)
                    regulator_derivatives += 1
                    assert physical_ct([Q(0)] + coefficients, h + 1, covariance, t) == ct
                    stages += 1
                    s = Q(3, 2)
                    scaled_covariance = tuple(s * s * x for x in covariance)
                    scaled_coefficients = [c * s ** (j - h) for j, c in enumerate(coefficients)]
                    assert physical_ct(scaled_coefficients, h, scaled_covariance, t) == ct
                    scales += 1
    jet_products = 0
    for seed in range(12):
        g = [Q((-1) ** j * (seed + j + 1), j + 1) for j in range(10)]
        phi = [Q(seed + 2 * j + 3, j + 2) for j in range(10)]
        for order in range(9):
            direct = (-1) ** order * factorial(order) * sum(
                (g[j] * phi[order - j] for j in range(order + 1)), Q(0))
            inserted = sum(((-1) ** j * comb(order, j) * factorial(j) * g[j]
                            * (-1) ** (order - j) * factorial(order - j) * phi[order - j]
                            for j in range(order + 1)), Q(0))
            assert direct == inserted
            jet_products += 1
    print(f"PASS097 correlated-Gaussian Schwartz-test CT vs determinant: {pairings}")
    print(f"PASS097 physical derivative/pole-shift with nonzero mixed controls: {derivatives}")
    print(f"PASS097 fixed-y regulator derivative including Euler terms: {regulator_derivatives}")
    print(f"PASS097 actual representative changes: {stages}")
    print(f"PASS097 semilinear regulator scaling/finite invariance: {scales}")
    print(f"PASS097 signed normal-jet complement product: {jet_products}")
    print("LIMIT097 finite coefficient algebra; no Borel, liquid or mixed-corner proof")


if __name__ == "__main__":
    main()
