#!/usr/bin/env python3
"""Exact enumeration of classical B2 Sidon subsets for Erdős #861.

Each unordered pair a<=b (including a=b) has a distinct sum.
Finite enumeration does not establish asymptotic exponents.
"""
import json
from itertools import combinations


def exhaustive(n):
    count=0;maxsize=0;maximizers=[]
    def visit(x, selected, sums):
        nonlocal count,maxsize,maximizers
        if x>n:
            count+=1
            if len(selected)>maxsize:
                maxsize=len(selected);maximizers=[list(selected)]
            elif len(selected)==maxsize and len(maximizers)<4:
                maximizers.append(list(selected))
            return
        visit(x+1,selected,sums)
        news={x+x}|{x+a for a in selected}
        if not (news & sums):
            visit(x+1,selected+[x],sums|news)
    visit(1,[],set())
    return count,maxsize,maximizers


def independent_bitmask(n):
    c=0; f=0
    for mask in range(1<<n):
        A=[i+1 for i in range(n) if mask>>i&1]
        sums=[a+b for i,a in enumerate(A) for b in A[i:]]
        if len(sums)==len(set(sums)):
            c+=1;f=max(f,len(A))
    return c,f


def main():
    cases=[]
    for n in range(1,21):
        count,f,witness=exhaustive(n)
        if n<=13:assert (count,f)==independent_bitmask(n)
        cases.append({'N':n,'sidon_set_count':count,'max_size':f,
                      'ratio_A_to_2powf':f'{count}/{2**f}',
                      'maximizer_sample':witness[0]})
    print(json.dumps({'record_type':'EC_BULK_006_861_FINITE/1',
                      'authority':'EXACT_ENUMERATION_ONLY',
                      'definition':'distinct unordered pair sums, with repetitions a+a allowed',
                      'crosscheck':'independent bitmask enumeration for N<=13',
                      'cases':cases},indent=2))
if __name__=='__main__':main()
