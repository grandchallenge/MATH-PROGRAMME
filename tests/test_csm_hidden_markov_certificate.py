"""CSM-G2 exact finite tests for positive transition / observation channels."""
import math
import sys
import unittest
from fractions import Fraction
from itertools import product
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "research" / "csm-001"))
from hidden_markov_certificate import HiddenMarkovCertificate, compose_emissions

Q = Fraction


def specimen():
    return HiddenMarkovCertificate(
        ((Q(4, 5), Q(1, 5)), (Q(1, 3), Q(2, 3))),
        ((1, 0), (Q(1, 4), Q(3, 4))),
        (Q(5, 8), Q(3, 8)),
    )


class TestPositiveHiddenMarkovCertificate(unittest.TestCase):
    def test_source_semantics_and_symbol_masses(self):
        c = specimen()
        self.assertEqual(c.ratio, Q(4))
        self.assertEqual(c.kappa, Q(3, 5))
        self.assertEqual(c.output_masses, (Q(23, 32), Q(9, 32)))
        self.assertEqual(c.conditional_before_future(()), c.output_masses)

    def test_exact_forward_against_independent_enumeration(self):
        c = specimen()
        for n in range(0, 6):
            for word in product((0, 1), repeat=n):
                with self.subTest(word=word):
                    self.assertEqual(c.word_probability(word),
                                     c.word_probability_by_enumeration(word))
                    self.assertGreater(c.word_probability(word), 0)

    def test_conditional_as_cylinder_ratio_and_nonnull(self):
        c = specimen()
        for n in range(0, 5):
            for future in product((0, 1), repeat=n):
                q = c.conditional_before_future(future)
                for a in (0, 1):
                    self.assertEqual(
                        q[a], c.word_probability((a,) + future) /
                        c.word_probability(future))
                    self.assertGreaterEqual(q[a], c.positive_lower_bound(a))

    def test_uniform_exponential_log_variation(self):
        c = specimen()
        for prefix_len in range(1, 6):
            bound = 2 * math.log(float(c.ratio)) * float(c.kappa) ** (prefix_len - 1)
            for common in product((0, 1), repeat=prefix_len):
                for suffix1, suffix2 in product(
                        list(product((0, 1), repeat=2)), repeat=2):
                    p = c.conditional_before_future(common + suffix1)
                    q = c.conditional_before_future(common + suffix2)
                    for a in (0, 1):
                        self.assertLessEqual(
                            abs(math.log(float(p[a] / q[a]))), bound + 1e-12)

    def test_emission_composition_and_no_normalization_loss(self):
        first = ((1, 0, 0), (Q(1, 4), Q(1, 4), Q(1, 2)))
        second = ((Q(1, 2), Q(1, 2)), (1, 0), (0, 1))
        composed = compose_emissions(first, second)
        self.assertEqual(composed, ((Q(1, 2), Q(1, 2)),
                                    (Q(3, 8), Q(5, 8))))
        c = HiddenMarkovCertificate(
            ((Q(4, 5), Q(1, 5)), (Q(1, 3), Q(2, 3))),
            composed, (Q(5, 8), Q(3, 8)))
        self.assertEqual(c.ratio, specimen().ratio)
        self.assertEqual(c.kappa, specimen().kappa)
        for n in range(1, 5):
            for word in product((0, 1), repeat=n):
                self.assertEqual(c.word_probability(word),
                                 c.word_probability_by_enumeration(word))

    def test_degenerate_rank_one_transition_and_zero_emissions(self):
        c = HiddenMarkovCertificate(
            ((Q(1, 2), Q(1, 2)), (Q(1, 2), Q(1, 2))),
            ((1, 0), (0, 1)), (Q(1, 2), Q(1, 2)))
        self.assertEqual(c.kappa, 0)
        for future in product((0, 1), repeat=4):
            self.assertEqual(c.conditional_before_future(future), (Q(1, 2), Q(1, 2)))

    def test_preflight_rejects_false_hypotheses(self):
        with self.assertRaises(ValueError):
            HiddenMarkovCertificate(((1, 0), (Q(1, 2), Q(1, 2))),
                                    ((1, 0), (0, 1)), (Q(1, 2), Q(1, 2)))
        with self.assertRaises(ValueError):
            HiddenMarkovCertificate(((Q(1, 2), Q(1, 2)),) * 2,
                                    ((1, 0), (1, 0)), (Q(1, 2), Q(1, 2)))
        with self.assertRaises(ValueError):
            HiddenMarkovCertificate(((Q(4, 5), Q(1, 5)), (Q(1, 3), Q(2, 3))),
                                    ((1, 0), (0, 1)), (Q(1, 2), Q(1, 2)))
        with self.assertRaises(ValueError):
            compose_emissions(((1, 0),), ((1, 0, 0),))


if __name__ == "__main__":
    unittest.main()
