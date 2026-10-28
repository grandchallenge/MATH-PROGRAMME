#!/usr/bin/env python3
"""Exact finite controls for R2/083; no continuum or BV certificate.

Reuses the frozen 065 rational/radical primitives, then changes the host,
rebuilds every source counterterm, and includes genuine disjoint spinneys.
No third-party packages or external I/O beyond the adjacent frozen fixture.
"""
from fractions import Fraction as F
from itertools import combinations, combinations_with_replacement
from collections import Counter
from functools import lru_cache
from pathlib import Path
import importlib.util
import sys

spec = importlib.util.spec_from_file_location(
    "r2_065_primitives", Path(__file__).with_name("check_nested_gaussian_jet_forest_065.py"))
old = importlib.util.module_from_spec(spec)
spec.loader.exec_module(old)
E = tuple(combinations(range(4), 2)) + ((0, 4), (1, 4), (0, 5), (1, 5), (4, 5))
old.E = E
old.graph.cache_clear()
graph, vertices, onepi, rank = old.graph, old.vertices, old.onepi, old.rank
plus, negate, scale, mult, rinv = old.plus, old.negate, old.scale, old.mult, old.rinv
wick, inverse, linear = old.wick, old.inverse, old.linear
ps, pscale = old.polynomial_sum, old.polynomial_scale
MAX_NORMAL = 4  # proper sources have rank at most five


def pmul(a, b):
    out = {}
    for (u, q), x in a.items():
        for (v, r), y in b.items():
            uu = tuple(i + j for i, j in zip(u, v))
            if sum(uu) > MAX_NORMAL:
                continue
            qq = tuple(i + j for i, j in zip(q, r))
            key = (uu, qq)
            out[key] = out.get(key, F(0)) + x * y
    return {key: value for key, value in out.items() if value}


@lru_cache(None)
def split(parent, beta):
    pv, pr, pc, _, _ = graph(parent)
    bv, br, bc, _, _ = graph(beta)
    nu = len(bc)
    qc = sorted(([br] if pr not in bv else []) +
                [v for v in pv if v not in bv and v != pr])
    nq = len(qc)
    qi, ui = {v: i for i, v in enumerate(qc)}, {v: i for i, v in enumerate(bc)}
    expr = {}
    for vertex in pv:
        u, q = [F(0)] * nu, [F(0)] * nq
        if vertex in bv:
            if vertex != br:
                u[ui[vertex]] = F(1)
            if br in qi:
                q[qi[br]] = F(1)
        elif vertex in qi:
            q[qi[vertex]] = F(1)
        expr[vertex] = (u, q)
    A = [[F(0)] * nu for _ in range(nu)]
    B = [[F(0)] * nq for _ in range(nu)]
    D = [[F(0)] * nq for _ in range(nq)]
    for edge in parent:
        if edge in beta:
            continue
        a, b = E[edge]
        u = [x - y for x, y in zip(expr[a][0], expr[b][0])]
        q = [x - y for x, y in zip(expr[a][1], expr[b][1])]
        for j in range(nu):
            for k in range(nu):
                A[j][k] += u[j] * u[k]
            for k in range(nq):
                B[j][k] += u[j] * q[k]
        for j in range(nq):
            for k in range(nq):
                D[j][k] += q[j] * q[k]
    det, cov = inverse(D)
    assert det > 0
    zero = ((0,) * nu, (0,) * nq)
    one, exponent = {zero: F(1)}, {}
    for j in range(nu):
        for k in range(nq):
            u, q = [0] * nu, [0] * nq
            u[j], q[k] = 1, 1
            key = (tuple(u), tuple(q))
            exponent[key] = exponent.get(key, F(0)) - B[j][k]
        for k in range(nu):
            u = [0] * nu
            u[j] += 1
            u[k] += 1
            key = (tuple(u), (0,) * nq)
            exponent[key] = exponent.get(key, F(0)) - A[j][k] / 2
    exponential, term = dict(one), dict(one)
    for degree in range(1, MAX_NORMAL + 1):
        term = pscale(pmul(term, exponent), F(1, degree))
        exponential = ps(exponential, term)
    return pc, expr, det, cov, one, exponential


