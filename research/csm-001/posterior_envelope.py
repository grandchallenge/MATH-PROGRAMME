"""CSM-G2-WP05: rational posterior-diameter envelopes under structural zeros.

Finite exact identities and established Birkhoff/HMM reconstruction. No novel
Gibbs theorem claimed. Depends on WP04 observable-memory transfer semantics.
"""
from fractions import Fraction
from itertools import product

from observable_memory_certificate import ObservableFiniteMemory, _dot, _rank


class PosteriorEnvelope:
    def __init__(self, model):
        if not isinstance(model, ObservableFiniteMemory):
            raise TypeError("finite rational stationary transfer required")
        forbidden = model.full_support_obstruction()
        if forbidden is not None:
            raise ValueError("output not full-shift; forbidden word: " + repr(forbidden))
        self.model = model
        self.base_nonnulllower = min(x for _, dist in self.columns(())
                                      for x in dist)

    def _rows_after(self, prefix):
        model = self.model
        p = tuple(prefix)
        r = model.pi
        numerator_rows = [model._left_step(model.pi, a)
                          for a in range(model.alphabet)]
        for z in model._word(p):
            r = model._left_step(r, z)
            numerator_rows = [model._left_step(v, z)
                              for v in numerator_rows]
        return r, tuple(numerator_rows)

    def columns(self, prefix):
        """(terminal_state, posterior law of present output | word, state).

        Only terminal states reachable with positive probability occur.
        Conditional distributions remain exact rationals for every prefix.
        """
        model = self.model
        r, numerators = self._rows_after(prefix)
        columns = []
        for j, mass in enumerate(r):
            if mass == 0:
                assert all(v[j] == 0 for v in numerators)
                continue
            law = tuple(v[j] / mass for v in numerators)
            assert sum(law) == 1 and all(v >= 0 for v in law)
            columns.append((j, law))
        assert columns
        return tuple(columns)

    def diameter(self, prefix):
        """Exact total-variation diameter of terminal-state posteriors."""
        columns = self.columns(prefix)
        diameter = Fraction(0)
        witness = (columns[0][0], columns[0][0])
        for i, a in columns:
            for j, b in columns:
                tv = sum((abs(x-y) for x, y in zip(a, b)),
                         Fraction(0)) / 2
                if tv > diameter:
                    diameter, witness = tv, (i, j)
        return {"diameter": diameter, "states": witness,
                "prefix": tuple(prefix)}

    def uniform_diameter(self, k):
        if not isinstance(k, int) or k < 0:
            raise ValueError("nonnegative length required")
        worst = {"diameter": Fraction(0), "states": (0, 0), "prefix": ()}
        for u in product(range(self.model.alphabet), repeat=k):
            entry = self.diameter(u)
            if entry["diameter"] > worst["diameter"]:
                worst = entry
        return worst

    def conditional(self, symbol, future):
        model = self.model
        future = model._word(future)
        if not isinstance(symbol, int) or not 0 <= symbol < model.alphabet:
            raise ValueError("invalid present output")
        return (model.word_probability((symbol,) + future) /
                model.word_probability(future))


def positive_current_emission_model():
    """Positive 2-hidden-state emission with generic infinite output memory."""
    F = Fraction
    P = ((F(4,5), F(1,5)), (F(1,3), F(2,3)))
    pi = (F(5,8), F(3,8))
    emission_one = (F(1,4), F(3,4))
    T = tuple(
        tuple(tuple(P[s][t] * (emission_one[s] if z == 1 else 1-emission_one[s])
                    for t in (0,1)) for s in (0,1))
        for z in (0,1))
    return ObservableFiniteMemory(pi, T)


def permute_hidden_states(model, permutation):
    """Change hidden basis by a permutation; preserves every word probability."""
    n = model.dimension
    perm = tuple(permutation)
    if sorted(perm) != list(range(n)):
        raise ValueError("permutation must contain all hidden states once")
    pi = tuple(model.pi[perm[i]] for i in range(n))
    matrices = tuple(
        tuple(tuple(A[perm[i]][perm[j]] for j in range(n))
              for i in range(n)) for A in model.matrices
    )
    return ObservableFiniteMemory(pi, matrices)


def disjoint_phase_union(a, b, mixing_weight=Fraction(1,2)):
    """Stationary direct-sum presentation with no cross-sector transitions."""
    if a.alphabet != b.alphabet:
        raise ValueError("output alphabets disagree")
    F = Fraction
    weight = F(mixing_weight)
    if not 0 < weight < 1:
        raise ValueError("mixing weight must be strictly interior")
    n,m=a.dimension,b.dimension
    pi = tuple(weight*x for x in a.pi) + tuple((1-weight)*x for x in b.pi)
    matrices=[]
    for A,B in zip(a.matrices,b.matrices):
        rows=[]
        for i in range(n):
            rows.append(tuple(A[i]) + (F(0),)*m)
        for i in range(m):
            rows.append((F(0),)*n + tuple(B[i]))
        matrices.append(tuple(rows))
    return ObservableFiniteMemory(pi, tuple(matrices))


def observational_equivalence(a, b):
    """Finite, exact word-series equality from the full future-message span.

    If the two stationary output measures differ, return an actual finite
    word and its two unequal rational cylinder probabilities.
    """
    joint = disjoint_phase_union(a,b)
    difference = tuple(a.pi) + tuple(-x for x in b.pi)
    for word, message in joint.right_basis:
        if _dot(difference,message) != 0:
            return {"equivalent":False, "witness_word":word,
                    "a_probability":a.word_probability(word),
                    "b_probability":b.word_probability(word),
                    "basis_dimension":len(joint.right_basis)}
    return {"equivalent":True, "basis_dimension":len(joint.right_basis),
            "checked_tail_cutoff":joint.dimension-1}


def positive_sector_rate(model):
    """Exact rational conservative projective contraction constants.

    This requires STRICTLY positive sector matrices; it is only a route
    to a proved all-k posterior-envelope bound for a structurally zero
    disjoint presentation with observationally equivalent sectors.
    """
    T=model.matrices
    d=model.dimension
    if any(x<=0 for A in T for row in A for x in row):
        raise ValueError("sector transfer matrices must be strictly positive")
    C=max(A[i][j]*A[k][l]/(A[i][l]*A[k][j])
          for A in T for i in range(d) for k in range(d)
          for j in range(d) for l in range(d))
    rate=(C-1)/(C+1)
    e=PosteriorEnvelope(model)
    cols=[law for _,law in e.columns(())]
    R0=max(cols[i][a]/cols[j][a]
           for i in range(d) for j in range(d)
           for a in range(model.alphabet))
    coefficient=Fraction(model.alphabet,2)*(R0-1)
    return {"cross_ratio":C, "rational_contraction":rate,
            "initial_ratio":R0, "tv_prefactor":coefficient,
            "uniform_nonnulllower":e.base_nonnulllower}


def sector_posterior_tv_bound(data, k):
    if not isinstance(k, int) or k<0:
        raise ValueError("nonnegative prefix length required")
    return data["tv_prefactor"]*data["rational_contraction"]**k
