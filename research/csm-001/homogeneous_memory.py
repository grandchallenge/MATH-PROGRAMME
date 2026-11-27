"""Homogeneous conservative exchange: exact finite projection and mode controls."""
from fractions import Fraction as F
from itertools import combinations
from math import comb, cos, exp, pi
from cmath import exp as cexp

def sector(n,k,budget=256):
    if not 0<=k<=n or comb(n,k)>budget:raise ValueError("sector budget")
    return [tuple(int(i in a) for i in range(n)) for a in combinations(range(n),k)]

def ring(n):
    if n<4:raise ValueError("ring too small")
    return [(i,i+1) for i in range(n-1)]+[(0,n-1)]

def generator(xs,bonds,w,edges):
    n=len(w);ids={x:i for i,x in enumerate(xs)}
    if not bonds or len(set(bonds))!=len(bonds) or any(not 0<=i<j<n for i,j in bonds):raise ValueError("invalid bonds")
    if any(F(v)<=0 for v in w) or any(not 0<=i<j<n or F(v)<=0 for i,j,v in edges):raise ValueError("invalid factors")
    mass=[]
    for x in xs:
        a=F(1)
        for i,v in enumerate(w):a*=F(v)**x[i]
        for i,j,v in edges:a*=F(v)**(x[i]*x[j])
        mass.append(a)
    L=[[F(0) for _ in xs] for _ in xs]
    for a,x in enumerate(xs):
        for i,j in bonds:
            if x[i]==x[j]:continue
            y=list(x);y[i],y[j]=y[j],y[i];b=ids[tuple(y)]
            r=mass[b]/(mass[a]+mass[b]);L[a][b]+=r;L[a][a]-=r
    z=sum(mass);return L,[a/z for a in mass]

def mm(A,B):return [[sum(a*b for a,b in zip(row,col)) for col in zip(*B)] for row in A]
def mv(A,b):return [sum(x*y for x,y in zip(row,b)) for row in A]
def dot(a,b,p):return sum(x*y*w for x,y,w in zip(a,b,p))
def sub(A,B):return [[a-b for a,b in zip(r,s)] for r,s in zip(A,B)]
def identity(n):return [[F(i==j) for j in range(n)] for i in range(n)]

def projection(labels,p):
    masses={}
    for k,w in zip(labels,p):masses[k]=masses.get(k,F(0))+w
    return [[w/masses[k] if k==l else F(0) for l,w in zip(labels,p)] for k in labels]

def decomposition(L,P):
    Q=sub(identity(len(L)),P)
    return mm(mm(P,L),P),mm(mm(Q,L),Q),mm(mm(Q,L),P),Q

def hs2(B,p):
    """Squared Hilbert-Schmidt norm in L2(pi), an exact upper bound on norm^2."""
    return sum(p[i]*a*a/p[j] for i,row in enumerate(B) for j,a in enumerate(row))

def residual_bound2(B,p,g,t,f):
    if F(g)<=0 or F(t)<0:raise ValueError("invalid gap or horizon")
    return F(t)*hs2(B,p)*dot(f,f,p)/(2*F(g))

def ring_correlations(n,ell,t):
    """Exact Fourier formula evaluated numerically; no sector enumeration."""
    if ell<1 or n%ell or n//ell<3 or t<0:raise ValueError("invalid scale")
    M=n//ell
    physical=0.
    for l in range(ell):
        k=1+l*M
        coeff=sum(cexp(-2j*pi*k*j/n) for j in range(ell))/ell
        physical+=abs(coeff)**2*exp(-t*(1-cos(2*pi*k/n)))
    naive=exp(-t*(1-cos(2*pi/M))/ell)
    corrected=exp(-t*(1-cos(2*pi/n)))
    return physical,naive,corrected

def phase_certificate(n,lam):
    lam=F(lam)
    if n<4 or n%2 or not 0<lam<1:raise ValueError("invalid phase control")
    return F(2)/(2+(comb(n,n//2)-2)*lam),n*lam/(1+lam)
