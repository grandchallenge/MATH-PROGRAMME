"""WP12: rational preconditioning, adaptive image boxes, graph contraction.

All accepted margins are checked in exact arithmetic. Bounded synthesis
failure is inconclusive. Short primitive blocks are optional; long
contraction horizons are checked by graph dynamic programming, not words.
"""
from fractions import Fraction as F
from itertools import product
from math import floor, ceil
from observable_memory_certificate import _rank
from observable_polytope_certificate import PredictiveQuotient, row_mul, project, solve_square
from marked_reset_spectral import identity, multiply


def inverse(A):
    return tuple(zip(*(solve_square(A,col) for col in identity(len(A)))))


def centered_basis(model,q,mode="weighted",swaps=32):
    """Exact model-derived affine basis, weighted hidden rows or reachable rows.

    Max-volume swaps only improve the determinant relative to the finite
    candidate pool. They do not assert optimal numerical conditioning.
    """
    d=q.dimension
    if mode=="raw":
        return (q.initial,)+tuple(identity(d)[i] for i in range(1,d))
    if mode in ("weighted","hidden"):
        cols=[model.message(w) for w in q.probes]
        points=[tuple(col[i] for col in cols) for i in range(model.dimension)]
        weights=model.pi if mode=="weighted" else (F(1),)*len(points)
    elif mode=="reachable":
        points=[q.state(w) for w,_ in model.left_basis]
        weights=(F(1),)*len(points)
    else:raise ValueError("unknown chart")
    pool=tuple(tuple(t*(x-y) for x,y in zip(p,q.initial))
               for p,t in zip(points,weights))
    basis=[q.initial]
    for v in pool:
        if _rank(basis+[v])>len(basis):basis.append(v)
        if len(basis)==d:break
    if len(basis)!=d:raise ValueError("chart basis incomplete")
    for _ in range(swaps):
        inv=inverse(tuple(basis))
        best=None;gain=F(1)
        for v in pool:
            coords=row_mul(v,inv)
            for j in range(1,d):
                if abs(coords[j])>gain:gain=abs(coords[j]);best=(j,v)
        if best is None:break
        basis[best[0]]=best[1]
    return tuple(basis)


class Chart:
    def __init__(self,q,basis):
        self.quotient=q
        self.basis=tuple(tuple(map(F,row)) for row in basis)
        d=q.dimension
        if len(self.basis)!=d or any(len(row)!=d for row in self.basis):
            raise ValueError("basis shape")
        if tuple(row[0] for row in self.basis)!=(F(1),)+(F(0),)*(d-1):
            raise ValueError("basis must preserve normalization")
        inv=inverse(self.basis)
        self.inv=inv
        self.initial=row_mul(q.initial,inv)
        self.matrices=tuple(multiply(multiply(self.basis,A),inv) for A in q.matrices)
        self.dimension=d;self.alphabet=q.alphabet

    def word_matrix(self,w):
        A=identity(self.dimension)
        for a in w:A=multiply(A,self.matrices[a])
        return A

    def state(self,w):
        return project(self.initial,self.word_matrix(w))

    def probability(self,w):
        return row_mul(self.initial,self.word_matrix(w))[0]


def corners(box):
    return tuple((F(1),)+v for v in product(*tuple(
        (lo,) if lo==hi else (lo,hi) for lo,hi in box)))


def hull(points):
    return tuple((min(x[j] for x in points),max(x[j] for x in points))
                 for j in range(1,len(points[0])))


def contains(box,other):
    return all(lo<=l and h<=hi for (lo,hi),(l,h) in zip(box,other))


def join(a,b):
    return tuple((min(l,x),max(h,y)) for (l,h),(x,y) in zip(a,b))


def padded(box,h):
    return tuple((h*(floor(lo/h)-1),h*(ceil(hi/h)+1)) for lo,hi in box)


def image(A,V):
    rows=tuple(row_mul(v,A) for v in V)
    den=min(y[0] for y in rows)
    if den<=0:raise ValueError("nonpositive denominator")
    Y=tuple(tuple(x/y[0] for x in y) for y in rows)
    return den,Y,hull(Y)


def linear_min(box,col):
    return col[0]+sum(min(a*l,a*u) for a,(l,u) in zip(col[1:],box))


