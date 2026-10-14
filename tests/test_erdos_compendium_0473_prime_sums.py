"""Bounded exact source checks for Erdős #473.

These checks do not reproduce Odlyzko's original one-sided infinite permutation
construction, which is cited without a located original proof.
"""

from math import isqrt


def prime(n: int) -> bool:
    return n >= 2 and all(n % d for d in range(2, isqrt(n) + 1))


def greedy_prefix(length: int) -> list[int]:
    q = [1]
    used = {1}
    for _ in range(1, length):
        last = q[-1]
        # For each finite prefix a candidate always exists: for a sufficiently
        # large prime p, x=p-last is positive and unused.
        for x in range(1, 10000):
            if x not in used and prime(last + x):
                q.append(x)
                used.add(x)
                break
        else:
            raise AssertionError("Exceeded bounded primality search")
    return q


def test_473_initial_greedy_terms_and_minimality() -> None:
    q = greedy_prefix(100)
    assert q[:25] == [
        1, 2, 3, 4, 7, 6, 5, 8, 9, 10, 13, 16, 15,
        14, 17, 12, 11, 18, 19, 22, 21, 20, 23, 24, 29,
    ]
    seen = {q[0]}
    for a, b in zip(q, q[1:]):
        assert b not in seen
        assert prime(a + b)
        assert all(x in seen or not prime(a + x) for x in range(1, b))
        seen.add(b)
    assert len(seen) == len(q)


def test_473_197_and_199_never_occur_in_greedy_prime_sums() -> None:
    # Complete finite obstruction: the 99th and 100th terms cross the
    # threshold beyond which all consecutive sums are >=200.
    q = greedy_prefix(100)
    assert set(q[:99]) == set(range(1, 100))
    assert q[98:100] == [89, 102]
    early_sums = [q[i] + q[i + 1] for i in range(99)]
    assert all(prime(s) for s in early_sums)
    assert 197 not in early_sums and 199 not in early_sums
    # All future terms belong to unused values >=100, hence any subsequent
    # sum is >=200. No heuristic or million-term extrapolation is needed.
    assert all(x >= 100 for x in q[99:])


def test_473_small_finite_prime_sum_permutation_is_not_global() -> None:
    # Example of a valid finite permutation; no claim for every n.
    q = [1, 4, 3, 2]
    assert set(q) == {1, 2, 3, 4}
    assert all(prime(a + b) for a, b in zip(q, q[1:]))
