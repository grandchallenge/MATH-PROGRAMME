"""Exact finite ordered self-avoiding-walk counts for open #528.

No finite count or decimal numerical estimate determines mu_k exactly.
"""
from itertools import product


def directions(k):
    assert k >= 1
    return tuple(tuple(sign if axis == j else 0 for axis in range(k))
                 for j in range(k) for sign in (-1, 1))


def count_and_endpoint_histograms(k, max_steps):
    dirs = directions(k)
    origin = (0,) * k
    counts = [0] * (max_steps + 1)
    hist = [{} for _ in range(max_steps + 1)]
    visited = {origin}

    def visit(position, depth):
        counts[depth] += 1
        dist_sq = sum(a * a for a in position)
        hist[depth][dist_sq] = hist[depth].get(dist_sq, 0) + 1
        if depth == max_steps:
            return
        for step in dirs:
            nxt = tuple(a + b for a, b in zip(position, step))
            if nxt not in visited:
                visited.add(nxt)
                visit(nxt, depth + 1)
                visited.remove(nxt)

    visit(origin, 0)
    return counts, hist


def brute_force_count(k, n):
    origin = (0,) * k
    count = 0
    for steps in product(directions(k), repeat=n):
        p = origin
        seen = {p}
        for step in steps:
            p = tuple(a + b for a, b in zip(p, step))
            if p in seen:
                break
            seen.add(p)
        else:
            count += 1
    return count


def test_528_exact_square_lattice_counts():
    counts, hist = count_and_endpoint_histograms(2, 8)
    assert counts == [1, 4, 12, 36, 100, 284, 780, 2172, 5916]
    for n, c in enumerate(counts):
        assert sum(hist[n].values()) == c


def test_528_one_dimensional_and_three_dimensional_counts():
    line, _ = count_and_endpoint_histograms(1, 8)
    assert line == [1] + [2] * 8
    cube, _ = count_and_endpoint_histograms(3, 7)
    assert cube[:5] == [1, 6, 30, 150, 726]
    assert all(cube[n] >= 3**n for n in range(8))


def test_528_submultiplicativity_exact_prefixes():
    for k in (1, 2, 3):
        counts, _ = count_and_endpoint_histograms(k, 7)
        for m in range(8):
            for n in range(8 - m):
                assert counts[m + n] <= counts[m] * counts[n]
        for n in range(1, 8):
            assert k**n <= counts[n] <= 2*k*(2*k-1)**(n-1)
    # Fekete gives mu=inf_n c_n^(1/n) for all n, and k<=mu<=2k-1.


def test_528_independent_step_sequence_enumerator_cross_check():
    for k in (1, 2, 3):
        counts, _ = count_and_endpoint_histograms(k, 4)
        for n in range(5):
            assert counts[n] == brute_force_count(k, n)
