"""WP14: exact conditioned space-time small gain for local labelled networks.

No global state-space or joint transfer matrix is constructed by the verifier.
The optional exact-blanket method strengthens reusable per-factor bounds.
"""
from fractions import Fraction as F
from itertools import product, combinations
from math import prod, isqrt
from collections import defaultdict
from observable_polytope_certificate import solve_square


class LocalNetwork:
    """T_i[label][parent configuration][next local state], lexicographic rows."""
    def __init__(self,sizes,parents,tables):
        self.sizes=tuple(sizes);self.n=len(sizes)
        if not self.n or any(type(s)!=int or s<1 for s in sizes):
            raise ValueError("invalid state sizes")
        self.parents=tuple(tuple(p) for p in parents)
        if len(parents)!=self.n or len(tables)!=self.n:
            raise ValueError("factor count")
        self.tables=[];self.lookup=[];self.labels=[]
        self.children=[[] for _ in sizes]
        for i,p in enumerate(self.parents):
            if len(set(p))!=len(p) or any(type(j)!=int or not 0<=j<self.n for j in p):
                raise ValueError("invalid parents")
            for j in p:self.children[j].append(i)
            configs=tuple(product(*(range(sizes[j]) for j in p)))
            self.lookup.append({x:j for j,x in enumerate(configs)})
            T=tuple(tuple(tuple(F(v) for v in row) for row in M) for M in tables[i])
            if not T or any(len(M)!=len(configs) for M in T) or any(
                len(row)!=sizes[i] or any(v<=0 for v in row) for M in T for row in M):
                raise ValueError("strictly positive local table required")
            if any(sum(sum(M[r]) for M in T)!=1 for r in range(len(configs))):
                raise ValueError("local joint transition not normalized")
            self.labels.append(len(T))
            Q=tuple(tuple(sum(M[r][y] for M in T) for y in range(sizes[i]))
                    for r in range(len(configs)))
            self.tables.append(T+(Q,))
        self.tables=tuple(self.tables);self.labels=tuple(self.labels)

    def factor(self,i,label,parents,y):
        return self.tables[i][label][self.lookup[i][tuple(parents)]][y]

    def likelihood(self,i,label,parents):
        return sum(self.tables[i][label][self.lookup[i][tuple(parents)]])


def ratio_tv(R):
    """Rational upper bound on (sqrt(R)-1)/(sqrt(R)+1)."""
    R=F(R)
    if R<1:raise ValueError("bad cross ratio")
    scale=4096
    top=(R.numerator*scale*scale+R.denominator-1)//R.denominator
    s=isqrt(top)
    if s*s<top:s+=1
    return min((R-1)/(R+3),F(s-scale,s+scale))


def factor_envelope(net,i,observed=True):
    """Reusable local pair cross-ratios, including the wildcard label."""
    sizes=tuple(net.sizes[j] for j in net.parents[i])+(net.sizes[i],)
    table=net.tables[i]
    labels=range(len(table)) if observed else (net.labels[i],)
    result={}
    for u,v in combinations(range(len(sizes)),2):
        other=tuple(k for k in range(len(sizes)) if k not in (u,v))
        bound=F(1)
        for a in labels:
            for rest in product(*(range(sizes[j]) for j in other)):
                x=[0]*len(sizes)
                for j,z in zip(other,rest):x[j]=z
                A=[]
                for p in range(sizes[u]):
                    x[u]=p;row=[]
                    for q in range(sizes[v]):
                        x[v]=q;row.append(net.factor(i,a,x[:-1],x[-1]))
                    A.append(tuple(row))
                for p,q in combinations(range(sizes[u]),2):
                    ratios=tuple(A[p][r]/A[q][r] for r in range(sizes[v]))
                    bound=max(bound,max(ratios)/min(ratios))
        result[u,v]=bound
    return result


def incident(net,i,terminal):
    """Each factor scope relative to target (time 0, site i)."""
    factors=[(i,tuple((-1,j) for j in net.parents[i])+((0,i),))]
    if not terminal:
        factors.extend((j,tuple((0,k) for k in net.parents[j])+((1,j),))
                       for j in net.children[i])
    return tuple(factors)


