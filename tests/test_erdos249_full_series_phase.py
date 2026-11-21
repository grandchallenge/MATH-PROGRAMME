"""Exact-rational and modular controls for ERDOS249 moving-depth phase experiment."""
import unittest,math,json
from fractions import Fraction
from experiments.erdos249_full_series_phase.depth_stress import main as run_depth_stress
from pathlib import Path
from experiments.erdos249_full_series_phase.fourier_probe import totients, comparator, exact_residue, residue_sequence, phase_scan

def mobius(n):
    is_prime=[True]*(n+1)
    is_prime[:2]=[False,False]
    mu=[1]*(n+1)
    for x in range(2,n+1):
        if is_prime[x]:
            for k in range(x,n+1,x):
                mu[k]*=-1
                if k>x:
                    is_prime[k]=False
            for k in range(x*x,n+1,x*x):
                mu[k]=0
    return mu

class PhaseProbeTests(unittest.TestCase):
    def test_totient_against_definition(self):
        from math import gcd
        a=totients(192)
        for n in range(1,193):
            self.assertEqual(a[n],sum(gcd(n,j)==1 for j in range(1,n+1)))
    def test_elementary_totient_lower_bound(self):
        a=totients(132000)
        self.assertTrue(all(2*a[n]*a[n]>=n for n in range(1,len(a))))
    def test_rolling_residues_vs_independent_direct(self):
        phi=totients(512)
        for L in (2,4,8,16,48):
            X=96
            seq=list(residue_sequence(phi.__getitem__,X,L))
            self.assertEqual(len(seq),X)
            for k,r in enumerate(seq):
                N=X+k
                naive=sum(phi[N+j]*2**(L-j) for j in range(1,L+1))%(2**L)
                self.assertEqual(r,naive)
    def test_rational_comparator_exact(self):
        N=44
        prefix=Fraction(sum(comparator(n)*(2**(N-n)) for n in range(1,N+1)),2**N)
        self.assertGreater(Fraction(4,3),prefix)
        self.assertLessEqual(Fraction(4,3)-prefix,Fraction(N+2,2**N))
        z=phase_scan(comparator,512,48,3)
        self.assertLess(abs(z[0]['modulus']-0.5),1e-6)
        self.assertLess(abs(z[2]['modulus']-1.0),1e-6)
    def test_exact_finite_mobius_totient_identity(self):
        N,D=72,24
        a=totients(N)
        mu=mobius(D)
        prefix=Fraction(sum(a[n]*2**(N-n) for n in range(1,N+1)),2**N)
        mobius_prefix=Fraction(1,2)+sum((Fraction(mu[d],(2**d-1)**2) for d in range(1,D+1)),Fraction(0))
        bound=Fraction(N+2,2**N)+Fraction(4,3*4**D)
        self.assertLessEqual(abs(prefix-mobius_prefix),bound)
    def test_depth_stress_module_exact_replay(self):
        from hashlib import sha256
        run_depth_stress()
        d=Path(__file__).resolve().parents[1]/'experiments'/'erdos249_full_series_phase'
        self.assertEqual(
            sha256((d/'depth_stress_results.json').read_bytes()).hexdigest(),
            '368db4b6674c75b915fa103f8287d8347a6c07dc83b7ddf34afd5d5633201d33')

    def test_output_integrity_and_known_controls(self):
        d=Path(__file__).resolve().parents[1]/'experiments'/'erdos249_full_series_phase'
        for X,H in ((1024,32),(4096,32),(16384,64),(65536,64)):
            z=json.loads((d/f'result_{X}.json').read_text())
            self.assertEqual((z['x'],z['truncation_L'],z['max_h']),(X,48,H))
            self.assertEqual(len(z['actual_totient']),H)
            self.assertEqual(z['rational_control_4_over_3'][2]['modulus'],1)
            self.assertLess(z['actual_totient'][0]['modulus'],0.05)
            self.assertLess(z['phase_error_le'],1e-6)
        ds=json.loads((d/'depth_stress_results.json').read_text())
        self.assertEqual(len(ds['rows']),32)
        self.assertEqual([(r['integral_fraction']) for r in ds['rows'] if r['L']==2],
                sorted([r['integral_fraction'] for r in ds['rows'] if r['L']==2]))


from experiments.erdos249_full_series_phase.nearmax_totient_valuation import (
    totients as nearmax_totients,
    factors as nearmax_factors,
    v2 as nearmax_v2,
    odd_part as nearmax_odd_part,
    is_nearmax,
    restricted_factor_shape,
    small_odd_exponent_patterns,
    weighted_subset_envelope,
    finite_shape_envelope,
    nearmax_witnesses,
    termwise_nearlog_starts,
    research_receipt as nearmax_receipt,
)


