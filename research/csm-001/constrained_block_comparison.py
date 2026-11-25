"""WP16: safe-reset block comparison for nonrectangular labelled supports.

Finite spatial partition, replicated at every time. Exact local factor
checks and optional blanket enumeration; never enumerate global states.
"""
from collections import defaultdict
from fractions import Fraction as F
from itertools import product, combinations
from math import prod
from support_aware_interacting import SupportedNetwork, discover_partition
from interacting_small_gain import ratio_tv, discover_gain, verify_gain, row_action


class BlockNetwork:
    def __init__(self,net,blocks,safe=None,max_block_states=256):
        self.net=net;self.blocks=tuple(tuple(b) for b in blocks)
        if not self.blocks or any(not b for b in self.blocks) or sorted(j for b in self.blocks for j in b)!=list(range(net.n)):
            raise ValueError("blocks must partition sites")
        self.n=len(self.blocks)
        self.owner={j:i for i,b in enumerate(self.blocks) for j in b}
        self.safe=tuple((0,)*net.n if safe is None else safe)
        if len(self.safe)!=net.n or any(type(x)!=int or not 0<=x<s for x,s in zip(self.safe,net.sizes)):
            raise ValueError("bad safe state")
        if any(prod(net.sizes[j] for j in b)>max_block_states for b in self.blocks):
            raise ValueError("block state budget")
        self.states=tuple(tuple(product(*(range(net.sizes[j]) for j in b))) for b in self.blocks)
        self.safes=tuple(tuple(self.safe[j] for j in b) for b in self.blocks)
        self.pos={j:k for b in self.blocks for k,j in enumerate(b)}
        self.factors=[]
        self.inc=[[] for _ in self.blocks]
        # Group each factor's coordinates by relative time and spatial block.
        for i,p in enumerate(net.parents):
            scope=tuple((-1,j) for j in p)+((0,i),)
            groups={}
            for k,(t,j) in enumerate(scope):groups.setdefault((t,self.owner[j]),[]).append(k)
            nodes=tuple(sorted(groups));groups=tuple(tuple(groups[v]) for v in nodes)
            vals=tuple(tuple(product(*(range(net.sizes[scope[k][1]]) for k in g))) for g in groups)
            sf=tuple(tuple(self.safe[scope[k][1]] for k in g) for g in groups)
            tables=[]
            for z in range(net.labels[i]+1):
                D={}
                for v in product(*vals):
                    x=[0]*len(scope)
                    for g,row in zip(groups,v):
                        for k,a in zip(g,row):x[k]=a
                    D[v]=net.factor(i,z,x[:-1],x[-1])
                tables.append(D)
            self.factors.append((scope,nodes,groups,vals,sf,tuple(tables)))
            for u,(t,b) in enumerate(nodes):self.inc[b].append((i,u,t))
        self.verify_safe()

    def verify_safe(self):
        """Every factor can reset any intersecting block without losing positivity."""
        for _,nodes,groups,vals,sf,tables in self.factors:
            for D in tables:
                if D[sf]<=0:raise ValueError("all-safe label unsupported")
                for x,v in D.items():
                    if v<=0:continue
                    for u,s in enumerate(sf):
                        if D[x[:u]+(s,)+x[u+1:]]<=0:
                            raise ValueError("safe block reset failed")
        return True

    def incident(self,b,terminal=False):
        out=[]
        for f,u,t in self.inc[b]:
            scope,nodes,groups,vals,sf,T=self.factors[f]
            if terminal and t==-1:continue
            out.append((f,u,tuple((h-t,j) for h,j in nodes)))
        return tuple(out)

    def partial(self,f,u,node_state):
        scope,nodes,groups,vals,sf,T=self.factors[f]
        return tuple(node_state[self.pos[scope[k][1]]] for k in groups[u])

    def restriction(self,f,u,z,context):
        """Local factor section; zero section replaced at all-safe exterior."""
        _,_,_,vals,sf,T=self.factors[f];D=T[z]
        out=tuple(D[context[:u]+(a,)+context[u+1:]] for a in vals[u])
        if not any(out):
            out=tuple(D[sf[:u]+(a,)+sf[u+1:]] for a in vals[u])
        return dict(zip(vals[u],out))

    def insertion(self):
        """Safe-repair lower bound for each output port (both temporal sides)."""
        minima=tuple(min(v for A in T for row in A for v in row if v>0)
                     for T in self.net.tables)
        result=[]
        for f,(_,nodes,_,_,_,_) in enumerate(self.factors):
            touched=set()
            volume=1
            for t,b in nodes:
                volume*=len(self.states[b])
                for j,u,h in self.inc[b]:touched.add((t-h,j))
            # target likelihood ratio >= min labelled safe entry / wildcard <=1.
            # Safe configuration mass >= product minima / volume.
            result.append(minima[f]*prod(minima[j] for _,j in touched)/volume)
        return tuple(result)


