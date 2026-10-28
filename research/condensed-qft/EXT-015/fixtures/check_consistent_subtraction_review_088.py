#!/usr/bin/env python3
"""Non-author 088 controls: Taylor normal jets and derived marked operators.

No import of 087, its memo, its recurrence, or the reviewer's 086 Schur code.
Only 065's rational/radical, matrix-inverse and scalar-Wick primitives are
shared. Rebuild the unallocated normalized forest by expanding before quotient
integration, and derive the marked operator polynomials from cusp derivatives.
Finite checks only; no external/institutional independence or BV certificate.
"""
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations, combinations_with_replacement
from math import comb, factorial
from pathlib import Path
import importlib.util

spec = importlib.util.spec_from_file_location(
    'arithmetic065', Path(__file__).with_name('check_nested_gaussian_jet_forest_065.py'))
ar = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ar)
edges = tuple(combinations(range(4), 2)) + ((0,4),(1,4),(0,5),(1,5),(4,5))
MAX_NORMAL = 4

def vertices(ids):
    return sorted({v for e in ids for v in edges[e]})

def connected(ids, vs):
    seen = {vs[0]}
    for _ in vs:
        for e in ids:
            a,b = edges[e]
            if a in seen or b in seen: seen.update((a,b))
    return seen == set(vs)

sources = [ids for size in range(3,12) for ids in combinations(range(11),size)
           if all(connected(tuple(e for e in ids if e != erased), vertices(ids))
                  for erased in ids)]
sources.sort(key=lambda a:(len(a),a))
host, proper = tuple(range(11)), tuple(sources[:-1])
pairs = [(a,b) for a,b in combinations(proper,2) if not set(vertices(a)) & set(vertices(b))]
assert sources[-1] == host and len(proper) == 277 and len(pairs) == 2

def rank(ids): return len(ids)-len(vertices(ids))+1

@lru_cache(None)
def graph(ids):
    coords = vertices(ids)[1:]
    Q = [[F(0)]*len(coords) for _ in coords]
    for e in ids:
        a,b = edges[e]
        v = [F(int(j == b)-int(j == a)) for j in coords]
        for i in range(len(coords)):
            for j in range(len(coords)): Q[i][j] += v[i]*v[j]
    det,cov = ar.inverse(Q)
    assert det > 0
    return coords,det,cov

def padd(a,b):
    out = dict(a)
    for k,v in b.items(): out[k] = out.get(k,F(0))+v
    return {k:v for k,v in out.items() if v}

def pscale(a,c): return {k:v*c for k,v in a.items() if v*c}

def pmul(a,b):
    out = {}
    for (u,q),x in a.items():
        for (v,r),y in b.items():
            nu = tuple(i+j for i,j in zip(u,v))
            if sum(nu) > MAX_NORMAL: continue
            nq = tuple(i+j for i,j in zip(q,r))
            out[nu,nq] = out.get((nu,nq),F(0))+x*y
    return {k:v for k,v in out.items() if v}

@lru_cache(None)
def normal_taylor(parent,beta):
    pv,bv = vertices(parent),vertices(beta)
    pc,bc = pv[1:],bv[1:]
    pr,br = pv[0],bv[0]
    qc = [v for v in pv if v != pr and (v not in bv or v == br)]
    nu,nq = len(bc),len(qc)
    def coordinate(v):
        u,q = [F(0)]*nu,[F(0)]*nq
        if v in bc: u[bc.index(v)] = F(1)
        if v in bv:
            if br in qc: q[qc.index(br)] = F(1)
        elif v in qc: q[qc.index(v)] = F(1)
        return u,q
    expr = {v:coordinate(v) for v in pv}
    A,B,D = ([[F(0)]*nu for _ in range(nu)],
             [[F(0)]*nq for _ in range(nu)],
             [[F(0)]*nq for _ in range(nq)])
    for e in parent:
        if e in beta: continue
        a,b = edges[e]
        u = [x-y for x,y in zip(expr[b][0],expr[a][0])]
        q = [x-y for x,y in zip(expr[b][1],expr[a][1])]
        for i in range(nu):
            for j in range(nu): A[i][j] += u[i]*u[j]
            for j in range(nq): B[i][j] += u[i]*q[j]
        for i in range(nq):
            for j in range(nq): D[i][j] += q[i]*q[j]
    det,cov = ar.inverse(D)
    assert det > 0
    one = {((0,)*nu,(0,)*nq):F(1)}
    exponent = {}
    for i in range(nu):
        for j in range(nu):
            u = [0]*nu
            u[i] += 1; u[j] += 1
            key = (tuple(u),(0,)*nq)
            exponent[key] = exponent.get(key,F(0))-A[i][j]/2
        for j in range(nq):
            u,q = [0]*nu,[0]*nq
            u[i] = q[j] = 1
            key = (tuple(u),tuple(q))
            exponent[key] = exponent.get(key,F(0))-B[i][j]
    term,exponential = one,one
    for n in range(1,MAX_NORMAL+1):
        term = pscale(pmul(term,exponent),F(1,n))
        exponential = padd(exponential,term)
    return expr,det,cov,one,exponential