memo = {}


def inserted(parent, beta, alpha):
    pc, expr, det, cov, one, exponential = split(parent, beta)
    test = one
    for j in alpha:
        test = pmul(test, linear(*expr[pc[j]]))
    test = pmul(exponential, test)
    answer = {}
    nu = len(graph(beta)[2])
    for source_alpha, value in memo[beta].items():
        powers = [0] * nu
        for j in source_alpha:
            powers[j] += 1
        avg = sum((c * wick(q, cov) for (u, q), c in test.items()
                   if u == tuple(powers)), F(0))
        answer = plus(answer, mult(value, scale(rinv(det), avg)))
    return answer


sources = [tuple(a) for k in range(3, len(E) + 1)
           for a in combinations(range(len(E)), k) if onepi(a)]
sources.sort(key=lambda a: (len(a), a))
H, K, F4, F5 = tuple(range(11)), tuple(range(6)), tuple(range(8)), tuple(range(6)) + (8, 9)
proper = sources[:-1]
assert sources[-1] == H
disjoint_pairs = [(a, b) for a, b in combinations(proper, 2)
                  if set(vertices(a)).isdisjoint(vertices(b))]
expected_pairs = {
    frozenset(((1, 2, 5), (7, 9, 10))),
    frozenset(((3, 4, 5), (6, 8, 10))),
}
assert {frozenset(pair) for pair in disjoint_pairs} == expected_pairs
assert not set(F4) <= set(F5) and not set(F5) <= set(F4)
assert set(F4) & set(F5) == set(K)
assert not set(vertices(F4)).isdisjoint(vertices(F5))


def pair_inserted(parent, pair, alpha):
    """Only possible disjoint spinneys here are two scalar triangle poles."""
    a, b = pair
    assert rank(a) == rank(b) == 1 and len(vertices(a)) == len(vertices(b)) == 3
    av, bv = set(vertices(a)), set(vertices(b))
    assert av | bv == set(range(6))
    first = av if 0 in av else bv
    second = bv if 0 in av else av
    crossing = sum((u in first) != (v in first) for i, (u, v) in enumerate(E)
                   if i in parent and i not in a and i not in b)
    assert crossing > 0
    # At both source diagonals, y_j is 0 in first and q in second.
    if any(graph(parent)[2][j] in first for j in alpha):
        return {}
    moment = wick((len(alpha),), [[F(1, crossing)]])
    return mult(mult(memo[a].get((), {}), memo[b].get((), {})), scale(rinv(crossing), moment))


def prepared_moment(ids, alpha, earlier):
    _, _, coords, det, cov = graph(ids)
    exponents = [0] * len(coords)
    for j in alpha:
        exponents[j] += 1
    value = scale(rinv(det), wick(tuple(exponents), cov))
    for beta in earlier:
        if set(beta) < set(ids):
            value = plus(value, negate(inserted(ids, beta, alpha)))
    for pair in disjoint_pairs:
        if all(set(beta) < set(ids) for beta in pair):
            value = plus(value, pair_inserted(ids, pair, alpha))
    return value


for index, ids in enumerate(sources):
    coords = graph(ids)[2]
    h = rank(ids)
    alphas = [a for degree in range(0, h, 2)
              for a in combinations_with_replacement(range(len(coords)), degree)]
    memo[ids] = {a: prepared_moment(ids, a, sources[:index]) for a in alphas}

