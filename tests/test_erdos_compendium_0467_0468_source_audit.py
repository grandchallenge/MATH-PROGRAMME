"""Exact finite checks for EC-BULK-004 #467/#468; no asymptotic proof."""
from math import isqrt

def primes(n):
    s=[True]*(n+1)
    s[0:2]=[False,False]
    for p in range(2,isqrt(n)+1):
        if s[p]:
            for j in range(p*p,n+1,p):s[j]=False
    return [p for p in range(2,n+1) if s[p]]

def tree(V,w):
    if len(V)<2:return 0
    seen={V[0]};left=set(V[1:]);total=0
    while left:
        score,v=max((w[min(u,v),max(u,v)],v) for u in seen for v in left)
        total+=score;seen.add(v);left.remove(v)
    return total

def forest(N,P):
    w={(i,j):N//(P[i]*P[j]) for i in range(len(P)) for j in range(i+1,len(P))}
    best=None
    for mask in range(1<<len(P)):
        a=[i for i in range(len(P)) if mask>>i&1]
        b=[i for i in range(len(P)) if not(mask>>i&1)]
        z=tree(a,w)+tree(b,w)
        best=z if best is None else min(best,z)
    return best

def deficit(p):
    N=p-1;P=primes(p)
    return sum((N+q-1)//q for q in P)-2*N-forest(N,P[:10])

def prefixes(M):
    d=[[] for _ in range(M+1)]
    for x in range(2,M+1):
        for n in range(x,M+1,x):d[n].append(x)
    first={};new=0
    for n in range(1,M+1):
        s=0
        for x in d[n]:
            s+=x
            if s not in first:first[s]=n;new+=1
    return first,new

def test_0467_all_prime_endpoints_below_607():
    assert all(deficit(p)<0 for p in primes(606))

def test_0467_cutoff_is_not_a_solution():
    assert deficit(601)==-1
    assert deficit(607)==1

def test_0467_crt_pair_intersections():
    for p,q in [(2,3),(3,5),(5,7),(7,11)]:
        N=601
        for a in range(p):
            for b in range(q):
                assert sum(n%p==a and n%q==b for n in range(1,N+1))>=N//(p*q)

def test_0468_first_1000():
    f,n=prefixes(1000)
    assert n==924 and f[17]==10

def test_0468_first_10000():
    f,n=prefixes(10000)
    assert n==8697
    assert sum(f.get(N,10001)>10000 for N in range(1,10001))==2969

def test_0468_undefined_small_values():
    f,_=prefixes(10000)
    assert 1 not in f and 4 not in f and f[28]==102
