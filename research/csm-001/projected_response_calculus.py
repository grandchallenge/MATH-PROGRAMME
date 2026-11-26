"""Finite-sector response oracle and coarse physical-graph minorization."""
from fractions import Fraction as F
from itertools import combinations
from math import comb

def states(n,k,budget=512):
    if n<2 or not 0<=k<=n or comb(n,k)>budget:
        raise ValueError("invalid or over-budget sector")
    return [tuple(int(i in x) for i in range(n)) for x in combinations(range(n),k)]

def kernel(xs,bonds,w,edges):
    n=len(w); bonds=list(bonds); edges=list(edges); w=list(map(F,w))
    if not bonds or len(set(bonds))!=len(bonds) or any(not 0<=i<j<n for i,j in bonds):
        raise ValueError("invalid physical graph")
    if min(w)<=0 or any(not 0<=i<j<n or F(a)<=0 for i,j,a in edges):
        raise ValueError("invalid weights")
    ids={x:i for i,x in enumerate(xs)}
    def weight(x):
        z=F(1)
        for i,b in enumerate(x):
            if b:z*=w[i]
        for i,j,a in edges:
            if x[i] and x[j]:z*=F(a)
        return z
    mass=[weight(x) for x in xs]
    Q=[[F(0) for _ in xs] for _ in xs]
    for k,x in enumerate(xs):
        for i,j in bonds:
            if x[i]==x[j]:Q[k][k]+=F(1,len(bonds));continue
            y=list(x);y[i],y[j]=y[j],y[i]; l=ids[tuple(y)]
            p=mass[l]/(mass[k]+mass[l])/len(bonds)
            Q[k][l]+=p;Q[k][k]+=F(1,len(bonds))-p
    return Q,[z/sum(mass) for z in mass]

def coarse_delta(n,E,eta,ratios):
    m=n*(n-1)//2; eta=F(eta); ratios=list(map(F,ratios))
    if n<2 or E<1 or not 0<eta<=1 or len(ratios)!=m-1 or any(r<1 for r in ratios):
        raise ValueError("invalid block inputs")
    d=(eta/E)**m
    for r in ratios:d/=r
    return d

def mm(A,B):
    return [[sum(a*b for a,b in zip(row,col)) for col in zip(*B)] for row in A]

def transfer(Qs,ls,s,t):
    if not 0<=s<t<len(ls):raise ValueError("invalid interval")
    B=[[Q*ls[s+1][j] for j,Q in enumerate(row)] for row in Qs[s]]
    for v in range(s+1,t):
        B=mm(B,[[q*ls[v+1][j] for j,q in enumerate(row)] for row in Qs[v]])
    return B

def column_delta(B):
    cols=[col for col in zip(*B) if max(col)>0]
    if not cols:raise ValueError("empty transfer")
    return min(min(col)/max(col) for col in cols)

class Posterior:
    def __init__(self,xs,initial,Qs,ls):
        self.xs=xs; self.n=len(xs[0]); self.Qs=Qs
        self.ls=[list(map(F,l)) for l in ls]; self.H=len(Qs)
        if len(ls)!=self.H+1 or any(len(l)!=len(xs) or min(l)<=0 for l in self.ls):
            raise ValueError("positive slice likelihoods required")
        a=[F(v)*l for v,l in zip(initial,self.ls[0])]
        self.a=[a]
        for Q,l in zip(Qs,self.ls[1:]):
            a=[sum(x*y for x,y in zip(a,col))*g for col,g in zip(zip(*Q),l)]
            self.a.append(a)
        self.z=sum(a)
        if self.z<=0:raise ValueError("empty posterior")
        self.b=[[F(1)]*len(xs)]
        for Q,l in zip(reversed(Qs),reversed(self.ls[1:])):
            self.b.append([sum(q*g*b for q,g,b in zip(row,l,self.b[-1])) for row in Q])
        self.b.reverse()
        self.marg=[[a*b/self.z for a,b in zip(A,B)] for A,B in zip(self.a,self.b)]
    def means(self,t):
        return [sum(p*x[i] for p,x in zip(self.marg[t],self.xs)) for i in range(self.n)]
    def response(self,t,s):
        if t<s:return [list(row) for row in zip(*self.response(s,t))]
        n=self.n; xs=self.xs; pt,ps=self.means(t),self.means(s)
        if t==s:
            return [[sum(p*x[i]*x[j] for p,x in zip(self.marg[t],xs))-pt[i]*ps[j] for j in range(n)] for i in range(n)]
        B=transfer(self.Qs,self.ls,s,t)
        J=[[a*v*b/self.z for v,b in zip(row,self.b[t])] for a,row in zip(self.a[s],B)]
        return [[sum(J[k][l]*y[i]*x[j] for k,x in enumerate(xs) for l,y in enumerate(xs))-pt[i]*ps[j] for j in range(n)] for i in range(n)]

def solve(A,b):
    """Exact consistent linear system, free variables set to zero."""
    m=len(b); M=[list(map(F,row))+[F(v)] for row,v in zip(A,b)]
    piv=[]; r=0
    for c in range(m):
        k=next((k for k in range(r,m) if M[k][c]),None)
        if k is None:continue
        M[r],M[k]=M[k],M[r]; z=M[r][c]; M[r]=[v/z for v in M[r]]
        for k in range(m):
            if k!=r:
                z=M[k][c];M[k]=[v-z*u for v,u in zip(M[k],M[r])]
        piv.append(c);r+=1
    if any(row[-1] for row in M[r:]):raise ValueError("inconsistent projection")
    x=[F(0)]*m
    for k,c in enumerate(piv):x[c]=M[k][-1]
    return x

def closure_defect(p,t,u,s,i,j):
    C=p.response(u,u); a=p.response(t,u)[i]; b=p.response(s,u)[j]
    coef=solve(C,b)
    return p.response(t,s)[i][j]-sum(x*y for x,y in zip(a,coef))
