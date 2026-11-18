"""Hostile exact arithmetic checks for Erdős #249 WP05.

No finite CRT witness is presented as proof of infinitely many primes or
irrationality of the full binary totient series.
"""
import math
import unittest
from fractions import Fraction

from experiments.erdos249_full_series_phase.prime_pulse_crt import (
    backward_midpoint, forward_family, forward_receipt, is_prime,
    midpoint_receipt, phi, progression, scan_prime, v2,
)


class PrimePulseCrtTests(unittest.TestCase):
    def test_phi_factorization_vs_independent_gcd_count(self):
        for n in range(1, 151):
            self.assertEqual(phi(n), sum(math.gcd(n, k) == 1
                                         for k in range(1, n + 1)))

    def test_prime_and_valuation_edge_cases(self):
        self.assertEqual([is_prime(k) for k in range(10)],
                         [False, False, True, True, False, True, False,
                          True, False, False])
        self.assertEqual([v2(x) for x in (2, 4, 6, 8, -24)],
                         [1, 2, 1, 3, 3])
        with self.assertRaises(ValueError):
            v2(0)

    def test_ill_formed_crt_rejected(self):
        for args in (((), 2, 4, 3), ((0,), 2, 4, 3),
                     ((1,), 1, 4, 3), ((1,), 2, 4, 2)):
            with self.assertRaises(ValueError):
                progression(*args)
        with self.assertRaises(ValueError):
            backward_midpoint(2, 3)

    def test_forward_crt_is_reduced_and_satisfies_all_offsets(self):
        for hset, L, K in (((1,), 1, 1), ((1,), 2, 3),
                           ((1, 2), 1, 2)):
            data = forward_family(hset, L, K)
            self.assertEqual(math.gcd(data["residue"], data["modulus"]), 1)
            self.assertEqual(data["residue"] % 4, 3)
            self.assertEqual(data["modulus"],
                             4 * math.prod(data["offset_primes"].values()))
            self.assertEqual(len(data["offset_primes"]),
                             len(set(data["offset_primes"].values())))
            for t, q in data["offset_primes"].items():
                self.assertTrue(is_prime(q))
                self.assertGreater(q, abs(t))
                self.assertEqual(q % (1 << max(K, 2)), 1)
                self.assertEqual((data["residue"] + t) % q, 0)

    def test_single_prime_forward_pulses(self):
        for L, K in ((1, 1), (2, 3)):
            data = forward_family((1,), L, K)
            p = scan_prime(data, max_steps=300)
            row = forward_receipt(data, p)
            self.assertEqual(row["prime"] % 4, 3)
            self.assertEqual(row["shift_values"][1]["delta0"] % 4, 2)
            if K >= L:
                self.assertEqual(row["shift_values"][1]["residue"], 0)
            self.assertEqual(row["boundary"],
                             "FINITE_CONGRUENCE_ONLY__FULL_S_OPEN")

    def test_simultaneous_forward_family_has_one_prime(self):
        data = forward_family((1, 2), 1, 2)
        p = scan_prime(data, max_steps=200)
        receipt = forward_receipt(data, p)
        for h in (1, 2):
            self.assertEqual(receipt["shift_values"][h]["delta0"] % 4, 2)
            self.assertEqual(receipt["shift_values"][h]["residue"], 0)

    def test_forward_dyadic_sum_exact(self):
        data = forward_family((1,), 2, 3)
        p = scan_prime(data, max_steps=150)
        v = forward_receipt(data, p)["shift_values"][1]
        self.assertEqual(
            v["finite_fraction"],
            sum((Fraction(d, 1 << (j+1))
                 for j, d in enumerate(v["deltas"])), Fraction()))
        self.assertEqual(v["finite_fraction"].denominator, 1)
        self.assertEqual(v["finite_fraction"].numerator % 2, 0)

    def test_backward_cook_midpoint_residue(self):
        for H, K in ((3, 2), (4, 3)):
            data = backward_midpoint(H, K)
            p = scan_prime(data, lower=H + K + 1, max_steps=300)
            value = midpoint_receipt(data, p)
            self.assertEqual(value["residue"], 1 << (K - 1))
            self.assertGreater(value["directed_lower_threshold"],
                               (1 << K) - 1)
            self.assertFalse(value["same_depth_certificate_passes"])
            self.assertGreaterEqual(p - 1, 1 << K)

    def test_midpoint_hostile_malformed_prime_rejected(self):
        data = backward_midpoint(3, 2)
        for bad_p in (3, 4, 5):
            with self.assertRaises((ValueError, AssertionError)):
                midpoint_receipt(data, bad_p)

    def test_undefined_primality_search_limit_rejected(self):
        with self.assertRaises(ValueError):
            scan_prime(forward_family((1,), 1, 2), max_steps=0)

    def test_strictly_finite_rational_control(self):
        data = forward_family((1,), 1, 2)
        p = scan_prime(data, max_steps=100)
        # A rational finite polynomial shares all coefficients at the
        # witnessed indices. It changes with p: NOT a cofinal control.
        n = p + 5
        comparator = sum((Fraction(phi(j), 1 << j)
                          for j in range(1, n + 1)), Fraction())
        self.assertIsInstance(comparator, Fraction)
        self.assertEqual(forward_receipt(data, p)["shift_values"][1]["residue"], 0)

    def test_discarded_error_is_only_an_upper_bound(self):
        data = forward_family((1,), 1, 2)
        p = scan_prime(data, max_steps=100)
        v = forward_receipt(data, p)["shift_values"][1]
        self.assertEqual(v["tail_error_upper"], Fraction(p + 7, 2))
        self.assertGreater(v["tail_error_upper"], 1)


if __name__ == "__main__":
    unittest.main()