def fractional_max(box,num,den):
    """Exact linear-fractional maximum on a box with positive denominator.

    Sweep sign changes of num_i-r*den_i in ascending breakpoint order.
    At most k+1 vertices, generated incrementally, rather than 2**k.
    """
    if linear_min(box,den)<=0:raise ValueError("nonpositive denominator")
    v=[];flips=[]
    for i,(lo,hi) in enumerate(box,1):
        a,b=num[i],den[i]
        if b>0:
            v.append(hi);flips.append((a/b,i,lo-hi))
        elif b<0:
            v.append(lo);flips.append((a/b,i,hi-lo))
        else:v.append(hi if a>=0 else lo)
    top=num[0]+sum(a*x for a,x in zip(num[1:],v))
    bottom=den[0]+sum(b*x for b,x in zip(den[1:],v))
    best=top/bottom
    for _,i,delta in sorted(flips):
        top+=num[i]*delta;bottom+=den[i]*delta
        best=max(best,top/bottom)
    return best


def image_box(A,box):
    """Exact coordinate envelope of a projective box image, no corners."""
    cols=tuple(zip(*A));den=cols[0]
    low=linear_min(box,den)
    if low<=0:raise ValueError("nonpositive denominator")
    im=tuple((-fractional_max(box,tuple(-x for x in col),den),
              fractional_max(box,col,den)) for col in cols[1:])
    return low,im


def component_numerator(A,im):
    """Exact coordinatewise numerator suprema, independent of source cell."""
    d=len(A)
    return tuple(tuple(max(abs(A[i][j]-A[i][0]*lo),
                           abs(A[i][j]-A[i][0]*hi))
                       for j,(lo,hi) in enumerate(im,1)) for i in range(1,d))


def block_system(chart,block):
    words=tuple(product(range(chart.alphabet),repeat=block))
    A=tuple(chart.word_matrix(w) for w in words)
    seeds=tuple(chart.state(w) for n in range(block)
                for w in product(range(chart.alphabet),repeat=n))
    return A,seeds


def adaptive_boxes(chart,block,bits,rounds,max_cells,depth=1,max_extent=64):
    """Image-driven local hulls indexed by short block contexts.

    The transient seeds include all shorter-prefix histories. Boxes widen
    only when an exact image is not enclosed. Dyadic rounding is outward.
    No uniform grid of the ambient prediction space is enumerated.
    """
    if any(not isinstance(n,int) or n<1 for n in (block,bits,rounds,max_cells,depth)):
        raise ValueError("invalid cover budget")
    m=chart.alphabet**block
    seed_count=sum(chart.alphabet**n for n in range(block))
    if seed_count+sum(m**n for n in range(1,depth+1))>max_cells:
        raise ValueError("cell budget")
    A,seeds=block_system(chart,block)
    keys=tuple(w for n in range(1,depth+1) for w in product(range(m),repeat=n))
    idx={w:len(seeds)+i for i,w in enumerate(keys)}
    h=F(1,2**bits)
    boxes=[hull((x,)) for x in seeds]
    for w in keys:
        X=seeds[0]
        for a in w:X=project(X,A[a])
        boxes.append(padded(hull((X,)),h))
    edges=tuple(tuple(idx[((() if i<len(seeds) else keys[i-len(seeds)])+(a,))[-depth:]]
                      for a in range(m)) for i in range(len(boxes)))
    for step in range(rounds+1):
        updates=list(boxes);changed=False
        for i,box in enumerate(boxes):
            for a,T in enumerate(A):
                _,im=image_box(T,box);j=edges[i][a]
                if not contains(updates[j],im):
                    updates[j]=join(updates[j],padded(im,h));changed=True
        if not changed:
            return tuple(boxes),edges,step
        if any(max(abs(l),abs(u))>max_extent for box in updates for l,u in box):
            raise ValueError("cover extent budget")
        boxes=updates
    raise ValueError("cover widening budget")


def component_bound(A,den,Y):
    """Entrywise nonnegative secant majorant, row-vector orientation."""
    d=len(A)
    return tuple(tuple(max(abs(A[i][j]-A[i][0]*y[j]) for y in Y)/den
                       for j in range(1,d)) for i in range(1,d))