def rectangular_packets(B):
    """Fast path: product support across block coordinates, not micro sites."""
    env=[]
    for _,nodes,groups,vals,sf,tables in B.factors:
        out={uv:F(1) for uv in combinations(range(len(nodes)),2)}
        for D in tables:
            active=tuple(x for x,v in D.items() if v)
            S=tuple(tuple(sorted({x[u] for x in active})) for u in range(len(nodes)))
            if len(active)!=prod(map(len,S)):raise ValueError("cross-block support")
            for u,v in out:
                rest=tuple(k for k in range(len(nodes)) if k not in (u,v))
                for ctx in product(*(S[k] for k in rest)):
                    x=list(sf)
                    for k,a in zip(rest,ctx):x[k]=a
                    rows=[]
                    for a in S[u]:
                        x[u]=a;row=[]
                        for b in S[v]:
                            x[v]=b;row.append(D[tuple(x)])
                        rows.append(row)
                    for a,b in combinations(rows,2):
                        r=tuple(x/y for x,y in zip(a,b))
                        out[u,v]=max(out[u,v],max(r)/min(r))
        env.append(out)
    return tuple(env)


def rectangular_rows(B):
    env=rectangular_packets(B);out=[]
    for terminal in (False,True):
        rows=[]
        for b in range(B.n):
            R=defaultdict(lambda:F(1))
            for f,u,nodes in B.incident(b,terminal):
                for v,node in enumerate(nodes):
                    if u!=v:R[node]*=env[f][tuple(sorted((u,v)))]
            rows.append({j:ratio_tv(r) for j,r in R.items() if r>1})
        out.append(tuple(rows))
    return out[0],out[1],len(env)


def blanket_row(B,b,terminal,max_contexts):
    factors=B.incident(b,terminal)
    nodes=tuple(sorted({v for _,_,ns in factors for v in ns}-{(0,b)}))
    sizes=tuple(len(B.states[j]) for _,j in nodes)
    labels=tuple(range(B.net.labels[f]+1) for f,_,_ in factors)
    work=prod(sizes)*prod(map(len,labels))*len(B.states[b])
    if work>max_contexts:raise ValueError("local blanket budget")
    contexts=tuple(product(*(range(n) for n in sizes)))
    # Precompute each factor's extended restriction once per boundary context.
    sections={}
    for k,(f,u,ns) in enumerate(factors):
        for a in labels[k]:
            S={}
            for x in product(*(range(len(B.states[j])) if v!=u else range(1)
                               for v,(_,j) in enumerate(ns))):
                ctx=tuple(B.partial(f,v,B.states[j][x[v]]) for v,(_,j) in enumerate(ns))
                res=B.restriction(f,u,a,ctx)
                S[x]=tuple(res[B.partial(f,u,s)] for s in B.states[b])
            sections[k,a]=S
    index={v:k for k,v in enumerate(nodes)}
    keys=tuple(tuple(tuple(0 if v==u else x[index[node]] for v,node in enumerate(ns))
                           for f,u,ns in factors) for x in contexts)
    row={v:F(0) for v in nodes}
    ctxindex={x:k for k,x in enumerate(contexts)}
    for obs in product(*labels):
        D=[]
        for key in keys:
            weights=tuple(prod(sections[k,a][x][s] for k,(a,x) in enumerate(zip(obs,key)))
                          for s in range(len(B.states[b])))
            total=sum(weights)
            if total<=0:raise ValueError("safe extension normalization")
            D.append(tuple(v/total for v in weights))
        for k,x in enumerate(contexts):
            for j,node in enumerate(nodes):
                for z in range(x[j]+1,sizes[j]):
                    y=x[:j]+(z,)+x[j+1:];q=D[ctxindex[y]]
                    row[node]=max(row[node],sum(abs(a-b) for a,b in zip(D[k],q))/2)
    return {j:v for j,v in row.items() if v},work


