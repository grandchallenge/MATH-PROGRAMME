#!/usr/bin/env python3
"""Independent finite maximal-sum-free counts, with a+a=b forbidden."""
import json
from itertools import combinations

def sum_free(A):
    s=set(A)
    return all(a+b not in s for a in s for b in s)

def is_maximal_direct(A,n):
    s=set(A)
    return sum_free(s) and all(not sum_free(s|{x}) for x in range(1,n+1) if x not in s)

def maximal_by_obstructions(A,n):
    s=set(A)
    if not sum_free(s):return False
    for x in range(1,n+1):
        if x in s:continue
        # Adding x creates a forbidden Schur triple iff x is either
        # a summand of z=x+a, or the sum x=a+b (including a=b), or z=2*x.
        witness=(2*x in s or any(x+a in s for a in s)
                 or any(a+b==x for a in s for b in s))
        if not witness:return False
    return True

def enumerate_masks(n):
    total=maximal=maximum=0
    witnesses=[]
    for mask in range(1<<n):
        A=tuple(i+1 for i in range(n) if mask>>i&1)
        if not sum_free(A):continue
        total+=1;maximum=max(maximum,len(A))
        if maximal_by_obstructions(A,n):
            maximal+=1
            if len(witnesses)<3:witnesses.append(list(A))
        if n<=11:
            assert maximal_by_obstructions(A,n)==is_maximal_direct(A,n)
    return {'n':n,'sum_free':total,'maximal_sum_free':maximal,
            'largest_size':maximum,'example_maximal_sets':witnesses}

def main():
    rows=[enumerate_masks(n) for n in range(1,17)]
    for row in rows:
        assert row['sum_free']>=2**((row['n']+1)//2)
        assert row['sum_free']>=row['maximal_sum_free']>0
    print(json.dumps({'record_type':'EC_BULK_006_877_FINITE/1',
                      'authority':'EXACT_FINITE_ENUMERATION_ONLY',
                      'definition':'sum-free includes doubled terms a+a; inclusion-maximal within [n]',
                      'independent_maximal_checks':'obstruction criterion versus direct extension for n<=11',
                      'cases':rows},indent=2))
if __name__=='__main__':main()
