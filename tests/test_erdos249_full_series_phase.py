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
