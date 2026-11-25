"""Exact finite controls for the collision-moment liquid comparison.

This checks polynomial, weight and label computations. The source estimates
and cochain equivalences are proved in the accompanying mathematical returns.
"""

from collections import Counter
from fractions import Fraction
from itertools import combinations, permutations
from math import comb, prod


def multiaffine_lift(values, power):
    """Evaluate the normalized symmetric multiaffine lift of x**power."""
    return sum(
        (prod(terms) for terms in combinations(values, power)),
        Fraction(0),
    ) / comb(len(values), power)


def product_monomial(*factors):
    """A symmetric monomial of (component, block size, center power) labels."""
    return tuple(sorted(factor for monomial in factors for factor in monomial))


def extend_support(monomial, component_map):
    return tuple(sorted(
        (component_map[component], size, power)
        for component, size, power in monomial
    ))


def cross_wick(left_moments, right_moments):
    """Cross coefficient from P_0(x,y)=(y-x)/2 on left < right."""
    left_mass, left_first = left_moments
    right_mass, right_first = right_moments
    return (left_mass * right_first - left_first * right_mass) / 2


def check_pair_and_separated_product():
    center = Fraction(7, 5)
    normal = Fraction(3, 4)
    left = center + normal / 2
    right = center - normal / 2
    assert multiaffine_lift((left, right), 0) == 1
    assert multiaffine_lift((left, right), 1) == center
    quadratic = multiaffine_lift((left, right), 2)
    assert quadratic == center**2 - normal**2 / 4
    assert 2 * (quadratic - center**2) / normal**2 == Fraction(-1, 2)

    mass = (Fraction(1), Fraction(0))
    first = (Fraction(0), Fraction(1))
    assert cross_wick((Fraction(1), Fraction(-2)), (Fraction(1), Fraction(3))) == Fraction(5, 2)
    assert cross_wick(mass, first) - cross_wick(first, mass) == 1

    left_mass = (("left", 1, 0),)
    left_first = (("left", 1, 1),)
    right_mass = (("right", 1, 0),)
    right_first = (("right", 1, 1),)
    merged = {"left": "outer", "right": "outer"}
    mixed = product_monomial(left_mass, right_first)
    reversed_moments = product_monomial(left_first, right_mass)
    assert mixed != reversed_moments
    assert extend_support(mixed, merged) == extend_support(reversed_moments, merged)
    assert all(size == 1 for _, size, _ in extend_support(mixed, merged))
    for power in range(3):
        pair = (("left", 2, power),)
        assert extend_support(pair, merged) == (("outer", 2, power),)


def free_moment_ranks(arity_cutoff, components):
    """Count graded polynomial monomials by inserting each generator once."""
    ranks = [1] + [0] * arity_cutoff
    for size in range(1, arity_cutoff + 1):
        for _ in range(components * (size + 1)):
            for arity in range(size, arity_cutoff + 1):
                ranks[arity] += ranks[arity - size]
    return ranks


def check_ranks_and_block_normalization():
    for components in range(5):
        arity_ranks = free_moment_ranks(2, components)
        assert arity_ranks[1] == 2 * components
        assert 1 + arity_ranks[2] == 1 + 6 * components + 4 * comb(components, 2)
    assert free_moment_ranks(4, 1) == [1, 2, 6, 14, 33]

    for size in range(1, 7):
        values = tuple(Fraction(index, size) for index in range(size))
        for power in range(size + 1):
            assert multiaffine_lift((Fraction(3, 5),) * size, power) == Fraction(3, 5)**power
            assert multiaffine_lift(values, power) == multiaffine_lift(values[::-1], power)
            span = (
                multiaffine_lift((Fraction(5), *values[1:]), power)
                + multiaffine_lift((Fraction(-5), *values[1:]), power)
            )
            assert span == 2 * multiaffine_lift((Fraction(0), *values[1:]), power)

    triple = (("left", 3, 3),)
    pair = (("left", 2, 2),)
    separated_spectator = (("right", 1, 0),)
    merged = {"left": "outer", "right": "outer"}
    assert extend_support(triple, merged) == (("outer", 3, 3),)
    assert extend_support(product_monomial(pair, separated_spectator), merged) == (
        ("outer", 1, 0), ("outer", 2, 2)
    )

    def canonical_pairs(labels):
        return tuple(sorted((
            tuple(sorted(labels[:2])),
            tuple(sorted(labels[2:])),
        )))

    placements = Counter(canonical_pairs(labels) for labels in permutations(range(4)))
    assert sorted(placements.values()) == [8, 8, 8]
    assert sum(Fraction(count, 24) for count in placements.values()) == 1
    assert len({tuple(sorted(pair_powers)) for pair_powers in permutations((0, 1, 2), 2)}
               | {(power, power) for power in range(3)}) == 6


if __name__ == "__main__":
    check_pair_and_separated_product()
    check_ranks_and_block_normalization()
    print("collision-liquid exact finite controls: PASS")
