#!/usr/bin/env python3
"""Erdős #896 product singleton fibers and #897 additive-extension finite interface.
Finite checks alone do NOT validate external Ford/Wirsing or Lean proofs.
"""
import json
from functools import lru_cache
from itertools import combinations
from math import gcd
def product_multiplicities(A,B):
    mult={}
    for a in A:
        for b in B:
            mult[a*b]=mult.get(a*b,0)+1
    return mult
def product_score(A,B):
    return sum(c==1 for c in product_multiplicities(A,B).values())
def prime(n):
    return n>1 and all(n%p for p in range(2,int(n**0.5)+1))
def elementary_lower(N):
    P=[p for p in range(N//2+1,N+1) if prime(p)]
    A=[a for a in range(1,N+1) if a not in P]
    B=P
    # A excludes all primes in P; no number <=N except that prime
    # is divisible by a given p>N/2.
    assert all(a%p for a in A for p in P)
    M=product_multiplicities(A,B)
    assert len(M)==len(A)*len(B) and all(c==1 for c in M.values())
    return dict(N=N,A=A if N<=10 else None,B=B,product_score=len(M),
                formula=f"({N}-{len(P)})*{len(P)}")
def optimize_product(N):
    # Enumerate all pairs of subset masks A,B; exact 4^N possibilities.
    best=-1;witness=None;howmany=0
    for a_mask in range(1<<N):
        A=[i+1 for i in range(N) if a_mask>>i&1]
        for b_mask in range(1<<N):
            B=[i+1 for i in range(N) if b_mask>>i&1]
            sc=product_score(A,B)
            howmany+=1
            if sc>best:best=sc;witness=(A,B)
    A,B=witness
    assert product_score(A,B)==best
    return dict(N=N,maximum=best,A=A,B=B,all_ordered_pairs_of_subsets=howmany,
                multiplication_table_size=len({a*b for a in range(1,N+1) for b in range(1,N+1)}))
def primitive_gcd_product():
    # F(A,B) depends on ORDERED (a in A,b in B), not unordered {a,b}.
    A=[2];B=[3];m=product_multiplicities(A,B)
    assert m=={6:1}
    AA=[2,3];BB=[2,3]
    assert product_multiplicities(AA,BB)[6]==2
    return dict(singleton_A=[2],singleton_B=[3],unique_m=[6],
                double_A=AA,double_B=BB,nonunique_m=6)

def factor_exp(n):
    out=[];x=n;p=2
    while p*p<=x:
        e=0
        while x%p==0:
            x//=p;e+=1
        if e:out.append((p,e))
        p+=1
    if x>1:out.append((x,1))
    return out
def f(n):
    """An arbitrary (not Wirsing's counterexample!) real-free additive example."""
    return sum(e*(e+1) for p,e in factor_exp(n))
def research_897():
    for a in range(1,151):
        for b in range(1,151):
            if gcd(a,b)==1:
                assert f(a*b)==f(a)+f(b),(a,b)
    assert f(1)==0
    # f(2^k)=k(k+1), so ratio f(2^k)/log(2^k)=(k+1)/log 2
    # unbounded. This example does NOT establish small consecutive increments.
    powers=[dict(k=k,prime_power=2**k,f_value=f(2**k),
                 quotient_without_log_factor=k+1) for k in range(1,33)]
    assert all(row['f_value']==row['k']*(row['k']+1) for row in powers)
    delta=[f(n+1)-f(n) for n in range(2,2001)]
    assert max(delta)>0 and min(delta)<0
    return dict(
      additive_coprime_direct_check_a_b_range=[1,150],
      prime_power_ratios=powers,
      arithmetic_function="f(n)=sum_{p^e || n} e(e+1)",
      prime_power_growth="f(2^k)/log(2^k)=(k+1)/log(2) tends to infinity",
      finite_adjacent_delta_range=[2,2000],
      min_f_next_minus_f=min(delta),max_f_next_minus_f=max(delta),
      source_boundary="This toy f meets prime-power growth but is NOT claimed as Wirsing's counterexample to either limsup conclusion",
      care="Ratios f(n+1)/f(n) defined for n>=2 since f(n)>0 there")
def main():
    out=dict(record_type='EC_BULK_006_896_897_FINITE/1',
             authority='Exact finite optimization and elementary additive extension only; no external asymptotic/Lean proof',
             p896=dict(exact_maxima=[optimize_product(n) for n in range(1,9)],
                       elementary_examples=[elementary_lower(n) for n in (8,12,24,40,80)],
                       semantics=primitive_gcd_product()),
             p897=research_897())
    print(json.dumps(out,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
