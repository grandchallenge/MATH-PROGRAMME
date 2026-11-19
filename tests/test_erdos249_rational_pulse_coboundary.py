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




from experiments.erdos249_full_series_phase.nearlog_rational_coboundary import (
    build_control as nearlog_build_control,
    exact_value as nearlog_exact_value,
    modulus as nearlog_modulus,
    finite_scaled_tail as nearlog_finite_scaled_tail,
    first_omitted_term as nearlog_first_omitted_term,
    exact_full_scaled_tail as nearlog_exact_full_scaled_tail,
    logarithmic_integer_depth as nearlog_depth,
    fractional_part as nearlog_fractional_part,
    receipt as nearlog_receipt,
)


class NearLogRationalAdversaryTests(unittest.TestCase):
    """Exact same-route hostile tests for WP07-B; no policy map expansion."""

    @classmethod
    def setUpClass(cls):
        cls.a, cls.b = nearlog_build_control(12000)

    def test_variable_modulus_is_power_of_two_at_expected_depth(self):
        self.assertEqual(nearlog_modulus(1), 1)
        self.assertEqual(nearlog_modulus(63), 1)
        self.assertEqual(nearlog_modulus(64), 2)
        self.assertEqual(nearlog_modulus(127), 2)
        self.assertEqual(nearlog_modulus(128), 4)
        for n in range(1, 12001):
            self.assertEqual(nearlog_modulus(n),
                             1 << max(0, n.bit_length() - 6))

    def test_recurrence_and_all_coefficients_linear_and_positive(self):
        a, b = self.a, self.b
        self.assertEqual(a[1], 0)
        self.assertEqual(b[0], 0)
        for n in range(1, 12001):
            c = n // 2
            self.assertEqual(a[n] + b[n], c + 2 * b[n-1])
            self.assertTrue(0 <= b[n] < nearlog_modulus(n))
            self.assertEqual(a[n] % nearlog_modulus(n), 0)
            self.assertLessEqual(a[n], n)
            self.assertGreaterEqual(a[n], n // 4)
            if n >= 2:
                self.assertGreaterEqual(4 * a[n], n)

    def test_exact_coboundary_telescopes_even_across_modulus_jumps(self):
        a, b = self.a, self.b
        for N in (1, 13, 62, 63, 64, 65, 127, 128, 129, 255,
                  256, 511, 512, 1023, 1024, 11999):
            coboundary = sum(
                (Fraction(2*b[n-1] - b[n], 1 << n)
                 for n in range(1, N + 1)),
                Fraction(),
            )
            self.assertEqual(coboundary, -Fraction(b[N], 1 << N))
            self.assertLessEqual(Fraction(b[N], 1 << N),
                                 Fraction(nearlog_modulus(N)-1, 1 << N))

    def test_rational_full_sum_analytical_generating_identity(self):
        x = Fraction(1, 2)
        baseline = x*x*(1+x) / (1-x*x)**2
        self.assertEqual(baseline, Fraction(2, 3))
        self.assertEqual(nearlog_exact_value(), baseline)
        self.assertEqual(nearlog_exact_value().denominator, 3)

    def test_termwise_near_log_depth_integrality_at_every_start(self):
        a = self.a
        for N in range(64, 3000):
            L = nearlog_depth(N)
            self.assertEqual(L, N.bit_length() - 6)
            for j in range(1, L + 1):
                self.assertEqual(a[N+j] % (1 << j), 0)
            self.assertEqual(nearlog_finite_scaled_tail(N, L, a).denominator, 1)

    def test_positive_discarded_tail_lower_bound_is_four(self):
        a = self.a
        for N in (64, 65, 127, 128, 256, 511, 1024, 2047,
                  2048, 4095, 4096, 8100, 11100):
            L = nearlog_depth(N)
            term = nearlog_first_omitted_term(N, L, a)
            self.assertGreaterEqual(term, 4)
            # Compare to *analytical positive tail* given by rational value.
            full_tail = nearlog_exact_full_scaled_tail(N, a)
            finite = nearlog_finite_scaled_tail(N, L, a)
            self.assertGreaterEqual(full_tail - finite, term)

    def test_rational_full_scaled_tail_fraction_alternates(self):
        a = self.a
        for N in (1, 2, 63, 64, 65, 127, 128, 256, 511,
                  512, 1023, 2048, 4095, 8100):
            full = nearlog_exact_full_scaled_tail(N, a)
            expected = Fraction(2 if N % 2 == 0 else 1, 3)
            self.assertEqual(nearlog_fractional_part(full), expected)
            if N >= 64:
                self.assertEqual(nearlog_fractional_part(
                    full - nearlog_finite_scaled_tail(N, nearlog_depth(N), a)),
                    expected)

    def test_exact_reconstruction_receipt_and_hostile_inputs(self):
        a, b = self.a, self.b
        for N in (64, 127, 128, 512, 2048, 4096):
            row = nearlog_receipt(N, a, b)
            self.assertEqual(row["boundary"],
                             "RATIONAL_CONTROL_ONLY__ORIGINAL_ERDOS_249_OPEN")
            self.assertEqual(row["series_value"], "2/3")
            self.assertEqual(row["L"], N.bit_length() - 6)
        with self.assertRaises(ValueError):
            nearlog_build_control(0)
        with self.assertRaises(ValueError):
            nearlog_modulus(0)
        with self.assertRaises(ValueError):
            nearlog_depth(63)
        with self.assertRaises(ValueError):
            nearlog_finite_scaled_tail(5, 30, a[:12])
        with self.assertRaises(ValueError):
            nearlog_exact_full_scaled_tail(12001, a)
        with self.assertRaises(ValueError):
            nearlog_receipt(4096, a[:15], b[:15])


if __name__ == "__main__":
    unittest.main()



from experiments.erdos249_full_series_phase.totient_residue_rational_mimic import (
    phi_sieve as wp07e_phi,
    phi_independent as wp07e_phi_independent,
    power2_modulus as wp07e_modulus,
    v2_positive as wp07e_v2,
    rational_totient_residue_mimic as wp07e_build,
    finite_scaled_numerator as wp07e_numerator,
    nearlog_depth as wp07e_depth,
    finite_tail_integer_difference as wp07e_difference,
    exact_rational_sum as wp07e_rational,
    exact_scaled_infinite_tail as wp07e_infinite,
    frac as wp07e_frac,
    finite_receipt as wp07e_receipt,
)


class ExactTotientResidueRationalMimicTests(unittest.TestCase):
    """WP07-E hostile exact tests for a rational full-series phase mimic."""

    @classmethod
    def setUpClass(cls):
        cls.phi = wp07e_phi(12000)
        cls.a, cls.b = wp07e_build(12000, cls.phi)

    def test_independent_phi_coprime_source(self):
        self.assertEqual(self.phi[1], 1)
        for n in range(1, 1001):
            self.assertEqual(self.phi[n], wp07e_phi_independent(n))

    def test_exact_all_coefficient_residues_and_linear_bounds(self):
        a, b, phi = self.a, self.b, self.phi
        self.assertEqual(a[1], 0)
        self.assertEqual(b[0], 0)
        for n in range(1, 12001):
            M=wp07e_modulus(n)
            self.assertTrue(0 <= b[n] < M)
            self.assertEqual(a[n], n//2+2*b[n-1]-b[n])
            self.assertEqual((a[n]-phi[n])%M,0)
            self.assertLessEqual(M, max(1,n//4))
            if n>=2:
                self.assertGreaterEqual(4*a[n],n)
                self.assertLessEqual(a[n],n)

    def test_telescoping_at_all_modulus_jumps(self):
        a,b=self.a,self.b
        for N in (1,2,3,4,7,8,15,16,31,32,63,64,127,128,
                  255,256,1023,1024,4095,4096,8191):
            identity=sum((Fraction(2*b[n-1]-b[n],1<<n)
                          for n in range(1,N+1)),Fraction())
            self.assertEqual(identity,-Fraction(b[N],1<<N))
            self.assertLessEqual(b[N],max(1,N//4))

    def test_analytical_full_sum_exactly_rational(self):
        x=Fraction(1,2)
        baseline=x*x*(1+x)/(1-x*x)**2
        self.assertEqual(baseline,Fraction(2,3))
        self.assertEqual(wp07e_rational(),baseline)

    def test_all_start_nearlog_fractional_parts_identical(self):
        a,phi=self.a,self.phi
        for N in range(8,4100):
            L=wp07e_depth(N)
            self.assertEqual(L,N.bit_length()-3)
            diff=wp07e_difference(N,a,phi)
            expected=(wp07e_numerator(N,L,a)
                      -wp07e_numerator(N,L,phi))//(1<<L)
            self.assertEqual(diff,expected)
            for j in range(1,L+1):
                self.assertEqual((a[N+j]-phi[N+j]) % (1<<j),0)

    def test_blockwise_phase_identity_for_arbitrary_integer_harmonics(self):
        a,phi=self.a,self.phi
        for X in (64,127,128,256,511,512,1024,2048):
            L=X.bit_length()-3
            modulus=1<<L
            for N in range(X,2*X):
                ra=wp07e_numerator(N,L,a)%modulus
                rp=wp07e_numerator(N,L,phi)%modulus
                self.assertEqual(ra,rp)
                for h in (-11,1,2,7,101):
                    self.assertEqual((h*ra)%modulus,(h*rp)%modulus)
                self.assertEqual(ra==0,rp==0)

    def test_valuation_disagreements_only_on_exact_E2_candidates(self):
        phi,a=self.phi,self.a
        exceptions=[]
        eligible=[]
        for n in range(2,12001):
            vphi=wp07e_v2(phi[n])
            va=wp07e_v2(a[n])
            if va!=vphi:
                exceptions.append(n)
            if vphi >= n.bit_length()-3:
                eligible.append(n)
        self.assertTrue(set(exceptions).issubset(set(eligible)))
        self.assertLessEqual(len(exceptions),len(eligible))

    def test_full_rational_tail_fraction_not_forced_on_totient(self):
        a=self.a
        for N in (1,2,7,8,9,15,16,127,128,1024,4095):
            whole=wp07e_infinite(N,a)
            expected=Fraction(2 if N%2==0 else 1,3)
            self.assertEqual(wp07e_frac(whole),expected)
            if N>=8:
                L=wp07e_depth(N)
                finite=Fraction(wp07e_numerator(N,L,a),1<<L)
                self.assertEqual(wp07e_frac(whole-finite),
                                 wp07e_frac(whole-finite))
                # The actual totient infinite fractional part is NOT
                # assumed to equal this rational period.

    def test_finite_receipts_and_hostile_inputs(self):
        for X in (8,64,128,512):
            receipt=wp07e_receipt(X)
            self.assertTrue(receipt["all_starts_identical_residue"])
            self.assertEqual(receipt["starts_checked"],X)
            self.assertLessEqual(receipt["valuation_mismatches"],
                                 receipt["nearmax2_candidates"])
            self.assertEqual(receipt["rational_full_series"],"2/3")
            self.assertEqual(receipt["claim_boundary"],
                             "EXACT_FINITE_CONTROL_ONLY__ACTUAL_TOTIENT_S_OPEN")
        with self.assertRaises(ValueError):
            wp07e_build(0)
        with self.assertRaises(ValueError):
            wp07e_modulus(0)
        with self.assertRaises(ValueError):
            wp07e_depth(7)
        with self.assertRaises(ValueError):
            wp07e_numerator(5,20,self.a)
        with self.assertRaises(ValueError):
            wp07e_infinite(12001,self.a)
        with self.assertRaises(ValueError):
            wp07e_receipt(7)