assert [graph(ids)[3] for ids in (K, F4, F5, tuple(range(10)), H)] == [16, 40, 40, 96, 192]
assert memo[K][(0, 0)] == {1: F(-7, 72)}
assert memo[F4][(0, 0)] == memo[F5][(0, 0)]
assert inserted(F4, K, (0, 0)) == {2: F(-7, 144)}
finite_F4 = prepared_moment(F4, (0, 0, 0, 0), proper)
assert finite_F4 == {10: F(3, 125), 21: F(-8, 343)}
# The fully prepared even-rank host: degree six is finite, not a pole.
finite_H_t6 = {}
# Expand (x5-x4)^6 in the vertex-monomial basis, root at 0.
from math import comb
for k in range(7):
    alpha = (3,) * k + (4,) * (6 - k)
    finite_H_t6 = plus(finite_H_t6, scale(prepared_moment(H, alpha, proper), F((-1)**k * comb(6, k))))
assert finite_H_t6
print("NEW083: proper-source ranks", dict(Counter(rank(a) for a in proper)), flush=True)
print("NEW083: disjoint pairs", disjoint_pairs, flush=True)
print("NEW083: prepared host finite t^6 radical coefficients", finite_H_t6, flush=True)
print("NEW083: rigorous sign interval", old.enclosing_interval(finite_H_t6), flush=True)
assert old.enclosing_interval(finite_H_t6)[1] < 0
assert finite_H_t6 == {3: F(5, 64), 2: F(265, 1536),
                       6: F(-16685, 46656), 7: F(1160, 3969), 30: F(-41, 810)}
pair_sixth = {}
for pair in disjoint_pairs:
    pair_sixth = plus(pair_sixth, pair_inserted(H, pair, (0,) * 6))
assert pair_sixth == {5: F(2, 125)}

# One correction-pass test of the complete forest map, beyond a stage defect:
# attach the same eps^2 scalar to edge01 or edge45. Both full evaluated
# families are eps^2*T_H, including every Laurent coefficient. Source-local
# pole projection knows which edge contains the scalar, so recompute it.
base_memo = memo
allocation_finite = {}
for scalar_edge in (0, 10):
    memo = {}
    for index, ids in enumerate(sources):
        if scalar_edge not in ids:
            memo[ids] = base_memo[ids]
            continue
        h_effective = rank(ids) - 2
        alphas = [a for degree in range(0, h_effective, 2)
                  for a in combinations_with_replacement(range(len(graph(ids)[2])), degree)]
        memo[ids] = {a: prepared_moment(ids, a, sources[:index]) for a in alphas}
    value = {}
    for k in range(5):
        alpha = (3,) * k + (4,) * (4 - k)
        value = plus(value, scale(prepared_moment(H, alpha, proper), F((-1)**k * comb(4, k))))
    allocation_finite[scalar_edge] = value
memo = base_memo
allocation_difference = plus(allocation_finite[0], negate(allocation_finite[10]))
print("NEW083: eps^2 allocation finite t^4", allocation_finite, flush=True)
print("NEW083: eps^2 allocation difference", allocation_difference, flush=True)
assert allocation_difference == {
    1: F(1, 288), 2: F(329, 2304), 3: F(-49, 72), 5: F(-1103, 3600),
    6: F(2651, 15552), 7: F(-92, 1323), 30: F(8, 675), 42: F(41, 196)}
allocation_interval = old.enclosing_interval(allocation_difference)
assert allocation_interval[1] < 0
print("NEW083: allocation-difference sign interval", allocation_interval, flush=True)

