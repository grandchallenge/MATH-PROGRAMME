#!/usr/bin/env python3
"""Finite and exact source examples for Erdős #1109,#1110,#1111,#1113,#1114,#1115.

No numerical computation here proves global, asymptotic, infinite or
universal assertions. The #1110 induction is independently implemented
and its divisibility invariant exhaustively checked for bounded n.
"""
from itertools import combinations
from math import gcd, lcm
from functools import lru_cache
import json


def squarefree(n):
    if n<1:return False
    p=2
    while p*p<=n:
        if n%(p*p)==0:return False
        p+=1
    return True


def finite_squarefree_sumset(N):
    good=[x for x in range(1,N+1) if squarefree(2*x)]
    goodpairs={(x,y) for x,y in combinations(good,2) if squarefree(x+y)}
    maxset=()
    for r in range(1,len(good)+1):
        for S in combinations(good,r):
            if all((a,b) in goodpairs for a,b in combinations(S,2)):
                maxset=S
        if len(maxset)<r:break
    if not maxset:maxset=()
    assert all(squarefree(a+b) for a in maxset for b in maxset)
    return {'N':N,'eligible_by_self_sum':good,
            'f_N_exact':len(maxset),'maximal_witness':list(maxset),
            'all_self_and_pair_sums_squarefree':True}


@lru_cache(None)
def antichain23(n):
    # Strong induction from the maintained #1110 text.
    if n==0:return ()
    if n%2==0:return tuple(2*x for x in antichain23(n//2))
    q=1
    while q*3<=n:q*=3
    return (q,)+tuple(2*x for x in antichain23((n-q)//2))


def check_antichain23(U):
    length=0
    worst=None
    for n in range(1,U+1):
        S=antichain23(n)
        assert sum(S)==n and len(S)==len(set(S))
        for x in S:
            t=x
            while t%2==0:t//=2
            while t%3==0:t//=3
            assert t==1
        assert all(a%b and b%a for a,b in combinations(S,2))
        if len(S)>length:length=len(S);worst=n
    examples={str(n):list(antichain23(n)) for n in (1,2,7,31,101,256)}
    return {'p':3,'q':2,'checked_all_n_through':U,
            'max_summands_in_checked_range':length,
            'example_n_at_max_summands':worst,
            'examples':examples,
            'complete_induction_argument_separate_from_finite_replay':True}


def c5_anticomplete_edges():
    V=range(5)
    E={frozenset((i,(i+1)%5)) for i in V}
    disjoint_edges=[(tuple(a),tuple(b)) for a,b in combinations(E,2)
           if not (a&b)]
    anticomplete=[(a,b) for a,b in disjoint_edges
           if all(frozenset((u,v)) not in E for u in a for v in b)]
    assert len(E)==5 and len(disjoint_edges)==5 and not anticomplete
    return {'graph':'C5','vertices':5,'edges':5,
            'chromatic_number':3,'clique_number':2,
            'disjoint_edge_pairs':len(disjoint_edges),
            'anticomplete_pairs_of_induced_edges':0,
            'finite_witness_only':True}


def covering_sierpinski():
    m=78557
    primes=(3,5,7,13,19,37,73)
    periods={}
    covered={}
    for p in primes:
        assert pow(2,p-1,p)==1
        period=next(k for k in range(1,p) if pow(2,k,p)==1)
        periods[str(p)]=period
        covered[str(p)]=[k for k in range(period) if (m*pow(2,k,p)+1)%p==0]
    period=lcm(*periods.values())
    uncovered=[k for k in range(period) if not any((m*pow(2,k,p)+1)%p==0 for p in primes)]
    assert not uncovered,(period,uncovered[:8])
    # finite covering + periodicity is a complete proof that all 2^k*m+1 composite,
    # since each expression > all the cover primes when k>=0 and m=78557.
    assert m+1>max(primes)
    return {'m':m,'covering_primes':list(primes),'orders_of_2':periods,
            'covered_residue_classes':covered,
            'combined_period':period,'uncovered_residues':0,
            'periodic_cover_is_rigorous_for_this_m':True,
            'does_not_address_no_finite_covering_conjecture':True}


def arithmetic_progression_derivative():
    # f(x)=x(x²-1)(x²-4), f'(x)=5x^4-15x²+4.
    # Critical roots ±sqrt((15±sqrt145)/10).
    # To compare outer gap s2-s1 to central gap 2s1:
    # s2 > 3*s1 iff sqrt(145)>12 iff 145>144.
    # This holds strictly, so the gaps grow outward.
    assert 145>144
    return {'polynomial':'x*(x^2-1)*(x^2-4)',
            'polynomial_degree':5,
            'roots':[-2,-1,0,1,2],
            'derivative':'5*x^4-15*x^2+4',
            'inner_root_square':'(15-sqrt(145))/10',
            'outer_root_square':'(15+sqrt(145))/10',
            'outer_gap_exceeds_center_gap_exact_witness':'sqrt(145)>12 since 145>144',
            'source_degree_n_vs_n_plus_one_index_mismatch':True}


def entire_path():
    # f(z)=exp(z) along real x>=0; M(r)=e^r, Gamma length within |z|<r is r.
    # This is a simple positive illustration, NOT an obstruction example.
    return {'function':'exp(z)','path':'z=t, t>=0, along positive real axis',
            'M_r':'exp(r)','arc_length_inside_radius_r':'r',
            'f_along_path_tends_to_infinity':True,
            'not_a_universal_result':True}


def main():
    r={'record_type':'EC_BULK_007_FINITE_ARITHMETIC_PHASE_12/1',
       'cohort_id':'EC-BULK-007','mathematical_certification':False,
       'problem_1109':finite_squarefree_sumset(16),
       'problem_1110':check_antichain23(1024),
       'problem_1111':c5_anticomplete_edges(),
       'problem_1113':covering_sierpinski(),
       'problem_1114':arithmetic_progression_derivative(),
       'problem_1115':entire_path(),
       'result':'FINITE_CHECKS_PASS'}
    print(json.dumps(r,indent=2))


if __name__=='__main__':main()
