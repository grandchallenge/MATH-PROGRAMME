"""WP11: bounded, complete-on-positive-class predictive grid synthesis."""
from fractions import Fraction as F
from itertools import product
from math import floor

from observable_polytope_certificate import row_mul, project, secant_bound
from marked_reset_spectral import identity, multiply
from observable_memory_certificate import ObservableFiniteMemory


class BudgetExceeded(Exception):
    pass


class ForbiddenWord(Exception):
    def __init__(self,word):
        self.word=word
        super().__init__(str(word))


def extend_products(q, previous, max_products):
    """All distinct matrices M_w/p(w) at next length, with exact witnesses.

    Positive scalar normalization preserves maps and secant constants.
    Deduplication is exact and sound under subsequent concatenation.
    """
    out={}
    for A,w in previous.items():
        for a,B in enumerate(q.matrices):
            C=multiply(A,B)
            p=row_mul(q.initial,C)[0]
            if p<=0:raise ForbiddenWord(w+(a,))
            C=tuple(tuple(x/p for x in r) for r in C)
            if C not in out:
                if len(out)>=max_products:raise BudgetExceeded("product budget")
                out[C]=w+(a,)
    return out


def normalized_products(q,block,max_products):
    current={identity(q.dimension):()}
    for _ in range(block):
        current=extend_products(q,current,max_products)
    return current


def grid_center(x,radius):
    h=radius/2
    if x[0]!=1 or any(not 0<=t<=1 for t in x[1:]):
        raise ValueError("invalid actual predictive state")
    return (F(1),)+tuple(h*floor(t/h) for t in x[1:])


def grid_vertices(centers,radius,max_vertices):
    d=len(centers[0])
    if 2**(d-1)>max_vertices:raise BudgetExceeded("box vertex budget")
    vertices=set()
    for x in centers:
        for signs in product((-1,1),repeat=d-1):
            v=(F(1),)+tuple(t+radius*s for t,s in zip(x[1:],signs))
            vertices.add(v)
            if len(vertices)>max_vertices:raise BudgetExceeded("vertex budget")
    # In one free dimension the exact hull is just its endpoints.
    if d==2:return (min(vertices),max(vertices))
    return tuple(sorted(vertices))


def check_grid(q,products,radius,max_vertices):
    """Verify stronger WP10 witness: each block image is in its own box.

    Uses no convex membership solver; positive-denominator convexity proves
    invariance from the local box inclusions. Stationarity places the initial
    state in the hull of the exact length-block states, all inside these boxes.
    """
    radius=F(radius)
    if not 0<radius<=F(1,4):raise ValueError("radius outside (0,1/4]")
    if not products:raise ValueError("empty products")
    centers={A:grid_center(project(q.initial,A),radius) for A in products}
    V=grid_vertices(tuple(sorted(set(centers.values()))),radius,max_vertices)
    c=min(row_mul(v,A)[0] for v in V for A in q.matrices)
    if c<=0:raise ValueError("one-letter nonnullness")
    eta=F(0)
    slack=radius
    for A,center in centers.items():
        rate,images=secant_bound(A,V)
        if rate>=1:raise ValueError("block contraction")
        eta=max(eta,rate)
        distance=max((abs(y[j]-center[j]) for y in images
                      for j in range(1,q.dimension)),default=F(0))
        if distance>=radius:raise ValueError("strict local box inclusion")
        slack=min(slack,radius-distance)
    diameter=max(max(v[j] for v in V)-min(v[j] for v in V)
                 for j in range(q.dimension))
    J=max(sum(abs(A[i][0]) for i in range(1,q.dimension)) for A in q.matrices)
    return {"radius":radius,"vertices":V,"distinct_products":len(products),
            "grid_centers":len(set(centers.values())),
            "eta":eta,"nonnull":c,"slack":slack,"diameter":diameter,
            "log_variation_constant":J*diameter/c}


def validate_budgets(block,grid_bits,max_products,max_vertices):
    if any(not isinstance(v,int) or v<1 for v in
           (block,grid_bits,max_products,max_vertices)) or grid_bits<2:
        raise ValueError("invalid finite synthesis budget")


def synthesize(q,max_block=12,max_grid_bits=12,max_products=4096,max_vertices=4096):
    """Construct a finite witness or return an explicitly inconclusive result."""
    validate_budgets(max_block,max_grid_bits,max_products,max_vertices)
    current={identity(q.dimension):()}
    attempts=0;skipped=0
    for s in range(1,max_block+1):
        try:current=extend_products(q,current,max_products)
        except ForbiddenWord as exc:
            return {"outcome":"forbidden_word","word":exc.word,"attempts":attempts}
        except BudgetExceeded:
            return {"outcome":"undecided","boundary":"product_budget",
                    "checked_through":s-1,"attempts":attempts,"skipped":skipped}
        for j in range(2,max_grid_bits+1):
            attempts+=1
            try:data=check_grid(q,current,F(1,2**j),max_vertices)
            except BudgetExceeded:
                skipped+=1
                continue
            except ValueError:
                continue
            return dict(data,outcome="certified",block=s,grid_bits=j,
                        attempts=attempts,skipped=skipped)
    return {"outcome":"undecided","boundary":"search_budget",
            "checked_through":max_block,"attempts":attempts,"skipped":skipped}


def replay(q,block,grid_bits,max_products=4096,max_vertices=4096):
    """Reconstruct the witness from only two integers and the exact model."""
    validate_budgets(block,grid_bits,max_products,max_vertices)
    A=normalized_products(q,block,max_products)
    return dict(check_grid(q,A,F(1,2**grid_bits),max_vertices),
                block=block,grid_bits=grid_bits)


def quantitative_bounds(d,alphabet,b,J,H,theta):
    """Conditional worst-case resource bound given valid WP07 constants.

    J bounds every entry of M_w/p(w); H theta^|w| bounds every minor
    of M_w/p(w). b is the all-word quasi-Bernoulli lower bound.
    These inputs are hypotheses, NOT inferred from finite sample checks.
    """
    b,J,H,theta=map(F,(b,J,H,theta))
    if not isinstance(d,int) or d<1 or not isinstance(alphabet,int) or alphabet<1:
        raise ValueError("bad dimensions")
    if not 0<b<=1 or J<=0 or H<0 or not 0<theta<1:
        raise ValueError("bad quantitative hypotheses")
    k=d-1
    if k==0:return {"block":1,"grid_bits":2,"radius":F(1,4),
                   "vertex_bound":1,"word_bound":alphabet,"D":F(0)}
    j=2
    while F(1,2**j)>b/(8*k*J):j+=1
    delta=F(1,2**j)
    D=4*k*(1+2*k)*H/b**2
    s=1
    while D*theta**s>=delta/4:s+=1
    return {"block":s,"grid_bits":j,"radius":delta,"D":D,
            "word_bound":alphabet**s,
            "vertex_bound":min(2**k*alphabet**s,(2**(j+1)+5)**k)}


def slow_reset_model(N):
    """Positive-Hölder family requiring a growing block in the secant norm."""
    if not isinstance(N,int) or N<1:raise ValueError("positive N required")
    eps=F(1,1+2**N)
    A=((F(1,2),F(0)),(F(0),F(1,4)))
    B=((eps/4,(1-eps)/4),)*2
    C=((F(1,8),F(1,8)),(F(1,4),F(1,4)))
    pi=(2*(1+eps)/5,(3-2*eps)/5)
    return ObservableFiniteMemory(pi,(A,B,C))
