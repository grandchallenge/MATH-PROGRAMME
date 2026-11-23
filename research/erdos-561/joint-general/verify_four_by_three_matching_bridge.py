#!/usr/bin/env python3
"""Finite symbolic and explicit graph-witness tests for 4-by-3 matching bridge.

NOT a proof by finite enumeration of arbitrary host graphs.
All-host lemma is a Gallai factor-critical argument in companion manuscript.
"""
from collections import Counter
from itertools import combinations_with_replacement
import functools

def diag_zero(n,m):
    return tuple(max(n[i]+m[j]-1 for i in range(len(n)) for j in range(len(m))
                     if i+j==k) for k in range(len(n)+len(m)-1))
def diag_one(n,m):
    return tuple(max(n[i-1]+m[k-i-1]-1 for i in range(1,len(n)+1)
                     if 1<=k-i<=len(m)) for k in range(2,len(n)+len(m)+1))
def positive(x):
    return max(0,x)
def joint(n,m):
    return sum(diag_zero(n,m)[1:])
def separate(n,m):
    return sum(diag_zero(n[1:],m)),sum(diag_zero(n,m[1:]))

ct=Counter()
for a in range(2,12):
 for b in range(2,a+1):
  for c in range(2,b+1):
   for d in range(1,12):
    for e in range(1,d+1):
     n=(a,b,c,1);m=(d,e,1)
     w=diag_zero(n,m)
     assert w==diag_one(n,m)
     T=max(b,c+e-1)
     P=positive(d-T)+positive(e-c)
     redshort=(a-1,b-1,c-1)
     assert joint(n,m)-(joint(redshort,m)+5)==P
     assert P==0 if (e<=c and d<=T) else P>0
     assert len(w)==6 and sum(w[1:])==joint(n,m)
     A,B=separate(n,m)
     assert joint(n,m)>=A and joint(n,m)>=B
     sigma=joint(n,m)-max(A,B)
     assert sigma>=0
     # Independent exact separate residual theorems give the sharp
     # complementary lower Jcan-sigma.
     Pb=10**9
     if e>=2:
      X=max(b+e-1,c+d-1);Z=max(c+e-1,d)
      Pb=positive(a-X)+positive(b-Z)+positive(c-e)
      # Full BLUE matching deletion gives 4x2 two-component JOINT bridge.
      assert joint(n,m)-joint(n,(d-1,e-1))-5==Pb
      ct['dual_blue_legal']+=1
      ct['dual_blue_sharp']+=(Pb==0)
     previous_deficit=min(P,sigma)
     combined_deficit=min(P,Pb,sigma)
     assert 0<=combined_deficit<=previous_deficit
     assert joint(n,m)-combined_deficit==max(joint(n,m)-P,joint(n,m)-Pb,A,B)
     ct['previous_exact_covered']+=(previous_deficit==0)
     ct['combined_exact_covered']+=(combined_deficit==0)
     ct['blue_newly_exact']+=(previous_deficit>0 and combined_deficit==0)
     ct['triple_positive_remaining']+=(combined_deficit>0)
     ct['sigma_zero']+=(sigma==0)
     ct['positive_P_and_sigma']+=(P>0 and sigma>0)
     ct['positive_P_sigma_zero']+=(P>0 and sigma==0)
     # Theorem D: each uniform BLUE size shift is carried by a 5-edge BLUE
     # matching, preserving the reduced lower-bound deficits and switching.
     for g in (2,4):
      lifted_blue=(d+g-1,e+g-1,g)
      wb=diag_zero(n,lifted_blue)
      assert wb==diag_one(n,lifted_blue)
      assert joint(n,lifted_blue)==joint(n,m)+5*(g-1)
      assert sum(wb)==sum(w)+6*(g-1)
      sepLb,sepRb=separate(n,lifted_blue)
      assert joint(n,lifted_blue)-max(sepLb,sepRb)==sigma
      ct['blue_terminal_arm_lifts']+=1
     ct['base_all']+=1
     if P==0:
      ct['base_sharp']+=1
      if joint(n,m)>max(A,B):ct['base_switching']+=1
      D=a+d-2;W=sum(w)
      if d>=2 and W<=D*(D+1)//2:ct['base_original_core']+=1
     else:
      ct['positive_deficit']+=1
     # Uniform red arm shifts raise each of the six antidiagonal weights by
     # f-1, preserving the exact base deficit and switching surplus.
     if combined_deficit==0:
      for f in (2,3,5):
       lifted=(a+f-1,b+f-1,c+f-1,f)
       wl=diag_zero(lifted,m)
       assert wl==diag_one(lifted,m)
       assert joint(lifted,m)==joint(n,m)+5*(f-1)
       assert sum(wl)==sum(w)+6*(f-1)
       assert joint(lifted,m)-joint(tuple(v-1 for v in lifted),m)==5
       ct['lifted_sharp']+=1

