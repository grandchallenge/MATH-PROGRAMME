#!/usr/bin/env python3
"""Exact finite controls for the retained-record construction 087.

Rebuilds normalized counterterms for all proper sources of the fixed host.
Schur integration includes the marked Gaussian-convolved cusp and its
derivatives. No floats, dependencies, graph-label quotient or hosted compute.
The infinite asymptotic and record-coherence statements are proved in 087.
"""
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations_with_replacement, product
from math import comb, factorial
from pathlib import Path
import importlib.util

spec = importlib.util.spec_from_file_location(
    "schur086", Path(__file__).with_name("check_common_domain_schur_086.py"))
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
ar = base.ar
plus, neg, scale, mult = ar.plus, ar.negate, ar.scale, ar.mult
HOST = tuple(range(11))
PROPER = tuple(s for s in base.sources if s != HOST)
assert len(PROPER) == 277 and len(base.pairs) == 2


def invsqrt(q):
    """The old squarefree primitive accepts integers, not arbitrary rationals."""
    q = F(q)
    assert q > 0
    return scale(ar.rinv(q.numerator * q.denominator), q.denominator)


def dfact(n):
    out = 1
    for j in range(n, 0, -2):
        out *= j
    return out


assert invsqrt(F(3, 2)) == {6: F(1, 3)}


@lru_cache(None)
def cusp_derivative(n, variance):
    """Derivative at zero of sqrt(2*pi) P_s, with s^2=variance."""
    if n == 0:
        return scale(invsqrt(variance), variance)
    if n % 2:
        return {}
    k = n // 2
    return scale(invsqrt(variance),
                 F((-1) ** (k - 1) * dfact(2*k - 3)) * variance ** (1-k))


@lru_cache(None)
def marked_moment(exponents, covariance, tilt, variance, derivative):
    """Differentiate exp(z C z/2) sqrt(2*pi) P_s^(r)(tilt.z).

    This recurrence differentiates the Gaussian once or the marked factor
    once. The formal covariance in an insertion need not be positive.
    """
    if not any(exponents):
        return cusp_derivative(derivative, variance)
    i = next(j for j, n in enumerate(exponents) if n)
    left = list(exponents)
    left[i] -= 1
    answer = scale(marked_moment(tuple(left), covariance, tilt,
                                 variance, derivative + 1), tilt[i])
    for j, n in enumerate(left):
        if n and covariance[i][j]:
            rest = list(left)
            rest[j] -= 1
            answer = plus(answer, scale(marked_moment(tuple(rest), covariance,
                                  tilt, variance, derivative), n*covariance[i][j]))
    return answer


def vec_contraction(v, matrix, w):
    return sum((v[i]*matrix[i][j]*w[j]
                for i in range(len(v)) for j in range(len(w))), F(0))


@lru_cache(None)
def bare_marked_geometry(ids):
    backbone = tuple(e for e in ids if e != 10)
    coords, det, cov = base.lap(backbone)
    assert coords == base.lap(ids)[0]  # Removing a nonbridge preserves vertices.
    edge = tuple(F(int(v == 5) - int(v == 4)) for v in coords)
    tilt = tuple(sum((cov[i][j]*edge[j] for j in range(len(edge))), F(0))
                 for i in range(len(edge)))
    return det, tuple(tuple(row) for row in cov), tilt, 1+vec_contraction(edge, cov, edge)


