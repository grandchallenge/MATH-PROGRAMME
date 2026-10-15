"""EC-BULK-005 Erdős #732-741: exact finite source fixtures ONLY.
No claimed proof of asymptotic counts, infinite chromatic results,
relative consistency, or external Lean certificate.
"""
import itertools
import math
import unittest
from fractions import Fraction


def collinear(a,b,c):
    return (b[0]-a[0])*(c[1]-a[1]) == (c[0]-a[0])*(b[1]-a[1])


def unique_lines(points):
    # Each frozenset is the full rich-point incidence set for a line.
    out=set()
    for i,j in itertools.combinations(range(len(points)),2):
        on=frozenset(k for k in range(len(points))
                     if collinear(points[i],points[j],points[k]))
        out.add(on)
    return out


def fano():
    return [frozenset((i%7,(i+1)%7,(i+3)%7)) for i in range(7)]


class ExactFixtures(unittest.TestCase):
    def test_732_pairwise_balanced_designs(self):
        pairs=list(itertools.combinations(range(4),2))
        self.assertEqual(len(pairs),6)
        self.assertEqual(sum(math.comb(len(p),2) for p in pairs),
                         math.comb(4,2))
        lines=fano()
        self.assertEqual(len(set(lines)),7)
        self.assertTrue(all(sum(set(p).issubset(L) for L in lines)==1
                            for p in itertools.combinations(range(7),2)))

    def test_733_line_sequence_multiplicity(self):
        p3=[(0,0),(1,0),(0,1)]
        self.assertEqual(sorted(map(len,unique_lines(p3))),[2,2,2])
        generic=[(0,0),(1,0),(0,1),(2,3)]
        self.assertEqual(sorted(map(len,unique_lines(generic))),[2]*6)
        col3=[(0,0),(1,0),(2,0),(0,1)]
        self.assertEqual(sorted(map(len,unique_lines(col3))),[2,2,2,3])

    def test_734_size_frequency_pair_identity(self):
        L=fano()
        from collections import Counter
        counts=Counter(map(len,L))
        self.assertEqual(counts,{3:7})
        self.assertEqual(sum(c*math.comb(k,2) for k,c in counts.items()),21)
        self.assertEqual(math.comb(7,2),21)

    def test_735_positive_incidence_weights(self):
        generic=[(0,0),(1,0),(0,1),(2,3)]
        self.assertEqual({sum(1 for i in L) for L in unique_lines(generic)},
                         {2})
        col=[(i,0) for i in range(4)]+[(0,1)]
        weights=[1]*4+[3]
        self.assertEqual({sum(weights[i] for i in L)
                          for L in unique_lines(col)}, {4})
        self.assertTrue(all(w>0 for w in weights))

    def test_736_finite_patterns_not_infinitary_claim(self):
        # Purely a finite analogy, NOT a consistency test.
        edges=list(itertools.combinations(range(4),2))
        self.assertEqual(len(edges),6)
        self.assertEqual(sum(i<3 and j<3 for i,j in edges),3)

    def test_737_fixed_edge_cycles_in_K4(self):
        V=range(4)
        edge={0,1}
        lengths=set()
        for length in (3,4):
            for cyc in itertools.permutations(V,length):
                e=[{cyc[i],cyc[(i+1)%length]} for i in range(length)]
                if edge in e:
                    lengths.add(length)
        self.assertEqual(lengths,{3,4})

    def test_738_cycle_five_induced_tree_boundaries(self):
        edges={frozenset((i,(i+1)%5)) for i in range(5)}
        self.assertFalse(any(all(frozenset(e) in edges
                     for e in itertools.combinations(triple,2))
                     for triple in itertools.combinations(range(5),3)))
        self.assertTrue(all(sum(v in E for E in edges)==2 for v in range(5)))
        # Induced 3-vertex path 0-1-2.
        self.assertTrue(frozenset((0,1)) in edges)
        self.assertTrue(frozenset((1,2)) in edges)
        self.assertFalse(frozenset((0,2)) in edges)

    def test_739_finite_chromatic_subgraph_analogy(self):
        # K4 has 6 edges, a K3 subgraph has 3 edges.
        self.assertEqual(math.comb(4,2),6)
        self.assertEqual(math.comb(3,2),3)

    def test_740_triangle_free_not_five_cycle_free(self):
        edges={frozenset((i,(i+1)%5)) for i in range(5)}
        self.assertEqual(len(edges),5)
        self.assertFalse(any(all(frozenset(e) in edges
                            for e in itertools.combinations(t,2))
                            for t in itertools.combinations(range(5),3)))
        self.assertTrue(all(frozenset((i,(i+1)%5)) in edges for i in range(5)))

    def test_741_even_odd_partition_sumset_densities(self):
        A1={2*i for i in range(200)}
        A2={2*i+1 for i in range(200)}
        S1={a+b for a,b in itertools.product(range(0,100,2),repeat=2)}
        S2={a+b for a,b in itertools.product(range(1,100,2),repeat=2)}
        self.assertEqual({x for x in S1 if x<100},set(range(0,100,2)))
        self.assertEqual({x for x in S2 if x<100},set(range(2,100,2)))
        self.assertEqual(Fraction(len([x for x in range(100) if x%2==0]),100),
                         Fraction(1,2))
        self.assertFalse(A1&A2)


if __name__=="__main__":
    unittest.main(verbosity=2)
