"""Erdős #469: exact finite primitive-pseudoperfect fixtures.

This does not prove convergence of the primitive reciprocal series. A July 2026
claimed solution and external Lean development await independent GCL review.
"""

from functools import lru_cache


@lru_cache(maxsize=None)
def pseudoperfect(n: int) -> bool:
    """Subset-sum of distinct positive proper divisors equals n."""
    if n <= 1:
        return False
    divs = [d for d in range(1, n) if n % d == 0]
    reachable = {0}
    for d in divs:
        reachable |= {s + d for s in tuple(reachable) if s + d <= n}
    return n in reachable


def primitive_pseudoperfect(n: int) -> bool:
    return pseudoperfect(n) and all(
        not pseudoperfect(d) for d in range(1, n) if n % d == 0
    )


def _check_test_469_exact_positive_membership_examples() -> None:
    assert primitive_pseudoperfect(6)  # 6 = 1+2+3
    assert primitive_pseudoperfect(20)  # 20 = 1+4+5+10
    assert primitive_pseudoperfect(28)  # 28 = 1+2+4+7+14
    assert pseudoperfect(12) and not primitive_pseudoperfect(12)
    assert not pseudoperfect(70)  # 70 is weird, not pseudoperfect


def _check_test_469_initial_primitive_pseudoperfect_sequence() -> None:
    expected = [6, 20, 28, 88, 104, 272, 304, 350, 368, 464, 490, 496]
    actual = [n for n in range(1, 501) if primitive_pseudoperfect(n)]
    assert actual == expected


def _check_test_469_divisor_primitivity_not_enough_for_convergence() -> None:
    # The prime set is primitive under divisibility, yet its reciprocal
    # series diverges. The stronger pseudoperfect structure is essential.
    # This test checks only finite nondivisibility, not divergence.
    primes = [
        k for k in range(2, 101)
        if all(k % d for d in range(2, int(k**0.5) + 1))
    ]
    assert all(a != b and b % a for i, a in enumerate(primes)
               for b in primes[i+1:])


import unittest


class CompendiumFiniteQA(unittest.TestCase):
    def test_469_exact_positive_membership_examples(self):
        _check_test_469_exact_positive_membership_examples()

    def test_469_initial_primitive_pseudoperfect_sequence(self):
        _check_test_469_initial_primitive_pseudoperfect_sequence()

    def test_469_divisor_primitivity_not_enough_for_convergence(self):
        _check_test_469_divisor_primitivity_not_enough_for_convergence()
