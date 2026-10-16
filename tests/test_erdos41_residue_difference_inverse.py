"""Erdos 41: exact signed-difference residue inverse and CRT density cost.

Run: python -m unittest discover -s tests -p 'test_erdos41_residue_difference_inverse.py' -v
Research-only. Requires genuine B3/B2 outer differences for inverse statements.
"""
from collections import Counter, defaultdict
from itertools import combinations_with_replacement
from math import prod
from fractions import Fraction
import unittest

A = [
    1, 2, 5, 14, 33, 72, 125, 219, 376, 573, 745,
    1209, 1557, 2442, 3098, 4048, 5298, 6704, 7839,
    10987, 12332, 15465, 19144, 24546, 28974,
    34406, 37769, 45864, 50877,
]


def is_b3(a):
    sums = [sum(t) for t in combinations_with_replacement(sorted(a), 3)]
    return len(sums) == len(set(sums))


def is_b2(a):
    sums = [sum(t) for t in combinations_with_replacement(sorted(a), 2)]
    return len(sums) == len(set(sums))


def pair_sums(u):
    return {a+b for a,b in combinations_with_replacement(sorted(u), 2)}


def half_difference_weights(p, L):
    weights = Counter()
    for p1 in p:
        for p2 in p:
            gap = p1-p2
            if gap > 0 and gap % 2 == 0 and gap <= 2*L:
                weights[gap//2] += 1
    return weights


def energy(p, w):
    L=max(w)-min(w)
    weights = half_difference_weights(p, L)
    return sum(weights[b-a] for i,a in enumerate(sorted(w))
               for b in sorted(w)[i+1:])


def residue_profiles(w, Q):
    b=Counter(v % Q for v in w)
    m=len(w)
    # O(m^2) independent of potentially huge Q. Pair counts agree
    # with the quadratic convolution of the residue occupancies.
    K=Counter((y-x)%Q for x in w for y in w if x!=y)
    assert sum(K.values()) == m*(m-1)
    return b,K


def residue_order_statistic(p, w, Q):
    L=max(w)-min(w)
    weights=half_difference_weights(p,L)
    b,K=residue_profiles(w,Q)
    eligible=defaultdict(list)
    for h in range(-L,L+1):
        if h:
            eligible[h%Q].append(weights[abs(h)])
    value=0
    for d in range(Q):
        arr=sorted(eligible[d])
        assert 0<=K[d]<=len(arr), (d,Q,K[d],len(arr))
        value+=sum(arr[:K[d]])
    return value,b,K,eligible,weights


def threshold_residue_certificate(p,w,Q,threshold):
    value,b,K,eligible,weights=residue_order_statistic(p,w,Q)
    z={d:sum(v<threshold for v in eligible[d]) for d in range(Q)}
    threshold_lower=threshold*sum(max(0,K[d]-z[d]) for d in range(Q))
    return value,threshold_lower,z,b,K




def localized_bin_inverse(p, low, high, Q, threshold=1):
    """Oriented cross-bin certificate using actual short difference range."""
    assert min(high)>max(low)
    lower=min(high)-max(low)
    upper=max(high)-min(low)
    r=half_difference_weights(p,upper)
    K=Counter((z-y)%Q for y in low for z in high)
    eligible=defaultdict(list)
    for h in range(lower,upper+1):
        eligible[h%Q].append(r[h])
    order_lower=0
    threshold_lower=0
    zcounts={}
    for d, needed in K.items():
        values=sorted(eligible[d])
        assert needed<=len(values)
        order_lower+=sum(values[:needed])
        z=sum(v<threshold for v in values)
        zcounts[d]=z
        threshold_lower+=threshold*max(0,needed-z)
    actual=sum(r[z-y] for y in low for z in high)
    return actual,order_lower,threshold_lower,K,zcounts,upper-lower+1


class ResidueDifferenceInverseTests(unittest.TestCase):
    def test_all_genuine_b3_prefixes(self):
        self.assertTrue(is_b3(A))
        self.assertTrue(is_b2(A))
        for n in (3,5,8,12,14,20,29):
            self.assertTrue(is_b3(A[:n]))

    def test_weighted_order_statistics_on_actual_outer_sets(self):
        fixture={8:0,14:3}
        for n, expected in fixture.items():
            u,w=A[:n],A[n:]
            p=pair_sums(u)
            actual=energy(p,w)
            self.assertEqual(actual,expected)
            L=max(w)-min(w)
            for Q in (1,2,3,4,5,7,11,19,2*L+1):
                with self.subTest(n=n,Q=Q):
                    lower, b,K, eligible, weights=residue_order_statistic(p,w,Q)
                    self.assertLessEqual(lower,2*actual)
                    self.assertEqual(sum(K.values()),len(w)*(len(w)-1))
                    if Q>2*L:
                        self.assertEqual(lower,2*actual)
                    for threshold in (1,2,3,4):
                        _,t_lower,z,b,K=threshold_residue_certificate(
                            p,w,Q,threshold
                        )
                        self.assertLessEqual(t_lower,2*actual)
                        if actual == 0:
                            self.assertTrue(all(K[d]<=z[d] for d in range(Q)))

    def test_positive_profiles_for_many_prefix_outer_cuts(self):
        for n in range(3,24):
            u,w=A[:n],A[n:]
            p=pair_sums(u)
            M=energy(p,w)
            for Q in (1,2,3,5,7,11):
                with self.subTest(n=n,Q=Q):
                    val,*_ = residue_order_statistic(p,w,Q)
                    self.assertLessEqual(val,2*M)

    def test_repeated_differences_hostile_graph_independence(self):
        # Inner U is genuinely B3. An AP of centers with stride 5 avoids
        # every forbidden inner half-difference, but is not B2.
        u=[1,2,5]
        p=pair_sums(u)
        w=[100+5*j for j in range(10)]
        self.assertTrue(is_b3(u))
        self.assertFalse(is_b2(w))
        self.assertEqual(energy(p,w),0)
        L=max(w)-min(w)
        _,K=residue_profiles(w,1)
        available_zeros=sum(
            half_difference_weights(p,L)[abs(h)]==0
            for h in range(-L,L+1) if h
        )
        self.assertGreater(K[0],available_zeros)
        # Therefore the B2-dependent capacity inequality is deliberately
        # NOT applied to this arbitrary graph-independent W.

    def test_crt_product_density_cost_on_actual_b3_blocks(self):
        from math import gcd
        moduli_sets=((2,3),(2,3,5),(3,5,7),(2,3,5,7),(5,7,11))
        for n in (5,8,14,20,29):
            x=A[:n];D=x[-1]-x[0]
            for moduli in moduli_sets:
                Q=prod(moduli)
                if Q>D:
                    continue
                self.assertTrue(all(gcd(q,r)==1 for i,q in enumerate(moduli)
                                    for r in moduli[i+1:]))
                t=[len({v%q for v in x}) for q in moduli]
                with self.subTest(n=n,moduli=moduli):
                    self.assertLessEqual(n**3*Q,12*D*prod(t)**3)
                    tQ=len({v%Q for v in x})
                    self.assertLessEqual(tQ,prod(t))

    def test_coprime_concentration_cost_multiplies(self):
        moduli=(2,3,5,7,11,13)
        Q=prod(moduli)
        x=[Q*v+17 for v in A[:8]]
        self.assertTrue(is_b3(x))
        D=x[-1]-x[0]
        t=[len({v%q for v in x}) for q in moduli]
        self.assertEqual(t,[1]*len(moduli))
        self.assertLessEqual(len(x)**3*Q,12*D*prod(t)**3)
        # Normalized density drops relative to the unscaled base sequence.
        unscaled=A[:8]
        D0=unscaled[-1]-unscaled[0]
        self.assertLess(Fraction(len(x)**3,D),Fraction(len(unscaled)**3,D0))


    def test_localized_oriented_cross_bin_certificates(self):
        p=pair_sums(A[:14])
        w=A[14:]
        bins=[w[:3],w[3:7],w[7:]]
        total=0
        for i in range(len(bins)):
            for j in range(i+1,len(bins)):
                lo,hi=bins[i],bins[j]
                actual=energy(p,lo+hi)-energy(p,lo)-energy(p,hi)
                total+=actual
                width=max(hi)-min(lo)-(min(hi)-max(lo))+1
                for Q in (1,2,3,5,7,11,16,width+1):
                    with self.subTest(i=i,j=j,Q=Q):
                        observed,weighted,thresholded,K,Z,length=localized_bin_inverse(
                            p,lo,hi,Q,threshold=1)
                        self.assertEqual(observed,actual)
                        self.assertLessEqual(weighted,actual)
                        self.assertLessEqual(thresholded,actual)
                        self.assertEqual(sum(K.values()),len(lo)*len(hi))
                        self.assertEqual(length,width)
                        if Q>width:
                            self.assertEqual(weighted,actual)
                        if actual==0:
                            self.assertTrue(all(K[d]<=Z[d] for d in K))
        self.assertLessEqual(total,energy(p,w))

    def test_small_positive_cross_bin_and_exact_large_modulus(self):
        p=pair_sums(A[:14])
        low=A[15:17]  # 4048,5298
        high=A[17:19] # 6704,7839
        self.assertEqual(low,[4048,5298])
        self.assertEqual(high,[6704,7839])
        observed,lower,thresholded,K,Z,width=localized_bin_inverse(p,low,high,5000)
        self.assertEqual(observed,1)
        self.assertEqual(lower,1)
        self.assertEqual(sum(K.values()),4)
        self.assertGreater(5000,width)
        self.assertLessEqual(thresholded,observed)

    def test_cross_bin_repeated_difference_hostile(self):
        # 10x10 graph-independent center pairs with repeated differences.
        # A Sidon-only inverse applied here would yield a false conclusion.
        p=pair_sums([1,2,5])
        low=[100+5*j for j in range(10)]
        high=[200+5*j for j in range(10)]
        self.assertFalse(is_b2(low+high))
        self.assertEqual(energy(p,low+high),0)
        left=min(high)-max(low)
        right=max(high)-min(low)
        r=half_difference_weights(p,right)
        eligible_zero=sum(r[h]==0 for h in range(left,right+1))
        self.assertEqual(eligible_zero,right-left+1)
        self.assertGreater(len(low)*len(high),eligible_zero)


if __name__=="__main__":
    unittest.main()
