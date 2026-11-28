"""Rational time-residual certificates and finite-range canonical marginals."""
from fractions import Fraction as F
from itertools import product
from math import isqrt

def dot(a,b):return sum(x*y for x,y in zip(a,b))

def solve(A,b):
    n=len(b); M=[list(map(F,row))+[F(v)] for row,v in zip(A,b)]
    for j in range(n):
        i=next((i for i in range(j,n) if M[i][j]),None)
        if i is None:raise ValueError("dependent trial basis")
        M[j],M[i]=M[i],M[j];v=M[j][j];M[j]=[a/v for a in M[j]]
        for i in range(n):
            if i!=j:
                v=M[i][j]
                if v:M[i]=[a-v*b for a,b in zip(M[i],M[j])]
    return [r[-1] for r in M]

def sqrt_up(x,scale=10**12):
    x=F(x)
    if x<0:raise ValueError("negative squared norm")
    k=isqrt(x.numerator*scale**2//x.denominator)
    if k*k*x.denominator<x.numerator*scale**2:k+=1
    return F(k,scale)

def time_certificate(gram,stiff,leak,f,T,n):
    """Gram <u,u>, stiffness <u,G u>, leakage <(I-P)G u,(I-P)G u>.
    Caller supplies exact consistent forms from a reversible generator.
    """
    T=F(T)
    if T<=0 or n<2:raise ValueError("invalid horizon")
    h=T/n;d=len(f)
    H=[[gram[i][j]-h*stiff[i][j] for j in range(d)] for i in range(d)]
    v=list(map(F,f))
    base=F(2,n)*sqrt_up(dot(v,[dot(row,v) for row in gram]))
    total=F(0)
    for _ in range(n):
        v=solve(H,[dot(row,v) for row in gram])
        total+=h*sqrt_up(dot(v,[dot(row,v) for row in leak]))
    return v,base,total

def ring_partition(w,lam,K,fixed=None):
    """Transfer recursion for fixed count and pinned local bits."""
    w=list(map(F,w));lam=list(map(F,lam));N=len(w);fixed=dict(fixed or {})
    if N<3 or len(lam)!=N or not 0<=K<=N or min(w+lam)<=0:
        raise ValueError("invalid ring")
    if any(not 0<=i<N or b not in (0,1) for i,b in fixed.items()):
        raise ValueError("invalid pinned bit")
    z=F(0)
    for first in (0,1):
        if fixed.get(0,first)!=first or first>K:continue
        dp={(first,first):w[0]**first}
        for i in range(1,N):
            nd={}
            for (a,k),v in dp.items():
                for b in (0,1):
                    if k+b>K or fixed.get(i,b)!=b:continue
                    key=(b,k+b);nd[key]=nd.get(key,0)+v*w[i]**b*lam[i-1]**(a*b)
            dp=nd
        z+=sum(v*lam[-1]**(a*first) for (a,k),v in dp.items() if k==K)
    return z

class Ring:
    def __init__(self,w,lam,K):
        self.w=tuple(map(F,w));self.lam=tuple(map(F,lam));self.K=K;self.N=len(w)
        self.z=ring_partition(w,lam,K);self.cache={}
    def prob(self,bits):
        key=tuple(sorted(bits.items()))
        if key not in self.cache:self.cache[key]=ring_partition(self.w,self.lam,self.K,bits)/self.z
        return self.cache[key]
    def cylinder(self,S,fn):
        S=tuple(sorted(set(S)))
        return (S,{v:F(fn(dict(zip(S,v)))) for v in product((0,1),repeat=len(S))})
    def inner(self,f,g):
        S,V=f;R,W=g;U=tuple(sorted(set(S)|set(R)))
        val=F(0)
        for bits in product((0,1),repeat=len(U)):
            a=dict(zip(U,bits));x=V[tuple(a[i] for i in S)];y=W[tuple(a[i] for i in R)]
            if x and y:val+=x*y*self.prob(a)
        return val
    def action(self,f):
        """Local cylinder summands of Gf, no global sector construction."""
        S,V=f;N=self.N;out=[]
        for i in range(N):
            j=(i+1)%N
            if i not in S and j not in S:continue
            U=set(S)|{(i-1)%N,i,j,(j+1)%N}
            es={(i-1)%N,i,j}
            def val(a):
                if a[i]==a[j]:return 0
                b=dict(a);b[i],b[j]=b[j],b[i]
                def mass(x):
                    z=self.w[i]**x[i]*self.w[j]**x[j]
                    for k in es:z*=self.lam[k]**(x[k]*x[(k+1)%N])
                    return z
                p=mass(b)/(mass(a)+mass(b))
                return p*(V[tuple(b[k] for k in S)]-V[tuple(a[k] for k in S)])
            out.append(self.cylinder(U,val))
        return out
    def forms(self,trial):
        """Each basis observable is a sum of cylinders."""
        G=[sum((self.action(f) for f in v),[]) for v in trial]
        def inn(a,b):return sum((self.inner(f,g) for f in a for g in b),F(0))
        gram=[[inn(a,b) for b in trial] for a in trial]
        stiff=[[inn(a,b) for b in G] for a in trial]
        second=[[inn(a,b) for b in G] for a in G]
        coeff=[solve(gram,[row[j] for row in stiff]) for j in range(len(trial))]
        leak=[[second[i][j]-dot([row[i] for row in stiff],coeff[j]) for j in range(len(trial))] for i in range(len(trial))]
        return gram,stiff,leak

def collision(p):
    p=list(map(F,p));z=sum(a*a for a in p)
    if min(p)<0 or sum(p)!=1:raise ValueError("invalid marginal")
    return z,[a*a/z for a in p]

def ising_torus_counts(L,aligned=16):
    """Integer one-layer partition by up-spin count; width budget 4.
    Aligned-bond weight exp(2 beta), anti-aligned weight 1.
    """
    if L!=4 or not isinstance(aligned,int) or aligned<1:raise ValueError("reference width budget")
    rows=list(range(1<<L)); mask=(1<<L)-1
    cnt=[i.bit_count() for i in rows]
    hor=[aligned**(L-(i^(((i<<1)&mask)|(i>>(L-1)))).bit_count()) for i in rows]
    ver=[[aligned**(L-(i^j).bit_count()) for j in rows] for i in rows]
    z=[0]*(L*L+1)
    for first in rows:
        dp={(first,cnt[first]):hor[first]}
        for _ in range(1,L):
            nd={}
            for (a,k),v in dp.items():
                for b in rows:
                    key=(b,k+cnt[b]);nd[key]=nd.get(key,0)+v*hor[b]*ver[a][b]
            dp=nd
        for (a,k),v in dp.items():z[k]+=v*ver[a][first]
    return z
