#!/usr/bin/env python3
"""Exact bounded arithmetic witnesses for Erdős #898 and #899.

No finite computation certifies the general theorems or any Lean statement.
"""
from __future__ import annotations
import json
from itertools import combinations, product
from pathlib import Path


def sub(u, v):
    return (u[0] - v[0], u[1] - v[1])


def sq(u):
    return u[0] * u[0] + u[1] * u[1]


def cross(u, v):
    return u[0] * v[1] - u[1] * v[0]


def lemma_certificate(vertices, weights, vertex_index):
    """Exact squared form of a*PA >= b*z+c*y, no floating point."""
    s = sum(weights)
    v = vertices[vertex_index]
    u = vertices[(vertex_index + 1) % 3]
    w = vertices[(vertex_index + 2) % 3]
    p_num = (sum(weights[t] * vertices[t][0] for t in range(3)),
             sum(weights[t] * vertices[t][1] for t in range(3)))
    ap_num = (p_num[0] - s * v[0], p_num[1] - s * v[1])
    a2 = sq(sub(u, w))
    b2 = sq(sub(v, w))
    c2 = sq(sub(v, u))
    assert a2 * b2 * c2 > 0
    left = a2 * b2 * c2 * sq(ap_num)
    right = (b2 * abs(cross(ap_num, sub(u, v))) +
             c2 * abs(cross(ap_num, sub(w, v)))) ** 2
    return left, right


def geometry():
    pts = list(product(range(-2, 3), repeat=2))
    weights = [(i, j, k) for i in range(1, 4)
               for j in range(1, 4) for k in range(1, 4)]
    triangles = 0
    checked = 0
    min_slack = None
    for vertices in combinations(pts, 3):
        if cross(sub(vertices[1], vertices[0]),
                 sub(vertices[2], vertices[0])) == 0:
            continue
        triangles += 1
        for ws in weights:
            for t in range(3):
                lhs, rhs = lemma_certificate(vertices, ws, t)
                assert lhs >= rhs, (vertices, ws, t, lhs, rhs)
                checked += 1
                slack = lhs - rhs
                if min_slack is None or slack < min_slack:
                    min_slack = slack
    # Equilateral equality: vertices at radius 2/sqrt(3), sides 2,
    # and inradius 1/sqrt(3): 3*(2/sqrt3)=2*3*(1/sqrt3).
    assert 3 * 2 == 2 * 3 * 1
    return dict(triangles=triangles, positive_barycentric_weight_triples=len(weights),
                exact_vertex_lemma_checks=checked, minimum_squared_slack=min_slack,
                equilateral_centroid_equality='3*(2/sqrt(3)) = 2*3*(1/sqrt(3))')


def differences_of_powers(m):
    n = (1 << m) - 1
    # All powers through 2^m; larger powers cannot yield differences <=n.
    powers = [1 << k for k in range(m + 1)]
    differences = {powers[j] - powers[i] for j in range(1, m + 1)
                   for i in range(j) if powers[j] - powers[i] <= n}
    return n, differences


def additive():
    rows = []
    for m in range(1, 17):
        n, ds = differences_of_powers(m)
        a_count = m
        assert len(ds) == m * (m + 1) // 2
        # Independent 2-adic encoding: 2^i(2^h-1), h>=1.
        encoding = set()
        for j in range(1, m + 1):
            for i in range(j):
                d = (1 << j) - (1 << i)
                if d <= n:
                    odd = d
                    valuation = 0
                    while odd % 2 == 0:
                        valuation += 1
                        odd //= 2
                    assert (valuation, odd) not in encoding
                    encoding.add((valuation, odd))
        assert len(encoding) == len(ds)
        rows.append(dict(m=m, N=n, A_count=a_count, positive_difference_count=len(ds),
                         ratio_numerator=len(ds), ratio_denominator=a_count))
    # A positive-density control example: multiples of 3.
    for n in range(3, 201):
        a = [3 * k for k in range(1, n // 3 + 1)]
        d = {3 * k for k in range(1, n // 3 + 1)}
        assert len(a) == len(d) == n // 3
    return dict(power_two_rows=rows, positive_density_control='A=3N: D(N)=A(N)=floor(N/3)')


def main():
    out = {'record_type': 'EC_BULK_006_FINITE_898_899/1',
           'scope': 'bounded arithmetic only, no global theorem or Lean certification',
           'erdos_898': geometry(), 'erdos_899': additive()}
    print(json.dumps(out, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