for h in range(1,151):
 n=(6*h,4*h,4*h,1);m=(4*h,3*h,1)
 w=diag_zero(n,m)
 assert w==(10*h-1,9*h-1,8*h-1,7*h-1,4*h,1)
 assert diag_one(n,m)==w
 assert joint(n,m)==28*h-2 and sum(w)==38*h-3
 a,b=separate(n,m)
 assert a==b==27*h-2 and joint(n,m)-max(a,b)==h
 D=10*h-2;W=38*h-3
 assert D*(D+1)-2*(W-1)==(h-1)*(100*h-6)+4>0
 ct['unbounded_switching_scale']+=1
 # Complementary BLUE bridge loses zero although RED bridge and switching
 # each lose h; the original transfers when h>=2.
 nn=(4*h,2*h,2*h,1);mm=(4*h,3*h,1)
 ww=diag_zero(nn,mm)
 assert ww==(8*h-1,7*h-1,6*h-1,5*h-1,3*h,1)
 assert diag_one(nn,mm)==ww
 JJ=joint(nn,mm);Ss1,Ss2=separate(nn,mm)
 assert JJ==21*h-2 and sum(ww)==29*h-3
 assert Ss1==Ss2==20*h-2 and JJ-max(Ss1,Ss2)==h
 PR=positive(4*h-max(2*h,2*h+3*h-1))+positive(3*h-2*h)
 PB=positive(4*h-max(2*h+3*h-1,2*h+4*h-1))
 PB+=positive(2*h-max(2*h+3*h-1,4*h))+positive(2*h-3*h)
 assert PR==h and PB==0
 if h>=2:
  D=8*h-2;W=29*h-3
  assert D*(D+1)-2*(W-1)==64*h*h-82*h+10>0
 ct['dual_unbounded_switching_scale']+=1
 # New 3-parameter h,r,k families. All original components >=2 when r,k>=1.
 for r,k in ((0,0),(1,1),(2,3),(5,0),(0,6)):
  x=r+k
  nr=(6*h+r,4*h+r,4*h+r,1+r)
  mr=(4*h+k,3*h+k,1+k)
  wr=diag_zero(nr,mr)
  assert wr==tuple(z+x for z in w)
  assert wr==diag_one(nr,mr)
  jr=joint(nr,mr)
  assert jr==28*h-2+5*x and sum(wr)==38*h-3+6*x
  sep1,sep2=separate(nr,mr)
  assert sep1==sep2==27*h-2+5*x
  assert jr-max(sep1,sep2)==h
  Dr=10*h+x-2
  assert Dr*(Dr+1)-2*(sum(wr)-1)==(h-1)*(100*h-6)+4+(20*h-15)*x+x*x>0
  ct['all_positive_shift_red_bridge']+=1
  nb=(4*h+r,2*h+r,2*h+r,1+r)
  mb=(4*h+k,3*h+k,1+k)
  wb=diag_zero(nb,mb)
  assert wb==tuple(z+x for z in ww)
  assert wb==diag_one(nb,mb)
  jb=joint(nb,mb)
  assert jb==21*h-2+5*x and sum(wb)==29*h-3+6*x
  sep1,sep2=separate(nb,mb)
  assert sep1==sep2==20*h-2+5*x
  assert jb-max(sep1,sep2)==h
  Db=8*h+x-2
  gap=Db*(Db+1)-2*(sum(wb)-1)
  assert gap==64*h*h-82*h+10+(16*h-15)*x+x*x
  if h>=2 or x>=3:
   assert gap>0
   ct['all_positive_shift_blue_original_core']+=1
  else:
   assert h==1 and x<3
  ct['all_positive_shift_blue_bridge_joint']+=1