class NearMaxTotientValuationTests(unittest.TestCase):
    """WP07-C elementary shape and nearlog counting controls."""

    def test_independent_factor_oracle_and_totient_sieve(self):
        phi = nearmax_totients(720)
        for n in range(1, 721):
            self.assertEqual(phi[n], sum(math.gcd(n,j)==1 for j in range(1,n+1)))
            reconstruction = n
            for p, a in nearmax_factors(n):
                self.assertGreaterEqual(a, 1)
                self.assertEqual(reconstruction % (p**a), 0)
                reconstruction //= p**a
            self.assertEqual(reconstruction, 1)

    def test_oddpart_and_prime_shape_at_all_eligible_small_indices(self):
        X=6000
        phi=nearmax_totients(X)
        for C in (0, 1, 2, 3, 5):
            B=1 << (C+1)
            eligible=nearmax_witnesses(X,C,phi)
            self.assertTrue(1 in eligible)
            for n in eligible:
                cert=restricted_factor_shape(n,C,phi)
                self.assertLess(cert["bounded_odd_part"], B)
                self.assertEqual(cert["boundary"],
                                 "SHAPE_NECESSARY_ONLY__FULL_S_OPEN")
                for p,a,r,d in cert["odd_primes"]:
                    self.assertEqual(p,1+d*(1<<r))
                    self.assertEqual(nearmax_odd_part(p-1),d)
                    self.assertLess(d,B)
                    if p>B:
                        self.assertEqual(a,1)

    def test_small_prime_exponent_choices(self):
        self.assertEqual(small_odd_exponent_patterns(2),1)
        self.assertEqual(small_odd_exponent_patterns(4),3)
        self.assertEqual(small_odd_exponent_patterns(8),27)
        self.assertEqual(small_odd_exponent_patterns(16),4*3**4)

    def test_partition_majorant_against_independent_subset_enumeration(self):
        from itertools import product
        for R,B in ((3,2),(4,2),(4,3)):
            # B independent distinguishable candidate slots at each level.
            brute=sum(
                sum((i//B+1)*bit for i,bit in enumerate(bits))<=R
                for bits in product((0,1), repeat=R*B)
            )
            self.assertEqual(weighted_subset_envelope(R,B),brute)

    def test_all_nearmax_counts_below_exact_combinatorial_envelope(self):
        for X,C in ((100,0),(1000,1),(10000,2),(10000,3)):
            count=len(nearmax_witnesses(X,C))
            self.assertLessEqual(count,finite_shape_envelope(X,C))
            self.assertGreaterEqual(count,1)

    def test_nearlog_termwise_windows_imply_nearmax_last_term(self):
        for X,C in ((64,0),(128,1),(512,2),(2048,2),(4096,3)):
            L=X.bit_length()-1-C
            phi=nearmax_totients(3*X)
            good=termwise_nearlog_starts(X,C,phi)
            eligible=set(nearmax_witnesses(3*X,C+2,phi))
            self.assertTrue(all(N+L in eligible for N in good))
            for N in good:
                self.assertEqual(phi[N+L] % (1<<L),0)

    def test_finite_receipts_have_correct_epistemic_boundary(self):
        for X,C in ((64,1),(256,2),(1024,3)):
            r=nearmax_receipt(X,C)
            self.assertEqual(r["X"],X)
            self.assertEqual(r["C"],C)
            self.assertLessEqual(r["termwise_integer_starts"],
                                 r["nearmax_eligible_until_3X"])
            self.assertEqual(
                r["claim_boundary"],
                "FINITE_CHECK_ONLY__EXACT_ELEMENTARY_PROOF__FULL_S_OPEN",
            )

    def test_high_valuation_does_not_imply_full_series_irrationality(self):
        # A synthetic rational nearlog comparator has such valuations
        # everywhere, but its full sum remains 2/3.
        # Independent witness code is deliberately local: WP07-B may still be
        # awaiting protected admission, and this test must not import it.
        a=[0]*512
        b=[0]*512
        for n in range(1,512):
            M=1<<max(0,n.bit_length()-6)
            q=(n//2)+2*b[n-1]
            b[n]=q%M
            a[n]=q-b[n]
        x=Fraction(1,2)
        self.assertEqual(x*x*(1+x)/(1-x*x)**2,Fraction(2,3))
        for N in range(64,300):
            L=N.bit_length()-6
            finite=sum((Fraction(a[N+j],1<<j) for j in range(1,L+1)),
                       Fraction())
            self.assertEqual(finite.denominator,1)
        # Termwise integrality is stronger than total integrality:
        phi=nearmax_totients(4)
        self.assertEqual(Fraction(phi[2],2)+Fraction(phi[3],4),1)
        self.assertEqual(phi[2]%2,1)

    def test_malformed_contracts_fail(self):
        with self.assertRaises(ValueError):
            nearmax_totients(0)
        with self.assertRaises(ValueError):
            nearmax_factors(0)
        with self.assertRaises(ValueError):
            nearmax_v2(0)
        with self.assertRaises(ValueError):
            nearmax_odd_part(0)
        with self.assertRaises(ValueError):
            finite_shape_envelope(1,0)
        with self.assertRaises(ValueError):
            finite_shape_envelope(100,-1)
        with self.assertRaises(ValueError):
            weighted_subset_envelope(0,2)
        with self.assertRaises(ValueError):
            termwise_nearlog_starts(64,8)
        with self.assertRaises(ValueError):
            restricted_factor_shape(9,0,nearmax_totients(15))


    def test_exact_rolling_integral_sum_recurrence_vs_direct_definition(self):
        from experiments.erdos249_full_series_phase.nearmax_totient_valuation import (
            finite_scaled_numerator, nearlog_integral_sums_and_adjacent_pairs,
        )
        for X,C in ((32,1),(64,0),(128,2),(256,2),(512,3)):
            L=X.bit_length()-1-C
            phi=nearmax_totients(3*X)
            starts, adjacent=nearlog_integral_sums_and_adjacent_pairs(X,C,phi)
            expected=[]
            expected_adj=[]
            for N in range(X,2*X):
                A=finite_scaled_numerator(N,L,phi)
                next_A=finite_scaled_numerator(N+1,L,phi)
                self.assertEqual(next_A,2*A-(1<<L)*phi[N+1]+phi[N+L+1])
                if A % (1<<L)==0:
                    expected.append(N)
                    if next_A % (1<<L)==0:
                        expected_adj.append(N)
            self.assertEqual(starts,tuple(expected))
            self.assertEqual(adjacent,tuple(expected_adj))

    def test_adjacent_integral_sums_force_nearmax_last_coefficient(self):
        from experiments.erdos249_full_series_phase.nearmax_totient_valuation import (
            nearlog_integral_sums_and_adjacent_pairs,
        )
        for X,C in ((64,0),(128,1),(512,2),(2048,2),(4096,3)):
            phi=nearmax_totients(3*X)
            L=X.bit_length()-1-C
            starts,adjacent=nearlog_integral_sums_and_adjacent_pairs(X,C,phi)
            eligible=set(nearmax_witnesses(3*X,C+2,phi))
            self.assertTrue(all(N+L+1 in eligible for N in adjacent))
            self.assertLessEqual(len(adjacent),len(eligible))
            self.assertLessEqual(len(starts),(X+1)//2+len(adjacent))

    def test_nearlog_rational_control_not_replicated_by_totient_recurrence(self):
        # Independent local synthetic recurrence: no dependency on the WP07-B
        # branch, which might still be in the protected merge queue.
        X,C=128,5
        L=X.bit_length()-1-C
        a=[0]*512
        b=[0]*512
        for n in range(1,512):
            M=1<<max(0,n.bit_length()-6)
            q=n//2+2*b[n-1]
            b[n]=q%M
            a[n]=q-b[n]
        self.assertTrue(all(
            sum(a[N+j] << (L-j) for j in range(1,L+1)) % (1<<L)==0
            for N in range(X,2*X+1)
        ))
        from experiments.erdos249_full_series_phase.nearmax_totient_valuation import (
            nearlog_integral_sums_and_adjacent_pairs,
        )
        phi=nearmax_totients(3*X)
        actual_starts,adjacent=nearlog_integral_sums_and_adjacent_pairs(X,C,phi)
        self.assertLessEqual(len(adjacent),len(nearmax_witnesses(3*X,C+2,phi)))
        self.assertLessEqual(len(actual_starts),(X+1)//2+len(adjacent))



from experiments.erdos249_full_series_phase.nearmax_totient_valuation import (
    odd_part_budget as wp07d_odd_budget,
    fermat_exponent_slots as wp07d_fermat_slots,
    polylog_fermat_envelope as wp07d_polylog_bound,
    fermat_prime_shape_check as wp07d_prime_shape,
    fermat_equality_criterion as wp07d_equality,
    polylog_research_receipt as wp07d_receipt,
)


class FermatPolylogNearmaxTests(unittest.TestCase):
    """Independent arithmetical checks of WP07-D's proved bounds.

    The tests do not establish a new asymptotic, novelty or irrationality.
    """

    def test_exact_odd_factor_budget_and_fermat_exponent_levels(self):
        for B in (2, 3, 4, 8, 9, 10, 16, 32, 64, 128):
            expected = 0
            while 3 ** (expected + 1) < B:
                expected += 1
            self.assertEqual(wp07d_odd_budget(B), expected)
        for R in range(1, 150):
            brute = sum(1 for r in range(1, R + 1)
                        if (r & (r-1)) == 0)
            self.assertEqual(wp07d_fermat_slots(R), brute)
            self.assertLessEqual(1 << brute, 2*R)

    def test_fermat_product_identity_without_primality_assumption(self):
        for m in range(6):
            factors_list = [(1 << (1 << j)) + 1 for j in range(m + 1)]
            product = math.prod(factors_list)
            self.assertEqual(product, (1 << (1 << (m + 1))) - 1)
            total_r = sum(1 << j for j in range(m + 1))
            self.assertGreaterEqual(product, 1 << total_r)
            self.assertLess(product, 1 << (total_r+1))

    def test_extremal_totient_classification_independently_to_100000(self):
        phi = nearmax_totients(100000)
        actual = [n for n in range(1, 100001)
                  if nearmax_v2(phi[n]) >= n.bit_length()-1]
        expected = [1,3,5,15,17,51,85,255,257,771,1285,3855,
                    4369,13107,21845,65535,65537]
        self.assertEqual(actual, expected)
        for n in range(1, 100001):
            # This follows from the *actual* independent factorization,
            # rather than from the WP07-D bound or the source dataset.
            self.assertEqual(wp07d_equality(n), n in set(expected))

    def test_large_fermat_prime_forces_power_two_exponent(self):
        phi = nearmax_totients(12000)
        for C in (0,1,2,3,4):
            for n in nearmax_witnesses(12000,C,phi):
                row = wp07d_prime_shape(n,C,phi)
                self.assertEqual(
                    row["claim_boundary"],
                    "NECESSARY_SHAPE_ONLY__ORIGINAL_249_OPEN",
                )
                self.assertGreaterEqual(row["odd_part"],
                                        row["odd_d_product"])
                for p in row["large_fermat_factors"]:
                    r = nearmax_v2(p-1)
                    self.assertEqual((p-1)>>r,1)
                    self.assertEqual(r & (r-1), 0)
                self.assertLessEqual(len(row["large_nonfermat_factors"]),
                                     wp07d_odd_budget(1 << (C+1)))

    def test_polylog_envelope_bounds_exhaustive_totient_counts(self):
        for X in (100,1000,10000,30000):
            phi = nearmax_totients(X)
            for C in range(5):
                count = len(nearmax_witnesses(X,C,phi))
                self.assertLessEqual(count, wp07d_polylog_bound(X,C))
                self.assertGreaterEqual(wp07d_polylog_bound(X,C),1)
        self.assertLessEqual(wp07d_polylog_bound(100000,0),
                             4*(100000).bit_length()**2)

    def test_exact_polylog_endpoints_for_adjacent_integral_sums(self):
        for X,C in ((128,0),(512,1),(1024,2),(4096,3)):
            result = wp07d_receipt(X,C)
            self.assertEqual(result["full_series_status"],"OPEN")
            self.assertEqual(result["claim_boundary"],
                             "FINITE_CHECK_ONLY__EXACT_MANUSCRIPT_PROOF__NOT_MATHCERT")
            self.assertLessEqual(result["eligible_count"],
                                 int(result["exact_polylog_envelope"]))
            self.assertLessEqual(result["adjacent_integral_pairs"],
                                 wp07d_polylog_bound(3*X,C+2))

    def test_rational_comparator_has_even_stronger_finite_nonintegrality(self):
        # The *rational* sequence floor(n/2) has sum 2/3 and only
        # O_C(1) integral complete nearlog finite sums in dyadic blocks.
        x=Fraction(1,2)
        self.assertEqual(x*x*(1+x)/(1-x*x)**2, Fraction(2,3))
        for X,C in ((64,0),(256,1),(1024,2),(4096,3)):
            L=X.bit_length()-1-C
            modulus=1<<L
            actual=0
            for N in range(X,2*X):
                whole=sum((N+j)//2 << (L-j) for j in range(1,L+1))
                if whole % modulus == 0:
                    actual+=1
            self.assertLessEqual(actual,(1 << (C+1))+2)

    def test_resource_and_invalid_input_contracts(self):
        for args in ((1,0),(100,-1),(100,11)):
            with self.assertRaises(ValueError):
                wp07d_polylog_bound(*args)
        with self.assertRaises(ValueError):
            wp07d_odd_budget(1)
        with self.assertRaises(ValueError):
            wp07d_fermat_slots(0)
        with self.assertRaises(ValueError):
            wp07d_equality(0)
        with self.assertRaises(ValueError):
            wp07d_receipt(1,0)
        with self.assertRaises(ValueError):
            wp07d_prime_shape(9,0,nearmax_totients(15))



from experiments.erdos249_full_series_phase.overlog_phase_separation import (
    totients as overlog_totients,
    direct_totient as overlog_direct_totient,
    overlog_depth,
    centered as overlog_centered,
    finite_numerator as overlog_finite_numerator,
    rolling_numerators as overlog_rolling,
    rational_baseline_half as overlog_half,
    rational_baseline_three_quarters as overlog_three,
    rational_six_defect as overlog_six,
    rational_sum_half, rational_sum_three_quarters,
    rational_sum_six_defect, exact_phase_gaps,
    adjacent_phase_rigidity,
)


class OverlogTotientPhaseSeparationTests(unittest.TestCase):
    """WP08-A: finite hostile cross-checks for all-X manuscript theorems."""

    def test_totient_against_independent_coprime_oracle(self):
        values = overlog_totients(600)
        for n in range(1,601):
            self.assertEqual(values[n],overlog_direct_totient(n))
            self.assertTrue(1 <= values[n] <= n)

    def test_exact_overlog_depth_and_centered_modulus(self):
        for X in (64,65,127,128,129,255,256,511,512,1024):
            L=overlog_depth(X)
            Q=1<<L
            self.assertEqual(L,X.bit_length()+3)
            self.assertTrue(8*X < Q <= 16*X)
            self.assertLessEqual(L+1,X)
            self.assertLess(2*X+L,3*X)
            for z in (-Q-3,-Q//2,-1,0,1,Q//2,Q+3):
                r=overlog_centered(z,Q)
                self.assertTrue(-Q//2 <= r < Q//2)
                self.assertEqual((r-z)%Q,0)
        with self.assertRaises(ValueError):
            overlog_depth(63)

    def test_direct_vs_independent_rolling_full_integer_numerators(self):
        for X in (64,128,256):
            L=overlog_depth(X)
            phi=overlog_totients(2*X+L+1)
            roll=overlog_rolling(X,phi)
            self.assertEqual(len(roll),X+1)
            for N in range(X,2*X+1):
                direct=overlog_finite_numerator(N,L,phi)
                self.assertEqual(roll[N-X],direct)
                if N<2*X:
                    self.assertEqual(
                        roll[N-X+1],
                        2*roll[N-X]-(1<<L)*phi[N+1]+phi[N+L+1],
                    )

    def test_mean_ratio_endpoint_anti_concentration_pairwise(self):
        for X in (64,128,256,512,1024,4096):
            e=exact_phase_gaps(X)
            L,Q=e["L"],e["Q"]
            phi=overlog_totients(2*X+L+1)
            roll=overlog_rolling(X,phi)
            good=set(e["totient_intrinsic_phase_gap_starts"])
            endpoint=e["high_ratio_endpoint_indices"]
            self.assertGreater(len(endpoint),0)
            self.assertGreaterEqual(len(good)*2,len(endpoint))
            for n in endpoint:
                N=n-L-1
                r=overlog_centered(roll[N-X],Q)
                t=overlog_centered(roll[N-X+1],Q)
                self.assertGreaterEqual(max(6*abs(r),6*abs(t)),X)
                self.assertTrue(N in good or N+1 in good)
            self.assertGreaterEqual(len(good),int(X*0.08))

    def test_multiples_six_multiplicative_difference_large_phase(self):
        for X in (64,128,512,2048):
            e=exact_phase_gaps(X)
            L,Q=e["L"],e["Q"]
            phi=overlog_rolling(X,overlog_totients(2*X+L+1))
            half=overlog_rolling(X,overlog_half(2*X+L+1))
            good=set(e["totient_vs_half_phase_gap_starts"])
            multiple=e["multiple_six_endpoint_indices"]
            self.assertGreaterEqual(len(multiple),X//6-1)
            # Spacing of 6 forces disjoint adjacent two-start pairs.
            self.assertGreaterEqual(len(good),len(multiple))
            for n in multiple:
                N=n-L-1
                self.assertLessEqual(
                    overlog_totients(n)[n],n//3
                )
                r=overlog_centered(phi[N-X]-half[N-X],Q)
                t=overlog_centered(phi[N-X+1]-half[N-X+1],Q)
                self.assertGreaterEqual(max(18*abs(r),18*abs(t)),X)

    def test_hostile_rational_full_series_closed_forms(self):
        self.assertEqual(rational_sum_half(),Fraction(2,3))
        self.assertEqual(rational_sum_three_quarters(),Fraction(14,15))
        self.assertEqual(rational_sum_six_defect(),Fraction(2582,3969))
        x=Fraction(1,2)
        self.assertEqual(
            Fraction(3,4)*x/(1-x)**2-
            Fraction(1,4)*(3*x+2*x*x+x*x*x)/(1-x**4),
            Fraction(14,15),
        )
        self.assertEqual(
            Fraction(2,3)-x**6/(1-x**6)**2,
            Fraction(2582,3969),
        )
        for X in (64,128,512,1024):
            e=exact_phase_gaps(X)
            self.assertGreaterEqual(
                len(e["rational_three_quarters_phase_gap_starts"]),
                (X-1)//2,
            )
            self.assertGreaterEqual(
                len(e["rational_six_defect_phase_gap_starts"]),
                len(e["multiple_six_endpoint_indices"]),
            )

    def test_overlog_phase_rigidity_and_actual_difference(self):
        for X in (64,128,512,2048):
            L=overlog_depth(X)
            phi=overlog_totients(2*X+L+1)
            half=overlog_half(2*X+L+1)
            self.assertEqual(
                adjacent_phase_rigidity(X,phi,phi)["rigidity_violations"],0
            )
            out=adjacent_phase_rigidity(X,phi,half)
            self.assertEqual(out["rigidity_violations"],0)
            # On n divisible by six, phi(n) != floor(n/2).
            for n in range(X+L+1,2*X+L):
                if n%6==0:
                    self.assertNotEqual(phi[n],half[n])
            self.assertEqual(out["conjecture_status"],"OPEN")

    def test_bad_sources_fail_closed(self):
        with self.assertRaises(ValueError):
            overlog_totients(0)
        with self.assertRaises(ValueError):
            overlog_direct_totient(0)
        with self.assertRaises(ValueError):
            overlog_centered(6,9)
        with self.assertRaises(ValueError):
            overlog_finite_numerator(32,100,[0]*50)
        with self.assertRaises(ValueError):
            overlog_rolling(64,[0]*50)
        with self.assertRaises(ValueError):
            adjacent_phase_rigidity(64,[0]*50,[0]*50)
        L=overlog_depth(64)
        phi=overlog_totients(128+L+1)
        bad=list(phi)
        bad[65]=-5
        with self.assertRaises(ValueError):
            adjacent_phase_rigidity(64,bad,phi)


    def test_exact_finite_prime_euler_coefficients_and_rational_sums(self):
        from experiments.erdos249_full_series_phase.overlog_phase_separation import (
            prime_euler_coefficients, finite_prime_rational_sum,
            finite_prime_weight,
        )
        self.assertEqual(finite_prime_rational_sum(()),Fraction(2))
        self.assertEqual(finite_prime_rational_sum((2,)),Fraction(14,9))
        for ps in ((),(2,),(2,3),(2,3,5),(2,3,5,7)):
            a=prime_euler_coefficients(1000,ps)
            phi=overlog_totients(1000)
            self.assertEqual(a[0],0)
            weight=finite_prime_weight(ps)
            for n in range(1,1001):
                independent=Fraction(n)
                for p in ps:
                    if n%p==0:
                        independent*=Fraction(p-1,p)
                self.assertEqual(a[n],independent.numerator)
                self.assertEqual(independent.denominator,1)
                self.assertGreaterEqual(a[n],phi[n])
                self.assertGreaterEqual(Fraction(a[n],n),weight)
            result=finite_prime_rational_sum(ps)
            self.assertGreater(result,0)
            # An exact rational lower prefix, not a floating approximation.
            prefix=sum((Fraction(a[n],1<<n) for n in range(1,100)),
                       Fraction())
            self.assertGreater(result,prefix)

    def test_missing_prime_escapes_at_many_independent_supports(self):
        from experiments.erdos249_full_series_phase.overlog_phase_separation import (
            prime_escape_phase_gaps,
        )
        for X,ps,p in (
            (128,(),2),
            (128,(2,),3),
            (512,(2,3),5),
            (1024,(2,3,5),7),
            (2048,(2,3,5,7),11),
        ):
            result=prime_escape_phase_gaps(X,ps,p)
            self.assertTrue(result["all_prime_escape_implications"])
            self.assertGreaterEqual(
                result["phase_separated_starts"],
                result["omitted_prime_endpoints"],
            )
            self.assertGreaterEqual(
                result["omitted_prime_endpoints"],
                (X-1)//p,
            )
            self.assertEqual(result["actual_full_totient_sum_status"],"OPEN")

    def test_bad_finite_prime_sets_and_omitted_prime_fail_closed(self):
        from experiments.erdos249_full_series_phase.overlog_phase_separation import (
            prime_euler_coefficients, finite_prime_rational_sum,
            prime_escape_phase_gaps, finite_prime_weight,
        )
        with self.assertRaises(ValueError):
            prime_euler_coefficients(50,(2,2))
        with self.assertRaises(ValueError):
            finite_prime_weight((4,))
        with self.assertRaises(ValueError):
            finite_prime_rational_sum((1,))
        with self.assertRaises(ValueError):
            finite_prime_rational_sum((2,3,5,7,11))
        with self.assertRaises(ValueError):
            prime_euler_coefficients(0,(2,))
        with self.assertRaises(ValueError):
            prime_escape_phase_gaps(64,(2,3),2)
        with self.assertRaises(ValueError):
            prime_escape_phase_gaps(64,(2,),9)



from experiments.erdos249_full_series_phase.moving_prime_escape import (
    primes_to as wp08b_primes,
    finite_prime_euler_sieve as wp08b_euler,
    unique_large_prime_sieve as wp08b_large,
    moving_prime_receipt as wp08b_receipt,
    rational_finite_patch as wp08b_rational_patch,
)


class MovingPrimeEscapeTests(unittest.TestCase):
    """WP08-B exact hostile arithmetic; no numerical asymptotic claim."""

    def test_independent_small_prime_support_oracle(self):
        from math import gcd
        self.assertEqual(wp08b_primes(1),())
        self.assertEqual(wp08b_primes(32),
                         (2,3,5,7,11,13,17,19,23,29,31))
        for y in (2,5,11,29):
            values=wp08b_euler(350,y)
            ps=wp08b_primes(y)
            for n in range(1,351):
                smallfactor=math.prod(p for p in ps if n%p==0)
                independent=sum(gcd(k,smallfactor)==1
                                for k in range(1,n+1))
                self.assertEqual(values[n],independent)
                self.assertLessEqual(values[n],n)

    def test_exact_unique_large_prime_pulse_vs_totient(self):
        for X,y in ((1024,64),(4096,128),(16384,256)):
            L=overlog_depth(X)
            limit=2*X+L+1
            phi=overlog_totients(limit)
            g=wp08b_euler(limit,y)
            factors=wp08b_large(limit,y)
            self.assertGreater(y*y,3*X)
            for n in range(1,limit+1):
                p=factors[n]
                self.assertEqual(g[n]-phi[n],
                                 phi[n//p] if p else 0)
                if p:
                    self.assertGreater(p,y)
                    self.assertLess(n//p,y)
                    self.assertEqual(n%p,0)

    def test_exact_all_prime_phase_certificate_and_count(self):
        for X,y in ((1024,64),(4096,128),(16384,256)):
            r=wp08b_receipt(X,y)
            endpoints=r["good_prime_endpoints"]
            self.assertGreater(len(endpoints),0)
            self.assertGreaterEqual(len(r["strong_gap_starts"])*2,
                                    len(endpoints))
            self.assertGreaterEqual(len(r["theorem_gap_starts"]),
                                    len(r["strong_gap_starts"]))
            self.assertEqual(r["theorem_gap_threshold"],
                             f"1/{192*y}")
            self.assertEqual(r["full_series_irrationality"],"OPEN")
            self.assertEqual(len(set(r["all_prime_endpoints"])),
                             len(r["all_prime_endpoints"]))
            self.assertEqual(len(set(n for n,p,m in endpoints)),
                             len(endpoints))

    def test_all_missing_prime_pulses_are_genuinely_aggregated(self):
        for X,y in ((1024,64),(4096,128),(16384,256)):
            r=wp08b_receipt(X,y)
            selected=r["good_prime_endpoints"]
            by_prime={}
            for n,p,m in selected:
                by_prime[p]=by_prime.get(p,0)+1
                self.assertTrue(y<p<=2*y)
                self.assertEqual(n,p*m)
            self.assertGreater(len(by_prime),1)
            self.assertGreater(sum(by_prime.values()),max(by_prime.values()))
            self.assertEqual(sum(by_prime.values()),len(selected))

    def test_independent_direct_finite_sum_matches_rolling_phase(self):
        from experiments.erdos249_full_series_phase.overlog_phase_separation import (
            finite_numerator, rolling_numerators, centered,
        )
        X,y=1024,64
        L=overlog_depth(X)
        Q=1<<L
        limit=2*X+L+1
        p=overlog_totients(limit)
        g=wp08b_euler(limit,y)
        delta=[p[n]-g[n] for n in range(limit+1)]
        rolled=rolling_numerators(X,delta)
        r=wp08b_receipt(X,y)
        strong=set(r["strong_gap_starts"])
        for N in list(range(X,X+24))+list(range(2*X-24,2*X)):
            direct=finite_numerator(N,L,p)-finite_numerator(N,L,g)
            self.assertEqual(rolled[N-X],direct)
            v=centered(direct,Q)
            self.assertEqual(N in strong,12*y*abs(v)>=X)
            self.assertEqual((direct-v)%Q,0)

    def test_rational_finite_patch_cannot_certify_irrationality(self):
        from experiments.erdos249_full_series_phase.overlog_phase_separation import (
            finite_numerator,
        )
        for X,y in ((128,32),(1024,64)):
            patched,phi=wp08b_rational_patch(X,y)
            L=overlog_depth(X)
            gy=wp08b_euler(3*X-1,y)
            self.assertTrue(any(patched[n]!=gy[n]
                                for n in range(X+1,2*X+L+1)))
            for N in range(X,2*X):
                self.assertEqual(finite_numerator(N,L,patched),
                                 finite_numerator(N,L,phi))
            # The full patched infinite sum is rational because it is
            # a finite dyadic modification of the rational full g_y sum.
            finite_correction=sum(
                (Fraction(patched[n]-gy[n],1<<n)
                 for n in range(X+1,2*X+L+1)),
                Fraction(),
            )
            self.assertLessEqual(finite_correction,0)
            self.assertIsInstance(finite_correction,Fraction)

    def test_malformed_and_duplicate_support_fail_closed(self):
        with self.assertRaises(ValueError):
            wp08b_euler(0,3)
        with self.assertRaises(ValueError):
            wp08b_euler(50,1)
        with self.assertRaises(ValueError):
            wp08b_large(50,3)
        with self.assertRaises(ValueError):
            wp08b_large(0,100)
        with self.assertRaises(ValueError):
            wp08b_receipt(63,64)
        with self.assertRaises(ValueError):
            wp08b_receipt(4096,64)
        with self.assertRaises(ValueError):
            wp08b_rational_patch(4096,64)



from experiments.erdos249_full_series_phase.shifted_first_harmonic import (
    shift_modulus as wp09a_modulus,
    cook_minimal_depth as wp09a_depth,
    signed_shift_numerators as wp09a_rolling,
    direct_shift_numerator as wp09a_direct,
    signed_shift_receipt as wp09a_receipt,
    rational_shift_control as wp09a_control,
    rational_shift_control_sum as wp09a_control_sum,
)


class ShiftedFirstHarmonicTests(unittest.TestCase):
    """WP09-A: exact hostile tests of the actual Cook shifted D_h phase."""

    def test_arithmetic_modulus_independent_exact_ratio(self):
        for h in (1,2,3,6):
            M,eta,primes=wp09a_modulus(h)
            self.assertEqual(math.gcd(M,h),1)
            self.assertTrue(M>=2 and eta<=Fraction(29,50))
            self.assertEqual(M,math.prod(primes))
            self.assertEqual(eta,math.prod(
                (Fraction(p-1,p) for p in primes),start=Fraction(1)
            ))
        self.assertEqual(wp09a_modulus(1)[:2],(2,Fraction(1,2)))
        self.assertEqual(wp09a_modulus(2)[:2],(15,Fraction(8,15)))
        self.assertEqual(wp09a_modulus(6)[:2],(5005,Fraction(576,1001)))

    def test_minimal_cook_size_condition_and_upper_ratio(self):
        for h,X in ((1,64),(1,128),(2,512),(3,1024),(6,65536)):
            L=wp09a_depth(X,h)
            self.assertTrue((1<<L)>=16*(2*X+h+L+2))
            self.assertTrue((1<<(L-1))<16*(2*X+h+L+1))
            self.assertLessEqual(1<<L,96*X)
            self.assertTrue(h+L+1<=X)

    def test_rolling_matches_independent_direct_cook_D(self):
        for h,X in ((1,64),(2,128),(3,256),(6,512)):
            L=wp09a_depth(X,h)
            Q=1<<L
            phi=overlog_totients(2*X+L+h+1)
            rolled=wp09a_rolling(X,h,L,phi)
            self.assertEqual(len(rolled),X+1)
            for N in range(X,2*X+1):
                self.assertEqual(rolled[N-X],wp09a_direct(N,h,L,phi))
                if N<2*X:
                    d=phi[N+h+L+1]-phi[N+L+1]
                    self.assertEqual(
                        (rolled[N-X+1]-2*rolled[N-X]-d)%Q,0
                    )

    def test_all_signed_contrast_endpoints_force_gaps(self):
        for h,X in ((1,256),(2,1024),(3,4096),(6,65536)):
            r=wp09a_receipt(X,h)
            self.assertGreater(len(r["negative_endpoints"]),0)
            self.assertGreater(len(r["positive_endpoints"]),0)
            self.assertTrue(
                len(r["negative_endpoints"])+len(r["positive_endpoints"])
                <=2*r["strong_gap_starts"]
            )
            self.assertGreaterEqual(
                r["fixed_fraction_gap_starts"],r["strong_gap_starts"]
            )
            self.assertTrue(r["M"]>=2)
            self.assertEqual(
                r["original_totient_irrationality"],"OPEN"
            )
            self.assertEqual(r["cook_required_10_percent_saving"],"OPEN")

    def test_harmonic_saving_proof_has_exact_positive_budget(self):
        # Finite checks test the exact fractional-distance implication.
        # The global density and all-X harmonic estimate are proved
        # independently from the conditional totient mean in the source.
        for h,X in ((1,256),(2,1024),(6,65536)):
            r=wp09a_receipt(X,h)
            count=r["fixed_fraction_gap_starts"]
            self.assertGreater(count,0)
            # 1-cos(2*pi*t) >= 8*t^2 for 0<=t<=1/2.
            # Therefore the actual first harmonic has the exact
            # mathematical upper bound X - 8*count/28800^2.
            bound=Fraction(X)-Fraction(8*count,28800**2)
            self.assertLess(bound,X)
            self.assertGreater(bound,0)

    def test_hostile_rational_full_sum_with_two_signed_shifts(self):
        for h,M in ((1,3),(2,3),(3,5),(6,7)):
            total=wp09a_control_sum(h,M)
            self.assertTrue(isinstance(total,Fraction) and total>0)
            prefix=sum((Fraction(wp09a_control(n,h,M),1<<n)
                        for n in range(1,120)),Fraction())
            self.assertLess(prefix,total)
            self.assertLess(total-prefix,Fraction(125,1<<119))
            for n in range(2*M,100, M):
                self.assertEqual(wp09a_control(n,h,M),0)
                self.assertEqual(wp09a_control(n+h,h,M),n+h)
                self.assertEqual(wp09a_control(n-h,h,M),n-h)
                self.assertEqual(
                    wp09a_control(n+h,h,M)-wp09a_control(n,h,M),
                    n+h,
                )
                self.assertEqual(
                    wp09a_control(n,h,M)-wp09a_control(n-h,h,M),
                    -(n-h),
                )

    def test_guarded_source_contracts(self):
        with self.assertRaises(ValueError):
            wp09a_modulus(0)
        with self.assertRaises(ValueError):
            wp09a_modulus(6,max_product=20)
        with self.assertRaises(ValueError):
            wp09a_depth(63,2)
        with self.assertRaises(ValueError):
            wp09a_depth(64,0)
        with self.assertRaises(ValueError):
            wp09a_rolling(64,1,10,[0]*10)
        with self.assertRaises(ValueError):
            wp09a_direct(64,1,10,[0]*10)
        with self.assertRaises(ValueError):
            wp09a_receipt(64,20)
        with self.assertRaises(ValueError):
            wp09a_control(5,1,2)
        with self.assertRaises(ValueError):
            wp09a_control_sum(1,65)


    def test_exact_all_shift_cocycle_and_marginal_phase_obstruction(self):
        X=128
        L=wp09a_depth(X,6)
        phi=overlog_totients(2*X+L+12)
        for N in (X,X+1,X+19,2*X-2):
            for h in (1,2,3,4):
                for k in (1,2,3):
                    left=wp09a_direct(N,h+k,L,phi)
                    right=(wp09a_direct(N,h,L,phi)
                           +wp09a_direct(N+h,k,L,phi))
                    self.assertEqual(left,right)
                    self.assertEqual(
                        left,
                        sum(wp09a_direct(N+j,1,L,phi)
                            for j in range(h+k)),
                    )
        # Abstract logical counterexample: zero one-phase mean,
        # but every adjacent product equals +1 exactly.
        u=[(1j if n%2==0 else -1j) for n in range(100)]
        self.assertEqual(sum(u,0j),0j)
        self.assertTrue(all(u[n]*u[n+1]==1 for n in range(99)))



from experiments.erdos249_full_series_phase.shifted_moment_energy import (
    prime_list as wp09b_primes,
    finite_euler_moments as wp09b_euler,
    exact_finite_crt_period as wp09b_crt,
    first_omitted_prime as wp09b_omitted,
    euler_moment_bounds as wp09b_bounds,
    exact_phase_energy as wp09b_energy,
    rational_hostile_phase_energy as wp09b_hostile,
)


class ShiftedSecondMomentEnergyTests(unittest.TestCase):
    """WP09-B exact CRT correlation and Cook-phase energy hostiles."""

    def test_prime_support_and_local_euler_products(self):
        self.assertEqual(wp09b_primes(2),(2,))
        self.assertEqual(
            wp09b_primes(31),(2,3,5,7,11,13,17,19,23,29,31)
        )
        a=wp09b_euler(1,(2,3))
        self.assertEqual(a["A_f_squared"],
                         Fraction(5,8)*Fraction(22,27))
        self.assertEqual(a["B_shifted_correlation"],
                         Fraction(1,2)*Fraction(7,9))
        self.assertEqual(
            a["V_squared_difference"],
            2*(a["A_f_squared"]-a["B_shifted_correlation"])
        )
        self.assertEqual(
            wp09b_euler(30,(2,3,5))["V_squared_difference"],
            0,
        )
        self.assertEqual(
            wp09b_euler(1,(2,3,5))["Bstar_baseline"],
            Fraction(1,2)*Fraction(7,9)*Fraction(23,25),
        )

    def test_independent_exact_full_period_crt_correlations(self):
        for ps in ((2,3),(2,3,5),(2,3,5,7)):
            for h in (1,2,3,6,30,210):
                got=wp09b_crt(h,ps)
                expected=wp09b_euler(h,ps)
                self.assertEqual(got["A_exact_period"],
                                 expected["A_f_squared"])
                self.assertEqual(got["B_exact_period"],
                                 expected["B_shifted_correlation"])
                self.assertEqual(got["V_exact_period"],
                                 expected["V_squared_difference"])
                self.assertGreaterEqual(got["V_exact_period"],0)
                self.assertEqual(got["period"],math.prod(ps))

    def test_rigorous_infinite_euler_tail_envelopes(self):
        for h in (1,2,3,6,30,210,2310):
            p=wp09b_omitted(h)
            self.assertEqual(h%p!=0,True)
            for k in range(2,p):
                if all(k%d for d in range(2,math.isqrt(k)+1)):
                    self.assertEqual(h%k,0)
            low=wp09b_bounds(h,31)
            high=wp09b_bounds(h,127)
            trunc=wp09b_euler(h,wp09b_primes(257))
            v=trunc["V_squared_difference"]
            self.assertTrue(
                low["lower_V_from_tail"] <= v <=
                low["upper_V_from_tail"]
            )
            self.assertTrue(
                high["lower_V_from_tail"] <= v <=
                high["upper_V_from_tail"]
            )
            self.assertGreater(
                high["upper_V_from_tail"],
                high["unconditional_strict_V_lower"]
            )
            self.assertEqual(
                high["unconditional_strict_V_lower"],
                Fraction(1,9*p**3),
            )
            self.assertEqual(
                high["rigorous_harmonic_saving_lower"],
                Fraction(1,22500*p**3),
            )

    def test_exact_all_shift_phase_energy_transfer(self):
        for X,h in ((512,1),(1024,2),(4096,3),(8192,6)):
            got=wp09b_energy(X,h)
            self.assertEqual(got["source"],"ACTUAL_EULER_TOTIENT")
            self.assertLessEqual(
                got["arithmetic_squared_energy"],
                9*got["centered_residual_squared_energy"],
            )
            self.assertGreater(got["arithmetic_squared_energy"],0)
            self.assertGreater(got["rigorous_harmonic_deficit_lower"],0)
            self.assertEqual(got["original_irrationality"],"OPEN")
            self.assertEqual(got["single_step_Cook_ten_percent"],
                             "NOT_CERTIFIED")
            self.assertGreater(got["Q"],32*X)

    def test_cook_energy_differences_vs_independent_direct_oracle(self):
        for h,X in ((1,128),(2,256),(3,512)):
            L=wp09a_depth(X,h)
            Q=1<<L
            phi=overlog_totients(2*X+L+h+1)
            got=wp09b_energy(X,h)
            self.assertEqual(got["L"],L)
            self.assertEqual(got["Q"],Q)
            r2=sum(
                overlog_centered(
                    wp09a_direct(N,h,L,phi),Q
                )**2
                for N in range(X,2*X)
            )
            d2=sum(
                (phi[n+h]-phi[n])**2
                for n in range(X+L+1,2*X+L)
            )
            self.assertEqual(
                got["centered_residual_squared_energy"],r2
            )
            self.assertEqual(got["arithmetic_squared_energy"],d2)
            self.assertEqual(
                got["rigorous_harmonic_deficit_lower"],
                Fraction(8*d2,9*Q*Q),
            )

    def test_hostile_rational_series_still_has_shifted_energy(self):
        for X,h,M in ((512,1,3),(1024,2,3),(1024,6,7)):
            got=wp09b_hostile(X,h,M)
            self.assertEqual(got["source"],"EXPLICIT_INTEGER_COMPARATOR")
            self.assertGreater(got["arithmetic_squared_energy"],0)
            self.assertGreater(got["rigorous_harmonic_deficit_lower"],0)
            # WP09-A independently established the FULL series is rational.
            self.assertIsInstance(wp09a_control_sum(h,M),Fraction)
            self.assertEqual(got["original_irrationality"],"OPEN")

    def test_methodological_10_percent_ceiling_exact_finite(self):
        for X,h in ((512,1),(1024,2),(4096,6)):
            got=wp09b_energy(X,h)
            L=got["L"]
            Q=got["Q"]
            cap=Fraction(8*(X-1)*(2*X+L+h)**2,9*Q**2)
            self.assertLessEqual(
                got["rigorous_harmonic_deficit_lower"],cap
            )
            self.assertLess(cap,Fraction(X,10))
            self.assertLessEqual(
                got["arithmetic_squared_energy"],
                (X-1)*(2*X+L+h)**2,
            )

    def test_truncation_and_source_fail_closed(self):
        with self.assertRaises(ValueError):
            wp09b_primes(1)
        with self.assertRaises(ValueError):
            wp09b_euler(0,(2,3))
        with self.assertRaises(ValueError):
            wp09b_euler(1,(2,2,3))
        with self.assertRaises(ValueError):
            wp09b_euler(1,(4,))
        with self.assertRaises(ValueError):
            wp09b_crt(1,(2,3,5,7),max_period=100)
        with self.assertRaises(ValueError):
            wp09b_bounds(0,127)
        with self.assertRaises(ValueError):
            wp09b_bounds(1,2)
        with self.assertRaises(ValueError):
            wp09b_bounds(1,4097)
        with self.assertRaises(ValueError):
            wp09b_omitted(0)
        with self.assertRaises(ValueError):
            wp09b_energy(63,1)
        with self.assertRaises(ValueError):
            wp09b_energy(512,0)
        with self.assertRaises(ValueError):
            wp09b_energy(512,1,coefficients=[0]*10)
        with self.assertRaises(ValueError):
            wp09b_hostile(512,1,2)


from experiments.erdos249_full_series_phase.joint_local_prime_law import (
    primes_through as wp09c_primes,
    profile as wp09c_profile,
    exact_moment as wp09c_moment,
    characteristic as wp09c_characteristic,
    effective_error as wp09c_error,
    infinite_model_truncation_bound as wp09c_tail,
    actual_local_characteristic as wp09c_actual,
)


class JointLocalPrimeLawTests(unittest.TestCase):
    """WP09-C: exact CRT oracle, effective local-law and promotion firewall."""

    def test_independent_crt_shift_bundle_oracle(self):
        terms = ((2, 1, 0), (-1, 2, 1), (1, 5, 3))
        for y in (2, 3, 5, 7):
            ps = wp09c_primes(y)
            P, ds = wp09c_profile(y, terms)
            self.assertEqual(P, math.prod(ps))
            def oracle(n):
                return math.prod(
                    (Fraction(p - 1, p) for p in ps if n % p == 0),
                    start=Fraction(1))
            self.assertEqual(
                ds, tuple(sum(
                    (w * (oracle(a + u) - oracle(a + v))
                     for w, u, v in terms), Fraction())
                    for a in range(P)))
            self.assertEqual(
                wp09c_moment(y, terms, 2),
                sum((d*d for d in ds), Fraction()) / P)

    def test_finite_single_shift_moment_matches_wp09b_euler(self):
        from experiments.erdos249_full_series_phase.shifted_moment_energy import (
            finite_euler_moments,
        )
        for h in (1, 2, 3, 6):
            for y in (3, 5, 7):
                ps = wp09c_primes(y)
                expected = finite_euler_moments(h, ps)[
                    "V_squared_difference"]
                self.assertEqual(
                    wp09c_moment(y, ((1, h, 0),), 2), expected)

    def test_single_shift_antipodal_crt_symmetry(self):
        for h in (1, 2, 3, 5, 6):
            P, ds = wp09c_profile(7, ((1, h, 0),))
            for a in range(P):
                self.assertEqual(ds[a], -ds[(-a-h) % P])
            self.assertEqual(sum(ds, Fraction()), 0)

    def test_nontrivial_joint_characteristic_finite_formula(self):
        terms = ((1, 1, 0), (-2, 3, 1))
        P, ds = wp09c_profile(7, terms)
        from cmath import exp
        from math import sin, pi
        for rho in (32.0, 45.0, 128.0):
            direct = 0j
            for d in ds:
                theta = pi * float(d) / rho
                direct += exp(3j * theta) * (
                    sin(theta)/theta if theta else 1)
            self.assertLess(
                abs(wp09c_characteristic(7, terms, rho)-direct/P),
                2e-13)
            self.assertLessEqual(abs(wp09c_characteristic(
                7, terms, rho)), 1 + 1e-12)

    def test_actual_totients_vs_effective_uniform_error_envelope(self):
        from experiments.erdos249_full_series_phase.overlog_phase_separation import (
            totients,
        )
        X = 4096
        y = 7
        for terms in (((1, 1, 0),), ((1, 2, 0), (-1, 3, 1))):
            H = max(max(u, v) for _, u, v in terms)
            phi = totients(2*X + H + 1)
            Q = 64*X
            actual = wp09c_actual(X, Q, terms, phi)
            modeled = wp09c_characteristic(y, terms, Q/X)
            bound = wp09c_error(X, Q, y, terms)
            self.assertGreater(bound, 0)
            self.assertLessEqual(abs(actual-modeled), bound + 1e-12)

    def test_truncation_bound_and_real_shift_characteristic(self):
        for h in (1, 2, 3):
            terms = ((1, h, 0),)
            c7 = wp09c_characteristic(7, terms, 32.0)
            c11 = wp09c_characteristic(11, terms, 32.0)
            self.assertLess(abs(c7-c11), wp09c_tail(7, terms, 32.0))
            self.assertLess(abs(c11.imag), 1e-12)
            self.assertGreater(1-c11.real, 0)

    def test_does_not_replace_full_cook_phase(self):
        from experiments.erdos249_full_series_phase.overlog_phase_separation import (
            totients,
        )
        X, h = 64, 1
        L = wp09a_depth(X, h)
        Q = 1 << L
        phi = totients(2*X + L + h + 3)
        differences = []
        for N in range(X, 2*X):
            cook = wp09a_direct(N, h, L, phi)
            local = phi[N+L+h+1] - phi[N+L+1]
            differences.append((cook-local) % Q)
        self.assertTrue(any(z != 0 for z in differences))

    def test_malformed_period_and_triples_fail_closed(self):
        terms = ((1, 1, 0),)
        for bad in ((), ((0, 1, 0),), ((1, -1, 0),),
                    ((True, 1, 0),), [(1, 1, 0)]):
            with self.assertRaises(ValueError):
                wp09c_profile(5, bad)
        with self.assertRaises(ValueError):
            wp09c_primes(1)
        with self.assertRaises(ValueError):
            wp09c_profile(11, terms, max_period=100)
        with self.assertRaises(ValueError):
            wp09c_moment(5, terms, -1)
        with self.assertRaises(ValueError):
            wp09c_characteristic(5, terms, 31.0)
        with self.assertRaises(ValueError):
            wp09c_actual(64, 2047, terms, [0] * 200)
        with self.assertRaises(ValueError):
            wp09c_error(64, 2048, 11, terms, max_period=100)


from experiments.erdos249_full_series_phase.joint_covariance_gap import (
    signature as wp09d_signature,
    signature_norms as wp09d_norms,
    first_separating_prime as wp09d_prime,
    conditional_projection as wp09d_projection,
    finite_product_covariance as wp09d_product,
    finite_cos_gap_bound as wp09d_cos_gap,
    actual_phase_energy as wp09d_actual,
)
from experiments.erdos249_full_series_phase.joint_local_prime_law import (
    profile as wp09d_profile,
)


class JointCovarianceGapTests(unittest.TestCase):
    """WP09-D: exact all-signature arithmetic, phases, hostile controls."""

    def test_signed_offset_canonicalization_and_separating_prime(self):
        cases = [
            (((1, 1, 0),), ((0, -1), (1, 1)), 2),
            (((2, 3, 1), (-1, 1, 0)),
             ((0, 1), (1, -3), (3, 2)), 5),
            (((1, 4, 2), (-1, 2, 0)),
             ((0, 1), (2, -2), (4, 1)), 5),
        ]
        for terms, expected, p in cases:
            self.assertEqual(wp09d_signature(terms), expected)
            self.assertEqual(wp09d_prime(terms), p)
            n = wp09d_norms(terms)
            self.assertEqual(n["squared"], sum(c*c for _, c in expected))
            self.assertEqual(n["B"], sum(abs(c) for _, c in expected))
            self.assertEqual(sum(c for _, c in expected), 0)

    def test_independent_prime_conditional_crt_oracle(self):
        for terms, y in (
            (((1, 1, 0),), 3),
            (((1, 2, 0), (-1, 3, 1)), 7),
            (((1, 4, 2), (-1, 2, 0)), 7),
        ):
            r = wp09d_projection(terms, y)
            P, ds = wp09d_profile(y, terms)
            p = r["separating_prime"]
            self.assertEqual(P, r["period"])
            self.assertEqual(r["exact_variance"],
                             sum((v*v for v in ds), Fraction()) / P)
            self.assertEqual(r["conditional_means"], tuple(
                sum((ds[k] for k in range(a, P, p)), Fraction())/(P//p)
                for a in range(p)))
            self.assertEqual(
                r["conditional_energy"],
                sum((v*v for v in r["conditional_means"]), Fraction())/p)
            self.assertGreaterEqual(
                r["exact_variance"], r["conditional_energy"])
            self.assertGreaterEqual(
                r["conditional_energy"], r["simple_uniform_lower"])

    def test_strict_positive_higher_rank_and_exact_sample(self):
        signature = ((1, 3, 0), (2, 3, 1))
        r = wp09d_projection(signature, 7)
        self.assertEqual(r["separating_prime"], 5)
        self.assertGreater(r["conditional_energy"], 0)
        self.assertGreater(r["exact_variance"], 0)
        self.assertEqual(r["exact_variance"], Fraction(9559, 22050))
        self.assertEqual(r["conditional_energy"], Fraction(2048, 42875))

    def test_independent_finite_euler_pair_vs_crt(self):
        for terms in (
            ((1, 1, 0),),
            ((1, 3, 0), (2, 3, 1)),
            ((1, 4, 2), (-1, 2, 0)),
        ):
            for y in (5, 7):
                direct_P, direct_ds = wp09d_profile(y, terms)
                exact = sum((z*z for z in direct_ds),
                            Fraction()) / direct_P
                self.assertEqual(wp09d_product(terms, y), exact)

    def test_quantitative_local_phase_gap_all_signature(self):
        for terms, y, rho in (
            (((1, 1, 0),), 5, 32),
            (((1, 3, 0), (2, 3, 1)), 7, 64),
            (((1, 4, 2), (-1, 2, 0)), 7, 48),
        ):
            gap = wp09d_cos_gap(terms, y, rho)
            r = wp09d_projection(terms, y)
            self.assertEqual(gap,
                             Fraction(56, 3*rho*rho)*r["exact_variance"])
            self.assertGreaterEqual(gap,
                                    Fraction(56, 3*rho*rho) *
                                    r["simple_uniform_lower"])
            self.assertGreater(gap, 0)
            self.assertLess(gap, 2)

    def test_actual_totient_exact_phase_energy_bound(self):
        for terms, X in (
            (((1, 1, 0),), 128),
            (((1, 3, 0), (2, 3, 1)), 256),
            (((1, 4, 2), (-1, 2, 0)), 512),
        ):
            B = wp09d_norms(terms)["B"]
            Q = max(32, 6*B)*X
            r = wp09d_actual(X, Q, terms)
            self.assertGreater(r["local_difference_energy"], 0)
            self.assertGreater(r["exact_phase_gap_lower"], 0)
            self.assertGreaterEqual(
                r["numeric_actual_phase_gap"] + 1e-12,
                float(r["exact_phase_gap_lower"]))
            self.assertFalse(r["full_cook_harmonic"])
            self.assertEqual(r["irrationality_status"], "OPEN")

    def test_hostile_signature_and_modulus_rejection(self):
        bad = (
            (), ((0, 1, 0),),
            ((1, 3, 1), (1, 1, 3)), ((1, 2, 2),),
            ((True, 1, 0),), ((1, -1, 0),),
            [(1, 1, 0)],
        )
        for terms in bad:
            with self.assertRaises(ValueError):
                wp09d_signature(terms)
        with self.assertRaises(ValueError):
            wp09d_projection(((1, 3, 0),), 3)
        with self.assertRaises(ValueError):
            wp09d_projection(((1, 1, 0),), 11, max_period=200)
        with self.assertRaises(ValueError):
            wp09d_cos_gap(((1, 3, 0), (2, 3, 1)), 7, 20)
        with self.assertRaises(ValueError):
            wp09d_actual(128, 100, ((1, 1, 0),))

    def test_rational_full_series_can_have_local_phase_variance(self):
        # Exact generating function:
        # sum floor(n/2) * x**n = x²(1+x)/(1-x²)².
        x = Fraction(1, 2)
        rational_total = x*x*(1+x)/(1-x*x)**2
        self.assertEqual(rational_total, Fraction(2, 3))
        diffs = tuple((n+1)//2-n//2 for n in range(128, 256))
        self.assertEqual(set(diffs), {0, 1})
        self.assertEqual(sum(diffs), 64)
        self.assertEqual(sum((2*v-1)**2 for v in diffs), 128)
        # The strict positive finite local gap is not enough to
        # infer an irrational full sum for a generic coefficient model.
        Q = 4096
        from cmath import exp
        from math import pi
        self.assertGreater(
            1 - sum(exp(2j*pi*v/Q).real for v in diffs)/len(diffs),
            0)


from experiments.erdos249_full_series_phase.full_window_prime_projection import (
    fixed_separating_prime as wp09e_prime,
    cook_minimal_depth as wp09e_depth,
    dyadic_residue_weights as wp09e_alias,
    exact_finite_crt_projection as wp09e_crt,
    projection_certificate as wp09e_certificate,
    cook_numerator_direct as wp09e_direct,
    cook_numerators_rolling as wp09e_rolling,
    exact_actual_window_energy as wp09e_energy,
)


class FullWindowPrimeProjectionTests(unittest.TestCase):
    """WP09-E: full actual Cook logarithmic window and exact fixed-prime CRT."""

    def test_fixed_prime_nondivisor_depends_on_h_not_L(self):
        self.assertEqual(
            [wp09e_prime(h) for h in (1, 2, 3, 4, 6, 30, 210)],
            [2, 3, 2, 3, 5, 7, 11])
        for h in (1, 2, 6, 30):
            p = wp09e_prime(h)
            for L in (1, 2, 7, 30, 96):
                a = wp09e_alias(h, L)
                self.assertEqual(a["p"], p)
                self.assertEqual(a["Q"], 1 << L)
                self.assertEqual(sum(a["t_numerators"]), 0)
                self.assertGreaterEqual(
                    6*a["t_numerators"][a["positive_class"]], a["Q"])
                self.assertGreaterEqual(
                    -6*a["t_numerators"][a["negative_class"]], a["Q"])
                self.assertNotEqual(
                    a["positive_class"], a["negative_class"])

    def test_exact_aliased_residue_vectors_and_l2_lower(self):
        self.assertEqual(wp09e_alias(1, 4)["q_numerators"], (5, 10))
        self.assertEqual(wp09e_alias(1, 4)["t_numerators"], (5, -5))
        self.assertEqual(wp09e_alias(2, 4)["q_numerators"], (2, 9, 4))
        self.assertEqual(wp09e_alias(2, 4)["t_numerators"], (7, -5, -2))
        for h, L in ((1, 7), (2, 9), (6, 11), (30, 50)):
            a = wp09e_alias(h, L)
            self.assertGreaterEqual(
                18*a["alias_l2_numerator"], a["Q"]**2)

    def test_independent_finite_crt_overlapping_shifts(self):
        from experiments.erdos249_full_series_phase.joint_local_prime_law import primes_through
        from math import prod
        cases = ((1, 4, 3), (2, 5, 5), (6, 10, 7), (30, 12, 7))
        for h, L, y in cases:
            r = wp09e_crt(h, L, y)
            p, P = r["p"], r["period"]
            self.assertEqual(P, prod(primes_through(y)))
            self.assertLess(p, L+h)  # Genuine overlapping prime residues
            self.assertEqual(r["observed"], r["predicted"])
            self.assertEqual(sum(r["observed"], Fraction()), 0)
            self.assertGreater(r["l2_mean_projection"], 0)
            self.assertGreaterEqual(
                18 * sum(k*k for k in r["fixed_prime_alias_vector"]),
                (1 << L)**2)

    def test_real_full_window_decomposition_exact_fraction(self):
        from experiments.erdos249_full_series_phase.fourier_probe import totients
        for h, L in ((1, 4), (2, 6), (6, 9)):
            phi = totients(150)
            ratio = [Fraction(0) if n == 0
                     else Fraction(phi[n], n) for n in range(len(phi))]
            for N in (50, 57, 63):
                G = sum((Fraction(1, 1 << j) *
                         (ratio[N+h+j]-ratio[N+j])
                         for j in range(1, L+1)), Fraction())
                R = sum((Fraction(1, 1 << j) *
                         ((h+j)*ratio[N+h+j]-j*ratio[N+j])
                         for j in range(1, L+1)), Fraction())
                A = Fraction(wp09e_direct(phi, N, h, L), 1 << L)
                self.assertEqual(A, N*G+R)
                self.assertLessEqual(abs(R), h+4)
                self.assertLessEqual(abs(G), 1)

    def test_exact_rolling_vs_independent_direct_at_several_depths(self):
        from experiments.erdos249_full_series_phase.fourier_probe import totients
        X = 96
        for h, L in ((1, 3), (1, 9), (2, 7), (6, 12)):
            phi = totients(2*X+h+L+2)
            vals = wp09e_rolling(phi, X, h, L)
            self.assertEqual(len(vals), X)
            for i, D in enumerate(vals):
                self.assertEqual(D, wp09e_direct(phi, X+i, h, L))
            with self.assertRaises(ValueError):
                wp09e_rolling(phi[:100], X, h, L)

    def test_explicit_true_cook_eligible_depths(self):
        for X, h, p in ((4096, 1, 2), (8192, 2, 3), (32768, 6, 5)):
            c = wp09e_certificate(X, h)
            self.assertEqual(c["L"], wp09e_depth(X, h))
            self.assertEqual(c["p"], p)
            self.assertTrue(c["eligible"])
            self.assertLessEqual(
                16*(2*X+h+c["L"]+2), c["Q"])
            self.assertGreater(
                16*(2*X+h+c["L"]+1), c["Q"]//2)
            self.assertGreater(c["Q"], 32*X)
            self.assertLessEqual(c["H"], X)
            self.assertLessEqual(c["required_min_X"], X)
            self.assertEqual(
                c["normalized_ratio_mean_square_lower"],
                Fraction(1, 400*p**3))
            self.assertEqual(
                c["unwrapped_phase_sum_square_lower"],
                Fraction(X**3, 1600*p**3))
            self.assertFalse(c["weighted_first_harmonic_tenth_saving"])
            self.assertEqual(c["original_irrationality"], "OPEN")

    def test_actual_totient_full_cook_integer_energy(self):
        for X, h in ((4096, 1), (8192, 2), (32768, 6)):
            c = wp09e_energy(X, h)
            self.assertTrue(c["eligible"])
            self.assertTrue(c["energy_bound_passed"])
            self.assertGreaterEqual(
                1600*c["p"]**3*c["sum_D_squared"],
                X**3*c["Q"]**2)
            self.assertEqual(c["source"],
                             "actual Euler totient, exact integer rolling")
        # Independent exact-rational test of the OTHER primary theorem (G),
        # at a genuine Cook least depth where the finite bound is nonvacuous.
        X, h = 4096, 1
        c = wp09e_certificate(X, h)
        p = c["p"]
        from experiments.erdos249_full_series_phase.fourier_probe import totients
        phi = totients(2*X+c["H"]+1)
        f = [Fraction(0)] + [Fraction(phi[n], n) for n in range(1,len(phi))]
        residue_sums = [Fraction() for _ in range(p)]
        squared = Fraction()
        for N in range(X, 2*X):
            G = sum((Fraction(1, 1 << j) *
                     (f[N+h+j]-f[N+j]) for j in range(1,c["L"]+1)),
                    Fraction())
            residue_sums[N % p] += G
            squared += G*G
        self.assertGreaterEqual(squared, Fraction(X, 400*p**3))
        for a in ((-1) % p, (-1-h) % p):
            self.assertGreaterEqual(abs(residue_sums[a]),
                                    Fraction(X, 20*p*p))

    def test_exact_ineligible_and_bad_parameters_fail_closed(self):
        for X, h in ((64, 1), (128, 2), (512, 6)):
            c = wp09e_certificate(X, h)
            self.assertFalse(c["eligible"])
            self.assertIsNone(c["unwrapped_phase_sum_square_lower"])
            self.assertIsNone(c["normalized_ratio_mean_square_lower"])
        for h, L, p in ((1, 5, 2), (2, 6, 2), (6, 10, 3)):
            if h % p == 0:
                with self.assertRaises(ValueError):
                    wp09e_alias(h, L, p)
        with self.assertRaises(ValueError):
            wp09e_alias(1, 3, 9)
        with self.assertRaises(ValueError):
            wp09e_crt(6, 8, 3)
        with self.assertRaises(ValueError):
            wp09e_crt(1, 5, 11, max_period=200)
        with self.assertRaises(ValueError):
            wp09e_energy(4096, 1, max_X=128)
        with self.assertRaises(ValueError):
            wp09e_depth(0, 1)
        with self.assertRaises(ValueError):
            wp09e_prime(-2)

    def test_unwrapped_cubic_energy_cannot_imply_modular_cancellation(self):
        # Purely mathematical hostile example A_N=N has huge real energy
        # yet e(A_N) is identically 1. Not a constructed totient sequence.
        for X in (16, 32, 64):
            arr = tuple(range(X, 2*X))
            self.assertGreaterEqual(
                sum(a*a for a in arr), X**3)
            self.assertTrue(all(a % 1 == 0 for a in arr))
            self.assertEqual(
                sum(1 for a in arr if a % 1 != 0), 0)


from experiments.erdos249_full_series_phase.conditional_cook_phase import (
    conditional_certificate as wp09f_certificate,
    exact_conditional_replay as wp09f_replay,
    centered_representative as wp09f_center,
    source_integer_delta as wp09f_delta,
)


class ConditionalCookModularPhaseTests(unittest.TestCase):
    """WP09-F: true source-locked Cook modulo-one residue-class deficits."""

    def test_exact_conditional_constants_and_distinct_classes(self):
        for X, h, p in ((4096, 1, 2), (8192, 2, 3),
                        (16384, 3, 2), (32768, 6, 5)):
            c = wp09f_certificate(X, h)
            self.assertTrue(c["eligible"])
            self.assertTrue(c["cook_depth_admissible"])
            self.assertTrue(c["least_depth_absolute_eligible"])
            self.assertEqual(c["p"], p)
            self.assertEqual(c["Q"], 1 << c["L"])
            self.assertGreater(c["Q"], 32*X)
            self.assertLess(c["Q"], 96*X)
            self.assertNotEqual(c["prime_positive_class"],
                                c["prime_negative_class"])
            self.assertEqual(c["source_square_energy_lower"],
                             Fraction(X**3, 32*p**3))
            self.assertEqual(c["cocycle_real_deficit_lower"],
                             Fraction(X**3, 4*p**3*c["Q"]**2))
            self.assertEqual(c["pair_original_cook_real_deficit_lower"],
                             Fraction(X**3, 20*p**3*c["Q"]**2))
            self.assertEqual(
                c["exists_single_original_class_average_gap_lower"],
                Fraction(X**2, 80*p**2*c["Q"]**2))
            self.assertEqual(c["least_depth_cocycle_relative_gap"],
                             Fraction(1, 73728*p*p))
            self.assertEqual(c["least_depth_pair_block_deficit"],
                             Fraction(X, 184320*p**3))
            self.assertEqual(c["least_depth_exists_class_relative_gap"],
                             Fraction(1, 737280*p*p))
            self.assertFalse(c["cook_full_global_tenth_saving_proved"])
            self.assertEqual(c["original_irrationality"], "OPEN")

    def test_both_signs_genuine_full_cook_integer_replay(self):
        for X, h, p in ((4096, 1, 2), (8192, 2, 3), (32768, 6, 5)):
            c = wp09f_replay(X, h)
            self.assertEqual(c["exact_integer_replay"], "PASS")
            self.assertEqual(c["p"], p)
            self.assertEqual(len(c["reports"]), 2)
            self.assertEqual(
                set(row["sign"] for row in c["reports"]),
                {"positive", "negative"})
            for row in c["reports"]:
                sg = 1 if row["sign"] == "positive" else -1
                self.assertGreaterEqual(
                    2*p*p*sg*row["full_signed_delta_sum"], X**2)
                self.assertGreaterEqual(
                    4*p*p*sg*row["source_signed_delta_sum"], X**2)
                self.assertGreaterEqual(
                    32*p**3*row["source_delta_squared"], X**3)
                self.assertGreaterEqual(
                    5*row["pair_centered_residue_squared"],
                    row["source_delta_squared"])
                self.assertGreaterEqual(
                    160*p**3*row["pair_centered_residue_squared"], X**3)
                self.assertTrue(row["exact_cocycle_and_phase_transfer_pass"])
            self.assertTrue(c["phase_representatives_all_centered"])

    def test_exact_prime_residue_class_source_oracle(self):
        from experiments.erdos249_full_series_phase.fourier_probe import totients
        for X, h in ((4096, 1), (8192, 2), (32768, 6)):
            c = wp09f_certificate(X, h)
            p, s = c["p"], c["s"]
            phi = totients(2*X+s+h+3)
            for sign, r in ((1, c["prime_positive_class"]),
                            (-1, c["prime_negative_class"])):
                a = [N for N in range(X, 2*X) if N % p == r]
                d = [wp09f_delta(phi, N, h, s) for N in a]
                self.assertGreaterEqual(
                    2*p*p*sign*sum(d), X**2)
                self.assertGreaterEqual(
                    4*p*p*sign*sum(d[:len(d)-(a[-1] == 2*X-1)]),
                    X**2)

    def test_centered_representative_and_wrap_hostiles(self):
        Q = 256
        self.assertEqual(
            [wp09f_center(v, Q) for v in
             (-2*Q, -Q//2, -1, 0, 1, Q//2-1, Q//2, Q, Q+1)],
            [0, -128, -1, 0, 1, 127, -128, 0, 1])
        for D, mod in ((4, 0), (4, 3), (3.5, 256), (True, 256)):
            with self.assertRaises(ValueError):
                wp09f_center(D, mod)

    def test_true_cook_cocycle_plus_phase_deficits_numerically(self):
        # Numerical trig is a *diagnostic*; proof tests above use integers.
        from experiments.erdos249_full_series_phase.fourier_probe import totients
        from experiments.erdos249_full_series_phase.full_window_prime_projection import (
            cook_numerators_rolling,
        )
        from math import sin, pi
        X, h = 4096, 1
        c = wp09f_certificate(X, h)
        Q, p, s, L = c["Q"], c["p"], c["s"], c["L"]
        phi = totients(2*X+s+h+3)
        Ds = cook_numerators_rolling(phi, X, h, L)
        centers = [wp09f_center(d, Q) for d in Ds]
        for r in (c["prime_positive_class"], c["prime_negative_class"]):
            S = [i for i in range(X-1) if (X+i) % p == r]
            T = [i for i in range(X) if (X+i) % p in {r, (r+1)%p}]
            real_cocycle_deficit = sum(
                2*sin(pi*wp09f_delta(phi,X+i,h,s)/Q)**2 for i in S)
            real_pair_deficit = sum(
                2*sin(pi*centers[i]/Q)**2 for i in T)
            self.assertGreaterEqual(
                real_cocycle_deficit + 1e-11,
                float(c["cocycle_real_deficit_lower"]))
            self.assertGreaterEqual(
                real_pair_deficit + 1e-11,
                float(c["pair_original_cook_real_deficit_lower"]))
            one_classes = [sum(2*sin(pi*centers[i]/Q)**2
                               for i in range(X) if (X+i)%p==a)
                           for a in (r,(r+1)%p)]
            self.assertAlmostEqual(sum(one_classes),real_pair_deficit,places=7)
            self.assertGreaterEqual(max(one_classes),
                                    real_pair_deficit/2-1e-10)

    def test_nonminimal_depth_has_only_scale_dependent_bound(self):
        X, h = 8192, 2
        minimum = wp09f_certificate(X, h)
        c = wp09f_certificate(X, h, minimum["L"]+3)
        self.assertTrue(c["eligible"])
        self.assertFalse(c["least_depth_absolute_eligible"])
        self.assertIsNone(c["least_depth_pair_block_deficit"])
        self.assertGreater(c["pair_original_cook_real_deficit_lower"], 0)
        replay = wp09f_replay(X, h, minimum["L"]+3)
        self.assertEqual(replay["exact_integer_replay"], "PASS")

    def test_ineligible_and_invalid_prime_fail_closed(self):
        for X,h in ((64,1),(128,2),(512,6)):
            c = wp09f_certificate(X,h)
            self.assertFalse(c["eligible"])
            self.assertIsNone(c["cocycle_real_deficit_lower"])
            self.assertIsNone(c["exists_single_original_class_average_gap_lower"])
            with self.assertRaises(ValueError):
                wp09f_replay(X,h)
        for p in (2,3,4,9):
            with self.assertRaises(ValueError):
                wp09f_certificate(8192,6,p=p)
        self.assertFalse(wp09f_certificate(8192,2,L=1)["eligible"])
        with self.assertRaises(ValueError):
            wp09f_certificate(0,1)
        with self.assertRaises(ValueError):
            wp09f_replay(4096,1,max_X=512)

    def test_unwrapped_winding_falsification_and_cocycle_diagnosis(self):
        # Generic model theta_N=N: huge unwrapped energy but phase=1.
        # Its modulo-Q one-step forcing must be identically 0 and so
        # cannot satisfy WP09-F's fixed-prime signed source lower bound.
        for X, Q in ((64,4096),(128,8192)):
            D = [N*Q for N in range(X,2*X)]
            self.assertGreaterEqual(
                sum(Fraction(d*d, Q*Q) for d in D), X**3)
            self.assertTrue(all(wp09f_center(d,Q)==0 for d in D))
            self.assertTrue(all(
                (D[i+1]-2*D[i]) % Q == 0
                for i in range(X-1)))
            self.assertFalse(any(
                wp09f_center(D[i],Q) != 0 for i in range(X)))
