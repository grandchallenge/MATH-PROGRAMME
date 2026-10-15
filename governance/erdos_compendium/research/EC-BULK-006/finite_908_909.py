#!/usr/bin/env python3
"""Exact finite interfaces, not independent Laczkovich or Anderson–Keisler proof."""
from fractions import Fraction as Q
from itertools import combinations
import json

def step(x): return int(x>=0)

def p908():
    # For any t>0, Δ_t 1_{x>=0}=1 on [-t,0) and 0 outside.
    # Such a step cannot agree a.e. with a continuous function:
    # continuity and a.e. equality on each of the three open intervals
    # (-∞,-t),(-t,0),(0,∞) force incompatible endpoint limits.
    comparisons=0
    for a in range(1,12):
        t=Q(a,3)
        for k in range(-48,49):
            x=Q(k,7)
            exact=step(x+t)-step(x)
            assert exact==int(-t<=x<0),(a,k,x,t)
            comparisons+=1
    # The corrected measurable theorem is compatible: g=f, H=r=0.
    # Exhibit a genuine almost-invariant term differing on one point.
    # r=1_{x=0}; Δ_t r is nonzero only at {0,-t}.
    exceptional=0
    for t in (Q(1,3),Q(1),Q(-2,5)):
        support={Q(0),-t}
        for x in (Q(k,15) for k in range(-45,46)):
            r=lambda u:int(u==0)
            assert r(x+t)-r(x)==0 or x in support
            exceptional+=1
    return dict(function='f(x)=1 if x>=0 else 0',all_positive_rational_shifts_checked=11,
        step_interval_identity_checks=comparisons,
        discontinuity_proof='If a continuous u equals Δ_t f a.e., it equals zero everywhere on (-∞,-t) and (0,∞), and one everywhere on (-t,0); left/right limits at -t contradict continuity.',
        corrected_measurable_decomposition='g=f measurable, H=0, r=0',
        nonzero_residual_example='r=1_{x=0}, each Δ_t r supported on at most two points; a.e. zero',
        finite_residual_checks=exceptional,
        boundary='Explicit analytic counterexample to continuous-g claim; DOES NOT reprove Laczkovich general measurable-g theorem.')

def finite_discrete_cover_verification():
    out=[]
    for m in range(1,5):
        # For a discrete finite S, every cover by arbitrary nonempty subsets
        # is refined by singleton opens of order exactly 1. Its square is also
        # finite discrete; hence both have Lebesgue covering dimension zero.
        nonempty=list(range(1,1<<m))
        covers=0
        for family in range(1<<len(nonempty)):
            union=0
            for i,mask in enumerate(nonempty):
                if family>>i&1:union|=mask
            if union!=(1<<m)-1:continue
            covers+=1
            for i in range(m):
                assert any((family>>j&1) and (subset>>i&1)
                           for j,subset in enumerate(nonempty))
        out.append(dict(points=m,all_possible_cover_families=1<<len(nonempty),
            valid_open_covers=covers,
            canonical_refinement='m singleton open sets; each point belongs to exactly one',
            square_points=m*m,dimension_S=0,dimension_square=0))
    return out

def theorem_arithmetic_interface():
    # External theorem: for each q>=1, exists K subset R^q with dim K^s=q-1
    # for all finite s>=1 and s=omega. Substitute q=n+1 to obtain #909.
    r=[]
    for n in range(1,10):
        q=n+1
        for s in range(1,7):
            assert q-1==n
            r.append(dict(target_dimension=n,ambient_euclidean_dimension=q,
                product_power=s,predicted_dimension=n))
    return dict(formal_substitution_rows=r,
      original_theorem='Anderson–Keisler 1967: K ⊂ R^q, dim(K^s)=q−1 for all finite s and countable omega.',
      exact_deduction='q=n+1 and s=2 yield dim K=dim(K×K)=n',
      interpretation='Topological dimension (inductive/covering for separable metric spaces), not vector-space linear dimension.',
      boundary='Integer parameter algebra only; transfinite construction and dimension inequalities remain external published proof.')
if __name__=='__main__':
 print(json.dumps(dict(record_type='EC_BULK_006_908_909_FINITE/1',
    authority='exact bounded identities; universal mathematical source results imported',
    p908=p908(),p909=dict(discrete=finite_discrete_cover_verification(),
                          theorem_interface=theorem_arithmetic_interface())),
    indent=2,sort_keys=True))
