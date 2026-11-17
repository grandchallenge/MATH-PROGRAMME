#!/usr/bin/env python3
"""Exact-rational and modular controls for ERDOS249 moving-depth phase experiment."""
import unittest,math,json
from fractions import Fraction
from pathlib import Path
from fourier_probe import totients, comparator, exact_residue, residue_sequence, phase_scan

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
    def test_output_integrity_and_known_controls(self):
        d=Path(__file__).parent
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
if __name__=='__main__':unittest.main()
