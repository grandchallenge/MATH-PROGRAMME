"""Rational sufficient comparison certificate for binary canonical Gibbs laws."""
from fractions import Fraction as F
from collections import deque

def certificate(n, edges, ratio):
    if n<3 or F(ratio)<1: raise ValueError("invalid size or ratio")
    adj=[{} for _ in range(n)]
    products=[F(1)]*n
    seen=set()
    for i,j,v in edges:
        if not 0<=i<j<n or (i,j) in seen or F(v)<=0:
            raise ValueError("invalid edge")
        seen.add((i,j)); v=F(v); r=max(v,1/v)
        if r==1: continue
        adj[i][j]=adj[j][i]=(r-1)/4
        products[i]*=r; products[j]*=r
    L=max(sum(row.values(),F(0)) for row in adj)
    eta=1/(1+F(ratio)*max(products)**2)
    A0=1+(n-2)*eta; A=A0-2*(n-3)*L
    if A<=0: raise ValueError("nonpositive sufficient gain: undecided")
    return adj,L,eta,A0,A

def bounds(w,u,edges):
    w,u=tuple(map(F,w)),tuple(map(F,u))
    n=len(w)
    if len(u)!=n or min(w+u)<=0: raise ValueError("invalid fields")
    adj,L,eta,A0,A=certificate(n,edges,max(w+u)/min(w+u))
    tau=[(max(a/b,b/a)-1)/4 for a,b in zip(w,u)]
    T=sum(tau,F(0)); q=(n-3)*L/A0
    D=(n-1)*T/A
    base=(T+(1+2*L)*D)/(A0*(1-q))
    amp=(n-2)*max(tau)/(A0*(1-q))
    dist=[None]*n
    queue=deque()
    for i,t in enumerate(tau):
        if t: dist[i]=0; queue.append(i)
    while queue:
        i=queue.popleft()
        for j in adj[i]:
            if dist[j] is None: dist[j]=dist[i]+1; queue.append(j)
    local=[min(F(1),base+(amp*q**r if r is not None else 0)) for r in dist]
    return {"D":D,"base":base,"amplitude":amp,"q":q,"local":local,"A":A,"eta":eta}

def walk_column(n,edges,j,t):
    if n<2 or not 0<=j<n or t<0: raise ValueError("invalid walk")
    edges=list(edges)
    if not edges or len(set(edges))!=len(edges) or any(not 0<=a<b<n for a,b in edges):
        raise ValueError("invalid bonds")
    v=[F(int(i==j)) for i in range(n)]
    for _ in range(t):
        u=v[:]
        for a,b in edges:
            delta=(v[b]-v[a])/(2*len(edges))
            u[a]+=delta; u[b]-=delta
        v=u
    return v

def temporal_response(n,edges,k,j,t,h):
    h=F(h)
    if not 0<=k<=n or h<=0: raise ValueError("invalid observation")
    rho=F(k,n)
    scale=rho*(1-rho)*F(n,n-1)*(h-1)/(1+(h-1)*rho)
    return [scale*(v-F(1,n)) for v in walk_column(n,edges,j,t)]
