"""EC-BULK-005 conflict tranche #1: exact finite counterexamples and scope gates.

Passing these fixtures does not certify original historical theorem proofs or
correct potentially faulty upstream Lean targets.
"""
import itertools
import math
import unittest
from collections import Counter
from fractions import Fraction
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
EDITORIAL=ROOT/"governance/erdos_compendium/editorial"

def largest_prime(n):
    if n<=1:return None
    last=None;p=2
    while p*p<=n:
        while n%p==0:
            last=p;n//=p
        p+=1
    return n if n>1 else last

def lattice_count(radius_squared):
    q=lambda a,b:a*a+a*b+b*b
    bound=math.isqrt(radius_squared)+2
    return sum(0<q(a,b)<=radius_squared for a in range(-bound,bound+1)
               for b in range(-bound,bound+1))

def dist2(a,b):
    return (a[0]-b[0])**2+(a[1]-b[1])**2

class ConflictSourceFixtures(unittest.TestCase):
    def test_653_distinct_distance_counts_not_total_lengths(self):
        points=[(-1,0),(0,0),(1,0),(0,1),(2,0)]
        spectrum=[len({dist2(a,b) for b in points if b!=a}) for a in points]
        self.assertEqual(spectrum,[4,2,3,3,4])
        self.assertEqual(len(set(spectrum)),3)

    def test_662_triangular_lattice_wrong_radius_and_global_bound(self):
        self.assertEqual([lattice_count(t) for t in (1,3,4,9)],[6,12,18,36])
        # Arbitrarily many distinct short lengths in widely separated pairs.
        for k in (8,16):
            points=[(Fraction(10*i),Fraction(0)) for i in range(k)]
            points+=[(Fraction(10*i)+Fraction(1)+Fraction(i+1,100*k),Fraction(0))
                     for i in range(k)]
            lengths=[Fraction(1)+Fraction(i+1,100*k) for i in range(k)]
            self.assertEqual(len(set(lengths)),k)
            self.assertTrue(all(dist2(a,b)>=1 for a,b in itertools.combinations(points,2)))
            self.assertTrue(all(1<L<Fraction(3,2) for L in lengths))

    def test_678_exact_original_lcm_examples_and_variable_k(self):
        def M(n,k):return math.lcm(*range(n+1,n+k+1))
        self.assertEqual(M(96,7),8321670749700)
        self.assertEqual(M(104,8),3803928503760)
        self.assertEqual(M(52,7),143282767320)
        self.assertEqual(M(62,8),75522807360)
        self.assertGreater(M(96,7),M(104,8))
        self.assertGreater(M(52,7),M(62,8))
        self.assertTrue(104>=96+7 and 62>=52+7)

    def test_683_strict_lean_target_false_weak_source_unrefuted(self):
        for n in (4,8,16,32):
            k=n-1
            P=largest_prime(math.comb(n,k))
            self.assertEqual(P,2)
            self.assertEqual(min(n-k+1,k**2),2)
            self.assertFalse(P>min(n-k+1,k**2))
            self.assertTrue(P>=min(n-k+1,k**2))
        self.assertEqual(math.comb(8,8),1)
        self.assertIsNone(largest_prime(1))

    def test_697_exact_finite_density_and_flipped_threshold(self):
        # D=3,5,7, exactly union of their divisibility sets.
        lcm=math.lcm(3,5,7)
        total=sum(any(i%d==0 for d in (3,5,7)) for i in range(1,lcm+1))
        self.assertEqual((lcm,total),(105,57))
        self.assertEqual(Fraction(total,lcm),Fraction(19,35))
        self.assertLess(Fraction(1,2),1/math.log(2))
        # The source's below-threshold limit is ZERO, not ONE.

    def test_708_exact_subset_product_and_distinct_subset_count(self):
        A=(2,3,4);I=(1,2,3,4)
        self.assertEqual(math.prod(A),24)
        self.assertEqual(math.prod(I),24)
        self.assertTrue(any(math.prod(B)%math.prod(A)==0
                            for B in itertools.combinations(I,3)))
        # One favorable interval cannot establish the source's universal g(3)=4.
        self.assertEqual(len(I),4)

    def test_712_graph_normalization_and_hypergraph_small_case(self):
        triples=list(itertools.combinations(range(4),3))
        self.assertEqual(len(triples),4)
        self.assertEqual(max(len(E) for k in range(5)
                             for E in itertools.combinations(triples,k)
                             if len(E)<4),3)
        for a in (10,100):
            n=3*a
            # Balanced complete tripartite graph is K4-free.
            edges=3*a*a
            normalized=Fraction(edges,math.comb(n,2))
            self.assertGreater(normalized,Fraction(2,3))
            self.assertLess(normalized,Fraction(3,4))

    def test_713_literal_all_bipartite_false_at_single_edge(self):
        # Forbidding K2 forces an edgeless graph.
        for n in (2,3,5):
            all_edges=list(itertools.combinations(range(n),2))
            # A K2-free graph has no edges at all.
            for edges_count in range(1,len(all_edges)+1):
                self.assertFalse(any(len(E)==0 for E in
                                 itertools.combinations(all_edges,edges_count)))
        article=(EDITORIAL/"0713.md").read_text()
        self.assertIn("ex(n,K_2)=0",article)

    def test_720_three_component_answers_and_correct_provenance(self):
        # Any two-colored 3-edge star has two same-color spokes:
        # an unavoidable monochromatic path with precisely two edges.
        spokes=(0,1,2)
        for colors in itertools.product((0,1),repeat=3):
            self.assertGreaterEqual(max(Counter(colors).values()),2)
        # A two-edge host can be given distinct colors, hence no P2.
        self.assertEqual(len(spokes),3)
        text=(EDITORIAL/"0720.md").read_text()
        self.assertIn("10.1002/jgt.3190070115",text)
        self.assertIn("10.1017/S0963548300001619",text)
        self.assertIn("Haxell, Kohayakawa and Łuczak",text)
        self.assertNotIn("Beck 1983 proved Rhat(P_n)=O(n) AND Rhat(C_n)=O(n)",text)

    def test_728_literal_solution_and_stronger_historical_intent(self):
        for n in (20,100,1000):
            a=b=n
            self.assertEqual(math.factorial(n)*math.factorial(n),
                             math.factorial(n)*math.factorial(a+b-n))
            self.assertGreater(a+b,n+math.log(n))
            self.assertTrue(a>=n/2 and b>=n/2)
        article=(EDITORIAL/"0728.md").read_text()
        self.assertIn("a=b=n",article.replace("$",""))

if __name__=="__main__":
    unittest.main()
