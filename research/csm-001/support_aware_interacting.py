"""WP15: exact contextual quotients and rectangular-support small gain.

Only local transition tables, their scopes and sparse comparison rows are
used for acceptance. No hidden tensor or joint observation alphabet.
"""
from collections import defaultdict
from fractions import Fraction as F
from itertools import product, combinations
from math import prod
from interacting_small_gain import (
    ratio_tv, incident, discover_gain, verify_gain, observable_margins,
    row_action, column_gain, search_columns,
)


class SupportedNetwork:
    """Nonnegative labelled update tables in WP14's local port convention."""
    def __init__(self,sizes,parents,tables):
        self.sizes=tuple(sizes);self.n=len(self.sizes)
        self.parents=tuple(tuple(p) for p in parents)
        if not self.n or len(self.parents)!=self.n or len(tables)!=self.n:
            raise ValueError("factor count")
        if any(type(s)!=int or s<1 for s in self.sizes):
            raise ValueError("state sizes")
        self.lookup=[];self.children=[[] for _ in self.sizes]
        self.tables=[];self.labels=[]
        for i,p in enumerate(self.parents):
            if len(set(p))!=len(p) or any(type(j)!=int or not 0<=j<self.n for j in p):
                raise ValueError("invalid parents")
            for j in p:self.children[j].append(i)
            configs=tuple(product(*(range(self.sizes[j]) for j in p)))
            self.lookup.append({x:r for r,x in enumerate(configs)})
            T=tuple(tuple(tuple(F(v) for v in row) for row in A) for A in tables[i])
            if not T or any(len(A)!=len(configs) for A in T) or any(
                    len(row)!=self.sizes[i] or any(v<0 for v in row) for A in T for row in A):
                raise ValueError("invalid local table")
            if any(sum(sum(A[r]) for A in T)!=1 for r in range(len(configs))):
                raise ValueError("local transition not normalized")
            Q=tuple(tuple(sum(A[r][y] for A in T) for y in range(self.sizes[i]))
                    for r in range(len(configs)))
            self.labels.append(len(T));self.tables.append(T+(Q,))
        self.tables=tuple(self.tables);self.labels=tuple(self.labels)

    def factor(self,i,label,parents,y):
        return self.tables[i][label][self.lookup[i][tuple(parents)]][y]

    def likelihood(self,i,label,parents):
        return sum(self.tables[i][label][self.lookup[i][tuple(parents)]])


def canonical(values):
    ids={};out=[]
    for v in values:
        if v not in ids:ids[v]=len(ids)
        out.append(ids[v])
    return tuple(out)


def partition_check(net,P):
    P=tuple(tuple(row) for row in P)
    if len(P)!=net.n or any(len(row)!=s for row,s in zip(P,net.sizes)):
        raise ValueError("partition shape")
    if any(type(x)!=int or x<0 for row in P for x in row):
        raise ValueError("partition labels")
    if any(canonical(row)!=row for row in P):raise ValueError("noncanonical partition")
    return P


def aggregated_rows(net,P,i):
    d=max(P[i])+1;rows={}
    for x,r in net.lookup[i].items():
        row=[]
        for A in net.tables[i][:-1]:
            sums=[F(0)]*d
            for y,v in enumerate(A[r]):sums[P[i][y]]+=v
            row.append(tuple(sums))
        rows[x]=tuple(row)
    return rows


def contextual_quotient(net,P):
    """Exact deterministic interface for every micro parent configuration."""
    P=partition_check(net,P);sizes=tuple(max(p)+1 for p in P);tables=[]
    for i,p in enumerate(net.parents):
        rows={}
        for x,v in aggregated_rows(net,P,i).items():
            key=tuple(P[j][a] for j,a in zip(p,x))
            if key in rows and rows[key]!=v:raise ValueError("contextual lumpability failed")
            rows[key]=v
        values=tuple(rows[x] for x in product(*(range(sizes[j]) for j in p)))
        tables.append(tuple(tuple(row[z] for row in values) for z in range(net.labels[i])))
    return SupportedNetwork(sizes,net.parents,tuple(tables))


def discover_partition(net,initial=None):
    """Coarsest stable componentwise refinement of supplied initial classes."""
    P=partition_check(net,initial if initial is not None else tuple((0,)*s for s in net.sizes))
    steps=0;scans=0
    while True:
        sig=[[[] for _ in range(s)] for s in net.sizes]
        for i,p in enumerate(net.parents):
            rows=aggregated_rows(net,P,i)
            scans+=len(rows)
            for k,j in enumerate(p):
                rest=tuple(h for h in range(len(p)) if h!=k)
                for ctx in product(*(range(net.sizes[p[h]]) for h in rest)):
                    for x in range(net.sizes[j]):
                        v=list(ctx);v.insert(k,x)
                        sig[j][x].append(rows[tuple(v)])
        Q=tuple(canonical((P[i][x],tuple(s)) for x,s in enumerate(row))
                for i,row in enumerate(sig))
        if Q==P:
            return P,contextual_quotient(net,P),{"rounds":steps,"local_rows_scanned":scans}
        P=Q;steps+=1


