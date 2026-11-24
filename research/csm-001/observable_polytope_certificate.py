"""WP10: exact finite predictive-polytope contraction on the observable quotient."""
from fractions import Fraction as F
from itertools import combinations, product
from observable_memory_certificate import ObservableFiniteMemory, _rank, _dot
from marked_reset_spectral import identity, multiply
from finite_range_block_certificate import finite_range_lift


def solve_square(a,b):
    """Exact square system A x=b, reject singular."""
    n=len(a)
    rows=[list(map(F,r))+[F(t)] for r,t in zip(a,b)]
    if len(rows)!=n or any(len(r)!=n+1 for r in rows):
        raise ValueError("bad square system")
    for j in range(n):
        k=next((i for i in range(j,n) if rows[i][j]),None)
        if k is None:raise ValueError("singular system")
        rows[j],rows[k]=rows[k],rows[j]
        p=rows[j][j];rows[j]=[x/p for x in rows[j]]
        for i in range(n):
            if i!=j:
                p=rows[i][j]
                rows[i]=[x-p*y for x,y in zip(rows[i],rows[j])]
    return tuple(r[-1] for r in rows)


class PredictiveQuotient:
    """Coordinates x_j=p(uv_j)/p(u), v_0=empty; matrices may be signed."""
    def __init__(self,model):
        self.alphabet=model.alphabet
        p=model.word_probability
        us=tuple(w for w,_ in model.left_basis)
        vs=tuple(w for w,_ in model.right_basis)
        cols=[];probes=[]
        for v in vs:
            c=tuple(p(u+v) for u in us)
            if _rank(cols+[c])>len(cols):cols.append(c);probes.append(v)
        self.probes=tuple(probes)
        self.dimension=d=len(probes)
        assert probes[0]==() and d==model.minimal_linear_dimension
        rows=[];prefixes=[]
        for u in us:
            row=tuple(p(u+v) for v in probes)
            if _rank(rows+[row])>len(rows):rows.append(row);prefixes.append(u)
        H=tuple(rows)
        self.initial=tuple(p(v) for v in probes)
        mats=[]
        for a in range(self.alphabet):
            targets=tuple(tuple(p(u+(a,)+v) for v in probes) for u in prefixes)
            mats.append(tuple(zip(*(solve_square(H,col) for col in zip(*targets)))))
        self.matrices=tuple(mats)
        # Check quotient intertwining on all spanning rows, not just selected rows.
        for u in us:
            x=tuple(p(u+v) for v in probes)
            for a,A in enumerate(self.matrices):
                assert row_mul(x,A)==tuple(p(u+(a,)+v) for v in probes)
        assert self.initial[0]==1

    def word_matrix(self,w):
        A=identity(self.dimension)
        for a in w:
            if not isinstance(a,int) or not 0<=a<self.alphabet:
                raise ValueError("invalid symbol")
            A=multiply(A,self.matrices[a])
        return A

    def probability(self,w):
        return row_mul(self.initial,self.word_matrix(w))[0]

    def state(self,w):
        return project(self.initial,self.word_matrix(w))


def row_mul(x,A):
    return tuple(_dot(x,col) for col in zip(*A))


def project(x,A):
    y=row_mul(x,A)
    if y[0]<=0:raise ValueError("nonpositive projective denominator")
    return tuple(t/y[0] for t in y)


def in_hull(x,vertices):
    """Exact finite Caratheodory membership in affine plane x[0]=1."""
    d=len(x)
    # Any feasible nonnegative combination has an affinely independent support.
    for k in range(1,min(d,len(vertices))+1):
        for V in combinations(vertices,k):
            if _rank(V)!=k:continue
            for idx in combinations(range(d),k):
                A=tuple(tuple(v[i] for v in V) for i in idx)
                try:c=solve_square(A,tuple(x[i] for i in idx))
                except ValueError:continue
                if all(t>=0 for t in c) and all(
                    sum(t*v[j] for t,v in zip(c,V))==x[j] for j in range(d)):
                    return True
                break
    return False


def secant_bound(A,vertices):
    """Exact upper bound on l_infty projective Lipschitz constant."""
    d=len(A)
    den=min(row_mul(v,A)[0] for v in vertices)
    if den<=0:raise ValueError("nonpositive block denominator")
    images=tuple(project(v,A) for v in vertices)
    rate=max((sum(abs(A[i][j]-A[i][0]*y[j]) for i in range(1,d))
              for y in images for j in range(1,d)),default=F(0))/den
    return rate,images


def verify_polytope(quotient,vertices,block):
    """Finite exact proof of positive exponential conditional regularity.

    Full-dimensionality in x[0]=1 is required for the completeness theorem.
    Vertices may have negative coordinates; actual predictions remain probabilities.
    No spectral inference from finite samples. Rejection is not a negative decision.
    """
    d=quotient.dimension
    V=tuple(tuple(map(F,v)) for v in vertices)
    if not isinstance(block,int) or block<1:raise ValueError("bad block")
    if not V or any(len(v)!=d or v[0]!=1 for v in V) or _rank(V)!=d:
        raise ValueError("full affine dimension required")
    if not in_hull(quotient.initial,V):raise ValueError("stationary state outside polytope")
    c=min(row_mul(v,A)[0] for v in V for A in quotient.matrices)
    if c<=0:raise ValueError("one-letter nonnullness not certified")
    eta=F(0)
    for w in product(range(quotient.alphabet),repeat=block):
        A=quotient.word_matrix(w)
        rate,images=secant_bound(A,V)
        if any(not in_hull(y,V) for y in images):
            raise ValueError("block invariance not certified")
        eta=max(eta,rate)
    if eta>=1:raise ValueError("strict block contraction not certified")
    diameter=max(abs(v[j]-u[j]) for u,v in product(V,repeat=2) for j in range(d))
    likelihood=max(sum(abs(A[i][0]) for i in range(1,d)) for A in quotient.matrices)
    return {"block":block,"eta":eta,"nonnull":c,"diameter":diameter,
            "log_variation_constant":diameter*likelihood/c,
            "dimension":d,"vertices":V}


def balanced_source():
    """Balanced binary Markov source with observation-invisible coupled parity.

    State (observed bit, nuisance bit); nuisance flips only on 1->1.
    Both bits have uniform stationary distribution. Microscopic chain primitive.
    """
    states=tuple(product((0,1),repeat=2))
    T=tuple(tuple(tuple(
        (F(3,4) if a==b else F(1,4))
        if b==z and j==(i^(a==b==1)) else F(0)
        for b,j in states) for a,i in states) for z in (0,1))
    return ObservableFiniteMemory((F(1,4),)*4,T)


def coupled_kernel():
    """Output zero only on equal adjacent input bits; unequal likelihoods."""
    return ((F(3,4),F(1,4)),(F(0),F(1)),
            (F(0),F(1)),(F(1,4),F(3,4)))


def balanced_overlap():
    return finite_range_lift(balanced_source(),1,coupled_kernel())[0]


def balanced_vertices():
    return ((F(1),F(3,10)),(F(1),F(9,16)))
