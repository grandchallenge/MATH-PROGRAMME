"""Reproducible finite examples and mathematical exception fixtures for EC-BULK-004.

These are sanity checks, not proofs of asymptotic density or analytic theorems.
"""
from fractions import Fraction


def divisors(n: int) -> list[int]:
    return [d for d in range(1, n + 1) if n % d == 0]


def occupied_dyadic_bins(n: int) -> int:
    return len({d.bit_length() - 1 for d in divisors(n)})


def close_divisor_pairs(n: int) -> int:
    ds = divisors(n)
    return sum(a < b < 2 * a for a in ds for b in ds)


def primes_in_open_interval(lo: int, hi: int) -> list[int]:
    return [
        p for p in range(lo + 1, hi)
        if p >= 2 and all(p % d for d in range(2, int(p**0.5) + 1))
    ]


def acceptable_451(k: int, n: int) -> bool:
    assert n > 2 * k
    return all(
        all((n - i) % p for i in range(1, k + 1))
        for p in primes_in_open_interval(k, 2 * k)
    )


def test_448_examples() -> None:
    assert divisors(12) == [1, 2, 3, 4, 6, 12]
    assert occupied_dyadic_bins(12) == 4
    assert divisors(6) == [1, 2, 3, 6]
    assert occupied_dyadic_bins(6) == 3


def test_449_secondary_claim_counterexample() -> None:
    tau, tau_plus, r = len(divisors(6)), occupied_dyadic_bins(6), close_divisor_pairs(6)
    assert (tau, tau_plus, r) == (4, 3, 1)
    assert r + tau < Fraction(tau * tau, tau_plus)  # Online displayed inequality is false.
    for n in range(1, 1001):
        tau, tau_plus, r = len(divisors(n)), occupied_dyadic_bins(n), close_divisor_pairs(n)
        assert 2 * r + tau >= Fraction(tau * tau, tau_plus)  # Correct general inequality.


def test_450_exact_periodicity() -> None:
    # At n=3, the admissible divisors in (n,2n) are 4 and 5.
    count = lambda m: m % 4 == 0 or m % 5 == 0
    assert sum(count(m) for m in range(20)) == 8
    assert sum(count(m) for m in range(1, 20)) == 7
    assert all(count(m) == count(m + 20) for m in range(100))


def test_451_small_cases_and_product_upper_construction() -> None:
    for k, answer in [(2, 6), (3, 9), (4, 20), (5, 13)]:
        assert acceptable_451(k, answer)
        assert all(not acceptable_451(k, n) for n in range(2 * k + 1, answer))
    for k in range(2, 31):
        primes = primes_in_open_interval(k, 2 * k)
        m = 1
        for p in primes:
            m *= p
        n = m * (2 * k // m + 1)
        assert acceptable_451(k, n)


def test_453_pomerance_strict_prime_product_examples() -> None:
    # Paper p. 400: a GOOD index satisfies the strict > inequality for ALL 1 <= i < n.
    primes = primes_in_open_interval(1, 1000)
    assert primes[:10] == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

    def strict_good(n: int) -> bool:
        return all(primes[n - 1] ** 2 > primes[n - i - 1] * primes[n + i - 1]
                   for i in range(1, n))

    assert [n for n in range(2, 21) if strict_good(n)] == [3, 5, 7, 10, 12, 13, 16, 17, 19, 20]
    assert strict_good(3) and strict_good(5)
    assert not strict_good(2) and not strict_good(4)
    assert [primes[4 - i] * primes[4 + i] for i in range(1, 5)] == [91, 85, 57, 46]
    # Incorrect reversal at n=3 is explicitly falsified.
    assert all(not (primes[2] ** 2 < primes[2 - i] * primes[2 + i]) for i in (1, 2))


def test_453_sublinear_midpoint_identity() -> None:
    # The elementary model a_n = log(n+1) has exact strict midpoint inequality:
    # (n+1)^2 - (n-i+1)(n+i+1) = i^2 > 0.
    # This does NOT establish the infinite-vertex theorem for arbitrary sublinear sequences.
    for n in range(2, 100):
        for i in range(1, n):
            assert (n + 1) ** 2 - (n - i + 1) * (n + i + 1) == i * i



def test_452_explicit_crt_three_integer_block() -> None:
    # These finite congruences are a reproducible CRT fixture, not an asymptotic proof.
    from math import log, prod

    groups = ((5, 7, 11, 13), (17, 19, 23, 29), (31, 37, 41, 43))
    moduli = [prod(group) for group in groups]
    assert moduli == [5005, 215441, 2022161]
    assert prod(moduli) == 2180460221945005
    a = 2099999228442114
    for j, group in enumerate(groups, 1):
        assert (a + j) % moduli[j - 1] == 0
        for p in group:
            assert all(p % d != 0 for d in range(2, int(p**0.5) + 1))
            assert (a + j) % p == 0
        assert 4 > log(log(a + j))


def test_454_prime_graph_additive_gap() -> None:
    # The signed gap can be negative; do NOT use truncated natural subtraction.
    primes = primes_in_open_interval(1, 1000)
    def difference(n: int) -> int:
        return min(primes[n - i - 1] + primes[n + i - 1] - 2 * primes[n - 1]
                   for i in range(1, n))
    assert {n: difference(n) for n in (2, 3, 4, 5)} == {2: 1, 3: 0, 4: 2, 5: -2}
    # For n>=3, all offsets except i=n-1 have odd primes on both sides.
    for n in range(3, 20):
        for i in range(1, n - 1):
            d = primes[n - i - 1] + primes[n + i - 1] - 2 * primes[n - 1]
            assert d % 2 == 0
            if d > 0:
                assert d >= 2



def test_456_totient_and_least_prime_examples() -> None:
    # Direct exact finite fixtures; no inference about density-one conjectures.
    from math import gcd

    def prime(k: int) -> bool:
        return k >= 2 and all(k % d != 0 for d in range(2, int(k**0.5) + 1))

    def phi(k: int) -> int:
        return sum(1 for t in range(1, k + 1) if gcd(t, k) == 1)

    for n, expected_p, expected_m in (
        (2, 3, 3), (3, 7, 7), (4, 5, 5),
        (8, 17, 15), (16, 17, 17), (32, 97, 51),
    ):
        p = next(q for q in range(n + 1, 2000, n) if prime(q))
        m = next(q for q in range(1, p + 1) if phi(q) % n == 0)
        assert (p, m) == (expected_p, expected_m)
        assert n + 1 <= m <= p
    # For odd exponents >=3, n+1 is composite, phi(2n)=n,
    # and the first prime congruent to 1 mod n must be >=2n+1.
    for k in range(1, 6):
        n = 2 ** (2 * k + 1)
        assert (n + 1) % 3 == 0 and n + 1 > 3
        assert phi(2 * n) == n
