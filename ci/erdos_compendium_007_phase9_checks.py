#!/usr/bin/env python3
"""Exact bounded graph/number witnesses for #1091..#1096.
No finite table proves infinitely-many or asymptotic statements.
"""
from itertools import combinations
from math import comb, gcd
from fractions import Fraction as F
import json


def primes_upto(n):
    p=[True]*(n+1)
    if n>=0:p[0]=False
    if n>=1:p[1]=False
    for i in range(2,int(n**.5)+1):
        if p[i]:
            for j in range(i*i,n+1,i):p[j]=False
    return [i for i in range(2,n+1) if p[i]]


def low_prime_factors(N,limit):
    return [p for p in primes_upto(limit) if N%p==0]


def small_min_factor(N):
    for p in primes_upto(int(N**.5)+1):
        if N%p==0:return p
    return N


def deficiency(n,k):
    if n<2*k:return None
    N=comb(n,k)
    if low_prime_factors(N,k):return None
    def smooth(t):
        for p in primes_upto(k):
            while t%p==0:t//=p
        return t==1
    return sum(smooth(n-i) for i in range(k))


def binomial_examples():
    list14=[(7,3),(13,4),(23,5),(14,4),(44,8),(46,10),
      (47,10),(47,11),(62,6),(74,10),(94,10),(95,10),(241,16),(284,28)]
    out=[]
    for n,k in list14:
        B=comb(n,k);bound=max(F(n,k),F(k))
        tested_primes=primes_upto(max(n//k,k))
        hits=[p for p in tested_primes if p<=bound and B%p==0]
        assert not hits,(n,k,hits)
        d=deficiency(n,k)
        assert isinstance(d,int) and d>=1,(n,k,d)
        out.append({"n":n,"k":k,"threshold":str(bound),
          "small_prime_factor_at_or_below_threshold":False,"deficiency":d})
    assert deficiency(7,3)==1 and deficiency(47,11)==4 and deficiency(284,28)==9
    # Scan and deduplicate all small counterexamples; not a global exception classification.
    discovered=[]
    for k in range(2,11):
        for n in range(2*k,201):
            B=comb(n,k);T=max(F(n,k),F(k))
            if not any(B%p==0 for p in primes_upto(max(n//k,k)) if p<=T):
                discovered.append((n,k))
    return {"historical_14_verified":out,"bounded_scan_k2_to10_n_le200":discovered,
     "bounded_scan_only":True}


def thresholds():
    out=[]
    for k in range(2,10):
        answers=[]
        for n in range(k+2,5001):
            if not low_prime_factors(comb(n,k),k):
                answers.append(n)
                break
        assert answers,k
        out.append({"k":k,"first_n":answers[0],
                    "all_prime_factors_greater_than_k":True,
                    "n_checked_up_to":answers[0]})
    return out


def wheel():
    # Rim 0..4 and hub 5. Simple six-vertex odd wheel:
    E={tuple(sorted((u,(u+1)%5))) for u in range(5)}
    E|={(u,5) for u in range(5)}
    assert len(E)==10
    verts=range(6)
    assert not any(all(tuple(sorted(z)) in E for z in combinations(Q,2))
                   for Q in combinations(verts,4))
    # K4-free; 4 chromatic because C5 must use >=3 colours and hub adjacent to all.
    diag_counts=[]
    for m in (5,):
        for S in combinations(verts,m):
            for tail in __import__('itertools').permutations(S[1:]):
                cycle=(S[0],)+tail
                if cycle[1]>cycle[-1]:continue
                CE={tuple(sorted((cycle[i],cycle[(i+1)%m]))) for i in range(m)}
                if not CE<=E:continue
                diag=sum(e in E-CE for e in combinations(S,2))
                diag_counts.append(diag)
    assert diag_counts and max(diag_counts)<=2
    return {"vertices":6,"edges":10,"K4_free":True,"chromatic_number":4,
           "odd_cycles_of_length_5_enumerated":len(diag_counts),
           "maximum_diagonals_length5":max(diag_counts)}


def basic_k4_decomposition():
    # K4 = K2,2 (bipartite with 4 edges) plus two edges inside its parts
    E=set(combinations(range(4),2))
    bip={tuple(sorted((a,b))) for a in (0,1) for b in (2,3)}
    return {"vertices":4,"total_edges":len(E),"bipartite_edges":len(bip),
            "deleted_to_bipartite":len(E-bip)}


def finite_q():
    # For q=11/10, finite exponent 0..8; distinct sorted finite sums.
    q=F(11,10);powers=[q**i for i in range(9)]
    sums={sum((powers[i] for i in range(9) if mask>>i&1),F(0))
          for mask in range(1<<9)}
    vals=sorted(sums)
    gaps=[b-a for a,b in zip(vals,vals[1:])]
    assert vals[0]==0 and vals[1]==1
    return {"q":"11/10","highest_exponent":8,"distinct_sums":len(vals),
            "min_gap":str(min(gaps)),"max_gap":str(max(gaps)),
            "finite_truncation_cannot_test_limit":True}


def main():
    r={"record_type":"EC_BULK_007_FINITE_ARITHMETIC_PHASE_9/1",
       "cohort_id":"EC-BULK-007","mathematical_certification":False,
       "problem_1091":wheel(),
       "problem_1092":basic_k4_decomposition(),
       "problem_1093_and_1094":binomial_examples(),
       "problem_1095":thresholds(),
       "problem_1096":finite_q(),
       "status":"FINITE_CHECKS_PASS"}
    print(json.dumps(r,indent=2))


if __name__=="__main__":main()
