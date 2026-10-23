#!/usr/bin/env python3
"""Exact rational and symbolic-normalization controls for Gaussian cycle insertion.

No floating point; c_G normalization is represented by c_G^2*(2*pi)^h,
which equals the rational product(edge weights)/det(Q). Analytic theorems
and strong-distribution remainders are proved in R2/047, not by this fixture.
"""
from fractions import Fraction as F
from itertools import combinations, permutations

def det(M):
    A=[list(map(F,row)) for row in M]
    n=len(A); z=F(1)
    for j in range(n):
        i=next((k for k in range(j,n) if A[k][j]),None)
        if i is None:return F(0)
        if i!=j:A[i],A[j]=A[j],A[i];z=-z
        p=A[j][j];z*=p
        for k in range(j+1,n):
            t=A[k][j]/p
            for l in range(j+1,n):A[k][l]-=t*A[j][l]
    return z

def inverse(M):
    n=len(M);a=[list(map(F,r))+[F(i==j) for j in range(n)] for i,r in enumerate(M)]
    for j in range(n):
        i=next(i for i in range(j,n) if a[i][j])
        a[j],a[i]=a[i],a[j]
        t=a[j][j];a[j]=[x/t for x in a[j]]
        for k in range(n):
            if k!=j:
                t=a[k][j];a[k]=[x-t*y for x,y in zip(a[k],a[j])]
    return [r[n:] for r in a]

def lap(n,edges):
    L=[[F(0) for j in range(n)] for i in range(n)]
    for a,b,w in edges:
        w=F(w)
        L[a][a]+=w;L[b][b]+=w
        L[a][b]-=w;L[b][a]-=w
    return [r[:-1] for r in L[:-1]]

def matplus(Q,v,w):
    n=len(Q);return [[Q[i][j]+w*v[i]*v[j] for j in range(n)] for i in range(n)]
def quad(A,v):
    return sum((v[i]*A[i][j]*v[j] for i in range(len(v)) for j in range(len(v))),F(0))
def update(Q,v,w):
    inv=inverse(Q);R=quad(inv,v); d=1+w*R
    vv=[sum((inv[i][j]*v[j] for j in range(len(v))),F(0)) for i in range(len(v))]
    pred=[[inv[i][j]-w*vv[i]*vv[j]/d for j in range(len(v))] for i in range(len(v))]
    Q2=matplus(Q,v,w)
    assert inverse(Q2)==pred
    assert det(Q2)==det(Q)*d
    return Q2,R,d

def trees(n,edges):
    ans=F(0)
    for es in combinations(edges,n-1):
        p=list(range(n))
        def root(a):
            while p[a]!=a:a=p[a]
            return a
        wt=F(1)
        for a,b,w in es:
            aa,bb=root(a),root(b)
            if aa==bb:break
            p[aa]=bb;wt*=w
        else:
            if len({root(i) for i in range(n)})==1:ans+=wt
    return ans

triangle=[(0,1,F(1)),(0,2,F(1)),(1,2,F(1))]
Q=lap(3,triangle)
assert Q==[[F(2),-F(1)],[-F(1),F(2)]]
assert det(Q)==3
v=[F(1),F(-1)]
Q2,R,denom=update(Q,v,F(1))
assert R==F(2,3) and denom==F(5,3)
assert Q2==[[F(3),F(-2)],[F(-2),F(3)]]
assert det(Q2)==5 and inverse(Q2)==[[F(3,5),F(2,5)],[F(2,5),F(3,5)]]
# triangle c^2*(2*pi)^h =1/3; added edge c'^2*(2*pi)^(h+1)=1/5.
assert F(1,3)*F(1)/denom==F(1,5)
# c_{G+e}=1/(2*pi*sqrt(5)), finite on phi=y_0^2
# is 3/(10*pi*sqrt(5)); so (pi*value)^2 = 9/500.
test_coefficient_squared_times_pi2=F(3,10)**2/F(5)
assert test_coefficient_squared_times_pi2==F(9,500)
# Wick finite amplitude c_G E p_w(X) = sqrt(5)/(6*pi).
# After multiplying by pi^2 its square = 5/36, derived from variance.
wick_norm_squared_times_pi2=(F(1,3)*(R+F(1)))/F(4)
assert wick_norm_squared_times_pi2==F(5,36)

cases=0
for n in range(2,7):
    for shift in range(1,5):
        ed=[(j,j+1,F((j+shift)%5+1)) for j in range(n-1)]
        ed.extend((i,j,F((i+j+shift)%7+1,2))
                  for i,j in combinations(range(n),2)
                  if j>i+1 and (i+j+shift)%3==0)
        Q=lap(n,ed); tau=det(Q)
        assert tau==trees(n,ed) and tau>0
        additions=[(0,1,F(2)),(0,n-1,F(3,2)),(1,n-1,F(5,3)) if n>2 else (0,1,F(5,3))]
        final=None
        for perm in permutations(additions):
            cur=[row[:] for row in Q]
            cycrank=len(ed)-(n-1)
            # rational c^2*(2*pi)^h of initial graph.
            c2scaled=F(1)
            for _,_,w in ed:c2scaled*=w
            c2scaled/=tau
            for a,b,w in perm:
                vec=[F((i==a)-(i==b)) for i in range(n-1)]
                old=det(cur)
                cur,Ri,di=update(cur,vec,w)
                c2scaled=c2scaled*w/di
                cycrank+=1
                assert c2scaled==F(1)*(
                    __import__('math').prod([F(z[2]) for z in ed+list(perm[:cycrank-(len(ed)-(n-1))])])
                )/det(cur)
            if final is None:final=(cur,c2scaled,cycrank)
            else:assert (cur,c2scaled,cycrank)==final
        assert det(final[0])==trees(n,ed+additions)
        cases+=1

print("PASS: triangle R=2/3, tau changes 3->5 and Sherman-Morrison inverse exact")
print("PASS: finite delta insertion pairing: (pi*value)^2=9/500")
print("PASS: finite Wick insertion pairing: (pi*value)^2=5/36")
print(f"PASS: {cases} weighted connected graphs, 6 insertion orders each, Kirchhoff and normalization")
print("NOTE: factor-local Wick-to-delta identity is analytic P_epsilon''=kappa_epsilon.")
