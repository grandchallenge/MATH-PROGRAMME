#!/usr/bin/env python3
"""Exact finite illustrations for #1208-1218. These do not certify general theorems."""
import itertools,math,json
from fractions import Fraction
from collections import Counter,deque
def prime(n):
 return n>=2 and all(n%d for d in range(2,math.isqrt(n)+1))
def distinct_pair_differences(points):
 return [sum((a-b)**2 for a,b in zip(p,q)) for p,q in itertools.combinations(points,2)]
def p1208():
 # In a 3x3 planar grid look for the largest subset with ALL pairwise distances unique.
 grid=list(itertools.product(range(3),repeat=2));best=[];cnt=0
 for mask in range(1<<len(grid)):
  S=[grid[i] for i in range(len(grid)) if mask>>i&1]
  vals=distinct_pair_differences(S)
  if len(vals)==len(set(vals)):
   cnt+=1
   if len(S)>len(best):best=S
 assert len(best)>=3
 return {'grid':'3x3 integer planar grid','subsets_checked':512,
  'distance_distinct_subsets':cnt,'maximum_subsets_all_pairwise_distances_distinct':len(best),
  'witness_points':best,'dimension':2,'not_extremal_all_n':True}
def p1209():
 out=[]
 for k in range(1,8):
  q=next(p for p in range(2,100) if prime(p) and k%p)
  a=next(p for p in range(max(3,(out[-1]['a']+1) if out else 3),30000)
   if prime(p) and (p+k)%q==0 and p+k>q)
  out.append({'k':k,'a':a,'q':q,'a_plus_k_divisible_q':(a+k)%q==0})
 assert all(x['a_plus_k_divisible_q'] for x in out)
 return {'diagonal_prime_sequence_prefix':out,
  'each_positive_shift_n_equals_k_obstructed_at_index_k':True,
  'infinite_sequence_uses_Dirichlet_not_finite_primality':True}
def p1210():
 ans={}
 for n in range(5,15):
  best=(Fraction(-1),[])
  for mask in range(1<<(n-1)):
   A=[i+1 for i in range(n-1) if mask>>i&1]
   if all(math.gcd(a,b)==1 for a,b in itertools.combinations(A,2)):
    s=sum((Fraction(1,n-a) for a in A),Fraction())
    if s>best[0]:best=(s,A)
  ans[str(n)]={'best_sum':str(best[0]),'witness':best[1]}
 return {'exact_max_over_pairwise_coprime_A_subset_1_to_n_minus_1':ans,
  'not_uniform_prime_reciprocal_plus_O_1':True}
def p1211():
 N=30;A=[n for n in range(1,N+1) if n%2];B=[n for n in range(1,N+1) if not n%2]
 def subset_sums(xs):
  S={0}
  for a in xs:S|={a+s for s in list(S) if a+s<=N}
  return sorted(S-{0})
 SA=subset_sums(A);SB=subset_sums(B)
 assert all(t%2==0 for t in SB) and 1 in SA and 3 in SA
 return {'finite_partition_N':N,'A':'odds','B':'evens',
  'subset_sums_A_below_31_count':len(SA),
  'subset_sums_B_below_31_count':len(SB),
  'published_exact_c':'(2+sqrt(3))/4',
  'finite_partition_not_upper_logarithmic_density':True}
def p1212():
 V={(x,y) for x in range(2,18) for y in range(2,18)
    if math.gcd(x,y)==1 and (not prime(x) or not prime(y))}
 start=(4,3);assert start in V
 seen={start};Q=deque([start])
 while Q:
  x,y=Q.popleft()
  for z in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
   if z in V and z not in seen:seen.add(z);Q.append(z)
 return {'box':'2..17 squared','allowed_vertices':len(V),'seed':[4,3],
  'finite_reachable_vertices':len(seen),'max_x_reached':max(x for x,y in seen),
  'max_y_reached':max(y for x,y in seen),
  'finite_graph_not_infinite_path':True}
