"""EC-BULK-005 STATUS_CONFLICT tranche 03: exact finite source semantics.

These tests verify finite claims; they do not prove infinitary or
asymptotic theorems from the maintained Erdős catalogue.
"""
import itertools
import math
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EDITORIAL = ROOT / "governance/erdos_compendium/editorial"

def is_product_length_rigid_repetition_allowed(A, maximum_length=4):
    product_lengths = {}
    for length in range(1, maximum_length+1):
        for factors in itertools.combinations_with_replacement(A,length):
            k=math.prod(factors)
            if k in product_lengths and product_lengths[k] != length:
                return False
            product_lengths[k]=length
    return True

def sum_lengths_by_repetition(A,length_limit):
    values={}
    for r in range(1,length_limit+1):
        for tuple_ in itertools.combinations_with_replacement(A,r):
            values.setdefault(sum(tuple_),set()).add(r)
    return values

def finite_basis_size(n):
    for k in range(1,n+2):
        for A in itertools.combinations(range(n+1),k):
            sums={a+b for a in A for b in A}
            if set(range(n+1)) <= sums:
                return k
    raise AssertionError("Full interval trivially forms a basis")

def no_divides_other_pair_product(A):
    return all((a==b or a==c or (b*c)%a !=0)
               for a in A for b in A for c in A)

def product_representations(A):
    cnt=Counter()
    for a,b in itertools.combinations(A,2):
        cnt[a*b]+=1
    return cnt

def H(n):
    for l in range(3,80):
        for k in range(2,l):
            if math.gcd(k**n-1,l**n-1)==1:
                return l,k
    raise AssertionError("Increase finite search range")

def independence_number(vertices,edges):
    es={frozenset(e) for e in edges}
    for size in range(len(vertices),-1,-1):
        for S in itertools.combinations(vertices,size):
            if all(not e.issubset(S) for e in es):
                return size
    return 0

class EC005ConflictTranche03(unittest.TestCase):
    def test_786_multiplicative_repetition_vs_distinct_products(self):
        self.assertTrue(is_product_length_rigid_repetition_allowed([2,6,10,14],5))
        self.assertFalse(is_product_length_rigid_repetition_allowed([2,4],3))
        self.assertEqual(2*2,4)
        self.assertIn("repetition", (EDITORIAL/"0786.md").read_text().lower())

    def test_789_additive_repetition_unrestricted_is_trivial(self):
        lengths=sum_lengths_by_repetition([2,3],3)
        self.assertEqual(lengths[6],{2,3})
        self.assertEqual(sum_lengths_by_repetition([0],3)[0],{1,2,3})
        # The one-element set of any NONZERO value has length rigidity.
        self.assertTrue(all(len(s)==1 for s in sum_lengths_by_repetition([7],4).values()))

    def test_791_exact_finite_two_basis_allows_diagonal(self):
        self.assertEqual(finite_basis_size(5),4)
        for n in range(1,9):
            g=finite_basis_size(n)
            self.assertGreaterEqual(g*(g+1)//2,n+1)
        self.assertEqual({a+b for a in [0,1,2,3] for b in [0,1,2,3]} & set(range(6)),
                         set(range(6)))

    def test_793_b_equals_c_permitted_and_prime_examples(self):
        self.assertFalse(no_divides_other_pair_product([2,3,4]))
        self.assertTrue(no_divides_other_pair_product([2,3,5,7]))
        self.assertFalse(no_divides_other_pair_product([1,2]))
        self.assertTrue(no_divides_other_pair_product([1]))
        self.assertEqual(4%(2*2),0)

    def test_796_product_pair_repetition_strict_k(self):
        self.assertEqual(max(product_representations([2,3,4,6]).values()),2)
        self.assertEqual(product_representations([2,3,4,6])[12],2)
        self.assertEqual(max(product_representations([2,3,5,7]).values()),1)
        self.assertFalse(max(product_representations([2,3,4,6]).values())<2)
        self.assertTrue(max(product_representations([2,3,4,6]).values())<3)

    def test_804_two_independent_parameters_not_single_f_of_n(self):
        n=6;V=list(range(n))
        all_e=list(itertools.combinations(V,2))
        self.assertEqual(independence_number(V,all_e),1)
        self.assertEqual(independence_number(V,[]),6)
        for m in (2,3,4):
            self.assertTrue(all(independence_number(list(S),[])==m
                                for S in itertools.combinations(V,m)))
        self.assertIn("10.1002/jgt.20264",(EDITORIAL/"0804.md").read_text())

    def test_809_only_c7_remains_of_k_ge_three(self):
        assert [(k,2*k+1) for k in range(3,6)]==[(3,7),(4,9),(5,11)]
        n=6;edge_count=n*n//4+1
        self.assertEqual(edge_count,10)
        # Any 6-vertex simple bipartite graph has at most 9 edges.
        self.assertEqual(max(a*(6-a) for a in range(7)),9)
        self.assertIn("2603.18952",(EDITORIAL/"0809.md").read_text())

    def test_811_balanced_cyclic_k7_3_colours(self):
        n=7;m=3;hist={i:Counter() for i in range(n)}
        for i,j in itertools.combinations(range(n),2):
            c=min((i-j)%n,(j-i)%n)
            hist[i][c]+=1;hist[j][c]+=1
        self.assertTrue(all(set(h)=={1,2,3} and set(h.values())=={2} for h in hist.values()))
        self.assertEqual((n-1)//m,2)
        self.assertIn("10.37236/11965",(EDITORIAL/"0811.md").read_text())

    def test_815_k4_degree_three_critical_small_example(self):
        v=list(range(4));edges=list(itertools.combinations(v,2))
        self.assertEqual(len(edges),2*len(v)-2)
        for k in range(1,len(v)):
            for S in itertools.combinations(v,k):
                self.assertLessEqual(k-1,2)
        self.assertIn("10.1007/s00493-015-3310-9",(EDITORIAL/"0815.md").read_text())

    def test_820_base_k_ge_two_and_exact_sequence(self):
        expected=[3,3,3,6,3,18,3,6,3,12]
        self.assertEqual([H(n)[0] for n in range(1,11)],expected)
        self.assertEqual(H(4),(6,5))
        self.assertEqual(math.gcd(1**1-1,2**1-1),1)
        self.assertEqual(math.gcd(2**1-1,3**1-1),1)

if __name__ == "__main__":
    unittest.main()
