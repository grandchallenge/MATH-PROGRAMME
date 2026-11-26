"""Exact canonical comparison without enumeration in the producer."""
from fractions import Fraction as F

def elementary(weights,k):
    if k<0 or k>len(weights): return F(0)
    p=[F(1)]+[F(0)]*k
    for w in weights:
        for j in range(k,0,-1): p[j]+=w*p[j-1]
    return p[k]

def moments(weights,k,i,j):
    w=tuple(map(F,weights))
    if not w or any(x<=0 for x in w) or not 0<=k<=len(w):
        raise ValueError("invalid sector")
    if i==j or not (0<=i<len(w) and 0<=j<len(w)):
        raise ValueError("distinct valid sites required")
    z=elementary(w,k)
    rest=[v for h,v in enumerate(w) if h not in (i,j)]
    pi=w[i]*elementary([v for h,v in enumerate(w) if h!=i],k-1)/z
    pj=w[j]*elementary([v for h,v in enumerate(w) if h!=j],k-1)/z
    pij=w[i]*w[j]*elementary(rest,k-2)/z
    c=w[i]*w[j]*(elementary(rest,k-1)**2-elementary(rest,k-2)*elementary(rest,k))/z**2
    assert c==pi*pj-pij
    return pi,pj,pij,c

def comparison_bound(n,s,m,ratio):
    r=F(ratio)
    if not 1<=s<n or not 0<=m<=n-s or r<1:
        raise ValueError("invalid comparison inputs")
    return min(F(1),s*m*(r-1)*r**3/(4*(n-s)))

def exchange_alpha(n,ratio):
    r=F(ratio)
    if n<2 or r<1: raise ValueError("invalid exchange inputs")
    return (1+F(n-2)/(1+r))/F(n*(n-1)//2)
