"""CSM G2 XOR-block obstruction: independently enumerated finite conditional replay."""
import sys
import unittest
from fractions import Fraction
from itertools import product
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "research" / "csm-001"))
from xor_block_obstruction import (
    endpoint_likelihoods, exterior_conditional, cylinder_probability,
)


def independent_brute_conditional(L, R, K, p):
    """Independent complete enumeration of all hidden spins in both exterior arms."""
    p = Fraction(p)
    left = (0,) * K + (1,) * L
    right = (1,) * R + (0,) * K
    numerator = denominator = Fraction(0)
    for l in product((0, 1), repeat=len(left) + 1):
        if any((l[j] ^ l[j+1]) != y for j, y in enumerate(left)):
            continue
        lw = p ** sum(l) * (1-p) ** (len(l)-sum(l))
        for r in product((0, 1), repeat=len(right) + 1):
            if any((r[j] ^ r[j+1]) != y for j, y in enumerate(right)):
                continue
            rw = p ** sum(r) * (1-p) ** (len(r)-sum(r))
            v = lw * rw
            denominator += v
            if l[-1] != r[0]:
                numerator += v
    return numerator / denominator


class TestXorTwoBlockObstruction(unittest.TestCase):
    def test_against_full_hidden_enumeration(self):
        for L in range(1, 4):
            for R in range(1, 4):
                for K in range(0, 3):
                    with self.subTest(L=L, R=R, K=K):
                        self.assertEqual(
                            exterior_conditional(L, R, K, Fraction(3, 4)),
                            independent_brute_conditional(L, R, K, Fraction(3, 4)))

    def test_exact_boundary_probabilities(self):
        p = Fraction(3, 4)
        self.assertEqual(exterior_conditional(2, 2, 2, p), Fraction(27, 392))
        self.assertEqual(exterior_conditional(2, 3, 2, p), Fraction(61, 70))
        for n in range(1, 9):
            self.assertEqual(exterior_conditional(n, n, 0, p),
                             Fraction(1, 2) if n % 2 else Fraction(3, 8))

    def test_opposed_limits_on_arbitrary_common_neighborhoods(self):
        p = Fraction(3, 4)
        for n in (1, 2, 3, 5, 8):
            q_match = exterior_conditional(n, n, 10, p)
            q_differ = exterior_conditional(n, n + 1, 10, p)
            self.assertLess(q_match, Fraction(1, 1000))
            self.assertGreater(q_differ, Fraction(999, 1000))

    def test_fair_coin_image_is_iid(self):
        p = Fraction(1, 2)
        for n in range(0, 7):
            for word in product((0, 1), repeat=n):
                self.assertEqual(cylinder_probability(word, p), Fraction(1, 2) ** n)
        for L in range(1, 5):
            self.assertEqual(exterior_conditional(L, L + 1, 5, p), Fraction(1, 2))
            self.assertEqual(exterior_conditional(L, L, 5, p), Fraction(1, 2))

    def test_finite_cylinder_support_and_nonnormalized_weights(self):
        for n in range(0, 7):
            masses = [cylinder_probability(word, Fraction(3, 4))
                      for word in product((0, 1), repeat=n)]
            self.assertTrue(all(m > 0 for m in masses))
            self.assertEqual(sum(masses), 1)

    def test_invalid_parameters_and_observations(self):
        with self.assertRaises(ValueError):
            exterior_conditional(-1, 1, 2)
        with self.assertRaises(ValueError):
            exterior_conditional(2, 1, 1, 1)
        with self.assertRaises(ValueError):
            endpoint_likelihoods((0, 2), Fraction(3, 4))
        with self.assertRaises(ValueError):
            cylinder_probability((1, 0, 3))


if __name__ == "__main__":
    unittest.main()
