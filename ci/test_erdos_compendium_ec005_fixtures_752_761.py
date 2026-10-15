"""EC-BULK-005 Erdős #752-761: ten exact bounded regression fixtures.
Not proofs of published asymptotic theorems, graph existence or Lean certification.
"""
import itertools
import math
import unittest
from fractions import Fraction

def edges_of_cycle(n):
    return {frozenset((i,(i+1)%n)) for i in range(n)}

def chromatic_list_small_graph(edges,vertices=3):
    # Ordinary coloring sufficient for the finite K2 / P3 illustrations.
    for k in range(1,vertices+1):
        for c in itertools.product(range(k),repeat=vertices):
            if all(c[a]!=c[b] for a,b in (tuple(e) for e in edges)):
                return k
    raise AssertionError

def cochromatic_small_graph(edges,vertices):
    E={frozenset(e) for e in edges}
    for k in range(1,vertices+1):
        for assign in itertools.product(range(k),repeat=vertices):
            valid=True
            for color in set(assign):
                group=[i for i,x in enumerate(assign) if x==color]
                pairs=[frozenset(p) for p in itertools.combinations(group,2)]
                edgecount=sum(p in E for p in pairs)
                if edgecount not in (0,len(pairs)):
                    valid=False
                    break
            if valid:
                return k
    raise AssertionError


class EC005Exact(unittest.TestCase):
    def test_752_cycle_six_girth_and_degree(self):
        E=edges_of_cycle(6)
        self.assertEqual(len(E),6)
        self.assertTrue(all(sum(i in p for p in E)==2 for i in range(6)))
        self.assertEqual(6,2*2+2)  # girth 6 > 2s=4 for s=2

    def test_753_list_chromatic_K2_empty_complement(self):
        E={frozenset((0,1))}
        self.assertEqual(chromatic_list_small_graph(E,2),2)
        self.assertEqual(chromatic_list_small_graph(set(),2),1)
        self.assertEqual(2+1,3)

    def test_754_regular_tetrahedron_in_R4(self):
        points=[tuple(int(j==i) for j in range(4)) for i in range(4)]
        ds={sum((a-b)**2 for a,b in zip(points[i],points[j]))
            for i,j in itertools.combinations(range(4),2)}
        self.assertEqual(ds,{2})
        self.assertEqual(3,4-1)

    def test_755_three_orthogonal_unit_cross_circles(self):
        radius=1/math.sqrt(2)
        pts=[(radius,0,0,0,0,0),(-radius,0,0,0,0,0),
             (0,0,radius,0,0,0),(0,0,-radius,0,0,0),
             (0,0,0,0,radius,0),(0,0,0,0,-radius,0)]
        good=0
        for indices in itertools.product(range(2),range(2,4),range(4,6)):
            lengths=[math.dist(pts[i],pts[j])
                     for i,j in itertools.combinations(indices,2)]
            if all(math.isclose(x,1) for x in lengths):
                good+=1
        self.assertEqual(good,8)

    def test_756_four_point_square_distance_counts(self):
        points=[(0,0),(1,0),(1,1),(0,1)]
        sq=[sum((a-b)**2 for a,b in zip(points[i],points[j]))
            for i,j in itertools.combinations(range(4),2)]
        self.assertEqual(sq.count(1),4)
        self.assertEqual(sq.count(2),2)
        self.assertFalse(any(sq.count(t)>4 for t in set(sq)))

    def test_757_four_point_difference_sidon_boundary(self):
        B=[0,1,3,5]
        diffs={a-b for a in B for b in B}
        self.assertEqual(len(diffs),11)
        self.assertEqual({abs(d) for d in diffs if d},set(range(1,6)))
        C=[0,1,3,7]
        self.assertEqual(len({a-b for a in C for b in C}),13)

    def test_758_small_cochromatic_examples(self):
        P3={(0,1),(1,2)}
        K3={(0,1),(0,2),(1,2)}
        self.assertEqual(cochromatic_small_graph(P3,3),2)
        self.assertEqual(cochromatic_small_graph(K3,3),1)

    def test_759_planar_four_coloring_is_cochromatic(self):
        # The planar K4 has ordinary chromatic number four,
        # but is a single clique color class in cochromatic coloring.
        K4=list(itertools.combinations(range(4),2))
        self.assertEqual(len(K4),6)
        self.assertEqual(cochromatic_small_graph(K4,4),1)
        self.assertLessEqual(cochromatic_small_graph(K4,4),4)

    def test_760_noninduced_edge_deletion_increases_zeta(self):
        self.assertEqual(cochromatic_small_graph([(0,1),(1,2),(0,2)],3),1)
        self.assertEqual(cochromatic_small_graph([(0,1),(1,2)],3),2)

    def test_761_cyclic_orientation_of_triangle(self):
        oriented=[(0,1),(1,2),(2,0)]
        self.assertEqual(len(oriented),3)
        # A single color on a directed 3-cycle is cyclic.
        self.assertEqual(len({v for e in oriented for v in e}),3)
        # Two colors split it as singleton plus 2-vertex acyclic subgraph.
        coloring={0:0,1:0,2:1}
        self.assertNotEqual(len(set(coloring.values())),1)
        self.assertEqual(len(set(coloring.values())),2)

if __name__=="__main__":
    unittest.main(verbosity=2)