def matrix_max(matrices,k):
    return tuple(tuple(max(A[i][j] for A in matrices) for j in range(k))
                 for i in range(k))


def column_norm(A,weights):
    return max((sum(weights[i]*A[i][j] for i in range(len(weights)))/weights[j]
                for j in range(len(weights))),default=F(0))


def comparison_weights(E):
    """Candidate diagonal metric from a common positive majorant.

    Solve (I-E^T) w=1 and accept only a positive exact solution.
    A failed solve is not a stability decision.
    """
    k=len(E)
    if not k:return ()
    A=tuple(tuple(F(i==j)-E[j][i] for j in range(k)) for i in range(k))
    try:w=solve_square(A,(F(1),)*k)
    except ValueError:return (F(1),)*k
    if min(w)<=0:return (F(1),)*k
    return tuple(F(ceil(256*x/min(w)),256) for x in w)


def rational_rate(eta,horizon):
    """Rational 0<rho<1 with eta < rho**horizon, using strict checks."""
    if not 0<=eta<1 or horizon<1:raise ValueError("invalid contraction rate")
    rho=F(1,2)
    while rho**horizon<=eta:rho=(1+rho)/2
    return rho


def scalar_potential(scalars,targets,eta,horizon):
    """Local positive rational graph potential for a scalar horizon proof."""
    rho=rational_rate(eta,horizon)
    h=(F(1),)*len(scalars)
    for _ in range(horizon-1):
        h=tuple(max(F(1),max(l*h[q]/rho for l,q in zip(row,dest)))
                for row,dest in zip(scalars,targets))
    if any(l*h[q]>rho*h[p] for p,(row,dest) in enumerate(zip(scalars,targets))
           for l,q in zip(row,dest)):
        raise ValueError("scalar potential identity failed")
    return {"rho":rho,"potential":h,"potential_ratio":max(h)/min(h)}


def graph_horizon(B,targets,max_horizon,weights=None):
    """Exact scalar and componentwise Bellman upper bounds on all paths.

    B[p][a] is the nonnegative secant matrix for an ordered pair of cells.
    No enumeration of paths of length t. One componentwise maximum may
    combine different words; it is conservative, not an equality claim.
    """
    if not B or len(B)!=len(targets) or max_horizon<1:
        raise ValueError("invalid graph")
    k=len(B[0][0])
    if k==0:return {"horizon":1,"eta":F(0),"method":"zero tangent","weights":()}
    w=tuple(weights) if weights is not None else comparison_weights(
        matrix_max(tuple(A for row in B for A in row),k))
    if len(w)!=k or min(w)<=0:raise ValueError("bad metric")
    scalars=tuple(tuple(column_norm(A,w) for A in row) for row in B)
    scalar=(F(1),)*len(B);mat=(identity(k),)*len(B)
    for t in range(1,max_horizon+1):
        scalar=tuple(max(l*scalar[q] for l,q in zip(row,dest))
                     for row,dest in zip(scalars,targets))
        mat=tuple(matrix_max(tuple(multiply(A,mat[q]) for A,q in zip(row,dest)),k)
                  for row,dest in zip(B,targets))
        e1=max(scalar);e2=max(column_norm(A,w) for A in mat)
        if min(e1,e2)<1:
            data={"horizon":t,"eta":min(e1,e2),
                    "method":"scalar" if e1<=e2 else "component",
                    "weights":w,"one_step_eta":max(max(row) for row in scalars)}
            if e1<1:data.update(scalar_potential(scalars,targets,e1,t))
            return data
    raise ValueError("graph horizon budget")


