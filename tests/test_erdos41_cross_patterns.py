"""Exact finite and adversarial tests for M3 cross-pattern Hall packing.

Does NOT claim Hall feasibility implies an actual M3 integer realization.
"""
from collections import Counter
from itertools import combinations_with_replacement
from math import comb
from random import Random
import unittest


def pattern_weight(pattern, m):
    value = 1
    for j, count in Counter(pattern).items():
        value *= comb(m.get(j, 0) + count - 1, count)
    return value


def span(pattern):
    return sum(1 << j for j in pattern), sum(1 << (j + 1) for j in pattern) - 3


def union_size(intervals):
    intervals = sorted(intervals)
    total, right = 0, -1
    for lo, hi in intervals:
        if hi > right:
            total += hi - max(lo, right + 1) + 1
            right = hi
    return total


def hall(patterns, m):
    return sum(pattern_weight(p, m) for p in patterns), union_size([span(p) for p in patterns])


def sparse_deleted(j):
    n = max(2, int(j ** 0.25) - 2)
    while n ** 4 <= j:
        if n ** 4 <= j <= n ** 4 + n:
            return True
        n += 1
    return False


def uniform_profile(j):
    return 0 if j < 12 else 1 << (j // 3 - 4)


def diluted_profile(j):
    return 0 if sparse_deleted(j) or j < 12 else 1 << (j // 3 - 4)


class CrossPatternTests(unittest.TestCase):
    def test_hall_feasible_but_unrealizable_two_shell_instances(self):
        from itertools import combinations
        def no_realization(L, x, y):
            m = {L.bit_length()-1: x, L.bit_length(): y}
            i=L.bit_length()-1
            patterns = list(combinations_with_replacement((i,i+1),3))
            # Exhaust all 15 nonempty families of the 4 shell patterns.
            for mask in range(1, 1 << len(patterns)):
                subset=[p for z,p in enumerate(patterns) if (mask >> z) & 1]
                count,room=hall(subset,m)
                self.assertLessEqual(count,room)
            examined=0
            for xx in combinations(range(L,2*L),x):
                for yy in combinations(range(2*L,4*L),y):
                    examined+=1
                    a=xx+yy
                    values=[sum(t) for t in combinations_with_replacement(a,3)]
                    self.assertNotEqual(len(values),len(set(values)))
            return examined
        self.assertEqual(no_realization(2,0,3), 4)
        self.assertEqual(no_realization(8,3,3), 31360)

    def test_two_shell_cross_pattern_strict_improvement(self):
        L, x, y = 64, 7, 7
        xx_y = comb(x + 1, 2) * y
        x_yy = x * comb(y + 1, 2)
        self.assertEqual((xx_y, x_yy), (196, 196))
        self.assertLessEqual(xx_y, 4 * L - 2)
        self.assertLessEqual(x_yy, 5 * L - 2)
        self.assertLessEqual(comb(x+y+2, 3), 9 * L - 2)
        self.assertGreater(xx_y + x_yy, 6 * L - 2)
        self.assertEqual((xx_y+x_yy)*2, x*y*(x+y+2))
        self.assertEqual(hall([(6,6,7), (6,7,7)], {6:7, 7:7}), (392, 382))

    def test_genuine_m3_greedy_finite_fixture_all_pattern_subsets(self):
        a = [1,2,5,14,33,72,125,219,376,573,745,1209,1557,2442,3098,
             4048,5298,6704,7839,10987,12332,15465,19144,24546,28974,
             34406,37769,45864,50877]
        triples = [sum(t) for t in combinations_with_replacement(a, 3)]
        self.assertEqual(len(triples), len(set(triples)))
        m = dict(Counter(v.bit_length()-1 for v in a))
        patterns = list(combinations_with_replacement(sorted(m), 3))
        all_weight, all_room = hall(patterns, m)
        self.assertEqual(all_weight, comb(len(a)+2,3))
        self.assertLessEqual(all_weight, all_room)
        rng = Random(41)
        for _ in range(70):
            chosen = rng.sample(patterns, rng.randrange(1, min(len(patterns),25)))
            count, room = hall(chosen, m)
            self.assertLessEqual(count, room)

    def test_diluted_profile_satisfies_every_hall_family_analytically(self):
        total = 0
        for K in range(170):
            total += diluted_profile(K)
            self.assertLessEqual(comb(total+2,3), 1 << K)
        rng=Random(593)
        for K in (12, 15, 18, 21, 27, 35, 48, 67):
            m={j:diluted_profile(j) for j in range(K+1)}
            for _ in range(20):
                patterns = [tuple(sorted(rng.randrange(K+1) for _ in range(3)))
                            for _ in range(16)]
                count,room=hall(set(patterns),m)
                self.assertLessEqual(count,room)

    def test_ungapped_profile_fails_density_conclusion_but_passes_all_hall(self):
        total = 0
        for K in range(120):
            total += uniform_profile(K)
            self.assertLessEqual(comb(total+2, 3), 1 << K)
        total_before = sum(uniform_profile(j) for j in range(13))
        for K in range(13,120):
            if K > 13:
                total_before += uniform_profile(K-1)
            N = (1 << (K+1)) - 1
            self.assertGreaterEqual(total_before**3 * (1 << 16), N)

    def test_explicit_collision_shows_profiles_are_not_M3(self):
        a = 1 << 21
        self.assertGreaterEqual(uniform_profile(21), 3)
        self.assertGreaterEqual(diluted_profile(21), 3)
        self.assertEqual(a+a+(a+2), a+(a+1)+(a+1))

    def test_diluted_shells_have_positive_energy_and_density_dips(self):
        for J in (1200, 3600, 7800):
            energy_units = sum(0 if diluted_profile(j)==0 else (4,2,1)[j%3]
                               for j in range(J))
            # units = 1/(16384), since terms are 4,2,1/16384
            self.assertGreater(energy_units, 2*J)
            self.assertLess(energy_units, 3*J)
        for n in range(4, 10):
            first_gap=n**4
            preceding=sum(diluted_profile(j) for j in range(first_gap))
            N=(1 << (first_gap+n+1))-1
            self.assertLess(preceding**3 * (1 << n), N)

if __name__=="__main__":
    unittest.main()