@lru_cache(None)
def marked_complement_geometry(parent, beta):
    """Integrate the Gaussian quotient before differentiating the cusp jet."""
    pv, bv = base.verts(parent), base.verts(beta)
    pc, bc = pv[1:], bv[1:]
    pr, br = pv[0], bv[0]
    qc = [v for v in pv if v != pr and (v not in bv or v == br)]
    nu, nq = len(bc), len(qc)

    def coordinate(v):
        z = [F(0)]*(nu+nq)
        if v in bc:
            z[bc.index(v)] = 1
        if v in bv:
            if br in qc:
                z[nu+qc.index(br)] = 1
        elif v in qc:
            z[nu+qc.index(v)] = 1
        return z

    matrix = [[F(0)]*(nu+nq) for _ in range(nu+nq)]
    for e in parent:
        if e in beta or e == 10:
            continue
        a, b = base.edges[e]
        z = [x-y for x, y in zip(coordinate(b), coordinate(a))]
        for i in range(nu+nq):
            for j in range(nu+nq):
                matrix[i][j] += z[i]*z[j]
    A = [row[:nu] for row in matrix[:nu]]
    B = [row[nu:] for row in matrix[:nu]]
    det, Dinv = ar.inverse([row[nu:] for row in matrix[nu:]])
    assert det > 0
    U = [coordinate(v)[:nu] for v in pc]
    V = [coordinate(v)[nu:] for v in pc]
    C = [[F(0)]*(nu+len(pc)) for _ in range(nu+len(pc))]
    for i in range(nu):
        for j in range(nu):
            C[i][j] = -A[i][j]+vec_contraction(B[i], Dinv, B[j])
        for j in range(len(pc)):
            C[i][nu+j] = C[nu+j][i] = U[j][i]-vec_contraction(B[i], Dinv, V[j])
    for i in range(len(pc)):
        for j in range(len(pc)):
            C[nu+i][nu+j] = vec_contraction(V[i], Dinv, V[j])
    edge = [x-y for x, y in zip(coordinate(5), coordinate(4))]
    lu, lq = edge[:nu], edge[nu:]
    tilt = tuple(lu[i]-vec_contraction(lq, Dinv, B[i]) for i in range(nu)) + tuple(
        vec_contraction(lq, Dinv, V[j]) for j in range(len(pc)))
    return det, tuple(tuple(row) for row in C), nu, tilt, 1+vec_contraction(lq, Dinv, lq)


def edge_polynomial_terms(coords, degree):
    """Expand (x5-x4)^degree; a root vertex has coordinate zero."""
    terms = [((), F(1))]
    for _ in range(degree):
        next_terms = []
        for alpha, value in terms:
            for vertex, sign in ((5, 1), (4, -1)):
                if vertex in coords:
                    next_terms.append((alpha+(coords.index(vertex),), value*sign))
        terms = next_terms
    out = {}
    for alpha, value in terms:
        key = tuple(sorted(alpha))
        out[key] = out.get(key, F(0))+value
    return {a: c for a, c in out.items() if c}


@lru_cache(None)
def bare_moment(ids, alpha, derivative, polynomial):
    coords, det, cov = base.lap(ids)
    if derivative is None or 10 not in ids:
        exponents = tuple(alpha.count(i) for i in range(len(coords)))
        return scale(invsqrt(det), ar.wick(exponents, cov))
    det, C, tilt, variance = bare_marked_geometry(ids)
    value = {}
    for extra, coefficient in edge_polynomial_terms(coords, polynomial).items():
        exponents = tuple((alpha+extra).count(i) for i in range(len(coords)))
        value = plus(value, scale(marked_moment(exponents, C, tilt, variance,
                                               derivative), coefficient))
    return mult(invsqrt(det), value)


@lru_cache(None)
def insertion_moment(parent, beta, eta, alpha, derivative, polynomial):
    if derivative is None or 10 not in parent or 10 in beta:
        return base.integrated_jet(parent, beta, eta, alpha)
    coords = base.lap(parent)[0]
    det, C, nu, tilt, variance = marked_complement_geometry(parent, beta)
    denominator = 1
    for n in Counter(eta).values():
        denominator *= factorial(n)
    value = {}
    for extra, coefficient in edge_polynomial_terms(coords, polynomial).items():
        augmented = alpha+extra
        exponents = tuple(eta.count(i) for i in range(nu)) + tuple(
            augmented.count(i) for i in range(len(coords)))
        value = plus(value, scale(marked_moment(exponents, C, tilt, variance,
                                  derivative), coefficient/denominator))
    return mult(invsqrt(det), value)


