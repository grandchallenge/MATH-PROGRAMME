#!/usr/bin/env python3
"""Finite exact and constructive fixtures for Erdős 1144–1151; no general certification."""
import itertools,json,math,decimal
from math import gcd,isqrt
def primes(N):
    return [n for n in range(2,N+1) if all(n%d for d in range(2,isqrt(n)+1))]
def parity_square_free(n):
    b=0
    for j,p in enumerate(primes(16)):
        while n%p==0:
            n//=p;b^=1<<j
    assert n==1
    return b
def p1144():
    N=16
    masks=[parity_square_free(n) for n in range(1,N+1)]
    sums=[]
    for signs in itertools.product((-1,1),repeat=len(primes(N))):
        P={p:signs[i] for i,p in enumerate(primes(N))}
        def f(n):
            z=1
            for j,p in enumerate(primes(N)):
                if (parity_square_free(n)>>j)&1:z*=P[p]
            return z
        sums.append(sum(f(n) for n in range(1,N+1)))
    first=sum(sums)//len(sums)
    second=sum(x*x for x in sums)//len(sums)
    paircount=sum((a*b and isqrt(a*b)**2==a*b) for a in range(1,N+1) for b in range(1,N+1))
    assert first==isqrt(N)==4 and second==paircount
    return {'N':N,'sign_assignments':len(sums),'E_S_N':first,
      'E_S_N_squared':second,'exact_pair_product_square_count':paircount,
      'nonzero_mean_from_perfect_squares':True,
      'finite_expectations_not_almost_sure_limsup':True}
def p1145():
    # Unrestricted zero-inclusive binary digit decomposition is unique.
    evenbits=[sum((1<<(2*j)) for j in range(3) if mask>>j&1) for mask in range(8)]
    oddbits=[2*a for a in evenbits]
    counts={n:0 for n in range(64)}
    for a,b in itertools.product(evenbits,oddbits):counts[a+b]+=1
    assert all(v==1 for v in counts.values())
    return {'binary_bits':6,'A_zero_included':evenbits,'B_zero_included':oddbits,
      'each_n_0_through_63_has_exactly_one_representation':True,
      'construction_fails_as_ratio_an_over_bn_tends_to_one':True,
      'positive_A_equals_positive_B_integers_has_r_n':'n-1 for n>=2'}
def p1146():
    B={1}|set(range(2,1001,2))
    assert all(2*len(B.intersection(range(1,N+1)))>=N for N in range(1,1001))
    smooth=set()
    for i in range(11):
        for j in range(8):
            z=2**i*3**j
            if z<=1000:smooth.add(z)
    sums={x+y for x in smooth for y in B if x+y<=1000}
    assert 1 not in sums and 1 in B
    return {'B_example':'{1} union positive even integers','B_schnirelmann_density':'1/2',
      'literal_A_positive_no_zero':'{2^i3^j:i,j>=0}','1_in_B':True,
      '1_not_in_A_plus_B':True,'literal_schnirelmann_density_A_plus_B':0,
      'mandatory_zero_or_shift_convention_source_conflict':True,
      'does_not_disprove_properly_normalized_open_conjecture':True}
def p1147():
    D=decimal.Decimal;decimal.getcontext().prec=55
    a=D(2).sqrt()
    chosen=[]
    for n in range(2,501):
        x=a*n*n
        nearest=x.to_integral_value(rounding=decimal.ROUND_HALF_EVEN)
        if abs(x-nearest)<1/D(n).ln():chosen.append(n)
    reachable={x+y for x in chosen for y in chosen if x+y<=1000}
    missing=[n for n in range(4,1001) if n not in reachable]
    assert missing
    return {'alpha':'sqrt(2)','n_min':2,'n_max':500,'members':len(chosen),
      'first_members':chosen[:12],'missing_pair_sums_up_to_1000_count':len(missing),
      'first_missing':[n for n in missing[:12]],
      'finite_missing_values_not_failure_of_asymptotic_basis':True}
def p1148():
    def representable(n):
        S={k*k for k in range(isqrt(n)+1)}
        T={a+b for a in S for b in S if a+b<=2*n}
        return any(n+z in T for z in S)
    missing=[n for n in range(1,301) if not representable(n)]
    assert not representable(6563)
    assert representable(6564)
    return {'range':300,'unrepresentable':missing,
      '6563_not_representable_bounded_square':True,
      '6564_representable':True,'finite_range_not_eventual_all_n_proof':True}
def p1149():
    N=10000
    good=[n for n in range(1,N+1) if gcd(n,isqrt(n))==1]
    return {'alpha':'1/2','n_le':N,'coprime_count':len(good),
      'fraction_exact':str(len(good))+'/'+str(N),
      'reference_limit':'6/pi^2','finite_ratio_not_density_theorem':True}
def p1150():
    # P(z)=1+z+z²+z³ has sup exactly 4 by triangle inequality at z=1.
    # Rudin-Shapiro P1=1+z and Q1=1-z: |P1|²+|Q1|²=4 on |z|=1.
    return {'degree3_four_coefficients_polynomial':'1+z+z^2+z^3',
      'unit_circle_sup_exact':4,'parseval_lower_bound':'sqrt(4)=2',
      'unit_circle_L2_norm_squared':4,
      'rudin_shapiro_degree1':'P=1+z,Q=1-z; |P|²+|Q|²=4',
      'degree_n_has_n_plus_one_coefficients':True,
      'finite_example_not_universal_gap':True}
def p1151():
    # All polynomial interpolation at distinct nodes reproduces constant f.
    return {'f':'f(x)=1/2 for every x in [-1,1]',
      'any_chebyshev_nodes':'unique interpolation polynomial identically 1/2',
      'cluster_set_for_fixed_x':['1/2'],
      'empty_set_and_arbitrary_closed_set_not_established':True,
      'fixed_x_quantifier_requires_source_normalization':True}
def main():
    j={'record_type':'EC_BULK_007_FINITE_PHASE_17/1',
       'cohort_id':'EC-BULK-007','mathematical_certification':False}
    for n in range(1144,1152):j[f'problem_{n}']=globals()[f'p{n}']()
    j['result']='FINITE_CHECKS_PASS'
    print(json.dumps(j,indent=2))
if __name__=='__main__':main()
