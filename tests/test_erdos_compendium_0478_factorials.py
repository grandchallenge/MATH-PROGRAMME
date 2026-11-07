"""Finite arithmetic source fixtures for Erdős #478.

No finite modular residue list proves the conjectured density (1-1/e).
The independent 2026 p**(8/15) claim requires an incidence theorem audit.
"""

from math import factorial, isqrt


def prime(n: int) -> bool:
    return n >= 2 and all(n % k != 0 for k in range(2, isqrt(n) + 1))


def factorial_residues(p: int) -> set[int]:
    assert prime(p)
    return {factorial(k) % p for k in range(1, p)}


def _check_test_478_factorial_residue_examples() -> None:
    expected = {
        2: {1}, 3: {1, 2}, 5: {1, 2, 4}, 7: {1, 2, 3, 6},
        11: {1, 2, 5, 6, 10}, 13: {1, 2, 3, 5, 6, 7, 9, 11, 12},
    }
    for p, result in expected.items():
        assert factorial_residues(p) == result


def _check_test_478_quotient_set_is_every_nonzero_residue() -> None:
    for p in range(2, 102):
        if not prime(p):
            continue
        A = factorial_residues(p)
        quotients = {(a * pow(b, -1, p)) % p for a in A for b in A}
        assert quotients == set(range(1, p))
        assert len(A) * len(A) >= p - 1
        if p >= 5:
            assert len(A) <= p - 2
        else:
            assert len(A) > p - 2  # The common blanket p-2 bound is false.


def _check_test_478_2026_author_transition_identity_only() -> None:
    # Verifies an early arithmetic lemma, NOT the incidence-based exponent.
    for p in (3, 5, 7, 11, 13, 17, 19, 23, 29):
        A = factorial_residues(p)
        pairs = set()
        for n in range(p - 2):
            x = factorial(n) % p
            a = factorial(n + 1) % p
            z = factorial(n + 2) % p
            assert x != 0 and a != 0
            assert (a + a * a * pow(x, -1, p)) % p == z
            assert x in A and a in A and z in A
            pairs.add((x, a))
        assert len(pairs) == p - 2


import unittest


class CompendiumFiniteQA(unittest.TestCase):
    def test_478_factorial_residue_examples(self):
        _check_test_478_factorial_residue_examples()

    def test_478_quotient_set_is_every_nonzero_residue(self):
        _check_test_478_quotient_set_is_every_nonzero_residue()

    def test_478_2026_author_transition_identity_only(self):
        _check_test_478_2026_author_transition_identity_only()
