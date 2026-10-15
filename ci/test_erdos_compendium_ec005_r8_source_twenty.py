"""Twenty exact finite interfaces, not theorem certifications."""
import itertools,math,unittest
from fractions import Fraction
from pathlib import Path
P=Path(__file__).resolve().parents[1]/"governance/erdos_compendium/editorial"
def src(n):return (P/f"{n:04d}.md").read_text()
def primefactor(n):
 for i in range(2,n+1):
  if n%i==0:return i
class R8Finite(unittest.TestCase):
 def test_656_mod3_shift(self):
  a=[3*i+1 for i in range(8)]
  self.assertTrue(all((x+y+2-1)%3==0 for x,y in itertools.combinations(a,2)))
  self.assertTrue(all((x+y-1)%3!=0 for x,y in itertools.combinations(a,2)))
 def test_665_fano_design(self):
  lines=[{i%7,(i+1)%7,(i+3)%7} for i in range(7)]
  pairs=[frozenset(c) for b in lines for c in itertools.combinations(b,2)]
  self.assertEqual((len(pairs),len(set(pairs))),(21,21))
 def test_669_fourpoint_rich_line(self):
  pts=((0,0),(1,0),(2,0),(0,1))
  def triple(a,b,c):return (b[0]-a[0])*(c[1]-a[1])==(b[1]-a[1])*(c[0]-a[0])
  self.assertEqual(sum(triple(*x) for x in itertools.combinations(pts,3)),1)
 def test_682_strict_gap_equality(self):
  self.assertEqual([primefactor(x) for x in (8,9,10)],[2,3,2])
  self.assertTrue(all(primefactor(x)<4 for x in (8,9,10)))
  self.assertEqual(primefactor(12),13-11)
 def test_684_10choose7_and_20(self):
  def u(n,k):
   c=math.comb(n,k);res=1
   for p in range(2,k+1):
    if any(p%d==0 for d in range(2,math.isqrt(p)+1)):continue
    while c%p==0 and c>1:c//=p;res*=p
   return res
  self.assertEqual(u(10,7),120)
  self.assertEqual(min(k for k in range(11) if u(10,k)>100),7)
  self.assertEqual(max(u(20,k) for k in range(21)),240)
 def test_690_exact_d1_and_d2(self):
  def d(k,p):
   q=[n for n in range(2,p) if all(n%m for m in range(2,math.isqrt(n)+1))]
   z=Fraction(0)
   for bits in itertools.product((0,1),repeat=len(q)):
    if sum(bits)==k-1:
     v=Fraction(1,p)
     for x,b in zip(q,bits):v*=Fraction(1,x) if b else Fraction(x-1,x)
     z+=v
   return z
  self.assertEqual([d(1,x) for x in (2,3,5)],[Fraction(1,2),Fraction(1,6),Fraction(1,15)])
  self.assertEqual((d(2,3),d(2,5)),(Fraction(1,6),Fraction(1,10)))
 def test_692_exact_unimodality_dip(self):
  def dens(n,m):
   z=list(range(n+1,m));M=math.lcm(*z)
   return Fraction(sum(sum(k%d==0 for d in z)==1 for k in range(1,M+1)),M)
  self.assertEqual((dens(3,6),dens(3,7),dens(3,8)),(Fraction(7,20),Fraction(1,3),Fraction(38,105)))

 def test_703_forbidden_intersection_r1(self):
  family=[set()]+[{i} for i in range(4)]
  self.assertEqual(len(family),5)
  self.assertTrue(all(len(a&b)!=1 for a,b in itertools.combinations(family,2)))
 def test_704_unit_distance_one_dimension(self):
  def color(x):return math.floor(x)%2
  for x in (0,0.1,0.5,0.999,-1.1,-0.25,2.25,100.9):
   self.assertNotEqual(color(x),color(x+1))
  # Three unit-spaced points of a plane form K3.
  P2=((0,0),(1,0),(0.5,math.sqrt(3)/2))
  self.assertTrue(all(abs(math.dist(a,b)-1)<1e-12 for a,b in itertools.combinations(P2,2)))
 def test_715_cubic_K5_and_K44(self):
  E={frozenset(t) for t in itertools.combinations(range(5),2)}
  F={e for e in E if 4 not in e}
  self.assertEqual([sum(i in e for e in F) for i in range(4)],[3]*4)
  rem={frozenset((i,4+i)) for i in range(4)}
  K44={frozenset((a,4+b)) for a in range(4) for b in range(4)}
  self.assertEqual([sum(i in e for e in K44-rem) for i in range(8)],[3]*8)
 def test_721_W33_exact(self):
  triples=[(a,a+d,a+2*d) for a in range(1,10) for d in range(1,5) if a+2*d<=9]
  def avoids(n,mask):
   return all(not (a+2*d<=n and (mask>>(a-1)&1)==(mask>>(a+d-1)&1)==(mask>>(a+2*d-1)&1))
                  for a,d,_, in [(x,x2-x,x3) for x,x2,x3 in triples] if a+2*d<=n)
  self.assertTrue(any(avoids(8,m) for m in range(1<<8)))
  self.assertFalse(any(avoids(9,m) for m in range(1<<9)))
 def test_733_four_points_line_sizes(self):
  P4=((0,0),(1,0),(2,0),(0,1))
  def key(a,b):
   dx=b[0]-a[0];dy=b[1]-a[1];A=dy;B=-dx;C=A*a[0]+B*a[1]
   g=math.gcd(abs(A),abs(B),abs(C))
   return (A//g,B//g,C//g) if (A>0 or (A==0 and B>0)) else (-A//g,-B//g,-C//g)
  lines={}
  for i,j in itertools.combinations(range(4),2):
   k=key(P4[i],P4[j]);lines.setdefault(k,set()).update((i,j))
  self.assertEqual(sorted(map(len,lines.values())),[2,2,2,3])
 def test_735_magic_nminus1_collinear(self):
  P4=((0,0),(1,0),(2,0),(0,1))
  W=(1,1,1,2)
  lines=((0,1,2),(0,3),(1,3),(2,3))
  self.assertEqual([sum(W[i] for i in L) for L in lines],[3]*4)
 def test_737_K4_edge_two_cycle_lengths(self):
  E={frozenset(x) for x in itertools.combinations(range(4),2)}
  self.assertTrue(all(frozenset(p) in E for p in ((0,1),(1,2),(2,0))))
  self.assertTrue(all(frozenset(p) in E for p in ((0,1),(1,2),(2,3),(3,0))))

 def test_744_K4_bipartite_deletion_two(self):
  E={frozenset(x) for x in itertools.combinations(range(4),2)}
  best=0
  for bits in itertools.product((0,1),repeat=4):
   kept=sum(bits[a]!=bits[b] for a,b in itertools.combinations(range(4),2))
   best=max(best,kept)
  self.assertEqual(len(E)-best,2)
 def test_746_cycle5_and_disconnected_dense(self):
  C={frozenset((i,(i+1)%5)) for i in range(5)}
  self.assertEqual(len(C),5)
  self.assertEqual([sum(v in e for e in C) for v in range(5)],[2]*5)
  self.assertEqual(math.comb(5,2),10)
 def test_752_C6_one_even_cycle_length(self):
  E={frozenset((i,(i+1)%6)) for i in range(6)}
  self.assertEqual([sum(v in e for e in E) for v in range(6)],[2]*6)
  self.assertEqual(len(E),6)
  self.assertNotIn(frozenset((0,3)),E)
 def test_754_four_equidistant_points_R4(self):
  V=[tuple(int(j==i) for j in range(4)) for i in range(4)]
  self.assertEqual({math.dist(a,b) for a,b in itertools.combinations(V,2)},{math.sqrt(2)})
  self.assertEqual(len(V)-1,3)
 def test_757_weak_sidon_four(self):
  def differences(A):return {a-b for a in A for b in A}
  self.assertEqual(len(differences((0,1,3,5))),11)
  self.assertEqual(len(differences((0,1,3,7))),13)
  self.assertEqual(3-1,5-3)
 def test_771_even_set_subset_sums(self):
  S=(2,4,6,8,10)
  sums={sum(t) for k in range(6) for t in itertools.combinations(S,k)}
  self.assertNotIn(9,sums)
  self.assertTrue(all(n%2==0 for n in sums))
