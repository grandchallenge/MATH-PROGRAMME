"""Deterministic elementary fixtures for EC-BULK-005 (#663–#669).

Does not establish the cited asymptotic bounds, Alon's random-line
construction, Chung's uniform four-color theorem, or editorial admission.
"""
import itertools
import math
import unittest


def least_missing_prime(n, k):
    product = math.prod(n + i for i in range(1, k + 1))
    for p in range(2, 1000):
        if p > 1 and all(p % a for a in range(2, math.isqrt(p) + 1)):
            if product % p:
                return p
    raise AssertionError("prime bound insufficient")


def fano_lines():
    return [{(a + i) % 7 for a in (0, 1, 3)} for i in range(7)]


class CohortFixtures(unittest.TestCase):
    def test_663_missing_prime_primorial(self):
        self.assertEqual(least_missing_prime(20, 2), 5)
        self.assertEqual(least_missing_prime(209, 2), 11)

    def test_664_projective_line_intersections(self):
        ls = fano_lines()
        self.assertEqual(len(ls), 7)
        for a, b in itertools.combinations(ls, 2):
            self.assertEqual(len(a & b), 1)

    def test_665_pairwise_balanced_fano(self):
        ls = fano_lines()
        for x, y in itertools.combinations(range(7), 2):
            self.assertEqual(sum({x, y} <= b for b in ls), 1)
        self.assertEqual(sum(math.comb(len(b), 2) for b in ls), math.comb(7, 2))

    def test_666_cube_cycle_and_direction_matchings(self):
        edges = {(x, x ^ (1 << j), j) for x in range(8) for j in range(3)
                 if x < (x ^ (1 << j))}
        self.assertEqual(len(edges), 12)
        for j in range(3):
            degrees = {}
            for a, b, color in edges:
                if color == j:
                    degrees[a] = degrees.get(a, 0) + 1
                    degrees[b] = degrees.get(b, 0) + 1
            self.assertTrue(all(deg == 1 for deg in degrees.values()))
        walk = [0, 4, 6, 7, 3, 1, 0]
        self.assertEqual(len(set(walk[:-1])), 6)
        for a, b in itertools.pairwise(walk):
            self.assertEqual((a ^ b).bit_count(), 1)

    def test_667_matching_complement(self):
        for n in range(4, 11):
            missing = {(i, i + 1) for i in range(0, n - 1, 2)}

            def edge(a, b):
                return tuple(sorted((a, b))) not in missing

            for tri in itertools.combinations(range(n), 3):
                self.assertGreaterEqual(sum(edge(a, b)
                                            for a, b in itertools.combinations(tri, 2)), 2)
            max_clique = max(len(subset)
                             for r in range(1, n + 1)
                             for subset in itertools.combinations(range(n), r)
                             if all(edge(a, b)
                                    for a, b in itertools.combinations(subset, 2)))
            self.assertEqual(max_clique, (n + 1) // 2)

    def test_668_four_point_five_unit_distances(self):
        # Represent Cartesian (u/2,v*sqrt(3)/2) by integer tuple (u,v).
        ps = [(-1, 0), (1, 0), (0, 1), (0, -1)]
        q = [(a[0]-b[0])**2 + 3*(a[1]-b[1])**2
             for a, b in itertools.combinations(ps, 2)]
        self.assertEqual(sorted(q), [4, 4, 4, 4, 4, 12])

    def test_669_single_three_rich_line(self):
        pts = [(0, 0), (1, 0), (2, 0), (0, 1)]
        lines = set()
        for (x1, y1), (x2, y2) in itertools.combinations(pts, 2):
            A, B = y2-y1, x1-x2
            C = -(A*x1+B*y1)
            g = math.gcd(math.gcd(abs(A), abs(B)), abs(C))
            A, B, C = A//g, B//g, C//g
            if A < 0 or A == 0 and B < 0:
                A, B, C = -A, -B, -C
            lines.add((A, B, C))
        rich = [line for line in lines
                if sum(A*x+B*y+C == 0 for x, y in pts
                       for A, B, C in (line,)) >= 3]
        self.assertEqual(len(rich), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
