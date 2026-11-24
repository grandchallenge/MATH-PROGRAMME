"""Exact certificates for singular-gap obstruction and finite-range block lifts."""
from fractions import Fraction as F
from itertools import product
from observable_memory_certificate import ObservableFiniteMemory
from observable_exterior_square import word_matrix, exterior_norm, _check_cone
from polarized_exterior_channel import mixed_exterior
from marked_reset_spectral import norm_inf


def singular_gap_counterexample():
    return ObservableFiniteMemory((F(1,2),F(1,2)),
        (((F(1,2),0),(0,F(1,4))),
         ((0,0),(0,F(1,4))),
         ((F(1,4),F(1,4)),(F(1,4),F(1,4)))))


def finite_range_lift(model, memory, kernel):
    """Read H(z | previous r input letters, current letter).

    Hidden state (input history, current microscopic hidden state).
    Kernel rows follow lexicographic input words of length r+1.
    Independent randomization at each output site is assumed.
    Zero-stationary states are removed exactly.
    """
    if not isinstance(memory,int) or memory<0:
        raise ValueError("nonnegative memory required")
    m,d=model.alphabet,model.dimension
    words=tuple(product(range(m),repeat=memory+1))
    H=tuple(tuple(map(F,row)) for row in kernel)
    if len(H)!=len(words) or not H or not H[0]:
        raise ValueError("kernel shape mismatch")
    k=len(H[0])
    if any(len(row)!=k or any(x<0 for x in row) or sum(row)!=1 for row in H):
        raise ValueError("kernel rows must be stochastic")
    if any(sum(row[z] for row in H)==0 for z in range(k)):
        raise ValueError("remove unused output labels")
    lookup=dict(zip(words,H))
    states=[];pi=[]
    for hist in product(range(m),repeat=memory):
        row=model.pi
        for a in hist:row=model._left_step(row,a)
        for i,p in enumerate(row):
            if p>0:states.append((hist,i));pi.append(p)
    mats=[]
    for z in range(k):
        rows=[]
        for hist,i in states:
            line=[]
            for tail,j in states:
                mass=F(0)
                for a in range(m):
                    w=hist+(a,)
                    if w[1:]==tail:
                        mass+=model.matrices[a][i][j]*lookup[w][z]
                line.append(mass)
            rows.append(tuple(line))
        mats.append(tuple(rows))
    out=ObservableFiniteMemory(tuple(pi),tuple(mats))
    return out,tuple(states)


def block_mixed_certificate(model, anchor, L, R, block):
    """Finite uniform certificate; only complete blocks need preserve cones.

    Stationarity extends the two cone bounds to all word lengths.
    No single-letter positive pivot or invertibility is required.
    """
    d=model.dimension
    if not isinstance(anchor,int) or not 0<=anchor<d or not isinstance(block,int) or block<1:
        raise ValueError("bad anchor or block")
    L,R=tuple(map(F,L)),tuple(map(F,R))
    if len(L)!=d or len(R)!=d or L[anchor]!=1 or R[anchor]!=1 or any(x<0 for x in L+R):
        raise ValueError("bad anchor bounds")
    if any(model.pi[i]>L[i]*model.pi[anchor] or R[i]<1 for i in range(d)):
        raise ValueError("initial messages outside cones")
    mats=tuple(word_matrix(model,w) for w in product(range(model.alphabet),repeat=block))
    if any(A[anchor][anchor]<=0 for A in mats):
        raise ValueError("positive block pivots required")
    _check_cone(mats,L,anchor,True)
    _check_cone(mats,R,anchor,False)
    eta=max((norm_inf(mixed_exterior(A,B))/(A[anchor][anchor]*B[anchor][anchor])
             for A,B in product(mats,repeat=2)),default=F(0)) if d>1 else F(0)
    if eta>=1:raise ValueError("mixed block contraction not certified")
    b=1/(sum(L)*sum(p*r for p,r in zip(model.pi,R)))
    # Exact normalized residual bound; all short words positive by block support.
    residual=F(1)
    for n in range(1,block):
        for w in product(range(model.alphabet),repeat=n):
            p=model.word_probability(w)
            if p<=0:raise ValueError("short forbidden word")
            residual=max(residual,exterior_norm(word_matrix(model,w))/p**2)
    # If there is no remainder, the extra b^-2 is conservative.
    constant=residual/(model.pi[anchor]**2*b**4*min(model.pi))
    return {"block":block,"eta":eta,"b":b,"constant":constant,
            "nonnull":b*min(model.word_probability((a,)) for a in range(model.alphabet))}


