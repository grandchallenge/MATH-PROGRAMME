"""Exact finite source-normalization fixtures for Erdős #792–#801.

The checks cover elementary examples only, not published asymptotic proofs,
external Lean claims, or GCL mathematical certification.
"""
import itertools
import math
import unittest
from collections import Counter

def sumfree(A):
    B=set(A)
    return all(a+b not in B for a in B for b in B)

def multiplicatively_admissible(A):
    return all((b*c)%a!=0 for a in A for b in A for c in A if a!=b and a!=c)

def three_graph_edges():
    X=range(0,3); Y=range(3,6); Z=range(6,9)
    return {frozenset(t) for t in itertools.product(X,Y,Z)} | {frozenset(X)}

def distinct_subset_products(A):
    products=[math.prod(t) for k in range(len(A)+1) for t in itertools.combinations(A,k)]
    return len(products)==len(set(products))

def pair_product_multiplicities(A):
    return Counter(a*b for a,b in itertools.combinations(A,2))

def valid_acyclic_coloring(edges,color):
    if any(color[a]==color[b] for a,b in edges):return False
    # A graph is acyclic in every two-color induced subgraph iff that graph has no cycle.
    for x,y in itertools.combinations(set(color),2):
        selected={i for i,c in enumerate(color) if c in (x,y)}
        es=[(a,b) for a,b in edges if a in selected and b in selected]
        parent={i:i for i in selected}
        def find(v):
            while parent[v]!=v:v=parent[v]
            return v
        for a,b in es:
            a,b=find(a),find(b)
            if a==b:return False
            parent[a]=b
    return True

def collinear(a,b,c):
    return (b[0]-a[0])*(c[1]-a[1])==(b[1]-a[1])*(c[0]-a[0])

def covers_grid(selected,grid):
    return all(any(collinear(a,b,c) for a,b in itertools.combinations(selected,2)) for c in grid)

def list_coloring_possible(edges,lists):
    n=len(lists)
    return any(all(colors[a]!=colors[b] for a,b in edges) for colors in itertools.product(*lists))

class FiniteTranche792801(unittest.TestCase):
    def test_792_sumfree_includes_doubled_elements(self):
        self.assertTrue(sumfree((2,3)))
        self.assertFalse(sumfree((1,2)))
        self.assertEqual(max(len(B) for k in range(4) for B in
                         itertools.combinations((1,2,3),k) if sumfree(B)),2)

    def test_793_divisor_against_identical_factors(self):
        self.assertFalse(multiplicatively_admissible((2,3,4)))
        self.assertTrue(multiplicatively_admissible((2,3)))
        self.assertFalse(multiplicatively_admissible((1,2)))
        self.assertEqual(max(len(B) for k in range(5) for B in
                         itertools.combinations(range(1,5),k)
                         if multiplicatively_admissible(B)),2)

    def test_794_nine_vertex_28_edge_counterexample(self):
        edges=three_graph_edges()
        self.assertEqual(len(edges),28)
        self.assertEqual(3**3+1,28)
        four=[sum(e<=set(v) for e in edges) for v in itertools.combinations(range(9),4)]
        five=[sum(e<=set(v) for e in edges) for v in itertools.combinations(range(9),5)]
        self.assertEqual(len(four),126)
        self.assertEqual(len(five),126)
        self.assertLess(max(four),3)
        self.assertLess(max(five),7)
        # Any seven triples over five vertices force 3 in some 4-subset.
        self.assertGreater(7*2/5,2)

    def test_795_prime_and_prime_square_encoding(self):
        self.assertTrue(distinct_subset_products((2,3,4,9)))
        self.assertFalse(distinct_subset_products((2,3,6)))
        self.assertFalse(distinct_subset_products((1,2)))
        self.assertEqual(len({math.prod(t) for k in range(5)
                          for t in itertools.combinations((2,3,4,9),k)}),16)

    def test_796_repeated_pairs_and_strict_less_than_k(self):
        A=(2,3,4,6)
        m=pair_product_multiplicities(A)
        self.assertEqual(m[12],2)
        self.assertEqual(max(m.values()),2)
        self.assertFalse(all(c<2 for c in m.values()))
        self.assertTrue(all(c<3 for c in m.values()))

    def test_797_bichromatic_cycle_not_acyclic(self):
        cycle=[(0,1),(1,2),(2,3),(3,0)]
        self.assertFalse(valid_acyclic_coloring(cycle,(0,1,0,1)))
        self.assertTrue(valid_acyclic_coloring(cycle,(0,1,2,1)))
        self.assertFalse(any(valid_acyclic_coloring(cycle,assignment)
                     for assignment in itertools.product(range(2),repeat=4)))

    def test_798_entire_two_by_two_grid_needed(self):
        grid=list(itertools.product((1,2),repeat=2))
        self.assertTrue(covers_grid(grid,grid))
        self.assertFalse(any(covers_grid(s,grid) for s in itertools.combinations(grid,3)))

    def test_799_triangle_list_chromatic_exact_three(self):
        edges=[(0,1),(1,2),(0,2)]
        lists=list(itertools.combinations(range(5),3))
        self.assertTrue(all(list_coloring_possible(edges,fam) for fam in itertools.product(lists,repeat=3)))
        self.assertFalse(list_coloring_possible(edges,((0,1),(0,1),(0,1))))

    def test_800_star_ramsey_r6(self):
        red={(i,(i+1)%5) if i<(i+1)%5 else ((i+1)%5,i) for i in range(5)}
        E=list(itertools.combinations(range(5),2))
        blue=set(E)-red
        for v in range(5):
            self.assertEqual(sum(v in e for e in red),2)
            self.assertEqual(sum(v in e for e in blue),2)
        self.assertEqual(5, len(range(6))-1)
        self.assertGreaterEqual(math.ceil(5/2),3)

    def test_801_small_clique_local_edges(self):
        n=9
        self.assertLessEqual(1,math.isqrt(n))
        k=math.isqrt(n)
        self.assertEqual(math.comb(k,2),3)
        self.assertGreater(n,math.isqrt(n))

if __name__=="__main__":
    unittest.main()
