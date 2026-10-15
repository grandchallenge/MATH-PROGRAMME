"""EC005 editorial source-lock batch: finite examples, not theorem certification."""
import itertools, math, unittest
from pathlib import Path
P=Path(__file__).resolve().parents[1]/"governance/erdos_compendium/editorial"
def choose(n,k):return list(itertools.combinations(range(n),k))
def source(n):return (P/f"{n:04d}.md").read_text()
def sumdiv(n):return sum(i for i in range(1,n+1) if n%i==0)
class SourceLock25(unittest.TestCase):
 def test_780_K5_two_color_disjoint_pair(self):
  E=choose(5,2)
  for colors in itertools.product((0,1),repeat=10):
   self.assertTrue(any(colors[i]==colors[j] and not(set(a)&set(b)) for i,a in enumerate(E) for j,b in enumerate(E) if i<j))
  self.assertIn("disjoint",source(780))
 def test_781_reflection_wave(self):
  a=[1,3,4];b=sorted(6-x for x in a)
  self.assertEqual((b,[b[1]-b[0],b[2]-b[1]]),([2,3,5],[1,2]))
 def test_794_harris_28_edge(self):
  E={frozenset(t) for t in itertools.product(range(3),range(3,6),range(6,9))}|{frozenset((0,1,2))}
  self.assertEqual(len(E),28)
  for k,limit in ((4,2),(5,6)):
   self.assertTrue(all(sum(e<=set(s) for e in E)<=limit for s in choose(9,k)))
 def test_795_distinct_subset_products(self):
  a=[2,3,4,9]
  vals=[math.prod(c) for k in range(5) for c in itertools.combinations(a,k)]
  self.assertEqual(len(set(vals)),16)
 def test_797_C4_acyclic_three(self):
  x=(0,1,2,1);self.assertTrue(all(x[i]!=x[(i+1)%4] for i in range(4)))
  self.assertEqual(len(set(x)),3)
 def test_798_square_three_points_no_fourth(self):
  p=((0,0),(0,1),(1,0),(1,1))
  def online(a,b,c):return (p[b][0]-p[a][0])*(p[c][1]-p[a][1])==(p[b][1]-p[a][1])*(p[c][0]-p[a][0])
  for v in range(4):
   S=[i for i in range(4) if i!=v]
   self.assertFalse(any(online(a,b,v) for a,b in itertools.combinations(S,2)))
 def test_799_K3_two_lists_impossible(self):
  self.assertTrue(all(len(set(x))<3 for x in itertools.product(range(2),repeat=3)))
 def test_800_K13_ramsey6(self):
  E=choose(6,2)
  for bits in itertools.product((0,1),repeat=15):
   c={tuple(e):bits[i] for i,e in enumerate(E)}
   self.assertTrue(any(sum(c[tuple(sorted((v,w)))]==color for w in range(6) if w!=v)>=3 for v in range(6) for color in (0,1)))

 def test_801_K9_induced_three(self):
  self.assertEqual(math.comb(3,2),3)
  self.assertIn("induced",source(801).lower())
 def test_803_degree_balance(self):
  deg=[3,1,1,1];self.assertEqual(max(deg)/min(deg),3)
 def test_806_repeated_sumset(self):
  B=(1,3);self.assertEqual({x+y for x in B for y in B},{2,4,6})
  self.assertEqual({sum(pair) for pair in itertools.combinations(B,2)},{4})
 def test_807_K4_edge_disjoint_stars(self):
  E={frozenset(x) for x in choose(4,2)}
  sets=({frozenset((0,x)) for x in (1,2,3)}, {frozenset((1,x)) for x in (2,3)}, {frozenset((2,3))})
  self.assertEqual(set.union(*sets),E)
  self.assertEqual(sum(map(len,sets)),6)
 def test_808_graph_restricted_operations(self):
  E=[(1,2),(1,3),(2,4)]
  self.assertEqual({x+y for x,y in E},{3,4,6})
  self.assertEqual({x*y for x,y in E},{2,3,8})
 def test_814_threshold_induced_K4(self):
  E={frozenset(t) for t in choose(5,2)}-{frozenset((0,1))}
  self.assertEqual(len(E),9)
  self.assertEqual(sum(e<={1,2,3,4} for e in E),6)
 def test_816_K23_path_end_degrees(self):
  adj={v:set() for v in range(5)}
  for x in (0,1):
   for y in (2,3,4):adj[x].add(y);adj[y].add(x)
  self.assertEqual(sorted(len(x) for x in adj.values()),[2,2,2,3,3])
  for a,b,c,d in itertools.permutations(range(5),4):
   if b in adj[a] and c in adj[b] and d in adj[c]:
    self.assertNotEqual(len(adj[a]),len(adj[d]))
 def test_818_doubling_and_products(self):
  A=(1,2,3,4)
  self.assertEqual(len({x+y for x in A for y in A}),7)
  self.assertEqual(len({x*y for x in A for y in A}),9)
 def test_823_equal_sigma(self):
  self.assertEqual(sumdiv(6),sumdiv(11))
  self.assertEqual(sumdiv(14),sumdiv(15))

 def test_833_Fano_degree(self):
  E=[frozenset((i,(i+1)%7,(i+3)%7)) for i in range(7)]
  self.assertEqual(len(set(E)),7)
  self.assertEqual([sum(v in e for e in E) for v in range(7)],[3]*7)
 def test_841_t6_interval(self):
  sq=lambda n:math.isqrt(n)**2==n
  for t in range(6):
   self.assertFalse(any(sq(6*math.prod(sub)) for k in range(t+1) for sub in itertools.combinations(range(7,7+t),k)))
  self.assertEqual(6*8*12,24**2)
 def test_842_cycle_two_triangles(self):
  col=(0,1,2,2,0,1)
  E=((0,1),(1,2),(2,0),(3,4),(4,5),(5,3),(0,3),(3,1),(1,4),(4,2),(2,5),(5,0))
  self.assertTrue(all(col[u]!=col[v] for u,v in E))
 def test_843_square_subset_sums(self):
  A=(1,4,9);S={sum(c) for k in range(4) for c in itertools.combinations(A,k)}
  self.assertEqual(S,{0,1,4,5,9,10,13,14})
 def test_844_squarefree_pair_product_N10(self):
  squarefree=lambda n:all(n%(i*i) for i in range(2,math.isqrt(n)+1))
  self.assertEqual([n for n in range(1,11) if not squarefree(n)],[4,8,9])
  best=0
  for mask in range(1<<10):
   A=[j+1 for j in range(10) if (mask>>j)&1]
   if all(not squarefree(a*b) for a,b in itertools.combinations_with_replacement(A,2)):
    best=max(best,len(A))
  self.assertEqual(best,6)
 def test_845_smooth_5_7(self):
  self.assertEqual((2+3,3+4),(5,7))
  self.assertLess(3/2,6)
  self.assertLess(4/3,6)
 def test_846_no_three_collinear(self):
  P=((0,0),(0,1),(1,0),(1,3))
  self.assertTrue(all((b[0]-a[0])*(c[1]-a[1])!=(b[1]-a[1])*(c[0]-a[0]) for a,b,c in itertools.combinations(P,3)))
 def test_847_AP_free_three_of_four(self):
  A={1,2,3,4};free=lambda s:all(a+c!=2*b for a,b,c in itertools.combinations(sorted(s),3))
  self.assertFalse(free(A));self.assertTrue(free({1,2,4}))
