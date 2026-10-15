"""Exact failure cases for historical variants of Erdős #494; no global theorem."""

from collections import Counter
from itertools import combinations


def multiset_sums(A: tuple[int, ...], k: int) -> Counter[int]:
    assert len(A) == len(set(A))
    return Counter(sum(choice) for choice in combinations(A, k))


def product_exponents_mod_six(indices: tuple[int, ...], k: int) -> Counter[int]:
    assert len(indices) == len(set(indices))
    return Counter(sum(choice) % 6 for choice in combinations(indices, k))


def test_494_same_full_sum_does_not_determine_k_element_set():
    A = (0, 1, 4)
    B = (0, 2, 3)
    assert set(A) != set(B)
    assert multiset_sums(A, 3) == multiset_sums(B, 3) == Counter({5: 1})


def test_494_zero_sum_half_set_ambiguity_and_multiplicity():
    A = (-7, -3, -2, 1, 5, 6)
    B = tuple(-x for x in A)
    assert sum(A) == 0 and len(set(A)) == 6
    assert set(A) != set(B)
    assert multiset_sums(A, 3) == multiset_sums(B, 3)
    assert sum(multiset_sums(A, 3).values()) == 20
    for pair in combinations(A, 3):
        complement = set(A) - set(pair)
        assert sum(pair) == -sum(complement)


def test_494_nonzero_sixth_roots_exact_exponent_counterexample():
    # All elements are distinct NONZERO sixth roots of unity.
    A = (0, 1, 2, 4)
    B = (0, 2, 3, 4)
    assert set(A) != set(B)
    eA = product_exponents_mod_six(A, 3)
    eB = product_exponents_mod_six(B, 3)
    assert eA == eB
    assert eA == Counter({0: 1, 1: 1, 3: 1, 5: 1})


def test_494_multiset_is_not_set_and_known_k2_failure():
    A = (0, 1, 3, 4)
    B = (0, 2, 3, 3)  # repeated element invalid: don't use as distinct set
    # A product-proof cannot silently use multisets with repeated originals.
    assert len(B) != len(set(B))
    assert sum(multiset_sums(A, 2).values()) == 6
    # A true n=4 pair-sum ambiguity, inherited from the translate construction:
    C = (0, 1, 2, 5)
    D = (-1, 2, 3, 4)
    assert set(C) != set(D)
    assert multiset_sums(C, 2) == multiset_sums(D, 2)


def test_494_necessary_power_sum_coefficient_at_k2():
    # For two-sums, sum_{a<b}(a+b)^j has p_j coefficient n - 2^(j-1).
    # At n=4, j=3 the coefficient vanishes: the triangular recovery fails.
    assert 4 - 2**(3 - 1) == 0
    assert 3 - 2**(3 - 1) != 0
