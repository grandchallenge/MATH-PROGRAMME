"""WP08: channel-closed polarized exterior-square certificate (exact rationals)."""
from fractions import Fraction as F
from itertools import combinations, product
from observable_memory_certificate import ObservableFiniteMemory
from observable_exterior_square import anchored_certificate, tensor
from marked_reset_spectral import norm_inf


def mixed_exterior(a,b):
    """Symmetric polarization of the quadratic map A -> wedge^2 A."""
    pairs=tuple(combinations(range(len(a)),2))
    return tuple(tuple((a[i][k]*b[j][l]+b[i][k]*a[j][l]
                        -a[i][l]*b[j][k]-b[i][l]*a[j][k])/2
                       for k,l in pairs) for i,j in pairs)


def channel_closed_certificate(model,anchor,L,R):
    """Finite witness for every subsequent sitewise stochastic output channel.

    All outputs must have nonempty incoming support. A failed witness is not
    a negative Gibbs decision. The nonnull field from the input certificate
    refers to the original alphabet; subsequent alphabets need new p(a).
    """
    data=anchored_certificate(model,anchor,L,R)
    eta=F(0)
    for a,b in product(model.matrices,repeat=2):
        e=mixed_exterior(a,b)
        if e:
            eta=max(eta,norm_inf(e)/(a[anchor][anchor]*b[anchor][anchor]))
    if eta>=1:
        raise ValueError("mixed exterior-square contraction not certified")
    return dict(data,eta=eta,channel_closed=True)


def postprocess(model,channel):
    """Independent sitewise stochastic output channel (source rows)."""
    H=tuple(tuple(map(F,row)) for row in channel)
    if len(H)!=model.alphabet or not H or not H[0]:
        raise ValueError("channel source shape mismatch")
    m=len(H[0])
    if any(len(row)!=m or any(x<0 for x in row) or sum(row)!=1 for row in H):
        raise ValueError("channel rows must be stochastic")
    if any(sum(row[z] for row in H)==0 for z in range(m)):
        raise ValueError("unused output label must be removed")
    d=model.dimension
    mats=tuple(tuple(tuple(sum(H[a][z]*model.matrices[a][i][j]
                               for a in range(model.alphabet))
                           for j in range(d)) for i in range(d)) for z in range(m))
    return ObservableFiniteMemory(model.pi,mats)


def strong_base():
    d=F(1,1024)
    T=(((F(1,2),0),(0,d)),
       ((F(1,4),d),(0,d)),
       ((F(1,4)-d,0),(1-3*d,d)))
    return ObservableFiniteMemory(((1-3*d)/(1-2*d),d/(1-2*d)),T)


def staggered_raw():
    """Y_i=(A_i,B_i), raw Z_i=(A_i,B_(i+1)), independent stationary tracks."""
    base=strong_base()
    return ObservableFiniteMemory(tuple(x*y for x in base.pi for y in base.pi),
                                  tuple(tensor(a,b) for a,b in
                                        product(base.matrices,repeat=2)))


def coupled_channel(epsilon=F(1,4096)):
    """Randomly exchange pair labels (1,1) and (2,2), leave the rest intact."""
    e=F(epsilon)
    if not 0<=e<=1:
        raise ValueError("invalid swap probability")
    H=[[F(i==j) for j in range(9)] for i in range(9)]
    for i,j in ((4,8),(8,4)):
        H[i][i]=1-e
        H[i][j]=e
    return tuple(tuple(row) for row in H)


def coupled_model(epsilon=F(1,4096)):
    return postprocess(staggered_raw(),coupled_channel(epsilon))
