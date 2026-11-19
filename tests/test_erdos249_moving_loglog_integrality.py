"""Adversarial finite checks for WP07-A, not a numerical asymptotic proof."""
import math
import unittest
from fractions import Fraction

from experiments.erdos249_full_series_phase.moving_loglog_integrality import (
    distinct_prime_factor_sieve, finite_explicit_bad_count_bound,
    finite_markov_envelope, finite_tail_numerator, first_omitted_term,
    termwise_bad_positions, totient_independent, totient_sieve, v2,
    verify_totient_square_bound,
)


class MovingLoglogIntegralityTests(unittest.TestCase):
    def test_sieve_totient_against_independent_coprime_count(self):
        values = totient_sieve(360)
        self.assertEqual(values[1], 1)
        for n in range(1, 361):
            self.assertEqual(values[n], totient_independent(n))

    def test_distinct_prime_factors_against_trial_division(self):
        values = distinct_prime_factor_sieve(800)
        for n in range(1, 801):
            r, count = n, 0
            for p in range(2, math.isqrt(n) + 1):
                if r % p == 0:
                    count += 1
                    while r % p == 0:
                        r //= p
            if r > 1:
                count += 1
            self.assertEqual(values[n], count)

    def test_val2_phi_at_least_omega_minus_one(self):
        phis = totient_sieve(20000)
        omega = distinct_prime_factor_sieve(20000)
        for n in range(1, 20001):
            self.assertGreaterEqual(v2(phis[n]), omega[n] - 1)

    def test_termwise_integrality_entails_finite_sum_integrality(self):
        X, L = 64, 7
        phis = totient_sieve(2 * X + L)
        bad = set(termwise_bad_positions(X, L, phis))
        for N in range(X, 2 * X):
            q = finite_tail_numerator(N, L, phis)
            if N not in bad:
                self.assertEqual(q % (1 << L), 0)

    def test_converse_is_false_due_to_finite_cancellation(self):
        phis = totient_sieve(8)
        # N=1, L=2: phi(2)/2 + phi(3)/4 = 1/2 + 1/2 = 1.
        self.assertEqual(phis[2], 1)
        self.assertEqual(phis[3], 2)
        self.assertEqual(finite_tail_numerator(1, 2, phis), 4)
        self.assertNotEqual(phis[2] % 2, 0)
        self.assertEqual(finite_tail_numerator(1, 2, phis) % 4, 0)

    def test_exact_finite_omega_markov_bound(self):
        for X, L in ((16, 2), (32, 3), (64, 4), (100, 5)):
            bad_count = len(termwise_bad_positions(X, L))
            for z in (Fraction(1, 2), Fraction(1, 3), Fraction(3, 4)):
                upper = finite_markov_envelope(X, L, z)
                self.assertLessEqual(bad_count, upper)

    def test_source_receipt_finite_not_asymptotic(self):
        receipt = finite_explicit_bad_count_bound(512, 5)
        self.assertEqual(receipt["X"], 512)
        self.assertEqual(receipt["L"], 5)
        self.assertLessEqual(receipt["nonintegral_sum_count"],
                             receipt["bad_count"])
        self.assertEqual(
            receipt["boundary"],
            "FINITE_CHECK_ONLY__SELBERG_DELANGE_EXTERNAL__FULL_S_OPEN"
        )
        self.assertLessEqual(
            receipt["bad_count"] * int(receipt["markov_bound_denominator"]),
            int(receipt["markov_bound_numerator"]),
        )

    def test_totient_square_lower_bound(self):
        self.assertTrue(verify_totient_square_bound(10000))

    def test_first_omitted_term_dominates_square_root_lower_bound(self):
        phis = totient_sieve(1000)
        for N in (3, 50, 300):
            for L in (1, 4, 10):
                n = N + L + 1
                first = first_omitted_term(N, L, phis)
                self.assertEqual(first, Fraction(phis[n], 1 << (L + 1)))
                self.assertGreaterEqual(
                    2 * (first * (1 << (L + 1)))**2, n,
                )
                several = sum((Fraction(phis[N + j], 1 << j)
                               for j in range(L + 1, L + 8)), Fraction())
                self.assertGreaterEqual(several, first)

    def test_rational_positive_comparator_cannot_be_ignored(self):
        # GCL's earlier bounded positive even comparator:
        # sum_{n>=1} 2*floor(n/2)/2^n = 4/3.
        x = Fraction(1, 2)
        closed = 2 * x * x * (1 + x) / (1 - x * x)**2
        self.assertEqual(closed, Fraction(4, 3))
        for n in range(1, 500):
            self.assertLessEqual(2 * (n // 2), n)

    def test_invalid_finite_contracts_rejected(self):
        with self.assertRaises(ValueError):
            totient_sieve(0)
        with self.assertRaises(ValueError):
            distinct_prime_factor_sieve(0)
        with self.assertRaises(ValueError):
            v2(0)
        with self.assertRaises(ValueError):
            termwise_bad_positions(8, 9)
        with self.assertRaises(ValueError):
            finite_markov_envelope(32, 3, Fraction(1))
        with self.assertRaises(ValueError):
            first_omitted_term(0, 2)
        with self.assertRaises(ValueError):
            finite_tail_numerator(50, 2, totient_sieve(40))


if __name__ == "__main__":
    unittest.main()
