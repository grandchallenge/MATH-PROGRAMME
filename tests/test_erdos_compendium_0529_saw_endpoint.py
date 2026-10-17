"""Exact finite endpoint laws for Erdős #529, not critical exponents."""
from collections import Counter
from itertools import product
import sympy as S


def directions(k):
    return [tuple(1 if j == i else 0 for j in range(k)) for i in range(k)] + [
        tuple(-1 if j == i else 0 for j in range(k)) for i in range(k)
    ]


def endpoint_histogram(k, n):
    origin = (0,) * k
    hist = Counter()
    mean_position = [0] * k
    seen = {origin}

    def visit(p, depth):
        if depth == n:
            r = sum(x * x for x in p)
            hist[r] += 1
            for i in range(k):
                mean_position[i] += p[i]
            return
        for step in directions(k):
            nxt = tuple(a + b for a, b in zip(p, step))
            if nxt not in seen:
                seen.add(nxt)
                visit(nxt, depth + 1)
                seen.remove(nxt)
    visit(origin, 0)
    assert not any(mean_position)
    return hist


def moment_values(hist):
    count = sum(hist.values())
    mean = S.simplify(sum(c * S.sqrt(r) for r, c in hist.items()) / count)
    mean_sq = S.Rational(sum(r*c for r,c in hist.items()), count)
    return count, mean, mean_sq


def brute_force_histogram(k, n):
    dirs = directions(k)
    ans = Counter()
    for steps in product(dirs, repeat=n):
        p = (0,) * k
        seen = {p}
        for st in steps:
            p = tuple(a + b for a,b in zip(p,st))
            if p in seen:
                break
            seen.add(p)
        else:
            ans[sum(x*x for x in p)] += 1
    return ans


def _check_test_529_square_lattice_two_step_exact_radicals():
    hist = endpoint_histogram(2, 2)
    assert hist == Counter({2:8, 4:4})
    count, mean, mean_sq = moment_values(hist)
    assert count == 12
    assert S.simplify(mean - (2+2*S.sqrt(2))/3) == 0
    assert mean_sq == S.Rational(8,3)
    assert S.simplify(mean**2 - mean_sq) < 0


def _check_test_529_line_endpoint_distance_linear():
    for n in range(1, 9):
        hist = endpoint_histogram(1,n)
        assert hist == Counter({n*n:2})
        count, mean, mean_sq = moment_values(hist)
        assert count==2 and mean==n and mean_sq==n*n


def _check_test_529_exact_histogram_reflection_parity_and_jensen():
    for k in (2,3):
        for n in range(1,7):
            hist = endpoint_histogram(k,n)
            count, mean, mean_sq = moment_values(hist)
            assert sum(hist.values()) == count
            assert all(1 <= r <= n*n for r in hist)
            # Nearest-neighbour walk gives ||endpoint||_2^2 congruent n mod 2.
            assert all(r % 2 == n % 2 for r in hist)
            assert S.simplify(mean_sq - mean**2) >= 0


def _check_test_529_independent_short_step_enumeration():
    for k in (1,2,3):
        for n in range(5):
            assert endpoint_histogram(k,n) == brute_force_histogram(k,n)
    # Neither finite n nor Duminil-Copin/Hammond sub-ballisticity
    # determines d2(n)/sqrt(n) or the 3D, 4D critical exponents.


import unittest


class CompendiumFiniteQA(unittest.TestCase):
    def test_529_square_lattice_two_step_exact_radicals(self):
        _check_test_529_square_lattice_two_step_exact_radicals()

    def test_529_line_endpoint_distance_linear(self):
        _check_test_529_line_endpoint_distance_linear()

    def test_529_exact_histogram_reflection_parity_and_jensen(self):
        _check_test_529_exact_histogram_reflection_parity_and_jensen()

    def test_529_independent_short_step_enumeration(self):
        _check_test_529_independent_short_step_enumeration()
