"""Finite fixtures for Erdős #460; no asymptotic or source-status certification."""
from math import gcd
import unittest


def is_rough(m: int, a: int) -> bool:
    return all(m % d for d in range(2, a + 1))


def greedy_below_n(n: int, case: str) -> list[int]:
    assert n >= 3 and case in ("A", "B")
    selected = [1]
    for a in range(2, n):
        if case == "B" and gcd(n - a, n) != 1:
            continue
        if all(gcd(n - a, n - b) == 1 for b in selected):
            selected.append(a)
    return selected


class Erdos460FiniteTests(unittest.TestCase):
    def test_forced_rough_inclusion(self):
        for n in range(3, 251):
            rough = {a for a in range(1, n) if is_rough(n - a, a)}
            for case in ("A", "B"):
                self.assertLessEqual(rough, set(greedy_below_n(n, case)))

    def test_exact_small_cases(self):
        expected = {
            (6, "A"): [1, 2, 3, 5],
            (6, "B"): [1, 5],
            (12, "A"): [1, 2, 3, 5, 11],
            (12, "B"): [1, 5, 7, 11],
            (30, "A"): [1, 2, 3, 5, 7, 11, 13, 17, 19, 29],
            (30, "B"): [1, 7, 11, 13, 17, 19, 23, 29],
        }
        for key, values in expected.items():
            self.assertEqual(greedy_below_n(*key), values)

    def test_rough_weight_lower_bound(self):
        for n in range(3, 251):
            f = sum(1 / a for a in range(1, n) if is_rough(n - a, a))
            for case in ("A", "B"):
                self.assertGreaterEqual(sum(1 / a for a in greedy_below_n(n, case)) + 1e-12, f)

    def test_claimed_logarithmic_integral(self):
        # Integral of 1/(a log a) over [N^(1/3), N^(1/2)] is log(3/2).
        # Thus this range cannot imply growth of order log log N.
        from math import log
        self.assertAlmostEqual(log((1 / 2) / (1 / 3)), log(3 / 2), places=12)
