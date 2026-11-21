#!/usr/bin/env python3
"""Independent finite checks of saturated matching/star residual theorems.

The all-finite-simple-host lower proof is in SATURATED_MATCHING_JOINT_THEOREM.md;
the parameter grid is corroboration, not an unrestricted-host proof by sampling.
"""
from itertools import combinations_with_replacement,product
from collections import Counter

def diag0(n,m):
    return tuple(max(n[i]+m[j]-1 for i in range(len(n)) for j in range(len(m)) if i+j==z)
                 for z in range(len(n)+len(m)-1))
def diag1(n,m):
    return tuple(max(n[i-1]+m[z-i-1]-1 for i in range(1,len(n)+1) if 1<=z-i<=len(m))
                 for z in range(2,len(n)+len(m)+1))
def includes(arms,target):
    a=sorted((x for x in arms if x>0),reverse=True)
    t=sorted(target,reverse=True)
    return len(a)>=len(t) and all(x>=y for x,y in zip(a,t))
count=Counter()
for s in range(3,8):
 for t in range(max(3,s-1),9):
  for item in combinations_with_replacement(range(1,7),t):
   m=item[::-1];n=(1,)*s;M=sum(m)
   w=diag0(n,m);w1=diag1(n,m)
   A=diag0(n[1:],m);B=diag0(n,m[1:])
   assert w==w1 and A==diag1(n[1:],m) and B==diag1(n,m[1:])
   canon=tuple(max(x,y) for x,y in zip(A,B))
   J=sum(w[1:])
   assert canon==(m[0],)*(s-1)+m[1:] and J==sum(canon)
   lower=m[0]+M+sum(m[2:s-1])
   assert lower<=J
   count['general']+=1
   if lower==J:count['bound_exact']+=1
   if all(x==m[0] for x in m[:s-1]):
    assert lower==J==(2*s-3)*m[0]+sum(m[s-1:])
    assert sum(w)==(2*s-2)*m[0]+sum(m[s-1:])
    count['saturated_exact']+=1
cases=[
 (3,(3,2,1)),(3,(3,3,2,1)),(4,(2,2,2,1)),
 (4,(3,3,3,2,1)),(5,(2,2,2,2,1)),
 (5,(3,3,3,3,1,1)),(6,(2,2,2,2,2,1)),
]
for s,m in cases:
 n=(1,)*s
 h=(m[0],)*(s-1)+m[1:]
 assert len(h)==s+len(m)-2
 for red in product(*(range(x+1) for x in h)):
  blue=tuple(x-y for x,y in zip(h,red))
  assert includes(red,n[1:]) or includes(blue,m),('R1',s,m,red)
  assert includes(red,n) or includes(blue,m[1:]),('R2',s,m,red)
  count['complete_arm_colours']+=1
 count['upper_hosts']+=1
original_examples=[
 (3,(2,2,1)),(4,(2,2,2,1)),(5,(2,2,2,2,1))
]
for s,m in original_examples:
 n=(1,)*s
 full=(m[0],)*s+m[1:]
 assert len(full)==s+len(m)-1
 for red in product(*(range(x+1) for x in full)):
  blue=tuple(x-y for x,y in zip(full,red))
  assert includes(red,n) or includes(blue,m),('original',s,m,red)
  count['original_upper_arm_colours']+=1
 count['original_upper_hosts']+=1
assert count==Counter({'general':14203,'bound_exact':4651,
                       'saturated_exact':3385,'complete_arm_colours':116386,
                       'upper_hosts':7,'original_upper_hosts':3,
                       'original_upper_arm_colours':14742}),count
print('ERDOS561_MATCHING_GENERAL_14203_PARAMETER_GRID_PASS')
print('ERDOS561_MATCHING_SATURATED_EXACT_3385_PARAMETER_GRID_PASS')
print('ERDOS561_MATCHING_COMPLETE_UPPER_HOSTS_7_PASS')
print('ERDOS561_MATCHING_COMPLETE_ARM_COLOURS_116386_PASS')
print('ERDOS561_MATCHING_ORIGINAL_3_HOSTS_14742_ARM_COLOURS_PASS')