class NormalizedForest:
    """Finite source normalization, not the canonical actual-family record.

    CT(target) is the raw whole-family coefficient. Individual auxiliary
    channel counterterms may still differ under a changed allocation.
    """
    def __init__(self, name, derivative=None, polynomial=0, allocation=None):
        self.name, self.derivative, self.polynomial = name, derivative, polynomial
        self.allocation = dict(allocation or {})
        self.counterterms = {}
        self.finite_sources = 0
        for ids in PROPER:
            h = self.degree(ids)
            parity = ((derivative+polynomial) % 2
                      if derivative is not None and 10 in ids else 0)
            ct = {}
            for degree in range(parity, h+1, 2):
                for alpha in combinations_with_replacement(range(len(base.lap(ids)[0])), degree):
                    prepared = self.prepared(ids, alpha)
                    value = (prepared if degree < h else
                             plus(prepared, neg(self.bare(ids, alpha))))
                    if value:
                        ct[alpha] = value
            self.counterterms[ids] = ct
            if h >= 0 and any(len(a) == h for a in ct):
                self.finite_sources += 1
        self.coefficients = sum(len(c) for c in self.counterterms.values())
        print('NORMALIZED087', name, '277 proper sources;', self.coefficients,
              'nonzero coefficients;', self.finite_sources, 'finite-normalized sources', flush=True)

    def degree(self, ids):
        value = base.rank(ids)-sum(self.allocation.get(e, 0) for e in ids)
        if self.derivative is not None and 10 in ids:
            value += self.derivative-self.polynomial-2
        return value

    def bare(self, ids, alpha):
        return bare_moment(ids, alpha, self.derivative, self.polynomial)

    def prepared(self, ids, alpha):
        value = self.bare(ids, alpha)
        for beta, ct in self.counterterms.items():
            if not set(beta) < set(ids):
                continue
            for eta, coefficient in ct.items():
                inserted = insertion_moment(ids, beta, eta, alpha,
                                             self.derivative, self.polynomial)
                value = plus(value, neg(mult(coefficient, inserted)))
        for a, b in base.pairs:
            if not (set(a) < set(ids) and set(b) < set(ids)):
                continue
            # Marked edge belongs to one triangle, so the complement is Gaussian.
            assert 10 in a or 10 in b
            ca, cb = self.counterterms[a].get((), {}), self.counterterms[b].get((), {})
            assert all(not eta for eta in self.counterterms[a])
            assert all(not eta for eta in self.counterterms[b])
            first = set(base.verts(a)) if 0 in base.verts(a) else set(base.verts(b))
            crossing = sum((base.edges[e][0] in first) != (base.edges[e][1] in first) for e in ids)
            if any(base.lap(ids)[0][i] in first for i in alpha):
                continue
            moment = ar.wick((len(alpha),), [[F(1, crossing)]])
            value = plus(value, mult(mult(ca, cb), scale(invsqrt(crossing), moment)))
        return value

    def directional(self, degree, finite_counterterm=False):
        value = {}
        for alpha, coefficient in edge_polynomial_terms(base.lap(HOST)[0], degree).items():
            prepared = self.prepared(HOST, alpha)
            if finite_counterterm:
                prepared = plus(prepared, neg(self.bare(HOST, alpha)))
            value = plus(value, scale(prepared, coefficient))
        return value

    def finite_output(self, degree):
        assert degree == self.degree(HOST)
        prepared = self.directional(degree)
        finite_ct = self.directional(degree, finite_counterterm=True)
        return plus(prepared, neg(finite_ct)), finite_ct


delta = NormalizedForest('delta')
assert delta.finite_sources > 0
out_delta, ct_delta = delta.finite_output(6)
assert out_delta == {3: F(5, 64)}
assert ct_delta
print('RESULT087 delta t6 output / (2pi)^-3:', out_delta, flush=True)
print('RESULT087 delta intrinsic finite host counterterm:', ct_delta, flush=True)

allocations = []
for edge in (0, 10):
    normalized = NormalizedForest('delta eps2@'+str(edge), allocation={edge: 2})
    result, correction = normalized.finite_output(4)
    assert result == {3: F(1, 32)}
    allocations.append(result)
    print('RESULT087 delta eps2 allocation', edge, 'output:', result,
          'finite host counterterm:', correction, flush=True)
assert allocations[0] == allocations[1]

