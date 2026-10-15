#!/usr/bin/env python3
"""Exact finite interval checks for Erdős #891 (distinct prime divisors only)."""
import json
from math import isqrt,prod
def omega_distinct_sieve(cap):
    spf=list(range(cap+1))
    for p in range(2,isqrt(cap)+1):
        if spf[p]!=p:continue
        for q in range(p*p,cap+1,p):
            if spf[q]==q:spf[q]=p
    result=[0]*(cap+1)
    for x in range(2,cap+1):
        p=spf[x];y=x//p
        result[x]=result[y]+int(y%p!=0)
    return result
def primes_count(k):
    p=2;ans=[]
    while len(ans)<k:
        if all(p%q for q in ans if q*q<=p):ans.append(p)
        p+=1
    return ans
def check(k,omega,upper):
    ps=primes_count(k+1)
    L=prod(ps[:k])
    Lsch=prod(ps[:k-1])*ps[k]
    assert L<Lsch
    # prefix sum of qualifying integers t with omega(t)>=k+1
    pref=[0]
    for x in range(1,upper+Lsch):
        pref.append(pref[-1]+int(omega[x]>=k+1))
    valid=[];fail=[];schinzel_fail=[]
    for n in range(1,upper+1):
        ok=pref[n+L-1]-pref[n-1]>0
        (valid if ok else fail).append(n)
        if pref[n+Lsch-1]-pref[n-1]==0:schinzel_fail.append(n)
    # For n sufficiently large Schinzel's theorem implies no long-window failures.
    # This finite table is NOT the theorem and captures small exceptions.
    assert len(valid)+len(fail)==upper
    examples=[]
    for n in (1,10,100,1000,20000,upper):
        if n<=upper:
            best=max(omega[n:n+L])
            first=next(n+i for i in range(L) if omega[n+i]==best)
            examples.append(dict(start=n,length=L,max_omega=best,witness=first))
    return dict(k=k,primorial=L,schinzel_length=Lsch,checked_start_range=[1,upper],
                first_failing_starts=fail[:30],fail_count=len(fail),
                last_failure=max(fail,default=None),
                schinzel_fail_count=len(schinzel_fail),
                last_schinzel_failure=max(schinzel_fail,default=None),
                examples=examples)
def test_primorial():
    rows=[]
    for k in range(2,6):
        ps=primes_count(k);L=prod(ps)
        for t in range(1,min(L,3000)):
            # We test exact distinct prime factor count for all t < L.
            f=0;v=t;p=2
            while p*p<=v:
                if v%p==0:
                    f+=1
                    while v%p==0:v//=p
                p+=1
            if v>1:f+=1
            assert f<k,(k,t,f)
        rows.append(dict(k=k,primorial=L,verified_t_below=min(L,3000)))
    return rows
def main():
    upper=100000
    omega=omega_distinct_sieve(upper+1000)
    rec=dict(record_type="EC_BULK_006_891_FINITE/1",
        authority="finite exact checks only, no eventual or conditional infinite proof",
        primorial_distinct_prime_count_lemma=test_primorial(),
        cases=[check(k,omega,upper) for k in (2,3,4)])
    print(json.dumps(rec,indent=2))
if __name__=="__main__":main()
