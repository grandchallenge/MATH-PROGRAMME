"""Erdos #41 Stage B: exact forbidden-distance and inverse tiling regression.

Run: python -m unittest discover -s tests -p 'test_erdos41_popular_forbidden_distance.py' -v
The source theorem does not establish the Erdős #41 density dip.
"""
from collections import Counter
from itertools import combinations_with_replacement
from fractions import Fraction
import cmath
import math
import unittest

A = [
    1, 2, 5, 14, 33, 72, 125, 219, 376, 573, 745,
    1209, 1557, 2442, 3098, 4048, 5298, 6704, 7839,
    10987, 12332, 15465, 19144, 24546, 28974,
    34406, 37769, 45864, 50877,
]


def b3(a):
    sums = [sum(t) for t in combinations_with_replacement(sorted(a), 3)]
    return len(set(sums)) == len(sums)


def pair_sums(u):
    return {x + y for x, y in combinations_with_replacement(sorted(u), 2)}


def half_diff_profile(p):
    result = Counter()
    for a in p:
        for b in p:
            if a > b and (a-b)%2 == 0:
                result[(a-b)//2] += 1
    return result


def popular_certificate(u, k=None):
    u = sorted(u)
    n = len(u)
    d = u[-1]-u[0]
    p = pair_sums(u)
    assert n >= 2 and d >= 1 and b3(u)
    if k is None:
        profile = half_diff_profile(p)
        s = sum(profile.values())
        h = d
        picked = p
    else:
        assert d >= 2*k and n*n >= 32*k
        arr = sorted(p)
        lo, hi = min(arr), max(arr)
        # Equal-size consecutive integer bins, length at most ceil((2D+1)/(2k)).
        width = math.ceil((hi-lo+1)/(2*k))
        buckets = [[] for _ in range(2*k)]
        for v in arr:
            index = min((v-lo)//width, 2*k-1)
            buckets[index].append(v)
        most = max(buckets, key=len)
        evens = [v for v in most if v%2==0]
        odds = [v for v in most if v%2==1]
        picked = set(evens if len(evens)>=len(odds) else odds)
        profile = half_diff_profile(picked)
        s = sum(profile.values())
        h = math.ceil(d/k)
        assert all(1<=v<=h for v in profile)
    threshold = Fraction(s,2*h)
    heavy = [x for x in range(1,h+1) if profile[x]>=threshold]
    return n,d,p,s,h,threshold,heavy,profile,picked


def translate_convolution(p,w):
    return Counter(x+2*y for x in p for y in w)


def transform(values, M, xi):
    return sum(cmath.exp(-2j*cmath.pi*xi*x/M) for x in values)


class PopularDistancesTests(unittest.TestCase):
    def test_b3_fixture(self):
        self.assertTrue(b3(A))
        self.assertEqual(len(set(sum(t) for t in combinations_with_replacement(A,3))),4495)

    def test_global_even_mass_and_popular_bounds(self):
        for n in (2,3,5,8,12,14,20,29):
            with self.subTest(n=n):
                block = A[:n]
                nv,d,p,s,h,t,heavy,r,picked = popular_certificate(block)
                q0=sum(v%2==0 for v in p); q1=len(p)-q0
                self.assertEqual(s,q0*(q0-1)//2+q1*(q1-1)//2)
                self.assertGreaterEqual(s,Fraction(nv**4,32))
                self.assertLessEqual(max(r.values()),nv)
                self.assertEqual(h,d)
                self.assertGreaterEqual(t,Fraction(nv**4,64*d))
                self.assertGreaterEqual(len(heavy),Fraction(s*s,2*d*nv*nv))
                self.assertGreaterEqual(len(heavy),Fraction(nv**6,2048*d))
                self.assertTrue(all(r[x]>=t for x in heavy))

    def test_local_ratio_popular_windows(self):
        for n,k in ((12,1),(12,2),(14,1),(14,3),(20,2),(20,5),(29,1),(29,3),(29,8)):
            with self.subTest(n=n,k=k):
                nv,d,p,s,h,t,heavy,r,picked = popular_certificate(A[:n],k)
                self.assertLessEqual(h,math.ceil(d/k))
                self.assertGreaterEqual(len(picked),Fraction(nv*nv,8*k))
                self.assertGreaterEqual(s,Fraction(nv**4,256*k*k))
                self.assertGreaterEqual(t,Fraction(nv**4,1024*k*d))
                self.assertGreaterEqual(len(heavy),Fraction(nv**6,262144*k**3*d))
                self.assertTrue(all(half_diff_profile(p)[x]>=t for x in heavy))

    def test_independence_packing_bound(self):
        for n in (3,8,14):
            u=A[:n]; p=pair_sums(u)
            d=u[-1]-u[0]
            for r in (n+1,len(A)):
                w=A[n:r]
                if not w:
                    continue
                correlation=sum(half_diff_profile(p).get(y-x,0)
                                for i,x in enumerate(w) for y in w[i+1:])
                if correlation:
                    continue
                L=max(w)-min(w)
                self.assertEqual(len(translate_convolution(p,w)),len(p)*len(w))
                self.assertLessEqual(len(p)*len(w),2*d+2*L+1)

    def test_exact_cyclic_hole_complementarity(self):
        # U={0,1} is B3. Candidate W={10,12} is graph independent.
        u=[0,1]; w=[10,12]; p=pair_sums(u)
        self.assertTrue(b3(u))
        sums=translate_convolution(p,w)
        self.assertEqual(max(sums.values()),1)
        M=2*(max(u)-min(u))+2*(max(w)-min(w))+1
        self.assertEqual(M,7)
        offset=min(sums)
        occupied={s-offset for s in sums}
        holes=set(range(M))-occupied
        self.assertEqual(holes,{3})
        self.assertEqual(len(occupied),len(p)*len(w))
        for xi in range(1,M):
            lhs=transform(p,M,xi)*transform([2*z for z in w],M,xi)
            rhs=-transform([s+offset for s in holes],M,xi)
            self.assertLess(abs(lhs-rhs),1e-8)
            self.assertLessEqual(abs(lhs),len(holes)+1e-8)
            self.assertLessEqual(
                abs(lhs)/(len(p)*len(w)),
                Fraction(len(holes),len(occupied))+1e-8
            )

    def test_no_count_only_intersection_claim(self):
        # Two positive-density distance subsets of the same finite window
        # can avoid each other; this is a logical control, not a B3 example.
        left=set(range(1,31))
        right=set(range(31,61))
        self.assertTrue(left)
        self.assertTrue(right)
        self.assertFalse(left & right)
        self.assertEqual(len(left)+len(right),60)

    def test_non_b3_hostile_invalidates_pointwise_matching(self):
        u=[1,2,3,4]
        self.assertFalse(b3(u))
        p=pair_sums(u)
        # The cap theorem must never be invoked without unique pair sums.
        self.assertLess(len(p),len(u)*(len(u)+1)//2)


if __name__ == "__main__":
    unittest.main()
