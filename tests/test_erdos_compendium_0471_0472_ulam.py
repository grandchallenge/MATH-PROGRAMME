"""Source-bound mathematical finite fixtures for Erdős #471 and #472.

These checks do not certify Vinogradov's analytic theorem or prove that the
specific Ulam recurrence (3, 5) is infinite.
"""

from itertools import combinations
from math import isqrt


def prime(n: int) -> bool:
    if n < 2:
        return False
    return all(n % d for d in range(2, isqrt(n) + 1))


def closure_step(primes: set[int]) -> set[int]:
    return primes | {sum(t) for t in combinations(sorted(primes), 3)
                     if prime(sum(t))}


def ulam_step(prefix: list[int]) -> int | None:
    last = prefix[-1]
    candidates = [last + a - 1 for a in prefix if prime(last + a - 1)]
    return min(candidates) if candidates else None


def _check_test_471_named_seed_first_generations() -> None:
    q = {3, 5, 7, 11}
    assert closure_step(q) == {3, 5, 7, 11, 19, 23}
    sizes = [len(q)]
    for _ in range(3):
        q = closure_step(q)
        sizes.append(len(q))
    assert sizes == [4, 6, 12, 29]
    assert {29, 31, 37, 41, 47, 53} <= q
    assert all(prime(p) for p in q)


def _check_test_471_three_inputs_are_distinct() -> None:
    q = {3, 5, 7, 11}
    sums = {tuple(t): sum(t) for t in combinations(sorted(q), 3)}
    assert sums == {
        (3, 5, 7): 15,
        (3, 5, 11): 19,
        (3, 7, 11): 21,
        (5, 7, 11): 23,
    }
    assert closure_step(q) - q == {19, 23}


def _check_test_472_exact_starting_prefix() -> None:
    expected = [
        3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
        53, 59, 61, 67, 71, 73, 79, 83, 89, 101, 103, 107, 109,
    ]
    q = [3, 5]
    while len(q) < len(expected):
        nxt = ulam_step(q)
        assert nxt is not None and nxt > q[-1]
        assert prime(nxt)
        # This check covers the exact minimum, not only one prime witness.
        assert all(not prime(q[-1] + a - 1) for a in q
                   if q[-1] + a - 1 < nxt)
        q.append(nxt)
    assert q == expected


def _check_test_472_single_seed_can_terminate() -> None:
    assert ulam_step([5]) is None  # 5+5-1=9 is composite
    assert ulam_step([3, 5]) == 7


def _check_test_471_is_not_472() -> None:
    assert closure_step({3, 5, 7, 11}) == {3, 5, 7, 11, 19, 23}
    assert ulam_step([3, 5]) == 7


import unittest


class CompendiumFiniteQA(unittest.TestCase):
    def test_471_named_seed_first_generations(self):
        _check_test_471_named_seed_first_generations()

    def test_471_three_inputs_are_distinct(self):
        _check_test_471_three_inputs_are_distinct()

    def test_472_exact_starting_prefix(self):
        _check_test_472_exact_starting_prefix()

    def test_472_single_seed_can_terminate(self):
        _check_test_472_single_seed_can_terminate()

    def test_471_is_not_472(self):
        _check_test_471_is_not_472()
