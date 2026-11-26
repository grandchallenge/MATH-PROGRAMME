"""Exact finite observable-space and Markov-algebra reference certificates."""
from fractions import Fraction as F
from itertools import combinations
from math import comb

def sector(n,k,budget=256):
    if not 0<=k<=n or comb(n,k)>budget: raise ValueError("sector budget")
    return [tuple(int(i in s) for i in range(n)) for s in combinations(range(n),k)]

def exchange(xs,bonds):
    n=len(xs[0]); q=[[F(0) for _ in xs] for _ in xs]
    if not bonds or any(not 0<=i<j<n or F(w)<=0 for i,j,w in bonds):raise ValueError("invalid bond")
    z=sum(F(w) for _,_,w in bonds); ids={x:i for i,x in enumerate(xs)}
    for a,x in enumerate(xs):
        for i,j,w in bonds:
            y=list(x);y[i],y[j]=y[j],y[i]
            p=F(w)/(2*z);q[a][a]+=p;q[a][ids[tuple(y)]]+=p
    return q

def mv(M,v):return [sum(a*b for a,b in zip(row,v)) for row in M]
def transfer(P,L):return [[a*F(b) for a,b in zip(row,L)] for row in P]

class Span:
    def __init__(self,n): self.n=n; self.rows={}
    def add(self,v):
        v=list(map(F,v))
        if len(v)!=self.n:raise ValueError("dimension")
        for i,r in sorted(self.rows.items()):
            if v[i]:
                a=v[i];v=[x-a*y for x,y in zip(v,r)]
        i=next((j for j,x in enumerate(v) if x),None)
        if i is None:return False
        a=v[i];self.rows[i]=[x/a for x in v];return True

def predictive(n,targets,actions,h=None):
    S=Span(n);S.add([1]*n)
    for v in targets:S.add(v)
    dims=[len(S.rows)]
    while h is None or len(dims)<=h:
        old=list(S.rows.values())
        for v in old:
            for M in actions:S.add(mv(M,v))
        dims.append(len(S.rows))
        if dims[-1]==dims[-2]:break
    return S,dims

def group(keys):
    d={}
    for i,key in enumerate(keys):d.setdefault(tuple(key),[]).append(i)
    return list(d.values())

def aggregate(row,part):return [sum(row[i] for i in C) for C in part]

def refine(n,features,kernels):
    part=group(zip(*features)) if features else [list(range(n))]
    sizes=[len(part)]
    while True:
        new=[]
        for C in part:
            sig=[tuple(v for P in kernels for v in aggregate(P[x],part)) for x in C]
            new.extend([[C[i] for i in D] for D in group(sig)])
        sizes.append(len(new))
        if len(new)==len(part):return new,sizes
        part=new

def quotient_ratio(M,part):
    """Representative-row transfer with exact multiplicative envelope."""
    B=[aggregate(M[C[0]],part) for C in part]
    lo=hi=F(1)
    for C,row in zip(part,B):
        for x in C:
            for a,b in zip(aggregate(M[x],part),row):
                if not a and not b:continue
                if not a or not b:raise ValueError("support mismatch: undecided")
                r=a/b;lo=min(lo,r);hi=max(hi,r)
    return B,lo,hi

def tv_bound(ratios):
    G=F(1)
    for l,u in ratios:
        if not 0<l<=u:raise ValueError("invalid ratio")
        G*=u/l
    return (G-1)/(G+1)

def monomials(xs,r):
    from math import prod
    return [[prod(x[i] for i in s) for x in xs] for k in range(r+1) for s in combinations(range(len(xs[0])),k)]

def count_features(xs,blocks):
    return [[sum(x[i] for i in B) for x in xs] for B in blocks]

def partitions(items):
    if not items:
        yield []
        return
    a,*rest=items
    for part in partitions(rest):
        yield [[a]]+[C[:] for C in part]
        for i in range(len(part)):
            yield [([a]+C if j==i else C[:]) for j,C in enumerate(part)]

def refinements(part):
    if not part:
        yield []
        return
    for head in partitions(part[0]):
        for tail in refinements(part[1:]):
            yield head+tail

def minimum_certified(part, actions, tolerance, budget=10000):
    """Global optimum for this representative-rule certificate, or undecided on budget."""
    tolerance=F(tolerance)
    if not 0<=tolerance<=1 or budget<1:raise ValueError("invalid search input")
    best=None; seen=0
    for p in refinements(part):
        seen+=1
        if seen>budget:raise ValueError("partition search budget: undecided")
        if best is not None and len(p)>=len(best[0]):continue
        try: ratios=[quotient_ratio(M,p)[1:] for M in actions]
        except ValueError:continue
        error=tv_bound(ratios)
        if error<=tolerance:best=(p,error)
    if best is None:raise ValueError("no certified refinement")
    return best[0],best[1],seen
