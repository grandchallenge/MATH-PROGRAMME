"""Exact adversarial regression checks for the shell-Hardy derivation.

These tests check finite identities with rational arithmetic. They cannot prove
universal asymptotic propositions or that the synthetic counterprofile is B3.
"""
from fractions import Fraction
from itertools import combinations_with_replacement
from random import Random
import unittest


def shell_energy(m):
    return sum((Fraction(x**3, 2**j) for j, x in enumerate(m)), Fraction(0))


def grouped_norms(m):
    assert len(m) % 3 == 0
    u = [Fraction(sum(m[3*k:3*k+3]), 2**k) for k in range(len(m)//3)]
    d = []
    prev = Fraction(0)
    for value in u:
        prev = value + prev/2
        d.append(prev)
    return u, d


def is_excluded(j):
    n = max(2, int(j**0.25) - 2)
    while n**4 <= j:
        if n**4 <= j <= n**4+n:
            return True
        n += 1
    return False


def packed_only_profile(j):
    return 0 if is_excluded(j) else 2**(j//3)


def exact_m3(a):
    vals = [sum(t) for t in combinations_with_replacement(a, 3)]
    return len(vals) == len(set(vals))


class ShellHardyTests(unittest.TestCase):
    def test_exact_finite_hardy_bounds_arbitrary_profiles(self):
        rng = Random(41)
        for k in range(1, 21):
            for variant in range(4):
                m = [rng.randrange(0, 7) for _ in range(3*k)]
                if variant == 1:
                    m = [2**(j//3) if j % 4 else 0 for j in range(3*k)]
                if variant == 2:
                    m = [0]* (3*k-1) + [9999]
                if variant == 3:
                    m = [0]*(3*k)
                u, d = grouped_norms(m)
                energy = shell_energy(m)
                self.assertLessEqual(sum((x**3 for x in d), Fraction(0)), 288*energy)
                self.assertLessEqual(energy, sum((x**3 for x in d), Fraction(0)))
                self.assertLessEqual(sum((x**3 for x in d), Fraction(0)),
                                     8*sum((x**3 for x in u), Fraction(0)))

    def test_genuine_m3_greedy_occupancies_and_window_tail(self):
        a = [1,2,5,14,33,72,125,219,376,573,745,1209,1557,2442,3098,
             4048,5298,6704,7839,10987,12332,15465,19144,24546,28974,
             34406,37769,45864,50877]
        self.assertTrue(exact_m3(a))
        m = [sum(2**j <= v < 2**(j+1) for v in a) for j in range(18)]
        u, d = grouped_norms(m)
        self.assertTrue(all(x <= 6 for x in u))
        for k in range(len(u)):
            for length in range(1, k+2):
                recent = sum((u[k-r]/(2**r) for r in range(length)), Fraction(0))
                self.assertLessEqual(d[k] - recent, Fraction(12,2**length))
                self.assertLessEqual(recent, d[k])

    def test_packing_only_profile_has_positive_shell_average(self):
        for j in range(4800):
            m = packed_only_profile(j)
            self.assertLessEqual(m**3, 2**j)
        for J in (1200, 2400, 4800):
            quarter_units = sum(0 if is_excluded(j) else (4,2,1)[j%3]
                                for j in range(J))
            energy_average = Fraction(quarter_units, 4*J)
            self.assertGreater(energy_average, Fraction(1,2))
            self.assertLess(energy_average, Fraction(7,12))

    def test_packing_only_profile_passes_isolated_mixed_shell_counts(self):
        from math import comb
        m = [packed_only_profile(j) for j in range(94)]
        for i in range(94):
            for j in range(i, 94):
                for k in range(j, 94):
                    if i == j == k:
                        count = comb(m[i]+2,3)
                    elif i == j:
                        count = comb(m[i]+1,2)*m[k]
                    elif j == k:
                        count = m[i]*comb(m[j]+1,2)
                    else:
                        count = m[i]*m[j]*m[k]
                    self.assertLessEqual(count, 2**i+2**j+2**k-2)

    def test_packing_only_profile_has_deep_rare_dips(self):
        for n in (4,5,6,7,8,9,10):
            start = n**4
            count_before_gap = sum(packed_only_profile(j) for j in range(start))
            gap_end = start+n
            cubic_density_at_gap = Fraction(count_before_gap**3, 2**gap_end)
            self.assertLessEqual(cubic_density_at_gap, Fraction(216,2**n))
        self.assertFalse(exact_m3([1024, 1025, 1026, 1027]))

if __name__ == '__main__':
    unittest.main()
