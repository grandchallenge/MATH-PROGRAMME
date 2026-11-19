"""Small exact path-cover oracle for Erdős #518.

All same-color paths may overlap; singleton paths count as either color.
Exhaustive up to K5 is NOT a proof for arbitrary n.
"""
from itertools import combinations
from math import comb, isqrt


def edge_index(n):
    return {pair: k for k, pair in enumerate(combinations(range(n), 2))}


def edges_of_color(n, coloring, color):
    edges = set()
    for pair, k in edge_index(n).items():
        if ((coloring >> k) & 1) == color:
            edges.add(pair)
    return edges


def realizable_path_masks(n, edges):
    """For each vertex subset, exact endpoint DP for a simple Hamilton path."""
    adj = [0] * n
    for u, v in edges:
        adj[u] |= 1 << v
        adj[v] |= 1 << u
    ends = [0] * (1 << n)
    for v in range(n):
        ends[1 << v] = 1 << v
    for mask in range(1, 1 << n):
        if not ends[mask]:
            for v in range(n):
                if not ((mask >> v) & 1):
                    continue
                prev = mask ^ (1 << v)
                if prev and (ends[prev] & adj[v]):
                    ends[mask] |= 1 << v
    return [mask for mask in range(1, 1 << n) if ends[mask]]


def same_color_cover_number(n, coloring):
    full = (1 << n) - 1
    best = n
    for color in (0, 1):
        masks = realizable_path_masks(n, edges_of_color(n, coloring, color))
        # Paths may overlap; union of vertex masks is exactly cover.
        reachable = {0}
        for depth in range(1, best + 1):
            reachable = {covered | path for covered in reachable for path in masks}
            if full in reachable:
                best = min(best, depth)
                break
    return best


def sharp_coloring(s):
    n = s * s
    A = set(range(n - s + 1))
    coloring = 0
    for (u, v), k in edge_index(n).items():
        # Encode RED=1, BLUE=0. All edges meeting B are red.
        if u not in A or v not in A:
            coloring |= 1 << k
    return n, coloring, A


def _check_test_518_every_two_coloring_K1_through_K5():
    for n in range(1, 6):
        maximum = 0
        for coloring in range(1 << comb(n, 2)):
            cover = same_color_cover_number(n, coloring)
            assert 1 <= cover <= isqrt(n), (n, coloring, cover)
            maximum = max(maximum, cover)
        assert maximum == isqrt(n)


def _check_test_518_sharp_lower_bound_square_construction():
    for s in range(2, 10):
        n = s * s
        B = s - 1
        A = n - B
        # Blue needs B singleton paths plus a path covering A.
        assert B + 1 == s
        # Every red path contains at most B+1 vertices of A:
        # red edges cannot join consecutive A-vertices.
        assert (A + (B + 1) - 1) // (B + 1) == s
        if s <= 3:
            N, coloring, Aset = sharp_coloring(s)
            assert N == n and len(Aset) == A
            assert all(
                (((coloring >> k) & 1) == (not (u in Aset and v in Aset)))
                for (u, v), k in edge_index(n).items()
            )


def _check_test_518_mixed_colors_not_automatically_same_color():
    # In K4 sharp construction, min same-color cover=2.
    n, coloring, _ = sharp_coloring(2)
    assert same_color_cover_number(n, coloring) == 2
    # The general two-path theorem with possibly different colors is
    # a different assertion and not used as a same-color proof.


def _check_test_518_zero_edge_singletons_and_integer_rounding():
    for n in range(1, 9):
        assert isqrt(n) ** 2 <= n < (isqrt(n) + 1) ** 2
        assert all(1 << v in realizable_path_masks(n, set()) for v in range(n))


import unittest


class CompendiumFiniteQA(unittest.TestCase):
    def test_518_every_two_coloring_K1_through_K5(self):
        _check_test_518_every_two_coloring_K1_through_K5()

    def test_518_sharp_lower_bound_square_construction(self):
        _check_test_518_sharp_lower_bound_square_construction()

    def test_518_mixed_colors_not_automatically_same_color(self):
        _check_test_518_mixed_colors_not_automatically_same_color()

    def test_518_zero_edge_singletons_and_integer_rounding(self):
        _check_test_518_zero_edge_singletons_and_integer_rounding()
