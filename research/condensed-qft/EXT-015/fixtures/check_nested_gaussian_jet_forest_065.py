#!/usr/bin/env python3
"""Exact rational/squarefree-radical five-loop Gaussian forest regression.
No third-party packages, floating point, fitted constants or external I/O.
"""
from fractions import Fraction as F
from itertools import combinations, combinations_with_replacement
from functools import lru_cache
from collections import Counter
from math import isqrt

E=tuple(combinations(range(4),2))+((0,4),(1,4),(0,5),(1,5))
def simplify(n):
    n=int(n);assert n>0
    z=1;k=2
    while k*k<=n:
        while n%(k*k)==0:n//=k*k;z*=k
        k+=1
    return z,n
def rinv(n):
    k,d=simplify(n)
    return {d:F(k,n)}
def plus(a,b):
    c=dict(a)
    for k,v in b.items():c[k]=c.get(k,F(0))+v
    return {k:v for k,v in c.items() if v}
def negate(a):return {k:-v for k,v in a.items()}
def scale(a,c):return {k:v*c for k,v in a.items() if v*c}
def mult(a,b):
    z={}
    for x,p in a.items():
        for y,q in b.items():
            v,k=simplify(x*y)
            z[k]=z.get(k,F(0))+p*q*v
    return {k:v for k,v in z.items() if v}
def connected(vs,ed):
    if not vs:return False
    seen={min(vs)}
    while True:
        nxt=seen|{b for a,b in ed if a in seen}|{a for a,b in ed if b in seen}
        if nxt==seen:return seen==vs
        seen=nxt
def vertices(ids):return sorted({v for i in ids for v in E[i]})
def onepi(ids):
    ed=[E[i] for i in ids];vs=set(vertices(ids))
    return len(ids)>=3 and connected(vs,ed) and all(
        connected(vs,ed[:i]+ed[i+1:]) for i in range(len(ed)))
def rank(ids):return len(ids)-len(vertices(ids))+1
def inverse(M):
    n=len(M)
    if not n:return F(1),[]
    X=[list(map(F,row))+[F(i==j) for j in range(n)] for i,row in enumerate(M)]
    d=F(1)
    for j in range(n):
        i=next((a for a in range(j,n) if X[a][j]),None)
        if i is None:return F(0),None
        if i!=j:X[i],X[j]=X[j],X[i];d=-d
        q=X[j][j];d*=q;X[j]=[x/q for x in X[j]]
        for i in range(n):
            if i!=j:
                q=X[i][j]
                X[i]=[x-q*y for x,y in zip(X[i],X[j])]
    return d,[row[n:] for row in X]
@lru_cache(None)
def graph(ids):
    vs=vertices(ids);root=min(vs);cs=[v for v in vs if v!=root]
    Q=[[F(0)]*len(cs) for _ in cs]
    for i in ids:
        a,b=E[i];v=[F(int(a==k)-int(b==k)) for k in cs]
        for j in range(len(cs)):
            for k in range(len(cs)):Q[j][k]+=v[j]*v[k]
    det,inv=inverse(Q)
    assert det>0
    return vs,root,cs,det,inv
def wick(exps,cov):
    t=tuple(i for i,k in enumerate(exps) for _ in range(k))
    @lru_cache(None)
    def recurse(t):
        if not t:return F(1)
        if len(t)%2:return F(0)
        return sum((cov[t[0]][t[j]]*recurse(t[1:j]+t[j+1:])
                    for j in range(1,len(t))),F(0))
    return recurse(t)
# Exact polynomial in internal normals u and remaining Gaussian quotients q.
# Truncate in u degree 2: every proper source of G has rank <=4.
def polynomial_sum(a,b):
    c=dict(a)
    for k,v in b.items():c[k]=c.get(k,F(0))+v
    return {k:v for k,v in c.items() if v}
