"""Exact finite checks for Erdős #459; not a proof of density one."""
import math
import unittest

def is_u_smooth(v, u):
    while v > 1:
        d = math.gcd(v, u)
        if d == 1:
            return False
        v //= d
    return True

def f(u):
    return next(v for v in range(u + 1, u * u + 1) if is_u_smooth(v, u))

class Erdos459FiniteTests(unittest.TestCase):
    def test_examples(self):
        expected = {2: 4, 3: 9, 6: 8, 14: 16, 30: 32,
                    31: 961, 62: 64, 126: 128}
        for u, v in expected.items():
            self.assertEqual(f(u), v)
    def test_global_finite_bounds(self):
        for u in range(2, 201):
            assert f(u) >= u + 2
            assert f(u) <= u * u

    def test_extreme_families(self):
        for k in range(2, 9):
            u = 2 ** k - 2
            assert f(u) == u + 2
        for p in range(2, 100):
            if all(p % d for d in range(2, math.isqrt(p) + 1)):
                assert f(p) == p * p