wick = NormalizedForest('Wick P', derivative=0)
out_wick, ct_wick = wick.finite_output(4)
assert out_wick == {3: F(23, 48)}
print('RESULT087 Wick t4 output / (2pi)^-3:', out_wick, flush=True)
for edge in (0, 10):
    normalized = NormalizedForest('Wick eps2@'+str(edge), derivative=0, allocation={edge: 2})
    result, _ = normalized.finite_output(2)
    assert result == {3: F(1, 8)}

# P'' is kappa as an actual edge family. Check all proper counterterm tensors.
converted = NormalizedForest('Wick Psecond', derivative=2)
assert converted.counterterms == delta.counterterms
assert converted.finite_output(6)[0] == out_delta

ward_specs = [
    ('mixed t Pprime / eps2', 1, 1, -2, {3: F(177, 64)}),
    ('mixed t2 P / eps4', 0, 2, -4, {3: F(1451, 64)}),
    ('mixed P / eps2', 0, 0, -2, {3: F(91, 32)}),
]
ward = []
for name, order, polynomial, shift, expected in ward_specs:
    normalized = NormalizedForest(name, derivative=order, polynomial=polynomial,
                                  allocation={10: shift})
    result, _ = normalized.finite_output(6)
    assert result == expected
    ward.append(result)
rhs = plus(plus(out_delta, scale(ward[0], -2)), plus(ward[1], neg(ward[2])))
assert rhs == scale(out_wick, 30) == {3: F(115, 8)}

# Independently derive marked moments by one-dimensional Stein recurrences.
# I_n=E[T^n P_1(T)]sqrt(pi), J_n=E[T^n P_1'(T)]sqrt(pi).
I, J = {0: F(1)}, {0: F(0)}
for n in range(8):
    K = F(dfact(n-1), 2**(n//2+1)) if n % 2 == 0 else F(0)
    J[n+1] = n*J.get(n-1, F(0))+K
    I[n+1] = n*I.get(n-1, F(0))+J[n]
assert (I[2], I[4], I[6], I[8], J[7]) == (F(3,2), F(23,4), F(273,8), F(4353,16), F(531,16))
assert out_wick == scale({3: F(1, 12)}, I[4])
assert ward[0] == scale({3: F(1, 12)}, J[7])
assert ward[1] == scale({3: F(1, 12)}, I[8])
assert ward[2] == scale({3: F(1, 12)}, I[6])

# Full-record formal controls with actual one-dimensional Gaussian coefficients.
# Keys are (regulator degree, delta derivative order).
germ = {(2*k-1, 2*k): F(1, 2**k*factorial(k)) for k in range(9)}
def shifted(g, n): return {(p+n, d): c for (p,d), c in g.items()}
def derivative(g): return {(p,d+1): c for (p,d), c in g.items()}
def times_y(g): return {(p,d-1): -d*c for (p,d), c in g.items() if d}
left = shifted(derivative(germ), 2)
right = times_y(germ)
for key in set(left) | set(right):
    if key[0] <= 15:
        assert left.get(key, 0)+right.get(key, 0) == 0
def pp(g): return {key:c for key,c in g.items() if key[0] < 0}
assert pp(shifted(germ, 2)) != shifted(pp(germ), 2)
cross = {}
for (p,d), a in germ.items():
    for (q,e), b in germ.items():
        if p+q == 0: cross[d,e] = cross.get((d,e), F(0))+a*b
assert cross == {(0,2): F(1,2), (2,0): F(1,2)}
assert not any(p == 0 for p,d in germ)  # Individual finite outputs vanish.
for s in (F(1,2), F(1), F(3)):
    for t in (F(1,3), F(2)):
        assert {k:c*s**k[0]*t**k[0] for k,c in germ.items()} == {
            k:c*(s*t)**k[0] for k,c in germ.items()}

print('PASS087 all proper normalized sources and both disjoint spinneys', flush=True)
print('PASS087 actual Psecond=kappa on every proper counterterm tensor', flush=True)
print('PASS087 both old delta allocations and both marked Wick allocations', flush=True)
print('PASS087 full marked tangent identity with every mixed term', flush=True)
print('PASS087 independent Stein moment controls and nonzero finite values', flush=True)
print('PASS087 signed Gaussian derivative, regulator shift, disjoint cross-contact and dilation controls', flush=True)
print('LIMIT087 finite controls; 087 proves strong asymptotics and record coherence', flush=True)
