"""GCL CSM-G2: exact positive-transfer certificate for two overlapping layers.

The mathematical result is a positive-matrix/Birkhoff reconstruction, not
a new Gibbs preservation theorem. Finite rational witnesses only.
"""
from fractions import Fraction


def _r(value):
    v = Fraction(value)
    if v < 0:
        raise ValueError("negative probability or weight")
    return v


def _matrix(rows):
    a = tuple(tuple(_r(x) for x in row) for row in rows)
    if not a or not a[0] or any(len(row) != len(a[0]) for row in a):
        raise ValueError("nonempty rectangular matrix required")
    return a


def _dot(u, v):
    return sum((x * y for x, y in zip(u, v)), Fraction(0))


def _apply(a, v):
    return tuple(_dot(row, v) for row in a)


class PositiveTransferCertificate:
    """A family of positive observation-labelled matrices summing to P.

    T_z has row indexed by present hidden state, column by next hidden state.
    pi is a stationary probability row for P=sum_z T_z.
    """

    def __init__(self, pi, matrices):
        self.transfer = tuple(_matrix(a) for a in matrices)
        if not self.transfer:
            raise ValueError("at least one observed symbol required")
        n = len(self.transfer[0])
        if any(len(a) != n or len(a[0]) != n for a in self.transfer):
            raise ValueError("all transfer matrices must be same square dimension")
        if any(v <= 0 for a in self.transfer for row in a for v in row):
            raise ValueError("strictly positive transfer matrices required")
        self.pi = tuple(_r(x) for x in pi)
        if len(self.pi) != n or any(x <= 0 for x in self.pi) or sum(self.pi) != 1:
            raise ValueError("pi must be a positive probability vector")
        self.transition = tuple(
            tuple(sum(a[i][j] for a in self.transfer) for j in range(n))
            for i in range(n)
        )
        if any(sum(row) != 1 for row in self.transition):
            raise ValueError("sum of transfer matrices must be row stochastic")
        if any(_dot(self.pi, tuple(self.transition[i][j] for i in range(n)))
               != self.pi[j] for j in range(n)):
            raise ValueError("pi must be stationary for summed transition")
        self.n = n
        self.alphabet_size = len(self.transfer)
        self.projective_cross_ratio = max(
            a[i][k] * a[j][l] / (a[i][l] * a[j][k])
            for a in self.transfer
            for i in range(n) for j in range(n)
            for k in range(n) for l in range(n)
        )
        c = self.projective_cross_ratio
        self.kappa = (c - 1) / (c + 1)
        self.lower_bounds = tuple(
            min(sum(self.pi[i] * a[i][j] for i in range(n)) / self.pi[j]
                for j in range(n)) for a in self.transfer
        )
        assert all(b > 0 for b in self.lower_bounds)

    def _check_word(self, word):
        seq = tuple(word)
        if any(not isinstance(z, int) or z not in range(self.alphabet_size)
               for z in seq):
            raise ValueError("observed symbol outside alphabet")
        return seq

    def future_message(self, future):
        b = (Fraction(1),) * self.n
        for z in reversed(self._check_word(future)):
            b = _apply(self.transfer[z], b)
        return b

    def word_probability(self, observed):
        return _dot(self.pi, self.future_message(observed))

    def conditional_before_future(self, future):
        b = self.future_message(future)
        normalizer = _dot(self.pi, b)
        q = tuple(_dot(self.pi, _apply(a, b)) / normalizer
                  for a in self.transfer)
        assert sum(q) == 1 and all(x >= lb for x, lb in zip(q, self.lower_bounds))
        return q


class TwoLayerOverlappingCertificate(PositiveTransferCertificate):
    """S_i,S_(i+1)->Y_i, then Y_i,Y_(i+1)->Z_i.

    P[s][t] strict positive transition, K[s][t][y] strict positive channel,
    H[y][w][z] strict positive channel; all rows stochastic.
    """

    def __init__(self, P, pi, K, H):
        p = _matrix(P)
        n = len(p)
        if len(p[0]) != n or any(sum(row) != 1 for row in p) or any(
                v <= 0 for row in p for v in row):
            raise ValueError("hidden transition must be strictly positive stochastic")
        stationary = tuple(_r(v) for v in pi)
        if len(stationary) != n or any(x <= 0 for x in stationary) or sum(stationary) != 1:
            raise ValueError("hidden pi must be positive and normalized")
        if any(sum(stationary[i] * p[i][j] for i in range(n)) != stationary[j]
               for j in range(n)):
            raise ValueError("hidden pi must be stationary")
        if len(K) != n or any(len(row) != n for row in K):
            raise ValueError("first-layer hidden pair shape mismatch")
        first = tuple(tuple(tuple(_r(v) for v in outcomes) for outcomes in row)
                      for row in K)
        if not first[0][0]:
            raise ValueError("empty first-layer alphabet")
        m = len(first[0][0])
        if any(len(a) != m or sum(a) != 1 or any(v <= 0 for v in a)
               for row in first for a in row):
            raise ValueError("first-layer channel must be strict positive stochastic")
        if len(H) != m or any(len(row) != m for row in H):
            raise ValueError("second-layer pair shape mismatch")
        second = tuple(tuple(tuple(_r(v) for v in outcomes) for outcomes in row)
                       for row in H)
        if not second[0][0]:
            raise ValueError("empty final alphabet")
        zsize = len(second[0][0])
        if any(len(a) != zsize or sum(a) != 1 or any(v <= 0 for v in a)
               for row in second for a in row):
            raise ValueError("second-layer channel must be strict positive stochastic")
        states = tuple((s, y) for s in range(n) for y in range(m))
        lam = tuple(sum(stationary[u] * p[u][s] * first[u][s][y]
                        for u in range(n)) for s, y in states)
        lifted = tuple(tuple(p[s][t] * first[s][t][w]
                             for t, w in states) for s, y in states)
        matrices = tuple(
            tuple(tuple(lifted[i][j] * second[states[i][1]][states[j][1]][z]
                        for j in range(len(states))) for i in range(len(states)))
            for z in range(zsize))
        super().__init__(lam, matrices)
        self.original_transition = p
        self.original_stationary = stationary
        self.first_channel = first
        self.second_channel = second
        self.lifted_states = states
        self.lifted_transition = lifted


def noisy_xor_certificate(p, epsilon):
    """Transfer certificate for iid Bernoulli-p, XOR edge, BSC(epsilon).

    A positive transfer exists for 0<epsilon<1. At endpoint noise 0 or 1,
    this routine must reject rather than incorrectly certify continuity.
    """
    p, epsilon = Fraction(p), Fraction(epsilon)
    if not 0 < p < 1 or not 0 < epsilon < 1:
        raise ValueError("strictly positive source and noise required")
    pi = (1 - p, p)
    t = tuple(
        tuple(tuple(
            pi[j] * ((1 - epsilon) if ((i ^ j) == z) else epsilon)
            for j in (0, 1)) for i in (0, 1)) for z in (0, 1)
    )
    return PositiveTransferCertificate(pi, t)
