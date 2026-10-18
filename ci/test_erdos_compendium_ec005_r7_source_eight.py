"""R7 eight authenticated source interfaces; elementary checks only."""
import itertools,math,unittest
from pathlib import Path
P=Path(__file__).resolve().parents[1]/"governance/erdos_compendium/editorial"
class Eight(unittest.TestCase):
 def test_717_topological_clique_K4(self):
  self.assertEqual(math.comb(4,2),6)
  self.assertEqual(4,4)
  self.assertIn("Fox", (P/"0717.md").read_text())
 def test_718_K4_edge_threshold(self):
  self.assertEqual(math.comb(4,2),6)
  self.assertEqual(2*4-2,6)
  self.assertEqual(6-1,5)
 def test_722_fano_exact_pair_design(self):
  triples=[{i,(i+1)%7,(i+3)%7} for i in range(7)]
  pairs=[tuple(sorted(x)) for B in triples for x in itertools.combinations(B,2)]
  self.assertEqual(len(pairs),21);self.assertEqual(len(set(pairs)),21)
  self.assertEqual(math.comb(7,2)//math.comb(3,2),7)
 def test_747_matching_on_six_vertices(self):
  matchings={frozenset((frozenset(A),frozenset(set(range(6))-set(A)))) for A in itertools.combinations(range(6),3)}
  self.assertEqual(len(matchings),10)
  self.assertTrue(all(len(e)==2 and len(set.union(*(set(x) for x in e)))==6 for e in matchings))
 def test_748_sumfree_repetition_allowed(self):
  def sumfree(A):return not any(a+b in A for a in A for b in A)
  for n in range(2,9):
   upper=list(range(n//2+1,n+1))
   self.assertTrue(all(sumfree(set(z)) for k in range(len(upper)+1) for z in itertools.combinations(upper,k)))
   f=sum(sumfree({j+1 for j in range(n) if bits>>j&1}) for bits in range(1<<n))
   self.assertGreaterEqual(f,2**len(upper))
  self.assertFalse(sumfree({1,2}))
 def test_763_ordered_two_sum(self):
  A={1,2,3}
  c=[sum(a+b==n for a in A for b in A) for n in range(2,7)]
  self.assertEqual(c,[1,2,3,2,1]);self.assertEqual(sum(c),9)
 def test_776_antichain_occupied_level(self):
  F=[{1,2},{3,4}]
  self.assertTrue(all(not (A<B or B<A) for A,B in itertools.combinations(F,2)))
  self.assertEqual({len(x) for x in F},{2})
  self.assertEqual(len(F),2)
 def test_777_boolean_lattice_strict_comparability(self):
  F=[frozenset(),frozenset((1,)),frozenset((2,)),frozenset((1,2))]
  c=sum(A<B or B<A for A,B in itertools.combinations(F,2))
  self.assertEqual(c,5);self.assertEqual(math.comb(len(F),2),6)
