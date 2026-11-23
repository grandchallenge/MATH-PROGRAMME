#!/usr/bin/env python3
"""Finite exact tests for all-s single BLUE matching theorem; not a full-host proof."""
from collections import Counter
from functools import lru_cache
from itertools import combinations_with_replacement, combinations, product
C=Counter()
def a0(n,m):
 return tuple(max(n[i]+m[j]-1 for i in range(len(n)) for j in range(len(m)) if i+j==k) for k in range(len(n)+len(m)-1))
def a1(n,m):
 return tuple(max(n[i-1]+m[k-i-1]-1 for i in range(1,len(n)+1) if 1<=k-i<=len(m)) for k in range(2,len(n)+len(m)+1))
def W(n,m):return sum(a0(n,m))
def J(n,m):return sum(a0(n,m)[1:])
def Bpen(n,U,V):
 s=len(n);assert n[-1]==1 and U>=V>=2
 return sum(max(0,n[i]-max(n[i+1]+V-1,
               n[i+2]+U-1 if i+2<s else -10**30)) for i in range(s-1))
def A(s,h):
 return ((2*s-3)*h+1,2*(s-3)*h+1)+tuple(2*(s-i)*h+1 for i in range(3,s+1))
def E(L,h):
 return (2*(L-2)*h+1,2*(L-2)*h+1)+tuple(2*(L-i)*h+1 for i in range(3,L+1))
# Full declared finite grid, sorted RED prefix, positive RED terminal 1.
for s in range(3,9):
 for asc in combinations_with_replacement(range(1,9),s-1):
  n=tuple(reversed(asc))+(1,)
  support=sum(n)+s>=3*s-1
  for U in range(2,9):
   for V in range(2,U+1):
    m=(U,V,1)
    assert a0(n,m)==a1(n,m)
    assert a0(n,(U-1,V-1))==a1(n,(U-1,V-1))
    P=Bpen(n,U,V)
    assert J(n,m)-(s+1)-J(n,(U-1,V-1))==P
    assert P>=0
    C['algebraic_blue_loss_identities']+=1
    if not support:continue
    C['red_vertex_support_satisfied']+=1
    if P:continue
    C['blue_loss_zero_with_support']+=1
    first=W(n[1:],m);second=W(n,m[1:])
    sigma=J(n,m)-max(first,second)
    assert sigma>=0
    if sigma:
     C['zero_loss_positive_canonical_switching']+=1
     D=n[0]+U-2
     if D*(D+1)>=2*W(n,m):
      C['positive_switching_and_original_core']+=1
    if C['blue_loss_zero_with_support']%37==0:
     for f,g in ((2,3),(4,2)):
      nn=tuple(x+f-1 for x in n)
      mm=(U+g-1,V+g-1,g)
      assert sum(nn)-s*(f-1)==sum(n)
      assert J(nn,mm)==J(n,m)+(s+1)*(f+g-2)
      assert W(nn,mm)==W(n,m)+(s+2)*(f+g-2)
      assert Bpen(tuple(x-f+1 for x in nn),
                  mm[0]-g+1,mm[1]-g+1)==0
      assert sum(tuple(x-f+1 for x in nn))+s>=3*s-1
      C['terminal_normalization_lifts']+=1
# Unbounded-in-symbols staircase proof: all penalty terms vanish directly,
# independently of length-recursion. Also check exact individual residuals.
for s in range(3,20):
 for h in range(1,41):
  n=A(s,h);m=(4*h+1,2*h+1,1)
  assert Bpen(n,m[0],m[1])==0
  assert sum(n)+s>=3*s-1
  J0=(s*s+s-1)*h+s+1
  W0=(s*s+3*s)*h+s+2
  S=(s*s+s-2)*h+s+1
  assert J(n,m)==J0 and W(n,m)==W0
  assert W(n[1:],m)==W(n,m[1:])==S and J0-S==h
  D=n[0]+m[0]-2
  assert D*(D+1)>=2*W0
  C['staircase_all_s_blue_one_step']+=1
# Independent RED-deleted equal-top residual: same one BLUE step works
# for L>=3; ORIGINAL core sufficient for L>=4, L3 original is source 3x3.
for L in range(3,18):
 for h in range(1,35):
  n=E(L,h);m=(4*h+1,2*h+1,1)
  assert Bpen(n,m[0],m[1])==0
  assert sum(n)+L>=3*L-1
  assert W(n,m)==(L*L+3*L)*h+L+2
  if L>=4:
   D=n[0]+m[0]-2
   assert D*(D+1)-2*W(n,m)>0
  C['equal_top_one_blue_step']+=1
# Actual sK3 avoiding edge-colouring graph witness under min support.
def star_options(edges,num):
 adj={}
 for x,y in edges:
  adj.setdefault(x,set()).add(y);adj.setdefault(y,set()).add(x)
 return tuple(set(frozenset((v,)+z) for v,near in adj.items()
                  for z in combinations(sorted(near),num)))
def embeds_graph(edges,target):
 opts=[star_options(edges,x) for x in sorted(target,reverse=True)]
 if any(not a for a in opts):return False
 @lru_cache(None)
 def dfs(i,used):
  if i==len(opts):return True
  return any(used.isdisjoint(v) and dfs(i+1,used|v) for v in opts[i])
 return dfs(0,frozenset())
for s in range(3,10):
 edges=[(3*i+j,3*i+(j+1)%3) for i in range(s) for j in range(3)]
 red=tuple((x,y) for x,y in edges if x//3<s-1)
 blue=tuple((x,y) for x,y in edges if x//3==s-1)
 assert not embeds_graph(red,(2,)*(s-1)+(1,))
 assert not embeds_graph(blue,(1,1))
 C['s_triangles_real_graph_avoiding_witness']+=1
def cap(arms,target):
 a=sorted((x for x in arms if x),reverse=True)
 t=sorted(target,reverse=True)
 return len(a)>=len(t) and all(x>=y for x,y in zip(a,t))
for n,m in (((4,1,1),(5,3,1)),((5,2,2,1),(4,2,1)),
            ((6,3,3,1),(5,3,1))):
 assert Bpen(n,m[0],m[1])==0
 assert sum(n)+len(n)>=3*len(n)-1
 arms=a0(n,m)[1:]
 for rr in product(*(range(z+1) for z in arms)):
  bb=tuple(z-v for z,v in zip(arms,rr))
  assert cap(rr,n[1:]) or cap(bb,m)
  assert cap(rr,n) or cap(bb,m[1:])
  C['complete_joint_canonical_host_colourings']+=1
assert C['algebraic_blue_loss_identities']==179928
assert C['red_vertex_support_satisfied']==177856
assert C['blue_loss_zero_with_support']==134447
assert C['zero_loss_positive_canonical_switching']==11142
assert C['positive_switching_and_original_core']==7090
for k in sorted(C):print('ERDOS561_ALL_S_BLUE_MATCHING',k,C[k])
print('ERDOS561_ALL_S_BLUE_MATCHING_FINITE_PASS')