def p1213():
 seq=[2,3,4,5]
 sums={}
 for i in range(len(seq)):
  for j in range(i+1,len(seq)+1):
   v=sum(seq[i:j]);sums.setdefault(v,[]).append([i,j])
 assert [0,2] in sums[5] and [3,4] in sums[5]
 return {'a':2,'K':1,'sequence':seq,'two_distinct_disjoint_intervals':[[0,2],[3,4]],
  'common_sum':5,'finite_example_not_exp_K_theorem':True}
def pf(n):
 return [p for p in range(2,n+1) if prime(p) and n%p==0]
def p1214():
 return {'x':2,'y':3,'prime_supports_x_n_minus_1':
  [pf(2**n-1) for n in range(1,7)],
  'prime_supports_y_n_minus_1':[pf(3**n-1) for n in range(1,7)],
  'first_n_distinguishing':1,
  'x_eq_1_has_x_n_minus_1_zero_prime_support_undefined_without_convention':True}
def p1215():
 # P(z)=1-z; |P(0)|=1 so the interior strict sublevel excludes start.
 import cmath
 vals={str(i):abs(1-i/10) for i in range(11)}
 assert vals['0']==1 and vals['10']==0
 return {'polynomial':'P(z)=1-z','P_0':1,'strict_sublevel_omits_z_0':True,
  'real_segment_0_to_1_moduli':vals,
  'path_from_boundary_in_relative_closure_interpretation_required':True,
  'finite_example_not_global_length_bound':True}
def p1216():
 def min_max_transitive(n):
  E=list(itertools.combinations(range(n),2)); worst=n;example=None
  for bits in range(1<<len(E)):
   adj={(a,b) if bits>>i&1 else (b,a) for i,(a,b) in enumerate(E)}
   mx=1
   for mask in range(1,1<<n):
    S=[i for i in range(n) if mask>>i&1]
    if len(S)<=mx:continue
    # transitive tournament iff no directed triangle
    if all(not(((a,b) in adj and (b,c) in adj and (c,a) in adj)
               or ((b,a) in adj and (c,b) in adj and (a,c) in adj))
       for a,b,c in itertools.combinations(S,3)):mx=len(S)
   if mx<worst:worst=mx;example=bits
  return {'n':n,'tournaments_checked':1<<len(E),'guaranteed_transitive_subtournament':worst,
          'worst_tournament_bitmask':example}
 return {'exact_small_n':[min_max_transitive(n) for n in range(3,6)],
  'all_n_lower_original_false_beyond_14_external_Reid_Parker':True}
def p1217():
 A=[2,4,8,16,32]
 assert all(A[i+1]%A[i]==0 for i in range(len(A)-1))
 return {'finite_divisibility_chain':A,'chain_members':5,
  'reciprocal_log_weights_approx':round(sum(1/(a*math.log(a)) for a in A),12),
  'not_infinite_lower_logarithmic_density_theorem':True}
def p1218():
 # Count number of 3-edges on five vertices and distinguish ordinal
 # beta from cardinal aleph_beta, and countably many other colors.
 return {'finite_vertex_count':5,'unordered_triples':math.comb(5,3),
  'color_palette_countably_infinite_in_the_question':True,
  'GCH_is_hypothesis':True,
  'beta':'omega_(omega+1)','first_target':'aleph_beta',
  'ambient':'aleph_(beta+1)','finite_triple_count_not_set_theory_certificate':True}
def main():
 d={'record_type':'EC_BULK_007_FINITE_PHASE_25/1','cohort_id':'EC-BULK-007',
  'mathematical_certification':False}
 for n in range(1208,1219):d[f'problem_{n}']=globals()[f'p{n}']()
 d['result']='FINITE_CHECKS_PASS'
 print(json.dumps(d,indent=2))
if __name__=='__main__':main()
