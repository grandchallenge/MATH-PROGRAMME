"""Finite regression for Erdős #449's incorrect secondary inequality."""
import unittest


def counts(n):
    divs = [d for d in range(1, n + 1) if n % d == 0]
    return (
        len(divs),
        len({d.bit_length() - 1 for d in divs}),
        sum(1 for i, d in enumerate(divs) for e in divs[i + 1:] if e < 2 * d),
    )


class DyadicBoundTests(unittest.TestCase):
    def test_published_auxiliary_inequality_fails_at_six(self):
        tau, plus, r = counts(6)
        self.assertEqual((tau, plus, r), (4, 3, 1))
        self.assertLess((r + tau) * plus, tau * tau)

    def test_corrected_inequality_for_small_integers(self):
        for n in range(1, 513):
            with self.subTest(n=n):
                tau, plus, r = counts(n)
                self.assertGreaterEqual((2 * r + tau) * plus, tau * tau)
