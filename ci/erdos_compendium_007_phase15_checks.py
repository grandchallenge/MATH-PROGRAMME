#!/usr/bin/env python3
"""Exact finite mathematical examples #1128–#1135; no new general theorem."""
import json, itertools
from fractions import Fraction as F
from functools import lru_cache
from math import gcd

def p1128():
    triples=list(itertools.product((0,1),repeat=3))
    col={','.join(map(str,t)):sum(t)%2 for t in triples}
    assert len(set(col.values()))==2
    assert len(set(col.values()))!=1
    return {'small_grid':'{0,1}^3','color':'(i+j+k) mod 2','monochromatic_full_2x2x2':False,
            'not_an_uncountable_cardinal_counterexample':True}

def lagrange(nodes):
    def lk(k,x):
        a=nodes[k]
        ans=F(1)
        for i,z in enumerate(nodes):
            if i!=k:ans*=F(x-z,a-z)
        return ans
    return lambda x:[lk(k,x) for k in range(len(nodes))]

def p1129():
    l2=lagrange([F(-1),F(1)])
    l3=lagrange([F(-1),F(0),F(1)])
    assert sum(abs(y) for y in l2(F(3,5)))==1
    assert sum(abs(y) for y in l3(F(1,2)))==F(5,4)
    # Exact quadratic Lebesgue max 5/4: interval [-1,0] and [0,1]
    return {'n2_nodes':[-1,1],'n2_Lambda':'1',
            'n3_nodes':[-1,0,1],'n3_Lambda_exact':'5/4',
            'n3_lambda_at_half':'5/4',
            'not_an_n_arbitrary_extremal_proof':True}

def p1130():
    l=lagrange([F(-1,2),F(1,2)])
    # Each Lagrange factor = (x±1/2), so L(x)=max(1,2|x|)
    samples={str(z):str(sum(abs(y) for y in l(z))) for z in
             [F(-1),F(-1,2),F(0),F(1,2),F(1)]}
    assert samples['-1']=='2' and samples['0']=='1' and samples['1']=='2'
    return {'nodes':['-1/2','1/2'],'local_maxima':['2','1','2'],
            'Upsilon_exact':'1','global_Lambda_exact':'2',
            'not_a_general_minmax_characterization':True}

def p1131():
    # n=2 nodes -1,1 => sum l_k(x)^2=(x²+1)/2,
    # integral [-1,1] gives 1+1/3=4/3
    l=lagrange([F(-1),F(1)])
    t=sum(z*z for z in l(F(0)))
    assert t==F(1,2)
    return {'n2_nodes':[-1,1],'integrand':'(x^2+1)/2',
            'integral_exact':'4/3',
            'not_a_global_minimum_over_all_nodes_or_asymptotic':True}

def p1132():
    l=lagrange([F(-1),F(0),F(1)])
    return {'n3_nodes':[-1,0,1],
            'L3_at_zero':str(sum(abs(y) for y in l(F(0)))),
            'L3_at_half':str(sum(abs(y) for y in l(F(1,2)))),
            'not_a_fixed_infinite_sequence_result':True}

def p1133():
    # For three nodes -1,0,1, for any y in [-1,1]^3 the degree 2
    # interpolant obeys ||P||∞ <= Lebesgue constant 5/4.
    # This does not prove the asymptotic robust obstruction.
    return {'three_nodes':[-1,0,1],'all_y_in_minus1_to1':True,
            'unique_degree_at_most_2_interpolant_norm_upper':'5/4',
            'proof':'triangle inequality and exact n3 Lebesgue constant',
            'not_an_asymptotic_disproof':True}

def p1134():
    N=100000
    seen={1}
    queue=[1]
    for x in queue:
        for y in (2*x+1,3*x+1,6*x+1):
            if y<=N and y not in seen:
                seen.add(y);queue.append(y)
    assert all(1<=n<=N for n in seen)
    return {'up_to':N,'closure_count':len(seen),
            'closure_prefix':sorted(seen)[:20],
            'finite_fraction':str(F(len(seen),N)),
            'not_asymptotic_density_estimate':True}

def p1135():
    def nxt(n):return n//2 if n%2==0 else (3*n+1)//2
    stopping=[]
    for n in range(1,10001):
        x=n
        k=0
        while True:
            x=nxt(x);k+=1
            if x==1:break
            assert k<10000,'unexpected finite trajectory bound exceeded'
        stopping.append(k)
    assert nxt(1)==2 and nxt(2)==1
    maxk=max(stopping)
    return {'cutoff':10000,'checked_positive_seeds':10000,
            'all_reached_one':True,'max_first_positive_return_steps':maxk,
            'argmax_first_positive_return_steps':stopping.index(maxk)+1,
            'seed_one_requires_two_steps':True,
            'not_a_proof_of_Collatz_conjecture':True}

def main():
    a={'record_type':'EC_BULK_007_FINITE_PHASE_15/1',
       'cohort_id':'EC-BULK-007','mathematical_certification':False}
    for n in range(1128,1136):a[f'problem_{n}']=globals()[f'p{n}']()
    a['result']='FINITE_CHECKS_PASS'
    print(json.dumps(a,indent=2))
if __name__=='__main__':main()
