"""WP13: reusable positive interfaces, finite-memory support synchronization,
and margin-conditional adaptive packing covers. Exact rational arithmetic.
"""
from fractions import Fraction as F
from itertools import product
from collections import deque
from math import prod, floor

from observable_memory_certificate import ObservableFiniteMemory
from observable_polytope_certificate import PredictiveQuotient, solve_square, row_mul, project
from adaptive_graph_certificate import (
    Chart, replay_witness, image_box, corners, contains, hull, rational_rate,
    linear_min, component_numerator, column_norm,
)
from marked_reset_spectral import multiply


def strict_box_interface(model, witness, max_bits=20, max_vertices=64):
    """Replay a WP12 witness, then try its padded enclosing box as an
    original-alphabet positive interface. No global network search.

    The box test is sufficient, not complete. Every accepted transfer has
    an exact stationary intertwiner to the factor's observable chart.
    """
    if witness["block"]!=1:
        raise ValueError("single-letter constituent witness required")
    replay_witness(model,witness)
    chart=Chart(PredictiveQuotient(model),witness["basis"])
    k=chart.dimension-1
    if 2**k>max_vertices:raise ValueError("interface vertex budget")
    enclosure=tuple((min(C[j][0] for C in witness["boxes"]),
                     max(C[j][1] for C in witness["boxes"])) for j in range(k))
    for bits in range(1,max_bits+1):
        box=tuple((lo-F(1,2**bits),hi+F(1,2**bits)) for lo,hi in enclosure)
        try:
            images=[image_box(A,box)[1] for A in chart.matrices]
        except ValueError:
            continue
        if all(all(lo<x and y<hi for (lo,hi),(x,y) in zip(box,im)) for im in images):
            break
    else:raise ValueError("strict interface box not found")
    V=corners(box);n=len(V);Ts=[]
    for A in chart.matrices:
        rows=[]
        for v in V:
            y=project(v,A);mass=row_mul(v,A)[0]
            t=tuple((x-lo)/(hi-lo) for x,(lo,hi) in zip(y[1:],box))
            weights=tuple(prod(t[j] if c[j+1]==box[j][1] else 1-t[j]
                               for j in range(k)) for c in V)
            rows.append(tuple(mass*w for w in weights))
        Ts.append(tuple(rows))
    Q=tuple(tuple(sum(A[i][j] for A in Ts) for j in range(n)) for i in range(n))
    if any(sum(r)!=1 for r in Q):raise ValueError("interface normalization")
    eq=tuple(tuple(Q[i][j]-F(i==j) for i in range(n)) for j in range(n-1))+((F(1),)*n,)
    pi=solve_square(eq,(F(0),)*(n-1)+(F(1),))
    interface=ObservableFiniteMemory(pi,tuple(Ts))
    verify_interface(chart,interface,V)
    return interface,{"basis":chart.basis,"box":box,"vertices":V,"padding_bits":bits}


def verify_interface(chart,interface,vertices):
    """Exact factor equivalence, checked on all words by intertwining."""
    V=tuple(tuple(map(F,row)) for row in vertices)
    if len(V)!=interface.dimension or any(len(v)!=chart.dimension or v[0]!=1 for v in V):
        raise ValueError("interface shape")
    if interface.alphabet!=chart.alphabet or row_mul(interface.pi,V)!=chart.initial:
        raise ValueError("interface stationary mismatch")
    if any(multiply(T,V)!=multiply(V,A) for T,A in zip(interface.matrices,chart.matrices)):
        raise ValueError("interface intertwiner mismatch")
    return positive_margins(interface)


def positive_margins(model):
    """Reusable rational constants from a strictly positive labelled realization."""
    if any(x<=0 for A in model.matrices for row in A for x in row):
        raise ValueError("strictly positive factor interface required")
    return {
        "alphabet":model.alphabet,"dimension":model.dimension,
        "lambda":min(sum(row) for A in model.matrices for row in A),
        "beta":min(A[i][j]/model.pi[j] for A in model.matrices
                   for i in range(model.dimension) for j in range(model.dimension)),
        "gamma":max(model.Q[i][j]/model.pi[j]
                    for i in range(model.dimension) for j in range(model.dimension)),
        "letter_lo":tuple(min(sum(row) for row in A) for A in model.matrices),
        "letter_hi":tuple(max(sum(row) for row in A) for A in model.matrices),
        "entry_lo":tuple(min(A[i][j]/model.pi[j] for i in range(model.dimension)
                            for j in range(model.dimension)) for A in model.matrices),
        "entry_hi":tuple(max(A[i][j]/model.pi[j] for i in range(model.dimension)
                            for j in range(model.dimension)) for A in model.matrices),
    }


