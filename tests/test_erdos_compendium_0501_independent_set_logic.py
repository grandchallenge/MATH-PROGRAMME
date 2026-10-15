"""Finite directed-relation semantics for #501, NOT ZFC independence evidence."""

from itertools import combinations


def independent(xset: frozenset[int], forbidden: tuple[frozenset[int], ...]) -> bool:
    """Every ordered pair of DISTINCT selected points must be allowed."""
    return all(
        x not in forbidden[y]
        for x in xset
        for y in xset
        if x != y
    )


def independent_alternate(xset: frozenset[int], forbidden: tuple[frozenset[int], ...]) -> bool:
    """Pairwise unordered edges: reject if EITHER directed membership is forbidden."""
    for x, y in combinations(sorted(xset), 2):
        if x in forbidden[y] or y in forbidden[x]:
            return False
    return True


def all_subsets(n: int):
    return (
        frozenset(i for i in range(n) if mask & (1 << i))
        for mask in range(1 << n)
    )


def test_501_empty_and_diagonal_only_are_fully_independent():
    for n in range(1, 9):
        empty = tuple(frozenset() for _ in range(n))
        diagonal = tuple(frozenset((i,)) for i in range(n))
        x = frozenset(range(n))
        assert independent(x, empty)
        assert independent(x, diagonal)
        assert independent_alternate(x, diagonal)
        assert independent(frozenset(), diagonal)
        # The original independence condition does not ban x in A_x.


def test_501_off_diagonal_blocks_pairs_and_order_matters():
    for n in range(2, 8):
        forbidden = tuple(frozenset(j for j in range(n) if j != i) for i in range(n))
        accepted = [x for x in all_subsets(n) if independent(x, forbidden)]
        assert max(map(len, accepted)) == 1
        assert len(accepted) == 1 + n
    asym = (frozenset((1,)), frozenset(), frozenset())
    assert not independent(frozenset((0, 1)), asym)
    assert not independent_alternate(frozenset((0, 1)), asym)
    assert independent(frozenset((0, 2)), asym)


def test_501_all_small_directed_relations_match_independent_algorithm():
    for n in range(4):
        # Enumerate all directed relations, including self loops.
        for edges in range(1 << (n * n)):
            forbidden = tuple(
                frozenset(x for x in range(n) if edges & (1 << (n * y + x)))
                for y in range(n)
            )
            for x in all_subsets(n):
                assert independent(x, forbidden) == independent_alternate(x, forbidden)
