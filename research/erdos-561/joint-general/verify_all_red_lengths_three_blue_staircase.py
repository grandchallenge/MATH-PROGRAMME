#!/usr/bin/env python3
"""Independent bounded integer and graph verification; NOT unbounded proof."""
from itertools import product,combinations
from collections import Counter
from functools import lru_cache
N=Counter()
def diag(a,b):
 return tuple(max(x+y-1 for i,x in enumerate(a) for j,y in enumerate(b) if i+j==k) for k in range(len(a)+len(b)-1))
def diag2(a,b):
 return tuple(max(a[i-1]+b[k-i-1]-1 for i in range(1,len(a)+1) if 1<=k-i<=len(b)) for k in range(2,len(a)+len(b)+1))
def J(a,b):return sum(diag(a,b)[1:])
def W(a,b):return sum(diag(a,b))
def A(s,h,r=0):
 return ((2*s-3)*h+1+r,2*(s-3)*h+1+r)+tuple(2*(s-i)*h+1+r for i in range(3,s+1))
def B(L,h,r=0):
 return (2*(L-2)*h+1+r,2*(L-2)*h+1+r)+tuple(2*(L-i)*h+1+r for i in range(3,L+1))
def M(h,k=0):return (4*h+1+k,2*h+1+k,1+k)
def tail_loss(n,m):
 return max(0,m[0]-max(n[-3],n[-2]+m[1]-1))+max(0,m[1]-n[-2])
def embeds(arms,targets):
 z=sorted((v for v in arms if v),reverse=True); t=sorted(targets,reverse=True)
 return len(z)>=len(t) and all(x>=y for x,y in zip(z,t))
for s in range(4,9):
 for h in range(1,5):
  for u in range(1,9):
   for v in range(1,u+1):
    m=(u,v,1)
    for p,q in product(range(3),repeat=2):
     n=tuple(sorted((2*h+4+p,2*h+2+q)+(2*h+1,)*(s-3)+(1,),reverse=True))
     reduced=tuple(z-1 for z in n[:-1])
     assert len(n)==s and n[-2]>=2
     assert diag(n,m)==diag2(n,m)
     assert J(n,m)-(s+1)-J(reduced,m)==tail_loss(n,m)
     N['all_s_tail_identities']+=1
for s in range(3,18):
 for h in range(1,31):
  for r,k in product(range(4),repeat=2):
   n=A(s,h,r);m=M(h,k);x=r+k
   assert len(n)==s and n==tuple(sorted(n,reverse=True))
   assert diag(n,m)==diag2(n,m)
   weights=((2*s+1)*h+1+x,(2*s-1)*h+1+x)+tuple(2*(s+3-j)*h+1+x for j in range(4,s+4))
   assert diag(n,m)==weights
   W0=(s*s+3*s)*h+(s+2)*(1+x)
   J0=(s*s+s-1)*h+(s+1)*(1+x)
   S=(s*s+s-2)*h+(s+1)*(1+x)
   assert W(n,m)==W0 and J(n,m)==J0
   assert W(n[1:],m)==S==W(n,m[1:]) and J0-S==h
   d=n[0]+m[0]-2
   excess=(2*s+1)**2*h*h-(2*s*s+4*s-1)*h-2*(s+2)+((4*s+2)*h-2*s-3)*x+x*x
   assert d==(2*s+1)*h+x and d*(d+1)-2*W0==excess and excess>0
   if r and k:
    assert min(n)>=2 and min(m)>=2
    N['all_positive_arm_cases']+=1
   if s>=4 and not r and not k:
    q=tuple(z-1 for z in n[:-1]);short=A(s-1,h)
    assert tail_loss(n,m)==0 and J(n,m)==(s+1)+J(q,m)
    assert J(q,m)-J(short,m)==(s-1)*(2*h-1)
    assert J(n,m)-J(short,m)==2*s*h+1
    for z in range(2*h):
     t=tuple(v-z for v in q)
     assert min(t)>=1 and sum(t)+(s-1)>=3*(s-1)-1
    N['staircase_inductive_cases']+=1
   N['all_s_family_cases']+=1
for L in range(3,17):
 for h in range(1,23):
  for r,k in product(range(3),repeat=2):
   n=B(L,h,r);m=M(h,k);x=r+k
   assert n==tuple(sorted(n,reverse=True)) and diag(n,m)==diag2(n,m)
   w0=(L*L+3*L)*h+(L+2)*(1+x)
   d=n[0]+m[0]-2
   core=4*L*L*h*h-(2*L*L+4*L)*h-2*(L+2)+(4*L*h-2*L-3)*x+x*x
   assert W(n,m)==w0 and d==2*L*h+x
   assert d*(d+1)-2*w0==core
   if L>=4:assert core>=4
   if L>=4 and not r and not k:
    q=tuple(z-1 for z in n[:-1]);short=B(L-1,h)
    assert tail_loss(n,m)==0 and J(n,m)==(L+1)+J(q,m)
    assert J(q,m)-J(short,m)==L*(2*h-1)
    assert J(n,m)-J(short,m)==2*L*h+1
    N['equal_top_inductive_cases']+=1
   N['equal_top_cases']+=1
def comps(s):
 for k in range(1,s+1):
  def rec(n,m):
   if not m:
    if not n:yield ()
    return
   for x in range(1,n-m+2):
    for t in rec(n-x,m-1):yield (x,)+t
  yield from rec(s,k)
def contains(edges,target):
 adj={}
 for x,y in edges:
  adj.setdefault(x,set()).add(y);adj.setdefault(y,set()).add(x)
 opts=[]
 for a in sorted(target,reverse=True):
  choices=set()
  for c,near in adj.items():
   for leaves in combinations(sorted(near),a):
    choices.add(frozenset((c,)+leaves))
  opts.append(tuple(choices))
 if any(not z for z in opts):return False
 @lru_cache(None)
 def dfs(i,used):
  return i==len(opts) or any(used.isdisjoint(v) and dfs(i+1,used|v) for v in opts[i])
 return dfs(0,frozenset())
for s in range(3,10):
 for p in comps(s):
  size=sum(2*z+1 for z in p)
  assert size<=3*s
  if size-1>=3*s-1:assert p==(1,)*s
  N['factorcritical_partitions']+=1
 E=[(3*i+j,3*i+(j+1)%3) for i in range(s) for j in range(3)]
 red=tuple(e for e in E if e[0]//3<s-1)
 blue=tuple(e for e in E if e[0]//3==s-1)
 assert not contains(red,(2,)*(s-1)+(1,))
 assert not contains(blue,(1,1))
 N['actual_s_triangles_avoiding_colouring']+=1
for s in (3,4):
 n=A(s,1);m=M(1);w=diag(n,m)
 for arms,r,b in ((w,n,m),(w[1:],n[1:],m),(w[1:],n,m[1:])):
  for t in product(*(range(z+1) for z in arms)):
   other=tuple(z-v for z,v in zip(arms,t))
   assert embeds(t,r) or embeds(other,b)
   N['complete_star_host_colour_allocations']+=1
  N['star_host_classes']+=1
assert N['all_s_family_cases']==15*30*16
assert N['equal_top_cases']==14*22*9
assert N['star_host_classes']==6
for key in sorted(N):print('ERDOS561_ALL_S',key,N[key])
print('ERDOS561_ALL_RED_LENGTHS_THREE_BLUE_STAIRCASE_FINITE_PASS')
