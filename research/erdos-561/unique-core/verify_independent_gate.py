#!/usr/bin/env python3
"""Independent self-contained 3-star integer gate, cross-checking full lists.
No imports from verify_parameter_gate.py or prior filter implementations.
"""
import itertools,json,hashlib
from collections import Counter
from pathlib import Path

all_trip=[p for p in itertools.product(range(1,10),repeat=3)
          if p[0]>=p[1]>=p[2] and p[0]>=2]
assert len(all_trip)==164
base=[];first=[];second=[];last=[]
for u,v in itertools.product(all_trip,repeat=2):
 d=u[0]+v[0]-2
 if d>9:continue
 w=[]
 for k in range(5):
  options=[u[i]+v[k-i]-1 for i in range(3) if 0<=k-i<3]
  w.append(max(options))
 edges=sum(w)-1
 L=max(3+sum(u),3+sum(v))
 t=d*(d+1)//2
 B=2*edges-d*d+1
 if edges<t or L>B:continue
 if L==B and min(sum(u)+3,sum(v)+3)>d+1 and edges-t<max(u[0],v[0]):continue
 base.append((u,v))
 slack=B-L
 parity=(d%2==0 and u[0]%2==0 and v[0]%2==0)
 if slack<=2*d-3 and ((not parity) or edges-t>slack):
  continue
 first.append((u,v))
 if slack>=d*d-1:
  last.append((u,v));continue
 if not parity:
  second.append((u,v));continue
 possible=False
 for c in range(d+1,2*d+2,2):
  spent=c*d//2
  if spent>edges:continue
  h=edges-spent
  leaf=(L>c+h)
  coreRed=(sum(u)+3>c and h<sum(v))
  coreBlue=(sum(v)+3>c and h<sum(u))
  # Minimal outside-edge recolouring: enough to reduce other-colour
  # edge count below target total, without providing enough vertices
  # to the core-colour target.
  rr=max(0,h-sum(v)+1)
  bb=max(0,h-sum(u)+1)
  mixedRed=(c+2*rr<sum(u)+3)
  mixedBlue=(c+2*bb<sum(v)+3)
  if not(leaf or coreRed or coreBlue or mixedRed or mixedBlue):
   possible=True
   break
 if possible:last.append((u,v))
 else:second.append((u,v))

assert len(base)==851,(len(base),len(all_trip))
assert len(first)==339,len(first)
assert len(second)==264,len(second)
assert len(last)==75,len(last)
prior=json.load(open(Path(__file__).with_name('GENERAL_CORE_PARAMETER_CERTIFICATE.json')))
main_new={(tuple(p[0]),tuple(p[1])) for p in prior['new_pairs']}
main_last={(tuple(p[0]),tuple(p[1])) for p in prior['remaining_pairs']}
assert set(second)==main_new,(len(set(second)^main_new))
assert set(last)==main_last,(len(set(last)^main_last))
print('INDEPENDENT_FULL_LIST_PASS',json.dumps({'initial':len(base),'previous':len(first),
 'new_exclusions':len(second),'remaining':len(last),
 'new_by_D':dict(Counter(u[0]+v[0]-2 for u,v in second)),
 'remaining_by_D':dict(Counter(u[0]+v[0]-2 for u,v in last))},sort_keys=True))
