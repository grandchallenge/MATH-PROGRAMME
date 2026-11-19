#!/usr/bin/env python3
"""Sharp k<=D+2 obstruction filter for original three-star Ramsey cases.
Proof depends on Lovasz factor and reviewed 3x3 joint residual theorem.
Exact integer verification only, with independent baseline filtering.
"""
from itertools import combinations_with_replacement
from collections import Counter
import json
from pathlib import Path

def weights(n,m):
 return tuple(max(n[i]+m[j]-1 for i in range(3) for j in range(3) if i+j==k)
              for k in range(5))

def evaluate():
 seq=[tuple(reversed(x)) for x in combinations_with_replacement(range(1,10),3) if x[-1]>=2]
 counts=Counter(); newly=[]; remaining=[]; prev_legacy=[]
 for n in seq:
  for m in seq:
   D=n[0]+m[0]-2
   if D>=10:continue
   counts['total']+=1
   E=sum(weights(n,m))-1
   T=D*(D+1)//2
   R=max(sum(n)+3,sum(m)+3)
   B=2*E-D*D+1
   if E<T:
    counts['edge']+=1;continue
   if R>B:
    counts['vertex']+=1;continue
   if R==B and min(sum(n)+3,sum(m)+3)>D+1 and E-T<max(n[0],m[0]):
    counts['previous_extra']+=1;continue
   counts['baseline']+=1
   slack=B-R
   excess=E-T
   previous=(slack==0 and D%2!=0) or (slack==0 and D%2==0 and excess>0) or (slack==1 and D>=3 and excess>0)
   if previous:counts['previous_proved']+=1
   small_core=slack<=2*D-3
   no_clique_parity=(D%2!=0 or (n[0]-1)%2==0 or (m[0]-1)%2==0)
   new=small_core and (no_clique_parity or excess>slack)
   if new:
    counts['new_exclusions']+=1
    if not previous:
     counts['beyond_previous']+=1
     reason='no_parity_obstruction' if no_clique_parity and not excess>slack else 'clique_defeated' if not no_clique_parity else 'both'
     newly.append({'red':n,'blue':m,'D':D,'W':E+1,'slack':slack,'edge_excess':excess,'reason':reason})
   else:
    assert not previous,(n,m,'prior proof exclusion not covered')
    remaining.append({'red':n,'blue':m,'D':D,'W':E+1,'slack':slack,'edge_excess':excess})
 counts['remaining']=len(remaining)
 assert (counts['total'],counts['edge'],counts['vertex'],counts['previous_extra'],counts['baseline'],counts['previous_proved'],counts['new_exclusions'],counts['beyond_previous'],counts['remaining'])==(4566,2725,918,72,851,96,512,416,339),counts
 return {'counts':dict(counts),'new_exclusions_by_degree':dict(Counter(x['D'] for x in newly)),'remaining_by_degree':dict(Counter(x['D'] for x in remaining)),'newly_closed_416':newly,'remaining_339':remaining}
if __name__=='__main__':
 result=evaluate()
 print(json.dumps({k:v for k,v in result.items() if not isinstance(v,list)},indent=2))
 if '--write-json' in __import__('sys').argv:
  Path(__file__).with_name('DPLUS2_PARAMETER_CERTIFICATE.json').write_text(json.dumps(result,indent=2)+'\n')
