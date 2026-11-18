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
                sum((r+1)*bit for r in range(R) for bit in bits)<=R
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
