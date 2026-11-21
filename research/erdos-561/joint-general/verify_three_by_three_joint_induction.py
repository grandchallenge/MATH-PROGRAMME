#!/usr/bin/env python3
"""Independent deterministic 3x3 joint residual algebra and upper host audits.

Mathematical all-host lower uses the paper matching/Gallai proof. This script
only checks explicit finite arithmetic, the published induction equalities, and
all red-arm allocations for declared canonical joint star hosts.
"""
from itertools import combinations_with_replacement, product
from collections import Counter

def diag0(x,y):
 return tuple(max(x[i]+y[j]-1 for i in range(len(x)) for j in range(len(y)) if i+j==k)
              for k in range(len(x)+len(y)-1))
def diag1(x,y):
 return tuple(max(x[i-1]+y[k-i-1]-1 for i in range(1,len(x)+1) if 1<=k-i<=len(y))
              for k in range(2,len(x)+len(y)+1))
def embeds(arms,tar):
 a=sorted((v for v in arms if v>0),reverse=True)
 tar=sorted(tar,reverse=True)
 return len(a)>=len(tar) and all(p>=q for p,q in zip(a,tar))

counts=Counter(); boundary=set()
for z in combinations_with_replacement(range(1,10),3):
 x=z[::-1]
 for h in combinations_with_replacement(range(1,10),3):
  y=h[::-1];a,b,e=x;c,d,f=y
  w=diag0(x,y)
  assert w==diag1(x,y)
  tail=sum(w[1:])
  assert sum(w)==tail+a+c-1
  A=diag0(x[1:],y);B=diag0(x,y[1:])
  assert A==diag1(x[1:],y) and B==diag1(x,y[1:])
  assert tuple(max(i,j) for i,j in zip(A,B))==w[1:]
  assert tail==max(a+d-1,b+c-1)+max(a+f-1,b+d-1,e+c-1)+max(b+f-1,e+d-1)+(e+f-1)
  if e>=2:
   assert tail-sum(diag0(tuple(v-1 for v in x),y)[1:])==4
   counts['red_matching_induction']+=1
  if f>=2:
   assert tail-sum(diag0(x,tuple(v-1 for v in y))[1:])==4
   counts['blue_matching_induction']+=1
  if e==1 and f==1:
   if b>=d:
    formula=max(a+d-1,b+c-1)+max(a,b+d-1,c)+b+1
    assert formula==tail
    if b>=2:
     t2=sum(diag0((a-1,b-1),y))
     gap=tail+a+c-1-t2
     assert gap==5+max(0,c-max(a,b+d-1))
     if c<=max(a,b+d-1):
      residual_bridge=max(a+d-2,b+c-2)+max(a-1,b+d-2)+b-1
      assert residual_bridge==tail-4
      counts['boundary_bridge']+=1
     else:
      assert tail==2*(b+c)
      assert sum(diag0((b,1),y))==2*(b+c)
      counts['boundary_individual']+=1
  if a>=2 and c>=2 and a+c-2>=10:
   D=a+c-2;W=sum(w)
   assert 2*(W-1)<D*(D+1)
   counts['large_leader_degree_gate']+=1
  counts['triple_pairs']+=1

# Check precisely the six low-leader exceptions obtained in the published
# original-boundary reduction when red second leader dominates blue second.
for a in range(2,11):
 for b in range(2,a+1):
  for c in range(1,13):
   for d in range(1,min(b,c)+1):
    if c>max(a,b+d-1) and b>d and a+c-2<=6 and not (a%2 and c%2):
     boundary.add((a,b,c,d))
expected={(2,2,3,1),(2,2,4,1),(2,2,5,1),(2,2,6,1),(3,2,4,1),(3,3,4,1)}
assert boundary==expected,boundary

for r in range(1,101):
 x=(3*r,r,r);y=(4*r,3*r,r)
 w=diag0(x,y)
 assert w==(7*r-1,6*r-1,5*r-1,4*r-1,2*r-1)
 assert sum(w)==24*r-5 and sum(w[1:])==17*r-4
 assert sum(diag0(x[1:],y))==sum(diag0(x,y[1:]))==16*r-4
 counts['switching_family']+=1

samples=[
 ((2,1,1),(2,1,1)),
 ((3,1,1),(4,3,1)),
 ((3,2,1),(3,2,1)),
 ((4,2,1),(4,3,1)),
 ((2,2,2),(3,2,2)),
 ((3,2,2),(3,1,1))
]
for x,y in samples:
 A=diag0(x[1:],y);B=diag0(x,y[1:])
 host=tuple(max(a,b) for a,b in zip(A,B))
 for red in product(*(range(z+1) for z in host)):
  blue=tuple(z-r for z,r in zip(host,red))
  assert embeds(red,x[1:]) or embeds(blue,y),('R1',x,y,red)
  assert embeds(red,x) or embeds(blue,y[1:]),('R2',x,y,red)
  counts['complete_arm_allocations']+=1
 counts['joint_upper_hosts']+=1

assert counts['triple_pairs']==165*165,counts
assert counts['switching_family']==100
assert counts['joint_upper_hosts']==6
assert counts['boundary_bridge']>0
print('ERDOS561_THREE_BY_THREE_ALL_ORDERED_TRIPLES',counts['triple_pairs'])
print('ERDOS561_THREE_BY_THREE_RED_BLUE_MATCHING_STEPS',counts['red_matching_induction'],counts['blue_matching_induction'])
print('ERDOS561_THREE_BY_THREE_BOUNDARY_BRIDGE',counts['boundary_bridge'])
print('ERDOS561_THREE_BY_THREE_SIX_PUBLIC_BOUNDARY_PROFILES_PASS')
print('ERDOS561_THREE_BY_THREE_LARGE_LEADER_GATE',counts['large_leader_degree_gate'])
print('ERDOS561_THREE_BY_THREE_SWITCHING_FAMILY_100_PASS')
print('ERDOS561_THREE_BY_THREE_JOINT_UPPER_HOSTS',counts['joint_upper_hosts'],'ALLOCATIONS',counts['complete_arm_allocations'])