def verify_cover(chart,block,boxes,edges,max_horizon,weights=None,local=None):
    """Replay complete finite witness, including all initial remainders.

    Boxes are allowed to be disconnected. Pair graph uses synchronized
    labels and two-point secants, not derivatives on an assumed convex union.
    """
    if not isinstance(block,int) or block<1:raise ValueError("bad block")
    A,seeds=block_system(chart,block)
    boxes=tuple(tuple(tuple(map(F,p)) for p in box) for box in boxes)
    n=len(boxes);k=chart.dimension-1
    if not n or any(len(box)!=k or any(l>u for l,u in box) for box in boxes):
        raise ValueError("invalid boxes")
    if any(not any(contains(box,hull((x,))) for box in boxes) for x in seeds):
        raise ValueError("missing seed")
    if len(edges)!=n or any(len(row)!=len(A) or any(not isinstance(j,int) or not 0<=j<n for j in row) for row in edges):
        raise ValueError("invalid successors")
    c=min(linear_min(box,tuple(row[0] for row in T))
          for box in boxes for T in chart.matrices)
    if c<=0:raise ValueError("one-letter nonnullness")
    info=[]
    for i,box in enumerate(boxes):
        row=[]
        for a,T in enumerate(A):
            den,im=image_box(T,box)
            if not contains(boxes[edges[i][a]],im):
                raise ValueError("image not enclosed")
            row.append((den,component_numerator(T,im)))
        info.append(tuple(row))
    pairs=tuple(product(range(n),repeat=2))
    B=tuple(tuple(tuple(tuple(v/info[i][a][0] for v in row)
                       for row in info[j][a][1])
                  for a in range(len(A))) for i,j in pairs)
    targets=tuple(tuple(edges[i][a]*n+edges[j][a] for a in range(len(A)))
                  for i,j in pairs)
    if local is None:
        result=graph_horizon(B,targets,max_horizon,weights)
        prefactor=F(1)
    else:
        rho,h=F(local[0]),tuple(map(F,local[1]))
        w=tuple(map(F,weights)) if weights is not None else (F(1),)*k
        if not 0<rho<1 or len(h)!=len(B) or min(h)<=0 or len(w)!=k or any(x<=0 for x in w):
            raise ValueError("invalid local potential")
        scalars=tuple(tuple(column_norm(A,w) for A in row) for row in B)
        if any(l*h[q]>rho*h[p] for p,(row,dest) in enumerate(zip(scalars,targets))
               for l,q in zip(row,dest)):
            raise ValueError("local potential inequality")
        prefactor=max(h)/min(h)
        result={"horizon":1,"eta":rho,"method":"local potential",
                "weights":w,"one_step_eta":max(max(row) for row in scalars),
                "rho":rho,"potential":h,"potential_ratio":prefactor}
    w=result["weights"]
    diameter=max(((max(box[j][1] for box in boxes)-min(box[j][0] for box in boxes))/w[j]
              for j in range(k)),default=F(0))
    diam=prefactor*diameter
    J=max(sum(w[i-1]*abs(T[i][0]) for i in range(1,k+1))
          for T in chart.matrices)
    return dict(result,block=block,contraction_length=block*result["horizon"],
                nonnull=c,cover_diameter=diameter,diameter=diam,
                log_variation_constant=J*diam/c,
                cells=n,pair_edges=n*n*len(A),primitive_words=len(A))


def discover(model,max_block=2,max_bits=10,max_depth=1,rounds=24,
             max_cells=32,max_horizon=12,modes=("weighted","reachable","hidden","raw")):
    """Bounded search; all acceptances replayable from basis, boxes, edges."""
    q=PredictiveQuotient(model)
    attempts=0;failures={}
    for block in range(1,max_block+1):
        for depth in range(1,max_depth+1):
            for mode in modes:
                chart=Chart(q,centered_basis(model,q,mode))
                for bits in range(2,max_bits+1):
                    attempts+=1
                    try:
                        boxes,edges,steps=adaptive_boxes(chart,block,bits,rounds,max_cells,depth)
                        data=verify_cover(chart,block,boxes,edges,max_horizon)
                    except ValueError as exc:
                        key=str(exc);failures[key]=failures.get(key,0)+1
                        continue
                    return dict(data,outcome="certified",mode=mode,basis=chart.basis,
                        boxes=boxes,edges=edges,bits=bits,depth=depth,widening_steps=steps,
                        attempts=attempts,failures=failures)
    return {"outcome":"undecided","attempts":attempts,"failures":failures}


