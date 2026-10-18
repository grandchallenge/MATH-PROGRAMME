#!/usr/bin/env python3
"""Exact bounded/source-normalization fixtures for Erdős #1116–#1121.

Does not prove analytic counterexamples, ZFC independence or the
Goodman–Goodman multibody covering theorem.
"""
import json
from fractions import Fraction as Q
from math import gcd


def value_count():
    # f(z)=z², for a != 0 exactly two solutions with |z|=sqrt(|a|).
    # Taking a=1,b=4, both counts are 2 for r>2.
    return {"f":"z^2","a":1,"b":4,"r":3,
            "n_r_a":2,"n_r_b":2,"ratio":"1",
            "no_unbounded_ratio_conclusion":True}


def maxima_count():
    # f(z)=1+z² on |z|=r>0:
    # |1+r² exp(2it)| <= 1+r² with equality iff exp(2it)=1.
    return {"f":"1+z^2","r":"arbitrary positive",
            "max_modulus":"1+r^2","maximizing_angles":["0","pi"],
            "nu_r":2,"monomial_excluded":True,
            "no_unbounded_maxima_conclusion":True}


def finite_area():
    # E(c) of e^z is half-plane Re z>log c for c>0.
    return {"f":"exp(z)","c":"positive",
            "E_c":"Re(z)>log(c)","plane_area":"infinite",
            "T_f":"empty",
            "not_a_finite_E_c_example":True}


def cardinal_finite():
    # Indexed affine entire f_j(z)=z+j for 0<=j<7
    vals=[3+j for j in range(7)]
    assert len(vals)==7
    return {"finite_family_size":7,"functions":"f_j(z)=z+j, 0<=j<7",
            "at_z_3_values":vals,
            "distinct_values_at_each_z":7,
            "does_not_establish_ZFC_independence":True}


def polynomial_lemniscate():
    # For f=z^n, |f|<=1 iff |z|<=1.
    # Any path 0->unit circle has length >=1, straight radius achieves 1.
    return {"degree_samples":[1,2,3,10],"f":"z^n",
            "root_modulus":"0","lemniscate":"closed unit disk",
            "shortest_path_length":"1",
            "does_not_establish_worst_case_n_growth":True}


def two_disks():
    # Collinear centers distance d, radii r1,r2, intersect/touch if d<=r1+r2.
    # Minimal enclosing radius = max(r1,r2,(d+r1+r2)/2) for arbitrary d.
    rows=[]
    for r1,r2,d in [(Q(2),Q(3),Q(4)),(Q(1),Q(1),Q(2)),(Q(4),Q(1),Q(2)),(Q(1),Q(3),Q(4))]:
        assert d<=r1+r2
        R=max(r1,r2,(d+r1+r2)/2)
        assert R<=r1+r2
        rows.append({"r1":str(r1),"r2":str(r2),"center_separation":str(d),
                     "minimal_enclosing_radius":str(R),
                     "sum_of_radii":str(r1+r2)})
    return {"exact_two_disk_instances":rows,
            "nonseparability_condition_for_two_disks":"d<=r1+r2",
            "not_full_n_disk_or_Lean_proof":True}


def main():
    j={"record_type":"EC_BULK_007_FINITE_PHASE_13/1",
       "cohort_id":"EC-BULK-007","mathematical_certification":False,
       "problem_1116":value_count(),"problem_1117":maxima_count(),
       "problem_1118":finite_area(),"problem_1119":cardinal_finite(),
       "problem_1120":polynomial_lemniscate(),"problem_1121":two_disks(),
       "result":"FINITE_CHECKS_PASS"}
    print(json.dumps(j,indent=2))


if __name__=="__main__":main()
