"""Exact local gradient identity, dilute bound and erasure-cylinder witnesses."""
from fractions import Fraction as F
from math import isqrt

def psi(a,x,y):
    return int(a+x+y>=2)

def current(a,x,y,b,lam):
    lam=F(lam)
    if lam<=0 or any(v not in (0,1) for v in (a,x,y,b)):raise ValueError("invalid bits or factor")
    if x==y:return F(0)
    odds=lam**((b-a)*(x-y))
    return (x-y)*odds/(1+odds)

def gradient(a,x,y,b,lam):
    lam=F(lam);c=(1-lam)/(2*(1+lam))
    return F(x-y,2)+c*(psi(a,x,y)-psi(x,y,b))

def dilute_bound2(N,K,lam):
    lam=F(lam)
    if N<5 or not 1<=K<N or lam<=0:raise ValueError("invalid ring")
    R=max(lam,1/lam)**K;c=(1-lam)/(2*(1+lam))
    return 72*c*c*R*R*F(K*(K-1),N-K)

def sqrt_up(q,scale=10**10):
    q=F(q)
    if q<0:raise ValueError("negative square")
    k=isqrt(q.numerator*scale**2//q.denominator)
    if k*k*q.denominator<q.numerator*scale**2:k+=1
    return F(k,scale)

def erasure_gap(a0,r):
    a0,r=F(a0),F(r)
    if not 0<a0<=1 or not 0<r<1:raise ValueError("invalid parameters")
    return (1-r)*a0/3

def noisy_plus(spin,r):
    spin,r=F(spin),F(r)
    if not -1<=spin<=1 or not 0<r<1:raise ValueError("invalid channel")
    return (1-r)*(F(1,2)+spin/6)

def mixture_cylinder(weights,means,r,n):
    """Finite algebraic control: arbitrary mixture of iid stationary components.
    Infinite bilayer proof uses the ergodic theorem, not iid components.
    """
    weights=list(map(F,weights));means=list(map(F,means));r=F(r)
    if len(weights)!=len(means) or min(weights)<=0 or sum(weights)!=1 or n<0:
        raise ValueError("invalid mixture")
    masses=[w*r**n for w in weights]
    targets=[noisy_plus(m,r) for m in means]
    return masses,targets,sum(m*t for m,t in zip(masses,targets))/sum(masses)

def half_density_static(s):
    """s=sqrt(lambda) supplied exactly; static derivative only."""
    s=F(s)
    if s<=0:raise ValueError("invalid factor root")
    q=s/(2*(1+s));dpsi=1+2/(1+s)**2
    return q,dpsi,2/((1+s)*(1+s*s))
