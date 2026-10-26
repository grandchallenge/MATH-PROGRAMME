#!/usr/bin/env python3
"""Exact rational/radical and forest controls for EXT-015 R2/057.

This regression independently computes local source coefficients and overall
delta/delta-jet poles. It does not replace the analytic distributional proof.
"""
from fractions import Fraction as F
from itertools import combinations
from collections import Counter

EDGES=((0,1),(1,2),(0,2),(3,4),(4,5),(3,5),(0,3),(1,4))

def rootrad(n):
    m=n;fac=1;d=2
    while d*d<=m:
        while m%(d*d)==0:
            m//=d*d;fac*=d
        d+=1
    return {m:F(fac)}

def mul(x,y):
    out={}
    for a,c in x.items():
        for b,d in y.items():
            for k,z in rootrad(a*b).items():
                out[k]=out.get(k,F(0))+c*d*z
    return {k:v for k,v in out.items() if v}
def add(x,y):
    out=dict(x)
    for k,v in y.items():out[k]=out.get(k,F(0))+v
    return {k:v for k,v in out.items() if v}
def scale(x,z):return {k:v*z for k,v in x.items() if v*z}
def invroot(n):return scale(rootrad(n),F(1,n))
def S(x=0):return {1:F(x)} if x else {}

def connected(edges,vs):
    if not vs:return False
    seen={min(vs)}
    while True:
        nxt=seen|{b for a,b in edges if a in seen}|{a for a,b in edges if b in seen}
        if nxt==seen:return seen==vs
        seen=nxt
def onepi(ids):
    edges=[EDGES[i] for i in ids]
    vs={v for e in edges for v in e}
    return len(ids)>=3 and connected(edges,vs) and all(
        connected(edges[:j]+edges[j+1:],vs) for j in range(len(ids)))
def V(ids):return {v for i in ids for v in EDGES[i]}
P=[frozenset(t) for k in range(3,8)
   for t in combinations(range(8),k) if onepi(t)]
P.sort(key=lambda z:(len(z),tuple(sorted(z))))
assert Counter(map(len,P))=={3:2,4:1,5:2,6:3,7:2}
assert len(P)==10
def compatible(a,b):
    return a<b or b<a or not (V(a)&V(b))
forests=[t for k in range(len(P)+1)
         for t in combinations(P,k)
         if all(compatible(a,b) for a,b in combinations(t,2))]
assert Counter(map(len,forests))=={0:1,1:10,2:13}
disjoint=[t for t in forests if len(t)==2 and not(V(t[0])&V(t[1]))]
assert len(disjoint)==1 and {frozenset((0,1,2)),frozenset((3,4,5))}==set(disjoint[0])

def det(a):
    a=[list(map(F,r)) for r in a];n=len(a);p=F(1)
    for j in range(n):
        i=next((k for k in range(j,n) if a[k][j]),None)
        if i is None:return F(0)
        if i!=j:a[j],a[i]=a[i],a[j];p=-p
        v=a[j][j];p*=v
        for i in range(j+1,n):
            t=a[i][j]/v
            for k in range(j+1,n):a[i][k]-=t*a[j][k]
    return p
def inverse(m):
    n=len(m);a=[list(map(F,row))+[F(i==j) for j in range(n)] for i,row in enumerate(m)]
    for j in range(n):
        i=next(i for i in range(j,n) if a[i][j])
        a[i],a[j]=a[j],a[i]
        q=a[j][j];a[j]=[v/q for v in a[j]]
        for i in range(n):
            if i!=j:
                q=a[i][j];a[i]=[v-q*w for v,w in zip(a[i],a[j])]
    return [row[n:] for row in a]
