"""Exact finite normalization checks for Erdős #772.

Independent finite diagnostics; neither a proof of asymptotics nor a GCL
certification of the 1985 Alon-Erdos theorem.
"""
import itertools
import unittest
from collections import Counter


def ordered_convolution(A):
    return Counter(a + b for a in A for b in A)


def distinct_unordered_sums(A):
    return Counter(a + b for a, b in itertools.combinations(A, 2))


def sidon_with_diagonal(A):
    return len(set(a + b for a, b in itertools.combinations_with_replacement(A, 2))) == len(A) * (len(A) + 1) // 2


class Erdos772Normalization(unittest.TestCase):
    def test_power_sets_satisfy_k2_and_are_sidon(self):
        for n in range(2, 11):
            A = [1 << j for j in range(n)]
            self.assertEqual(max(ordered_convolution(A).values()), 2)
            self.assertTrue(sidon_with_diagonal(A))
            self.assertEqual(max(distinct_unordered_sums(A).values()), 1)

    def test_ordered_k2_forces_sidon_in_bounded_ambient_set(self):
        for n in range(2, 5):
            seen = 0
            for A in itertools.combinations(range(1, 13), n):
                if max(ordered_convolution(A).values()) <= 2:
                    seen += 1
                    self.assertTrue(sidon_with_diagonal(A), A)
            self.assertGreater(seen, 0)

    def test_three_element_diagonal_collision_has_ordered_multiplicity_three(self):
        A = [1, 2, 3]
        self.assertEqual(ordered_convolution(A)[4], 3)  # 1+3,2+2,3+1
        self.assertEqual(distinct_unordered_sums(A)[4], 1)
        self.assertFalse(sidon_with_diagonal(A))

    def test_k1_empty_for_nontrivial_sets(self):
        for A in itertools.combinations(range(1, 9), 2):
            self.assertGreaterEqual(max(ordered_convolution(A).values()), 2)


if __name__ == "__main__":
    unittest.main()
