"""Exact grid of signed complex sums and mandatory open/closed counterexamples."""

from itertools import product
from math import comb


def signed_sums(z: tuple[complex, ...]) -> tuple[complex, ...]:
    return tuple(
        sum(s * v for s, v in zip(signs, z))
        for signs in product((-1, 1), repeat=len(z))
    )


def count_disc(z: tuple[complex, ...], center: complex, *, closed: bool) -> int:
    # All grid coordinates are Gaussian integers / halves, so squares are exact
    # binary rationals; no boundary rounding risk in this finite fixture.
    scores = (abs(s - center) ** 2 for s in signed_sums(z))
    return sum(score <= 1 if closed else score < 1 for score in scores)


def test_498_closed_disc_fails_at_weak_norm_boundary():
    assert count_disc((1 + 0j,), 0j, closed=True) == 2 > comb(1, 0)
    assert count_disc((1 + 0j,), 0j, closed=False) == 0
    assert count_disc((1 + 0j, 1 + 0j), 1 + 0j, closed=True) == 3 > comb(2, 1)
    assert count_disc((1 + 0j, 1 + 0j), 1 + 0j, closed=False) == 0


def test_498_middle_layer_sharpness_for_open_disc():
    for n in range(1, 21):
        center = 0j if n % 2 == 0 else 1 + 0j
        z = (1 + 0j,) * n
        assert count_disc(z, center, closed=False) == comb(n, n // 2)


def test_498_grid_complex_vectors_and_centers_exact():
    options = (1 + 0j, -1 + 0j, 1j, -1j, 1 + 1j, 2 + 0j)
    centers = tuple(complex(a / 2, b / 2) for a in range(-4, 5) for b in range(-4, 5))
    for n in range(5):
        maximum = comb(n, n // 2)
        for z in product(options, repeat=n):
            # No endpoint deduplication: sign vectors remain distinct.
            sums = signed_sums(z)
            assert len(sums) == 1 << n
            for center in centers:
                found = sum(abs(s - center) ** 2 < 1 for s in sums)
                assert found <= maximum, (n, z, center, found)


def test_498_real_antichain_separation_for_nested_sign_sets():
    for n in range(1, 7):
        z = tuple(1 + (i % 3) for i in range(n))
        for lower in range(1 << n):
            for upper in range(1 << n):
                if lower != upper and lower & upper == lower:
                    v1 = sum((1 if lower & (1 << i) else -1) * z[i] for i in range(n))
                    v2 = sum((1 if upper & (1 << i) else -1) * z[i] for i in range(n))
                    assert v2 - v1 >= 2
