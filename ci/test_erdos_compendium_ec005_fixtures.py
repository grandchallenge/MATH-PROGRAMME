"""Exact finite fixtures for EC-BULK-005 problems 657–662.

These regressions test elementary examples. They are not mathematical
proofs of asymptotic statements or source-fidelity certificates.
"""

from itertools import combinations
from math import cos, pi, sin, sqrt


def squared_lattice_distance(a, b):
    return (a[0] - b[0]) ** 2 + 2 * (a[1] - b[1]) ** 2


def test_657_scalene_rectangle_and_distance_matching():
    points = [(0, 0), (2, 0), (0, 1), (2, 1)]

    def d2(a, b):
        return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2

    assert {d2(a, b) for a, b in combinations(points, 2)} == {1, 4, 5}
    assert all(
        len({d2(a, b) for a, b in combinations(triple, 2)}) == 3
        for triple in combinations(points, 3)
    )


def test_658_axis_parallel_finite_fixture():
    good = {(1, 1), (3, 1), (1, 3), (3, 3)}
    no_square = {(1, 1), (2, 1), (1, 2)}

    def has_square(a):
        return any(
            {(x, y), (x + d, y), (x, y + d), (x + d, y + d)} <= a
            for x, y in a for d in range(1, 4)
        )

    assert has_square(good)
    assert not has_square(no_square)


def test_659_all_quadruples_in_stretched_lattice():
    expected = {
        2: (3, 1),
        3: (8, 126),
        4: (14, 1820),
        5: (22, 12650),
        6: (31, 58905),
    }
    for m, (distance_count, quadruple_count) in expected.items():
        points = [(x, y) for x in range(m) for y in range(m)]
        all_d2 = {
            squared_lattice_distance(a, b)
            for a, b in combinations(points, 2)
        }
        assert len(all_d2) == distance_count
        checked = 0
        for quad in combinations(points, 4):
            assert len({
                squared_lattice_distance(a, b)
                for a, b in combinations(quad, 2)
            }) >= 3
            checked += 1
        assert checked == quadruple_count


def test_660_regular_pyramids_have_floor_m_over_two_distances():
    for m in range(3, 18):
        k = m // 2
        longest_chord = 2 * sin(pi * k / m)
        height = sqrt(longest_chord**2 - 1)
        base = [
            (cos(2 * pi * j / m), sin(2 * pi * j / m), 0.0)
            for j in range(m)
        ]
        pts = base + [(0., 0., height)]

        def squared(a, b):
            return sum((a[z] - b[z])**2 for z in range(3))

        # Numerical check of the separate symbolic chord argument.
        vals = {
            round(squared(a, b), 10)
            for a, b in combinations(pts, 2)
        }
        assert len(vals) == k
        assert height > 0


def test_661_concentric_circle_bipartite_distances():
    for n in range(3, 18):
        x = [
            (cos(2 * pi * i / n), sin(2 * pi * i / n))
            for i in range(n)
        ]
        y = [
            (2 * cos(2 * pi * j / n), 2 * sin(2 * pi * j / n))
            for j in range(n)
        ]
        vals = {
            round((a[0] - b[0])**2 + (a[1] - b[1])**2, 10)
            for a in x for b in y
        }
        assert len(vals) == n // 2 + 1


def test_662_triangular_lattice_shells():
    counts = {}
    for a in range(-6, 7):
        for b in range(-6, 7):
            if a == b == 0:
                continue
            q = a*a + a*b + b*b
            if q <= 9:
                counts[q] = counts.get(q, 0) + 1

    assert counts == {1: 6, 3: 6, 4: 6, 7: 12, 9: 6}
    assert sum(v for q, v in counts.items() if q <= 1) == 6
    assert sum(v for q, v in counts.items() if q <= 3) == 12
    assert sum(v for q, v in counts.items() if q <= 4) == 18
    assert sum(v for q, v in counts.items() if q <= 9) == 36


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print("PASS", name)
