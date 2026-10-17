"""Finite exact arithmetic regressions for Erdős #457.

These tests do not prove infinitude or certify Lean.
"""
import math
import unittest

def primes_upto(bound):
    return [p for p in range(2, bound + 1)
            if all(p % d for d in range(2, math.isqrt(p) + 1))]

def q(n, k, primes):
    for p in primes:
        if all((n + i) % p for i in range(1, k + 1)):
            return p
    raise AssertionError("Prime search bound too small")

class Erdos457ArithmeticTests(unittest.TestCase):
    def test_explicit_witnesses(self):
        ps = primes_upto(200)
        for n, k, expected in [(32, 3, 13), (113729, 11, 59)]:
            with self.subTest(n=n):
                self.assertEqual(k, math.floor(math.log(n)))
                self.assertEqual(expected, q(n, k, ps))
                self.assertGreater(expected, 2.1 * math.log(n))

    def test_exact_residue_criterion(self):
        ps = primes_upto(97)
        for n in range(3, 1000):
            k = math.floor(math.log(n))
            for p in ps:
                actual = any((n + i) % p == 0 for i in range(1, k + 1))
                predicted = p <= k or (p > k and p - k <= n % p < p)
                self.assertEqual(actual, predicted, (n, k, p))

    def test_binomial_prime_intervals(self):
        for m in (10, 25, 50, 100):
            a = math.comb(2 * m, m)
            b = math.comb(3 * m, m)
            for p in primes_upto(3 * m):
                if m < p <= 2 * m:
                    self.assertEqual(a % p, 0, (m, p))
                if 2 * m < p <= 3 * m:
                    self.assertEqual(b % p, 0, (m, p))

    def test_prime_count_bound(self):
        for m in (10, 25, 50, 100):
            count = sum(2 * m < p <= 3 * m for p in primes_upto(3 * m))
            self.assertLessEqual(count * math.log(2 * m), 3 * m * math.log(2))

