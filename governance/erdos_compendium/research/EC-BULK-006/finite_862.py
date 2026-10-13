#!/usr/bin/env python3
"""Exact Sidon and inclusion-maximal Sidon enumeration; no asymptotic claims."""
import json
from itertools import combinations

def maximal(A, sums, n):
    chosen=set(A)
    for x in range(1,n+1):
        if x not in chosen:
            new={2*x}|{x+a for a in A}
            if not (sums & new):
                return False
    return True

def enumerate_backtracking(n):
    total=maximal_count=maximum=0
    def visit(x,A,sums):
        nonlocal total,maximal_count,maximum
        if x>n:
            total+=1
            maximum=max(maximum,len(A))
            maximal_count+=maximal(A,sums,n)
            return
        visit(x+1,A,sums)
        new={2*x}|{x+a for a in A}
        if not (new & sums):
            visit(x+1,A+[x],sums|new)
    visit(1,[],set())
    return total,maximal_count,maximum

def brute(n):
    total=mc=maximum=0
    for k in range(n+1):
        for A in combinations(range(1,n+1),k):
            sums=[a+b for i,a in enumerate(A) for b in A[i:]]
            if len(sums)!=len(set(sums)):continue
            total+=1
            maximum=max(maximum,k)
            mc+=maximal(A,set(sums),n)
    return total,mc,maximum

def main():
    receipt=[]
    for n in [1,2,3,4,5,6,7,8,9,10,12,14,18]:
        a=enumerate_backtracking(n)
        assert a==brute(n) if n<=12 else True,(n,a)
        assert a[0]<=a[1]*2**a[2],(n,a)
        receipt.append(dict(N=n,A=a[0],A1=a[1],f=a[2],
                            independent_brute_check=n<=12))
    data=dict(record_type='EC_BULK_006_862_FINITE/1',
              authority='EXACT_FINITE_ENUMERATION_ONLY',
              definition='unordered pair sums including doubles; inclusion-maximal',
              cases=receipt)
    assert next(x for x in receipt if x['N']==10)['A1']==64
    assert next(x for x in receipt if x['N']==18)['A1']==1086
    print(json.dumps(data,indent=2))
if __name__=='__main__':main()
