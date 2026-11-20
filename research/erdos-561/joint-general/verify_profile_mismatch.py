#!/usr/bin/env python3
"""Exact integer crosscheck for the general profile-mismatch theorem and
sharp two-parameter family. Finite checking is not the unbounded proof.
"""
from itertools import combinations_with_replacement
from collections import Counter
import json
from pathlib import Path

def W(n,m):
    return [max(n[i]+m[j]-1 for i in range(len(n)) for j in range(len(m)) if i+j==z)
            for z in range(len(n)+len(m)-1)]

def sumJ(n,m):return sum(W(n,m)[1:])

def profiles(length,limit):
    return (tuple(p[::-1]) for p in combinations_with_replacement(range(1,limit+1),length))

stats=Counter();extrema=[]
for s,t in [(3,4),(3,5),(4,4),(4,5),(5,4),(5,5)]:
 for n in profiles(s,5):
  N=sum(n)
  for m in profiles(t,5):
   if sum(m[1:])!=N:continue
   if sorted(n)==sorted(m[1:]):continue
   b=m[0];J=sumJ(n,m)
   stats['profile_mismatch_eligible']+=1
   assert J>=2*b+N+1,(s,t,n,m,J,2*b+N+1)
   stats['sharp']+=(J==2*b+N+1)
   if J==2*b+N+1 and len(extrema)<6:extrema.append((n,m,J))
for a in range(3,40):
 for b in range(2*a-2,2*a+20):
  n=(a,1,1);m=(b,a-1,2,1)
  w=W(n,m)
  assert w[1:]==[b,b,a,2,1],(a,b,w)
  assert sumJ(n,m)==2*b+a+3
  assert sum(m[1:])==sum(n)
  assert tuple(sorted(n))!=tuple(sorted(m[1:]))
  stats['sharp_infinite_family_checks']+=1
for b in range(4,400):
 n=(3,1,1);m=(b,2,2,1)
 assert sumJ(n,m)==2*b+6
 stats['original_case_parameter_checks']+=1
print('PROFILE_MISMATCH_PARAMETER_REPLAY_PASS',dict(stats),'examples',extrema)
Path(__file__).with_name('PROFILE_MISMATCH_PARAMETER_CERTIFICATE.json').write_text(json.dumps({
 'record_type':'ERDOS561_JOINT_PROFILE_MISMATCH_ARITHMETIC_REPLAY/1',
 'finite_parameter_counts':dict(stats),'sample_other_sharp_profiles':extrema,
 'proof_is_the_general_paper_argument':False,
 'satisfies_general_j_lower_bound':True,
 'not_global_conjecture_solution':True},indent=2)+'\n')
