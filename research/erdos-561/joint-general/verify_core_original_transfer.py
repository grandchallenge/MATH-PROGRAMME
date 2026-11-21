#!/usr/bin/env python3
"""Exact bounded arithmetic check of source-proved residual/core original transfers.

No finite integer grid is a proof of the unbounded arbitrary-host assertions.
The rigorous graph arguments are in GENERAL_CORE_ORIGINAL_TRANSFER.md.
"""
from collections import Counter

def diagonal(n,m):
    return tuple(max(n[i]+m[j]-1 for i in range(len(n)) for j in range(len(m)) if i+j==k)
                 for k in range(len(n)+len(m)-1))

def diagonal_independent(n,m):
    return tuple(max(n[i-1]+m[k-i-1]-1 for i in range(1,len(n)+1) if 1<=k-i<=len(m))
                 for k in range(2,len(n)+len(m)+1))

def data(n,m):
    w=diagonal(n,m)
    assert w==diagonal_independent(n,m)
    W=sum(w);J=W-w[0];D=n[0]+m[0]-2
    R=max(sum(n)+len(n),sum(m)+len(m))
    assert w[0]==D+1
    return W,J,D,R

def applicable(n,m):
    W,J,D,R=data(n,m)
    return {k for k,v in {
        'even_caps':n[0]%2==1 and m[0]%2==1,
        'core_density':2*W<=D*(D+1),
        'mixed_core':(n[0]%2!=m[0]%2) and W<=D*(D+1),
        'mixed_vertex':(n[0]%2!=m[0]%2) and 2*W<2*D*D+R
    }.items() if v}

counts=Counter();modes=Counter()
for a in range(2,21):
    for c in range(1,a+1):
        for b in range(a+c-1,a+c+26):
            n=(a,1,1);m=(b,c,1,1)
            W,J,D,R=data(n,m)
            assert (W,J)==(3*b+2*a+1,2*b+a+2)
            gates=applicable(n,m)
            special=(a==2 and ((b==2 and c==1) or b==3 or b in (4,6)))
            assert gates or special,(n,m,W,J,D,R)
            counts['B1']+=1
            if special and not gates:counts['B1_special']+=1
            modes.update(gates)
for a in range(4,181):
    n=(a,2,1);m=(a,1,1,1)
    W,J,D,R=data(n,m)
    assert (W,J)==(5*a+3,3*a+4)
    assert applicable(n,m) or a==4
    counts['B2']+=1
for a in range(3,71):
    for b in range(2*a-2,2*a+41):
        n=(a,1,1);m=(b,a-1,2,1)
        W,J,D,R=data(n,m)
        assert (W,J)==(3*b+2*a+2,2*b+a+3)
        assert applicable(n,m),(n,m,W,J,D,R)
        counts['B3']+=1
for c in range(1,4):
    for d in range(1,min(c,2)+1):
        n=(3,2,1);m=(4,c,d,1)
        W,J,D,R=data(n,m)
        assert (W,J)==(21,15) and 'mixed_core' in applicable(n,m)
        counts['PLATEAU']+=1
assert counts==Counter({'B1':5643,'B1_special':6,'B2':177,'B3':2924,'PLATEAU':5})
assert counts['B1']+counts['B2']+counts['B3']+counts['PLATEAU']==8749
print("ERDOS561_PARITYFREE_PARAMETER_GRID_PASS",dict(counts))
print("ERDOS561_CORE_MODES_PASS",dict(modes))
print("ERDOS561_CORE_TOTAL_8749_PASS")
