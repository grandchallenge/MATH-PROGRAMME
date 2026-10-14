"""Exact source-bound regression fixtures for Erdős #479.

These tests establish finite congruences and the known power-of-two-family
construction; they do NOT establish the universal all-integer-k conjecture.
"""

from math import gcd, isqrt, lcm


def prime(n: int) -> bool:
    return n >= 2 and all(n % d for d in range(2, isqrt(n) + 1))


def odd_prime_powers(n: int) -> list[int]:
    """Return odd prime-power factors of n, with independent trial division."""
    result = []
    t = n
    for q in range(2, isqrt(t) + 2):
        if t % q:
            continue
        power = 1
        while t % q == 0:
            t //= q
            power *= q
        if q > 2:
            result.append(power)
    if t > 1 and t % 2:
        result.append(t)
    return result


def multiplicative_order_of_two(modulus: int) -> int:
    assert modulus > 1 and modulus % 2
    r = 2 % modulus
    d = 1
    while r != 1:
        r = (r * 2) % modulus
        d += 1
        assert d <= modulus
    return d


def tang_modulus(i: int) -> int:
    assert i >= 1
    m = 1
    for prime_power in odd_prime_powers(i):
        d = multiplicative_order_of_two(prime_power)
        m = lcm(m, d // gcd(d, i))
    return m


def test_479_historical_small_family_exact() -> None:
    # For each fixed i, pick several primes p ≡ 1 mod L_i, p∤2i.
    for i in (1, 2, 3, 5, 6, 10, 12, 15, 20, 21):
        L = tang_modulus(i)
        ps = [p for p in range(3, 400)
              if prime(p) and i % p and (p - 1) % L == 0]
        assert len(ps) >= 2, (i, L)
        for p in ps[:7]:
            n = i * p
            assert pow(2, n, n) == pow(2, i, n), (i, p, L)
            assert n > i
    # In particular, Tang's illustrative i=3, p=5 gives n=15.
    assert pow(2, 15, 15) == 8


def test_479_k1_exception_and_zero_negative_families() -> None:
    assert all(pow(2, n, n) != 1 % n for n in range(2, 2500))
    for j in range(1, 12):
        n = 2**j
        assert pow(2, n, n) == 0  # k=0
    for j in range(1, 10):
        n = 3**j
        assert pow(2, n, n) == (-1) % n


def test_479_historical_huge_k3_exact_identity_not_minimality() -> None:
    n = 4_700_063_497
    assert 19 * 47 * 5_263_229 == n
    assert pow(2, n, n) == 3
    assert all(pow(2, t, t) != 3 % t for t in range(4, 1000))
    # No assertion here that all 4.7 billion earlier values were examined.


def test_479_prime_extension_lemma_finite_certificates() -> None:
    for k, n, p in [(-5, 7, 19), (7, 25, 1_342_177)]:
        assert prime(p) and n % p
        assert pow(2, n, n) == k % n
        assert pow(2, n, p) == k % p
        assert pow(k, p, n) == k % n
        assert pow(2, n * p, n * p) == k % (n * p)
