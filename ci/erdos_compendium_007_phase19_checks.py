#!/usr/bin/env python3
"""Exact finite examples for Erdős 1160–1167. Not asymptotic or ZFC certificates."""
import itertools,json,math
from collections import Counter
from fractions import Fraction as F
from functools import reduce
from math import factorial,gcd,lcm
def perms(n): return list(itertools.permutations(range(n)))
def order(p):
    n=len(p);seen=set();lens=[]
    for i in range(n):
        if i not in seen:
            j=i;length=0
            while j not in seen:
                seen.add(j);length+=1;j=p[j]
            lens.append(length)
    return math.lcm(*lens)
def p1160():
    # Valid small-order reference counts, explicitly an external classification table.
    g={1:1,2:1,3:1,4:2,5:1,6:2,7:1,8:5}
    assert all(g[n]<=g[8] for n in range(1,9))
    return {"order_n_1_to_8_group_counts":g,"highest_power_of_2":8,
            "classification_small_n_from_standard_group_table":True,
            "does_not_prove_all_n_le_2_power_m":True}
def p1161():
    laws={}
    for n in range(1,8):
        h=Counter(order(p) for p in perms(n))
        laws[str(n)]={"permutation_count":sum(h.values()),"modal_orders":sorted(k for k,v in h.items() if v==max(h.values())),
                      "maximum_frequency":max(h.values()),"n_minus_1_factorial":factorial(n-1),
                      "frequency_by_order":dict(sorted(h.items()))}
        assert sum(h.values())==factorial(n)
    return {"exact_S_n_orders":laws,"cannot_infer_asymptotic_eventual_modal_condition_from_n_le_7":True}
def mult(p,q):
    return tuple(p[q[i]] for i in range(len(p)))
def p1162_1163():
    P=perms(3);ident=tuple(range(3));grp=[]
    for mask in range(1<<len(P)):
        members=frozenset(P[i] for i in range(len(P)) if (mask>>i)&1)
        if ident not in members:continue
        if all(mult(a,b) in members for a in members for b in members): grp.append(members)
    assert len(grp)==6
    hist=Counter(len(g) for g in grp);assert dict(hist)=={1:1,2:3,3:1,6:1}
    return {"S3_subgroups_exact":6,"subgroup_order_histogram":dict(sorted(hist.items())),
            "number_of_subgroups_log_base_2_asymptotic_external_only":True,
            "S3_orders_do_not_establish_random_subgroup_statistics":True}
def p1164():
    ds=((1,0),(-1,0),(0,1),(0,-1))
    # Radius-1 Euclidean disc contains origin and four axial neighbors.
    total=0
    for seq in itertools.product(range(4),repeat=7):
        pos=(0,0);seen={pos}
        for j in seq:
            pos=(pos[0]+ds[j][0],pos[1]+ds[j][1]);seen.add(pos)
        if all(q in seen for q in ((1,0),(-1,0),(0,1),(0,-1))):total+=1
    assert total==112  # includes shortest paths between axial neighbours via diagonal sites
    assert all(math.exp(-4*x)>math.exp(-4*y) for x,y in ((0.5,1.0),(1.0,2.0)))
    return {"simple_symmetric_Z2_walk_length":7,"walks":4**7,"unit_disc_covering_walks":total,
            "unit_disc_covering_probability":str(F(total,4**7)),
            "first_possible_cover_time":7,
            "exp_minus_4x_strictly_decreasing_and_not_a_CDF":True,
            "original_limiting_formula_requires_primary_source_correction":True}
def favorite_state(path):
    visits=Counter({(0,0):1});pos=(0,0);fav={pos};union=set(fav);maxv=1
    ds=((1,0),(-1,0),(0,1),(0,-1))
    for k in path:
        d=ds[k];pos=(pos[0]+d[0],pos[1]+d[1]);visits[pos]+=1
        maxv=max(maxv,visits[pos])
        fav={p for p,c in visits.items() if c==maxv};union.update(fav)
    return len(fav),len(union),maxv
def p1165():
    h=Counter()
    for w in itertools.product(range(4),repeat=6):h[favorite_state(w)[0]]+=1
    assert sum(h.values())==4**6
    return {"length":6,"walks":4**6,"last_step_favorite_count_histogram":dict(sorted(h.items())),
           "endpoint_favorite_count_not_infinitely_often_event":True}
def p1166():
    max_union=0;maximum_ratio=F(0)
    for w in itertools.product(range(4),repeat=6):
        num,maxfav,maxv=favorite_state(w)
        max_union=max(max_union,maxfav);maximum_ratio=max(maximum_ratio,F(maxfav,maxv))
    return {"length":6,"walks":4**6,"max_distinct_ever_favorite_locations":max_union,
          "maximum_ratio_distinct_favorites_to_maximum_local_time":str(maximum_ratio),
          "finite_path_not_almost_sure_eventual_polylog_theorem":True}
def p1167():
    # Finite vs infinite cardinal addition, and the one-color size obstruction.
    finite={str(k):k+1 for k in (2,3,5)}
    return {"finite_cardinal_successors":finite,
            "infinite_successor_via_cardinal_addition":"aleph_1 + 1 = aleph_1",
            "one_color_partition_relation":"mu -> (nu)^r_1 iff mu >= nu",
            "unrestricted_gamma_1_counterexample":{
              "lambda":"aleph_0","kappa_0":"aleph_1",
              "premise":"2^aleph_0 >= aleph_1 (holds in ZFC)",
              "conclusion":"aleph_0 >= aleph_1 (false)"},
            "source_formalized_corrected_gamma_at_least_2_kappa_greater_than_r_still_OPEN":True}
def main():
    shared=p1162_1163()
    ans={"record_type":"EC_BULK_007_FINITE_PHASE_19/1",
         "cohort_id":"EC-BULK-007","mathematical_certification":False}
    for n in (1160,1161,1164,1165,1166,1167):ans[f"problem_{n}"]=globals()[f"p{n}"]()
    ans["problem_1162"]=shared
    ans["problem_1163"]=shared
    ans["result"]="FINITE_CHECKS_PASS"
    print(json.dumps(ans,indent=2))
if __name__=="__main__":main()
