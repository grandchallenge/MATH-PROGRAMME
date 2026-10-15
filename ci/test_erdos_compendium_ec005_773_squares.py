"""Finite exact examples for Erdős #773 (Sidon subsets of squares).

These tests establish only finite arithmetic, not asymptotic bounds.
"""
import itertools
import unittest
from collections import Counter


def squares(n):
    return tuple(k * k for k in range(1, n + 1))


def sums_with_diagonal(values):
    return [a + b for a, b in itertools.combinations_with_replacement(values, 2)]


def is_sidon(values):
    sums = sums_with_diagonal(values)
    return len(set(sums)) == len(sums)


def maximum_sidon_subset_cardinality(values):
    for k in range(len(values), -1, -1):
        if any(is_sidon(part) for part in itertools.combinations(values, k)):
            return k
    return 0


class Erdos773Squares(unittest.TestCase):
    def test_first_four_squares_are_sidon(self):
        a = squares(4)
        self.assertEqual(a, (1, 4, 9, 16))
        self.assertEqual(len(sums_with_diagonal(a)), 10)
        self.assertTrue(is_sidon(a))

    def test_seventh_square_introduces_diagonal_collision(self):
        a = squares(7)
        reps = Counter(sums_with_diagonal(a))
        self.assertEqual(reps[50], 2)
        self.assertFalse(is_sidon(a))
        self.assertEqual(1 * 1 + 7 * 7, 5 * 5 + 5 * 5)

    def test_small_exact_maxima_are_monotone(self):
        values = [maximum_sidon_subset_cardinality(squares(n)) for n in range(1, 11)]
        self.assertEqual(values[:4], [1, 2, 3, 4])
        self.assertTrue(all(a <= b <= a + 1 for a, b in zip(values, values[1:])))
        self.assertTrue(all(value <= n for n, value in enumerate(values, 1)))


if __name__ == "__main__":
    unittest.main()
