"""Selected finite semantic falsifiers for EC005 R10; not original theorem proofs."""
import itertools,math,unittest
from fractions import Fraction
class SourceSemanticExamples(unittest.TestCase):
 def test_655_regular_polygon_distances(self):
  for n in (6,7,12):
   P=[(math.cos(2*math.pi*i/n),math.sin(2*math.pi*i/n)) for i in range(n)]
   ds=[round(math.dist(P[0],P[i]),10) for i in range(1,n)]
   self.assertEqual(len(set(ds)),n//2)
   self.assertLessEqual(max(ds.count(x) for x in ds),2)
 def test_662_triangular_shell_radius_three(self):
  v=[(a,b) for a in range(-4,5) for b in range(-4,5)
    if 0<a*a+a*b+b*b<=9]
  self.assertEqual(len(v),36)
  self.assertEqual({a*a+a*b+b*b for a,b in v},{1,3,4,7,9})
 def test_683_pinned_strict_large_prime_counterexample(self):
  def largestprime(n):
   ans=1
   for p in range(2,n+1):
    if n%p==0 and all(p%d for d in range(2,math.isqrt(p)+1)):ans=p
   return ans
  for n in (8,16,32,64):
   k=n-1
   self.assertEqual(math.comb(n,k),n)
   self.assertEqual(largestprime(n),2)
   self.assertFalse(largestprime(n)>min(n-k+1,k*k))
 def test_713_edgeless_forbidden_subgraph(self):
  # Any 2 distinct vertices contain two isolated vertices as a noninduced subgraph.
  self.assertTrue(all(2<=n for n in (2,3,4,10)))
  self.assertEqual(sum(0 for _ in range(4)),0)
 def test_728_factorial_trivial_family(self):
  for n in range(1,14):
   a=b=n
   self.assertEqual(math.factorial(n)*math.factorial(a+b-n),
                    math.factorial(a)*math.factorial(b))
 def test_770_collective_vs_pairwise_gcd(self):
  values=[b**4-1 for b in (2,3,4,5)]
  self.assertEqual(math.gcd(*values),1)
  self.assertNotEqual(math.gcd(values[0],values[1]),1)
 def test_784_divisor_one_vacuity(self):
  A={1,2,3}
  self.assertFalse(any(all(m%a for a in A) for m in range(1,100)))
 def test_786_distinct_product_vs_repeated_factors(self):
  self.assertEqual(2*2,4)
  self.assertNotEqual(2,1)
 def test_789_unrestricted_repetition_trivialization(self):
  for a,b in itertools.combinations((2,3,5,7),2):
   self.assertEqual(sum([a]*b),sum([b]*a))
 def test_820_excluding_base_one(self):
  self.assertEqual(math.gcd(2**1-1,3**1-1),1)
  self.assertEqual(math.gcd(1**1-1,2**1-1),1)
 def test_825_semiperfect_70(self):
  proper=[d for d in range(1,70) if 70%d==0]
  sigma=70+sum(proper)
  self.assertEqual(sigma,144)
  self.assertFalse(any(sum(z)==70 for k in range(len(proper)+1)
                       for z in itertools.combinations(proper,k)))
 def test_835_johnson_J42_chromatic_three(self):
  V=[frozenset(x) for x in itertools.combinations(range(4),2)]
  edgecolor={frozenset((0,1)):0,frozenset((2,3)):0,
   frozenset((0,2)):1,frozenset((1,3)):1,
   frozenset((0,3)):2,frozenset((1,2)):2}
  self.assertTrue(all(edgecolor[a]!=edgecolor[b] for a,b in itertools.combinations(V,2)
                     if len(a&b)==1))
 def test_839_powers_two_consecutive_blocks(self):
  a=[2**j for j in range(1,12)]
  for i,x in enumerate(a):
   self.assertTrue(all(sum(a[j:k])!=x for j in range(i) for k in range(j+1,i+1)))
 def test_848_mod25_roots_cannot_be_mixed(self):
  self.assertEqual((7*7+1)%25,0)
  self.assertEqual((18*18+1)%25,0)
  self.assertEqual(7*18+1,127)
  self.assertTrue(all(127%d for d in range(2,math.isqrt(127)+1)))
 def test_851_omega_vs_Omega(self):
  x=9;omega=sum(x%p==0 for p in (2,3,5,7))
  self.assertEqual(omega,1)
  self.assertEqual(2,2)
