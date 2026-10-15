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


    def test_complete_pairtype_sidon_digit_lift(self):
        # Explicit quadratic-order Sidon code: k=4, prime p=5.
        k, p = 4, 5
        q = 6*p*p + 1
        labels = [i + 2*p*((i*i) % p) for i in range(k)]
        self.assertEqual(labels, [0, 11, 42, 43])
        self.assertLess(3*max(labels), q)
        type_labels = [labels[i] + labels[j]
                       for i in range(k) for j in range(i, k)]
        self.assertEqual(len(set(type_labels)), k*(k+1)//2)

        blocks = [[q*a + labels[i] for a in block]
                  for i, block in enumerate(self.blocks)]
        outer = [q*a for a in self.outer]
        lifted = [a for block in blocks for a in block] + outer
        self.assertTrue(is_b3(lifted))
        self.assertEqual(len(set(b3_sums(lifted))), 4495)

        pairtypes = {}
        for i in range(k):
            for j in range(i, k):
                if i == j:
                    pairtypes[(i, j)] = pair_sums(blocks[i])
                else:
                    pairtypes[(i, j)] = {
                        a+b for a in blocks[i] for b in blocks[j]
                    }
        self.assertEqual(len(pairtypes), 10)
        self.assertEqual(sum(map(len, pairtypes.values())), 78)
        self.assertEqual(
            len(set().union(*pairtypes.values())), 78
        )

        twice_differences = {2*h for h in positive_differences(outer)}
        self.assertEqual(len(twice_differences), 136)
        for alpha, pa in pairtypes.items():
            for beta, pb in pairtypes.items():
                if alpha == beta:
                    continue
                with self.subTest(alpha=alpha, beta=beta):
                    self.assertFalse(
                        {a-b for a in pa for b in pb} & twice_differences
                    )

    def test_sidon_label_scaling(self):
        # Elementary prime-table replay, no appeal to randomness.
        for k, p in ((2, 3), (3, 3), (4, 5), (5, 5), (7, 7), (11, 11)):
            q = 6*p*p + 1
            e = [i + 2*p*((i*i) % p) for i in range(k)]
            paircodes = [(e[i]+e[j]) % q
                         for i in range(k) for j in range(i, k)]
            with self.subTest(k=k):
                self.assertEqual(len(paircodes), k*(k+1)//2)
                self.assertEqual(len(set(paircodes)), len(paircodes))
                self.assertGreater(q, 3*max(e))
                self.assertGreaterEqual(q, len(paircodes))


    def test_complete_selector_and_binary_refinement(self):
        # One geometric inner block is the adversarial case for coloring:
        # all pair types coincide before refinement. Use 14 inner points
        # and 15 outer points from a genuine B3 fixture.
        inner, outer = BASE[:14], BASE[14:]
        pair_by_sum = {
            inner[i]+inner[j]: (i,j)
            for i in range(len(inner)) for j in range(i,len(inner))
        }
        hset = positive_differences(outer)
        events = [
            (pair, pair_by_sum[p-2*h])
            for p,pair in pair_by_sum.items()
            for h in hset if p-2*h in pair_by_sum
        ]
        M = len(events)
        self.assertEqual(M, 3)
        # Unique B2 pair labels and positive h give exact singleton capture.
        self.assertTrue(all(a != b for a,b in events))
        # Every positive and negative pair has disjoint vertex supports.
        self.assertTrue(
            all(set(a).isdisjoint(set(b)) for a,b in events)
        )
        # Distinct inner/outer differences eliminate double diagonals.
        self.assertTrue(
            all(not(a[0]==a[1] and b[0]==b[1]) for a,b in events)
        )

        def captured(mask):
            result = 0
            for a,b in events:
                ca = tuple(sorted(((mask >> a[0]) & 1, (mask >> a[1]) & 1)))
                cb = tuple(sorted(((mask >> b[0]) & 1, (mask >> b[1]) & 1)))
                result += (ca != cb)
            return result

        total = 0
        best = 0
        for mask in range(1 << len(inner)):
            value = captured(mask)
            total += value
            best = max(best, value)
        # Exact expectation bound >= 5/8, no simulation.
        self.assertGreaterEqual(8*total, 5*M*(1 << len(inner)))
        self.assertGreaterEqual(8*best, 5*M)

        # A complete Sidon type lift can still make total M vanish.
        p, q = 5, 151
        e = [i+2*p*((i*i) % p) for i in range(4)]
        lifted_inner = [q*a+e[i//3] for i,a in enumerate(BASE[:12])]
        lifted_outer = [q*a for a in BASE[12:]]
        self.assertEqual(
            correlation_on_positive_outer_differences(
                lifted_inner, lifted_inner, lifted_outer
            ), 0
        )


if __name__ == "__main__":
    unittest.main()
