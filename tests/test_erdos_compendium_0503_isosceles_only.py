"""Exact isosceles-set finite constructions for open #503, not global maximality."""

from fractions import Fraction
from itertools import combinations
from math import comb


def squared_distance(a, b):
    assert len(a) == len(b)
    return sum((x - y) ** 2 for x, y in zip(a, b))


def isosceles_triple(a, b, c):
    lengths = (squared_distance(a, b), squared_distance(a, c), squared_distance(b, c))
    return len(set(lengths)) <= 2


def weight_two_with_centroid(d):
    assert d >= 3
    pts = tuple(
        tuple(Fraction(int(k in (i, j))) for k in range(d + 1))
        for i, j in combinations(range(d + 1), 2)
    )
    center = tuple(Fraction(2, d + 1) for _ in range(d + 1))
    return pts + (center,)


def _check_test_503_weight_two_centroid_all_triples_exact():
    for d in range(3, 9):
        pts = weight_two_with_centroid(d)
        assert len(pts) == comb(d + 1, 2) + 1
        assert len(set(pts)) == len(pts)
        assert all(sum(p) == 2 for p in pts)  # affine dimension d, not d+1
        center = pts[-1]
        assert {
            squared_distance(center, p) for p in pts[:-1]
        } == {Fraction(2) - Fraction(4, d + 1)}
        # Check the all-triples local property, not a two-distance shortcut.
        assert all(isosceles_triple(*triple) for triple in combinations(pts, 3))
        distances = {
            squared_distance(a, b) for a, b in combinations(pts, 2)
        }
        assert distances == {
            Fraction(2), Fraction(4), Fraction(2) - Fraction(4, d + 1)
        }, (d, distances)


def _check_test_503_pentagon_with_center_combinatorial_chords():
    # 0..4 are regular pentagon vertices; 5 denotes the centre.
    # We only use exact CHORD CLASSES; numeric trigonometry is unnecessary.
    def chord_class(a, b):
        if a == 5 or b == 5:
            return 0  # all five centre-to-vertex radii equal
        gap = abs(a - b)
        return min(gap, 5 - gap)  # the only outer classes are 1 and 2

    assert {
        chord_class(a, b)
        for a, b in combinations(range(6), 2)
    } == {0, 1, 2}
    triples = list(combinations(range(6), 3))
    assert len(triples) == 20
    for a, b, c in triples:
        types = (chord_class(a, b), chord_class(a, c), chord_class(b, c))
        assert len(set(types)) <= 2, (a, b, c, types)


def _check_test_503_distinction_from_two_distance_set_502():
    # In dimension 3 the all-isosceles centroid construction has 7 points
    # and exactly THREE global distances. Croft's known true maximum is 8.
    pts = weight_two_with_centroid(3)
    assert len(pts) == 7
    assert len({
        squared_distance(a, b) for a, b in combinations(pts, 2)
    }) == 3
    # These fixtures DO NOT prove the Croft or Blokhuis upper bounds.


import unittest


class CompendiumFiniteQA(unittest.TestCase):
    def test_503_weight_two_centroid_all_triples_exact(self):
        _check_test_503_weight_two_centroid_all_triples_exact()

    def test_503_pentagon_with_center_combinatorial_chords(self):
        _check_test_503_pentagon_with_center_combinatorial_chords()

    def test_503_distinction_from_two_distance_set_502(self):
        _check_test_503_distinction_from_two_distance_set_502()
