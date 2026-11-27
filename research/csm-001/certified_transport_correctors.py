"""Exact rational Galerkin residual certificates; mean-field phase diagnostics."""
from fractions import Fraction as F
from math import exp, lgamma

def dot(a,b,p):
    return sum(x*y*w for x,y,w in zip(a,b,p))

def mv(A,x):
    return [sum(a*b for a,b in zip(row,x)) for row in A]

def add(x,y,c=1):
    return [a+c*b for a,b in zip(x,y)]

def solve(A,b):
    n=len(b); T=[list(map(F,row))+[F(v)] for row,v in zip(A,b)]
    for i in range(n):
        k=next((k for k in range(i,n) if T[k][i]),None)
        if k is None:raise ValueError("singular Gram system")
        T[i],T[k]=T[k],T[i]
        v=T[i][i];T[i]=[x/v for x in T[i]]
        for k in range(n):
            if k!=i:
                v=T[k][i];T[k]=add(T[k],T[i],-v)
    return [row[-1] for row in T]

def orthogonal(vs,p):
    """Rational orthogonal basis; no eigenvectors."""
    out=[]
    for v in vs:
        w=list(map(F,v))
        for u in out:w=add(w,u,-dot(w,u,p)/dot(u,u,p))
        if dot(w,w,p):out.append(w)
    return out

def galerkin(H,b,p,trial,g):
    """g is a supplied valid positive lower bound on H on the residual space."""
    g=F(g)
    if g<=0:raise ValueError("positive coercivity bound required")
    V=orthogonal(trial,p)
    HV=[mv(H,v) for v in V]
    G=[[dot(u,v,p) for v in HV] for u in V]
    c=solve(G,[dot(v,b,p) for v in V])
    x=[F(0)]*len(b)
    for a,v in zip(c,V):x=add(x,v,a)
    hx=mv(H,x);r=add(b,hx,-1)
    J=2*dot(b,x,p)-dot(x,hx,p)
    return {"dimension":len(V),"trial":x,"residual":r,"lower":J,"upper":J+dot(r,r,p)/g}

def shifted(L,z):
    return [[F(z)*int(i==j)-v for j,v in enumerate(row)] for i,row in enumerate(L)]

def relative_trace(L,D,B,p,retained,trial,z,g=0):
    """All retained-space form certificate, not a single-target assertion."""
    z,g=F(z),F(g)
    if z<=0 or g<0:raise ValueError("invalid shifts")
    V=orthogonal(retained,p)
    H=shifted(D,z);J=shifted(L,z)
    bs=[mv(B,v) for v in V]
    sol=[galerkin(H,b,p,trial,z+g) for b in bs]
    C=[[dot(u,mv(J,v),p)-dot(b,s["trial"],p)
        for v,s in zip(V,sol)] for u,b in zip(V,bs)]
    R=[[dot(u["residual"],v["residual"],p)/(z+g) for v in sol] for u in sol]
    eta=sum(solve(C,[row[j] for row in R])[j] for j in range(len(V)))
    return eta,C,R

def phase_bounds(n):
    """beta=log(4), exact conservative bounds for N divisible by 4."""
    if n<8 or n%4:raise ValueError("phase bound requires N>=8 divisible by four")
    b=F(1,2**(n-3))
    return b,2*n*b/(1-b),F(1,2**(1+n//2))

def phase_mass(n,beta):
    """Floating evaluation of exact multiplicity formula (not interval enclosure)."""
    if n<4 or n%4 or beta<=0:raise ValueError("invalid phase model")
    m=n//2
    values=[4*a/n-1 for a in range(m+1)]
    logw=[2*(lgamma(m+1)-lgamma(a+1)-lgamma(m-a+1))+beta*n*s*s
          for a,s in enumerate(values)]
    peak=max(logw);w=[exp(x-peak) for x in logw];z=sum(w)
    p=[x/z for x in w]
    return {"band":sum(x for x,s in zip(p,values) if abs(s)<=4/n+1e-14),
            "second_moment":sum(x*s*s for x,s in zip(p,values)),
            "central_half":sum(x for x,s in zip(p,values) if abs(s)<=0.5),
            "sign_variance":sum(x for x,s in zip(p,values) if s!=0)}