def envelope_rows(net,cache=None,observed=True):
    """Compose factor-local bounds; cache keyed by exact table and arities.

    Caller may keep cache across network edits; entries are generated here,
    not accepted as externally supplied certificate values.
    """
    if cache is None:cache={}
    env=[];new=0
    for i in range(net.n):
        key=(tuple(net.sizes[j] for j in net.parents[i])+(net.sizes[i],),
             net.tables[i],observed)
        if key not in cache:
            cache[key]=factor_envelope(net,i,observed);new+=1
        env.append(cache[key])
    rows=[]
    for terminal in (False,True):
        out=[]
        for i in range(net.n):
            R=defaultdict(lambda:F(1))
            for f,scope in incident(net,i,terminal):
                u=scope.index((0,i))
                for v,node in enumerate(scope):
                    if v!=u:R[node]*=env[f][tuple(sorted((u,v)))]
            out.append({node:ratio_tv(r) for node,r in R.items() if r>1})
        rows.append(tuple(out))
    return rows[0],rows[1],new


def conditional_distribution(net,i,factors,labels,assignment):
    mass=[]
    for x in range(net.sizes[i]):
        a=dict(assignment);a[0,i]=x
        weight=F(1)
        for (f,scope),z in zip(factors,labels):
            v=tuple(a[node] for node in scope)
            weight*=net.factor(f,z,v[:-1],v[-1])
        mass.append(weight)
    total=sum(mass)
    return tuple(v/total for v in mass)


def exact_rows(net,observed=True,max_contexts=1000000):
    """Exact blanket Dobrushin coefficients, not whole-network enumeration."""
    result=[];contexts=0
    for terminal in (False,True):
        rows=[]
        for i in range(net.n):
            factors=incident(net,i,terminal)
            nodes=tuple(sorted({node for _,scope in factors for node in scope}-{(0,i)}))
            shape=tuple(net.sizes[j] for _,j in nodes)
            label_sets=tuple(range(net.labels[f]+1) if observed else (net.labels[f],)
                             for f,_ in factors)
            count=prod(shape)*prod(map(len,label_sets))
            if contexts+count>max_contexts:raise ValueError("local context budget")
            contexts+=count
            row={node:F(0) for node in nodes}
            for labels in product(*label_sets):
                D={v:conditional_distribution(net,i,factors,labels,dict(zip(nodes,v)))
                   for v in product(*(range(s) for s in shape))}
                for v,p in D.items():
                    for j,node in enumerate(nodes):
                        for x in range(v[j]+1,shape[j]):
                            q=D[v[:j]+(x,)+v[j+1:]]
                            row[node]=max(row[node],sum(abs(a-b) for a,b in zip(p,q))/2)
            rows.append({j:x for j,x in row.items() if x})
        result.append(tuple(rows))
    return result[0],result[1],contexts


def row_action(row,w,r):
    return sum(c*w[j]*r**dt for (dt,j),c in row.items())


def verify_gain(interior,terminal,w,r):
    """Exact anisotropic supersolution check on the two local row types."""
    r=F(r);w=tuple(map(F,w));n=len(interior)
    if not 0<r<1 or len(w)!=n or min(w)<=0 or len(terminal)!=n:
        raise ValueError("invalid gain witness")
    ratios=tuple(max(row_action(A,w,r),row_action(B,w,r))/w[i]
                 for i,(A,B) in enumerate(zip(interior,terminal)))
    q=max(ratios)
    if q>=1:raise ValueError("conditioned small gain failed")
    internal=tuple(max(sum(c*r**dt for (dt,j),c in row.items() if j==i)
                       for row in (interior[i],terminal[i])) for i in range(n))
    return {"rho":r,"weights":w,"gain":q,"slack":1-q,"row_gains":ratios,
            "internal_gains":internal}


