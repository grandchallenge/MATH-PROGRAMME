#!/usr/bin/env python3
"""Independent exact integer audit of the new full-graph lower bound,
its symmetric form, known star-host upper bounds and equality families.
No prior (partially proved) size-Ramsey formulas imported.
"""
import itertools,json
from collections import Counter
from pathlib import Path

def W(n,m):
 out=[]
 for d in range(2,len(n)+len(m)+1):
  h=[n[i]+m[j]-1 for i in range(len(n)) for j in range(len(m)) if i+j==d-2]
  assert h
  out.append(max(h))
 return out

def J(n,m):return sum(W(n,m)[1:])

def lower(n,m):
 s,t=len(n),len(m);N=sum(n);M=sum(m)
 R=max(N+sum(m[:t-2]),M+sum(n[:s-2]))
 if t>=4:R=max(R,2*m[0]+N+(t-4)*n[0])
 if s>=4:R=max(R,2*n[0]+M+(s-4)*m[0])
 return R

def sorted_sequences(length,limit):
 for q in itertools.combinations_with_replacement(range(1,limit+1),length):
  yield q[::-1]

stats=Counter();examples=[]
for s,t in ((3,3),(3,4),(3,5),(3,6),(4,4),(4,5),(5,5),(5,6)):
 for n in sorted_sequences(s,4):
  for m in sorted_sequences(t,4):
   v=J(n,m);lb=lower(n,m)
   assert lb<=v,(n,m,lb,v)
   stats['all_cases']+=1
   if lb==v:stats['equality_cases']+=1
   if t>=4 and 2*m[0]+sum(n)+(t-4)*n[0]==v:
    stats['first_peeling_sharp_cases']+=1

# Exact infinite C1 family checked on broad, but finite integer,
# samples independently of the unbounded manuscript proof.
for t in range(4,12):
 for a in range(1,23):
  for c in range(1,a+1):
   for b in (a+c-1,a+c,a+c+3):
    n=(a,1,1);m=(b,c)+tuple(1 for _ in range(t-2))
    v=2*b+(t-3)*a+2
    assert J(n,m)==v
    assert lower(n,m)==v
    stats['C1_exact_examples']+=1
    A=sum(W(n[1:],m));B=sum(W(n,m[1:]))
    sig=v-max(A,B)
    assert sig==min((t-3)*(a-1)-(c-1),2*(b-a)-c+1)
    assert sig>=0

for s in range(3,12):
 for t in range(3,12):
  for a in range(1,25):
   n=(a,)+tuple([1]*(s-1));m=(a,)+tuple([1]*(t-1))
   v=(max(s,t)-1)*a+min(s,t)-1
   assert J(n,m)==v
   assert lower(n,m)==v
   stats['C2_exact_examples']+=1

for r in range(1,200):
 n=(2*r,1,1);m=(3*r,r,1,1)
 v=J(n,m)
 left=sum(W(n[1:],m));right=sum(W(n,m[1:]))
 assert (v,left,right,v-max(left,right))==(8*r+2,7*r+2,7*r+1,r)
 stats['unbounded_switch_exact_examples']+=1

out={'record_type':'ERDOS561_ITERATED_PEELING_PARAMETER_AUDIT/1',**stats,
     'sample_new_theorem_unresolved_case':{'red':[3,2,1],'blue':[4,1,1,1],
       'conjectured_joint_J':J((3,2,1),(4,1,1,1)),
       'proved_elementary_lower_bound':lower((3,2,1),(4,1,1,1))},
     'proof_is_unbounded':False,'role':'finite arithmetic corroboration; mathematical proof separate'}
Path(__file__).with_name('UNBOUNDED_FAMILY_PARAMETER_CERTIFICATE.json').write_text(json.dumps(out,indent=2)+'\n')
print('UNBOUNDED_FAMILY_INTEGER_AUDIT_PASS',json.dumps(out,sort_keys=True))
