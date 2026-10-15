"""Exact Laurent and harmonic sharpness checks for proved Littlewood #512."""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations


def correlation(frequencies):
    assert len(frequencies) == len(set(frequencies))
    return Counter(x - y for x in frequencies for y in frequencies)


def test_512_laurent_constant_coefficient_is_cardinality():
    for N in range(1, 17):
        for A in (
            tuple(range(N)),
            tuple(3*j*j-11 for j in range(N)),
            tuple((-1)**j * (2*j+1) for j in range(N)),
        ):
            counts = correlation(A)
            assert counts[0] == N
            assert sum(counts.values()) == N * N
            assert all(counts[m] == counts[-m] for m in counts)
            shifted = tuple(x + 37 for x in A)
            assert correlation(shifted) == counts


def test_512_consecutive_kernel_autocorrelation_coefficients():
    for N in range(2, 31):
        coefficients = correlation(tuple(range(N)))
        assert set(coefficients) == set(range(-N+1, N))
        for m in range(-N+1, N):
            assert coefficients[m] == N - abs(m)
        # This is the Laurent identity for |D_N|².
        assert coefficients[0] == N  # Parseval integral = N


def test_512_exact_harmonic_band_lower_bound():
    for N in (16, 20, 32, 64, 128, 256, 512):
        jmax = N // 4 - 1
        intervals = [
            (F(j, N) + F(1, 6 * N), F(j, N) + F(5, 6 * N))
            for j in range(1, jmax + 1)
        ]
        assert all(a < b <= F(1, 2) for a, b in intervals)
        assert all(intervals[i][1] < intervals[i+1][0]
                   for i in range(len(intervals)-1))
        # On each interval, numerator |sin(pi*N*t)|>=1/2 and
        # denominator |sin(pi*t)|<=pi*t; multiply lower bound by pi.
        lower_times_pi = sum(
            (F(1, 3) / (F(j) + F(5, 6)) for j in range(1, jmax + 1)),
            F(0),
        )
        harmonic_times_pi = sum(
            (F(1, 3*(j+1)) for j in range(1, jmax+1)), F(0)
        )
        assert lower_times_pi >= harmonic_times_pi > 0


def test_512_integration_of_sum_is_not_integral_of_absolute_value():
    # For A={1,...,N} all Fourier integrals vanish exactly, while
    # the L2 integral of absolute-square equals N>0.
    for N in range(1, 16):
        A = tuple(range(1, N+1))
        assert 0 not in A
        integral_of_sum = sum((int(m == 0) for m in A))
        assert integral_of_sum == 0
        assert correlation(A)[0] == N
