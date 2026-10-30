"""Exact finite controls for 096; no producer or earlier fixture imports."""
from fractions import Fraction as Q
from math import factorial

def moment(n):
    if n % 2:
        return Q(0)
    out = 1
    for k in range(1, n, 2):
        out *= k
    return Q(out)

def add_term(out, index, coefficient):
    out[index] = out.get(index, Q(0)) + coefficient
    if not out[index]:
        del out[index]

def physical_ct(data, h, lam):
    # Independent moment/test Taylor pairing of normalized Gaussian profiles.
    return sum((c * moment(r + h - j) * lam ** (h - j)
                / factorial(h - j)
                for (j, r), c in data.items() if j <= h), Q(0))

def gaussian_derivative_polynomial(order):
    # d^r/dt^r exp(t^2/2) = polynomial(t) exp(t^2/2).
    poly = {0: Q(1)}
    for _ in range(order):
        nxt = {}
        for k, c in poly.items():
            if k:
                add_term(nxt, k - 1, k * c)
            add_term(nxt, k + 1, c)
        poly = nxt
    return poly

def exact_integral_coefficient(data, h, lam):
    # Coefficient of epsilon^h in the exact Gaussian exponential-test integral.
    total = Q(0)
    for (j, r), c in data.items():
        for k, a in gaussian_derivative_polynomial(r).items():
            rest = h - j - k
            if rest >= 0 and rest % 2 == 0:
                n = rest // 2
                total += c * a * lam ** k * (lam ** 2 / 2) ** n / factorial(n)
    return total

def physical_derivative(data):
    out = {}
    for (j, r), c in data.items():
        if r:
            add_term(out, (j, r - 1), r * c)
        add_term(out, (j, r + 1), -c)
    return out

def shifted(data):
    return {(j + 1, r): c for (j, r), c in data.items()}

def multiply_cutoff_jet(data, cutoff):
    out = {}
    for (j, r), c in data.items():
        for b, k in cutoff.items():
            add_term(out, (j + b, r + b), c * k)
    return out

def physical_ct_with_cutoff(data, h, lam, cutoff):
    total = Q(0)
    for (j, r), c in data.items():
        for b, k in cutoff.items():
            a = h - j - b
            if a >= 0:
                total += c * k * moment(r + a + b) * lam ** a / factorial(a)
    return total

def main():
    pairings = derivatives = stage_changes = cutoffs = 0
    scales = [Q(0), Q(1), Q(-2), Q(3, 2)]
    # Mixed regulator jets are material here: j is not fixed at zero.
    for seed in range(12):
        data = {(j, (3 * j + seed) % 9): Q((-1) ** (seed + j) * (j + 1), seed + 1)
                for j in range(9)}
        cutoff = {0: Q(2), 1: Q(-1), 3: Q(1, 6)}
        for h in range(9):
            for lam in scales:
                value = physical_ct(data, h, lam)
                assert value == exact_integral_coefficient(data, h, lam)
                pairings += 1
                assert physical_ct(physical_derivative(data), h + 1, lam) == -lam * value
                derivatives += 1
                assert physical_ct(shifted(data), h + 1, lam) == value
                stage_changes += 1
                assert physical_ct(multiply_cutoff_jet(data, cutoff), h, lam) == (
                    physical_ct_with_cutoff(data, h, lam, cutoff))
                cutoffs += 1
    assert physical_ct({(0, 0): Q(1), (1, 0): Q(1)}, 1, Q(0)) == 1
    assert physical_ct({(0, 0): Q(1)}, 1, Q(0)) == 0
    assert physical_ct({(0, 0): Q(1)}, 2, Q(2)) == 2
    print(f"PASS096 mixed regulator-jet CT vs exact Gaussian integral: {pairings}")
    print(f"PASS096 physical derivative with pole-order shift: {derivatives}")
    print(f"PASS096 representative stage changes: {stage_changes}")
    print(f"PASS096 physical cutoff-jet multiplication: {cutoffs}")
    print("PASS096 leading-profile finite-contact loss and nonzero even-rank control")
    print("LIMIT096 finite coefficient algebra; no Borel, liquid or mixed-corner proof")

if __name__ == "__main__":
    main()

