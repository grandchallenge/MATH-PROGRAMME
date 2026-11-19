#!/usr/bin/env python3
"""Exact 3x3 integer gate. Independent from the previous D+2 script.
Requires paper-level joint-residual and Lovasz connected-core theorems.
No graph-solver search, floating-point arithmetic, or probabilistic check.
"""
from itertools import combinations_with_replacement
from collections import Counter
import json, hashlib
from pathlib import Path

triples=[]
for a in range(2,10):
 for b in range(1,a+1):
  for c in range(1,b+1):
   triples.append((a,b,c))

index=[]
for x in triples:
 for y in triples:
  d=x[0]+y[0]-2
  if d>=10:continue
  weights=[max(x[i]+y[j]-1 for i in range(3) for j in range(3) if i+j==k)
           for k in range(5)]
  e=sum(weights)-1
  r=max(sum(x)+3,sum(y)+3)
  core_e=d*(d+1)//2
  surplus=e-core_e
  slack=2*e-d*d+1-r
  if e<core_e:continue
  if slack<0:continue
  # old special equality colouring gate
  small=min(sum(x)+3,sum(y)+3)
  if slack==0 and small>d+1 and surplus<max(x[0],y[0]):continue
  index.append((x,y,d,e,r,slack,surplus))
assert len(index)==851,len(index)

new=[];kept=[];old_pass=0;grounds=Counter()
for (x,y,d,e,r,slack,surplus) in index:
  parity=(d%2==0 and x[0]%2==0 and y[0]%2==0)
  low=slack<=2*d-3
  if low and (not parity or surplus>slack):
   old_pass+=1
   continue
  assert old_pass<=512
  # New theorem implies k<=2D+1 unless this degree-excess threshold is hit.
  if slack>=d*d-1:
   kept.append([x,y,d,'very_high_core'])
   grounds['higher_core']+=1
   continue
  if not parity:
   new.append([x,y,d,'no_odd_regular_core'])
   grounds['parity_gate']+=1
   continue
  # An isolated D-regular odd component of size c costs cD/2 edges.
  possible=[]
  for c in range(d+1,2*d+2,2):
   assert d%2==0
   edge_c=c*d//2
   if edge_c>e:continue
   outside=e-edge_c
   if r<=c+outside:
    possible.append(c)
  if possible:
   kept.append([x,y,d,'possible_odd_core',possible]);grounds['possible_odd_core']+=1
  else:
   new.append([x,y,d,'detached_core_avoided']);grounds['detached_core_avoided']+=1

assert old_pass==512,old_pass
assert len(new)==186,(len(new),grounds)
assert len(kept)==153,(len(kept),grounds)
assert old_pass+len(new)+len(kept)==851
new_ids=sorted((tuple(x),tuple(y)) for x,y,*_ in new)
cert={'domain_total':4566,'baseline':851,'old_Dplus2_closed':512,
      'previous_survivors':339,'new_excluded':len(new),'remaining':len(kept),
      'new_reason_counts':dict(grounds),
      'new_by_D':dict(Counter(v[2] for v in new)),
      'remaining_by_D':dict(Counter(v[2] for v in kept)),
      'new_exact_sha256':hashlib.sha256(json.dumps(new_ids,separators=(',',':')).encode()).hexdigest(),
      'new_pairs':new,'remaining_pairs':kept}
print('CERTIFICATE_SUMMARY',json.dumps({k:v for k,v in cert.items() if k not in ('new_pairs','remaining_pairs')},sort_keys=True))
if __name__=='__main__':
 Path(__file__).with_name('GENERAL_CORE_PARAMETER_CERTIFICATE.json').write_text(json.dumps(cert,indent=2)+'\n')
