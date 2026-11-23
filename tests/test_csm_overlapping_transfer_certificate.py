"""Independent finite path replay for CSM two-layer overlapping Gibbs certificate."""
import math
import sys
import unittest
from fractions import Fraction as Q
from itertools import product
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "research" / "csm-001"))
from overlapping_transfer_certificate import (
    PositiveTransferCertificate,
    TwoLayerOverlappingCertificate,
    noisy_xor_certificate,
)

P = ((Q(4, 5), Q(1, 5)), (Q(1, 3), Q(2, 3)))
PI = (Q(5, 8), Q(3, 8))
K1 = ((Q(1, 5), Q(2, 5)), (Q(3, 5), Q(4, 5)))
H1 = ((Q(1, 6), Q(1, 3)), (Q(2, 3), Q(5, 6)))


def specimen():
    K = tuple(tuple((1 - K1[s][t], K1[s][t]) for t in range(2))
              for s in range(2))
    H = tuple(tuple((1 - H1[u][v], H1[u][v]) for v in range(2))
              for u in range(2))
    return TwoLayerOverlappingCertificate(P, PI, K, H)


def independent_two_layer_enumeration(word):
    """Directly enumerate all S0..S_{m+1} and Y0..Ym; no matrix methods."""
    m = len(word)
    total = Q(0)
    for states in product((0, 1), repeat=m + 2):
        hidden = PI[states[0]]
        for i in range(m + 1):
            hidden *= P[states[i]][states[i+1]]
        for intermediate in product((0, 1), repeat=m + 1):
            weight = hidden
            for i in range(m + 1):
                a = K1[states[i]][states[i+1]]
                weight *= a if intermediate[i] else (1-a)
            for i, z in enumerate(word):
                b = H1[intermediate[i]][intermediate[i+1]]
                weight *= b if z else (1-b)
            total += weight
    return total


def independent_noisy_xor_enumeration(word, p, epsilon):
    total = Q(0)
    for hidden in product((0, 1), repeat=len(word) + 1):
        weight = p ** sum(hidden) * (1 - p) ** (len(hidden) - sum(hidden))
        for i, z in enumerate(word):
            raw = hidden[i] ^ hidden[i+1]
            weight *= (1-epsilon) if raw == z else epsilon
        total += weight
    return total


class TestTwoLayerOverlappingCertificate(unittest.TestCase):
    def test_lifted_stationary_and_sharp_exact_certificate_data(self):
        c = specimen()
        self.assertEqual(len(c.lifted_states), 4)
        self.assertEqual(c.pi, (Q(9,20), Q(7,40), Q(1,8), Q(1,4)))
        self.assertEqual(c.projective_cross_ratio, Q(256, 5))
        self.assertEqual(c.kappa, Q(251, 261))
        self.assertEqual(c.lower_bounds, (Q(93,250), Q(443,1350)))
        for j in range(c.n):
            self.assertEqual(sum(c.pi[i] * c.transition[i][j]
                                 for i in range(c.n)), c.pi[j])

    def test_exact_cylinder_probabilities_against_unrelated_enumeration(self):
        c = specimen()
        for m in range(5):
            total = Q(0)
            for word in product((0, 1), repeat=m):
                with self.subTest(word=word):
                    p = c.word_probability(word)
                    self.assertEqual(p, independent_two_layer_enumeration(word))
                    total += p
            self.assertEqual(total, 1)

    def test_finite_conditional_cylinder_identity_and_lower_bound(self):
        c = specimen()
        for m in range(5):
            for future in product((0, 1), repeat=m):
                q = c.conditional_before_future(future)
                for a in (0, 1):
                    self.assertEqual(q[a], c.word_probability((a,) + future) /
                                     c.word_probability(future))
                    self.assertGreaterEqual(q[a], c.lower_bounds[a])

    def test_uniform_projective_variation_bound(self):
        c = specimen()
        for k in range(1, 6):
            limit = math.log(float(c.projective_cross_ratio)) * float(c.kappa) ** (k-1)
            for prefix in product((0, 1), repeat=k):
                for suffix1 in product((0, 1), repeat=2):
                    for suffix2 in product((0, 1), repeat=2):
                        q1 = c.conditional_before_future(prefix + suffix1)
                        q2 = c.conditional_before_future(prefix + suffix2)
                        for a in (0, 1):
                            self.assertLessEqual(abs(math.log(float(q1[a]/q2[a]))),
                                                 limit + 1e-12)

    def test_noisy_xor_is_restored_for_every_strict_noise(self):
        p = Q(3, 4)
        for eps in (Q(1, 100), Q(1, 4), Q(1, 2), Q(3, 4), Q(99, 100)):
            c = noisy_xor_certificate(p, eps)
            self.assertLess(c.kappa, 1)
            for m in range(6):
                for word in product((0, 1), repeat=m):
                    self.assertEqual(c.word_probability(word),
                                     independent_noisy_xor_enumeration(word, p, eps))
        c = noisy_xor_certificate(p, Q(1, 4))
        self.assertEqual(c.projective_cross_ratio, 9)
        self.assertEqual(c.kappa, Q(4, 5))
        self.assertEqual(c.lower_bounds, (Q(3,8), Q(3,8)))

    def test_fair_channel_and_rank_one_boundary(self):
        c = noisy_xor_certificate(Q(3, 4), Q(1, 2))
        self.assertEqual(c.projective_cross_ratio, 1)
        self.assertEqual(c.kappa, 0)
        for m in range(6):
            for word in product((0, 1), repeat=m):
                self.assertEqual(c.word_probability(word), Q(1, 2) ** m)
                self.assertEqual(c.conditional_before_future(word), (Q(1,2), Q(1,2)))

    def test_invalid_hypotheses_rejected(self):
        c = specimen()
        with self.assertRaises(ValueError):
            noisy_xor_certificate(Q(3,4), 0)
        with self.assertRaises(ValueError):
            noisy_xor_certificate(Q(3,4), 1)
        with self.assertRaises(ValueError):
            noisy_xor_certificate(0, Q(1,4))
        with self.assertRaises(ValueError):
            c.word_probability((5,))
        with self.assertRaises(ValueError):
            PositiveTransferCertificate((Q(1,2), Q(1,2)),
                                        (((1, 0), (0, 1)),))
        with self.assertRaises(ValueError):
            TwoLayerOverlappingCertificate(
                P, (Q(1,2), Q(1,2)), c.first_channel, c.second_channel)
        bad = tuple(tuple((Q(1), Q(0)) for _ in range(2)) for _ in range(2))
        with self.assertRaises(ValueError):
            TwoLayerOverlappingCertificate(P, PI, bad, c.second_channel)


if __name__ == "__main__":
    unittest.main()
