#!/usr/bin/env python3
"""Finite exact distinct-prime checks for Erdős–Selfridge #889–890.
No asymptotic limit or unbounded maximum is certified by these scans.
"""
import json
from math import isqrt
def sieve(N):
    spf=list(range(N+1))
    for p in range(2,isqrt(N)+1):
        if spf[p]!=p:continue
        for t in range(p*p,N+1,p):
            if spf[t]==t:spf[t]=p
    spf[0]=0;spf[1]=1
    return spf
def distinct_prime_divisors(t,spf):
    ans=[]
    while t>1:
        p=spf[t];ans.append(p)
        while t%p==0:t//=p
    return ans
def v(n,k,spf):
    return sum(p>k for p in distinct_prime_divisors(n+k,spf))
def omega_gt(n,k,spf):
    return sum(p>k for p in distinct_prime_divisors(n,spf))
def brute_novel(n,k,spf):
    existing=set()
    for i in range(k):existing.update(distinct_prime_divisors(n+i,spf))
    return len(set(distinct_prime_divisors(n+k,spf))-existing)
def research_889(spf):
    cutoff=2000
    exceptions=[];v1_eq1=[]
    minima=[100,300,500,1000,1500,2000]
    min_v0={str(c):1000 for c in minima}
    tails={str(c):0 for c in minima}
    argmax={}
    for n in range(1,cutoff+1):
        # If k>n then n+k<2k; at most ONE prime divisor can be >k.
        candidate=[v(n,k,spf) for k in range(n+1)]
        max0=max(candidate)
        max1=max(candidate[1:]) if n else 0
        if max0==1:exceptions.append(n)
        if max1==1:v1_eq1.append(n)
        if n<=24:argmax[str(n)]=dict(v0=max0,first_argmax=candidate.index(max0),
           v1=max1,brute_prefix=[brute_novel(n,k,spf) for k in range(n+1)])
        if n in minima:
            min_v0[str(n)]=min(max(v(t,k,spf) for k in range(t+1))
                                   for t in range(max(17,n//2),n+1))
            tails[str(n)]=n//2
    assert exceptions==[1,2,3,4,7,8,16],exceptions
    return dict(exceptions_v0_eq1_through_2000=exceptions,
       v1_eq1_up_to_2000=v1_eq1,
       primary_reported_v1_eq1_up_to_2500=[1,2,3,4,6,7,8,10,12,15,16,18,22,24,26,30,36,42,46,48,60,70,78,80,96,120,190,222,330],
       v1_matches_primary_up_to_2000=None,
       finite_tail_minima_v0=min_v0,argmax_small=argmax,
       cutoff_justification="k>n implies v(n,k)<=1")
def research_890(spf):
    ks=[1,2,3,4,5,8,12,26]
    outcomes=[]
    for k in ks:
        primes=[p for p in range(2,k+1) if spf[p]==p]
        deterministic=sum(k//p for p in primes)
        values=[]
        for n in range(100,5101):
            large=sum(omega_gt(n+i,k,spf) for i in range(k))
            allprime=sum(len(distinct_prime_divisors(n+i,spf)) for i in range(k))
            count_small=sum(sum(p<=k for p in distinct_prime_divisors(n+i,spf))
                 for i in range(k))
            assert allprime==large+count_small
            assert count_small>=deterministic,(n,k,count_small,deterministic)
            values.append((large,allprime,n,count_small))
        min_large=min(v[0] for v in values)
        min_all=min(v[1] for v in values)
        cases=[dict(n=n,omega_gt_sum=x,omega_sum=y,small_prime_contrib=z)
              for x,y,n,z in values if x==min_large][:4]
        outcomes.append(dict(k=k,prime_divisors_below_or_equal_k=primes,
          lower_bound_small_prime_occurrences=deterministic,
          observed_min_omega_gt=min_large,observed_min_omega=min_all,
          first_min_omega_gt_cases=cases))
    return dict(n_window=[100,5100],
       k_window=ks,
       lemma="sum of omega(n+i) = sum omega_{>k}(n+i) + count of small-prime occurrences",
       results=outcomes)
def main():
    spf=sieve(5200)
    a=research_889(spf)
    assert a['v1_eq1_up_to_2000']==a['primary_reported_v1_eq1_up_to_2500'],(a['v1_eq1_up_to_2000'],a['primary_reported_v1_eq1_up_to_2500'])
    a['v1_matches_primary_up_to_2000']=True
    print(json.dumps(dict(record_type="EC_BULK_006_889_890_FINITE/1",
            authority="exact finite only; no asymptotic proof or Lean replay",
            p889=a,p890=research_890(spf)),indent=2))
if __name__=="__main__":main()