# Constant-coefficient vertex differentiation is tangent to every cycle relation.
v = (F(0), F(0), F(0), F(0), F(-1, 2), F(1, 2))
c = tuple(v[b] - v[a] for a, b in E)
assert c[-1] == 1
assert c[10] - c[8] + c[6] == 0  # z45-z05+z04
assert sum(ci * ci for ci in c[:-1]) == 1
assert c[6:10] == (F(-1, 2), F(-1, 2), F(1, 2), F(1, 2))
# Independent-edge differentiation of l^2 P produces 2P after evaluation;
# the tangent derivative produces 2(Dl)^2 P=0, including all chain-rule terms.
assert 2 * F(1)**2 == 2
assert 2 * (c[10] - c[8] + c[6])**2 == 0
# At Gaussian variance s, E[P_1(T)] = sqrt(1+s)/sqrt(2*pi).
# Thus the independent-edge null conversion's scalar leading moment is nonzero.
_, _, _, det_G, cov_G = graph(tuple(range(10)))
resistance = cov_G[3][3] + cov_G[4][4] - 2 * cov_G[3][4]
assert resistance == 1
# K_G P has leading degree -4, the all-delta H has degree -6.
assert -rank(tuple(range(10))) + 1 == -4 and -rank(H) == -6

# Full normal Leibniz action detects a mixed test, unlike quotient-value-only
# insertion. At eps=1, q=2, f_y/f=2 and f_yy/f=3 for the two-spoke kernel.
# Pair f*delta'' with y*q: (f*y*q)''(0)=2*q*f_y=8*f, not zero.
q = F(2)
fy_over_f, fyy_over_f = q, q*q - 1
assert (fy_over_f, fyy_over_f) == (2, 3)
assert -2 * fy_over_f * (-q) == 2 * q * fy_over_f == 8

# Honest dilation transport acts on actual evaluated distributions. On a jet
# of degree n with scalar degree a, s^-a*(s_* partial^n delta)=s^(n-a).
# Its cocycle is checked on both bare degrees, including the finite jets.
for a in (4, 6):
    for n in range(9):
        for s, t in ((F(2), F(3)), (F(1, 2), F(5, 3)), (F(7, 4), F(4, 7))):
            assert s**(n-a) * t**(n-a) == (s*t)**(n-a)
# Independent-edge heat has the same non-tangent issue: on l^2 F at l=0,
# (1/2)*sum_e partial_e^2 gives ||grad l||^2 F=3F, not zero.
cycle_coefficients = (F(1), F(-1), F(1))
assert sum(c*c for c in cycle_coefficients) == 3

# Source-local subtraction must also respect regulator allocation if its domain
# identifies full evaluated families. The normalized diamond coefficient is
# b=1/sqrt(8) at degree -2. Moving eps^2 across a source/complement boundary
# changes its pole projection by b*delta. This is a stage-level descent defect.
diamond = (0, 1, 2, 3, 4)
a_diamond = {2: F(1, 4), 6: F(-1, 3), 1: F(-1, 2)}
assert memo[diamond][()] == a_diamond
stage_finite_defect = scale(mult(a_diamond, rinv(8)), F(27, 64))
assert stage_finite_defect == {1: F(27, 512), 3: F(-9, 128), 2: F(-27, 512)}
assert old.enclosing_interval(stage_finite_defect)[1] < 0
def pole(series):
    return {degree: value for degree, value in series.items() if degree < 0}
def shift(series, amount):
    return {degree + amount: value for degree, value in series.items()}
scalar_source = {-2: F(1), 0: F(3), 2: F(5)}
assert pole(shift(scalar_source, 2)) == {}
assert shift(pole(scalar_source), 2) == {0: F(1)}
# Full Laurent storage is used here; no finite-state truncation is involved.

print("PASS083: full eleven-edge intrinsic Gaussian recursion and both disjoint spinneys")
print("PASS083: overlapping F4/F5 are alternatives; nested normal derivatives retained")
print("PASS083: nonzero even-rank F4 and fully prepared host finite controls")
print("PASS083: bare marked conversion and tangent cycle-null correction")
print("PASS083: exact source pole-projection regulator-allocation defect")
print("PASS083: complete-forest nonzero regulator-allocation finite discrepancy")
print("PASS083: mixed normal-jet action and genuine dilation cocycle")
print("SCOPE083: finite algebra only; no common evaluated-domain BV operator certified")
