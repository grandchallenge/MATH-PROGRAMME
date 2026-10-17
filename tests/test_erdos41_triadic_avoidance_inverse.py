"""Exact triadic arithmetic-avoidance certificates for Erdős #41.

Research-only: proves finite B2/B3 weighted gap-triangle bounds, not
the unresolved persistent-density or multiscale deduction.
Run: python -m unittest discover -s tests -p 'test_erdos41_triadic_avoidance_inverse.py' -v
"""
from collections import Counter, defaultdict
from itertools import combinations, combinations_with_replacement
from math import comb
import unittest

A = [
    1, 2, 5, 14, 33, 72, 125, 219, 376, 573, 745,
    1209, 1557, 2442, 3098, 4048, 5298, 6704, 7839,
    10987, 12332, 15465, 19144, 24546, 28974,
    34406, 37769, 45864, 50877,
]


def is_b2(xs):
    sums = [sum(t) for t in combinations_with_replacement(xs, 2)]
    return len(sums) == len(set(sums))


def is_b3(xs):
    sums = [sum(t) for t in combinations_with_replacement(xs, 3)]
    return len(sums) == len(set(sums))


def pair_sums(u):
    return {a+b for a,b in combinations_with_replacement(sorted(u), 2)}


def half_difference_weights(u, L):
    p = pair_sums(u)
    return Counter({
        h: sum(p0-2*h in p for p0 in p)
        for h in range(1, L+1)
    })


def weighted_correlation(r, w):
    return sum(r[b-a] for a,b in combinations(sorted(w), 2))


def triangle_candidates(r, L):
    return sorted(
        (r[a]+r[b]+r[a+b],a,b)
        for a in range(1, L)
        for b in range(1, L-a+1)
        if a != b
    )


def triadic_certificate(u, w, threshold=1):
    assert len(w)>=3 and is_b2(w)
    L=max(w)-min(w)
    r=half_difference_weights(u,L)
    observed=weighted_correlation(r,w)
    m=len(w)
    candidates=triangle_candidates(r,L)
    k=comb(m,3)
    assert len(candidates)>=k
    bound_numerator=sum(x[0] for x in candidates[:k])
    good=sum(1 for cost,a,b in candidates if
             r[a]<threshold and r[b]<threshold and r[a+b]<threshold)
    threshold_lower=max(0,threshold*(k-good))
    return r,observed,bound_numerator,threshold_lower,candidates


def three_bin_certificate(u,Y,Z,V,Q):
    assert max(Y)<min(Z)<max(V) and max(Z)<min(V)
    assert is_b2(Y+Z+V)
    low_a,min_hi_a=min(Z)-max(Y),max(Z)-min(Y)
    low_b,min_hi_b=min(V)-max(Z),max(V)-min(Z)
    low_sum,high_sum=min(V)-max(Y),max(V)-min(Y)
    r=half_difference_weights(u, high_sum)
    weight_candidates=defaultdict(list)
    for a in range(low_a,min_hi_a+1):
        for b in range(low_b,min_hi_b+1):
            if a==b or not low_sum<=a+b<=high_sum:
                continue
            weight_candidates[(a%Q,b%Q)].append(
                r[a]+r[b]+r[a+b]
            )
    occupancy=Counter(
        ((z-y)%Q,(v-z)%Q)
        for y in Y for z in Z for v in V
    )
    bound=0
    zero_capacity={}
    for cls,k in occupancy.items():
        weights=sorted(weight_candidates[cls])
        assert len(weights)>=k
        bound+=sum(weights[:k])
        zero_capacity[cls]=sum(value==0 for value in weights)
    observed=sum(
        r[z-y]+r[v-z]+r[v-y]
        for y in Y for z in Z for v in V
    )
    myz=sum(r[z-y] for y in Y for z in Z)
    mzv=sum(r[v-z] for z in Z for v in V)
    myv=sum(r[v-y] for y in Y for v in V)
    assert observed==len(V)*myz+len(Y)*mzv+len(Z)*myv
    return observed,bound,occupancy,zero_capacity,(myz,mzv,myv)


