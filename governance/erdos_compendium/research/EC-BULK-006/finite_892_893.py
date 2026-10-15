#!/usr/bin/env python3
"""Bounded exact checks for Erdős #892 primitive sets and #893 Mersenne divisor sums.
SymPy factorint primality tests used only for factors < 2^64.
"""
from itertools import combinations
from math import gcd
import json
from sympy import factorint,isprime

def primitive(A):
    return all(x%y!=0 and y%x!=0 for x,y in combinations(A,2))

def gcd_free_historical(A):
    return all(gcd(x,y) not in A for x,y in combinations(A,2)
               if x%y!=0 and y%x!=0)

def gcd_free_literal(A):
    return all(gcd(x,y) not in A for x,y in combinations(A,2))

def primitive_finite():
    rows=[]
    for n in range(1,25):
        upper=list(range(n//2+1,n+1))
        assert len(upper)==(n+1)//2 and primitive(upper)
        # In a primitive set only one number with any fixed odd part
        # may occur, since odd-part chains are x,2x,4x,... .
        chains={}
        for x in range(1,n+1):
            m=x
            while m%2==0:m//=2
            chains.setdefault(m,[]).append(x)
        assert len(chains)==(n+1)//2
        if n<=15:
            max_size=max((mask.bit_count() for mask in range(1<<n)
                          if primitive([j+1 for j in range(n) if mask>>j&1])))
            assert max_size==(n+1)//2,(n,max_size)
        rows.append({'N':n,'max_antichain':(n+1)//2,'upper_half':upper if n in (6,10,16,24) else None})
    counter=[2,4,9]
    assert gcd_free_historical(counter) and not gcd_free_literal(counter) and not primitive(counter)
    good=[6,10,15]
    assert primitive(good) and gcd_free_historical(good)
    return {'N_range':[1,24],'independent_bruteforce_N_up_to':15,
            'exact_maximal_primitive_subset_cardinality':'ceil(N/2)',
            'cases':rows,'historical_vs_literal_gcd_example':counter,
            'literal_nontrivial_exclusion_forces_primitive':True,
            'finite_primitive_example':good}

def tau(n):
    fac=factorint(n)
    assert all(2<=p<2**64 and isprime(p) and e>0 for p,e in fac.items()),fac
    result=1
    for p,e in fac.items():result*=e+1
    product=1
    for p,e in fac.items():product*=int(p)**int(e)
    assert product==n
    return result,{str(p):int(e) for p,e in sorted(fac.items())}

def tau_trial(n):
    out=1;p=2
    while p*p<=n:
        e=0
        while n%p==0:
            n//=p;e+=1
        if e:out*=e+1
        p+=1 if p==2 else 2
    if n>1:out*=2
    return out

def mersenne_finite():
    max_k=64
    A=[0];B=[0];factors={}
    for k in range(1,max_k+1):
        u,fac=tau(2**k-1)
        A.append(u)
        if k<=32:
            v,fac_plus=tau(2**k+1)
            B.append(v)
            assert A[k]*B[k]==u*v
        if k<=24:assert u==tau_trial(2**k-1),(k,u)
        if k in (1,2,3,4,5,6,8,12,16,24,32,48,64):
            factors[str(k)]=fac
    F=[0]
    for k in range(1,max_k+1):F.append(F[-1]+A[k])
    cases=[]
    for n in range(1,33):
        assert A[2*n]==A[n]*B[n]
        assert F[2*n]>2*F[n]
        cases.append({'n':n,'f_n':F[n],'f_2n':F[2*n],
                'ratio_exact_numerator':F[2*n],'ratio_exact_denominator':F[n],
                'tau_plus_power':B[n]})
    return {'k_range':[1,64],
            'exact_factor_product_and_primality_checked':True,
            'factors_below_2_power_64':True,
            'independent_trial_division_k_up_to':24,
            'doubling_identity_n_range':[1,32],
            'dyadic_identity':'tau(2^(2k)-1)=tau(2^k-1)*tau(2^k+1)',
            'rigorous_elementary_bound':'f(2n)>2*f(n) all n>=1',
            'samples_factorization':factors,
            'samples_n':[x for x in cases if x['n'] in (1,2,3,4,6,8,12,16,24,32)]}

def main():
    print(json.dumps({
        'record_type':'EC_BULK_006_892_893_FINITE/1',
        'authority':'bounded finite exact arithmetic and elementary lemmas only',
        'p892':primitive_finite(),'p893':mersenne_finite()
    },indent=2))
if __name__=='__main__': main()
