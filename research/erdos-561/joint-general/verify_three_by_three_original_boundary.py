#!/usr/bin/env python3
"""Exact original 3x3 boundary arithmetic; not an all-host finite proof."""
from itertools import combinations_with_replacement,product
from collections import Counter

def diag(x,y):
 return tuple(max(x[i]+y[j]-1 for i in range(len(x)) for j in range(len(y)) if i+j==k)
              for k in range(len(x)+len(y)-1))
def includes(arms,target):
 a=sorted((v for v in arms if v),reverse=True);t=sorted(target,reverse=True)
 return len(a)>=len(t) and all(x>=y for x,y in zip(a,t))

z=Counter()
for A in range(2,12):
 for B in range(1,A+1):
  for E in range(1,B+1):
   x=(A,B,E)
   for C in range(2,12):
    for D in range(1,C+1):
     for F in range(1,D+1):
      y=(C,D,F)
      W=sum(diag(x,y))
      assert W<=5*(A+C-1)
      if E>=2:
       assert W-sum(diag(tuple(v-1 for v in x),y))==5
       z['red_matching_induction']+=1
      if F>=2:
       assert W-sum(diag(x,tuple(v-1 for v in y)))==5
       z['blue_matching_induction']+=1
      if E==F==1 and B>=D and B>=2:
       reduced=sum(diag((A-1,B-1),y))
       gap=W-reduced
       assert gap==5+max(0,C-max(A,B+D-1))
       z['boundary_subtraction']+=1
      if A+C>=12:
       max_degree=A+C-2
       assert 2*(W-1)<max_degree*(max_degree+1)
       z['large_leader_degree_budget']+=1
      z['original_profiles']+=1

pairs=[]
for a in range(2,10):
 for c in range(2,a+1):
  if a+c<=8 and not (a%2==1 and c%2==1):
   pairs.append((a,c))
assert sorted(pairs)==sorted([(2,2),(3,2),(4,2),(5,2),(6,2),(4,3),(4,4)])

exception=set()
for a in range(2,10):
 for b in range(2,a+1):
  for c in range(2,11):
   for d in range(1,min(b,c)+1):
    if c>max(a,b+d-1) and b>d and a+c-2<=6 and not (a%2 and c%2):
     exception.add((a,b,c,d))
assert exception=={(2,2,3,1),(2,2,4,1),(2,2,5,1),(2,2,6,1),(3,2,4,1),(3,3,4,1)}
for a,c in pairs:
 if (a,c) in [(6,2),(4,3),(4,4)]:
  deg=a+c-2;edges=3*a+c
  assert 2*edges-deg**2+1<a+5
for c in (4,5,6):
 degree=c;E=3*c+4
 hmax=(2*E)//degree
 assert hmax in (7,8) and hmax<2*(degree+1)
 z['vizing_missing_colour']+=1
for a,b,c,d in exception:
 x=(a,b,1);y=(c,d,1)
 W=sum(diag(x,y));D=a+c-2;E=W-1
 assert E==a+3*c+2*b-2
 assert D<=6 and E<=3*D+4
 z['exception_degree_arithmetic']+=1

# Finite complete canonical upper-host checks for explicit ORIGINAL triples,
# corroborating existence of the antidiagonal upper (not graph-wide lower).
cases=[
 ((2,1,1),(2,1,1)),
 ((3,1,1),(2,1,1)),
 ((2,2,1),(3,1,1)),
 ((3,2,1),(3,1,1)),
 ((2,2,2),(2,2,1)),
]
for x,y in cases:
 host=diag(x,y)
 for red in product(*(range(t+1) for t in host)):
  blue=tuple(a-r for a,r in zip(host,red))
  assert includes(red,x) or includes(blue,y),('upper',x,y,red)
  z['original_upper_allocations']+=1
 z['upper_hosts']+=1
assert z['upper_hosts']==5
print('ERDOS561_ORIGINAL_THREE_BY_THREE_ALL_PROFILES',z['original_profiles'])
print('ERDOS561_ORIGINAL_THREE_BY_THREE_FIVE_TERM_INDUCTION',z['red_matching_induction'],z['blue_matching_induction'])
print('ERDOS561_ORIGINAL_THREE_BY_THREE_BOUNDARY_SUBTRACTIONS',z['boundary_subtraction'])
print('ERDOS561_ORIGINAL_THREE_BY_THREE_EXCEPTIONAL_SEVEN_LEADER_PAIRS_PASS')
print('ERDOS561_ORIGINAL_THREE_BY_THREE_SIX_REMNANT_PARAMETERS_PASS')
print('ERDOS561_ORIGINAL_THREE_BY_THREE_VIZING_H_BUDGET_PASS')
print('ERDOS561_ORIGINAL_THREE_BY_THREE_COMPLETE_UPPER_HOSTS',z['upper_hosts'],'ALLOCATIONS',z['original_upper_allocations'])