def revealed_product_margin(models,witnesses):
    """Factorwise verification for the fully revealed synchronous product.
    No tensor matrices or product graph are built.
    """
    if not models or len(models)!=len(witnesses):raise ValueError("factor list")
    checks=[replay_witness(m,w,use_local=False)[0] for m,w in zip(models,witnesses)]
    theta=max(rational_rate(r["eta"],r["contraction_length"]) for r in checks)
    C=sum(r["log_variation_constant"]/theta**(r["contraction_length"]-1) for r in checks)
    return {"theta":theta,"constant":C,"nonnull":prod(r["nonnull"] for r in checks),
            "factor_cells":tuple(r["cells"] for r in checks)}


def check_transducer(T):
    n,m,k=(T[x] for x in ("states","inputs","outputs"))
    rows=T["rows"]
    if any(not isinstance(x,int) or x<1 for x in (n,m,k)) or len(rows)!=n*m:
        raise ValueError("transducer shape")
    for row in rows:
        if any(not isinstance(z,int) or not isinstance(t,int) or not 0<=z<k or not 0<=t<n
               or p<=0 for z,t,p in row) or sum(p for z,t,p in row)!=1:
            raise ValueError("transducer stochasticity")
    return n,m,k


def finite_range_transducer(alphabet,memory,kernel):
    """Finite window rule as a stochastic observation transducer."""
    if not isinstance(memory,int) or memory<0 or not isinstance(alphabet,int) or alphabet<1:
        raise ValueError("invalid history dimensions")
    histories=tuple(product(range(alphabet),repeat=memory))
    H=tuple(tuple(map(F,row)) for row in kernel)
    if len(H)!=len(histories)*alphabet or not H or not H[0]:
        raise ValueError("kernel shape")
    k=len(H[0]);idx={h:i for i,h in enumerate(histories)}
    if any(len(row)!=k or any(t<0 for t in row) or sum(row)!=1 for row in H):
        raise ValueError("kernel stochasticity")
    T={"states":len(histories),"inputs":alphabet,"outputs":k,
       "rows":tuple(tuple((z,idx[(h+(a,))[1:]],p) for z,p in enumerate(H[i*alphabet+a]) if p)
                    for i,h in enumerate(histories) for a in range(alphabet))}
    check_transducer(T)
    return T


def serial_transducer(first,second):
    """Exact serial composition; retains intermediate memory and randomness."""
    n,m,k=check_transducer(first);r,b,l=check_transducer(second)
    if k!=b:raise ValueError("serial alphabet mismatch")
    rows=[]
    for i,j in product(range(n),range(r)):
        for a in range(m):
            out={}
            for z,t,p in first["rows"][i*m+a]:
                for w,u,q in second["rows"][j*b+z]:
                    key=(w,t*r+u)
                    out[key]=out.get(key,F(0))+p*q
            rows.append(tuple((w,v,p) for (w,v),p in sorted(out.items()) if p))
    T={"states":n*r,"inputs":m,"outputs":l,"rows":tuple(rows)}
    check_transducer(T)
    return T


def transducer_support(T):
    n,m,k=check_transducer(T)
    masks=[[0]*k for _ in range(n)]
    for i in range(n):
        for a in range(m):
            for z,t,p in T["rows"][i*m+a]:masks[i][z]|=1<<t
    return tuple(tuple(row) for row in masks),min(p for row in T["rows"] for z,t,p in row)


def channel_support(alphabet,memory,kernel):
    return transducer_support(finite_range_transducer(alphabet,memory,kernel))


def _successor(mask,masks,z):
    out=0
    while mask:
        bit=mask & -mask;mask-=bit
        out|=masks[bit.bit_length()-1][z]
    return out


