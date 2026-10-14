#!/usr/bin/env python3
"""Exact finite evidence only: #881 sparse deletion and #882 primitive subset sums."""
from itertools import combinations
import json

def power_two(n):
    return n>0 and n&(n-1)==0

def two_basis_test():
    min_reps=10**9
    for n in range(30,2001):
        reps=sum(not power_two(a) and not power_two(n-a) for a in range(1,n))
        assert reps>0,n
        min_reps=min(reps,min_reps)
    return dict(target_range=[30,2000],minimum_ordered_representations=min_reps)

def subset_sums(A):
    sums=[0]
    for a in A:sums+=[v+a for v in sums]
    return sums

def primitive(sums):
    v=sorted(set(sums)-{0})
    return all(b%a!=0 for i,a in enumerate(v) for b in v[i+1:])

def exact_max(N):
    best=()
    tested=0
    def rec(n,A,sums):
        nonlocal best,tested
        tested+=1
        if len(A)>len(best):best=A
        if n>N:return
        rec(n+1,A,sums)
        extra=[n+v for v in sums]
        if primitive(sums+extra):rec(n+1,A+(n,),sums+extra)
    rec(1,(),[0])
    assert primitive(subset_sums(best))
    return dict(N=N,max_size=len(best),witness=list(best),states=tested)

def main():
    best=[exact_max(n) for n in range(1,19)]
    for n in range(1,13):
        brute=max((len(A) for k in range(n+1)
             for A in combinations(range(1,n+1),k)
             if primitive(subset_sums(A))),default=0)
        assert best[n-1]['max_size']==brute,n
    for n,k in ((3,2),(7,3),(15,4)):
        assert best[n-1]['max_size']==k,(n,best[n-1])
    binary=[]
    for m in range(1,11):
        A=sorted(2**m-2**j for j in range(m))
        S=subset_sums(A)
        assert len(S)==2**m and len(set(S))==2**m
        assert primitive(S) and max(A)==2**m-1
        binary.append(dict(m=m,A=A,distinct_nonempty_sums=len(S)-1))
    out=dict(record_type='EC_BULK_006_881_882_FINITE/1',
             authority='EXACT_FINITE_ONLY',
             sparse_deletion=two_basis_test(),
             primitive_extrema=best,
             brute_crosschecked_n_up_to=12,
             binary_family=binary)
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
