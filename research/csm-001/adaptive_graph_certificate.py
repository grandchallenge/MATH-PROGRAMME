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
            V=corners(box)
            for a,T in enumerate(A):
                _,_,im=image(T,V);j=edges[i][a]
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
    return tuple(x/min(w) for x in w)


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
            return {"horizon":t,"eta":min(e1,e2),
                    "method":"scalar" if e1<=e2 else "component",
                    "weights":w,"one_step_eta":max(max(row) for row in scalars)}
    raise ValueError("graph horizon budget")


def verify_cover(chart,block,boxes,edges,max_horizon,weights=None):
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
    V=tuple(corners(box) for box in boxes)
    c=min(sum(x[i]*T[i][0] for i in range(k+1))
          for vs in V for x in vs for T in chart.matrices)
    if c<=0:raise ValueError("one-letter nonnullness")
    info=[]
    for i,vs in enumerate(V):
        row=[]
        for a,T in enumerate(A):
            den,Y,im=image(T,vs)
            if not contains(boxes[edges[i][a]],im):
                raise ValueError("image not enclosed")
            row.append((den,Y))
        info.append(tuple(row))
    pairs=tuple(product(range(n),repeat=2))
    B=tuple(tuple(component_bound(T,info[i][a][0],info[j][a][1])
                  for a,T in enumerate(A)) for i,j in pairs)
    targets=tuple(tuple(edges[i][a]*n+edges[j][a] for a in range(len(A)))
                  for i,j in pairs)
    result=graph_horizon(B,targets,max_horizon,weights)
    w=result["weights"]
    diam=max(((max(box[j][1] for box in boxes)-min(box[j][0] for box in boxes))/w[j]
              for j in range(k)),default=F(0))
    J=max(sum(w[i-1]*T[i][0].__abs__() for i in range(1,k+1))
          for T in chart.matrices)
    return dict(result,block=block,contraction_length=block*result["horizon"],
                nonnull=c,diameter=diam,log_variation_constant=J*diam/c,
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
