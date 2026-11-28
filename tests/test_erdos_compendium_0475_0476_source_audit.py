"""Exact arithmetic checks for Erdős #475 and #476."""
import itertools
import unittest
from functools import lru_cache
from math import comb

PRIMES = (2, 3, 5, 7, 11, 13)

def valid(order, p):
    s = 0
    seen = set()
    for a in order:
        s = (s + a) % p
        if s in seen:
            return False
        seen.add(s)
    return True

def witness(A, p):
    A = tuple(sorted(A))
    @lru_cache(None)
    def dfs(mask, running, seen):
        if not mask:
            return ()
        for i, a in enumerate(A):
            if mask & (1 << i):
                s = (running + a) % p
                if not seen & (1 << s):
                    tail = dfs(mask ^ (1 << i), s, seen | (1 << s))
                    if tail is not None:
                        return (a,) + tail
        return None
    return dfs((1 << len(A)) - 1, 0, 0)

def sums(A, p):
    return {(a + b) % p for i, a in enumerate(A) for b in A[i + 1:]}

class ExactChecks(unittest.TestCase):
    def test_sharp(self):
        self.assertEqual(sums([0, 1, 2, 3], 11), set(range(1, 6)))
        self.assertEqual(sums([0, 1, 2, 3, 4], 7), set(range(7)))

    def test_all_476_subsets(self):
        for p in PRIMES:
            for mask in range(1 << p):
                A = [i for i in range(p) if mask >> i & 1]
                self.assertGreaterEqual(len(sums(A, p)), min(p, max(0, 2 * len(A) - 3)))

    def test_all_475_subsets(self):
        count = 0
        for p in PRIMES:
            for mask in range(1 << (p - 1)):
                A = [i + 1 for i in range(p - 1) if mask >> i & 1]
                w = witness(A, p)
                self.assertIsNotNone(w, (p, mask))
                self.assertEqual(set(w), set(A))
                self.assertTrue(valid(w, p))
                count += 1
        self.assertEqual(count, 5206)

    def test_475_brute_oracle(self):
        for p in (2, 3, 5, 7):
            for mask in range(1 << (p - 1)):
                A = tuple(i + 1 for i in range(p - 1) if mask >> i & 1)
                brute = any(valid(w, p) for w in itertools.permutations(A))
                self.assertEqual(brute, witness(A, p) is not None)

    def test_475_initial_zero_excluded(self):
        for p in (3, 5, 7, 11, 13):
            A = tuple(range(1, p))
            self.assertEqual(sum(A) % p, 0)
            self.assertTrue(valid(witness(A, p), p))