def verify_stochastic_interface(net,quotient,encodings):
    """Local stochastic intertwiner: exact for product encoders on each slice.

    Not a claim of minimality or stochastic-encoder synthesis.
    """
    if net.n!=quotient.n or net.parents!=quotient.parents or net.labels!=quotient.labels:
        raise ValueError("interface topology")
    E=tuple(tuple(tuple(F(v) for v in row) for row in A) for A in encodings)
    if len(E)!=net.n or any(len(A)!=s for A,s in zip(E,net.sizes)) or any(
        len(row)!=d or min(row)<0 or sum(row)!=1 for A,d in zip(E,quotient.sizes) for row in A):
        raise ValueError("encoding stochasticity")
    for i,p in enumerate(net.parents):
        configs=tuple(quotient.lookup[i])
        for x in net.lookup[i]:
            weights=tuple(prod(E[j][u][v] for j,u,v in zip(p,x,q)) for q in configs)
            for a in range(net.labels[i]):
                for y in range(quotient.sizes[i]):
                    lhs=sum(net.factor(i,a,x,v)*E[i][v][y] for v in range(net.sizes[i]))
                    rhs=sum(w*quotient.factor(i,a,q,y) for w,q in zip(weights,configs))
                    if lhs!=rhs:raise ValueError("stochastic intertwiner failed")
    return True


def rectangular_domains(net):
    """Supports may depend on the label, but not on any parent state."""
    domains=[]
    for i,T in enumerate(net.tables):
        ds=[]
        for A in T:
            S=tuple(j for j,v in enumerate(A[0]) if v>0)
            if not S or any(tuple(j for j,v in enumerate(row) if v>0)!=S for row in A):
                raise ValueError("nonrectangular label support")
            ds.append(S)
        # Remove globally unused states rather than silently treating them
        # as possible boundary values. This verifier requires full wildcard.
        if len(ds[-1])!=net.sizes[i]:raise ValueError("unused wildcard state")
        domains.append(tuple(ds))
    return tuple(domains)


def rectangular_envelope(net,i,domains):
    """WP14 cross ratios restricted to each labelled child domain."""
    p=net.parents[i];d=len(p)+1
    result={}
    for u,v in combinations(range(d),2):
        other=tuple(k for k in range(d) if k not in (u,v));R=F(1)
        for a,S in enumerate(domains[i]):
            choices=tuple(tuple(range(net.sizes[j])) for j in p)+(S,)
            for rest in product(*(choices[k] for k in other)):
                x=[0]*d
                for k,z in zip(other,rest):x[k]=z
                rows=[]
                for z in choices[u]:
                    x[u]=z;row=[]
                    for t in choices[v]:
                        x[v]=t;row.append(net.factor(i,a,x[:-1],x[-1]))
                    rows.append(tuple(row))
                for p1,p2 in combinations(rows,2):
                    ratio=tuple(a/b for a,b in zip(p1,p2))
                    R=max(R,max(ratio)/min(ratio))
        result[u,v]=R
    return result


def packets(net):
    domains=rectangular_domains(net);cache={};out=[]
    for i,p in enumerate(net.parents):
        key=(tuple(net.sizes[j] for j in p),net.sizes[i],net.tables[i])
        if key not in cache:cache[key]=rectangular_envelope(net,i,domains)
        out.append(cache[key])
    return tuple(out),domains,len(cache)


def site_rows(net,env):
    rows=[]
    for terminal in (False,True):
        out=[]
        for i in range(net.n):
            R=defaultdict(lambda:F(1))
            for f,scope in incident(net,i,terminal):
                u=scope.index((0,i))
                for v,node in enumerate(scope):
                    if u!=v:R[node]*=env[f][tuple(sorted((u,v)))]
            out.append({j:ratio_tv(r) for j,r in R.items() if r>1})
        rows.append(tuple(out))
    return tuple(rows)


