"""Exact finite fixtures for Erdős #484, Roth monochromatic sum density.

These tests verify distinct-summand semantics, a two-color obstruction,
and the missing-even Fibonacci recurrence. They cannot establish the
asymptotic theorem for arbitrary numbers of colors.
"""

from itertools import product


def target_set(colors: tuple[int, ...]) -> set[int]:
    """Count DISTINCT target values s<=N, not number of representations."""
    N = len(colors)
    return {
        a + b
        for a in range(1, N + 1)
        for b in range(a + 1, N + 1)
        if a + b <= N and colors[a - 1] == colors[b - 1]
    }


def reference_target_set(colors: tuple[int, ...]) -> set[int]:
    """Independently enumerate targets first, then search witnesses."""
    N = len(colors)
    found = set()
    for s in range(1, N + 1):
        for a in range(1, (s + 1) // 2):
            b = s - a
            if 1 <= a < b <= N and colors[a - 1] == colors[b - 1]:
                found.add(s)
                break
    return found


def odd_part_mod_four_color(n: int) -> int:
    assert n >= 1
    while n % 2 == 0:
        n //= 2
    return 0 if n % 4 == 1 else 1


def fibonacci(n: int) -> int:
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def _check_test_484_repeated_summands_are_not_allowed() -> None:
    assert target_set((0,)) == set()
    assert target_set((0, 0)) == set()  # 1+1=2 is prohibited
    assert target_set((0, 0, 0)) == {3}  # 1+2
    assert target_set((0, 0, 0, 0)) == {3, 4}
    # For one color, every s>=3 is representable using 1+(s-1).
    for N in range(3, 40):
        assert target_set((0,) * N) == set(range(3, N + 1))


def _check_test_484_independent_target_enumerations_agree() -> None:
    for k, N in ((1, 7), (2, 10), (3, 8)):
        for coloring in product(range(k), repeat=N):
            assert target_set(coloring) == reference_target_set(coloring)


def _check_test_484_two_color_odd_part_construction() -> None:
    N = 512
    colors = tuple(odd_part_mod_four_color(n) for n in range(1, N + 1))
    targets = target_set(colors)
    assert {1, 2, 4, 8, 16, 32, 64, 128, 256, 512}.isdisjoint(targets)
    assert all(s not in targets for s in (1 << j for j in range(10)))
    # The omitted family is logarithmic, not a contradiction to density.
    assert len(targets) > N // 4


def _check_test_484_missing_even_targets_grow_like_fibonacci() -> None:
    # Source 1989 p.51: successive missing even b_j satisfy
    # b_(j+2) >= b_j+b_(j+1), since otherwise a forbidden
    # same-color distinct-summand representation is forced.
    for N in range(3, 12):
        for coloring in product(range(2), repeat=N):
            good = target_set(coloring)
            bad = [s for s in range(2, N + 1, 2) if s not in good]
            for j in range(len(bad) - 2):
                assert bad[j + 2] >= bad[j] + bad[j + 1]
            for j, bj in enumerate(bad, 1):
                assert bj >= 2 * fibonacci(j + 1)


def _check_test_484_even_targets_and_k_one_edge() -> None:
    for N in range(4, 60):
        good = target_set((0,) * N)
        assert all(s in good for s in range(4, N + 1, 2))
        assert len(good) == N - 2
        assert len(good) >= N / 4


import unittest


class CompendiumFiniteQA(unittest.TestCase):
    def test_484_repeated_summands_are_not_allowed(self):
        _check_test_484_repeated_summands_are_not_allowed()

    def test_484_independent_target_enumerations_agree(self):
        _check_test_484_independent_target_enumerations_agree()

    def test_484_two_color_odd_part_construction(self):
        _check_test_484_two_color_odd_part_construction()

    def test_484_missing_even_targets_grow_like_fibonacci(self):
        _check_test_484_missing_even_targets_grow_like_fibonacci()

    def test_484_even_targets_and_k_one_edge(self):
        _check_test_484_even_targets_and_k_one_edge()
