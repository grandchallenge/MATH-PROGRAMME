"""Exact finite semantic fixtures for Erdős #487; no asymptotic proof claim."""

from itertools import combinations
from math import lcm, prod


def lcm_cube(mask: int, primes: tuple[int, ...], q: int = 1) -> int:
    assert mask < 2 ** len(primes)
    assert all(q % p for p in primes)
    return q * prod(p for i, p in enumerate(primes) if mask & (1 << i))


def triples_of_union(family: set[int]) -> set[tuple[int, int, int]]:
    return {
        (x, y, z)
        for x in family for y in family for z in family
        if len({x, y, z}) == 3 and x | y == z
    }


def triples_of_lcm(family: set[int]) -> set[tuple[int, int, int]]:
    return {
        (x, y, z)
        for x in family for y in family for z in family
        if len({x, y, z}) == 3 and lcm(x, y) == z
    }


def test_487_cube_preserves_distinct_triples_for_every_family_up_to_three_primes():
    primes = (2, 3, 5)
    for k in range(4):
        members = list(range(2 ** k))
        for selector in range(1 << len(members)):
            family = {x for x in members if selector & (1 << x)}
            union_triples = triples_of_union(family)
            for q in (1, 7, 11):
                d = {x: lcm_cube(x, primes[:k], q) for x in family}
                lcm_triples = triples_of_lcm(set(d.values()))
                assert len(set(d.values())) == len(family)
                assert lcm_triples == {
                    (d[x], d[y], d[z]) for x, y, z in union_triples
                }


def test_487_concrete_witness_and_divisibility_chain_trap():
    family = {0b011, 0b101, 0b111}
    numbers = {lcm_cube(x, (2, 3, 5)) for x in family}
    assert numbers == {6, 10, 30}
    assert (6, 10, 30) in triples_of_lcm(numbers)
    chain = {2, 4, 8, 16}
    assert all(a % b == 0 for a, b in ((4, 2), (8, 4), (16, 8)))
    # A chain has pairs with lcm equal to an INPUT, not a third distinct number.
    assert not triples_of_lcm(chain)


def test_487_union_free_middle_level_and_exhaustive_small_cases():
    # Equal-cardinality subsets have no distinct union triple.
    for k in range(1, 8):
        family = {x for x in range(2 ** k) if x.bit_count() == k // 2}
        assert not triples_of_union(family)
        assert len(family) == len(list(combinations(range(k), k // 2)))
    # Fully exhaustive Boolean lattice small sizes; empirical only.
    maxima = {}
    for k in range(4):
        maximum = 0
        for selector in range(1 << (2 ** k)):
            f = {x for x in range(2 ** k) if selector & (1 << x)}
            if not triples_of_union(f):
                maximum = max(maximum, len(f))
        maxima[k] = maximum
    assert maxima == {0: 1, 1: 2, 2: 3, 3: 5}