# NEW exact tied-bottom RED case: n=(A,B,1,1), A+B>=5.
# The analytical five-matching bridge here uses the support-size >=11
# strengthening, NOT the c>=f+1 result from the older RED proof.
for A in range(1,13):
 for B in range(1,A+1):
  if A+B<5: continue
  for D in range(2,13):
   for E in range(2,D+1):
    red=(A,B,1,1);blue=(D,E,1)
    W0=diag_zero(red,blue)
    Pb_tie=positive(A-max(B+E-1,D))+positive(B-D)
    J0=joint(red,blue)
    J_short=joint(red,(D-1,E-1))
    assert J0==5+J_short+Pb_tie
    S1,S2=separate(red,blue)
    sigma=J0-max(S1,S2)
    assert sigma>=0
    assert J0-min(Pb_tie,sigma)==max(5+J_short,S1,S2)
    ct['tied_red_base_profiles']+=1
    ct['tied_red_base_blue_sharp']+=(Pb_tie==0)
    ct['tied_red_base_separate_sharp']+=(sigma==0)
    ct['tied_red_base_combined_sharp']+=(min(Pb_tie,sigma)==0)
    ct['tied_red_base_positive_switching_blue_sharp']+=(Pb_tie==0 and sigma>0)
    for f in (1,2,4):
     for g in (1,2,3):
      nr=(A+f-1,B+f-1,f,f)
      mb=(D+g-1,E+g-1,g)
      assert diag_zero(nr,mb)==diag_one(nr,mb)
      assert joint(nr,mb)==J0+5*(f+g-2)
      W=sum(diag_zero(nr,mb))
      assert W==sum(W0)+6*(f+g-2)
      s1,s2=separate(nr,mb)
      assert joint(nr,mb)-max(s1,s2)==sigma
      # Every red terminal decrement preserves red nonisolated vertex
      # support >= A+B+6>=11, and every blue terminal decrement leaves
      # its two residual arms positive.
      assert A+B+6>=11
      assert mb[1]-mb[2]+1==E>=2
      DL=nr[0]+mb[0]-2
      ct['tied_red_both_minima_lifts']+=1
      ct['tied_red_original_core_eligible']+=(min(Pb_tie,sigma)==0 and W<=DL*(DL+1)//2)

# Third EXACT unbounded-switching heterogeneous 4x3 family: red has
# the two smallest arm sizes equal and both can be >=2.
for h in range(1,151):
 for r in range(4):
  for k in range(4):
   nr=(4*h+r,h+r,1+r,1+r)
   mb=(4*h+k,2*h+k,1+k)
   w=diag_zero(nr,mb)
   assert w==diag_one(nr,mb)
   x=r+k
   assert w==(8*h-1+x,6*h-1+x,4*h+x,4*h+x,2*h+x,1+x)
   J=joint(nr,mb)
   assert J==16*h+5*x
   assert sum(w)==24*h-1+6*x
   ss1,ss2=separate(nr,mb)
   assert J-max(ss1,ss2)==h
   A=nr[0]-nr[-1]+1;B=nr[1]-nr[-1]+1
   D=mb[0]-mb[-1]+1;E=mb[1]-mb[-1]+1
   assert (A,B,D,E)==(4*h,h,4*h,2*h)
   assert positive(A-max(B+E-1,D))+positive(B-D)==0
   L=nr[0]+mb[0]-2
   core=L*(L+1)-2*sum(w)
   assert core==64*h*h-72*h+4+(16*h-15)*x+x*x
   eligible=(h>=2 or x>=2)
   assert (core>=0)==eligible
   if r>=1 and k>=1:
    assert nr[-1]>=2 and mb[-1]>=2 and eligible
   ct['tied_red_unbounded_switching_family_checks']+=1
   ct['tied_red_unbounded_switching_original_core']+=eligible

# Independently check the Gallai equality-profile argument:
# if nu(Q)=4, matching-stable nontrivial factor-critical components C_i have
# order 2*nu(C_i)+1, nu(C_i)>=1, so 11 nonisolated vertices remain after
# deleting any nontrivial v only if all four components are triangles.
def positive_compositions(n):
 for k in range(1,n+1):
  def rec(rem,slots):
   if slots==0:
    if rem==0:yield ()
    return
   for z in range(1,rem-slots+2):
    for t in rec(rem-z,slots-1):yield (z,)+t
  yield from rec(n,k)
for shape in positive_compositions(4):
 nonisolated=sum(2*v+1 for v in shape)
 assert nonisolated<=12
 if nonisolated-1>=11:
  assert shape==(1,1,1,1) and nonisolated==12
 ct['factorcritical_matching_partition_shapes']+=1

# Test the actual exception 4K3, with three triangles RED and the fourth BLUE,
# against the MINIMAL targets (2,2,2,1) in red and (1,1) in blue.
edges=[(3*k+i,3*k+(i+1)%3) for k in range(4) for i in range(3)]
red=tuple(edge for edge in edges if edge[0]//3<3)
blue=tuple(edge for edge in edges if edge[0]//3==3)
def star_embeddings(edgelist,arm):
 adj={}
 for x,y in edgelist:
  adj.setdefault(x,set()).add(y);adj.setdefault(y,set()).add(x)
 import itertools
 ans=set()
 for centre,near in adj.items():
  for leaves in itertools.combinations(sorted(near),arm):
   ans.add(frozenset((centre,)+leaves))
 return tuple(ans)
def has_forest(edgelist,profile):
 options=[star_embeddings(edgelist,s) for s in sorted(profile,reverse=True)]
 if any(not x for x in options):return False
 @functools.lru_cache(None)
 def rec(i,used):
  if i==len(options):return True
  for vertices in options[i]:
   if used.isdisjoint(vertices) and rec(i+1,used|vertices):return True
  return False
 return rec(0,frozenset())
assert not has_forest(red,(2,2,2,1))
assert not has_forest(blue,(1,1))
# Minimal 11-vertex RED profile of the tied-tail theorem, blue 2-star forest.
assert not has_forest(red,(4,1,1,1))
assert not has_forest(blue,(2,1))
assert len(red)==9 and len(blue)==3
ct['gallai_extremal_actual_graph_witness']+=1

assert ct['base_all']>10000 and ct['base_sharp']>1000
assert ct['base_switching']>0
assert ct['previous_exact_covered']==13224
assert ct['blue_newly_exact']==838
assert ct['combined_exact_covered']==14062
assert ct['triple_positive_remaining']==458
assert ct['combined_exact_covered']==ct['base_all']-ct['triple_positive_remaining']
assert ct['blue_terminal_arm_lifts']==2*ct['base_all']
assert ct['lifted_sharp']==3*ct['combined_exact_covered']
assert ct['all_positive_shift_red_bridge']==750
assert ct['all_positive_shift_blue_bridge_joint']==750
assert ct['all_positive_shift_blue_original_core']==748
assert ct['unbounded_switching_scale']==150
print('ERDOS561_4X3_BASE_EXACT_DEFICIT_CASES',ct['base_all'])
print('ERDOS561_4X3_JOINT_SHARP_PARAMETER_CASES',ct['base_sharp'])
print('ERDOS561_4X3_POSITIVE_SWITCHING_SHARP_CASES',ct['base_switching'])
print('ERDOS561_4X3_QUANTIFIED_DEFICIT_NONZERO_CASES',ct['positive_deficit'])
print('ERDOS561_4X3_PREVIOUS_RED_OR_SIGMA_EXACT',ct['previous_exact_covered'])
print('ERDOS561_4X3_DUAL_BLUE_BRIDGE_NEWLY_EXACT',ct['blue_newly_exact'])
print('ERDOS561_4X3_TOTAL_EXACT_RED_BLUE_OR_SIGMA',ct['combined_exact_covered'])
print('ERDOS561_4X3_TRIPLE_POSITIVE_BOUNDARY',ct['triple_positive_remaining'])
print('ERDOS561_4X3_SIGMA_ZERO_CASES',ct['sigma_zero'])
print('ERDOS561_4X3_POSITIVE_P_ZERO_SIGMA_NEW_CASES',ct['positive_P_sigma_zero'])
print('ERDOS561_4X3_EXACT_REMAINING_COUPLED_P_SIGMA_POSITIVE_CASES',ct['positive_P_and_sigma'])
print('ERDOS561_4X3_LIFTED_ALL_POSITIVE_ARM_CASES',ct['lifted_sharp'])
print('ERDOS561_4X3_ORIGINAL_CORE_SUFFICIENT_CASES',ct['base_original_core'])
print('ERDOS561_4X3_GALLAI_FACTORCRITICAL_MATCHING_PARTITIONS',ct['factorcritical_matching_partition_shapes'])
print('ERDOS561_4X3_K3_QUADRUPLE_AVOIDING_COLOURING_PASS')
print('ERDOS561_4X3_UNBOUNDED_RED_BRIDGE_150_SCALES_PASS')
print('ERDOS561_4X3_UNBOUNDED_BLUE_BRIDGE_150_SCALES_PASS')
print('ERDOS561_4X3_UNIFORM_BLUE_MINIMUM_LIFT_PARAMS',ct['blue_terminal_arm_lifts'])
print('ERDOS561_4X3_TWO_SIDED_RED_ARM_LIFT_PARAMS',ct['lifted_sharp'])
print('ERDOS561_4X3_ALL_POSITIVE_RED_FAMILY_3PARAM_TESTS',ct['all_positive_shift_red_bridge'])
print('ERDOS561_4X3_ALL_POSITIVE_BLUE_FAMILY_JOINT_3PARAM_TESTS',ct['all_positive_shift_blue_bridge_joint'])
print('ERDOS561_4X3_ALL_POSITIVE_BLUE_FAMILY_ORIGINAL_CORE_TESTS',ct['all_positive_shift_blue_original_core'])
print('ERDOS561_4X3_TIED_RED_BASE_PROFILES',ct['tied_red_base_profiles'])
print('ERDOS561_4X3_TIED_RED_BLUE_BRIDGE_EXACT',ct['tied_red_base_blue_sharp'])
print('ERDOS561_4X3_TIED_RED_INDIVIDUAL_EXACT',ct['tied_red_base_separate_sharp'])
print('ERDOS561_4X3_TIED_RED_UNION_EXACT',ct['tied_red_base_combined_sharp'])
print('ERDOS561_4X3_TIED_RED_POSITIVE_SWITCHING_CLOSED_BY_BLUE',ct['tied_red_base_positive_switching_blue_sharp'])
print('ERDOS561_4X3_TIED_RED_RED_BLUE_TERMINAL_LIFTS',ct['tied_red_both_minima_lifts'])
print('ERDOS561_4X3_TIED_RED_ORIGINAL_CORE_ELIGIBLE',ct['tied_red_original_core_eligible'])
print('ERDOS561_4X3_THIRD_UNBOUNDED_SWITCHING_FAMILY_CHECKS',ct['tied_red_unbounded_switching_family_checks'])
print('ERDOS561_4X3_THIRD_FAMILY_ORIGINAL_CORE_CHECKS',ct['tied_red_unbounded_switching_original_core'])
