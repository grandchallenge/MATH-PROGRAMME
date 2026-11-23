"""Independent exact replay for CSM-G2 WP04 structural-zero memory proofs.

No neural inference, stochastic sampling, or reliance on the certificate's
rank routine for independent cylinder-probability calculations.
"""
import sys
import unittest
from fractions import Fraction as F
from itertools import product
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "research" / "csm-001"))
from observable_memory_certificate import (
    ObservableFiniteMemory, composed_xor_lift, observed_markov, phase_mixture,
    phase_mixture_conditional_ones,
)


def direct_stride_two_xor_probability(word, p):
    """Brute-force independent X_0,...,X_(m+1), with Z_i=X_i XOR X_(i+2)."""
    m = len(word)
    mass = F(0)
    for hidden in product((0, 1), repeat=m+2):
        if all((hidden[i] ^ hidden[i+2]) == z for i, z in enumerate(word)):
            k = sum(hidden)
            mass += p**k * (1-p)**(m+2-k)
    return mass


def product_matrix(a, b):
    n = len(a)
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(n))
                       for j in range(n)) for i in range(n))


class TestObservableMemoryCertificate(unittest.TestCase):
    def test_zero_tolerant_lift_matches_independent_two_layer_enumeration(self):
        for p in (F(1, 2), F(3, 4)):
            c = composed_xor_lift(p)
            self.assertEqual(c.dimension, 4)
            self.assertIsNone(c.full_support_obstruction())
            for n in range(0, 7):
                total = F(0)
                for word in product((0, 1), repeat=n):
                    with self.subTest(parameter=p, word=word):
                        observed = c.word_probability(word)
                        self.assertEqual(observed,
                                         direct_stride_two_xor_probability(word, p))
                        total += observed
                self.assertEqual(total, 1)

    def test_exact_iid_certificate_for_fair_overlapping_composition(self):
        c = composed_xor_lift(F(1, 2))
        self.assertEqual(c.minimal_linear_dimension, 1)
        self.assertEqual(len(c.right_basis), 1)
        decision = c.check_reverse_order(0)
        self.assertEqual(decision["outcome"], "certified")
        self.assertEqual(c.find_finite_reverse_order()["order"], 0)
        for n in range(1, 7):
            for word in product((0, 1), repeat=n):
                self.assertEqual(c.word_probability(word), F(1, 2)**n)

    def test_biased_same_graph_has_no_finite_memory(self):
        c = composed_xor_lift(F(3, 4))
        self.assertEqual(c.minimal_linear_dimension, 4)
        self.assertEqual(len(c.right_basis), 4)
        self.assertEqual(max(len(w) for w, _ in c.right_basis), 2)
        self.assertEqual(c.check_reverse_order(0)["outcome"], "counterexample")
        decision = c.find_finite_reverse_order()
        self.assertEqual(decision["outcome"],
                         "no_finite_order_under_external_theorem")
        self.assertEqual(decision["external_cutoff"], 6)
        self.assertEqual(len(decision["witnesses"]), 7)
        for k, witness in enumerate(decision["witnesses"]):
            self.assertEqual(witness["order"], k)
            self.assertNotEqual(witness["baseline"], witness["extended"])
            a = witness["symbol"]
            u = witness["prefix"]
            v = witness["tail"]
            self.assertEqual(witness["baseline"],
                             c.word_probability((a,) + u) / c.word_probability(u))
            self.assertEqual(witness["extended"],
                             c.word_probability((a,) + u + v) /
                             c.word_probability(u + v))
            self.assertLessEqual(len(v), c.dimension-1)

    def test_same_support_all_words_despite_opposite_memory_classes(self):
        fair = composed_xor_lift(F(1, 2))
        biased = composed_xor_lift(F(3, 4))
        for a, b in zip(fair.matrices, biased.matrices):
            self.assertEqual(tuple(tuple(x > 0 for x in row) for row in a),
                             tuple(tuple(x > 0 for x in row) for row in b))
        n = fair.dimension
        identity = tuple(tuple(F(int(i == j)) for j in range(n)) for i in range(n))
        for word in product((0, 1), repeat=4):
            signatures = []
            for model in (fair, biased):
                a = identity
                for z in word:
                    a = product_matrix(a, model.matrices[z])
                signatures.append(tuple(tuple(x > 0 for x in row) for row in a))
                self.assertTrue(any(a[i][j] == 0 for i in range(n) for j in range(n)))
            self.assertEqual(signatures[0], signatures[1])

    def test_non_iid_markov_output_has_reverse_order_one(self):
        P = ((F(4, 5), F(1, 5)), (F(1, 3), F(2, 3)))
        pi = (F(5, 8), F(3, 8))
        c = observed_markov(P, pi)
        self.assertEqual(c.minimal_linear_dimension, 2)
        self.assertEqual(c.check_reverse_order(0)["outcome"], "counterexample")
        self.assertEqual(c.check_reverse_order(1)["outcome"], "certified")
        self.assertEqual(c.find_finite_reverse_order()["order"], 1)
        for n in range(1, 7):
            for word in product((0, 1), repeat=n):
                direct = pi[word[0]]
                for i in range(n-1):
                    direct *= P[word[i]][word[i+1]]
                self.assertEqual(c.word_probability(word), direct)

    def test_forbidden_words_rejected_not_misclassified(self):
        alternating = ObservableFiniteMemory(
            (F(1, 2), F(1, 2)),
            (((0, 1), (0, 0)), ((0, 0), (1, 0))),
        )
        self.assertEqual(alternating.full_support_obstruction(), (0, 0))
        self.assertEqual(alternating.check_reverse_order(1)["outcome"],
                         "outside_full_shift")
        singleton = ObservableFiniteMemory((1,), (((1,),), ((0,),)))
        self.assertEqual(singleton.full_support_obstruction(), (1,))

    def test_phase_mixture_is_iid_only_at_exact_balance(self):
        balanced = phase_mixture(F(1, 2), F(1, 2))
        distinct = phase_mixture(F(49, 100), F(51, 100))
        self.assertEqual(balanced.minimal_linear_dimension, 1)
        self.assertEqual(balanced.check_reverse_order(0)["outcome"], "certified")
        self.assertEqual(distinct.minimal_linear_dimension, 2)
        self.assertEqual(distinct.find_finite_reverse_order()["outcome"],
                         "no_finite_order_under_external_theorem")
        for a, b in zip(balanced.matrices, distinct.matrices):
            self.assertEqual(tuple(tuple(x > 0 for x in row) for row in a),
                             tuple(tuple(x > 0 for x in row) for row in b))
        self.assertEqual(phase_mixture_conditional_ones(F(1,2), F(1,2), 90, 90),
                         F(1,2))

    def test_nearby_non_gibbs_phase_mixture_finite_word_discrepancy(self):
        center, delta = F(1, 2), F(1, 1000)
        distinct = phase_mixture(center-delta, center+delta)
        for n in range(1, 8):
            tv = sum((abs(distinct.word_probability(w) - center**n)
                      for w in product((0, 1), repeat=n)), F(0)) / 2
            self.assertLessEqual(tv, n*delta)
        lower = phase_mixture_conditional_ones(center-delta, center+delta,
                                                0, 2000)
        upper = phase_mixture_conditional_ones(center-delta, center+delta,
                                                2000, 0)
        self.assertLess(lower, center)
        self.assertGreater(upper, center)
        self.assertEqual(
            phase_mixture_conditional_ones(center-delta, center+delta, 0, 0),
            center
        )

    def test_invalid_models_and_orders(self):
        with self.assertRaises(ValueError):
            composed_xor_lift(0)
        with self.assertRaises(ValueError):
            phase_mixture(0, F(1, 2))
        with self.assertRaises(ValueError):
            phase_mixture_conditional_ones(F(1, 3), F(2, 3), -1)
        with self.assertRaises(ValueError):
            ObservableFiniteMemory((F(1,2), F(1,2)),
                                   (((1, 0), (0, 0)),))
        with self.assertRaises(ValueError):
            observed_markov(((F(1, 2), F(1, 2)), (F(1, 2), F(1, 2))),
                            (F(2,3), F(1,3)))
        c = composed_xor_lift(F(1, 2))
        with self.assertRaises(ValueError):
            c.check_reverse_order(-1)
        with self.assertRaises(ValueError):
            c.word_probability((3,))


if __name__ == "__main__":
    unittest.main()
