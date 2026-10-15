#!/usr/bin/env python3
"""Reproducible exact FINITE examples for EC-BULK-007 #1097..#1102.

No infinite, asymptotic, source-fidelity or formal Lean claim is certified.
"""
from itertools import combinations, permutations
from fractions import Fraction
from math import gcd, prod
import json


def progressions(points):
    A=set(points)
    ds={d for a in A for b in A if b>a for d in [b-a] if b+d in A}
    assert all(d>0 for d in ds)
    return sorted(ds)


def noncommuting_s3():
    S=list(permutations(range(3)))
    e=(0,1,2)
    def mul(p,q):return tuple(p[q[i]] for i in range(3))
    adj={(i,j) for i,j in combinations(range(6),2) if mul(S[i],S[j])!=mul(S[j],S[i])}
    maximal=0
    witness=None
    for size in range(1,7):
        for subset in combinations(range(6),size):
            if all((i,j) in adj for i,j in combinations(subset,2)):
                if size>maximal:
                    maximal=size;witness=[S[i] for i in subset]
    center=[p for p in S if all(mul(p,q)==mul(q,p) for q in S)]
    assert center==[e] and maximal==4
    return {"group":"S3","elements":6,"center":center,"center_index":6,
            "noncommuting_clique_max_exact":maximal,"clique_witness":witness}


def divisors(n):
    return [x for x in range(1,n+1) if n%x==0]


def ratio_sums(n):
    ds=divisors(n)
    ratios=[Fraction(y,x) for x,y in zip(ds,ds[1:])]
    h2=sum(((t-1)**2 for t in ratios),Fraction(0))
    cp=sum(gcd(x,y)==1 for x,y in zip(ds,ds[1:]))
    omega=len([p for p in range(2,n+1) if n%p==0 and all(p%q for q in range(2,p))])
    return {"n":n,"divisors":ds,"h2":str(h2),"consecutive_coprime":cp,
            "omega_distinct_primes":omega}


def sieve_sample():
    # Prime squares: pairwise coprime, reciprocal sum converges externally;
    # the finite prefix shows only the sieve mechanism.
    us=[4,9,25,49,121,169]
    assert all(gcd(a,b)==1 for a,b in combinations(us,2))
    remaining=[n for n in range(1,201) if all(n%u for u in us)]
    tx=3 # 4*9*25=900<=1000; next factor 49 takes product above 1000
    assert prod(us[:tx])<=1000<prod(us[:tx+1])
    density=prod((Fraction(u-1,u) for u in us),start=Fraction(1))
    return {"u_finite_prime_squares":us,"coprime_prefix":True,
            "survivors_up_to_200":len(remaining),
            "initial_survivors":remaining[:15],
            "t_1000_of_infinite_prime_square_sequence":tx,
            "finite_density_product":str(density),
            "does_not_prove_infinite_goodness":True}


def squarefree(n):
    if n<1:return False
    p=2
    while p*p<=n:
        if n%(p*p)==0:return False
        p+=1
    return True


def squarefree_demo():
    sf=[n for n in range(1,101) if squarefree(n)]
    # A finite A meets P trivially; a finite check cannot settle any
    # asymptotic density or eventual good sequence claim.
    A=[1,4]
    witnesses=[n for n in range(5,101)
               if all(squarefree(n+a) for a in A if a<n)]
    return {"squarefree_count_up_to_100":len(sf),
            "finite_A":A,"Q_finite_candidate_n_le100":witnesses[:20],
            "finite_witness_does_not_prove_infinite_Q":True}


def main():
    r={"record_type":"EC_BULK_007_FINITE_ARITHMETIC_PHASE_10/1",
       "cohort_id":"EC-BULK-007","mathematical_certification":False,
       "problem_1097":{"AP_differences_0_to_8":progressions(range(9)),
                       "AP_differences_sparse":progressions((0,1,3,4,9,10))},
       "problem_1098":noncommuting_s3(),
       "problem_1099":ratio_sums(12),
       "problem_1100":ratio_sums(30),
       "problem_1101":sieve_sample(),
       "problem_1102":squarefree_demo(),
       "result":"FINITE_CHECKS_PASS"}
    assert r["problem_1097"]["AP_differences_0_to_8"]==[1,2,3,4]
    assert r["problem_1099"]["h2"]=="47/18"
    assert r["problem_1100"]["consecutive_coprime"]>=r["problem_1100"]["omega_distinct_primes"]
    print(json.dumps(r,indent=2))


if __name__=="__main__":main()