def discover_gain(interior,terminal,rates=None,max_dense=64):
    """Try rational temporal rates and weights; no negative decision."""
    n=len(interior)
    if rates is None:rates=tuple(F(j,32) for j in range(1,32))+(F(63,64),F(127,128))
    for r in rates:
        r=F(r)
        if not 0<r<1:raise ValueError("invalid candidate rate")
        w=(F(1),)*n
        try:return verify_gain(interior,terminal,w,r)
        except ValueError:pass
        if n>max_dense:continue
        # Conservative common envelope of the two row types. Rational solve
        # produces candidate weights only; the two original rows are replayed.
        E=[]
        for A,B in zip(interior,terminal):
            a=[F(0)]*n;b=[F(0)]*n
            for (dt,j),c in A.items():a[j]+=c*r**dt
            for (dt,j),c in B.items():b[j]+=c*r**dt
            E.append(tuple(max(x,y) for x,y in zip(a,b)))
        try:
            w=solve_square(tuple(tuple(F(i==j)-E[i][j] for j in range(n))
                                 for i in range(n)),(F(1),)*n)
            if min(w)<=0:continue
            w=tuple(v/min(w) for v in w)
            return verify_gain(interior,terminal,w,r)
        except ValueError:continue
    return None


def observable_margins(net,gain):
    """Bounds for port probabilities even with other current ports clamped."""
    w=gain["weights"];r=gain["rho"];lo=[];C=[];osc=[]
    for i,p in enumerate(net.parents):
        c=min(sum(row) for M in net.tables[i][:-1] for row in M)
        lo.append(c);row={}
        for k,j in enumerate(p):
            diff=F(0)
            for x in net.lookup[i]:
                for y in range(net.sizes[j]):
                    z=x[:k]+(y,)+x[k+1:]
                    for a in range(net.labels[i]):
                        diff=max(diff,abs(net.likelihood(i,a,x)-net.likelihood(i,a,z)))
            if diff:row[j]=diff
        osc.append(row)
        C.append(sum(v*w[j]/min(w) for j,v in row.items())/c)
    # All-word quasi-Bernoulli margin by portwise relative likelihood bounds.
    # Head factors <=1; tail product >=1-sum of its relative errors.
    total=sum(C);tail=total/(1-r);head=F(1);error=tuple(C);n=0
    while tail>F(1,2):
        head*=prod(max(c,1-e) for c,e in zip(lo,error))
        error=tuple(e*r for e in error);tail*=r;n+=1
    return {"port_nonnull":tuple(lo),"port_constants":tuple(C),
            "port_oscillations":tuple(osc),"nonnull":prod(lo),"constant":total,
            "b":head*(1-tail),"tail_length":n}


def certify(net,method="factor",rates=None,max_contexts=1000000,max_dense=64,cache=None):
    if method=="factor":A,B,work=envelope_rows(net,cache)
    elif method=="exact":A,B,work=exact_rows(net,max_contexts=max_contexts)
    else:raise ValueError("unknown method")
    gain=discover_gain(A,B,rates,max_dense)
    if gain is None:return {"outcome":"undecided","boundary":"gain search",
                             "method":method,"work":work}
    return dict(gain,**observable_margins(net,gain),outcome="certified",
                method=method,work=work,interior=A,terminal=B,
                sites=net.n,joint_state_constructed=False)


def replay(net,witness):
    # Recompute local coefficients from actual tables (never trust a cache).
    if witness["method"]=="factor":A,B,_=envelope_rows(net)
    elif witness["method"]=="exact":A,B,_=exact_rows(net)
    else:raise ValueError("unknown witness method")
    G=verify_gain(A,B,witness["weights"],witness["rho"])
    return dict(G,**observable_margins(net,G))


def ring(n,self_gain=F(1,8),neighbor_gain=F(1,32),accuracy=F(5,8)):
    """Genuinely interacting binary parallel dynamics with noisy emissions."""
    if n<2:raise ValueError("ring requires at least two sites")
    parents=tuple((i,(i-1)%n) for i in range(n))
    T=tuple(tuple(tuple(
        (p if y else 1-p)*(accuracy if z==y else 1-accuracy)
        for y in (0,1)) for p in
        (F(1,2)+self_gain*(2*x-1)+neighbor_gain*(2*v-1)
         for x,v in product((0,1),repeat=2))) for z in (0,1))
    return LocalNetwork((2,)*n,parents,(T,)*n)


def conditioning_amplification():
    """Unlabelled dynamics iid; observed transition labels strong XOR constraints."""
    T=tuple(tuple(tuple(F(49,100) if y==(x^v^z) else F(1,100) for y in (0,1))
                  for x,v in product((0,1),repeat=2)) for z in (0,1))
    return LocalNetwork((2,2),((0,1),(1,0)),(T,T))