def column_events(net,env):
    kappa=tuple(ratio_tv(env[i][p.index(i),len(p)]) if i in p else F(0)
                for i,p in enumerate(net.parents))
    events=[[] for _ in net.sizes]
    for f,p in enumerate(net.parents):
        scope=tuple((-1,j) for j in p)+((0,f),)
        for i in set(j for _,j in scope):
            own=tuple(u for u,(_,j) in enumerate(scope) if i==j)
            for v,(dt,j) in enumerate(scope):
                if j==i:continue
                R=prod(env[f][tuple(sorted((u,v)))] for u in own)
                if R==1:continue
                times=tuple(scope[u][0]-dt for u in own)
                events[i].append((j,min(times),max(times),ratio_tv(R)))
    return kappa,tuple(tuple(sorted(row)) for row in events)


def spatial_margin(net,rows,w):
    """Two-sided spatial/space-time comparison with all clamp patterns.

    Return local insertion nonnullness and a uniform weighted row bound.
    The graph distance is on hidden variables sharing any factor scope.
    """
    w=tuple(map(F,w))
    if len(w)!=net.n or min(w)<=0:raise ValueError("spatial metric")
    q=max(row_action(row,w,F(1))/w[i] for i,row in enumerate(rows))
    if q>=1:return {"spatial_outcome":"undecided","spatial_gain":q}
    lo=[]
    minima=tuple(min(v for A in T for row in A for v in row if v>0)
                 for T in net.tables)
    for i in range(net.n):
        c=min(sum(row) for A in net.tables[i][:-1] for row in A)
        lo.append(c*prod(minima[j] for j in net.children[i]))
    return {"spatial_outcome":"certified","spatial_gain":q,
            "weight_ratio":max(w)/min(w),"insertion_nonnull":tuple(lo)}


def certify(net,method="site",rates=None,max_dense=64):
    try:env,domains,work=packets(net)
    except ValueError as exc:
        return {"outcome":"undecided","boundary":str(exc)}
    A,B=site_rows(net,env)
    if method=="site":G=discover_gain(A,B,rates,max_dense)
    elif method=="column":
        k,E=column_events(net,env)
        G=search_columns(net.n,k,E,rates,max_dense)
    else:raise ValueError("unknown method")
    if G is None:return {"outcome":"undecided","boundary":"gain search"}
    return dict(G,**observable_margins(net,G),**spatial_margin(net,A,G["weights"]),
                outcome="certified",method=method,work=work,domains=domains,
                sizes=net.sizes,joint_state_constructed=False)


def replay(net,witness):
    env,domains,_=packets(net);A,B=site_rows(net,env)
    if witness["method"]=="site":G=verify_gain(A,B,witness["weights"],witness["rho"])
    elif witness["method"]=="column":
        k,E=column_events(net,env)
        G=column_gain(k,E,witness["rho"],witness["weights"])
    else:raise ValueError("unknown method")
    return dict(G,**observable_margins(net,G),**spatial_margin(net,A,G["weights"]))


def reduce_and_certify(net,method="site",rates=None,max_dense=64,initial=None):
    P,Q,stats=discover_partition(net,initial)
    result=certify(Q,method,rates,max_dense)
    return dict(result,partition=P,quotient_sizes=Q.sizes,refinement=stats)


def replay_reduced(net,witness):
    Q=contextual_quotient(net,witness["partition"])
    return replay(Q,witness)


def revealed_ring(n,self_gain=F(1,8),neighbor_gain=F(1,32),nuisance=1):
    """Exact revealed binary update, optional conserved invisible color.

    Both binary dynamics and interactions are genuine. The color never
    changes, is not emitted, and has no effect on any other local port.
    """
    if n<2 or nuisance<1:raise ValueError("ring dimensions")
    sizes=(2*nuisance,)*n;parents=tuple((i,(i-1)%n) for i in range(n))
    table=[]
    for z in (0,1):
        rows=[]
        for x,v in product(range(2*nuisance),repeat=2):
            p=F(1,2)+self_gain*(2*(x//nuisance)-1)+neighbor_gain*(2*(v//nuisance)-1)
            rows.append(tuple((p if z else 1-p) if y//nuisance==z and y%nuisance==x%nuisance
                              else F(0) for y in range(2*nuisance)))
        table.append(tuple(rows))
    return SupportedNetwork(sizes,parents,(tuple(table),)*n)


def partly_revealed_ring(n,nuisance=1,self_gain=F(1,8),neighbor_gain=F(1,32)):
    """Three labels: exact 0, exact 1, or uninformative erasure."""
    net=revealed_ring(n,self_gain,neighbor_gain,nuisance)
    tables=[]
    for A,B,Q in net.tables:
        tables.append(tuple(tuple(tuple(v/2 for v in row) for row in M) for M in (A,B,Q)))
    return SupportedNetwork(net.sizes,net.parents,tuple(tables))
