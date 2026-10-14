#!/usr/bin/env python3
"""Exact bounded witnesses for #1085–#1090.

No asymptotic bound, original theorem priority or Lean kernel replay is
claimed. Generic projection is tested in finite dimension 3 only.
"""
import itertools
import json
from fractions import Fraction as F
from math import comb


def squared(a, b):
    return sum((x-y)**2 for x,y in zip(a,b))


def triangles_equal_area():
    pts=[(0,0),(1,0),(1,1),(0,1)]
    areas=[abs((b[0]-a[0])*(c[1]-a[1]) -
               (b[1]-a[1])*(c[0]-a[0]))
           for a,b,c in itertools.combinations(pts,3)]
    assert areas==[1,1,1,1]
    return {"vertices":4,"triangles":4,"twice_area_values":areas,"g_4":4}


def quadruple_repeated():
    square=[(0,0),(1,0),(1,1),(0,1)]
    generic=[(0,0),(2,0),(0,3),(4,5)]
    line=[(0,),(1,),(3,),(6,)]
    def classify(pts):
        edges=[(i,j,squared(pts[i],pts[j])) for i,j in itertools.combinations(range(4),2)]
        equal=[((i,j),(k,l)) for (i,j,d),(k,l,e) in itertools.combinations(edges,2) if d==e]
        return {"six_squared_distances":sorted(d for _,_,d in edges),
                "repeated_pair_pairs":len(equal),
                "shared_endpoint_equal_pairs":sum(bool({i,j}&{k,l}) for (i,j),(k,l) in equal),
                "disjoint_equal_pairs":sum(not bool({i,j}&{k,l}) for (i,j),(k,l) in equal)}
    a,b,c=classify(square),classify(generic),classify(line)
    assert a["six_squared_distances"]==[1,1,1,1,2,2] and a["repeated_pair_pairs"]>0
    assert b["repeated_pair_pairs"]==0
    assert c["six_squared_distances"]==[1,4,9,9,25,36] and c["shared_endpoint_equal_pairs"]>=1
    return {"square":a,"generic":b,"collinear_shared_endpoint":c,
            "original_1971_definition_pending_primary_source":True}


def rainbow_select():
    def rainbow(points, inds):
        ds=[squared(points[i],points[j]) for i,j in itertools.combinations(inds,2)]
        return len(ds)==len(set(ds))
    assert not rainbow([(0,),(1,),(2,)],(0,1,2))
    assert rainbow([(0,),(1,),(3,)],(0,1,2))
    pts=[(0,),(1,),(2,),(3,)]
    hit=[list(x) for x in itertools.combinations(range(4),3) if rainbow(pts,x)]
    assert hit==[[0,1,3],[0,2,3]]
    return {"bad_three_points":[0,1,2],"rainbow_triplets_in_0_1_2_3":hit}


def inverse_limit_finite():
    # This uses only the previously sourced binomial bracket, not a
    # numerical attempt to prove either external theorem.
    rows=[]
    n=3
    for d in (5,20,100,1000):
        lo=comb(d+1,n-1)+1
        hi=comb(d+n-1,n-1)+1
        assert lo<=hi
        rows.append({"d":d,"lower":lo,"upper":hi,
                     "lower_ratio":str(F(lo,d**(n-1))),
                     "upper_ratio":str(F(hi,d**(n-1)))})
    return {"fixed_distance_types_n":n,"target_lim":"1/2","rows":rows}


def projection_check():
    B=list(itertools.product(range(3),repeat=3))
    coeff=((1,7,49),(1,13,169))
    P=[tuple(sum(x[i]*coeff[row][i] for i in range(3)) for row in range(2)) for x in B]
    assert len(set(P))==len(B)==27
    original=projected=spurious=0
    for i,j,k in itertools.combinations(range(len(B)),3):
        a,b,c=B[i],B[j],B[k]
        in3=all((b[u]-a[u])*(c[v]-a[v])==(b[v]-a[v])*(c[u]-a[u])
                for u in range(3) for v in range(u+1,3))
        x,y,z=P[i],P[j],P[k]
        in2=(y[0]-x[0])*(z[1]-x[1])==(y[1]-x[1])*(z[0]-x[0])
        assert not (in3 and not in2)
        original+=in3
        projected+=in2
        spurious+=(in2 and not in3)
    assert original==projected==49 and spurious==0
    return {"alphabet_k":3,"dimension_N":3,"points":27,
            "triples_examined":comb(27,3),"original_collinear_triples":49,
            "projected_collinear_triples":49,"spurious_collinear_triples":0,
            "matrix_rows":list(map(list,coeff)),
            "HJ_min_dimension_threshold_not_tested":True}


def unit_distance():
    square=[(0,0),(1,0),(1,1),(0,1)]
    equal=sum(squared(a,b)==1 for a,b in itertools.combinations(square,2))
    assert equal==4
    return {"unit_square_points":4,"unit_pairs":equal,
            "trivial_equilateral_triangle_f2_3":3}


def main():
    result={"record_type":"EC_BULK_007_FINITE_ARITHMETIC_PHASE_8/1",
            "cohort_id":"EC-BULK-007","mathematical_certification":False,
            "problem_1085":unit_distance(),
            "problem_1086":triangles_equal_area(),
            "problem_1087":quadruple_repeated(),
            "problem_1088":rainbow_select(),
            "problem_1089":inverse_limit_finite(),
            "problem_1090":projection_check(),
            "result":"FINITE_CHECKS_PASS"}
    print(json.dumps(result,indent=2,ensure_ascii=False))


if __name__=="__main__":
    main()
