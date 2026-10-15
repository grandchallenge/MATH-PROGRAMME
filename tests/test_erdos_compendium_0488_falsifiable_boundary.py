"""Finite exact certificates for #488; not a universal decision procedure."""

from itertools import combinations
from math import lcm


def multiples_count(A: tuple[int, ...], x: int) -> int:
    return sum(any(t % a == 0 for a in A) for t in range(1, x + 1))


def complement_count(A: tuple[int, ...], x: int) -> int:
    return sum(all(t % a != 0 for a in A) for t in range(1, x + 1))


def inclusion_exclusion_count(A: tuple[int, ...], x: int) -> int:
    total = 0
    for k in range(1, len(A) + 1):
        for indices in combinations(A, k):
            total += (-1 if k % 2 == 0 else 1) * (x // lcm(*indices))
    return total


def primitive(A: tuple[int, ...]) -> bool:
    return all(a == b or b % a != 0 for a in A for b in A)


def test_488_complement_counterexample_does_not_refute_corrected_conjecture():
    A = (2, 3, 5, 7)
    assert (complement_count(A, 10), complement_count(A, 20)) == (1, 5)
    assert complement_count(A, 20) * 10 >= 2 * complement_count(A, 10) * 20
    assert (multiples_count(A, 10), multiples_count(A, 20)) == (9, 15)
    assert multiples_count(A, 20) * 10 < 2 * multiples_count(A, 10) * 20
    assert 1 + complement_count(A, 20) + multiples_count(A, 20) == 21


def test_488_singleton_sharpness_bounded_exact():
    for a in range(2, 501):
        n, m = 2 * a - 1, 2 * a
        assert multiples_count((a,), n) == 1
        assert multiples_count((a,), m) == 2
        assert (m // a) * n < 2 * (n // a) * m
        # The density ratio equals 2 - 1/a exactly.
        assert n * 2 == (2 * a - 1) * 2


def test_488_primitive_core_exhaustive_exact_bounded_sweep():
    checked = 0
    for maximum in range(2, 13):
        for selector in range(1 << (maximum - 2)):
            A = (maximum,) + tuple(
                a for a in range(2, maximum) if selector & (1 << (a - 2))
            )
            if not primitive(A):
                continue
            counts = [0] * 81
            for x in range(1, 81):
                counts[x] = counts[x - 1] + any(x % a == 0 for a in A)
                assert counts[x] == inclusion_exclusion_count(A, x)
            for n in range(maximum, 41):
                for m in range(n + 1, 81):
                    checked += 1
                    assert counts[m] * n < 2 * counts[n] * m, (A, n, m)
    assert checked == 427167


def test_488_redundant_generators_have_same_membership():
    for selector in range(1, 1 << 8):
        A = tuple(a for a in range(2, 10) if selector & (1 << (a - 2)))
        reduced = tuple(a for a in A if not any(b != a and a % b == 0 for b in A))
        for x in (1, 10, 40, 80):
            assert multiples_count(A, x) == multiples_count(reduced, x)
    # 1 is always trivial, as the pinned formal reduction assumes.
    for n in (1, 5, 13):
        assert multiples_count((1, 3, 8), n) == n
