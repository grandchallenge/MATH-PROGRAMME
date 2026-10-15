"""Exact finite source fixtures for EC-BULK-005 Erdős #702-711.

Does not certify published theorems, chromatic asymptotics, or Lean proofs.
"""
import itertools
import math
import unittest


def matching_exists(n,m,F):
    candidates=range(m+1,m+F)
    def search(k,used):
        if k>n:
            return True
        return any(search(k+1,used|{x}) for x in candidates
                   if x not in used and x%k==0)
    return search(1,set())


def min_f(n,m,limit=80):
    return next(F for F in range(1,limit+1) if matching_exists(n,m,F))


class CohortChecks(unittest.TestCase):
    def test_702_fixed_pair_sharp_family(self):
        n,k=6,4
        F=[set(c) for c in itertools.combinations(range(n),k)
           if {0,1}.issubset(c)]
        self.assertEqual(len(F),math.comb(n-2,k-2))
        self.assertTrue(all(len(a&b)>=2
                            for a,b in itertools.combinations(F,2)))

    def test_703_small_cardinality_forbidden_intersections(self):
        X=range(5)
        r=2
        F=[set(c) for j in range(r)
           for c in itertools.combinations(X,j)]
        self.assertEqual(len(F),6)
        self.assertTrue(all(len(a&b)!=r
                            for a,b in itertools.combinations(F,2)))

    def test_704_real_line_two_coloring_fixture(self):
        for a in range(-5,6):
            for t in [0.0,0.2,0.75,0.999]:
                x=a+t
                self.assertNotEqual(math.floor(x)%2,
                                    math.floor(x+1)%2)

    def test_705_unit_triangle_has_short_cycle(self):
        # Three pairwise unit-separated points, so K3 has girth 3.
        points=[(0,0),(1,0),(0.5,math.sqrt(3)/2)]
        for i,j in itertools.combinations(range(3),2):
            self.assertTrue(math.isclose(math.dist(points[i],points[j]),1))
        self.assertEqual(math.comb(3,2),3)

    def test_706_two_lengths_can_form_K3(self):
        pts=[0,1,2]
        self.assertEqual({abs(a-b) for a,b in
                          itertools.combinations(pts,2)},{1,2})

    def test_707_sidon_and_positive_perfect_difference(self):
        A=[1,2,4,8,13]
        sums=[a+b for i,a in enumerate(A) for b in A[i:]]
        self.assertEqual(len(sums),15)
        self.assertEqual(len(set(sums)),15)
        B=[1,2,4]
        differences={(a-b)%7 for a,b in itertools.permutations(B,2)}
        self.assertEqual(differences,set(range(1,7)))

    def test_708_product_divisibility_finite_examples(self):
        self.assertEqual((2*3)%(2*3),0)
        self.assertEqual((1*2*3*4)%(2*3*4),0)

    def test_709_greedy_matching_nM_interval_fixture(self):
        A=[2,3,4]
        M=max(A)
        for start in range(1,15):
            used=set()
            for a in A:
                candidates=[x for x in range(start,start+len(A)*M)
                            if x%a==0 and x not in used]
                self.assertTrue(candidates)
                used.add(candidates[0])
            self.assertEqual(len(used),len(A))

    def test_710_open_interval_minimal_lengths(self):
        self.assertEqual([min_f(n,n) for n in range(1,5)],[2,3,4,6])
        self.assertFalse(matching_exists(4,4,5))

    def test_711_first_two_offsets(self):
        for m in range(1,30):
            self.assertEqual(min_f(1,m),2)
            self.assertEqual(min_f(2,m),3)


if __name__=="__main__":
    unittest.main(verbosity=2)
