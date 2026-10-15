"""Exact small-set checks for Erdős #774: dissociation and finite colourings.

These are finite normalization fixtures, not a solution of the open infinitary
partition question.
"""
import itertools
import unittest


def dissociated(values):
    sums = [sum(combo) for size in range(len(values) + 1)
            for combo in itertools.combinations(values, size)]
    return len(sums) == len(set(sums))


def no_signed_relation(values):
    return not any(sum(a * e for a, e in zip(values, coeffs)) == 0
                   for coeffs in itertools.product((-1, 0, 1), repeat=len(values))
                   if any(coeffs))


def alpha(values):
    return max(size for size in range(len(values) + 1)
               if any(dissociated(combo) for combo in itertools.combinations(values, size)))


def chromatic(values):
    for r in range(1, len(values) + 1):
        for assignment in itertools.product(range(r), repeat=len(values)):
            if all(dissociated([a for a, color in zip(values, assignment) if color == j])
                   for j in range(r)):
                return r
    return 0


class DissociationFiniteFixtures(unittest.TestCase):
    def test_subset_sums_equivalent_to_signed_relation(self):
        for n in range(1, 5):
            for values in itertools.combinations(range(1, 8), n):
                self.assertEqual(dissociated(values), no_signed_relation(values))

    def test_three_element_relation_and_partition(self):
        self.assertFalse(dissociated((1, 2, 3)))
        self.assertEqual(alpha((1, 2, 3)), 2)
        self.assertEqual(chromatic((1, 2, 3)), 2)
        self.assertTrue(dissociated((1, 2)))

    def test_binary_powers_are_dissociated(self):
        values = (1, 2, 4, 8, 16, 32)
        self.assertTrue(dissociated(values))
        self.assertEqual(alpha(values), len(values))
        self.assertEqual(chromatic(values), 1)

    def test_finite_density_chromatic_necessity(self):
        for values in ((1, 2, 3), (1, 2, 3, 4), (1, 2, 3, 4, 5, 6),
                       (1, 3, 4, 7, 9)):
            c = chromatic(values)
            self.assertGreater(c, 0)
            self.assertGreaterEqual(alpha(values) * c, len(values))


if __name__ == "__main__":
    unittest.main()