def synchronization(masks,max_nodes=100000):
    """Decide eventual equality of all Boolean rows by unequal subset-pair graph.
    Assumes every history can emit every label (otherwise reject).
    """
    n=len(masks)
    if not n or not masks[0] or any(len(r)!=len(masks[0]) for r in masks):
        raise ValueError("bad support automaton")
    if any(not isinstance(x,int) or not 0<x<(1<<n) for r in masks for x in r):
        raise ValueError("every history must emit every label")
    if max_nodes<1:raise ValueError("node budget")
    k=len(masks[0])
    initial=[(1<<i,1<<j) for i in range(n) for j in range(i+1,n)]
    if len(initial)>max_nodes:return {"outcome":"undecided","boundary":"support node budget"}
    graph={p:None for p in initial};queue=deque(initial)
    while queue:
        p=queue.popleft();dest=set()
        for z in range(k):
            x,y=(_successor(t,masks,z) for t in p)
            if x==y:continue
            q=tuple(sorted((x,y)));dest.add(q)
            if q not in graph:
                if len(graph)>=max_nodes:return {"outcome":"undecided","boundary":"support node budget"}
                graph[q]=None;queue.append(q)
        graph[p]=tuple(sorted(dest))
    indeg={p:0 for p in graph}
    for dest in graph.values():
        for q in dest:indeg[q]+=1
    ready=deque(p for p in graph if indeg[p]==0);depth={p:0 for p in graph};seen=0
    while ready:
        p=ready.popleft();seen+=1
        for q in graph[p]:
            depth[q]=max(depth[q],depth[p]+1);indeg[q]-=1
            if indeg[q]==0:ready.append(q)
    if seen!=len(graph):
        return {"outcome":"support_obstruction","nodes":len(graph),
                "boundary":"reachable unequal subset-pair cycle"}
    return {"outcome":"synchronized","block":1+max(depth.values(),default=0),
            "nodes":len(graph),"edges":sum(map(len,graph.values()))}


def weighted_path_bounds(T,margins,s,max_words):
    """Optional tighter bounds using only weighted interface-state paths.

    At the final step the bounds are relative to product stationary mass.
    No joint microscopic transfer matrix is constructed.
    """
    n,m,k=check_transducer(T)
    if k**s>max_words:return None
    letters=tuple(product(*(range(r["alphabet"]) for r in margins)))
    weights={key:tuple(prod(r[key][a] for r,a in zip(margins,w)) for w in letters)
             for key in ("letter_lo","letter_hi","entry_lo","entry_hi")}
    matrices={}
    for key,v in weights.items():
        A=[[[F(0)]*n for _ in range(n)] for _ in range(k)]
        for i in range(n):
            for a in range(m):
                for z,j,p in T["rows"][i*m+a]:A[z][i][j]+=p*v[a]
        matrices[key]=tuple(tuple(tuple(row) for row in mat) for mat in A)
    delta=F(1,2)
    from marked_reset_spectral import identity
    for w in product(range(k),repeat=s):
        L=U=identity(n)
        for z in w[:-1]:
            L=multiply(L,matrices["letter_lo"][z])
            U=multiply(U,matrices["letter_hi"][z])
        L=multiply(L,matrices["entry_lo"][w[-1]])
        U=multiply(U,matrices["entry_hi"][w[-1]])
        for j in range(n):
            hi=max(row[j] for row in U)
            if hi:
                lo=min(row[j] for row in L)
                if lo<=0:raise ValueError("weighted support mismatch")
                delta=min(delta,lo/hi)
    return delta


