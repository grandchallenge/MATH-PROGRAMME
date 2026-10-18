"""Finite adversarial replay of the E3-to-H3 coding and M3 packing baseline.

The universal infinite reduction is proved in mathematical/Lean source, not inferred
from these bounded executable tests.
"""
from itertools import combinations, combinations_with_replacement
import unittest


def e3(a):
    sums = [sum(t) for t in combinations(a, 3)]
    return len(sums) == len(set(sums))


def h3(a):
    sums = [sum(t) for k in range(4) for t in combinations(a, k)]
    return len(sums) == len(set(sums))


def m3(a):
    sums = [sum(t) for t in combinations_with_replacement(a, 3)]
    return len(sums) == len(set(sums))


class DensityTransferTests(unittest.TestCase):
    def test_finite_prefixes_encode_exact_to_historical(self):
        for n in range(2, 7):
            a = (1, 2, 3) + tuple(100**k for k in range(1, n+1))
            b = tuple(4*x+1 for x in a)
            with self.subTest(n=n):
                self.assertTrue(e3(a))
                self.assertFalse(h3(a))
                self.assertTrue(h3(b))

    def test_affine_counts_exact(self):
        a = (1, 2, 3, 100, 10000, 1000000)
        b = tuple(4*x+1 for x in a)
        for threshold in range(1, 1000):
            self.assertEqual(sum(x <= threshold for x in b),
                             sum(x <= (threshold-1)//4 for x in a))

    def test_m3_packing_and_mixed_windows(self):
        a = (1, 4, 5, 100, 10000, 1000000)
        self.assertTrue(m3(a))
        self.assertLessEqual((len(a)+2)*(len(a)+1)*len(a)//6,
                             3*max(a)-2)
        blocks = ((1, 5), (100, 100), (10000, 10000))
        occupancies = [sum(lo<=x<=hi for x in a) for lo,hi in blocks]
        sum_lengths = sum(hi-lo for lo,hi in blocks)
        self.assertLessEqual(occupancies[0]*occupancies[1]*occupancies[2],
                             sum_lengths+1)

    def test_coding_does_not_repair_repetition(self):
        a = (1, 2, 3, 100, 10000)
        self.assertFalse(m3(a))
        self.assertFalse(m3(tuple(4*x+1 for x in a)))

if __name__ == '__main__':
    unittest.main()
