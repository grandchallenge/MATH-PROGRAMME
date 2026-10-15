#!/usr/bin/env python3
"""Exact bounded examples of #894, independent finite MILP encoding of #895.

MILP statuses are solver reports and NOT a checked DRAT/LRAT proof.
"""
import json
from itertools import combinations
from fractions import Fraction
from math import floor
import numpy as np
from scipy.optimize import milp, Bounds, LinearConstraint
from scipy.sparse import lil_matrix

def test_894():
    # Any positive power of 2 is nonzero mod 3.
    # Any positive power of 3 is nonzero mod 2.
    entries=[]
    for base,q,max_k in ((2,3,12),(3,2,8),(2,5,12)):
        seq=[base**k for k in range(max_k)]
        assert all(d%q !=0 for d in seq)
        assert all(seq[k+1]>=base*seq[k] for k in range(len(seq)-1))
        for bound in (32,200,2000):
            C=[v%q for v in range(1,bound+1)]
            D=set(d for d in seq if d<bound)
            assert all(C[a-1]!=C[a+d-1]
                for d in D for a in range(1,bound-d+1))
        entries.append(dict(sequence_base=base,modulus_q=q,
           exponents_checked=[0,max_k-1],max_n=2000,
           rotational_parameter=f"1/{q}",minimum_circle_distance=f"1/{q}",
           all_checked_powers_nonzero_mod_q=True,
           colour_by_integer_remainder_mod_q=True))
    # Exact elementary rotation-bin lemma checked on all rational theta in a grid:
    # If two positions in the same half-open bin have distance < w in the
    # circle metric, their difference has norm < w. (Use exact fractions.)
    tests=0
    for q in (3,5,7,11):
        for step in range(1,q):
            for b in range(1,q):
                width=Fraction(1,b)
                theta=Fraction(step,q)
                xs=[(n*theta)%1 for n in range(0,4*q)]
                for i,j in combinations(range(len(xs)),2):
                    if floor(xs[i]/width)==floor(xs[j]/width):
                        z=(j-i)*theta
                        dist=min(z%1,1-(z%1))
                        assert dist<width
                        tests+=1
    return dict(exact_modular_examples=entries,
       exact_rotation_bin_implications_tested=tests,
       note="explicit rational theta works for these particular lacunary sequences; theorem for ALL lacunary sequences is imported")

def graph_formulation(n,seconds=9):
    edge=list(combinations(range(1,n+1),2))
    idx={e:i for i,e in enumerate(edge)}
    rows=[];lb=[];ub=[]
    def add(edges,lo,hi):
        rows.append([idx[tuple(sorted(e))] for e in edges])
        lb.append(lo);ub.append(hi)
    for a,b,c in combinations(range(1,n+1),3):
        add(((a,b),(a,c),(b,c)),-np.inf,2)
    triples=[]
    for a in range(1,n+1):
        for b in range(a+1,n+1):
            c=a+b
            if c>n:continue
            triples.append((a,b,c))
            # To AVOID an independent triple, require at least one edge.
            add(((a,b),(a,c),(b,c)),1,np.inf)
    M=lil_matrix((len(rows),len(edge)),dtype=np.float64)
    for i,cols in enumerate(rows):
        for j in cols:M[i,j]=1
    res=milp(c=np.zeros(len(edge)),integrality=np.ones(len(edge),dtype=np.int8),
      bounds=Bounds(0,1),constraints=LinearConstraint(M.tocsr(),
      np.asarray(lb),np.asarray(ub)),options={'time_limit':seconds,'mip_rel_gap':0})
    data=dict(n=n,vertices=n,edges_variables=len(edge),
      triangle_constraints=n*(n-1)*(n-2)//6,
      schur_triples=len(triples),status=int(res.status),
      message=res.message,proof_grade='NUMERICAL_SOLVER_REPORT_ONLY')
    if res.x is not None:
        G=[list(e) for e,v in zip(edge,res.x) if v>0.5]
        E={tuple(e) for e in G}
        assert all(sum((tuple(sorted(p)) in E for p in combinations((a,b,c),2)))<=2
            for a,b,c in combinations(range(1,n+1),3))
        assert all(sum((tuple(sorted(p)) in E for p in combinations((a,b,c),2)))>=1
            for a,b,c in triples)
        data['counterexample_edges']=G
        data['counterexample_verified_exact']=True
    return data

def test_895():
    models=[graph_formulation(n,seconds=10 if n>=18 else 3)
            for n in (6,9,12,15,17,18)]
    return dict(
      counterexample_encoding="binary edge variables, every triangle <=2 edges, every positive a<b with a+b<=n triple >=1 edge",
      proof_boundary="infeasible MILP is not independently proof-certified without LRAT or exact exhaustive replay",
      models=models)

if __name__=='__main__':
    print(json.dumps(dict(record_type='EC_BULK_006_894_895_FINITE/1',
        authority='bounded modular/circle arithmetic and MILP evidence, NOT a certified SAT proof',
        p894=test_894(),p895=test_895()),indent=2))
