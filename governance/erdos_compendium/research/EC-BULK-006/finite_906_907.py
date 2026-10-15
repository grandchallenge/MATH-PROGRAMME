#!/usr/bin/env python3
"""Erdős 906 cofinite-hitting interfaces and Erdős 907 exact difference algebra.
DOES NOT PROVE 906 TRANSCENDENTAL EXISTENCE or replay full 1951 de Bruijn theorem.
"""
import json
from fractions import Fraction
from itertools import product

def periodic_hitting():
    # A periodic set of hits is cofinite iff it is all integers: a missed
    # residue class contributes an infinite avoiding subsequence.
    data=[]
    for period in range(1,10):
        pass_masks=0
        count=0
        for mask in range(1<<period):
            count+=1
            missing=[r for r in range(period) if not(mask>>r&1)]
            if not missing:
                assert mask==(1<<period)-1
                pass_masks+=1
            else:
                witness=missing[0]
                assert all(not(mask>>((witness+k*period)%period)&1) for k in range(1,11))
        assert pass_masks==1
        data.append(dict(period=period,total_hit_patterns=count,
             every_infinite_subsequence_hits_iff_all_residues_hit=True,
             passing_patterns=pass_masks))
    return dict(periodic_cases=data,total_patterns=sum(x['total_hit_patterns'] for x in data),
      mathematical_lemma='For any open U, universal infinite-subsequence density iff all but finitely many derivative orders have a zero in U.',
      polynomial_example='f(z)=z^3, f^(n) identically zero for n>=4, hence zero set all C.',
      exp_counterexample='f(z)=exp(z), no derivative ever has a zero.',
      warning='Periodic finite mock data does not establish existence of a transcendental entire function.')

def add(a,b):
    return a[0]+b[0],a[1]+b[1]
def mul(a,b):
    # a+b sqrt(2) times c+d sqrt(2)
    return a[0]*b[0]+2*a[1]*b[1], a[0]*b[1]+a[1]*b[0]
def neg(a):return -a[0],-a[1]
def g(a):return mul(a,a)
def h(a):return a[1]
def f(a):return add(g(a),(h(a),Fraction(0)))
def subtract(a,b):return add(a,neg(b))
def diff(x,t):return subtract(f(add(x,t)),f(x))
def difference_decomposition():
    # The Q-linear additive map h(a+b sqrt2)=b does not equal c*x on
    # the dense Q-vector subspace Q(sqrt2): h(1)=0, h(sqrt2)=1.
    # It extends to an additive map on R by extending a Hamel basis.
    points=[(Fraction(a,d),Fraction(b,e)) for a,b in product(range(-3,4),repeat=2)
          for d,e in ((1,1),(2,3))]
    increments=[(Fraction(1),Fraction(0)),
       (Fraction(0),Fraction(1)),(Fraction(1,2),Fraction(1,3)),
       (Fraction(-2),Fraction(3))]
    tests=0
    for x in points:
        for t in increments:
            assert diff(x,t)==add(add(mul((Fraction(2),Fraction(0)),mul(x,t)),g(t)),
                      (h(t),Fraction(0)))
            assert h(add(x,t))-h(x)==h(t)
            tests+=1
    mixed=0
    for x in points:
        for t in increments:
            for s in increments:
                dt_s=subtract(diff(add(x,s),t),diff(x,t))
                ds_t=subtract(diff(add(x,t),s),diff(x,s))
                assert dt_s==ds_t
                mixed+=1
    assert h((Fraction(1),Fraction(0)))==0
    assert h((Fraction(0),Fraction(1)))==1
    assert f((Fraction(0),Fraction(0)))==(Fraction(0),Fraction(0))
    return dict(domain='Q(sqrt(2))',function='f(x)=x^2+h(x),h(a+b sqrt2)=b',
        real_extension='Extend h to an additive map on R by Hamel basis, no continuity of h.',
        difference_formula='f(x+t)-f(x)=2*t*x+t^2+h(t)',
        exact_sample_points=len(points),directions=len(increments),
        exact_difference_identity_checks=tests,
        exact_commuting_mixed_differences=mixed,
        h_is_not_scalar_multiple_of_identity=True,
        boundary='An example of the decomposition, NOT independent proof of de Bruijn 1951 universal theorem.')
def main():
    def convert(obj):
        if isinstance(obj,Fraction):
            return str(obj)
        raise TypeError(type(obj))
    print(json.dumps(dict(record_type='EC_BULK_006_906_907_FINITE/1',
        p906=periodic_hitting(),p907=difference_decomposition()),
        indent=2,sort_keys=True,default=convert))
if __name__=='__main__':main()
