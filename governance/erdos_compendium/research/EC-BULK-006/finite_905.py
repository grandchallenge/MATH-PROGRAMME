#!/usr/bin/env python3
"""Exact finite clique-book bound for Erdős #905, not full 1979 theorem."""
from itertools import combinations
from math import comb
import json
def enumerate_n(n):
    E=list(combinations(range(n),2)); N=len(E)
    eligible=0;exact_boundary=0; minbook=None;minexample=None
    for mask in range(1<<N):
        m=mask.bit_count()
        # K_{floor(n/2),ceil(n/2)} gives m=floor(n²/4)
        if 4*m==n*n:exact_boundary+=1
        if 4*m<=n*n:continue
        eligible+=1
        adj=[0]*n
        for i,(a,b) in enumerate(E):
            if mask>>i&1:
                adj[a]|=1<<b
                adj[b]|=1<<a
        books=[(adj[a]&adj[b]).bit_count() for i,(a,b) in enumerate(E) if mask>>i&1]
        assert len(books)==m
        maxbook=max(books)
        assert 6*maxbook>=n,(n,m,maxbook,mask)
        if minbook is None or maxbook<minbook:
            minbook=maxbook
            minexample=([list(e) for i,e in enumerate(E) if mask>>i&1],m)
    return dict(n=n,all_graphs=1<<N,graphs_above_threshold=eligible,
         observed_minimum_of_maximum_booksize=minbook,
         corresponding_edges=minexample[0] if minexample is not None and n<=4 else None,
         corresponding_edge_count=minexample[1] if minexample is not None else None,
         ings='all triangle-book counts via bit-intersection exact')
def check_bipartite_threshold():
    r=[]
    for n in range(2,9):
        a=n//2;b=n-a
        assert a*b==n*n//4
        # Balanced complete bipartite has NO triangles, illustrating why
        # the hypothesis is strict > rather than >=.
        r.append(dict(n=n,edges=a*b,max_booksize=0,threshold_floor=n*n//4))
    return r
def main():
    rows=[enumerate_n(n) for n in range(2,7)]
    assert sum(x['all_graphs'] for x in rows)==33866
    assert all(x['graphs_above_threshold']>0 for x in rows[1:])
    print(json.dumps(dict(record_type='EC_BULK_006_905_FINITE/1',
      authority='exact finite graph orders 2..6 only; general Khadzhiivanov–Nikiforov proof imported',
      integer_predicate='4*m>n*n implies exists edge with 6*common_neighbours>=n',
      rows=rows,sharp_strict_threshold_examples=check_bipartite_threshold()),indent=2))
if __name__=='__main__':main()
