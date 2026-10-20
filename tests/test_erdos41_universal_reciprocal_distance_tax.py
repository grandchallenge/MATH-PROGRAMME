"""Erdos #41: universal, nonduplicated B3 reciprocal distance tax.

Proved finite invariant, not a density-valley theorem.
"""
from itertools import combinations, combinations_with_replacement
from math import comb, ceil
import unittest


A=[1,2,5,14,33,72,125,219,376,573,745,1209,1557,2442,
   3098,4048,5298,6704,7839,10987,12332,15465,19144,
   24546,28974,34406,37769,45864,50877]


def is_b3(a):
    tris=[sum(tr) for tr in combinations_with_replacement(sorted(a),3)]
    return len(set(tris))==len(tris)


def q_sums(a):
    return {x+y for x,y in combinations_with_replacement(sorted(a),2)}


def cubic_shadow(a):
    return {x+y-z for x,y in combinations_with_replacement(sorted(a),2)
                   for z in a}


def positive_q_differences(a):
    q=sorted(q_sums(a))
    return {y-x for x,y in combinations(q,2)}


def bands(p,y):
    return ({y-t for t in cubic_shadow(p)},
            {2*y-q for q in q_sums(p)})


def forced_tax(n):
    return (n*n*n+3*n)//2


class UniversalReciprocalDistanceTaxTests(unittest.TestCase):
    def test_finite_b3_fixture_and_exact_cubic_shadow(self):
        self.assertTrue(is_b3(A))
        for n in (1,2,3,4,5,8,12,17,29):
            with self.subTest(n=n):
                p=A[:n]
                self.assertEqual(len(q_sums(p)),comb(n+1,2))
                self.assertEqual(len(cubic_shadow(p)),
                                 (n**3-n**2+2*n)//2)

    def test_two_new_distance_bands_distinct_and_outside_old(self):
        for n in (1,2,3,4,5,8,12,17):
            p=A[:n]
            R=max(p)
            for y in (4*R+1,5*R,20*R):
                with self.subTest(n=n,y=y):
                    self.assertTrue(is_b3(p+[y]))
                    old=positive_q_differences(p)
                    new=positive_q_differences(p+[y])
                    one,two=bands(p,y)
                    self.assertFalse(one & two)
                    self.assertFalse((one|two)&old)
                    self.assertTrue((one|two).issubset(new-old))
                    self.assertEqual(len(one|two),forced_tax(n))
                    self.assertGreaterEqual(len(new-old),forced_tax(n))
                    self.assertTrue(all(d>2*R-2 for d in one|two))
                    self.assertLessEqual(max(one|two),2*y-2)

    def test_arbitrarily_shifting_arithmetic_geometry(self):
        p=[1,2,5,14]
        R=14
        # Translation/dilation variants of the NEW anchor never
        # change the forced new-distance cardinality.
        for y in (57,100,10_000,100_000_000):
            with self.subTest(y=y):
                self.assertEqual(len(bands(p,y)[0]),len(cubic_shadow(p)))
                self.assertEqual(len(bands(p,y)[1]),len(q_sums(p)))
                self.assertGreaterEqual(
                    len(positive_q_differences(p+[y])-
                        positive_q_differences(p)),forced_tax(len(p)))

    def test_exact_telescope_with_real_intermediate_b3_points(self):
        r=A[5]
        initial=[a for a in A if a<=r]
        stages=[(r,initial)]
        while len(stages)<4:
            nxt=next((x for x in A if x>4*r),None)
            if nxt is None:
                break
            previous=list(stages[-1][1])
            p_next=[a for a in A if a<=nxt]
            # There may be genuine A elements between r and nxt.
            assert len(p_next)>len(previous)
            stages.append((nxt,p_next))
            r=nxt
        self.assertGreaterEqual(len(stages),3)
        telescope=0
        forced_sum=0
        new_owned=[]
        for (_,p),(_,pnext) in zip(stages,stages[1:]):
            old=positive_q_differences(p)
            future=positive_q_differences(pnext)
            new=future-old
            self.assertGreaterEqual(len(new),forced_tax(len(p)))
            telescope+=len(new)
            forced_sum+=forced_tax(len(p))
            new_owned.append(new)
        self.assertGreaterEqual(telescope,forced_sum)
        self.assertEqual(telescope,
                         len(positive_q_differences(stages[-1][1]))-
                         len(positive_q_differences(stages[0][1])))
        for i in range(len(new_owned)):
            for j in range(i+1,len(new_owned)):
                self.assertFalse(new_owned[i]&new_owned[j])

    def test_persistent_density_implies_bounded_anchor_ratio_algebra(self):
        # This verifies an algebraic implication CONDITIONAL on
        # hypothetical persistent density; not a B3 counterexample.
        for inverse_c in (1,2,5,10,50,100):
            c=1/inverse_c
            K=ceil((5/c)**3)
            self.assertGreater(c*K**(1/3),72**(1/3))
            self.assertGreater(K,4)
            for R in (1,10,1000):
                self.assertGreater(
                    c*(K*R)**(1/3),
                    (72*R)**(1/3))

    def test_resource_budget_stays_linear_even_with_nonzero_taxes(self):
        # The formal sums of critical-order lower bounds do not
        # overwhelm the available difference range at later scales.
        for c in (.01,.1,.5,1.0):
            R=[100]
            for j in range(5):
                R.append(5*R[-1])
            for h in range(1,len(R)):
                taxes=(c**3/2)*sum(R[:h])
                self.assertLess(taxes,2*R[h])
                self.assertLess(sum(R[:h]),R[h]/3)

    def test_indefinite_sparse_extension_has_taxes_but_no_density(self):
        p=[1,2,5,14]
        for _ in range(7):
            y=5*max(p)
            before=positive_q_differences(p)
            after=positive_q_differences(p+[y])
            self.assertGreaterEqual(len(after-before),forced_tax(len(p)))
            p.append(y)
            self.assertTrue(is_b3(p))
        n=len(p)
        N=(n*100)**3
        self.assertLess(n/N**(1/3),.011)


    def test_one_anchor_difference_decomposition_is_exact_not_only_lower(self):
        for n in (1,2,3,4,5,8,12,17,29):
            p=A[:n]; R=max(p)
            for y in (4*R+1,5*R,10*R+1):
                with self.subTest(n=n,y=y):
                    old=positive_q_differences(p)
                    full=positive_q_differences(p+[y])
                    one,two=bands(p,y)
                    self.assertEqual(full,old|one|two)
                    self.assertFalse(old&one)
                    self.assertFalse(old&two)
                    self.assertFalse(one&two)
                    self.assertEqual(len(full)-len(old),forced_tax(n))

    def test_new_bands_are_invisible_to_short_intrawindow_differences(self):
        for n in (1,2,3,5,8,12):
            p=A[:n]; R=max(p); y=4*R+1
            one,two=bands(p,y)
            new=one|two
            self.assertGreater(min(new),2*R-2)
            for jstart in (y+R,2*y+2*R,100*y):
                # An interval of 2R-1 integer positions has max
                # pair distance 2R-2, strictly below both new bands.
                interval=range(jstart,jstart+2*R-1)
                if len(interval)>1:
                    self.assertLess(max(interval)-min(interval),min(new))
                self.assertFalse(
                    {v-u for u,v in combinations(interval,2)} & new
                )

    def test_scalar_persistent_critical_countermodel_without_overload(self):
        # Formal VOLUME model, NOT the prefixes of an actual infinite B3 set:
        # many intermediate additions are intentionally unmodelled.
        # All exact charged one-anchor increments remain compatible
        # with critical prefix cardinalities and the final spectrum range.
        for denominator in (2,5,10,100):
            cnum=1
            R0=max(10,denominator**3)
            radii=[R0*5**j for j in range(10)]
            d=0
            for h in range(1,len(radii)):
                Rprev=radii[h-1]
                # Minimal integer n with (denominator*n)^3>=Rprev.
                lo,hi=0,Rprev+1
                while lo+1<hi:
                    mid=(lo+hi)//2
                    if (denominator*mid)**3>=Rprev:
                        hi=mid
                    else:
                        lo=mid
                n=hi
                self.assertGreaterEqual((denominator*n)**3,Rprev)
                self.assertTrue(n==0 or (denominator*(n-1))**3<Rprev)
                self.assertGreaterEqual(n,1)
                d+=forced_tax(n)
                Rh=radii[h]
                self.assertGreater(Rh,4*Rprev)
                self.assertLessEqual(Rh,ceil((5*denominator)**3)*Rprev)
                self.assertLess(d,2*Rh-2)
                self.assertLess(d,7*Rh/(4*denominator**3))


if __name__=="__main__":
    unittest.main()
