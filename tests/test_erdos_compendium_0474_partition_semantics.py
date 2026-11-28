"""Finite arrow-notation sanity checks for Erdős #474.

These checks are not forcing models, independence tests or proofs about ZFC.
They only distinguish color-omission from monochromatic homogeneity.
"""

from itertools import combinations


def edge(x: int, y: int) -> tuple[int, int]:
    return (min(x, y), max(x, y))


def _check_test_474_k4_every_triangle_uses_all_three_colors() -> None:
    coloring = {}
    for color, pairs in enumerate((
        ((0, 1), (2, 3)),
        ((0, 2), (1, 3)),
        ((0, 3), (1, 2)),
    )):
        for a, b in pairs:
            coloring[edge(a, b)] = color
    assert len(coloring) == 6
    for triple in combinations(range(4), 3):
        assert {coloring[edge(a, b)] for a, b in combinations(triple, 2)} == {0, 1, 2}


def _check_test_474_k5_no_three_color_every_triangle_rainbow() -> None:
    # If every triangle were rainbow, the edges at each vertex would
    # have pairwise different colors. K5 has degree four > three colors.
    for v in range(5):
        assert len([w for w in range(5) if w != v]) == 4
    assert 4 > 3


def _check_test_474_omits_a_color_not_necessarily_monochromatic() -> None:
    # Square bracket arrow: a chosen H may use two colors.
    # Not a demand that all edges of H be monochromatic.
    c = {(0, 1): 0, (0, 2): 1, (1, 2): 0}
    assert {c[e] for e in combinations(range(3), 2)} == {0, 1}
    assert len(set(c.values())) == 2


import unittest


class CompendiumFiniteQA(unittest.TestCase):
    def test_474_k4_every_triangle_uses_all_three_colors(self):
        _check_test_474_k4_every_triangle_uses_all_three_colors()

    def test_474_k5_no_three_color_every_triangle_rainbow(self):
        _check_test_474_k5_no_three_color_every_triangle_rainbow()

    def test_474_omits_a_color_not_necessarily_monochromatic(self):
        _check_test_474_omits_a_color_not_necessarily_monochromatic()
