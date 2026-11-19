#!/usr/bin/env python3
"""Exact independent integer filter; the general theorem is in the proof text."""
from itertools import combinations_with_replacement
from collections import Counter
import hashlib,json
def diagonals(n,m):
    return [max(n[i]+m[j]-1 for i in range(3) for j in range(3) if i+j==k) for k in range(5)]
def run():
    tr=[(a,b,c) for a in range(2,10) for b in range(1,a+1) for c in range(1,b+1)]
    stats=Counter();bad=[];remaining=[]
    for n in tr:
        for m in tr:
            D=n[0]+m[0]-2
            if D>=10:continue
            stats['small_pairs']+=1
            W=sum(diagonals(n,m));E=W-1;T=D*(D+1)//2
            if E<T:stats['edge_budget']+=1;continue
            r=sum(n)+3;b=sum(m)+3;R=max(r,b);B=2*E-D*D+1
            if R>B:stats['vertex_budget']+=1;continue
            if R==B and min(r,b)>D+1 and E-T<max(n[0],m[0]):
                stats['older_equality_gate']+=1;continue
            stats['baseline']+=1
            delta=B-R;t=E-T
            if 0<=delta<=D-2 and t>delta:
                bad.append((n,m,delta,D))
                stats['new_excluded']+=1
            else:remaining.append((n,m))
    stats['remaining']=len(remaining)
    assert (stats['small_pairs'],stats['edge_budget'],stats['vertex_budget'],
            stats['older_equality_gate'],stats['baseline'],stats['new_excluded'],stats['remaining'])==(4566,2725,918,72,851,316,535),stats
    pairs=sorted([[list(n),list(m)] for n,m,_,_ in bad])
    h=hashlib.sha256(json.dumps(pairs,separators=(',',':')).encode()).hexdigest()
    assert h=="d2d741b5432bacce00fc5fc2a7394b54f966c66c9478dcbcb0e4e6b5e33df91b",h
    return {'counts':dict(stats),'by_slack':dict(sorted(Counter(x[2] for x in bad).items())),
      'by_degree':dict(sorted(Counter(x[3] for x in bad).items())),'pair_set_sha256':h}
if __name__=="__main__":print(json.dumps(run(),indent=2))
