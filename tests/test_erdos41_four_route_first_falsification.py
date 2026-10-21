"""Erdos 41: falsify finite-Xi4-only shortage and weak-spectral-only rescue.

All B3 checks use unordered 3-multisets WITH repetition. Original
mathematical status: bounded negative theorems; no solution of #41.
Run: python3 tests/test_erdos41_four_route_first_falsification.py -v
"""
from collections import Counter
from itertools import combinations_with_replacement, product
from math import comb, pi
import cmath
import unittest


S = [1, 2, 5, 14, 1033, 1072, 1125, 1219]
P, Y = S[:4], S[4:]


def is_b3(xs):
    words=[sum(a) for a in combinations_with_replacement(sorted(xs),3)]
    return len(words)==len(set(words))


def moment_code(p):
    B=3*p+1
    W=p*(1+B+B*B)+1
    e=[1+i+B*(i*i % p)+B*B*(i*i*i % p) for i in range(p)]
    return W,e


def enlarged(s,t,W):
    U=max(s)
    M=8*U+1
    H=8*M*W+8*U
    z=[H+M*v for v in t]
    return M,H,z


def shadow(xs):
    return {a+b-c for a,b in combinations_with_replacement(sorted(xs),2)
                  for c in xs}


def overlap_defect(p,y):
    u={z-t for z in y for t in shadow(p)}
    v={t-x for t in shadow(y) for x in p}
    base={z-x for z in y for x in p}
    return len((u&v)-base)


def sixth_moment_integer(xs):
    s=Counter(a+b+c for a,b,c in product(xs,repeat=3))
    return sum(v*v for v in s.values())


def empirical_mode(xs,W,t):
    return sum(cmath.exp(2j*pi*t*x/W) for x in xs)/len(xs)


class FourRouteFirstFalsificationTests(unittest.TestCase):
    def test_hostile_eight_member_carrier_has_four_sum_overlap(self):
        self.assertTrue(is_b3(S))
        self.assertEqual(overlap_defect(P,Y),11)
        self.assertEqual(1+1+1033+1125,2+14+1072+1072)

    def test_moment_code_is_exact_repetition_allowed_b3(self):
        for p in (5,7,11,17,31):
            W,T=moment_code(p)
            with self.subTest(p=p):
                self.assertEqual(len(set(T)),p)
                self.assertTrue(is_b3(T))
                self.assertTrue(all(1<=x<=W for x in T))
                self.assertLess(W,12*p**3)

    def test_any_fixed_old_b3_shape_accepts_critical_future_batches(self):
        for p in (5,7,11,17,31):
            W,T=moment_code(p)
            M,H,Z=enlarged(S,T,W)
            L=M*W
            with self.subTest(p=p):
                self.assertTrue(is_b3(S+Z))
                self.assertTrue(all(H+1<=z<=H+L for z in Z))
                self.assertEqual(len(Z),p)
                self.assertGreater(12*M*len(Z)**3,L)
                self.assertEqual(overlap_defect(P,Y),11)
                self.assertLess(max(S),min(Z))
                self.assertGreater(H,3*M*W+3*max(S))

    def test_far_future_template_not_required_to_be_same_dictionary(self):
        for prefix in ([1], [1,2,5], [1,2,5,14], S):
            self.assertTrue(is_b3(prefix))
            W,T=moment_code(7)
            M,H,Z=enlarged(prefix,T,W)
            with self.subTest(prefix=tuple(prefix)):
                self.assertTrue(is_b3(prefix+Z))
                self.assertGreaterEqual(len(Z)**3,
                                        (M*W)//(12*M))

    def test_weakly_same_critical_size_non_b3_companion(self):
        for p in (5,7,11,17,31):
            W,T=moment_code(p)
            bad=[1,2,3]+T[3:]
            with self.subTest(p=p):
                self.assertEqual(len(set(bad)),p)
                self.assertEqual(len(bad),p)
                self.assertTrue(all(1<=x<=W for x in bad))
                self.assertTrue(is_b3(T))
                self.assertFalse(is_b3(bad))
                self.assertGreater(12*p**3,W)
                shared=len(set(T)&set(bad))
                self.assertGreaterEqual(shared,p-3)
                # Probability measures differ in at most 3 atoms on
                # either side, in total variation at most 3/p.
                self.assertLessEqual(p-shared,3)

    def test_exact_sixth_moment_separates_weakly_same_sets(self):
        for p in (5,7,11,17):
            W,T=moment_code(p)
            bad=[1,2,3]+T[3:]
            exact=6*p**3-9*p*p+4*p
            with self.subTest(p=p):
                self.assertEqual(sixth_moment_integer(T),exact)
                self.assertGreater(sixth_moment_integer(bad),exact)

    def test_all_macroscopic_fourier_frequencies_are_close(self):
        for p in (5,7,11,17,31):
            W,T=moment_code(p)
            bad=[1,2,3]+T[3:]
            for t in (-12345.5,-3.1,-1,0,1,2,3.1,10001):
                with self.subTest(p=p,t=t):
                    self.assertLessEqual(
                        abs(empirical_mode(T,W,t)-empirical_mode(bad,W,t)),
                        6/p+1e-12)

    def test_no_claim_of_infinite_density(self):
        W,T=moment_code(31)
        M,H,Z=enlarged(S,T,W)
        n=len(S)+len(Z)
        # The constructed set is finite. For sufficiently large N
        # its normalized density necessarily tends to zero.
        N=max(Z)+n**4
        self.assertLess(n/N**(1/3),n/max(Z)**(1/3))


if __name__=="__main__":
    unittest.main()
