"""EC-BULK-005 original-source fixture review for #732–#741.

These are finite checks only. In particular, they cannot prove cardinal
independence, an infinitary chromatic statement, or source-proven
asymptotic theorems. Standard Python 3 library, no external packages.
"""
import itertools
import math
import unittest
from fractions import Fraction


def fano_lines():
    return [frozenset({j % 7, (j + 1) % 7, (j + 3) % 7})
            for j in range(7)]


def line_key(a,b):
    """Primitive integer normal a*x+b*y=c for two integer points."""
    x,y=a
    u,v=b
    A=v-y
    B=x-u
    C=A*x+B*y
    g=math.gcd(math.gcd(abs(A),abs(B)),abs(C))
    A,B,C=(A//g,B//g,C//g)
    if A<0 or (A==0 and B<0):
        A,B,C=-A,-B,-C
    return A,B,C


def triangle_free(edges):
    E={frozenset(e) for e in edges}
    vertices=set().union(*E)
    return not any(all(frozenset(e) in E
                       for e in itertools.combinations(t,2))
                   for t in itertools.combinations(vertices,3))


class EC005SourceFixtures(unittest.TestCase):
    def test_732_fano_block_compatibility_and_pair_budget(self):
        F=fano_lines()
        self.assertEqual(len(F),7)
        self.assertEqual(len(set(F)),7)
        for p in itertools.combinations(range(7),2):
            self.assertEqual(sum(set(p)<=L for L in F),1)
        self.assertEqual(sum(math.comb(len(L),2) for L in F),
                         math.comb(7,2))
        self.assertNotEqual(2*math.comb(2,2),math.comb(4,2))

    def test_733_four_square_point_line_multiplicity(self):
        P=[(0,0),(1,0),(0,1),(1,1)]
        lines={line_key(a,b) for a,b in itertools.combinations(P,2)}
        self.assertEqual(len(lines),6)
        occ=sorted(sum(A*x+B*y==C for x,y in P)
                   for A,B,C in lines)
        self.assertEqual(occ,[2]*6)

    def test_734_fano_block_size_histogram_finite_only(self):
        sizes=[len(x) for x in fano_lines()]
        self.assertEqual({t:sizes.count(t) for t in set(sizes)},{3:7})
        self.assertLessEqual(7,3*math.sqrt(7))

    def test_735_positive_magic_weights_general_and_three_plus_one(self):
        P=[(0,0),(1,0),(2,0),(0,1)]
        w=[1,1,1,2]
        lines={line_key(a,b) for a,b in itertools.combinations(P,2)}
        sums={sum(w[i] for i,(x,y) in enumerate(P) if A*x+B*y==C)
              for A,B,C in lines}
        self.assertEqual(sums,{3})
        self.assertTrue(all(x>0 for x in w))

    def test_736_finite_compatibility_not_infinitary_claim(self):
        # K3 contains smaller cliques as (ordinary) subgraphs.
        E={frozenset(p) for p in itertools.combinations(range(3),2)}
        self.assertEqual(len(E),3)
        self.assertIn(frozenset((0,1)),E)
        self.assertTrue(all(frozenset(p) in E
                            for p in itertools.combinations(range(3),2)))

    def test_737_K4_cycles_of_two_lengths_through_one_edge(self):
        # K4 has simple cycles length 3 and 4 through fixed edge 0--1.
        triangles=[(0,1,z,0) for z in (2,3)]
        squares=[(0,1,2,3,0),(0,1,3,2,0)]
        E={frozenset(p) for p in itertools.combinations(range(4),2)}
        self.assertTrue(all(all(frozenset((walk[i],walk[i+1])) in E
                                for i in range(len(walk)-1))
                            for walk in triangles+squares))
        self.assertEqual({len(c)-1 for c in triangles+squares},{3,4})

    def test_738_five_cycle_triangle_free_and_induced_P4(self):
        E={frozenset((i,(i+1)%5)) for i in range(5)}
        self.assertTrue(triangle_free(E))
        V=set([0,1,2,3])
        induced={e for e in E if e<=V}
        self.assertEqual(len(induced),3)
        self.assertEqual(sorted(sum(v in e for e in induced) for v in V),
                         [1,1,2,2])

    def test_739_finite_clique_subchromatic_examples(self):
        # K4 has K3 and K2 subgraphs, finite analogue only.
        E={frozenset(e) for e in itertools.combinations(range(4),2)}
        for n in (2,3):
            self.assertTrue(all(frozenset(e) in E for e in
                                itertools.combinations(range(n),2)))

    def test_740_odd_cycle_threshold_five_cycle(self):
        E={frozenset((i,(i+1)%5)) for i in range(5)}
        self.assertTrue(triangle_free(E))
        self.assertEqual(len(E),5)
        self.assertTrue(all(len(e)==2 for e in E))

    def test_741_even_odd_partition_sumsets_density(self):
        A1=[2*i for i in range(60)]
        A2=[2*i+1 for i in range(60)]
        s1={x+y for x in A1 for y in A1}
        s2={x+y for x in A2 for y in A2}
        self.assertEqual(len([x for x in range(100) if x in s1]),50)
        self.assertEqual(len([x for x in range(100) if x in s2]),49)
        self.assertTrue(all(x%2==0 for x in s1|s2))


if __name__=="__main__":
    unittest.main(verbosity=2)
