#!/usr/bin/env python3
"""Finite symbolic and exact star-host audit for matching-side universality.

No graph-host census is used to infer an unbounded lower bound: that is proved
by vertex-cover degree peeling in MATCHING_DEGREE_PEELING_THEOREM.md.
"""
from itertools import combinations_with_replacement, product
from collections import Counter

def diag_zero(n,m):
    return tuple(max(n[i]+m[j]-1 for i in range(len(n))
                     for j in range(len(m)) if i+j==k)
                 for k in range(len(n)+len(m)-1))
def diag_one(n,m):
    return tuple(max(n[i-1]+m[k-i-1]-1 for i in range(1,len(n)+1)
                     if 1<=k-i<=len(m)) for k in range(2,len(n)+len(m)+1))
def embeds(arms,forest):
    a=sorted((x for x in arms if x>0),reverse=True)
    t=sorted(forest,reverse=True)
    return len(a)>=len(t) and all(x>=y for x,y in zip(a,t))

counts=Counter()
for s in range(3,9):
 for t in range(3,9):
  for comb in combinations_with_replacement(range(1,7),t):
   m=comb[::-1]
   n=(1,)*s
   w=diag_zero(n,m)
   A=diag_zero(n[1:],m)
   B=diag_zero(n,m[1:])
   assert w==diag_one(n,m)
   assert A==diag_one(n[1:],m)
   assert B==diag_one(n,m[1:])
   W=(s-1)*m[0]+sum(m)
   J=(s-2)*m[0]+sum(m)
   assert sum(w)==W and sum(w[1:])==J
   assert tuple(max(a,b) for a,b in zip(A,B))==w[1:]
   assert (w==(m[0],)*s+m[1:])
   assert (w[1:]==(m[0],)*(s-1)+m[1:])
   assert (W-J)==m[0]
   counts['matching_all_profiles']+=1
   if len(set(m[:min(s-1,t)]))>1:counts['non_saturated_prefix']+=1

for s in range(3,7):
 for t in range(3,7):
  for n0 in combinations_with_replacement(range(1,5),s):
   n=n0[::-1]; N=sum(n)
   for m0 in combinations_with_replacement(range(1,5),t):
    m=m0[::-1];M=sum(m)
    w=diag_zero(n,m)
    J=sum(w[1:]); W=sum(w)
    P=max((s-2)*m[0]+M,(t-2)*n[0]+N)
    P_orig=max((s-1)*m[0]+M,(t-1)*n[0]+N)
    assert P<=J and P_orig<=W
    counts['universal_two_sided_pairs']+=1
    if P==J:counts['joint_peeling_exact']+=1

examples=[
 (3,(3,2,1)),
 (3,(4,2,1,1)),
 (4,(3,2,1)),
 (4,(4,2,1,1)),
 (5,(2,1,1)),
 (5,(3,2,1)),
]
for s,m in examples:
 n=(1,)*s; t=len(m)
 h=(m[0],)*(s-1)+m[1:]
 full=(m[0],)*s+m[1:]
 for red in product(*(range(a+1) for a in h)):
  blue=tuple(a-r for a,r in zip(h,red))
  assert embeds(red,n[1:]) or embeds(blue,m),('joint1',s,m,red)
  assert embeds(red,n) or embeds(blue,m[1:]),('joint2',s,m,red)
  counts['joint_upper_arm_colourings']+=1
 for red in product(*(range(a+1) for a in full)):
  blue=tuple(a-r for a,r in zip(full,red))
  assert embeds(red,n) or embeds(blue,m),('original',s,m,red)
  counts['original_upper_arm_colourings']+=1
 counts['complete_profile_pairs']+=1
assert counts['matching_all_profiles']>25000
assert counts['universal_two_sided_pairs']>10000
assert counts['non_saturated_prefix']>0
assert counts['complete_profile_pairs']==6
print('ERDOS561_MATCHING_ALL_PROFILES_EXACT',counts['matching_all_profiles'])
print('ERDOS561_MATCHING_NONSATURATED_PREFIX_CASES',counts['non_saturated_prefix'])
print('ERDOS561_UNIVERSAL_TWO_SIDED_PAIRS',counts['universal_two_sided_pairs'])
print('ERDOS561_JOINT_PEELED_EXACT_INSTANCES',counts['joint_peeling_exact'])
print('ERDOS561_COMPLETE_JOINT_UPPER_ARM_COLOURS',counts['joint_upper_arm_colourings'])
print('ERDOS561_COMPLETE_ORIGINAL_UPPER_ARM_COLOURS',counts['original_upper_arm_colourings'])
