#!/usr/bin/env python3
"""Independent exact finite algebra and graph witness for the 5x3 matching bridge.

All-host proof is the separate Gallai-based manuscript, not finite inference.
No external dependencies, network, GPU, or random sampling.
"""
from collections import Counter
from itertools import product
import functools
import itertools

def diag0(n,m):
    return tuple(max(n[i]+m[j]-1 for i in range(len(n)) for j in range(len(m))
                     if i+j==k) for k in range(len(n)+len(m)-1))
def diag1(n,m):
    return tuple(max(n[i-1]+m[k-i-1]-1 for i in range(1,len(n)+1)
                     if 1<=k-i<=len(m)) for k in range(2,len(n)+len(m)+1))
def J(n,m):return sum(diag0(n,m)[1:])
def W(n,m):return sum(diag0(n,m))
def S(n,m):return W(n[1:],m),W(n,m[1:])
def pos(x):return max(x,0)
def embed_arms(available,want):
    aa=sorted((x for x in available if x>0),reverse=True)
    ww=sorted(want,reverse=True)
    return len(aa)>=len(ww) and all(x>=y for x,y in zip(aa,ww))
ct=Counter()

# Exact all-positive six-weight identity for the 5x3 base with final RED=1.
for a in range(2,8):
 for b in range(2,a+1):
  for c in range(2,b+1):
   for d in range(2,c+1):
    for u in range(1,8):
     for v in range(1,u+1):
      for z in range(1,v+1):
       n=(a,b,c,d,1);m=(u,v,z);q=(a-1,b-1,c-1,d-1)
       assert diag0(n,m)==diag1(n,m)
       assert diag0(q,m)==diag1(q,m)
       penalty=pos(u-max(c+z-1,d+v-1))+pos(v-(d+z-1))+(z-1)
       assert J(n,m)==6+J(q,m)+penalty
       ct['six_weight_base_identity']+=1
       if z==1:
        ct['unit_blue_base_profiles']+=1
        assert penalty==pos(u-max(c,d+v-1))+pos(v-d)
        # Arbitrary red-terminal shift: all 6 joint and 7 original
        # antidiagonals rise by the amount added to all red arm sizes.
        for f in (2,4):
         red=(a+f-1,b+f-1,c+f-1,d+f-1,f)
         assert J(red,m)==J(n,m)+6*(f-1)
         assert W(red,m)==W(n,m)+7*(f-1)
         ct['red_uniform_terminal_lifts']+=1

# Explicit FIVE-vs-THREE scale family; includes both terminals >=2 when r,k>=1.
for h in range(1,151):
 for r in range(4):
  for k in range(4):
   n=(6*h+r,3*h+r,3*h+r,3*h+r,1+r)
   m=(4*h+k,2*h+k,1+k)
   x=r+k
   ww=diag0(n,m)
   assert ww==diag1(n,m)
   assert ww==(10*h-1+x,8*h-1+x,7*h-1+x,7*h-1+x,5*h-1+x,3*h+x,1+x)
   assert J(n,m)==30*h-3+6*x
   assert W(n,m)==40*h-4+7*x
   A,B= S(n,m)
   assert J(n,m)-max(A,B)==h
   # The canonical 4x3 reduction is n4=(6h-1,3h-1,3h-1,3h-1).
   n4=(6*h-1,3*h-1,3*h-1,3*h-1)
   assert J(n4,(4*h,2*h,1))==30*h-9
   Atop=3*h+1; Btop=1
   Ptie=pos(Atop-max(Btop+2*h-1,4*h))+pos(Btop-4*h)
   P5=pos(4*h-max(3*h,3*h+2*h-1))+pos(2*h-3*h)
   assert Atop+Btop>=5 and Ptie==0 and P5==0
   assert J(n,m)==6*(r+k)+6+J(n4,(4*h,2*h,1))
   D=10*h+x-2
   diff=D*(D+1)-2*W(n,m)
   assert diff==10*(h-1)*(10*h-1)+(20*h-17)*x+x*x>=0
   if r>=1 and k>=1:
    assert n[-1]>=2 and m[-1]>=2
    ct['all_nontrivial_arms']+=1
   if h>=2:
    # Protected 4x3 ORIGINAL first residual core criterion:
    nr=n[1:]
    Dr=nr[0]+m[0]-2
    assert W(nr,m)<=Dr*(Dr+1)//2
   ct['six_edge_unbounded_scale_cases']+=1

