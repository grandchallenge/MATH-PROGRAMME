"""WP14: exact conditioned space-time small gain for local labelled networks.

No global state-space or joint transfer matrix is constructed by the verifier.
The optional exact-blanket method strengthens reusable per-factor bounds.
"""
from fractions import Fraction as F
from itertools import product, combinations
from math import prod, isqrt, ceil
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


def factor_packets(net,observed=True):
    """Compute each distinct exact local factor envelope once."""
    cache={};env=[]
    for i in range(net.n):
        key=(tuple(net.sizes[j] for j in net.parents[i])+(net.sizes[i],),
             net.tables[i],observed)
        if key not in cache:cache[key]=factor_envelope(net,i,observed)
        env.append(cache[key])
    return tuple(env),len(cache)


def envelope_rows(net,observed=True):
    """Compose factor-local bounds; identical factors computed once per replay.
    No caller-supplied cache is trusted.
    """
    env,new=factor_packets(net,observed)
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
    self_rows=tuple(tuple(sum((c*r**dt for (dt,j),c in row.items() if j==i),F(0))
                          for row in (interior[i],terminal[i])) for i in range(n))
    cross_rows=tuple(tuple(row_action(row,w,r)/w[i]-d
                           for row,d in zip((interior[i],terminal[i]),self_rows[i]))
                     for i in range(n))
    # Internal damping must leave enough budget for cross-component feedback.
    normalized_cross=max(c/(1-d) for ss,cc in zip(self_rows,cross_rows)
                         for d,c in zip(ss,cc))
    return {"rho":r,"weights":w,"gain":q,"slack":1-q,"row_gains":ratios,
            "internal_gains":tuple(map(max,self_rows)),"self_rows":self_rows,
            "cross_rows":cross_rows,"cross_budget_fraction":normalized_cross}


def discover_gain(interior,terminal,rates=None,max_dense=64,sparse_steps=16):
    """Try rational temporal rates and weights; no negative decision."""
    n=len(interior)
    if rates is None:rates=tuple(F(j,32) for j in range(1,32))+(F(63,64),F(127,128))
    rates=tuple(map(F,rates))
    if any(not 0<r<1 for r in rates):raise ValueError("invalid candidate rate")
    # Try cheap uniform weights at every rate before any dense rational solve.
    w=(F(1),)*n
    for r in rates:
        try:return verify_gain(interior,terminal,w,r)
        except ValueError:pass
    # Monotone sparse positive-operator iteration: feasible strict weights
    # imply convergence of 1+max(M_int w,M_end w) to a finite fixed point.
    # The finite iteration budget is only a search limit.
    for r in rates:
        w=(F(1),)*n
        for _ in range(sparse_steps):
            w=tuple(1+max(row_action(A,w,r),row_action(B,w,r))
                    for A,B in zip(interior,terminal))
            try:return verify_gain(interior,terminal,w,r)
            except ValueError:pass
    if n>max_dense:return None
    for r in rates:
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


def observable_margins(net,gain,max_tail_steps=256,max_tail_bits=1000000):
    """Bounds for port probabilities even with other current ports clamped."""
    w=gain["weights"];r=gain["rho"];lo=[];C=[];osc=[];scale=min(w)
    prefactor=gain.get("boundary_prefactor",F(1))
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
        C.append(prefactor*sum(v*w[j]/scale for j,v in row.items())/c)
    # All-word quasi-Bernoulli margin by portwise relative likelihood bounds.
    # Head factors <=1; tail product >=1-sum of its relative errors.
    total=sum(C);tail=total/(1-r);head=F(1);error=tuple(C);n=0
    c=prod(lo);compact=None
    while tail>F(1,2):
        if n>=max_tail_steps or head.denominator.bit_length()>max_tail_bits:
            # Compact conservative margin: r**t <= 1/2, followed by j
            # halvings of the initial tail. Do not materialize c**(t*j).
            x=2*total/(1-r)
            j=max(0,x.numerator.bit_length()-x.denominator.bit_length())
            if 2**j<x:j+=1
            n=ceil(1/(1-r))*j
            compact={"coefficient":F(1,2),"base":c,"exponent":n}
            break
        head*=prod(max(c,1-e) for c,e in zip(lo,error))
        error=tuple(e*r for e in error);tail*=r;n+=1
    return {"port_nonnull":tuple(lo),"port_constants":tuple(C),
            "port_oscillations":tuple(osc),"nonnull":c,"constant":total,
            "b":head*(1-tail) if compact is None else None,
            "b_power":compact,"tail_length":n}


def column_events(net):
    """Internal chain rate and sparse factor-local exterior perturbations.

    A perturbation has (other component, first time offset, last time
    offset, central TV bound), offsets relative to the changed exterior site.
    """
    env,work=factor_packets(net)
    internal=tuple(ratio_tv(env[i][net.parents[i].index(i),len(net.parents[i])])
                   if i in net.parents[i] else F(0) for i in range(net.n))
    events=[[] for _ in range(net.n)]
    for f,p in enumerate(net.parents):
        scope=tuple((-1,j) for j in p)+((0,f),)
        for i in set(j for _,j in scope):
            own=tuple(u for u,(_,j) in enumerate(scope) if j==i)
            for v,(dt,j) in enumerate(scope):
                if j==i:continue
                R=prod(env[f][tuple(sorted((u,v)))] for u in own)
                if R==1:continue
                offsets=tuple(scope[u][0]-dt for u in own)
                events[i].append((j,min(offsets),max(offsets),ratio_tv(R)))
    return internal,tuple(tuple(sorted(row)) for row in events),work


