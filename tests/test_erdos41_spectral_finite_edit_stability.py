"""Exact Fourier sixth-energy finite-edit theorem for repetition-allowed B3.

This is a bounded no-go result for normalized spectral observables, not an
Erdos 41 solution or an independent specialist certification.
"""
from collections import Counter
from itertools import product, combinations_with_replacement
from math import comb, pi
import cmath
import unittest


def sixth_energy(xs):
    reps = Counter(a+b+c for a,b,c in product(xs, repeat=3))
    return sum(v*v for v in reps.values())


def b3(xs):
    sums = [sum(w) for w in combinations_with_replacement(sorted(xs), 3)]
    return len(sums) == len(set(sums))


def moment_code(p):
    radix = 3*p + 1
    W = p*(1+radix+radix*radix)+1
    values = [
        1+i+radix*(i*i % p)+radix*radix*(i*i*i % p)
        for i in range(p)
    ]
    return W, values


def predicted_sixth_energy(n):
    return 6*n**3 - 9*n*n + 4*n


def finite_edit_ceiling(n,r):
    return 6*r*(12+6*r+3*r*r+r**3)*n*n


def empirical_mode(values, W, real_t):
    return sum(cmath.exp(2j*pi*real_t*a/W) for a in values)/len(values)


class SpectralFiniteEditAudit(unittest.TestCase):
    def test_three_element_minimal_non_b3_edit(self):
        good = [1,2,5]
        bad = [1,2,3]
        self.assertTrue(b3(good))
        self.assertFalse(b3(bad))
        self.assertEqual(len(set(good)&set(bad)),2)
        exact = sixth_energy(good)
        defect = sixth_energy(bad)-exact
        self.assertEqual(exact,predicted_sixth_energy(3))
        self.assertGreater(defect,0)
        self.assertLessEqual(defect,finite_edit_ceiling(3,1))

    def test_arbitrary_replacements_with_large_and_negative_amplitudes(self):
        for n in (3,5,7,11):
            _,good = moment_code(max(n,5))
            good = good[:n]
            self.assertTrue(b3(good))
            for r in range(1,min(n,3)+1):
                bad = good[r:]+[-10**8*i-10**5 for i in range(1,r+1)]
                self.assertEqual(len(set(good)&set(bad)),n-r)
                with self.subTest(n=n,r=r):
                    self.assertGreaterEqual(
                        sixth_energy(bad), predicted_sixth_energy(n))
                    self.assertLessEqual(
                        abs(sixth_energy(bad)-sixth_energy(good)),
                        finite_edit_ceiling(n,r))

    def test_fixed_edited_points_make_non_b3_while_critical_size_is_retained(self):
        for p in (5,7,11,17,19,23,29,31,37,41,43):
            W,good=moment_code(p)
            bad=[1,2,3]+good[3:]
            self.assertEqual(len(good),p)
            self.assertEqual(len(set(bad)),p)
            self.assertLess(W,12*p**3)
            self.assertTrue(b3(good))
            self.assertFalse(b3(bad))
            self.assertEqual(predicted_sixth_energy(p),sixth_energy(good))
            defect=sixth_energy(bad)-sixth_energy(good)
            with self.subTest(p=p):
                self.assertGreater(defect,0)
                self.assertLessEqual(defect,finite_edit_ceiling(p,3))
                self.assertLessEqual(defect/p**3,1512/p)
                self.assertEqual(len(set(good)&set(bad)),p-2)

    def test_sixth_moment_minimum_exact_for_all_small_b3_subsets(self):
        for p in (5,7,11):
            _,code=moment_code(p)
            for n in range(1,p+1):
                x=code[:n]
                self.assertTrue(b3(x))
                self.assertEqual(sixth_energy(x),predicted_sixth_energy(n))

    def test_rescaled_fourier_modes_stay_close_at_any_tested_frequency(self):
        for p in (5,7,11,17,31,41):
            W,good=moment_code(p)
            bad=[1,2,3]+good[3:]
            for freq in (-10000.23,-11,-1,0,1,9,1000.19):
                with self.subTest(p=p,freq=freq):
                    self.assertLessEqual(
                        abs(empirical_mode(good,W,freq)-empirical_mode(bad,W,freq)),
                        6/p+1e-12)

    def test_general_l_inf_count_for_triplets_with_special_elements(self):
        for p in (5,7,11):
            _,good=moment_code(p)
            common=good[3:]
            bad=[1,2,3]+common
            rc=Counter(sum(z) for z in product(common, repeat=3))
            ra=Counter(sum(z) for z in product(good, repeat=3))
            rb=Counter(sum(z) for z in product(bad, repeat=3))
            difference_A=Counter({s:ra[s]-rc[s] for s in ra})
            difference_B=Counter({s:rb[s]-rc[s] for s in rb})
            self.assertTrue(all(0<=v<=6 for v in rc.values()))
            self.assertLessEqual(max(difference_A.values(),default=0),72)
            self.assertLessEqual(max(difference_B.values(),default=0),72)
            self.assertEqual(sum(difference_A.values()),p**3-(p-3)**3)
            self.assertEqual(sum(difference_B.values()),p**3-(p-3)**3)


if __name__=="__main__":
    unittest.main()
