#!/usr/bin/env python3
"""Bounded reproducible examples for Erdős #1079–#1084 (excluding #1082).

Verifies ONLY finite examples, no asymptotic, existential or optimality theorem.
"""
import json
from itertools import combinations, product
from math import comb, isqrt


def turan_edges(n, parts):
    sizes=[n//parts + (i<n%parts) for i in range(parts)]
    return (n*n - sum(x*x for x in sizes))//2


def complete_graph_neighborhood():
    # r=4, G=K4: E=6 exceeds ex(4;K4)=T3(4)=5
    # a vertex has d=3 and N(v)=K3 with 3 edges > ex(3;K3)=T2(3)=2
    assert turan_edges(4,3)==5
    assert turan_edges(3,2)==2
    return {'r':4,'n':4,'G':'K4','edges_G':comb(4,2),
            'ex_n_Kr':5,'vertex_degree':3,'edges_in_neighborhood':3,
            'ex_d_Krminus1':2,'strict_surplus':1}


def bipartite_star():
    # 13 vertices: star K1,12, 12 edges, no cycles at all.
    n=13
    e=n-1
    return {'vertices':n,'edges':e,'bipartition_sizes':[1,12],
            'contains_cycle_C6':False,
            'scope':'finite illustration ONLY: this does not refute existence of some large c'}


def squarefull(n):
    if n<1: return False
    t=n
    p=2
    while p*p<=t:
        if t%p==0:
            a=0
            while t%p==0:
                t//=p
                a+=1
            if a<2:return False
        p+=1
    return t==1 # residual prime to exponent 1 invalid


def squarefull_sums(limit):
    s=[n for n in range(1,limit+1) if squarefull(n)]
    a={x+y for x in s for y in s if x+y<=limit}
    assert 1 in s and 4 in s and 8 in s and 9 in s
    assert min(a)==2 and 5 in a and 8 in a and 10 in a
    return {'cutoff':limit,'squarefull_count':len(s),
            'squarefull_numbers':s,
            'representable_count':len(a),
            'first_20_representable':sorted(a)[:20],
            'A_of_250':len(a)}


def lattice_squared_distances(d,q):
    points=list(product(range(q),repeat=d))
    ds={sum((a[i]-b[i])**2 for i in range(d))
        for a,b in combinations(points,2)}
    assert len(points)==q**d
    assert all(0<x<=d*(q-1)**2 for x in ds)
    return {'dimension':d,'grid_side':q,'points':len(points),
            'squared_distinct_distance_types':len(ds),
            'squared_distances':sorted(ds),
            'elementary_upper_bound_types':d*(q-1)**2}


def hex_lattice(radius):
    # axial coordinates in Euclidean triangular lattice, squared distance:
    # (dx)^2 +(dx)*(dy)+(dy)^2, with basis vectors at 60 degrees.
    pts=[(a,b) for a in range(-radius,radius+1)
                 for b in range(-radius,radius+1)
                 if max(abs(a),abs(b),abs(a+b))<=radius]
    n=len(pts)
    target=3*radius*radius+3*radius+1
    assert n==target
    ds=lambda a,b:(a[0]-b[0])**2+(a[0]-b[0])*(a[1]-b[1])+(a[1]-b[1])**2
    assert all(ds(a,b)>=1 for a,b in combinations(pts,2))
    contacts=sum(ds(a,b)==1 for a,b in combinations(pts,2))
    target_contacts=9*radius*radius+3*radius
    assert contacts==target_contacts
    contact_formula=3*n-isqrt(12*n-3)
    assert isqrt(12*n-3)**2==12*n-3 and contact_formula==contacts
    return {'radius':radius,'points':n,'unit_contacts':contacts,
            'harborth_formula_at_n':contact_formula,
            'formula_checked_as_finite_lower_witness_only':True}


def main():
    result={'record_type':'EC_BULK_007_FINITE_ARITHMETIC_PHASE_7/1',
       'cohort_id':'EC-BULK-007',
       'problem_1079':complete_graph_neighborhood(),
       'problem_1080':bipartite_star(),
       'problem_1081':squarefull_sums(250),
       'problem_1083':[lattice_squared_distances(d,q) for d,q in ((3,2),(3,3),(4,2))],
       'problem_1084':[hex_lattice(r) for r in (1,2,3,4)],
       'mathematical_certification':False,
       'status':'FINITE_CHECKS_PASS'}
    print(json.dumps(result,indent=2,ensure_ascii=False))


if __name__=='__main__':
    main()