def certify_transducer(margins,T,max_nodes=100000,max_weighted_words=64):
    """Compose already verified positive factor margins with a transducer.

    The finite interface constants must come from positive_margins or exact
    interface replay. Use compose_positive for replay from actual models.
    """
    if not margins:raise ValueError("empty factors")
    n,m,k=check_transducer(T)
    if m!=prod(r["alphabet"] for r in margins):raise ValueError("joint input alphabet")
    masks,alpha=transducer_support(T)
    if any(not x for row in masks for x in row):
        return {"outcome":"support_obstruction","boundary":"missing row label"}
    sync=synchronization(masks,max_nodes)
    if sync["outcome"]!="synchronized":return sync
    s=sync["block"]
    lam=prod(r["lambda"] for r in margins)
    beta=prod(r["beta"] for r in margins)
    gamma=prod(r["gamma"] for r in margins)
    baseline=min(F(1,2),alpha**s*lam**(s-1)*beta/gamma)
    weighted=weighted_path_bounds(T,margins,s,max_weighted_words)
    delta=max(baseline,weighted) if weighted is not None else baseline
    eta=1-delta
    c=alpha*lam
    # Lower bound actual one-symbol mass using per-letter row bounds.
    letters=tuple(product(*(range(r["alphabet"]) for r in margins)))
    lows=tuple(prod(r["letter_lo"][a] for r,a in zip(margins,w)) for w in letters)
    c=max(c,min(sum(lows[a]*p for a in range(m) for z1,j,p in T["rows"][i*m+a] if z1==z)
                    for i in range(n) for z in range(k)))
    return dict(sync,outcome="certified",nonnull=c,eta=eta,
                constant=max(1/c,1/(delta**2*eta)),delta=delta,
                baseline_delta=baseline,weighted_delta=weighted,
                alpha=alpha,lambda_product=lam,beta_product=beta,gamma_product=gamma,
                history_states=n,factor_dimensions=tuple(r["dimension"] for r in margins),
                joint_lift_constructed=False)


def compose_positive(interfaces,memory,kernel,max_nodes=100000,max_weighted_words=64):
    """Verify factor interfaces and one finite-range readout, no joint lift."""
    if not interfaces:raise ValueError("empty factors")
    margins=tuple(positive_margins(m) for m in interfaces)
    T=finite_range_transducer(prod(r["alphabet"] for r in margins),memory,kernel)
    return certify_transducer(margins,T,max_nodes,max_weighted_words)


def joint_product(models):
    """Reference-only materialized independent product for tests."""
    states=tuple(product(*(range(m.dimension) for m in models)))
    letters=tuple(product(*(range(m.alphabet) for m in models)))
    pi=tuple(prod(m.pi[i] for m,i in zip(models,u)) for u in states)
    A=tuple(tuple(tuple(prod(m.matrices[a][i][j] for m,a,i,j in zip(models,w,u,v))
                        for v in states) for u in states) for w in letters)
    return ObservableFiniteMemory(pi,A)


def coupled_kernel4():
    """Two independent binary inputs, consecutive joint pair windows.
    Both output supports omit one transition, all two-step products full.
    Non-product likelihood in current and previous joint symbols.
    """
    zero=tuple(F(0) if (h,a)==(0,3) else F(1) if (h,a)==(3,0)
               else F(1+(h+2*a+h*a)%3,4) for h in range(4) for a in range(4))
    return tuple((x,1-x) for x in zero)


def packing_bound(k,radius,rate,diameter=1):
    """Lattice counting bound for separated adaptive centers, no grid traversal."""
    radius,rate,diameter=map(F,(radius,rate,diameter))
    if k<0 or radius<=0 or not 0<=rate<1 or diameter<0:
        raise ValueError("invalid packing margins")
    separation=(1-rate)*radius
    return (floor(diameter/separation)+1)**k


def packing_cover(chart,block,radius,rate,max_cells=256,max_primitives=4096):
    """Greedy exact centers, uniform radius. Reuse only at verified containment.
    Under uniform contraction on the reachable-state neighborhood this
    terminates by the packing bound; otherwise fail closed at finite budgets.
    """
    radius,rate=F(radius),F(rate)
    if radius<=0 or not 0<=rate<1 or max_cells<1 or block<1:
        raise ValueError("invalid packing search")
    if chart.alphabet**block>max_primitives:raise ValueError("primitive budget")
    A=tuple(chart.word_matrix(w) for w in product(range(chart.alphabet),repeat=block))
    sep=(1-rate)*radius
    centers=[]
    def near(x):
        return next((i for i,y in enumerate(centers)
                     if max((abs(a-b) for a,b in zip(x[1:],y[1:])),default=F(0))<=sep),None)
    def add(x):
        i=near(x)
        if i is not None:return i
        if len(centers)>=max_cells:raise ValueError("packing cell budget")
        centers.append(x);return len(centers)-1
    def box(x):
        return tuple((v-radius,v+radius) for v in x[1:])
    add(chart.initial)
    edges=[]
    for x in centers:
        row=[]
        for T in A:
            y=project(x,T);j=add(y)
            _,im=image_box(T,box(x))
            if not contains(box(centers[j]),im):
                raise ValueError("packing enclosure failed")
            row.append(j)
        edges.append(tuple(row))
    return tuple(box(x) for x in centers),tuple(edges),tuple(centers)


