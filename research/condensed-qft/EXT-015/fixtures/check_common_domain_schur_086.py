"""Independent 086 control: integrate quotient Gaussians before normal jets.

Uses only the frozen 065 rational/radical and Wick primitives, not its
graph(), inserted(), prepared_moment(), source inventory or forest recursion.
Durable review control; not an infinite proof.
"""
from fractions import Fraction as F
from itertools import combinations, combinations_with_replacement
from collections import Counter
from functools import lru_cache
from math import factorial, comb
from pathlib import Path
import importlib.util

spec = importlib.util.spec_from_file_location('radical065', Path(__file__).with_name('check_nested_gaussian_jet_forest_065.py'))
ar = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ar)
edges = tuple(combinations(range(4), 2)) + ((0,4),(1,4),(0,5),(1,5),(4,5))

def verts(ids):
    return sorted(set(v for e in ids for v in edges[e]))

def connected(ids, vs):
    seen = {vs[0]}
    for _ in vs:
        for e in ids:
            a,b = edges[e]
            if a in seen or b in seen:
                seen.update((a,b))
    return seen == set(vs)

sources = []
for size in range(3,12):
    for ids in combinations(range(11),size):
        vs = verts(ids)
        if all(connected(tuple(e for e in ids if e != erased),vs) for erased in ids):
            sources.append(ids)
sources.sort(key=lambda ids:(len(ids),ids))
host = tuple(range(11))
assert sources[-1] == host and len(sources) == 278
pairs = [(a,b) for a,b in combinations(sources[:-1],2) if not set(verts(a)) & set(verts(b))]
assert len(pairs) == 2

def rank(ids):
    return len(ids)-len(verts(ids))+1

@lru_cache(None)
def lap(ids):
    coords = verts(ids)[1:]
    matrix = [[F(0) for _ in coords] for _ in coords]
    for e in ids:
        a,b = edges[e]
        c = [int(v==b)-int(v==a) for v in coords]
        for i in range(len(coords)):
            for j in range(len(coords)):
                matrix[i][j] += c[i]*c[j]
    det,cov = ar.inverse(matrix)
    assert det > 0
    return coords,det,cov

@lru_cache(None)
def schur(parent,beta):
    pv,bv = verts(parent),verts(beta)
    pc,bc = pv[1:],bv[1:]
    pr,br = pv[0],bv[0]
    qc = [v for v in pv if v != pr and (v not in bv or v == br)]
    nu,nq = len(bc),len(qc)
    def coord(v):
        out = [F(0)]*(nu+nq)
        if v in bc: out[bc.index(v)] = F(1)
        if v in bv:
            if br in qc: out[nu+qc.index(br)] = F(1)
        elif v in qc: out[nu+qc.index(v)] = F(1)
        return out
    M = [[F(0)]*(nu+nq) for _ in range(nu+nq)]
    for e in parent:
        if e in beta: continue
        a,b = edges[e]
        linear = [x-y for x,y in zip(coord(b),coord(a))]
        for i in range(nu+nq):
            for j in range(nu+nq): M[i][j] += linear[i]*linear[j]
    A = [row[:nu] for row in M[:nu]]
    B = [row[nu:] for row in M[:nu]]
    det,Dinv = ar.inverse([row[nu:] for row in M[nu:]])
    assert det > 0
    U = [coord(v)[:nu] for v in pc]
    V = [coord(v)[nu:] for v in pc]
    n = nu+len(pc)
    C = [[F(0)]*n for _ in range(n)]
    def contraction(v,w):
        return sum((v[i]*Dinv[i][j]*w[j] for i in range(nq) for j in range(nq)), F(0))
    for i in range(nu):
        for j in range(nu): C[i][j] = -A[i][j]+contraction(B[i],B[j])
        for j in range(len(pc)):
            C[i][nu+j] = C[nu+j][i] = U[j][i]-contraction(B[i],V[j])
    for i in range(len(pc)):
        for j in range(len(pc)): C[nu+i][nu+j] = contraction(V[i],V[j])
    return det,tuple(tuple(row) for row in C),nu

@lru_cache(None)
def integrated_jet(parent,beta,eta,alpha):
    det,C,nu = schur(parent,beta)
    exps = [0]*len(C)
    for i in eta: exps[i] += 1
    for i in alpha: exps[nu+i] += 1
    denom = 1
    for k in Counter(eta).values(): denom *= factorial(k)
    return ar.scale(ar.rinv(det), ar.wick(tuple(exps),C)/denom)

memo = {}
def moment(ids,alpha):
    coords,det,cov = lap(ids)
    exps = tuple(alpha.count(i) for i in range(len(coords)))
    value = ar.scale(ar.rinv(det),ar.wick(exps,cov))
    for beta in sources:
        if len(beta) >= len(ids): break
        if not set(beta) < set(ids): continue
        for eta,m in memo[beta].items():
            value = ar.plus(value,ar.negate(ar.mult(m,integrated_jet(ids,beta,eta,alpha))))
    for a,b in pairs:
        if not (set(a)<set(ids) and set(b)<set(ids)): continue
        first = set(verts(a)) if 0 in verts(a) else set(verts(b))
        crossing = sum((edges[e][0] in first)!=(edges[e][1] in first) for e in ids)
        if any(coords[i] in first for i in alpha): continue
        m = ar.mult(memo[a].get((),{}),memo[b].get((),{}))
        value = ar.plus(value,ar.mult(m,ar.scale(ar.rinv(crossing), ar.wick((len(alpha),),[[F(1,crossing)]]))))
    return value

def prepare(scalar_edge):
    memo.clear()
    for ids in sources:
        h = rank(ids) - (2 if scalar_edge in ids else 0)
        memo[ids] = {alpha:moment(ids,alpha) for degree in range(0,h,2)
                     for alpha in combinations_with_replacement(range(len(lap(ids)[0])),degree)}

def t_moment(degree):
    answer = {}
    for k in range(degree+1):
        alpha = (3,)*k+(4,)*(degree-k)
        answer = ar.plus(answer,ar.scale(moment(host,alpha),F((-1)**k*comb(degree,k))))
    return answer

prepare(None)
A = t_moment(6)
assert A == {3:F(5,64),2:F(265,1536),6:-F(16685,46656),7:F(1160,3969),30:-F(41,810)}
print('INDEPENDENT086 Schur-integrated host t6:',A,flush=True)
prepare(0)
b01 = t_moment(4)
prepare(10)
b45 = t_moment(4)
B = ar.plus(b01,ar.negate(b45))
assert B == {1:F(1,288),2:F(329,2304),3:-F(49,72),5:-F(1103,3600),6:F(2651,15552),7:-F(92,1323),30:F(8,675),42:F(41,196)}
assert ar.enclosing_interval(A)[1]<0 and ar.enclosing_interval(B)[1]<0
print('INDEPENDENT086 Schur-integrated allocation difference:',B,flush=True)
print('PASS086 independent integration order, full sources and legal pairs',flush=True)
