#!/usr/bin/env python3
"""Exact finite tests for EC-BULK-006 #863 and #864; no asymptotic certification."""
from collections import Counter
from fractions import Fraction
from itertools import combinations
import json
from math import isqrt
def sum_admissible(A,r):
    c=Counter(a+b for i,a in enumerate(A) for b in A[i:])
    return max(c.values(),default=0)<=r
def diff_admissible(A,r):
    c=Counter(a-b for a in A for b in A if a>b)
    return max(c.values(),default=0)<=r
def maximal_small(n,r,check):
    counts=0; size=0
    for mask in range(1<<n):
        A=[i+1 for i in range(n) if mask>>i&1]
        if check(A,r):
            counts+=1;size=max(size,len(A))
    return dict(N=n,r=r,maximum=size,number_of_valid_sets=counts)
def almost_sidon(A):
    c=Counter(a+b for i,a in enumerate(A) for b in A[i:])
    bad=[(s,num) for s,num in c.items() if num>1]
    return len(bad)<=1
def incremental_almost(n):
    ans=0;witness=None
    def visit(x,A,sums,bad):
        nonlocal ans,witness
        if x>n:
            if len(A)>ans:ans=len(A);witness=A[:]
            return
        if len(A)+n-x+1<=ans:return
        visit(x+1,A,sums,bad)
        cnt=sums.copy();newbad=bad
        for a in A:cnt[x+a]+=1
        cnt[2*x]+=1
        newbad=sum(v>1 for v in cnt.values())
        if newbad<=1:visit(x+1,A+[x],cnt,newbad)
    visit(1,[],Counter(),0)
    return ans,witness
def brute_almost(n):
    best=0
    for k in range(n+1):
        for A in combinations(range(1,n+1),k):
            if almost_sidon(A):best=k
    return best
def no_nine(n=20):
    checked=0
    for A in combinations(range(1,n+1),9):
        checked+=1
        if almost_sidon(A):return (False,checked,A)
    return (True,checked,None)
def main():
    constants=[]
    for r in range(2,13):
        t=r//2
        # L^2-U^2 = t*t/(r+2*t)>0 by exact fractions
        L2=Fraction((r+t)**2,r+2*t)
        assert L2-Fraction(r,1)==Fraction(t*t,r+2*t)
        constants.append(dict(r=r,t=t,L_squared=str(L2),U_squared=r,gap_squared=str(L2-r)))
    small=[]
    for n in range(3,9):
        for r in (1,2,3):
            small.append(dict(sum=maximal_small(n,r,sum_admissible),difference=maximal_small(n,r,diff_admissible)))
    almost=[]
    for n in range(1,21):
        m,w=incremental_almost(n)
        if n<=12:assert m==brute_almost(n),(n,m,brute_almost(n))
        almost.append(dict(N=n,maximum=m,witness=w))
    assert almost[-1]['maximum']==8,almost[-1]
    w=[1,2,4,8,13,17,19,20]
    assert almost_sidon(w)
    c=Counter(a+b for i,a in enumerate(w) for b in w[i:])
    assert [(s,k) for s,k in sorted(c.items()) if k>1]==[(21,4)]
    nine=no_nine()
    assert nine==(True,167960,None),nine
    print(json.dumps(dict(record_type='EC_BULK_006_863_864_FINITE/1',authority='EXACT_FINITE_ENUMERATION_ONLY',
                          coefficients=constants,small_B2r=small,almost_sidon=almost,
                          N20_nine_subset_certificate={'no_valid_nine':nine[0],'checked':nine[1]},
                          N20_witness=w),indent=2))
if __name__=='__main__':main()
