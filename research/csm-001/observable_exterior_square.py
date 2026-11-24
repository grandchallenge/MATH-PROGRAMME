"""WP07: exact anchored exterior-square certificates for non-reset transfers."""
from fractions import Fraction as F
from itertools import combinations, product

from observable_memory_certificate import ObservableFiniteMemory
from marked_reset_spectral import identity, multiply, norm_inf


def word_matrix(model, word):
    result = identity(model.dimension)
    for z in model._word(word):
        result = multiply(result, model.matrices[z])
    return result


def exterior_square(a):
    pairs = tuple(combinations(range(len(a)), 2))
    return tuple(tuple(a[i][k]*a[j][l]-a[i][l]*a[j][k]
                       for k,l in pairs) for i,j in pairs)


def exterior_norm(a):
    e = exterior_square(a)
    return norm_inf(e) if e else F(0)


def conditional_defect(model, left, word, right):
    """Signed, exact relative conditional-independence error."""
    u,w,v = tuple(left),tuple(word),tuple(right)
    p=model.word_probability
    return p(u+w+v)*p(w)/(p(u+w)*p(w+v))-1


def normalized_basis_defect(model, word):
    """Max anchored minors over normalized actual-word left/right bases."""
    p=model.word_probability
    w=tuple(word)
    result=F(0)
    for u,_ in model.left_basis:
        for v,_ in model.right_basis:
            defect=(p(u+w+v)*p(w)-p(u+w)*p(w+v))
            result=max(result,abs(defect)/(p(u)*p(v)*p(w)**2))
    return result


def _check_cone(matrices, bounds, anchor, row):
    """Check all box vertices of x_h=1, 0<=x_i<=bounds_i."""
    d=len(bounds)
    other=tuple(i for i in range(d) if i!=anchor)
    for bits in product((0,1),repeat=len(other)):
        x=[F(0)]*d
        x[anchor]=F(1)
        for i,b in zip(other,bits):
            x[i]=bounds[i]*b
        for a in matrices:
            y=tuple(sum(x[i]*a[i][j] if row else a[j][i]*x[i]
                        for i in range(d)) for j in range(d))
            if y[anchor]<=0 or any(y[i]>bounds[i]*y[anchor] for i in other):
                raise ValueError("anchor cone not invariant")


def anchored_certificate(model, anchor, left_bounds, right_bounds, block=1):
    """Verify finite conditions for an all-word exponential defect bound.

    Exact arithmetic. Failure does NOT imply non-Gibbsianness.
    """
    d=model.dimension
    if not isinstance(anchor,int) or not 0<=anchor<d:
        raise ValueError("bad anchor")
    if not isinstance(block,int) or block<1:
        raise ValueError("bad block length")
    L,R=tuple(map(F,left_bounds)),tuple(map(F,right_bounds))
    if len(L)!=d or len(R)!=d or L[anchor]!=1 or R[anchor]!=1:
        raise ValueError("bad anchored bounds")
    if any(x<0 for x in L+R):
        raise ValueError("negative bounds")
    pi=model.pi
    if any(pi[i]>L[i]*pi[anchor] or R[i]<1 for i in range(d)):
        raise ValueError("initial row or column outside invariant cone")
    if any(a[anchor][anchor]<=0 for a in model.matrices):
        raise ValueError("positive common pivot required")
    _check_cone(model.matrices,L,anchor,True)
    _check_cone(model.matrices,R,anchor,False)
    b=1/(sum(L)*sum(pi[i]*R[i] for i in range(d)))
    # Use the actual block pivot, not a product of one-letter pivots.
    def ratio(w):
        a=word_matrix(model,w)
        return exterior_norm(a)/a[anchor][anchor]**2
    eta=max(ratio(w) for w in product(range(model.alphabet),repeat=block))
    if eta>=1:
        raise ValueError("exterior-square block contraction not certified")
    remainder=max([F(1)]+[ratio(w) for n in range(1,block)
                           for w in product(range(model.alphabet),repeat=n)])
    C=remainder/(min(pi)*b*b*pi[anchor]**2)
    return {"block":block,"eta":eta,"remainder":remainder,
            "quasi_bernoulli_lower":b,"constant":C,
            "nonnull":b*min(model.word_probability((a,)) for a in range(model.alphabet))}


def defect_bound(data, n):
    if not isinstance(n,int) or n<0:
        raise ValueError("bad separator length")
    return data["constant"]*data["eta"]**(n//data["block"])


def nonreset_model():
    """All three transfers invertible, none strictly positive, Q positive."""
    T=(((F(1,2),0),(0,F(1,8))),
       ((F(1,4),F(1,16)),(0,F(1,8))),
       ((F(3,16),0),(F(5,8),F(1,8))))
    return ObservableFiniteMemory((F(10,11),F(1,11)),T)


def tensor(a,b):
    return tuple(tuple(x*y for x in ar for y in br)
                 for ar in a for br in b)


def staggered_composition(model):
    """Independent edge-channel copies; Y_i=(A_i,B_i);
    Z_i=(A_i,A_i+B_(i+1) mod m), an overlapping pair readout.
    Stationarity and independence give the exact output transfer below.
    """
    m=model.alphabet
    transfers=tuple(tensor(model.matrices[a],model.matrices[(c-a)%m])
                    for a in range(m) for c in range(m))
    pi=tuple(x*y for x in model.pi for y in model.pi)
    return ObservableFiniteMemory(pi,transfers)


def product_defect_bound(base_bound):
    """If each factor has relative error <=e, product error <=2e+e^2."""
    e=F(base_bound)
    if e<0:
        raise ValueError("negative bound")
    return 2*e+e*e


def persistent_nonreset_model():
    """Primitive hidden Q, invertible transfers, uniform nonnull, bad zeros."""
    T=(((F(5,8),0),(0,F(5,8))),
       ((F(3,16),F(1,16)),(F(1,32),F(3,32))),
       ((F(3,32),F(1,32)),(F(1,16),F(3,16))))
    return ObservableFiniteMemory((F(1,2),F(1,2)),T)