def iid_binary(p):
    p=F(p)
    if not 0<p<1:raise ValueError("interior Bernoulli parameter required")
    return ObservableFiniteMemory((F(1),),(((1-p,),),((p,),)))


def rare_history_bounds(p,memory,alpha):
    """Universal sufficient inequalities for every binary iid block kernel
    whose constant-zero input gives each output probability >= alpha.
    """
    p,alpha=F(p),F(alpha)
    if not 0<p<1 or not 0<alpha<=1 or not isinstance(memory,int) or memory<1:
        raise ValueError("bad rare-history parameters")
    q=1-p
    mu=tuple(q**(memory-sum(h))*p**sum(h)
             for h in product((0,1),repeat=memory))
    e=(1-mu[0])/(mu[0]*alpha**memory)
    K=alpha**(-memory)
    eta=2*K*e+e**2
    if e>=F(1,2) or eta>=1:
        raise ValueError("universal rare-history bound insufficient")
    L=(F(1),)+tuple(2*x/(mu[0]*alpha**memory) for x in mu[1:])
    R=(F(1),)+(K/(1-e),)*(len(mu)-1)
    return {"L":L,"R":R,"eta_upper":eta,"escape":e,"anchor_ratio":K}


def parity_kernel(memory):
    """Noisy on the all-zero window, deterministic parity elsewhere."""
    return tuple((F(1,2),F(1,2)) if not any(w) else
                 (F(sum(w)%2==0),F(sum(w)%2==1))
                 for w in product((0,1),repeat=memory+1))


def universal_block_bounds(source,memory,reference,hidden_anchor,alpha,block=None):
    """A kernel-independent certificate for a whole class of overlapping maps.

    All output labels must have probability >=alpha at the constant
    reference input window. Uses only source transfers and the unlabelled
    history lift. Returns cone bounds, a rate upper bound and state ordering.
    """
    if not isinstance(memory,int) or memory<1:
        raise ValueError("positive history length required")
    if block is None:block=memory
    if not isinstance(block,int) or block<1:
        raise ValueError("positive block length required")
    alpha=F(alpha)
    if not 0<alpha<=1 or not isinstance(reference,int) or not 0<=reference<source.alphabet:
        raise ValueError("bad reference or alpha")
    if not isinstance(hidden_anchor,int) or not 0<=hidden_anchor<source.dimension:
        raise ValueError("bad microscopic anchor")
    # A one-output dummy channel yields exactly the unlabelled lift.
    lift,states=finite_range_lift(source,memory,((F(1),),)*(source.alphabet**(memory+1)))
    state=((reference,)*memory,hidden_anchor)
    if state not in states:raise ValueError("zero stationary anchor")
    h=states.index(state)
    c=word_matrix(source,(reference,)*block)[hidden_anchor][hidden_anchor]
    pivot=c*alpha**block
    if pivot<=0:raise ValueError("reference path has zero mass")
    Qs=word_matrix(lift,(0,)*block)
    bounds=tuple(max(row[j] for row in Qs)/pivot for j in range(lift.dimension))
    K=max(F(1),bounds[h])
    e=sum(bounds[j] for j in range(lift.dimension) if j!=h)
    eta=2*K*e+e**2
    if e>=F(1,2) or eta>=1:raise ValueError("universal path crowding insufficient")
    L=tuple(F(1) if j==h else 2*bounds[j] for j in range(lift.dimension))
    R=tuple(F(1) if j==h else K/(1-e) for j in range(lift.dimension))
    return {"anchor":h,"states":states,"L":L,"R":R,"block":block,
            "eta_upper":eta,"escape":e,"anchor_ratio":K,"pivot_lower":pivot}


def rare_non_iid_source():
    """Two-state non-iid source with a rare input and a rare hidden state."""
    d=F(1,1024)
    return ObservableFiniteMemory((1-d,d),
        (((1-2*d,d),(1-3*d,d)),((d,0),(2*d,0))))