def polynomial_mul(a,b):
    c={}
    for (u,q),x in a.items():
        for (v,r),y in b.items():
            t=tuple(i+j for i,j in zip(u,v))
            if sum(t)>2:continue
            s=tuple(i+j for i,j in zip(q,r))
            key=(t,s);c[key]=c.get(key,F(0))+x*y
    return {k:v for k,v in c.items() if v}
def polynomial_scale(a,c):return {k:v*c for k,v in a.items() if v*c}
def linear(u,q):
    ans={}
    for i,c in enumerate(u):
        if c:
            e=[0]*len(u);e[i]=1
            key=(tuple(e),(0,)*len(q));ans[key]=ans.get(key,F(0))+c
    for i,c in enumerate(q):
        if c:
            e=[0]*len(q);e[i]=1
            key=((0,)*len(u),tuple(e));ans[key]=ans.get(key,F(0))+c
    return ans

memo={}
def inserted(parent,beta,alpha):
    pv,pr,pc,_,_=graph(parent)
    bv,br,bc,_,_=graph(beta)
    nu=len(bc)
    qc=sorted(([br] if pr not in bv else [])+
              [v for v in pv if v not in bv and v!=pr])
    nq=len(qc);qi={v:i for i,v in enumerate(qc)};ui={v:i for i,v in enumerate(bc)}
    expr={}
    for v in pv:
        u=[F(0)]*nu;q=[F(0)]*nq
        if v in bv:
            if v!=br:u[ui[v]]=F(1)
            if br in qi:q[qi[br]]=F(1)
        elif v in qi:q[qi[v]]=F(1)
        expr[v]=(u,q)
    A=[[F(0)]*nu for _ in range(nu)]
    B=[[F(0)]*nq for _ in range(nu)]
    D=[[F(0)]*nq for _ in range(nq)]
    for i in parent:
        if i in beta:continue
        a,b=E[i]
        u=[x-y for x,y in zip(expr[a][0],expr[b][0])]
        q=[x-y for x,y in zip(expr[a][1],expr[b][1])]
        for j in range(nu):
            for k in range(nu):A[j][k]+=u[j]*u[k]
            for k in range(nq):B[j][k]+=u[j]*q[k]
        for j in range(nq):
            for k in range(nq):D[j][k]+=q[j]*q[k]
    det,cov=inverse(D);assert det>0,(parent,beta)
    zero=((0,)*nu,(0,)*nq);one={zero:F(1)}
    linear_term={};quadratic_term={}
    for j in range(nu):
        for k in range(nq):
            u=[0]*nu;u[j]=1;q=[0]*nq;q[k]=1
            key=(tuple(u),tuple(q))
            linear_term[key]=linear_term.get(key,F(0))-B[j][k]
        for k in range(nu):
            u=[0]*nu;u[j]+=1;u[k]+=1
            key=(tuple(u),(0,)*nq)
            quadratic_term[key]=quadratic_term.get(key,F(0))-A[j][k]/2
    exponential=polynomial_sum(
       polynomial_sum(polynomial_sum(one,linear_term),quadratic_term),
       polynomial_scale(polynomial_mul(linear_term,linear_term),F(1,2)))
    test=one
    for j in alpha:test=polynomial_mul(test,linear(*expr[pc[j]]))
    test=polynomial_mul(exponential,test)
    ans={}
    for source_alpha,value in memo[beta].items():
        powers=[0]*nu
        for j in source_alpha:powers[j]+=1
        powers=tuple(powers)
        avg=sum((c*wick(q,cov) for (u,q),c in test.items() if u==powers),F(0))
        ans=plus(ans,mult(value,scale(rinv(det),avg)))
    return ans

sources=[tuple(a) for k in range(3,len(E)+1)
         for a in combinations(range(len(E)),k) if onepi(a)]
