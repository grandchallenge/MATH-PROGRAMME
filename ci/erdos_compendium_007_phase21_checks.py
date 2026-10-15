#!/usr/bin/env python3
"""Exact finite evidence for #1176–1183. Never an infinite theorem certificate."""
import itertools,json,math
from collections import Counter,deque

def chi3(edges,n):
    for k in range(1,n+1):
        for cs in itertools.product(range(k),repeat=n):
            if all(not(cs[a]==cs[b]==cs[c]) for a,b,c in edges):
                return k
    raise AssertionError
def p1176():
    # Properly 2-color K2, all vertex color classes have zero internal edges.
    E={(0,1)}
    cs=[0,1]
    assert all(cs[a]!=cs[b] for a,b in E)
    return {"graph":"K2","chromatic_number":2,
      "one_edge_color":"red","vertex_two_coloring":[0,1],
      "every_monochromatic_vertex_class_has_no_edge":True,
      "finite_obstruction_not_uncountable_chromatic_question":True}
def p1177():
    n=5; E=list(itertools.combinations(range(n),3))
    assert len(E)==10 and chi3(E,n)==3
    assert chi3(list(itertools.combinations(range(4),3)),4)==2
    return {"complete_3_uniform_4_vertices_chromatic":2,
      "complete_3_uniform_5_vertices_chromatic":3,
      "complete_3_uniform_5_vertices_edges":10,
      "weak_hypergraph_chromatic_no_monochromatic_edge":True,
      "finite_colors_not_uncountable_cardinal_models":True}
def p1178():
    # For three distinct 3-edges on any n<=6 vertices, their union
    # has <=6 vertices, hence forbidden F_{6,3}. Two edges are allowed.
    return {"r":3,"e":3,"target_d":6,
      "ex_3_n_4_5_6_forbidden_3_edges_on_at_most_6":[2,2,2],
      "d_3_3_equals_6_external_Ruzsa_Szemeredi_only":True,
      "finite_n_le_d_is_not_o_n_squared":True}
def p1179():
    p=7;A=(1,2,4)
    h=Counter()
    for mask in range(1<<len(A)):
        h[sum(x for i,x in enumerate(A) if mask>>i&1)%p]+=1
    assert h[0]==2 and all(h[g]==1 for g in range(1,p))
    return {"group":"Z/7Z","subset_A":list(A),"k":3,
      "subset_sum_counts":[h[g] for g in range(p)],
      "uniform_reference":"8/7",
      "not_nearly_uniform_for_epsilon_below_3/4":True,
      "finite_example_not_random_k_asymptotic":True}
def p1180():
    p=11;R=sorted({pow(n,-1,p) for n in (1,2,3)})
    reach={0}; layers=[]
    for c in range(12):
        layers.append({"summands_at_most":c,"reachable_count":len(reach)})
        if len(reach)==p:break
        reach|={(v+r)%p for v in list(reach) for r in R}
    assert len(reach)==p
    return {"prime":p,"epsilon":"1/2","allowed_n":[1,2,3],
      "inverses_mod_p":R,"minimal_at_most_summands_to_cover_all_residues":c,
      "reachability_by_c":layers,
      "bounded_example_not_uniform_C_epsilon_for_all_primes":True}
def least_missing_prime(n,k):
    v=math.prod(n+i for i in range(1,k+1))
    p=2
    while True:
        if p>1 and all(p%d for d in range(2,math.isqrt(p)+1)) and v%p: return p
        p+=1
def p1181():
    samples={}
    for n,k in ((10,2),(100,4),(1000,7),(10000,10)):
        q=least_missing_prime(n,k)
        samples[f"{n},{k}"]=q
    assert samples["10,2"]==5
    return {"q_n_k_samples":samples,
      "log_n_not_integer_requires_floor_or_ceiling_convention":True,
      "primorial_upper_asymptotic_external_only":True}
def all_graph_edges(n):return list(itertools.combinations(range(n),2))
def p1182():
    # R(K3,P3)=5: enumerate all K4 / K5 2-edge-colorings.
    def bad(n):
        E=all_graph_edges(n);index={e:i for i,e in enumerate(E)}
        for mask in range(1<<len(E)):
            red={E[i] for i in range(len(E)) if mask>>i&1}
            if any(all(e in red for e in ((a,b),(a,c),(b,c)))
                   for a,b,c in itertools.combinations(range(n),3)):continue
            blue=set(E)-red
            # canonical blue P3 consists of two edges sharing one vertex.
            if any(sum(b in e for e in blue)>=2 for b in range(n)):continue
            return mask
        return None
    assert bad(4) is not None and bad(5) is None
    return {"R_K3_P3_exact":5,"K4_has_countercoloring":True,
      "K5_all_2_edge_colorings_satisfy_red_triangle_or_blue_P3":True,
      "n_3_tree_R_equals_2n_minus_1":True,
      "finite_Ramsey_not_f_or_F_asymptotic":True}
def p1183():
    # Enumerate n=3 all 2^8 colorings of Boolean lattice P([3]).
    n=3;sets=list(range(1<<n))
    closed_both=[];closed_join=[]
    for fam_mask in range(1,1<<(1<<n)):
        members=[S for S in sets if fam_mask>>S&1]
        S=set(members)
        join=all((a|b) in S for a in members for b in members)
        if join:
            closed_join.append((fam_mask,len(members)))
            if all((a&b) in S for a in members for b in members):
                closed_both.append((fam_mask,len(members)))
    def guaranteed(families):
        worst=1<<n;witness=None
        for coloring in range(1<<(1<<n)):
            maxmono=max((size for fam,size in families
                if ((fam&coloring)==fam or (fam&coloring)==0)),default=0)
            if maxmono<worst:worst=maxmono;witness=coloring
        return worst,witness
    f,wf=guaranteed(closed_both);F,wF=guaranteed(closed_join)
    assert 1<=f<=F<=8 and f>=2
    return {"n":3,"sets":8,"two_colorings":256,
      "families_closed_under_join_and_meet":len(closed_both),
      "families_closed_under_join":len(closed_join),
      "guaranteed_both_closed_f_3":f,"guaranteed_join_closed_F_3":F,
      "worst_colorings_binary_masks":[wf,wF],
      "finite_exact_not_superpolynomial_asymptotic":True}
def main():
    x={"record_type":"EC_BULK_007_FINITE_PHASE_21/1","cohort_id":"EC-BULK-007",
       "mathematical_certification":False}
    for n in range(1176,1184):x[f"problem_{n}"]=globals()[f"p{n}"]()
    x["result"]="FINITE_CHECKS_PASS"
    print(json.dumps(x,indent=2))
if __name__=="__main__":main()