# Canonical upper hosts are checked independently of the star-host theorem.
for h in (1,2):
 n=(6*h,3*h,3*h,3*h,1)
 m=(4*h,2*h,1)
 for typ,host in (('original',diag0(n,m)),('joint',diag0(n,m)[1:])):
  for reds in product(*(range(t+1) for t in host)):
   blues=tuple(t-x for t,x in zip(host,reds))
   if typ=='original':
    assert embed_arms(reds,n) or embed_arms(blues,m)
   else:
    assert embed_arms(reds,n[1:]) or embed_arms(blues,m)
    assert embed_arms(reds,n) or embed_arms(blues,m[1:])
   ct['upper_host_colour_allocations']+=1
  ct['upper_host_classes']+=1

# Complete small set of factor-critical component matching-number partitions.
def compositions(n):
 for k in range(1,n+1):
  def rec(rem,slots):
   if slots==0:
    if rem==0: yield ()
    return
   for x in range(1,rem-slots+2):
    for rest in rec(rem-x,slots-1): yield (x,)+rest
  yield from rec(n,k)
for parts in compositions(5):
 N=sum(2*q+1 for q in parts)
 assert N<=15
 if N-1>=14:
  assert parts==(1,1,1,1,1) and N==15
 ct['factorcritical_matching5_composition_checks']+=1

# Explicit G=5K3 witness: four entire triangles red, fifth entire triangle
# blue avoids red F(2,2,2,2,1) (14 vertices) and blue F(1,1) (4 vertices).
tri=[(3*i+j,3*i+(j+1)%3) for i in range(5) for j in range(3)]
red=tuple((x,y) for x,y in tri if x//3<4)
blue=tuple((x,y) for x,y in tri if x//3==4)
def star_options(edges,arm):
 adj={}
 for a,b in edges:
  adj.setdefault(a,set()).add(b)
  adj.setdefault(b,set()).add(a)
 out=set()
 for c,near in adj.items():
  for xs in itertools.combinations(sorted(near),arm):
   out.add(frozenset((c,)+xs))
 return tuple(out)
def graph_contains_forest(edges,target):
 opts=[star_options(edges,x) for x in sorted(target,reverse=True)]
 if any(not o for o in opts):return False
 @functools.lru_cache(maxsize=None)
 def dfs(i,used):
  if i==len(opts):return True
  for nodes in opts[i]:
   if nodes.isdisjoint(used) and dfs(i+1,used|nodes):return True
  return False
 return dfs(0,frozenset())
assert not graph_contains_forest(red,(2,2,2,2,1))
assert not graph_contains_forest(blue,(1,1))
ct['actual_5K3_avoiding_colouring']+=1

assert ct['six_weight_base_identity']==10584
assert ct['six_edge_unbounded_scale_cases']==2400
assert ct['upper_host_classes']==4
assert ct['factorcritical_matching5_composition_checks']==16
print('ERDOS561_5X3_EXACT_SIX_WEIGHT_PARAMETER_CASES',ct['six_weight_base_identity'])
print('ERDOS561_5X3_RED_TERMINAL_LIFTS',ct['red_uniform_terminal_lifts'])
print('ERDOS561_5X3_COMPLETE_CANONICAL_UPPER_HOST_ALLOCATIONS',ct['upper_host_colour_allocations'])
print('ERDOS561_5X3_FACTORCRITICAL_MATCHING5_COMPONENT_PARTITIONS',ct['factorcritical_matching5_composition_checks'])
print('ERDOS561_5X3_ACTUAL_5K3_AVOIDING_COLOURING_PASS')
print('ERDOS561_5X3_FOURTH_UNBOUNDED_SWITCHING_FAMILY_CASES',ct['six_edge_unbounded_scale_cases'])
print('ERDOS561_5X3_ALL_STAR_COMPONENTS_GE2_EXAMPLES',ct['all_nontrivial_arms'])