def quotient(parent_edges,groups,vs,root):
    parent={v:v for v in vs}
    def find(v):
        while parent[v]!=v:v=parent[v]
        return v
    for group in groups:
        vv=sorted(V(group))
        for v in vv[1:]:parent[find(v)]=find(vv[0])
    cls={v:find(v) for v in vs}
    roots=sorted(set(cls.values()));base=cls[root];others=[x for x in roots if x!=base]
    ix={v:i for i,v in enumerate(others)}
    q=[[F(0)]*len(others) for _ in others]
    removed=set().union(*groups) if groups else set()
    for e in parent_edges:
        if e in removed:continue
        a,b=EDGES[e];a,b=cls[a],cls[b]
        if a==b:continue
        if a!=base:q[ix[a]][ix[a]]+=1
        if b!=base:q[ix[b]][ix[b]]+=1
        if a!=base and b!=base:q[ix[a]][ix[b]]-=1;q[ix[b]][ix[a]]-=1
    tau=det(q) if q else F(1)
    assert tau>0 and tau.denominator==1
    inv=inverse(q) if q else []
    J=[[F(cls[v]==u) for u in others] for v in vs if v!=root]
    M=[[sum((J[i][a]*inv[a][b]*J[j][b]
             for a in range(len(others)) for b in range(len(others))),F(0))
        for j in range(len(J))] for i in range(len(J))]
    return int(tau),M

a={}
for g in P:
    vs=sorted(V(g));tau,_=quotient(g,[],vs,vs[0])
    coeff=invroot(tau)
    for h in P:
        if h<g:
            t,_=quotient(g,[h],vs,vs[0])
            coeff=add(coeff,scale(mul(a[h],invroot(t)),-1))
    a[g]=coeff
expected11=add(add(add(invroot(11),scale(S(F(1,3)),-1)),
                   scale(invroot(8),-1)),scale(invroot(5),-1))
expected14=add(add(add(invroot(14),scale(invroot(6),-1)),
                   scale(invroot(10),-1)),scale(invroot(12),-1))
assert [len(g)-len(V(g))+1 for g in P]==[1,1,1,1,1,2,2,1,2,2]
for i in (5,6):assert a[P[i]]==expected11
for i in (8,9):assert a[P[i]]==expected14

# The two-loop child quotient tau values are (3,2,1) and (4,2,1).
for i,counts in ((5,[1,2,3]),(6,[1,2,3]),(8,[1,2,4]),(9,[1,2,4])):
    g=P[i];got=sorted(quotient(g,[h],sorted(V(g)),min(V(g)))[0] for h in P if h<g)
    assert got==counts,(i,got)

G=frozenset(range(8));root=3
tau,mg=quotient(G,[],list(range(6)),root);assert tau==30
scalar=invroot(tau);matrix=[[scale(invroot(tau),mg[i][j]/2) for j in range(5)] for i in range(5)]
quot=[]
for g in P:
    t,m=quotient(G,[g],list(range(6)),root);quot.append(t)
    z=mul(a[g],invroot(t));scalar=add(scalar,scale(z,-1))
    for i in range(5):
        for j in range(5):matrix[i][j]=add(matrix[i][j],scale(z,-m[i][j]/2))
assert quot==[8,8,4,2,2,2,2,1,1,1]
t,m=quotient(G,list(disjoint[0]),list(range(6)),root);assert t==2
z=mul(mul(a[disjoint[0][0]],a[disjoint[0][1]]),invroot(t))
scalar=add(scalar,z)
for i in range(5):
    for j in range(5):matrix[i][j]=add(matrix[i][j],scale(z,m[i][j]/2))

expected_scalar=add(add(add(add(add(add(scale(rootrad(2),F(1,2)),S(F(1,4))),
                 scale(rootrad(3),F(1,3))),scale(rootrad(10),F(1,5))),
                 scale(rootrad(30),F(1,30))),scale(rootrad(14),-F(1,7))),
                 scale(rootrad(22),-F(1,11)))
expected_m00=add(add(scale(rootrad(6),-F(5,96)),
                      scale(rootrad(2),F(1,24))),
                      scale(rootrad(30),F(7,600)))
assert scalar==expected_scalar,(scalar,expected_scalar)
assert matrix[0][0]==expected_m00,(matrix[0][0],expected_m00)
assert matrix[0][0]!=S()
assert all(matrix[i][j]==matrix[j][i] for i in range(5) for j in range(5))
print("PASS: 10 1PI sources, 24 forests, including 12 nested and 1 disjoint")
print("PASS: two-loop intrinsic quotient tree counts and recursive scalar coefficients")
print("PASS: all 10 source quotient determinants and full tau=30")
print("PASS: exact seven-radical full-graph scalar and 5x5 derivative-pole matrix")
print("NOTE: corrected R2/057 manuscript uses the verified quotient-tree counts.")