def exact_rows(B,max_contexts=2000000):
    out=[];work=0;cache={}
    for terminal in (False,True):
        rows=[]
        for b in range(B.n):
            # Canonical local types using relative block IDs and exact factors.
            inc=B.incident(b,terminal);nodes=tuple(sorted({v for _,_,ns in inc for v in ns}-{(0,b)}))
            ids={v:k for k,v in enumerate(nodes)};ids[0,b]=-1
            key=(len(B.states[b]),B.safes[b],tuple((len(B.states[j]),B.safes[j]) for _,j in nodes),
                 tuple((u,tuple(ids[v] for v in ns),
                        tuple(tuple(B.partial(f,v,s) for s in B.states[j]) for v,(_,j) in enumerate(ns)),
                        B.factors[f][4],tuple(tuple(D.items()) for D in B.factors[f][5]))
                       for f,u,ns in inc))
            if key in cache:
                values=cache[key];row={v:a for v,a in zip(nodes,values) if a}
            else:
                row,c=blanket_row(B,b,terminal,max_contexts-work);work+=c
                cache[key]=tuple(row.get(v,F(0)) for v in nodes)
            rows.append(row)
        out.append(tuple(rows))
    return out[0],out[1],work


def verify_spatial(A,w,C=None):
    w=tuple(map(F,w))
    if len(A)!=len(w) or min(w)<=0:raise ValueError("spatial weights")
    C=A if C is None else C
    q=max(max(row_action(row,w,F(1)),row_action(end,w,F(1)))/w[i]
          for i,(row,end) in enumerate(zip(A,C)))
    if q>=1:raise ValueError("spatial gain failed")
    return {"spatial_gain":q,"spatial_rate":q,"spatial_prefactor":max(w)/min(w)}


def certify(net,blocks,safe=None,method="rectangular",rates=None,max_contexts=2000000,max_block_states=256):
    try:
        B=BlockNetwork(net,blocks,safe,max_block_states)
        if method=="rectangular":A,C,work=rectangular_rows(B)
        elif method=="exact":A,C,work=exact_rows(B,max_contexts)
        else:raise ValueError("unknown method")
    except ValueError as e:return {"outcome":"undecided","boundary":str(e)}
    G=discover_gain(A,C,rates,max_dense=32,sparse_steps=8)
    # Temporal tilt is optional for two-sided finite block comparison.
    w=G["weights"] if G else (F(1),)*B.n
    try:S=verify_spatial(A,w,C)
    except ValueError:
        return {"outcome":"undecided","boundary":"spatial gain search","work":work}
    return dict(S,outcome="certified",method=method,blocks=B.blocks,safe=B.safe,
                weights=w,temporal=G,insertion_nonnull=B.insertion(),
                positive_wildcard=all(v>0 for T in net.tables for row in T[-1] for v in row),
                interior=A,terminal=C,work=work,joint_state_constructed=False)


def replay(net,witness,max_contexts=2000000,max_block_states=256):
    B=BlockNetwork(net,witness["blocks"],witness["safe"],max_block_states)
    if witness["method"]=="rectangular":A,C,_=rectangular_rows(B)
    elif witness["method"]=="exact":A,C,_=exact_rows(B,max_contexts)
    else:raise ValueError("unknown method")
    S=verify_spatial(A,witness["weights"],C)
    G=witness.get("temporal")
    if G is not None:verify_gain(A,C,G["weights"],G["rho"])
    return dict(S,insertion_nonnull=B.insertion(),
                positive_wildcard=all(v>0 for T in net.tables for row in T[-1] for v in row))


def finest_product_scope(support,arity,budget):
    """Finest product decomposition of a finite nonempty relation.
    Exact support projections, with an explicit local split budget.
    """
    if not support:raise ValueError("empty factor support")
    def rec(indices,R):
        if len(indices)<2:return (indices,)
        k=len(indices)
        for mask in range(1<<(k-1)):
            A=(0,)+tuple(j for j in range(1,k) if mask & (1<<(j-1)))
            if len(A)==k:continue
            if budget[0]<=0:raise ValueError("support split budget")
            budget[0]-=1
            C=tuple(j for j in range(k) if j not in A)
            U={tuple(x[j] for j in A) for x in R}
            V={tuple(x[j] for j in C) for x in R}
            if len(R)==len(U)*len(V):
                return rec(tuple(indices[j] for j in A),U)+rec(tuple(indices[j] for j in C),V)
        return (indices,)
    return rec(tuple(range(arity)),set(support))


