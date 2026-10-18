"""Exact hostile and positive tests of B3 additive-shadow and moment constraints.

Finite evidence only: the universal mathematical proofs are in
research/erdos-41-density/ADDITIVE_SHADOW_MOMENTS.md.
"""
from itertools import combinations, combinations_with_replacement as multisets
from math import comb
from random import Random
import unittest
from tests.test_erdos41_cross_patterns import hall


def b3(values):
    triples = [sum(t) for t in multisets(values, 3)]
    return len(triples) == len(set(triples))


def pair_sums(values):
    return {sum(t) for t in multisets(values, 2)}


def shadow(values):
    return {p - x for p in pair_sums(values) for x in values}


def difference(values):
    return {a-b for a in values for b in values}


def cubic_shadow_count(n):
    return (n**3 - n**2 + 2*n)//2


def moment_slack(values):
    n = len(values)
    return 12*(n*sum(v*v for v in values) - sum(values)**2) - n*n*(n*n-1)


class AdditiveShadowTests(unittest.TestCase):
    def test_exact_cubic_shadow_formula_exhaustive_small_m3(self):
        count = 0
        for n in range(1, 5):
            for X in combinations(range(1, 15), n):
                if not b3(X):
                    continue
                count += 1
                self.assertEqual(len(shadow(X)), cubic_shadow_count(n))
                self.assertTrue(set(X).issubset(shadow(X)))
                D = max(X)-min(X)
                self.assertLessEqual(cubic_shadow_count(n), 3*D+1)
        self.assertGreater(count, 120)

    def test_cross_shadows_disjoint_on_real_m3_fixtures(self):
        A=(1,2,5,14,33,72,125,219,376,573,745,1209,1557,2442,3098,
           4048,5298,6704,7839,10987,12332,15465,19144,24546,28974,
           34406,37769,45864,50877)
        self.assertTrue(b3(A))
        chunks=[A[i:i+4] for i in range(0,len(A),4)]
        shadows=[shadow(x) for x in chunks]
        self.assertEqual(sum(map(len,shadows)),len(set().union(*shadows)))
        for X in chunks:
            self.assertEqual(len(shadow(X)), cubic_shadow_count(len(X)))
        for X in chunks:
            for Y in chunks:
                if X is Y or not X or not Y:continue
                PX=pair_sums(X)
                self.assertEqual(difference(PX).intersection(difference(Y)),{0})
                H=max(Y)-min(Y)
                in_window=sum(-H<=d<=H for d in difference(PX))
                self.assertLessEqual(in_window+len(Y)*(len(Y)-1),2*H+1)

    def test_joint_moment_strictly_stronger_than_shell_hall(self):
        X=(10,13)
        Y=(16,17)
        self.assertTrue(b3(X))
        self.assertTrue(b3(Y))
        patterns=list(multisets((3,4),3))
        for mask in range(1,16):
            subset=[p for i,p in enumerate(patterns) if mask >> i & 1]
            count,available=hall(subset,{3:2,4:2})
            self.assertLessEqual(count,available)
        P=sorted(pair_sums(X))
        Q=sorted(pair_sums(Y))
        s1=[p+y for p in P for y in Y]
        s2=[x+q for x in X for q in Q]
        self.assertEqual(len(s1),len(set(s1)))
        self.assertEqual(len(s2),len(set(s2)))
        self.assertEqual(moment_slack(s1),1440)
        self.assertEqual(moment_slack(s2),0)
        self.assertEqual(moment_slack(s1+s2),-1872)
        self.assertEqual(shadow(X).intersection(shadow(Y)),{16})
        self.assertEqual(set(s1).intersection(s2),{42,43})

    def test_single_pattern_moment_excludes_hall_feasible_arrangement(self):
        X=(9,12,13); Y=(16,20)
        P=sorted(pair_sums(X))
        s=[p+y for p in P for y in Y]
        self.assertTrue(b3(X))
        self.assertTrue(b3(Y))
        self.assertEqual(len(s),12)
        self.assertEqual(len(set(s)),9)
        self.assertEqual(moment_slack(s),-1200)
        self.assertLessEqual(len(s), 4*8-2)

    def test_distinct_integer_moment_bound_exact_integer_arithmetic(self):
        rng=Random(41)
        for n in range(1,19):
            for _ in range(100):
                values=rng.sample(range(-100,100),n)
                self.assertGreaterEqual(moment_slack(values),0)
            self.assertEqual(moment_slack(list(range(7,7+n))),0)

    def test_old_hall_counterprofile_fails_actual_cubic_shadow(self):
        X=tuple((1<<21)+i for i in range(8))
        self.assertFalse(b3(X))
        self.assertEqual(cubic_shadow_count(len(X)),232)
        self.assertEqual(len(shadow(X)),22)
        self.assertEqual(3*(max(X)-min(X))+1,22)
        self.assertGreater(cubic_shadow_count(len(X)),len(shadow(X)))

    def test_zeroth_and_one_element_boundaries(self):
        self.assertEqual(cubic_shadow_count(0),0)
        self.assertEqual(cubic_shadow_count(1),1)
        self.assertEqual(shadow((7,)),{7})
        self.assertEqual(moment_slack([]),0)

if __name__=="__main__":
    unittest.main()
