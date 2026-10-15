#!/usr/bin/env python3
"""Exact finite evidence for Erdos 1136–1143; no infinite theorem certification."""
import json
from math import gcd, log, isqrt, lcm

def isprime(n):
    if n<2:return False
    if n%2==0:return n==2
    for d in range(3,isqrt(n)+1,2):
        if n%d==0:return False
    return True

def primes_upto(N):
    return [n for n in range(2,N+1) if isprime(n)]

def factcounts(n):
    omega=Omega=0;v=n
    for p in range(2,isqrt(v)+1):
        if v%p==0:
            omega+=1
            while v%p==0:v//=p;Omega+=1
    if v>1:omega+=1;Omega+=1
    return omega,Omega

def p1136():
    def inset(n):
        if n<=0:return False
        while n%2==0:n//=2
        return n%4==3
    N=16384
    a=[n for n in range(1,N+1) if inset(n)]
    powers={1<<k for k in range(1,16)}
    # Any two positive a,b<=N whose sum is a power of two are excluded.
    assert not any(inset(a0) and inset(s-a0) for s in powers for a0 in range(1,s) if s-a0>=1)
    assert len(a)==N//2-1  # N=2^14: one missing boundary term; tends to half
    return {'cutoff':N,'count':len(a),'density_prefix':'8191/16384 (approaches 1/2)',
     'membership':'odd part congruent 3 mod 4',
     'no_pair_sum_a_power_of_two_by_modular_argument':True,
     'finite_count_does_not_prove_external_upper_density_bound':True}

def p1137():
    p=primes_upto(20000)
    d=[p[i+1]-p[i] for i in range(len(p)-1)]
    M=max(d);P=max(d[i]*d[i-1] for i in range(1,len(d)))
    from fractions import Fraction
    return {'primes_through':20000,'primes_count':len(p),
      'max_gap':M,'max_adjacent_gap_product':P,'ratio':str(Fraction(P,M*M)),
      'finite_ratio_not_limit':True}

def p1138():
    p=primes_upto(20000);d=[p[i+1]-p[i] for i in range(len(p)-1)]
    from bisect import bisect_right
    x=5000;y=4000;C=2
    D=max(d[i] for i in range(len(d)) if p[i]<x)
    lhs=bisect_right(p,y+C*D)-bisect_right(p,y)
    return {'x':x,'y':y,'C':C,'max_gap_d':D,
      'prime_count_in_y_to_y_plus_Cd':lhs,
      'expected_density_real':f'{C*D}/log({y})',
      'no_asymptotic_or_counterexample_claim':True}

def p1139():
    u=[n for n in range(1,10001) if factcounts(n)[1]<=2]
    v=[n for n in range(1,10001) if factcounts(n)[0]<=2]
    assert 8 not in u and 8 in v
    return {'cutoff':10000,'with_at_most_2_prime_factors_counting_multiplicity':len(u),
     'with_at_most_2_distinct_prime_factors':len(v),
     'ambiguity_witness_8':'8=2^3, Omega(8)=3,omega(8)=1',
     'largest_gap_in_Omega_at_most_two_prefix':max(b-a for a,b in zip(u,u[1:])),
     'finite_gaps_do_not_prove_limsup':True}

def p1140():
    good=[]
    for n in range(2,2001):
        if all(isprime(n-2*x*x) for x in range(0,isqrt((n-1)//2)+1)):
            good.append(n)
    assert good==[2,5,7,13,31,61,181,199],good
    return {'n_range':'2..2000','good_n':good,
      'published_list_through_2000':[2,5,7,13,31,61,181,199],
      'zero_included_for_x_integer_and_enforces_n_prime':True,
      'finite_not_complete_all_n':True}

def p1141():
    good=[]
    for n in range(2,2501):
        if all(isprime(n-k*k) for k in range(1,isqrt(n-1)+1) if gcd(k,n)==1):
            good.append(n)
    return {'n_range':'2..2500','good_n':good,'n_968_fails':'968-9=959=7*137',
      'n_1722_in_good_set':1722 in good,
      'finite_not_global_finiteness_theorem':True}

def p1142():
    good=[]
    for n in range(3,10001):
        if all(isprime(n-(1<<k)) for k in range(1,n.bit_length()) if (1<<k)<n):
            good.append(n)
    assert good==[4,7,15,21,45,75,105],good
    return {'n_range':'3..10000 (nonvacuous k-domain)','good_n':good,
      'n_2_satisfies_literal_universal_vacuously':True,
      'unconditional_small_prefix_only':True,
      'external_no_more_below_2_to_44_not_replayed':True}

def p1143():
    ps=[2,3,5]
    period=lcm(*ps)
    out={}
    for k in (1,5,10,16):
        v=[sum(any((s+i)%p==0 for p in ps) for i in range(k)) for s in range(period)]
        out[str(k)]={'minimum':min(v),'max':max(v),
          'minimizing_start_residue_mod30':[s for s,a in enumerate(v) if a==min(v)]}
    return {'primes':ps,'period':period,'exact_F_k_for_selected_k':out,
     'proof':'every prime-divisibility pattern is periodic modulo product 30',
     'does_not_cover_unverified_Erdos_Selfridge_exact_alpha_theorem':True}

def main():
    j={'record_type':'EC_BULK_007_FINITE_PHASE_16/1',
      'cohort_id':'EC-BULK-007','mathematical_certification':False}
    for n in range(1136,1144):j['problem_'+str(n)]=globals()['p'+str(n)]()
    j['result']='FINITE_CHECKS_PASS'
    print(json.dumps(j,indent=2))
if __name__=='__main__':main()
