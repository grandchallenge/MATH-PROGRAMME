"""Exact finite verification for the Erdős #41 dilation-energy Stage B gate.

Run: python -m unittest discover -s tests -p 'test_erdos41_dilation_energy_window.py' -v
No infinite B3 density, inverse theorem, or Stage C deficit is claimed.
"""
from collections import Counter
from fractions import Fraction
from itertools import combinations_with_replacement
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


def inner_pairs(u):
    return {x + y for x, y in combinations_with_replacement(sorted(u), 2)}


def positive_differences(w):
    w = sorted(w)
    return {w[j] - w[i] for i in range(len(w)) for j in range(i + 1, len(w))}


def correlation(p, h):
    return sum(1 for d in h for v in p if v - 2*d in p)


def profile(p, w, dilation=2):
    return Counter(v + dilation*z for v in p for z in w)


def collision_energy(c):
    return sum(m*(m-1)//2 for m in c.values())


def square_energy(c):
    return sum(m*m for m in c.values())


def integer_pressure(c, width, shift=0):
    """Sharp lower bound on unordered collisions from bin totals."""
    if width < 1:
        raise ValueError("width must be positive")
    totals = Counter()
    for loc, mult in c.items():
        totals[(loc-shift)//width] += mult
    pressure = 0
    for n in totals.values():
        q, r = divmod(n, width)
        pressure += width*q*(q-1)//2 + r*q
    return pressure


def cross_energy(a, b):
    return sum(m*b.get(s, 0) for s, m in a.items())


def cross_interval_bounds(a, b, width, shift=0):
    """Support-defect and Cauchy lower bounds, summed over disjoint intervals."""
    if width < 1:
        raise ValueError("width must be positive")
    bins = {}
    for loc in set(a) | set(b):
        bins.setdefault((loc-shift)//width, []).append(loc)
    support_bound = 0
    cauchy_bound = Fraction(0, 1)
    for locations in bins.values():
        ta = sum(a.get(s, 0) for s in locations)
        tb = sum(b.get(s, 0) for s in locations)
        va = sum(a.get(s, 0)*(a.get(s, 0)-1)//2 for s in locations)
        vb = sum(b.get(s, 0)*(b.get(s, 0)-1)//2 for s in locations)
        support_bound += max(0, ta + tb - va - vb - width)
        cauchy_bound += (
            Fraction((ta+tb)**2, width) - ta - tb - 2*(va+vb)
        ) / 2
    return support_bound, cauchy_bound


class DilationEnergyStageBTests(unittest.TestCase):
    def test_b3_fixture_and_positive_difference_uniqueness(self):
        self.assertEqual(len(A), 29)
        self.assertTrue(is_b3(A))
        self.assertEqual(len(set(sum(t) for t in combinations_with_replacement(A, 3))), 4495)
        for n in (8, 9, 12, 14, 16):
            w = A[n:]
            self.assertEqual(
                len(positive_differences(w)), len(w)*(len(w)-1)//2
            )

    def test_exact_dilation_identity_several_cuts(self):
        known = {8: (756, 0), 9: (900, 1), 12: (1326, 1),
                 14: (1575, 3), 16: (1768, 5), 20: (1890, 10)}
        for n, (total, overlaps) in known.items():
            with self.subTest(n=n):
                u, w = A[:n], A[n:]
                p = inner_pairs(u)
                self.assertEqual(len(p), n*(n+1)//2)
                self.assertEqual(total, len(p)*len(w))
                f1, f2 = profile(p, w, 1), profile(p, w, 2)
                h = positive_differences(w)
                self.assertEqual(square_energy(f1), total)
                self.assertEqual(
                    square_energy(f2) - square_energy(f1),
                    2*correlation(p, h)
                )
                self.assertEqual(correlation(p, h), overlaps)
                self.assertEqual(collision_energy(f2), overlaps)

    def test_integer_pressure_is_sharp_on_singleton_cells(self):
        u,w = A[:14], A[14:]
        c = profile(inner_pairs(u), w, 2)
        self.assertEqual(collision_energy(c), 3)
        self.assertEqual(integer_pressure(c, 1), 3)
        self.assertEqual(integer_pressure(c, 2), 2)
        self.assertEqual(integer_pressure(c, 4), 0)
        for width in (1,2,4,8,16,32,64,128,512):
            for shift in (0, width//2):
                with self.subTest(width=width, shift=shift):
                    self.assertLessEqual(
                        integer_pressure(c, width, shift), 3
                    )

    def test_exact_cross_bin_localized_identity(self):
        u, w = A[:14], A[14:]
        p = inner_pairs(u)
        bins = [w[:3], w[3:7], w[7:]]
        self.assertEqual(list(map(len, bins)), [3,4,8])
        profiles = [profile(p, b) for b in bins]
        h_parts = []
        overlap_sum = 0
        for i in range(len(bins)):
            for j in range(i+1, len(bins)):
                h = {high-low for low in bins[i] for high in bins[j]}
                h_parts.append(h)
                o = cross_energy(profiles[i], profiles[j])
                self.assertEqual(o, correlation(p, h))
                overlap_sum += o
                for width in (1,2,4,8,16,32,64):
                    for shift in (0,width//2):
                        support, cauchy = cross_interval_bounds(
                            profiles[i], profiles[j], width, shift)
                        self.assertLessEqual(support, o)
                        self.assertLessEqual(cauchy, o)
        union = set().union(*h_parts)
        self.assertEqual(sum(map(len, h_parts)), len(union))
        self.assertEqual(overlap_sum, correlation(p, union))
        self.assertLessEqual(overlap_sum, 3)

    def test_positive_localized_two_bin_certificate(self):
        p = inner_pairs(A[:14])
        w = A[14:]
        low, high = w[:3], w[3:]
        h = {b-a for a in low for b in high}
        self.assertEqual(len(h), len(low)*len(high))
        self.assertEqual(correlation(p, h), 1)
        lo, hi = profile(p, low), profile(p, high)
        self.assertEqual(cross_energy(lo, hi), 1)
        support, cauchy = cross_interval_bounds(lo, hi, 2)
        self.assertEqual(support, 1)
        self.assertLessEqual(cauchy, 1)

    def test_zero_overlap_is_real_not_an_implicit_contradiction(self):
        p = inner_pairs(A[:8])
        w = A[8:]
        self.assertEqual(correlation(p, positive_differences(w)), 0)
        self.assertEqual(integer_pressure(profile(p, w), 1), 0)
        low, high = w[:5], w[5:]
        self.assertEqual(cross_energy(profile(p, low), profile(p, high)), 0)

    def test_non_b3_hostile_control_breaks_e1_injectivity(self):
        u, w = [1,2,3], [4,5]
        self.assertFalse(is_b3(sorted(u+w)))
        p = inner_pairs(u)
        self.assertEqual(len(p), 5)  # pair sums collide already
        f1 = profile(p, w, 1)
        self.assertEqual(len(p)*len(w), 10)
        self.assertEqual(square_energy(f1), 18)
        self.assertGreater(square_energy(f1), len(p)*len(w))

    def test_sidon_digit_lift_is_a_zero_gate_hostile_fixture(self):
        p, q = 5, 151
        e = [i + 2*p*((i*i)%p) for i in range(4)]
        lifted_u = [q*a+e[i//3] for i,a in enumerate(A[:12])]
        lifted_w = [q*a for a in A[12:]]
        self.assertTrue(is_b3(sorted(lifted_u+lifted_w)))
        inner = inner_pairs(lifted_u)
        self.assertEqual(len(inner), 78)
        self.assertEqual(
            correlation(inner, positive_differences(lifted_w)), 0
        )


if __name__ == "__main__":
    unittest.main()