def linear(u,q):
    out = {}
    for i,c in enumerate(u):
        if c:
            e = [0]*len(u); e[i] = 1
            out[tuple(e),(0,)*len(q)] = c
    for i,c in enumerate(q):
        if c:
            e = [0]*len(q); e[i] = 1
            out[(0,)*len(u),tuple(e)] = c
    return out

counterterms = {}
def bare(ids,alpha):
    coords,det,cov = graph(ids)
    return ar.scale(ar.rinv(det), ar.wick(tuple(alpha.count(i) for i in range(len(coords))),cov))

def inserted(parent,beta,alpha):
    expr,det,cov,test,exponential = normal_taylor(parent,beta)
    for i in alpha: test = pmul(test,linear(*expr[graph(parent)[0][i]]))
    test = pmul(test,exponential)
    value = {}
    for eta,coefficient in counterterms[beta].items():
        powers = tuple(eta.count(i) for i in range(len(graph(beta)[0])))
        avg = sum((c*ar.wick(q,cov) for (u,q),c in test.items() if u == powers),F(0))
        value = ar.plus(value, ar.mult(coefficient,ar.scale(ar.rinv(det),avg)))
    return value

def prepared(ids,alpha):
    value = bare(ids,alpha)
    for beta in proper:
        if len(beta) >= len(ids): break
        if set(beta) < set(ids): value = ar.plus(value,ar.negate(inserted(ids,beta,alpha)))
    for a,b in pairs:
        if not (set(a)<set(ids) and set(b)<set(ids)): continue
        first = set(vertices(a)) if 0 in vertices(a) else set(vertices(b))
        if any(graph(ids)[0][i] in first for i in alpha): continue
        crossing = sum((edges[e][0] in first)!=(edges[e][1] in first) for e in ids)
        product = ar.mult(counterterms[a].get((),{}),counterterms[b].get((),{}))
        term = ar.scale(ar.rinv(crossing),ar.wick((len(alpha),),[[F(1,crossing)]]))
        value = ar.plus(value,ar.mult(product,term))
    return value

finite_sources = 0
for ids in proper:
    ct = {}
    h = rank(ids)
    for degree in range(0,h+1,2):
        for alpha in combinations_with_replacement(range(len(graph(ids)[0])),degree):
            value = prepared(ids,alpha)
            if degree == h: value = ar.plus(value,ar.negate(bare(ids,alpha)))
            if value: ct[alpha] = value
    counterterms[ids] = ct
    finite_sources += any(len(a) == h for a in ct)
coefficients = sum(len(ct) for ct in counterterms.values())
assert (coefficients,finite_sources) == (6698,137)

finite_host_ct = {}
for k in range(7):
    alpha = (3,)*k+(4,)*(6-k)
    term = ar.plus(prepared(host,alpha),ar.negate(bare(host,alpha)))
    finite_host_ct = ar.plus(finite_host_ct,ar.scale(term,F((-1)**k*comb(6,k))))
assert finite_host_ct == {2:F(265,1536),6:-F(70285,186624),7:F(8860,27783),30:-F(41,810)}
print('PASS088 Taylor-first normalized recursion: 277 proper sources, 6698 coefficients, 137 finite sources',flush=True)
print('PASS088 independently rebuilt finite host counterterm:',finite_host_ct,flush=True)

# Derive all marked coefficients from exp(L/2) P_s^(r)(D), s^2=2.
# Divide by the common P_s(0), and include the distributional (-1)^degree.
def dfact(n):
    value = 1
    for j in range(n,0,-2): value *= j
    return value

def cusp_at_zero(n):
    if n == 0: return F(1)
    if n % 2: return F(0)
    m = n//2
    return F((-1)**(m-1)*dfact(2*m-3),2**m)

def marked_operator(degree,derivative=0):
    return {(i,degree-2*i): F((-1)**degree,2**i*factorial(i)) *
            cusp_at_zero(degree-2*i+derivative)/factorial(degree-2*i)
            for i in range(degree//2+1) if cusp_at_zero(degree-2*i+derivative)}

assert marked_operator(2) == {(1,0):F(1,2),(0,2):F(1,4)}
assert marked_operator(4) == {(2,0):F(1,8),(1,2):F(1,8),(0,4):-F(1,96)}
assert marked_operator(6) == {(3,0):F(1,48),(2,2):F(1,32),(1,4):-F(1,192),(0,6):F(1,1920)}
assert marked_operator(8) == {(4,0):F(1,384),(3,2):F(1,192),(2,4):-F(1,768),(1,6):F(1,3840),(0,8):-F(1,43008)}
assert marked_operator(7,1) == {(3,1):-F(1,96),(2,3):F(1,192),(1,5):-F(1,640),(0,7):F(1,5376)}
print('PASS088 marked full operator coefficients derived from conditioned cusp Taylor derivatives',flush=True)
print('LIMIT088 finite arithmetic and matrix/profile identities; no proof of global BV or external certification',flush=True)
