"""Hostile exact-integer tests for the irrational sparse-orbit Fourier no-go."""
import cmath
import math
import unittest

import experiments.erdos249_full_series_phase.sparse_orbit as o


class SparseIrrationalOrbitTests(unittest.TestCase):
    def test_source_locked_binary_exponents_and_gap(self):
        es = [o.exponent(m) for m in range(13)]
        self.assertEqual(es[:7], [2, 3, 6, 13, 28, 59, 122])
        for m in range(1, 40):
            self.assertEqual(o.exponent(m+1)-o.exponent(m), (1 << (m+1))-1)
            self.assertGreaterEqual(o.exponent(m), 1 << m)

    def test_exact_fractional_residue_against_independent_sum(self):
        for N in [0, 1, 2, 3, 6, 11, 59, 70, 127, 997, 2048]:
            for L in [1, 2, 4, 11, 32, 48]:
                expected = sum(
                    (1 << (N + L - e))
                    for e in [((1 << (m+1))-m) for m in range(30)]
                    if N < e <= N+L
                )
                self.assertEqual(o.dyadic_residue(N, L), expected)
                self.assertLess(expected, 1 << L)

    def test_finite_truncations_are_nested_and_error_bounded(self):
        from fractions import Fraction
        for N in [0, 12, 28, 54, 111, 1023, 8180]:
            r24 = Fraction(o.dyadic_residue(N, 24), 1 << 24)
            r48 = Fraction(o.dyadic_residue(N, 48), 1 << 48)
            self.assertGreaterEqual(r48, r24)
            self.assertLessEqual(r48-r24, Fraction(1, 1 << 24))

    def test_bad_index_enumeration_and_uniform_analytic_bound(self):
        for X in [8, 16, 128, 1024]:
            for K in [1, 3, 11]:
                es = o.support_through(2*X+K)
                expected = sum(any(N < e <= N+K for e in es) for N in range(X, 2*X))
                self.assertEqual(o.exceptional_count(X, K), expected)
                self.assertLessEqual(expected, K * (2*X+K).bit_length())
                self.assertLessEqual(o.sharpened_phase_bound(X,K,64),
                                     o.universal_phase_bound(X,K,64)+1e-12)

    def test_polynomial_harmonic_bound_tends_to_zero(self):
        xs = [1024, 4096, 16384, 65536]
        for degree in [0, 1, 2]:
            bounds = [o.polynomial_harmonic_bound(X, degree)['universal_bound'] for X in xs]
            self.assertTrue(all(b > 0 for b in bounds))
            self.assertEqual(bounds, sorted(bounds, reverse=True))
            self.assertLess(bounds[-1], 0.1)
        self.assertEqual(o.polynomial_harmonic_bound(8192,1)['H'],8192)

    def test_actual_sparse_lacunary_phases_obey_explicit_bound(self):
        X, K, L = 8192, 3 * 13, 48
        for h in [1, 3, 7, 31, 64]:
            m = o.phase_mean(X, L, h)
            bound = o.sharpened_phase_bound(X,K,h) + 2*math.pi*h*2**(-L)
            self.assertLessEqual(abs(m-1),bound + 1e-12)
            self.assertLess(abs(m-1),0.06)
        self.assertLess(o.universal_phase_bound(65536,48,65536),0.05)

    def test_rational_control_not_conflated_with_irrational(self):
        # 4/3 has a period-two doubling orbit, h=3 is identically one.
        exact = [cmath.exp(2j*math.pi*(3 * (2**N%3) / 3)) for N in range(2,130)]
        self.assertTrue(all(abs(z-1)<1e-12 for z in exact))
        # This tests a negative inference: phase lock cannot imply rationality.
        self.assertLess(abs(o.phase_mean(8192,48,1)-1),0.06)


if __name__ == '__main__':
    unittest.main()