def discover_spatial_blocks(net,max_splits=100000,max_block_states=256):
    """Finest spatial partition making every label support a block product.

    A support component spanning times cannot be grouped by this language.
    A budget exhaustion is undecided, not a nonexistence decision.
    """
    root=list(range(net.n));budget=[max_splits];cache={}
    def find(i):
        while root[i]!=i:
            root[i]=root[root[i]];i=root[i]
        return i
    try:
        for i,p in enumerate(net.parents):
            scope=tuple((-1,j) for j in p)+((0,i),)
            for A in net.tables[i]:
                R=tuple(x+(y,) for x,k in net.lookup[i].items() for y,v in enumerate(A[k]) if v)
                key=(len(scope),R)
                if key not in cache:cache[key]=finest_product_scope(R,len(scope),budget)
                for C in cache[key]:
                    if len({scope[j][0] for j in C})>1:
                        return {"outcome":"cross_time_support","factor":i}
                    a=find(scope[C[0]][1])
                    for j in C[1:]:root[find(scope[j][1])]=a
    except ValueError as e:return {"outcome":"undecided","boundary":str(e)}
    groups=defaultdict(list)
    for j in range(net.n):groups[find(j)].append(j)
    blocks=tuple(tuple(b) for b in sorted(groups.values()))
    if max(prod(net.sizes[j] for j in b) for b in blocks)>max_block_states:
        return {"outcome":"undecided","boundary":"block state budget"}
    return {"outcome":"rectangular_partition","blocks":blocks,
            "split_checks":max_splits-budget[0]}


def pair_ring(n,eps=F(1,128)):
    """Hard equality observations within pairs, weak physical feedback across pairs."""
    if n<2:raise ValueError("two pairs required")
    parents=[];tables=[]
    for i in range(n):
        j=2*i;k=2*((i-1)%n)
        parents.extend(((j,j+1,k),()))
        T=[]
        for z in (0,1):
            rows=[]
            for x,y,v in product((0,1),repeat=3):
                h=F(1,2) if x==y else F(0)
                p=F(1,2)+eps*(2*x-1)+eps*(2*v-1)
                rows.append(tuple((h if z else 1-h)*(p if b else 1-p) for b in (0,1)))
            T.append(tuple(rows))
        tables.extend((tuple(T),(((F(1,2),F(1,2)),),)))
    return SupportedNetwork((2,)*(2*n),tuple(parents),tuple(tables))


def exclusion_ring(n,base=F(1,32),eps=F(1,256)):
    """Hard crossing constraint: label1 forbids child1 with occupied parent."""
    if n<2:raise ValueError("two sites required")
    parents=tuple((i,(i-1)%n) for i in range(n))
    T=[]
    for z in (0,1):
        rows=[]
        for x,v in product((0,1),repeat=2):
            p=base+eps*v
            row=[]
            for y in (0,1):
                h=F(0) if y and (x or v) else F(1,2)
                row.append((p if y else 1-p)*(h if z else 1-h))
            rows.append(tuple(row))
        T.append(tuple(rows))
    return SupportedNetwork((2,)*n,parents,(tuple(T),)*n)


def phase_channel(x,y):
    """E, soft plus, soft minus, D: full observed support with hard equality."""
    e=F(1,2) if x==y else F(0)
    p=F(1+x+y,16);m=F(3-x-y,16)
    return e,p,m,1-e-p-m


def phase_ring(n):
    """Finite periodic template for the spatial equality/soft pin channel."""
    if n<2:raise ValueError("ring size")
    T=tuple(tuple((phase_channel(x,y)[a]/2,)*2 for x,y in product((0,1),repeat=2))
            for a in range(4))
    return SupportedNetwork((2,)*n,tuple((i,(i+1)%n) for i in range(n)),(T,)*n)


def chain_mass(clamps,left=None):
    """Exact fair iid binary hidden chain with edge labels, wildcard None."""
    v=(F(1,2),F(1,2)) if left is None else tuple(F(a==left) for a in (0,1))
    for a in clamps:
        v=tuple(sum(v[x]*(F(1) if a is None else phase_channel(x,y)[a])/2 for x in (0,1)) for y in (0,1))
    return sum(v)


def phase_witness(n,sign):
    if n<1 or sign not in (1,2):raise ValueError("bad phase witness")
    pre=(sign,)+(0,)*n;post=(0,)*n+(sign,)
    p=chain_mass(pre+(None,)+post)
    return tuple(chain_mass(pre+(a,)+post)/p for a in range(4))
