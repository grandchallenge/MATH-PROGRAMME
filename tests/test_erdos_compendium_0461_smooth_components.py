"""Finite, reproducible Erdős #461 fixtures; no asymptotic certification."""
from math import lcm
import unittest


def smooth_component(m: int, t: int) -> int:
    assert m > 0 and t >= 2
    ans = 1
    for p in range(2, t):
        if any(p % d == 0 for d in range(2, int(p ** 0.5) + 1)):
            continue
        while m % p == 0:
            ans *= p
            m //= p
    return ans


def distinct_components(n: int, t: int) -> set[int]:
    return {smooth_component(n + i, t) for i in range(1, t + 1)}


class Erdos461FiniteTests(unittest.TestCase):
    def test_high_components_cannot_collide(self):
        for t in range(2, 46):
            for n in (1, 13, 91, 1407302):
                values = [smooth_component(n + i, t) for i in range(1, t + 1)]
                self.assertEqual(len([x for x in values if x >= t]),
                                 len(set(x for x in values if x >= t)))

    def test_periodic_maximal_examples(self):
        for t in range(2, 40):
            n = lcm(*range(1, t + 1)) ** 2
            values = [smooth_component(n + i, t) for i in range(1, t + 1)]
            expected = [smooth_component(i, t) for i in range(1, t + 1)]
            self.assertEqual(values, expected)
            self.assertEqual(len(set(values)), t - int(all(t % d for d in range(2, int(t ** 0.5) + 1))))

    def test_hall_counterexample_reported_in_forum(self):
        n, t = 1407302, 38
        values = {i: smooth_component(n + i, t) for i in range(1, t + 1)}
        D = (13, 15, 16, 17, 18, 19)
        neighbours = {values[i] for i in values if any(values[i] % d == 0 for d in D)}
        self.assertEqual(len(neighbours), 5)
        self.assertEqual(len(distinct_components(n, t)), 27)
        self.assertEqual(sorted(i for i in values if values[i] in neighbours), [9, 10, 13, 26, 28])

    def test_exact_small_density(self):
        # t=5, y=2, Q=12; s_5(m)=1 on four classes and =2 on two.
        values = [smooth_component(m, 5) for m in range(1, 13)]
        self.assertEqual(values.count(1), 4)
        self.assertEqual(values.count(2), 2)
        self.assertEqual(sum(x <= 2 for x in values), 6)
