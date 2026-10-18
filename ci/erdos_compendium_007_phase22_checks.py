#!/usr/bin/env python3
"""Deterministic exact phase-22 fixtures for Erdős #1184–1191, not asymptotic proofs."""
import itertools,json,math
from fractions import Fraction as Q
from collections import Counter

def isprime(n):
    return n>=2 and all(n%d for d in range(2,math.isqrt(n)+1))
def largest_prime_factor(n):
    assert n>1
    P=1
    for d in range(2,math.isqrt(n)+1):
        while n%d==0:
            P=d;n//=d
    return max(P,n)
def p1184():
    checks={}
    for n,k in ((100,10),(1000,20),(10000,40)):
        a=[n+i for i in range(1,k+1)]
        total=sum(largest_prime_factor(x)>k for x in a)
        checks[f'{n},{k}']={'large_prime_factor_count':total,'smooth_count':k-total}
    return {'samples':checks,'Dickman_rho_2':'1-log(2)','finite_smooth_counts_not_uniform_n_k_asymptotic':True}

def ap_count(A,d,k):
    return sum(all(a+j*d in A for j in range(k)) for a in range(1,21))
def p1185():
    A={i for i in range(1,21) if i%2}
    B={1,4}
    diffs={abs(a-b) for a in B for b in B if a!=b}
    assert diffs=={3} and ap_count(A,3,3)==0
    return {'N':20,'A':'odd numbers 1..20','A_size':len(A),'B':[1,4],
        'nonzero_absolute_B_minus_B':sorted(diffs),
        'three_term_AP_with_difference_3_in_A':0,
        'finite_B_size_2_does_not_disprove_arbitrarily_large_m':True}

def p1186():
    finite={}
    for n in (8,10,12):
        triples=[(a,a+d,a+2*d) for d in range(1,(n-1)//2+1)
                 for a in range(1,n-2*d+1)]
        count_by={}
        mini=None;witness=None
        for coloring in range(1<<n):
            m=sum(((coloring>>(a-1))&1)==((coloring>>(b-1))&1)==((coloring>>(c-1))&1)
                  for a,b,c in triples)
            count_by[m]=count_by.get(m,0)+1
            if mini is None or m<mini:mini=m;witness=coloring
        finite[str(n)]={'total_progressions':len(triples),'minimum_monochromatic_k3_APs':mini,
            'normalized_minimum_over_n_squared':str(Q(mini,n*n)),
            'witness_color_bitmask':witness,'colourings_checked':1<<n}
        assert sum(count_by.values())==1<<n
    cyc={}
    for p in (5,7,11):
        triples={(tuple(sorted(((a-d)%p,a%p,(a+d)%p))))
                 for a in range(p) for d in range(1,p) if len({(a-d)%p,a%p,(a+d)%p})==3}
        # For k=3, no repeated membership, each AP counted once.
        mn=min(sum(((mask>>a)&1)==((mask>>b)&1)==((mask>>c)&1)
                   for a,b,c in triples) for mask in range(1<<p))
        cyc[str(p)]={'distinct_unordered_3AP':len(triples),'min_mono':mn,
                     'min_over_p_squared':str(Q(mn,p*p))}
    return {'integer_interval_exact_k3':finite,'prime_field_exact_k3':cyc,
            'finite_minima_not_asymptotic_delta_3':True}

def p1187():
    for d in (2,3,5,7,11,13):
        for a in range(16):
            c=lambda x:((x%4) in (0,1))
            assert not(c(a)==c(a+d)==c(a+2*d)),(a,d)
        assert d%4 !=0
    return {'tested_prime_differences':[2,3,5,7,11,13],
      'four_color_residue_mod_4':'any prime step is nonzero modulo four, forbidding monochromatic pairs',
      'two_color_residues_red':'0,1 modulo 4','two_color_blue':'2,3 modulo 4',
      'no_three_term_progression_of_prime_difference_under_two_coloring':True,
      'Green_Tao_positive_density_prime_progressions_external':True}

def p1188():
    mods=(2,3,4,6,8,12);top=max(mods);period=math.lcm(*mods)
    full=(1<<period)-1
    coverings=[]
    for m in mods:
        covering=[]
        for a in range(m):
            mask=sum(1<<x for x in range(a,period,m))
            covering.append((m,a,mask))
        coverings.append([None]+covering)
    selected_count=0; minimal=0;witnesses=[]
    for choices in itertools.product(*coverings):
        chosen=[z for z in choices if z]
        if not chosen:continue
        joined=0
        for _,_,mask in chosen:joined|=mask
        if joined!=full:continue
        selected_count+=1
        if all((0 if len(chosen)==1 else __import__('functools').reduce(int.__or__,
                       (y[2] for y in chosen if y!=z),0))!=full for z in chosen):
            minimal+=1
            if len(witnesses)<5:
                witnesses.append([(m,a) for m,a,_ in chosen])
    assert minimal>0
    return {'largest_modulus':top,'allowed_distinct_moduli':list(mods),'test_period':period,'all_congruence_assignment_choices':math.prod(m+1 for m in mods),
      'covering_system_count':selected_count,'minimal_covering_system_count':minimal,
      'minimal_distinct_covering_sample':witnesses,
      'minimality_removes_original_congruence_assignment_only':True,
      'G_x_irreducible_modulus_sets_is_stronger_definition':True}

def p1189():
    moduli=[2,3,4,6,12];L=12
    def cover_possible(M):
        for residues in itertools.product(*(range(n) for n in M)):
            if all(any(x%n==a for n,a in zip(M,residues)) for x in range(L)):
                return residues
        return None
    witness=cover_possible(moduli)
    assert witness is not None
    for omit in range(len(moduli)):
        assert cover_possible(moduli[:omit]+moduli[omit+1:]) is None
    return {'irreducible_modulus_set_divisors_of_12':moduli,'covering_residue_choices':list(witness),
      'any_proper_modulus_subset_cannot_cover_even_with_new_residues':True,
      'maximum_modulus':12,'reciprocal_sum':str(sum((Q(1,n) for n in moduli),Q()))}

def p1190():
    # a mod m and b mod n disjoint iff a!=b modulo gcd(m,n).
    classes=[(4,0),(6,1)]
    assert (classes[0][1]-classes[1][1])%math.gcd(4,6)!=0
    return {'two_disjoint_congruences':['0 modulo 4','1 modulo 6'],
            'reciprocal_modulus_sum':str(Q(1,4)+Q(1,6)),
            'CRT_incompatibility_gcd_2':True,
            'single_finite_pair_not_sharp_epsilon_m_asymptotic':True}

def p1191():
    A=[1<<i for i in range(10)]
    rep={}
    for a,b in itertools.combinations_with_replacement(A,2):
        s=a+b;assert s not in rep,(s,rep.get(s),(a,b));rep[s]=(a,b)
    return {'finite_Sidon_prefix_powers_2':A,
        'unique_unordered_pair_sums':len(rep),
        'count_A_intersect_1_512':10,
        'finite_Sidon_property_not_dense_infinite_Sidon_construction':True}

def main():
    result={'record_type':'EC_BULK_007_FINITE_PHASE_22/1','cohort_id':'EC-BULK-007',
        'mathematical_certification':False}
    for n in range(1184,1192):result[f'problem_{n}']=globals()[f'p{n}']()
    result['result']='FINITE_CHECKS_PASS'
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
