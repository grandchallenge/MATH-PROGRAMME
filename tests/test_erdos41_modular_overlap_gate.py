"""Finite exact regressions for Erdős #41 modular overlap obstruction.

Run: python -m unittest discover -s tests -p 'test_erdos41_modular_overlap_gate.py'
No infinite B3 density conclusion is claimed.
"""
from itertools import combinations_with_replacement
import unittest

BASE = [
    1, 2, 5, 14, 33, 72, 125, 219, 376, 573, 745,
    1209, 1557, 2442, 3098, 4048, 5298, 6704, 7839,
    10987, 12332, 15465, 19144, 24546, 28974,
    34406, 37769, 45864, 50877,
]


def b3_sums(a):
    return [sum(t) for t in combinations_with_replacement(a, 3)]


def is_b3(a):
    triple_sums = b3_sums(a)
    return len(triple_sums) == len(set(triple_sums))


def positive_differences(a):
    return {u - v for u in a for v in a if u > v}


def pair_sums(a):
    return {x + y for x, y in combinations_with_replacement(a, 2)}


def correlation_on_positive_outer_differences(x_high, x_low, outer):
    ph, pl = pair_sums(x_high), pair_sums(x_low)
    hset = positive_differences(outer)
    return sum(
        1 for p in ph for pp in pl
        if p > pp and (p - pp) % 2 == 0 and (p - pp) // 2 in hset
    )


class ModularOverlapTests(unittest.TestCase):
    def setUp(self):
        self.blocks = [BASE[j:j + 3] for j in range(0, 12, 3)]
        self.outer = BASE[12:]

    def test_original_genuine_b3(self):
        self.assertEqual(len(BASE), 29)
        self.assertTrue(is_b3(BASE))
        self.assertEqual(len(set(b3_sums(BASE))), 4495)
        self.assertEqual(len(positive_differences(self.outer)), 136)

    def test_doubling_selector(self):
        d = {x - y for x in BASE for y in BASE}
        self.assertEqual({2*h for h in d if h != 0} & d, set())

    def test_lift_eliminates_existing_positive_cross_correlation(self):
        self.assertEqual(
            correlation_on_positive_outer_differences(
                self.blocks[3], self.blocks[0], self.outer
            ), 1
        )
        # Alternating residues on all four inner blocks.
        digits = {a: 1 + (i % 2) for i, block in enumerate(self.blocks) for a in block}
        lifted = [10*a + digits.get(a, 0) for a in BASE]
        self.assertTrue(is_b3(lifted))
        lifted_blocks = [
            [10*a + digits[a] for a in block] for block in self.blocks
        ]
        lifted_outer = [10*a for a in self.outer]
        self.assertEqual(len(positive_differences(lifted_outer)), 136)
        for i in range(4):
            for j in range(i):
                if (i - j) % 2:
                    with self.subTest(i=i, j=j):
                        self.assertEqual(
                            correlation_on_positive_outer_differences(
                                lifted_blocks[i], lifted_blocks[j], lifted_outer
                            ), 0
                        )

    def test_bad_unscaled_perturbation_is_not_b3(self):
        # Failure when q is not larger than 3K: this is an invalid lift.
        bad = [2, 4, 10, 29, 67]
        self.assertTrue(is_b3(BASE[:5]))
        self.assertFalse(is_b3(bad))

    def test_order_orientation_is_nonredundant(self):
        # Positive outer differences cannot equal pair sums of a lower
        # block minus those of a strictly higher block.
        for i in range(4):
            for j in range(i + 1, 4):
                self.assertEqual(
                    correlation_on_positive_outer_differences(
                        self.blocks[i], self.blocks[j], self.outer
                    ), 0
                )


if __name__ == "__main__":
    unittest.main()
