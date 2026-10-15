"""EC-BULK-005 #775-781 exact finite fixtures.

Regression evidence for definitions and examples only. No asymptotic theorem,
primary-source proof, formal Lean check, or editorial admission is certified.
"""
import itertools
import math
import unittest


def hypergraph_maximal_clique_sizes(n, k, edges):
    """All maximal complete vertex-set sizes; complete below k is vacuous."""
    E = {frozenset(e) for e in edges}
    subsets = [frozenset(s) for t in range(n + 1)
               for s in itertools.combinations(range(n), t)]
    def complete(s):
        return all(frozenset(e) in E for e in itertools.combinations(s, k))
    maximal = [s for s in subsets if complete(s)
               and not any(complete(s | {v}) for v in range(n) if v not in s)]
    return {len(s) for s in maximal}


def antichain_with_multiplicity(family, r):
    sets = list(map(frozenset, family))
    if len(sets) != len(set(sets)):
        return False
    if any(a < b or b < a for a, b in itertools.combinations(sets, 2)):
        return False
    sizes = {len(s) for s in sets}
    return all(sum(len(s) == size for s in sets) >= r for size in sizes)


def comparable_edges(family):
    s = list(map(frozenset, family))
    return sum(a < b or b < a for a, b in itertools.combinations(s, 2))


def clique_number(n, edges):
    E = {frozenset(e) for e in edges}
    return max(k for k in range(1, n + 1)
               if any(all(frozenset(p) in E for p in itertools.combinations(s, 2))
                      for s in itertools.combinations(range(n), k)))


def is_prime(n):
    return n >= 2 and all(n % d for d in range(2, math.isqrt(n) + 1))


def is_disjoint_matching(edges, k):
    return any(len(set().union(*(set(e) for e in matching))) == sum(map(len, matching))
               for matching in itertools.combinations(edges, k))


def descending(seq):
    return all(seq[i] - seq[i - 1] >= seq[i + 1] - seq[i]
               for i in range(1, len(seq) - 1))


def ascending(seq):
    return all(seq[i] - seq[i - 1] <= seq[i + 1] - seq[i]
               for i in range(1, len(seq) - 1))


class Erdos775Through781(unittest.TestCase):
    def test_775_maximal_sizes_not_all_complete_sizes(self):
        n, k = 4, 3
        self.assertEqual(hypergraph_maximal_clique_sizes(n, k, []), {2})
        self.assertEqual(hypergraph_maximal_clique_sizes(
            n, k, itertools.combinations(range(n), k)), {4})
        # Test all 2^4 three-edge choices on four vertices.
        triples = list(itertools.combinations(range(4), 3))
        for mask in range(1 << len(triples)):
            E = [e for i, e in enumerate(triples) if mask & (1 << i)]
            sizes = hypergraph_maximal_clique_sizes(4, 3, E)
            self.assertTrue(sizes)
            self.assertTrue(all(2 <= x <= 4 for x in sizes))

    def test_776_antichain_multiplicity_and_thinning(self):
        F = [{1, 2}, {3, 4}, {1, 3}, {2, 4}]
        self.assertTrue(antichain_with_multiplicity(F, 2))
        self.assertTrue(antichain_with_multiplicity(F[:2], 2))
        self.assertFalse(antichain_with_multiplicity([{1}, {1, 3}], 1))
        self.assertEqual({len(s) for s in F}, {2})

    def test_777_strict_comparability_count(self):
        F = [set(), {1}, {2}, {1, 2}]
        self.assertEqual(comparable_edges(F), 5)

    def test_778_k3_unbiased_clique_tie_always_bob(self):
        edges = list(itertools.combinations(range(3), 2))
        for alice in itertools.combinations(edges, 2):
            bob = [e for e in edges if e not in alice]
            self.assertEqual(clique_number(3, alice), 2)
            self.assertEqual(clique_number(3, bob), 2)

    def test_779_first_ten_prime_witnesses(self):
        witnesses = [(2, 6, 3, 5, 11), (3, 30, 5, 7, 37),
                     (4, 210, 7, 13, 223), (5, 2310, 11, 23, 2333),
                     (6, 30030, 13, 17, 30047),
                     (7, 510510, 17, 19, 510529),
                     (8, 9699690, 19, 23, 9699713),
                     (9, 223092870, 23, 37, 223092907),
                     (10, 6469693230, 29, 61, 6469693291)]
        primes = [p for p in range(2, 31) if is_prime(p)]
        for n, product, largest, q, candidate in witnesses:
            self.assertEqual(math.prod(primes[:n]), product)
            self.assertEqual(primes[n - 1], largest)
            self.assertTrue(largest < q < product)
            self.assertTrue(is_prime(q))
            self.assertEqual(product + q, candidate)
            self.assertTrue(is_prime(candidate))

    def test_780_sharp_threshold_sample_and_all_colourings(self):
        for n in [4, 5]:
            edges = list(itertools.combinations(range(n), 2))
            if n == 4:
                red = {e for e in edges if 3 not in e}
                blue = set(edges) - red
                self.assertFalse(is_disjoint_matching(red, 2))
                self.assertFalse(is_disjoint_matching(blue, 2))
            else:
                for mask in range(1 << len(edges)):
                    red = {e for i, e in enumerate(edges) if mask & (1 << i)}
                    blue = set(edges) - red
                    self.assertTrue(is_disjoint_matching(red, 2) or
                                    is_disjoint_matching(blue, 2))

    def test_781_reflection_transforms_descending_to_ascending(self):
        self.assertTrue(descending((1, 3, 4)))
        self.assertTrue(ascending((2, 3, 5)))
        for n in range(3, 13):
            for k in (3, 4):
                for seq in itertools.combinations(range(1, n + 1), k):
                    reflected = tuple(n + 1 - x for x in reversed(seq))
                    self.assertEqual(descending(seq), ascending(reflected))
                    self.assertEqual(reflected, tuple(sorted(reflected)))


if __name__ == "__main__":
    unittest.main()