class TriadicAvoidanceTests(unittest.TestCase):
    def test_b3_fixture(self):
        self.assertEqual(len(A),29)
        self.assertTrue(is_b3(A))
        self.assertTrue(is_b2(A))

    def test_triangle_weight_identity_for_sidons(self):
        fixtures = (
            ([1,2,5],[20,23,28]),
            (A[:3],A[3:6]),
            (A[:10],A[10:13]),
            (A[:10],A[10:14]),
            (A[:12],A[12:15]),
        )
        for u,w in fixtures:
            with self.subTest(u=u,w=w):
                self.assertTrue(is_b2(w))
                r,observed,numerator,threshold_lower,candidates=triadic_certificate(
                    u,w,1)
                m=len(w)
                cost_sum=sum(
                    r[y-x]+r[z-y]+r[z-x]
                    for x,y,z in combinations(sorted(w),3))
                self.assertEqual(cost_sum,(m-2)*observed)
                self.assertLessEqual(numerator,(m-2)*observed)
                self.assertLessEqual(threshold_lower,(m-2)*observed)
                self.assertGreaterEqual(len(candidates),comb(m,3))

    def test_pair_capacity_passes_but_triadic_rejects_zero(self):
        u=[1,2,5]
        w=[20,23,28]
        r,observed,numerator,threshold_lower,candidates=triadic_certificate(
            u,w,1)
        self.assertTrue(is_b3(u))
        self.assertTrue(is_b2(w))
        self.assertEqual(max(w)-min(w),8)
        self.assertEqual(observed,1)
        self.assertGreaterEqual(numerator,1)
        self.assertGreaterEqual(threshold_lower,1)
        # If the window expands to span ten, the pairwise Q=1
        # capacity still permits three B2-independent centers.
        L=10
        r=half_difference_weights(u,L)
        zeros=[h for h in range(1,L+1) if r[h]==0]
        self.assertEqual(zeros,[5,6,7,8,9,10])
        self.assertGreaterEqual(2*len(zeros),3*2)
        self.assertEqual(len([1 for a,b in ((a,b) for a in zeros
                                           for b in zeros)
                              if a != b and a+b<=L]),0)
        self.assertEqual(len(pair_sums(u))*3,18)
        self.assertEqual(2*(max(u)-min(u))+L+1,19)

    def test_non_b2_graph_independent_three_term_progression(self):
        u=[1,2,5]; w=[20,25,30]
        self.assertFalse(is_b2(w))
        r=half_difference_weights(u,10)
        self.assertEqual(weighted_correlation(r,w),0)
        self.assertEqual((w[1]-w[0],w[2]-w[1]),(5,5))
        # The theorem forbids equal adjacent gaps; no false application.

    def test_three_bin_oriented_zero_with_genuine_b3(self):
        u=A[:3]
        Y,Z,V=A[3:5],A[5:7],A[7:9]
        self.assertTrue(is_b3(u+Y+Z+V))
        for Q in (1,2,3,5,7,13,500):
            with self.subTest(Q=Q):
                observed,bound,K,Zcap,pair_energies=three_bin_certificate(
                    u,Y,Z,V,Q)
                self.assertEqual(observed,0)
                self.assertEqual(bound,0)
                self.assertEqual(sum(K.values()),len(Y)*len(Z)*len(V))
                self.assertTrue(all(K[c]<=Zcap[c] for c in K))
                self.assertEqual(pair_energies,(0,0,0))

    def test_three_bin_positive_real_b3(self):
        u=A[:10]
        Y,Z,V=A[10:11],A[11:12],A[12:13]
        self.assertTrue(is_b3(u+Y+Z+V))
        for Q in (1,2,3,7,500):
            with self.subTest(Q=Q):
                observed,bound,K,Zcap,energies=three_bin_certificate(
                    u,Y,Z,V,Q)
                self.assertEqual(observed,1)
                self.assertLessEqual(bound,observed)
                self.assertEqual(sum(K.values()),1)
                self.assertEqual(observed,sum(energies))

    def test_three_bin_positive_two_midpoints(self):
        u=A[:10]
        Y,Z,V=A[10:11],A[11:13],A[13:14]
        self.assertTrue(is_b3(u+Y+Z+V))
        for Q in (1,2,5,11,400):
            with self.subTest(Q=Q):
                observed,bound,K,Zcap,energies=three_bin_certificate(
                    u,Y,Z,V,Q)
                self.assertGreater(observed,0)
                self.assertLessEqual(bound,observed)
                self.assertEqual(sum(K.values()),2)

    def test_threshold_counts_nonnegative_and_bounded(self):
        u=[1,2,5]
        for w in ([20,23,28],[20,24,29],[20,26,33]):
            if not is_b2(w):
                continue
            for threshold in (1,2,3):
                with self.subTest(w=w,threshold=threshold):
                    r,observed,weighted,unscaled,_=triadic_certificate(
                        u,w,threshold)
                    self.assertGreaterEqual((len(w)-2)*observed,unscaled)


if __name__ == "__main__":
    unittest.main()
