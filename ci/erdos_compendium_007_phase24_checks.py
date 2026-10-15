#!/usr/bin/env python3
"""Finite reproducible checks for #1200–1207; no asymptotic theorem certified."""
import itertools,math,json
from fractions import Fraction as Q
def primes_below(n):
 return [x for x in range(2,n) if all(x%d for d in range(2,math.isqrt(x)+1))]
def P(n):
 r=1;d=2
 while d*d<=n:
  while n%d==0:r=d;n//=d
  d+=1
 return max(r,n)
def p1200():
 x=12;ps=primes_below(x);valid=[]
 for v in itertools.product(*(range(-1,p) for p in ps)):
  classes=[(p,a) for p,a in zip(ps,v) if a>=0]
  if all(any(n%p==a for p,a in classes) for n in range(1,x)):
   mass=sum((Q(1,p) for p,a in classes),Q())
   valid.append((mass,classes))
 assert valid
 best=min(valid,key=lambda z:z[0])
 assert best[0]>=1 # union-bound necessity for periodic full coverage does not apply to finite prefix! check carefully below
 return {'x':x,'primes_less_x':ps,'possible_assignments':math.prod(p+1 for p in ps),
  'covering_assignments':len(valid),'minimum_reciprocal_prime_sum':str(best[0]),
  'witness_classes':best[1],
  'finite_prefix_not_coverage_of_all_Z':True}
def p1201():
 results={}
 for n in (30,100,300):
  for k in (0,2,5):
   count=sum(P(math.prod(range(t,t+k+2)))>t**Q(3,5) for t in range(2,n+1))
   results[f'{n},{k}']={'sampled_n_2_to_N':n-1,'threshold_exponent':'3/5','successes':count}
 return {'finite_product_largest_prime_factor_samples':results,
  'epsilon':'2/5','finite_samples_not_density_1_eta':True}
def p1202():
 N=60;ps=[3,5,7];best=None;worst=None
 choices=[list(itertools.combinations(range(p),(p-1)//2)) for p in ps]
 for picked in itertools.product(*choices):
  survivors=[n for n in range(1,N+1) if all(n%p not in A for p,A in zip(ps,picked))]
  if best is None or len(survivors)<best[0]:best=(len(survivors),picked)
  if worst is None or len(survivors)>worst[0]:worst=(len(survivors),picked,survivors)
 return {'N':N,'primes':ps,'removed_residue_counts':[(p-1)//2 for p in ps],
  'assignments_checked':math.prod(len(c) for c in choices),
  'minimum_survivors':best[0],'maximum_survivors':worst[0],
  'max_survivor_residue_witness':worst[1], 'sample_survivors':worst[2],
  'finite_max_survivor_not_arbitrarily_large_k':True}
def omega(n):
 v=0;p=2
 while p*p<=n:
  if n%p==0:
   v+=1
   while n%p==0:n//=p
  p+=1
 return v+(n>1)
def p1203():
 ans={}
 for n in (100,1000,10000):
  vals=[(omega(n+k)*math.log(math.log(k))/math.log(k),k,omega(n+k))
   for k in range(3,101)]
  best=max(vals)
  ans[str(n)]={'k_range':[3,100],'max_F_partial_rounded':round(best[0],12),
   'maximizing_k':best[1],'omega_n_plus_k':best[2]}
 return {'samples':ans,'k_1_undefined_and_k_2_negative_factor':True,
  'finite_k_window_not_global_max_or_divergence':True}
def admissible(A):
 k=len(A)
 return all(len({a%p for a in A})<p for p in primes_below(k+1))
def p1204():
 out={}
 for k in range(2,7):
  valid=[(t[-1],Q(sum(t),k),list(t)) for mid in itertools.combinations(range(1,24),k-1)
   if admissible((0,)+mid) for t in [(0,)+mid]]
  assert valid
  ma=min(valid,key=lambda z:(z[0],z[1]))
  mb=min(valid,key=lambda z:(z[1],z[0]))
  out[str(k)]={'A_k':ma[0],'A_witness':ma[2],
    'B_k':str(mb[1]),'B_witness':mb[2]}
 return {'k_2_to_6_bounded_enumeration':out,
  'search_a_k_at_most_23':True,'small_k_not_asymptotic_k_log_k':True}
def p1205():
 out={}
 for x in range(2,9):
  best=-1;w=None
  for assignments in itertools.product(*(range(n) for n in range(1,x+1))):
   scores=[sum(m%n==a for n,a in enumerate(assignments,1)) for m in range(1,x+1)]
   q=min(scores)
   if q>best:best=q;w=list(assignments)
  out[str(x)]={'max_min_coverage':best,'witness_residue_by_modulus':w,
   'assignments_checked':math.factorial(x)}
 return {'exact_F_x_small':out,'not_proof_log_x_asymptotic':True}
def p1206():
 n=15;a=[i**3 for i in range(1,n+1)]
 def sidon(sub):
  sums=set()
  for i,x in enumerate(sub):
   for y in sub[i:]:
    if x+y in sums:return False
    sums.add(x+y)
  return True
 best=[]
 for mask in range(1<<n):
  if mask.bit_count()<=len(best):continue
  sub=[a[i] for i in range(n) if mask>>i&1]
  if sidon(sub):best=sub
 assert a[0]+a[11]==a[8]+a[9]==1729
 return {'cubes_1_to_N':n,'largest_Sidon_subset_size':len(best),
  'Sidon_witness_cubes':best,'taxicab_collision':'1^3+12^3=9^3+10^3=1729',
  'finite_max_subset_not_linear_in_N':True}
def p1207():
 results={}
 for n in range(5,11):
  triples={tuple(sorted(((a-d)%n,a%n,(a+d)%n)))
   for a in range(n) for d in range(1,n) if len({(a-d)%n,a%n,(a+d)%n})==3}
  best=[]
  for mask in range(1<<n):
   if mask.bit_count()<=len(best):continue
   S={i for i in range(n) if mask>>i&1}
   if all(not set(t).issubset(S) for t in triples):best=sorted(S)
  results[str(n)]={'regular_polygon_max_nonisosceles_vertices':len(best),
   'vertex_indices_witness':best,'three_term_cyclic_ap_count':len(triples)}
 return {'regular_polygon_checks':results,
  'angular_three_term_aps_correspond_to_isosceles_triangles':True,
  'finite_regular_polygon_not_general_planar_extremal_power_saving':True}
def main():
 d={'record_type':'EC_BULK_007_FINITE_PHASE_24/1','cohort_id':'EC-BULK-007',
   'mathematical_certification':False}
 for n in range(1200,1208):d[f'problem_{n}']=globals()[f'p{n}']()
 d['result']='FINITE_CHECKS_PASS'
 print(json.dumps(d,indent=2))
if __name__=='__main__':main()