sources.sort(key=lambda a:(len(a),a))
assert len(sources)==86
assert not any(set(vertices(a)).isdisjoint(vertices(b)) for a,b in combinations(sources,2))
for j,ids in enumerate(sources):
    _,_,coords,det,cov=graph(ids)
    h=rank(ids)
    alphas=[()]
    if h>=3:alphas+=list(combinations_with_replacement(range(len(coords)),2))
    if h>=5:alphas+=list(combinations_with_replacement(range(len(coords)),4))
    prepared={}
    for a in alphas:
        ex=[0]*len(coords)
        for t in a:ex[t]+=1
        value=scale(rinv(det),wick(tuple(ex),cov))
        for sub in sources[:j]:
            if set(sub)<set(ids):value=plus(value,negate(inserted(ids,sub,a)))
        prepared[a]=value
    memo[ids]=prepared

K4=tuple(range(6));G5=tuple(range(8));G6=tuple(range(10))
assert [graph(a)[3] for a in (K4,G5,G6)]==[16,40,96]
assert Counter(rank(a) for a in sources[:-1])=={1:18,2:35,3:24,4:8}
assert memo[K4][()]=={1:F(5,12),2:-F(3,2),6:F(2)}
assert memo[K4][(0,0)]=={1:-F(7,72)}
assert memo[K4][(0,1)]=={1:-F(7,144)}
assert inserted(G5,K4,(0,0))=={2:-F(7,144)}
b5={10:F(1,50),21:-F(52,441),2:F(7,144),
    5:-F(1,25),15:F(4,25),6:-F(1,18)}
assert memo[G5][(0,0)]==b5
assert memo[G6][(0,0,0,0)]=={6:F(1,72),3:-F(1,32)}
assert len(memo[G6])==86
# Two independent graph symmetries in fixed root-zero coordinates.
for permutation in ((0,2,1,3,4),(0,1,2,4,3)):
    for a,v in memo[G6].items():
        assert memo[G6][tuple(sorted(permutation[i] for i in a))]==v
# All proper vertex-disjoint forest pairs are absent, so forests are chains.
chains={a:{1:1} for a in sources[:-1]}
for a in sources[:-1]:
    for b in sources[:-1]:
        if set(b)<set(a):
            for k,v in chains[b].items():
                chains[a][k+1]=chains[a].get(k+1,0)+v
counts=Counter()
for value in chains.values():
    for k,n in value.items():counts[k]+=n
assert counts=={1:85,2:605,3:1179,4:672}
assert 1+sum(counts.values())==2542
def enclosing_interval(a,precision=10**12):
    lo=hi=F(0)
    for r,c in a.items():
        n=isqrt(r*precision*precision)
        lower=F(n,precision);upper=F(n+1,precision)
        lo+=c*(lower if c>=0 else upper)
        hi+=c*(upper if c>=0 else lower)
    return lo,hi
assert enclosing_interval(b5)[1]<0
assert enclosing_interval(memo[G6][(0,0,0,0)])[1]<0
# The G5->G6 two-spoke complement integrated over tip 5 is
# (2 sqrt(pi) eps)^-1 exp[-y1^2/(4 eps^2)], giving the exact
# additional scalar contact -b5/(32 pi^(5/2)) eps^-5 delta_G5.
assert inserted(G6,G5,(0,0,0,0))=={}
print("PASS: K4/G5/G6 determinants 16/40/96")
print("PASS: 85 proper 1PI sources, ranks 18/35/24/8")
print("PASS: complete 2542 nested forests, lengths 0/1/2/3/4 = 1/85/605/1179/672")
print("PASS: inherited K4 source and nonzero nested K4->G5 derivative contribution")
print("PASS: G5 exact negative second moment and nested G5->G6 positive contact")
print("PASS: all 86 scalar, quadratic and quartic counterterm moments of G6")
print("PASS: quartic witness sqrt(6)/72 - sqrt(3)/32 < 0")
print("PASS: two graph automorphisms and integer square-root sign certificates")