def discover_packing(chart,max_block=3,max_bits=10,max_cells=256,max_primitives=64):
    """Bounded margin-free trial of the constructive packing language."""
    attempts=0;failures={}
    for block in range(1,max_block+1):
        for bits in range(2,max_bits+1):
            attempts+=1
            try:
                boxes,edges,centers=packing_cover(chart,block,F(1,2**bits),F(1,2),
                                                 max_cells,max_primitives)
                result=verify_packing_cover(chart,block,boxes,edges)
            except ValueError as exc:
                key=str(exc);failures[key]=failures.get(key,0)+1
                continue
            return dict(result,outcome="certified",boxes=boxes,edges=edges,
                        centers=centers,bits=bits,attempts=attempts,failures=failures,
                        basis=chart.basis)
    return {"outcome":"undecided","attempts":attempts,"failures":failures}


def verify_packing_cover(chart,block,boxes,edges,weights=None):
    """Stationary convexification permits a single seed, no shorter words.
    Factorize max over ordered pairs into numerator maxima and denominator minima.
    """
    d=chart.dimension;k=d-1;n=len(boxes)
    if block<1 or not n or any(len(B)!=k or any(l>u for l,u in B) for B in boxes):
        raise ValueError("packing cover shape")
    if not any(contains(B,hull((chart.initial,))) for B in boxes):
        raise ValueError("missing stationary seed")
    A=tuple(chart.word_matrix(w) for w in product(range(chart.alphabet),repeat=block))
    if len(edges)!=n or any(len(r)!=len(A) or any(not isinstance(i,int) or not 0<=i<n for i in r) for r in edges):
        raise ValueError("packing edge shape")
    w=(F(1),)*k if weights is None else tuple(map(F,weights))
    if len(w)!=k or any(x<=0 for x in w):raise ValueError("bad packing metric")
    c=min(linear_min(B,tuple(row[0] for row in T)) for B in boxes for T in chart.matrices)
    if c<=0:raise ValueError("packing nonnullness")
    eta=F(0)
    for a,T in enumerate(A):
        den=[];num=[]
        for i,B in enumerate(boxes):
            low,im=image_box(T,B)
            if not contains(boxes[edges[i][a]],im):raise ValueError("packing enclosure failed")
            den.append(low);num.append(column_norm(component_numerator(T,im),w))
        eta=max(eta,max(num)/min(den))
    if eta>=1:raise ValueError("packing contraction failed")
    diameter=max(((max(B[j][1] for B in boxes)-min(B[j][0] for B in boxes))/w[j]
                  for j in range(k)),default=F(0))
    J=max(sum(w[i-1]*abs(T[i][0]) for i in range(1,d)) for T in chart.matrices)
    return {"block":block,"contraction_length":block,"horizon":1,"eta":eta,
            "nonnull":c,"diameter":diameter,"log_variation_constant":J*diameter/c,
            "cells":n,"enclosure_edges":n*len(A),"pair_edges":0,
            "primitive_words":len(A),"weights":w}


def guaranteed_packing_budget(d,alphabet,b,J,H,theta):
    """Conditional resources from WP11 all-word bounds in raw predictive coordinates."""
    b,J,H,theta=map(F,(b,J,H,theta));k=d-1
    if d<1 or alphabet<1 or not 0<b<=1 or J<=0 or H<0 or not 0<theta<1:
        raise ValueError("invalid packing hypotheses")
    if k==0:return {"block":1,"radius":F(1,4),"rate":F(1,2),
                   "cell_bound":1,"primitive_bound":alphabet}
    R=min(F(1,4),b/(2*k*J))
    D=4*k*(1+2*k)*H/b**2
    s=1
    while D*theta**s>F(1,2):s+=1
    return {"block":s,"radius":R,"rate":F(1,2),
            "cell_bound":packing_bound(k,R,F(1,2)),"primitive_bound":alphabet**s}
