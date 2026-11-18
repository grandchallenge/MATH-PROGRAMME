"""Independent rational-value and cofinal-pulse controls for WP06."""
import math
import unittest
from fractions import Fraction

from experiments.erdos249_full_series_phase.rational_pulse_coboundary import (
    coefficient, depth_for_unit_tail_bound, discarded_difference_bound,
    exact_value, partial_coboundary, partial_value,
    prime_3mod4_after, pulse_support, same_depth_obstruction,
    separated_pulse_primes, verify_finite_pulses,
)


class RationalPulseCoboundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.shifts = (1, 3, 7)
        cls.primes = separated_pulse_primes(cls.shifts, 5, lower=11)
        cls.support = pulse_support(cls.shifts, cls.primes)

    def test_prime_sequence_is_3_mod4_and_separated(self):
        self.assertEqual(len(self.primes), 5)
        for p in self.primes:
            self.assertEqual(p % 4, 3)
            self.assertTrue(all(p % d for d in range(2, math.isqrt(p)+1)))
        self.assertTrue(all(q > p + 4*max(self.shifts)+1
                            for p, q in zip(self.primes, self.primes[1:])))

    def test_simultaneous_pulse_at_each_prime(self):
        self.assertTrue(verify_finite_pulses(self.shifts, self.primes,
                                            self.support))
        for p in self.primes:
            for h in self.shifts:
                self.assertEqual(
                    (coefficient(p+4*h, self.support)-coefficient(p, self.support))%4,
                    2)

    def test_coefficients_nonnegative_and_bounded_by_index(self):
        for n in range(1, self.primes[-1]+4*max(self.shifts)+30):
            a = coefficient(n, self.support)
            self.assertGreaterEqual(a, 0)
            self.assertLessEqual(a, n)

    def test_finite_coboundary_telescopes_exactly(self):
        for N in range(1, self.primes[-1]+4*max(self.shifts)+35):
            if N % 3:
                continue
            self.assertEqual(partial_coboundary(N, self.support),
                             -Fraction(int(N in self.support), 1 << N))

    def test_exact_rational_base_generating_function(self):
        self.assertEqual(exact_value(), Fraction(8, 255))
        # Independent 8-block sum: floor(n/8)=k for 8k<=n<8k+8
        # Rewriting as sum of indicator tails gives x^8/((1-x)(1-x^8)).
        x = Fraction(1, 2)
        self.assertEqual(exact_value(), 4*x**8 / ((1-x)*(1-x**8)))

    def test_partial_values_and_exact_tail_to_rational_value(self):
        for N in (8, 16, 40, 120, self.primes[-1]+31):
            prefix = partial_value(N, self.support)
            base_prefix = sum((Fraction(4*(n//8), 1 << n)
                               for n in range(1, N+1)), Fraction())
            self.assertEqual(prefix - base_prefix, partial_coboundary(N, self.support))
            # Base residual is strictly positive, with a proven comparison
            # using 4*floor(n/8)<=n:
            base_residual = exact_value() - base_prefix
            self.assertGreater(base_residual, 0)
            self.assertLessEqual(base_residual, Fraction(N+2, 1 << N))
            self.assertLessEqual(abs(exact_value()-prefix),
                                 Fraction(N+3, 1 << N))

    def test_any_finite_shift_set_without_overlap(self):
        for shifts in ((1,), (2, 5), (1, 2, 3, 4), (6, 11)):
            ps = separated_pulse_primes(shifts, 3)
            b = pulse_support(shifts, ps)
            self.assertTrue(verify_finite_pulses(shifts, ps, b))

    def test_invalid_adversarial_inputs_rejected(self):
        with self.assertRaises(ValueError):
            separated_pulse_primes((), 1)
        with self.assertRaises(ValueError):
            separated_pulse_primes((0,), 1)
        with self.assertRaises(ValueError):
            separated_pulse_primes((1,), 0)
        with self.assertRaises(ValueError):
            pulse_support((1,), (9,))
        with self.assertRaises(ValueError):
            coefficient(0, set())
        with self.assertRaises(ValueError):
            depth_for_unit_tail_bound(0, 0)

    def test_two_scale_remainder_bound_monotone_sufficient_depth(self):
        for N, H in ((0, 1), (5, 4), (63, 17), (4096, 13)):
            L = depth_for_unit_tail_bound(N, H)
            self.assertLess(discarded_difference_bound(N, H, L), 1)
            if L > 1:
                self.assertGreaterEqual(discarded_difference_bound(N, H, L-1), 1)
        self.assertGreater(depth_for_unit_tail_bound(256, 4),
                           depth_for_unit_tail_bound(8, 4))

    def test_same_depth_obstruction_totient_endpoint(self):
        n = 16
        phi = sum(math.gcd(n,k)==1 for k in range(1,n+1))
        self.assertEqual(phi, 8)
        self.assertTrue(same_depth_obstruction(14, 4, 2, 3, phi))
        self.assertFalse(same_depth_obstruction(14, 4, 4, 3, phi))
        self.assertGreater(discarded_difference_bound(14, 4, 2), 1)
        with self.assertRaises(ValueError):
            same_depth_obstruction(14, 4, 2, 4, phi)
        with self.assertRaises(ValueError):
            same_depth_obstruction(0, 4, 2, 2, phi)

    def test_rational_value_does_not_force_pulse_periodicity(self):
        # b can be chosen with infinitely many arbitrary well-separated
        # prime pulses, while the exact real value stays 8/255.
        # The finite fixture checks the local identity, not infinitude.
        self.assertEqual(exact_value().denominator, 255)
        self.assertEqual(exact_value().numerator, 8)
        self.assertTrue(all(coefficient(p+4*h,self.support)-coefficient(p,self.support)
                            != 0 for p in self.primes for h in self.shifts))


if __name__ == "__main__":
    unittest.main()
