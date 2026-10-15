#!/usr/bin/env python3
"""Exact algebraic counterexample for local claim of Erdős 1082.

Calculations are in Q[sqrt(3)], implemented with rational coefficients.
All 28 pairwise distances and all 56 orientation determinants are checked;
no floating-point arithmetic and no external CAS are required.
"""
import itertools
import json
from fractions import Fraction as F


def Q(a=0, b=0):
    return (F(a), F(b))


def add(x, y):
    return (x[0]+y[0], x[1]+y[1])


def sub(x, y):
    return (x[0]-y[0], x[1]-y[1])


def mul(x, y):
    return (x[0]*y[0]+3*x[1]*y[1], x[0]*y[1]+x[1]*y[0])


def point(x, y):
    return (x, y)


def squared_distance(x, y):
    dx=sub(x[0],y[0])
    dy=sub(x[1],y[1])
    return add(mul(dx,dx),mul(dy,dy))


def determinant(a,b,c):
    x=sub(b[0],a[0])
    y=sub(b[1],a[1])
    z=sub(c[0],a[0])
    t=sub(c[1],a[1])
    return sub(mul(x,t),mul(y,z))


def pretty(x):
    return str(x[0]) + ('+' if x[1]>=0 else '') + str(x[1]) + '*sqrt(3)'


def main():
    half=F(1,2)
    pts=[
      point(Q(0),Q(0)),point(Q(1),Q(0)),
      point(Q(1),Q(1)),point(Q(0),Q(1)),
      point(Q(half),Q(0,-half)),
      point(Q(1,half),Q(half)),
      point(Q(half),Q(1,half)),
      point(Q(0,-half),Q(half)),
    ]
    global_distances=set()
    incident=[set() for _ in pts]
    for i,j in itertools.combinations(range(8),2):
        d=squared_distance(pts[i],pts[j])
        assert d!=Q(0)
        global_distances.add(d)
        incident[i].add(d)
        incident[j].add(d)
    all_triples=0
    for i,j,k in itertools.combinations(range(8),3):
        assert determinant(pts[i],pts[j],pts[k])!=Q(0), (i,j,k)
        all_triples+=1
    assert all_triples==56
    assert global_distances=={Q(1),Q(2),Q(2,1),Q(4,2)}
    assert all(incident[i]=={Q(1),Q(2),Q(2,1)} for i in range(4))
    assert all(incident[i]=={Q(1),Q(2,1),Q(4,2)} for i in range(4,8))
    assert len(global_distances)==4
    assert all(len(x)==3 for x in incident)
    receipt={
       "record_type":"EC_BULK_007_FINITE_ARITHMETIC_PHASE_6/1",
       "cohort_id":"EC-BULK-007","problem_id":1082,
       "finite_claim_verified":"eight-point geometric counterexample only to single-point version",
       "external_lean_kernel_replay":False,
       "global_distinct_distance_conjecture_resolved":False,
       "points":8,"pairs_checked":28,"triple_determinants_checked":56,
       "collinear_triples":0,
       "global_squared_distances":sorted(map(pretty,global_distances)),
       "global_distinct_distance_count":4,
       "distinct_distances_per_point":[len(x) for x in incident],
       "local_max_distinct_distance_count":3,
       "required_local_claim_floor_n_over_2":4,
       "individual_corner_squared_distances":sorted(map(pretty,incident[0])),
       "individual_apex_squared_distances":sorted(map(pretty,incident[4])),
       "result":"FINITE_COUNTEREXAMPLE_PASS",
    }
    print(json.dumps(receipt,indent=2))


if __name__=="__main__":
    main()
