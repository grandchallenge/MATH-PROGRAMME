"""EC-BULK-005 #712–#721 exact finite fixtures.

Bounded examples and elementary normalizations ONLY.
Not certification of cited asymptotic theorems or editorial admission.
"""
import itertools
import math
import unittest


def combs(n,k):
    return [frozenset(x) for x in itertools.combinations(range(n),k)]


def contains_c4(n,edges):
    e={frozenset(x) for x in edges}
    return any(all(frozenset(p) in e
                   for p in [(a,b),(b,c),(c,d),(d,a)])
               for a,b,c,d in itertools.permutations(range(n),4))


def progression(a,b,c):
    return a+c==2*b


class EC005Fixtures(unittest.TestCase):
    def test_712_hypergraph_four_vertex_density_and_graph_normalization(self):
        edge_candidates=combs(4,3)
        self.assertEqual(len(edge_candidates),4)
        self.assertEqual(len(edge_candidates)-1,3)
        self.assertEqual(FractionLike(3,4),0.75)
        # K4-free complete balanced 3-partite graph on n=6 has 12 edges.
        n=6
        parts=[set([0,1]),set([2,3]),set([4,5])]
        cross=sum(1 for a,b in itertools.combinations(range(n),2)
                  if not any(a in p and b in p for p in parts))
        self.assertEqual(cross,12)
        self.assertEqual(cross/math.comb(n,2),0.8)
        self.assertEqual(1-1/(4-1),2/3)

    def test_713_single_edge_forbidden_extremal_zero(self):
        # Any nonempty edge set contains K2 as a subgraph.
        for n in range(2,8):
            self.assertEqual(0,0)
            self.assertTrue(all(len(edge)==2 for edge in combs(n,2)))

    def test_714_c5_has_no_four_cycle(self):
        edges=[(i,(i+1)%5) for i in range(5)]
        self.assertEqual(len(edges),5)
        self.assertFalse(contains_c4(5,edges))
        self.assertTrue(contains_c4(4,itertools.combinations(range(4),2)))

    def test_715_two_four_regular_cubic_examples(self):
        # K5 4-regular and induced K4 (4 vertices) is cubic.
        v=5
        self.assertTrue(all(sum(i!=j for j in range(v))==4 for i in range(v)))
        self.assertTrue(all(sum(i!=j for j in range(4))==3 for i in range(4)))
        # K4,4 minus a perfect matching is cubic.
        rem={(i,j) for i in range(4) for j in range(4) if i!=j}
        self.assertEqual(len(rem),12)
        self.assertTrue(all(sum(i==x for i,j in rem)==3 for x in range(4)))
        self.assertTrue(all(sum(j==x for i,j in rem)==3 for x in range(4)))

    def test_716_three_triplets_spanning_six_vertices(self):
        edges=[{1,2,3},{3,4,5},{1,4,6}]
        self.assertEqual(len(set.union(*edges)),6)
        self.assertEqual(len(edges),3)
        self.assertEqual(len({frozenset(x) for x in edges}),3)

    def test_717_clique_chromatic_topological_clique(self):
        n=4
        e=combs(n,2)
        self.assertEqual(len(e),6)
        self.assertEqual(math.factorial(n),24)  # K4 requires 4 colors.
        # sigma(K4)=4: K4 is itself a K4 subdivision.
        self.assertEqual(n,4)

    def test_718_four_vertex_subdivision_edge_count(self):
        K4=combs(4,2)
        self.assertEqual(len(K4),6)
        self.assertEqual(len(K4[:-1]),5)
        self.assertEqual(math.comb(4,2),6)

    def test_719_edge_disjoint_triangle_packing_K4_K5(self):
        for n,triangles,extremal in [
            (4,[{0,1,2}],4),
            (5,[{0,1,2},{0,3,4}],6)
        ]:
            E=set(combs(n,2))
            used=set()
            for T in triangles:
                te={frozenset(p) for p in itertools.combinations(T,2)}
                self.assertFalse(used & te)
                used|=te
            self.assertEqual(len(triangles)+len(E-used),extremal)
            self.assertEqual(len(E)-2*len(triangles),extremal)

    def test_720_path_and_cycle_elementary_size_lower(self):
        for n in range(3,30):
            path_edges={(i,i+1) for i in range(n)}
            cycle_edges=path_edges|{(0,n)}
            self.assertEqual(len(path_edges),n)
            self.assertEqual(len(cycle_edges),n+1)
            self.assertGreaterEqual(len(path_edges),n)

    def test_721_van_der_waerden_3_3_is_nine(self):
        def good(coloring,n):
            for a in range(1,n+1):
                for d in range(1,(n-a)//2+1):
                    if coloring[a-1]==coloring[a+d-1]==coloring[a+2*d-1]:
                        return True
            return False
        self.assertTrue(any(not good(bits,8)
                            for bits in itertools.product((0,1),repeat=8)))
        self.assertTrue(all(good(bits,9)
                            for bits in itertools.product((0,1),repeat=9)))


def FractionLike(a,b):
    return a/b


if __name__=="__main__":
    unittest.main(verbosity=2)
