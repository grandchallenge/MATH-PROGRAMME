#!/usr/bin/env python3
"""Exact bounded examples for Erdős #1122–#1127; no research theorem certification."""
import itertools, json, math
from fractions import Fraction as F

def omega(n):
    p=2; count=0
    while p*p<=n:
        if n%p==0:
            count+=1
            while n%p==0:n//=p
        p+=1
    return count+(n>1)

def additive():
    verified=0
    for a in range(1,51):
        for b in range(1,51):
            if math.gcd(a,b)==1:
                assert omega(a*b)==omega(a)+omega(b)
                verified+=1
    desc=[n for n in range(1,201) if omega(n+1)<omega(n)]
    assert desc
    assert all(math.log(n+1)>math.log(n) for n in range(1,201))
    return {'strongly_additive_example':'omega(n) counts distinct prime factors','coprime_pairs_verified':verified,
            'descents_omega_n_to_omega_n_plus_1_up_to_200':len(desc),'first_descents':desc[:15],
            'log_n_descent_count_up_to_200':0,'finite_counts_not_density_theorem':True}

def density():
    N=10000
    squares={n*n for n in range(1,math.isqrt(N)+1)}
    nat=F(len(squares),N)
    harmonic=sum((F(1,n) for n in range(1,N+1)),F())
    squareharmonic=sum((F(1,n) for n in squares),F())
    assert squareharmonic<harmonic
    return {'cutoff':N,'square_count':len(squares),'natural_density_prefix':str(nat),
            'logarithmic_weight_prefix_less_than_total':True,
            'finite_sums_cannot_certify_any_Boolean_quotient_isomorphism':True}

def circle():
    return {'square_side':1,'square_area':1,
      'equal_area_circle_radius':'1/sqrt(pi)','circle_area_symbolically':1,
      'equal_area_not_finite_translation_equidecomposition_proof':True}

def inequality():
    # For f(x)=a*x+b, inequality reduces to 3*a*h>=0
    xx=[F(-3),F(0),F(1,7),F(10)]
    hs=[F(1,20),F(1),F(7)]
    for a in [F(0),F(1,2),F(3)]:
        for x,h in itertools.product(xx,hs):
            assert 2*a*x <= a*(x+h)+a*(x+2*h)
    assert 2*F(0)*F(0) > -F(3)*F(1) # f(x)=-x fails at x=0,h=1
    return {'affine_f':'a*x+b','valid_for_slopes':'a>=0',
            'exact_rational_nonnegative_slopes_checked':[0,'1/2',3],
            'negative_slope_fails':True,'not_a_general_nonmeasurable_proof':True}

def almost_everywhere():
    # f(x)=2x except f(0)=7. The defect of f(x+y)=f(x)+f(y)
    # is supported on the three null lines x=0,y=0,x+y=0 in R².
    def f(x):return F(7) if x==0 else 2*x
    pts=[F(-3),F(-1),F(0),F(1,2),F(1),F(7)]
    failures=[(str(x),str(y)) for x,y in itertools.product(pts,repeat=2)
              if f(x+y)!=f(x)+f(y)]
    assert failures
    assert all(x=='0' or y=='0' or F(x)+F(y)==0 for x,y in failures)
    return {'f':'2*x except f(0)=7','g':'2*x','defect_supported_on':'three measure-zero affine lines x=0,y=0,x+y=0',
            'exact_finite_grid_failure_count':len(failures),
            'all_failures_lie_on_null_lines':True,
            'illustrates_not_proves_general_stability':True}

def distinct_distances():
    pts=[0,1,3]
    ds=[abs(a-b) for a,b in itertools.combinations(pts,2)]
    assert len(set(ds))==3
    vals=[0,1,2]
    assert len({abs(a-b) for a,b in itertools.combinations(vals,2)})==2
    return {'rainbow_distance_three_point_set':pts,'three_distances':ds,
            'repeated_distance_counterexample_set':vals,
            'finite_example_not_a_countable_partition_of_reals':True,
            'finite_coloring_obstruction_not_by_itself_countable_coloring_obstruction':True}

def main():
    j={'record_type':'EC_BULK_007_FINITE_PHASE_14/1',
       'cohort_id':'EC-BULK-007','mathematical_certification':False,
       'problem_1122':additive(),'problem_1123':density(),
       'problem_1124':circle(),'problem_1125':inequality(),
       'problem_1126':almost_everywhere(),'problem_1127':distinct_distances(),
       'result':'FINITE_CHECKS_PASS'}
    print(json.dumps(j,indent=2))
if __name__=='__main__':main()
