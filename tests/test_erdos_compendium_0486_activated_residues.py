"""Exact finite fixtures for #486, not a proof of the unrestricted density conjecture."""

from fractions import Fraction
from itertools import combinations
from math import lcm


def is_allowed(m: int, residue_sets: dict[int, set[int]], strict: bool = True) -> bool:
    return all(
        (m <= n if strict else m < n) or (m % n not in residues)
        for n, residues in residue_sets.items()
    )


def finite_period_density(residue_sets: dict[int, set[int]], strict: bool) -> Fraction:
    period = lcm(*residue_sets) if residue_sets else 1
    # Shift every period representative beyond every activation threshold.
    accepted = sum(
        is_allowed(2 * period + r, residue_sets, strict)
        for r in range(1, period + 1)
    )
    return Fraction(accepted, period)


def test_486_two_modulus_example_and_threshold_boundary() -> None:
    x = {2: {0}, 3: {1}}
    assert finite_period_density(x, strict=True) == Fraction(1, 3)
    assert finite_period_density(x, strict=False) == Fraction(1, 3)
    assert is_allowed(2, x, strict=True)
    assert not is_allowed(2, x, strict=False)
    for m in range(4, 300):
        assert is_allowed(m, x) == (m % 6 in {3, 5})


def test_486_union_bound_all_subsets_small_moduli() -> None:
    moduli = [2, 3, 4]
    # Exhaust all possible residue-set selections for these moduli.
    powersets = [
        [set(c) for k in range(n + 1) for c in combinations(range(n), k)]
        for n in moduli
    ]
    for a in powersets[0]:
        for b in powersets[1]:
            for c in powersets[2]:
                full = {2: a, 3: b, 4: c}
                for strict in (False, True):
                    for cutoff in (0, 2, 3, 4):
                        truncated = {n: r for n, r in full.items() if n <= cutoff}
                        tail = sum(
                            (Fraction(len(r), n) for n, r in full.items() if n > cutoff),
                            Fraction(0),
                        )
                        for upper in (1, 2, 4, 6, 10, 23, 49):
                            removed = sum(
                                is_allowed(m, truncated, strict)
                                and not is_allowed(m, full, strict)
                                for m in range(1, upper + 1)
                            )
                            assert Fraction(removed, upper) <= tail


def test_486_infinite_summable_power_two_example() -> None:
    # Every integer >2 is either odd and always allowed, or even
    # and excluded by the modulus 2. n=2 survives only in strict mode.
    moduli = {2**k: {0} for k in range(1, 12)}
    for m in range(1, 2049):
        assert is_allowed(m, moduli, strict=True) == (m % 2 == 1 or m == 2)
        assert is_allowed(m, moduli, strict=False) == (m % 2 == 1)
    # Sum_{k>K} 1/2^k = 1/2^K, including K=0.
    for k in range(0, 20):
        assert sum((Fraction(1, 2**j) for j in range(k + 1, 101)), Fraction(0)) < Fraction(1, 2**k)