def image_cover(chart,block,bits,max_cells,max_extent=64):
    """Adaptive topology: create a rounded local cell only for an uncovered image.

    Closure is checked edge by edge, never inferred from proximity. The
    finite budget may be exhausted even for a regular model.
    """
    if any(not isinstance(v,int) or v<1 for v in (block,bits,max_cells)):
        raise ValueError("bad adaptive image budget")
    if chart.alphabet**block>max_cells:
        raise ValueError("primitive block budget")
    A,seeds=block_system(chart,block)
    boxes=list(dict.fromkeys(hull((x,)) for x in seeds))
    if len(boxes)>max_cells:raise ValueError("cell budget")
    edges=[];h=F(1,2**bits)
    for box in boxes:
        row=[]
        for T in A:
            _,im=image_box(T,box)
            j=next((j for j,C in enumerate(boxes) if contains(C,im)),None)
            if j is None:
                if len(boxes)>=max_cells:raise ValueError("cell budget")
                C=padded(im,h)
                if any(max(abs(l),abs(u))>max_extent for l,u in C):
                    raise ValueError("cover extent budget")
                j=len(boxes);boxes.append(C)
            row.append(j)
        edges.append(tuple(row))
    return tuple(boxes),tuple(edges)


def discover_images(model,max_bits=12,max_cells=48,max_horizon=24,
                    modes=("weighted","hidden","reachable","raw"),min_bits=3):
    """Single-letter adaptive-topology fallback; no observation words enumerated."""
    q=PredictiveQuotient(model)
    attempts=0;failures={}
    for mode in modes:
        chart=Chart(q,centered_basis(model,q,mode))
        for bits in range(min_bits,max_bits+1):
            attempts+=1
            try:
                boxes,edges=image_cover(chart,1,bits,max_cells)
                data=verify_cover(chart,1,boxes,edges,max_horizon)
            except ValueError as exc:
                key=str(exc);failures[key]=failures.get(key,0)+1
                continue
            return dict(data,outcome="certified",mode=mode,basis=chart.basis,
                        boxes=boxes,edges=edges,bits=bits,attempts=attempts,
                        failures=failures)
    return {"outcome":"undecided","attempts":attempts,"failures":failures}


def uniform_margins(model,chart,certificate):
    """Extract rational WP11 constants from a verified graph certificate.

    Call with the output of verify_cover, not an unchecked supplied dictionary.
    """
    from effective_polytope_synthesis import observable_entry_bound
    L=certificate["contraction_length"];eta=certificate["eta"]
    c=certificate["nonnull"];C=certificate["log_variation_constant"]
    w=certificate["weights"];diam=certificate["diameter"]
    # Use small dyadic conservative bounds for the tail calculation.
    scale=256
    while ceil(scale*eta)>=scale:scale*=2
    eta_upper=max(F(1,scale),F(ceil(scale*eta),scale))
    scale=256
    while floor(scale*c)==0:scale*=2
    c_lower=F(floor(scale*c),scale)
    C_upper=F(0) if C==0 else F(1)
    if C:
        while C_upper<C:C_upper*=2
        while C_upper/2>=C:C_upper/=2
    n=0;tail=C_upper*L/(1-eta_upper)
    head=F(1);error=C_upper
    while tail>F(1,2):
        # Per-letter conditional ratio >= max(c_lower, 1-error).
        # Round the second bound downward to a modest fixed grid.
        head*=max(c_lower,F(floor(256*(1-error)),256))**L
        n+=1;tail*=eta_upper;error*=eta_upper
    b=head*(1-tail)
    J=observable_entry_bound(model,chart.quotient)
    # Conversion of the weighted chart norm back to predictive probabilities.
    d=chart.dimension
    G=max((sum(w[i-1]*abs(chart.basis[i][j]) for i in range(1,d))
           for j in range(1,d)),default=F(0))
    theta=rational_rate(eta,L)
    H=2*G*diam*J**2/theta**(L-1)
    return {"b":b,"J":J,"H":H,"theta":theta,"tail_blocks":n,
            "nonnull_lower":c_lower,"eta_upper":eta_upper}


def replay_witness(model,witness,use_local=True):
    """Recompute chart, enclosure, and either local inequalities or graph DP."""
    q=PredictiveQuotient(model)
    chart=Chart(q,witness["basis"])
    local=(witness["rho"],witness["potential"]) if use_local and "potential" in witness else None
    result=verify_cover(chart,witness["block"],witness["boxes"],witness["edges"],
                        witness["horizon"],witness["weights"],local=local)
    return result,uniform_margins(model,chart,result)
