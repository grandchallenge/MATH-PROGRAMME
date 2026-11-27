"""Rational certificates for scheduled local equilibration and localized slow rates."""
from fractions import Fraction as F
from math import comb
from itertools import combinations, product

def influence(blocks,edges):
    owner={i:a for a,B in enumerate(blocks) for i in B}
    if len(owner)!=sum(map(len,blocks)):raise ValueError("overlapping blocks")
    if not blocks or any(not B for B in blocks):raise ValueError("empty partition")
    factors={}; seen=set()
    for i,j,v in edges:
        v=F(v)
        key=tuple(sorted((i,j)))
        if v<=0 or i==j or key in seen or i not in owner or j not in owner:raise ValueError("invalid factor")
        seen.add(key)
        a,c=owner[i],owner[j]
        if a!=c:
            key=tuple(sorted((a,c)))
            factors[key]=factors.get(key,F(1))*max(v,1/v)
    C=[{} for _ in blocks]
    for (a,c),v in factors.items():
        if v>1:C[a][c]=C[c][a]=min(F(1),v-1)
    q=max(sum(row.values(),F(0)) for row in C)
    if q>=1:raise ValueError("noncontractive certificate: undecided")
    return C,q

def fast_gap(sizes,bond_counts,etas,q):
    # Connectivity and uniform placement lower bounds are caller hypotheses.
    q=F(q)
    if not sizes or len(sizes)!=len(bond_counts) or len(sizes)!=len(etas) or not 0<=q<1:
        raise ValueError("invalid gap inputs")
    gs=[]
    for n,E,eta in zip(sizes,bond_counts,etas):
        eta=F(eta)
        if n<1 or not 0<eta<=F(1,2) or (n>1 and E<n-1):raise ValueError("invalid block")
        m=n*(n-1)//2
        gs.append((eta/E)**m/m if m else F(1))
    return (1-q)*min(gs)/len(sizes)

def factor_range(weights,edges,sites=None):
    v=F(1)
    for i,w in enumerate(weights):
        w=F(w)
        if w<=0:raise ValueError("invalid site weight")
        if sites is None or i in sites:v*=max(w,1/w)
    for i,j,a in edges:
        a=F(a)
        if a<=0:raise ValueError("invalid pair factor")
        if sites is None or i in sites or j in sites:v*=max(a,1/a)
    return v

def pi_floor(blocks,counts,w,edges):
    if len(blocks)!=len(counts) or any(not 0<=k<=len(B) for B,k in zip(blocks,counts)):raise ValueError("invalid counts")
    N=1
    for B,k in zip(blocks,counts):N*=comb(len(B),k)
    return 1/(N*factor_range(w,edges))

def relative_error(g,pi_min,t):
    g,pi_min=F(g),F(pi_min)
    if not 0<g<=1 or not 0<pi_min<=1 or t<0:raise ValueError("invalid schedule")
    return (1-g)**t/pi_min

def window_radius(q,d,pmin,H,epsilon,budget=100000):
    q,pmin,epsilon=map(F,(q,pmin,epsilon))
    if not 0<=q<1 or d<1 or not 0<pmin<=1 or H<1 or not 0<epsilon<1:raise ValueError("invalid tolerance")
    target=epsilon/(2*H); a=d*q/pmin
    for r in range(budget):
        if a<=target:return r,a
        a*=q
    raise ValueError("radius budget: undecided")

def fiber(blocks,k,budget=4096):
    if len(blocks)!=len(k) or sorted(i for B in blocks for i in B)!=list(range(sum(map(len,blocks)))):raise ValueError("invalid partition")
    n=sum(map(len,blocks)); size=1
    for B,h in zip(blocks,k):
        if not 0<=h<=len(B):raise ValueError("invalid count")
        size*=comb(len(B),h)
    if size>budget:raise ValueError("fiber budget")
    return [tuple(int(i in chosen) for i in range(n)) for sel in product(*(combinations(B,h) for B,h in zip(blocks,k))) for chosen in [set().union(*map(set,sel))]]

def weight(x,w,edges):
    v=F(1)
    for i,a in enumerate(w):
        if x[i]:v*=F(a)
    for i,j,a in edges:
        if x[i] and x[j]:v*=F(a)
    return v

def swap(x,i,j):
    y=list(x);y[i],y[j]=y[j],y[i];return tuple(y)

def placement(x,i,j,w,edges):
    if x[i]==x[j]:return F(0)
    a=weight(x,w,edges);b=weight(swap(x,i,j),w,edges)
    return b/(a+b)

def outcome(x,i,j,w,edges):
    p=placement(x,i,j,w,edges)
    return (p if x[i]>x[j] else F(0),p if x[j]>x[i] else F(0),1-p)

def averaged_outcomes(xs,i,j,w,edges):
    mass=[weight(x,w,edges) for x in xs]; z=sum(mass)
    return tuple(sum(a*b for a,b in zip(mass,col))/z for col in zip(*(outcome(x,i,j,w,edges) for x in xs)))

def local_outcomes(blocks,k,U,exterior,i,j,w,edges,budget=4096):
    """Exact window conditional with arbitrary frozen exterior."""
    n=sum(map(len,blocks)); U=set(U); nstates=1
    for a in U:nstates*=comb(len(blocks[a]),k[a])
    if nstates>budget:raise ValueError("window budget")
    if len(exterior)!=n or any(v not in (0,1) for v in exterior):raise ValueError("invalid exterior")
    xs=[]
    for sel in product(*(combinations(blocks[a],k[a]) for a in sorted(U))):
        x=list(exterior)
        for a,occupied in zip(sorted(U),sel):
            for site in blocks[a]:x[site]=int(site in occupied)
        xs.append(tuple(x))
    return averaged_outcomes(xs,i,j,w,edges)
