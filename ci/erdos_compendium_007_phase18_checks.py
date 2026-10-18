#!/usr/bin/env python3
"""Exact finite fixtures Erdős 1152–1159; explicitly not infinite theorem proofs."""
from fractions import Fraction as Q
from functools import lru_cache
from itertools import combinations
from math import comb
import json

def p1152():
    # Degree<3 interpolation of f(x)=x^3 at -1,0,1 equals x.
    nodes=[-1,0,1]
    assert all(x**3==x for x in nodes)
    x=Q(1,2)
    assert x**3!=x
    return {"nodes":nodes,"f":"x^3","interpolant_degree_below_3":"x",
            "difference_at_half":str(x-x**3),"finite_n_does_not_prove_almost_everywhere_nonconvergence":True}

def p1153():
    x=Q(1,2)
    basis=(x*(x-1)/2,1-x*x,x*(x+1)/2)
    assert sum(abs(u) for u in basis)==Q(5,4)
    return {"nodes":[-1,0,1],"leb_at_x_half":"5/4",
            "max_on_interval_[0,1]":"5/4",
            "finite_degree_not_uniform_log_n_lower_bound":True}

def p1154():
    return {"field_Q":"countable; Hausdorff dimension 0",
            "field_R":"full real line; Hausdorff dimension 1",
            "rational_sum_product_closed":True,
            "endpoint_examples_do_not_prove_intermediate_dimensions":True}

def triangles(edges,n):
    es=set(edges)
    return [frozenset(((i,j),(i,k),(j,k))) for i,j,k in combinations(range(n),3)
            if (i,j) in es and (i,k) in es and (j,k) in es]
def p1155():
    @lru_cache(None)
    def expected(es,n):
        tt=triangles(es,n)
        if not tt:return Q(len(es))
        return sum((expected(tuple(x for x in es if x not in t),n) for t in tt),Q())/len(tt)
    out={}
    for n in range(3,6):
        E=tuple(combinations(range(n),2))
        out[str(n)]=str(expected(E,n))
    assert out["3"]=="0" and out["4"]=="3"
    return {"process":"uniformly choose a PRESENT triangle; delete all 3 edges",
            "exact_expected_terminal_edges_n_3_to_5":out,
            "terminal_graph_triangle_free":True,
            "finite_exact_expectations_not_n_to_infinity_exponent":True}

def chromatic(edges,n):
    adjacency=[set() for _ in range(n)]
    for u,v in edges:adjacency[u].add(v);adjacency[v].add(u)
    order=sorted(range(n),key=lambda v:-len(adjacency[v]))
    def good(k,idx,colors):
        if idx==n:return True
        v=order[idx]
        for c in range(k):
            if all(colors[w]!=c for w in adjacency[v]):
                colors[v]=c
                if good(k,idx+1,colors):return True
                colors[v]=-1
        return False
    for k in range(1,n+1):
        if good(k,0,[-1]*n):return k
    raise AssertionError()
def p1156():
    out={}
    for n in (3,4):
        E=list(combinations(range(n),2));hist={}
        for mask in range(1<<len(E)):
            e=[E[i] for i in range(len(E)) if (mask>>i)&1]
            k=chromatic(e,n);hist[k]=hist.get(k,0)+1
        assert sum(hist.values())==2**comb(n,2)
        out[str(n)]={"possible_graphs":2**comb(n,2),"chromatic_histogram":hist}
    assert out["3"]["chromatic_histogram"]=={1:1,2:6,3:1}
    return {"G_n_half_exact_law":out,
            "finite_distributions_not_asymptotic_constant_window_or_anti_concentration":True}

def p1157():
    n=5
    E=list(combinations(range(n),2))
    no_tri=0;maxsize=0
    for mask in range(1<<len(E)):
        es={E[i] for i in range(len(E)) if mask>>i&1}
        if not triangles(tuple(sorted(es)),n):
            no_tri+=1;maxsize=max(maxsize,len(es))
    assert maxsize==6
    # For 3-uniform 4 vertices, two distinct triples share two vertices, union 4.
    return {"graph_r2_k3_s3":"K3 forbidden",
      "ex_2_5_K3":maxsize,"Mantel_floor_n²_over_4":6,
      "hypergraph_r3_k4_s2_n4_extremal_edge_count":1,
      "catalogue_statement_t_unused_and_s_not_bounded":True}

def has_c4(es,n):
    adjacency=[set() for _ in range(n)]
    for u,v in es:adjacency[u].add(v);adjacency[v].add(u)
    return any(len(adjacency[u]&adjacency[v])>=2 for u,v in combinations(range(n),2))
def p1158():
    n=4;E=list(combinations(range(n),2));best=0
    for mask in range(1<<len(E)):
        e=[E[i] for i in range(len(E)) if mask>>i&1]
        if not has_c4(e,n):best=max(best,len(e))
    assert best==4
    return {"t":2,"r":2,"K_2_2":"C4",
            "ex_2_4_K_2_2":best,
            "proposed_exponent_t_minus_r_power_1_minus_t":"3/2",
            "finite_extremal_count_not_asymptotic_lower_bound":True}

def plane(q):
    assert q in (2,3)
    def norm(v):
        i=next(i for i,x in enumerate(v) if x)
        inv=pow(v[i],-1,q)
        return tuple((x*inv)%q for x in v)
    pts=sorted({norm(x) for x in __import__('itertools').product(range(q),repeat=3) if any(x)})
    lines=pts[:]
    incident=[tuple(i for i,p in enumerate(pts) if sum(a*b for a,b in zip(p,L))%q==0) for L in lines]
    assert len(pts)==q*q+q+1 and all(len(L)==q+1 for L in incident)
    assert all(sum(i in A and i in B for i in range(len(pts)))==1 for A,B in combinations(incident,2))
    return pts,incident
def p1159():
    result={}
    for q in (2,3):
        pts,lines=plane(q)
        count=len(pts);hist={};best=None
        for mask in range(1<<count):
            occup=[sum((mask>>i)&1 for i in L) for L in lines]
            if all(occ>=1 for occ in occup):
                maxocc=max(occup);hist[maxocc]=hist.get(maxocc,0)+1
                cand=(maxocc,mask.bit_count(),mask)
                if best is None or cand<best:best=cand
        assert best
        mx,sz,mask=best
        if q==2:assert mx==3
        result[str(q)]={"points":count,"lines":len(lines),
             "points_per_line":q+1,"minimum_feasible_C":mx,
             "witness_point_indices":[i for i in range(count) if mask>>i&1],
             "witness_size":sz,"blocking_subset_counts_by_max_line_occupancy":hist}
    return {"finite_projective_planes_over_prime_fields":result,
            "Fano_plane_does_not_admit_C_2_blocking_set":True,
            "finite_cases_do_not_establish_universal_C_independent_of_order":True}

def main():
    out={"record_type":"EC_BULK_007_FINITE_PHASE_18/1",
         "cohort_id":"EC-BULK-007","mathematical_certification":False}
    for n in range(1152,1160):out[f"problem_{n}"]=globals()[f"p{n}"]()
    out["result"]="FINITE_CHECKS_PASS"
    print(json.dumps(out,indent=2))
if __name__=="__main__":main()
