"""Independent hostile tests for WP04; no S-irrationality assertion."""
import math
import unittest
from fractions import Fraction

from experiments.erdos249_full_series_phase.mobius_prime_denominators import (
    absolute_tail_upper,
    first_squarefree_after,
    mobius_one,
    mobius_values,
    prime_window_forced_factor,
    primes_in_terminal_half,
    reduced_denominator_receipt,
    sign_of_exact_tail,
    strict_gap_lower,
    truncation,
    weight,
)


class MobiusPrimeDenominatorsTests(unittest.TestCase):
    def test_sieve_vs_independent_trial_division(self):
        observed = mobius_values(180)
        self.assertEqual(observed[0], 0)
        self.assertEqual(observed[1], 1)
        self.assertEqual(observed[1:], [mobius_one(i) for i in range(1, 181)])
        self.assertEqual(first_squarefree_after(8), 10)
        self.assertEqual(first_squarefree_after(15), 17)

    def test_weight_is_exact_geometric_derivative(self):
        for n in range(1, 18):
            x = Fraction(1, 1 << n)
            self.assertEqual(weight(n), x / (1 - x) ** 2)
            self.assertGreater(weight(n), Fraction(0))

    def test_first_tail_term_strictly_dominates_every_later_weight(self):
        # Finite partial sum + an independently proved uniform upper bound:
        # sum_{d>H} weight(d) < absolute_tail_upper(H).
        for m in range(1, 22):
            H = max(64, m + 30)
            partial = sum((weight(d) for d in range(m + 1, H + 1)), Fraction())
            self.assertGreater(weight(m) - partial - absolute_tail_upper(H),
                               strict_gap_lower(m))

    def test_signed_mobius_tail_using_certified_truncation_error(self):
        H = 110
        full_approx = truncation(H)
        uncertainty = absolute_tail_upper(H)
        for D in range(1, 40):
            sign = sign_of_exact_tail(D)
            m = first_squarefree_after(D)
            signed_approx = sign * (full_approx - truncation(D))
            self.assertGreater(signed_approx - uncertainty, strict_gap_lower(m))
            self.assertLess(abs(full_approx - truncation(D)) + uncertainty,
                            absolute_tail_upper(D))

    def test_prime_window_denominator_divisibility(self):
        for D in range(2, 47):
            q = truncation(D).denominator
            factor = prime_window_forced_factor(D)
            self.assertEqual(q % factor, 0)
            for p in primes_in_terminal_half(D):
                self.assertEqual(q % ((1 << p) - 1) ** 2, 0)

    def test_prime_omission_removes_every_prime_window_factor(self):
        # Opposing the theorem: remove the isolated term mu(p)*a_p.
        # No other denominator in the truncated sum shares a prime with 2^p-1.
        for D in [5, 8, 13, 20, 31]:
            mu = mobius_values(D)
            for p in primes_in_terminal_half(D):
                self.assertEqual(mu[p], -1)
                other = truncation(D) - mu[p] * weight(p)
                self.assertEqual(math.gcd(other.denominator, (1 << p) - 1), 1)

    def test_strict_lower_and_upper_intervals(self):
        for D in range(1, 40):
            m = first_squarefree_after(D)
            self.assertLess(strict_gap_lower(m), absolute_tail_upper(D))
        self.assertEqual(prime_window_forced_factor(5), 7**2 * 31**2)

    def test_rational_comparator_exposes_unsupported_inference(self):
        # A superincreasing nonnegative rational-weight expansion can be rational:
        # sum_n (2^-n + 4^-n) = 1 + 1/3.
        self.assertEqual(Fraction(1) + Fraction(1, 3), Fraction(4, 3))
        for n in range(1, 12):
            w = Fraction(1, 2**n) + Fraction(1, 4**n)
            tail = Fraction(1, 2**n) + Fraction(1, 3 * 4**n)
            self.assertEqual(w - tail, Fraction(2, 3 * 4**n))
            self.assertGreater(w, tail)

    def test_full_totient_series_reconciles_with_mobius_truncation(self):
        # Independently enumerate coprime integers, without using the mu sieve
        # for totient values. Compare two independent convergent enclosures.
        N = 70
        mu = mobius_values(N)
        phi = lambda n: sum(math.gcd(n, k) == 1 for k in range(1, n + 1))
        for n in range(1, 51):
            mobius_convolution = sum(
                (n // d) * mu[d] for d in range(1, n + 1) if n % d == 0
            )
            self.assertEqual(phi(n), mobius_convolution)
        prefix = sum((Fraction(phi(n), 1 << n) for n in range(1, N + 1)),
                     Fraction())
        positive_tail_bound = Fraction(N + 2, 1 << N)
        for D in [1, 2, 5, 10, 18, 24]:
            self.assertLess(
                abs(prefix - truncation(D)),
                positive_tail_bound + absolute_tail_upper(D),
            )

    def test_receipt_is_exact_and_claim_bounded(self):
        receipt = reduced_denominator_receipt(24)
        self.assertEqual(receipt["claim_boundary"], "FULL_S_OPEN__FINITE_ARITHMETIC_ONLY")
        self.assertEqual(int(receipt["denominator"]) %
                         int(receipt["forced_factor"]), 0)
        self.assertEqual(receipt["exact_tail_sign"], mobius_one(receipt["next_squarefree"]))
        self.assertGreater(int(receipt["denominator_decimal_digits"]), 1)


if __name__ == "__main__":
    unittest.main()
