"""Finite #462 source-interpretation and algebra checks; no uniform theorem."""
from fractions import Fraction
from math import isqrt, log, sqrt
import unittest


def least_prime_factor(n: int) -> int:
    assert n >= 2
    for p in range(2, isqrt(n) + 1):
        if n % p == 0:
            return p
    return n


def omega_with_multiplicity(n: int) -> int:
    assert n >= 2
    count = 0
    while n > 1:
        p = least_prime_factor(n)
        n //= p
        count += 1
    return count


def is_prime(n: int) -> bool:
    return n >= 2 and least_prime_factor(n) == n


class Erdos462FiniteTests(unittest.TestCase):
    def test_prime_terms_change_literal_sum(self):
        for p in (2, 3, 5, 11, 101, 1009):
            self.assertTrue(is_prime(p))
            self.assertEqual(Fraction(least_prime_factor(p), p), 1)

    def test_semiprime_exact_weight(self):
        for n in range(4, 6000):
            if omega_with_multiplicity(n) != 2:
                continue
            p = least_prime_factor(n)
            q = n // p
            self.assertTrue(is_prime(q))
            self.assertLessEqual(p, q)
            self.assertEqual(Fraction(p, n), Fraction(1, q))

    def test_three_factor_remainder(self):
        for n in range(8, 6000):
            if omega_with_multiplicity(n) >= 3:
                self.assertLessEqual(least_prime_factor(n) ** 3, n)

    def test_mean_paper_algebra_obstruction(self):
        # The displayed paper bound L^2/X^2 * X/(log X)^2 is C^2 log^2 X,
        # NOT C^2 log^2 X / X. It does not tend to zero.
        for X in (10**4, 10**6, 10**8):
            C = 1.25
            L = C * sqrt(X) * log(X)**2
            displayed = (L**2 / X**2) * (X / log(X)**2)
            self.assertAlmostEqual(displayed, C**2 * log(X)**2, places=8)
            self.assertGreater(displayed, 100)

    def test_exact_small_interval_composite_weight(self):
        # The semiprime-only contribution is a rigorous lower bound on
        # the composite-only contribution, which in turn is bounded by
        # the literal sum including prime terms.
        for x, width in ((20, 15), (100, 35), (1000, 150)):
            semiprime = sum((Fraction(least_prime_factor(n), n)
                             for n in range(x, x + width + 1)
                             if n >= 4 and omega_with_multiplicity(n) == 2), Fraction())
            composite = sum((Fraction(least_prime_factor(n), n)
                             for n in range(x, x + width + 1)
                             if n >= 4 and not is_prime(n)), Fraction())
            literal = sum((Fraction(least_prime_factor(n), n)
                           for n in range(x, x + width + 1)
                           if n >= 2), Fraction())
            self.assertLessEqual(semiprime, composite)
            self.assertLessEqual(composite, literal)
            self.assertGreater(literal, composite)
