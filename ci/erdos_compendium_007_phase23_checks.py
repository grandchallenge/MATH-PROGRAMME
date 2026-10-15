#!/usr/bin/env python3
"""Deterministic finite fixtures for Erdős 1192–1199, without infinite proof claims."""
from collections import Counter
from fractions import Fraction
from itertools import combinations, combinations_with_replacement
from math import log, isqrt
import json

def p1192():
    A=[1,2,4,8]
    reps=Counter(a+b for a in A for b in A)
    assert sum(reps.values())==16
    return {"set_A":A,"ordered_pair_count":16,
            "f2_by_sum":dict(sorted(reps.items())),
            "sum_f2_squared":sum(x*x for x in reps.values()),
            "not_a_basis_of_order_2":True,
            "finite_moment_not_uniform_O_x_or_eventual_positive_representations":True}

def p1193():
    counts={str(n):n+1 for n in range(0,21)}
    for n in range(21):
        assert sum(1 for a in range(n+1) if (n-a)>=0)==n+1
    return {"N_0_nonnegative_integers":"A={0,1,2,...}",
            "g_n":"n+1","exact_n0_to_20":counts,
            "agreement_density":1,
            "positive_integer_convention_alternative":"A={1,2,...}, f(n)=n-1 for all n>=2",
            "literal_unrestricted_statement_false":True}

def p1194():
    A=[0,1,4,6]
    diffs={}
    for a,b in combinations(A,2):
        d=b-a
        assert d not in diffs
        diffs[d]=[b,a]
    assert sorted(diffs)==list(range(1,7))
    sums=[a+b for a,b in combinations_with_replacement(A,2)]
    assert len(sums)==len(set(sums))
    return {"finite_perfect_difference_ruler":A,
            "unique_positive_differences_1_through_6":diffs,
            "all_unordered_pair_sums_unique":True,
            "finite_graceful_ruler_not_infinite_perfect_difference_set":True}

def p1195():
    S=(Fraction(1,1),Fraction(7,5))
    # Within this interval no ratio between distinct points can equal an integer >=2.
    assert S[1]/S[0]<2
    return {"finite_measure_example":"S=(1,7/5)",
            "measure":"2/5",
            "integer_ratio_impossible_for_distinct_points_inside_interval":True,
            "growth_function_F_sqrt_x_integrable":r"integral_1^infty x^(-3/2)dx = 2",
            "growth_function_F_x_over_log_x_not_integrable":r"integral_e^infty dx/(x log x) diverges",
            "no_infinite_measure_construction_claimed":True}

def p1196():
    A=[2,3,5,7,11]
    assert all(not(b%a==0) for a,b in combinations(A,2))
    approximate=sum(1/(x*log(x)) for x in A)
    return {"primitive_set_of_primes":A,"primitive":True,
            "finite_reciprocal_log_sum_approx":round(approximate,12),
            "sum_cannot_establish_universal_tail_asymptotic":True}

def p1197():
    # For E=(1,2) and x=3/2, n=4, r=4 yields nx/r=3/2 in E.
    x=Fraction(3,2);n=4;r=4
    assert 1 < n*x/r < 2
    return {"E":"(1,2)","x":"3/2","n":4,"r":4,
            "nx_over_r":"3/2","r_window_at_x_n":"(3,6)",
            "for_any_fixed_x_positivity_eventual_window_length":"nx/2 grows without bound",
            "open_interval_positive_measure_case_does_not_cover_general_measurable_sets":True}

def p1198():
    A=(2,3,5)
    basic_sum=2+3
    basic_product=2*3
    disjoint_product_sum=2*3+5
    assert (basic_sum,basic_product,disjoint_product_sum)==(5,6,11)
    return {"finite_A":list(A),"two_singletons_sum":basic_sum,
            "one_nonsingleton_product":basic_product,
            "disjoint_blocks_product_plus_singleton":disjoint_product_sum,
            "nontrivial_product_sum_expressions_not_just_finite_sums":True,
            "finite_values_do_not_disprove_hindman_or_prove_smith_global_coloring":True}

def p1199():
    A=[1,3,5,7]
    sums={a+b for a,b in combinations_with_replacement(A,2)}
    assert sums=={2,4,6,8,10,12,14}
    diagonals=[2*a for a in A]
    assert set(diagonals).issubset(sums)
    return {"finite_A_all_odd":A,
            "sumset_including_diagonals":sorted(sums),
            "diagonal_sums":diagonals,
            "all_sums_even_for_parity_coloring":True,
            "finite_parity_example_not_every_two_coloring_theorem":True}

def main():
    d={"record_type":"EC_BULK_007_FINITE_PHASE_23/1",
       "cohort_id":"EC-BULK-007","mathematical_certification":False}
    for n in range(1192,1200):d[f"problem_{n}"]=globals()[f"p{n}"]()
    d["result"]="FINITE_CHECKS_PASS"
    print(json.dumps(d,indent=2))
if __name__=="__main__":main()
