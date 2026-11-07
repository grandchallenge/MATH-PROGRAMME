"""Finite exact regressions for Erdős #458; not a proof of the universal claim."""
import bisect
import math
import unittest


def primes_upto(bound):
    sieve = [True] * (bound + 1)
    sieve[0] = sieve[1] = False
    for p in range(2, math.isqrt(bound) + 1):
        if sieve[p]:
            for j in range(p * p, bound + 1, p):
                sieve[j] = False
    return [p for p in range(2, bound + 1) if sieve[p]]


def prime_powers(primes, bound):
    out = []
    for p in primes:
        v = p * p
        while v <= bound:
            out.append((v, p))
            v *= p
    return sorted(out)


class Erdos458FiniteTests(unittest.TestCase):
    def test_prime_power_product_criterion_to_100000(self):
        ps = primes_upto(100000)
        powers = prime_powers(ps, 100000)
        multi = []
        for p, r in zip(ps, ps[1:]):
            lo = bisect.bisect_right(powers, (p, 100001))
            hi = bisect.bisect_left(powers, (r, 0))
            in_gap = powers[lo:hi]
            bases = [q for _, q in in_gap]
            self.assertEqual(len(bases), len(set(bases)))
            self.assertLess(math.prod(bases), p, (p, r, in_gap))
            if len(in_gap) > 1:
                multi.append((p, r, math.prod(bases)))
        self.assertEqual(multi, [(7, 11, 6), (23, 29, 15), (113, 127, 55),
                                 (2179, 2203, 39), (32749, 32771, 362)])

    def test_direct_lcm_crosscheck_to_1000(self):
        ps = primes_upto(1000)
        lcm = 1
        values = {}
        for n in range(1, 1001):
            lcm = math.lcm(lcm, n)
            values[n] = lcm
        for p, r in zip(ps, ps[1:]):
            self.assertLess(values[r - 1], p * values[p])

    def test_first_gap_product(self):
        self.assertEqual(math.lcm(*range(1, 11)) // math.lcm(*range(1, 8)), 6)
        self.assertLess(6, 7)