def temporal_response(kappa,r,lo,hi):
    """Sum over exterior times, including the two geometric response tails."""
    kappa,r=F(kappa),F(r)
    if not 0<=kappa<r<1 or lo>hi:raise ValueError("invalid temporal response")
    return (sum(r**j for j in range(-hi,-lo+1))+
            r**(-hi)*kappa/(r-kappa)+r**(-lo)*kappa*r/(1-kappa*r))


def column_rows(internal,events,r):
    r=F(r)
    if any(k>=r for k in internal):raise ValueError("rate below internal chain")
    out=[]
    for k,ev in zip(internal,events):
        row=defaultdict(lambda:F(0))
        for j,lo,hi,a in ev:row[0,j]+=a*temporal_response(k,r,lo,hi)
        out.append(dict(row))
    return tuple(out)


def column_gain(internal,events,r,w):
    rows=column_rows(internal,events,r)
    data=verify_gain(rows,rows,w,r)
    return dict(data,internal_rates=internal,boundary_prefactor=1/(1-data["gain"]),
                interaction_rows=rows)


def certify_columns(net,rates=None,max_dense=64,sparse_steps=16):
    internal,events,work=column_events(net)
    if rates is None:rates=tuple(F(j,32) for j in range(1,32))+(F(63,64),F(127,128))
    rates=tuple(map(F,rates))
    if any(not 0<r<1 for r in rates):raise ValueError("invalid candidate rate")
    candidates=[]
    for r in rates:
        if max(internal)>=r:continue
        rows=column_rows(internal,events,r);candidates.append((r,rows))
        try:
            gain=column_gain(internal,events,r,(F(1),)*net.n)
            break
        except ValueError:continue
    else:
        gain=None
        for r,rows in candidates:
            data=discover_gain(rows,rows,(r,),max_dense,sparse_steps)
            if data is not None:
                gain=column_gain(internal,events,r,data["weights"]);break
    if gain is None:return {"outcome":"undecided","boundary":"column gain search",
                             "method":"column","work":work}
    return dict(gain,**observable_margins(net,gain),outcome="certified",
                method="column",work=work,events=events,sites=net.n,
                joint_state_constructed=False)


def certify(net,method="factor",rates=None,max_contexts=1000000,max_dense=64,sparse_steps=16):
    if method=="column":return certify_columns(net,rates,max_dense,sparse_steps)
    if method=="factor":A,B,work=envelope_rows(net)
    elif method=="exact":
        try:A,B,work=exact_rows(net,max_contexts=max_contexts)
        except ValueError as exc:
            if str(exc)!="local context budget":raise
            return {"outcome":"undecided","boundary":"local context budget","method":method}
    else:raise ValueError("unknown method")
    gain=discover_gain(A,B,rates,max_dense,sparse_steps)
    if gain is None:return {"outcome":"undecided","boundary":"gain search",
                             "method":method,"work":work}
    return dict(gain,**observable_margins(net,gain),outcome="certified",
                method=method,work=work,interior=A,terminal=B,
                sites=net.n,joint_state_constructed=False)


def replay(net,witness):
    # Recompute local coefficients from actual tables (never trust a cache).
    if witness["method"]=="column":
        internal,events,_=column_events(net)
        G=column_gain(internal,events,witness["rho"],witness["weights"])
        return dict(G,**observable_margins(net,G))
    if witness["method"]=="factor":A,B,_=envelope_rows(net)
    elif witness["method"]=="exact":A,B,_=exact_rows(net)
    else:raise ValueError("unknown witness method")
    G=verify_gain(A,B,witness["weights"],witness["rho"])
    return dict(G,**observable_margins(net,G))


def binary_network(coefficients,accuracy=F(5,8)):
    """Local Bernoulli transitions with additive signed parent influences."""
    accuracy=F(accuracy)
    parents=tuple(tuple(j for j,a in row) for row in coefficients)
    tables=[]
    for row in coefficients:
        probs=tuple(F(1,2)+sum(F(a)*(2*x-1) for (_,a),x in zip(row,v))
                    for v in product((0,1),repeat=len(row)))
        T=tuple(tuple(tuple(
            (p if y else 1-p)*(accuracy if z==y else 1-accuracy)
            for y in (0,1)) for p in probs) for z in (0,1))
        tables.append(T)
    return LocalNetwork((2,)*len(coefficients),parents,tuple(tables))


def ring(n,self_gain=F(1,8),neighbor_gain=F(1,32),accuracy=F(5,8)):
    """Genuinely interacting binary parallel dynamics with noisy emissions."""
    if n<2:raise ValueError("ring requires at least two sites")
    return binary_network(tuple(((i,self_gain),((i-1)%n,neighbor_gain))
                                for i in range(n)),accuracy)


def conditioning_amplification():
    """Unlabelled dynamics iid; observed transition labels strong XOR constraints."""
    T=tuple(tuple(tuple(F(49,100) if y==(x^v^z) else F(1,100) for y in (0,1))
                  for x,v in product((0,1),repeat=2)) for z in (0,1))
    return LocalNetwork((2,2),((0,1),(1,0)),(T,T))
