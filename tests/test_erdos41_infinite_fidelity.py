"""Executable finite-prefix checks of the explicitly proved infinite digit lift.

Not a substitute for the universal written lemma or a Lean infinity proof.
"""
from itertools import combinations, combinations_with_replacement
import json
import unittest

SEEDS = {
    "exact_only": (1, 2, 3),
    "historical_not_multiset": (1, 3, 5),
    "multiset_not_historical": (1, 4, 5),
}

def exact_three_unique(elements):
    sums = [sum(x) for x in combinations(elements, 3)]
    return len(sums) == len(set(sums))

def at_most_three_unique(elements):
    sums = [sum(t) for k in range(4) for t in combinations(elements,k)]
    return len(sums) == len(set(sums))

def multiset_three_unique(elements):
    sums = [sum(x) for x in combinations_with_replacement(elements, 3)]
    return len(sums) == len(set(sums))

class InfiniteDigitLiftTests(unittest.TestCase):
    def test_all_prefixes_match_infinite_theorem(self):
        for n in range(1, 7):
            tail = tuple(100**k for k in range(1,n+1))
            for seed_name, seed in SEEDS.items():
                with self.subTest(n=n,seed=seed_name):
                    a = seed+tail
                    self.assertTrue(exact_three_unique(a))
                    self.assertEqual(at_most_three_unique(a),
                                     seed_name=="historical_not_multiset")
                    self.assertEqual(multiset_three_unique(a),
                                     seed_name=="multiset_not_historical")
    def test_base_digits_have_no_carry(self):
        for seed in SEEDS.values():
            for n in range(1,6):
                a=seed+tuple(100**k for k in range(1,n+1))
                for t in combinations_with_replacement(a,3):
                    value=sum(t)
                    self.assertEqual(value%100, sum(x for x in t if x<100))
                    self.assertLess(value%100,100)

if __name__=="__main__": unittest.main()
