"""WP09-M finite source-exact large-prime localization; no cofinal claim."""
from collections import defaultdict
from fractions import Fraction
from math import isqrt

from experiments.erdos249_full_series_phase.cofactor_two_copy_transfer import (
    COMPONENT_UNITS_ERROR, SCALE, _largest_prime_factors, root_of_unity_fixed,
)
from experiments.erdos249_full_series_phase.fourier_probe import totients
from experiments.erdos249_full_series_phase.full_window_prime_projection import (
    cook_minimal_depth, cook_numerator_direct,
)


def localized_gate(X, H, upper):
    """Exact finite sufficient gate for the full real harmonic."""
    if type(X) is not int or type(H) is not int or X < 1 or not 0 <= H <= X:
        raise ValueError("invalid population")
    if not isinstance(upper, (int, Fraction)) or isinstance(upper, bool) or upper < 0:
        raise ValueError("invalid exact energy upper bound")
    margin = H - Fraction(X, 10)
    return margin >= 0 and H * upper <= margin**2


def certified_localized_energy(X, h=1, max_X=20000):
    """Use full Cook numerator and exact rational root enclosures."""
    if any(type(v) is not int or v < 1 for v in (X, h, max_X)) or X > max_X:
        raise ValueError("invalid finite scope")
    L = max(26+h, cook_minimal_depth(X, h))
    Q = 1 << L
    t = L-25
    phi = totients(2*X+h+L+4)
    lpf = _largest_prime_factors(2*X+t)
    groups = defaultdict(lambda: [0, 0, 0])
    D = cook_numerator_direct(phi, X, h, L)
    for N in range(X, 2*X):
        if N in (X, X+X//2, 2*X-1):
            if D != cook_numerator_direct(phi, N, h, L):
                raise AssertionError("rolling/direct Cook mismatch")
        p = lpf[N+t]
        m = (N+t)//p
        if p > 2*isqrt(X) and m <= isqrt(X)//2 and m**5 <= X:
            re, im = root_of_unity_fixed(D % Q, L)
            g = groups[m]
            g[0] += 1
            g[1] += re
            g[2] += im
        if N < 2*X-1:
            D = 2*D-Q*(phi[N+h+1]-phi[N+1])+(phi[N+h+L+1]-phi[N+L+1])
    H = sum(g[0] for g in groups.values())
    approx = sum((Fraction(re**2+im**2, n*SCALE**2)
                  for n, re, im in groups.values()), Fraction())
    upper = approx + Fraction(8*H*COMPONENT_UNITS_ERROR, SCALE)
    return dict(X=X, h=h, L=L, t=t, H=H, groups=len(groups),
                energy_upper=upper, finite_gate=localized_gate(X, H, upper),
                cofinal="OPEN", MATHCERT="NOT_SUBMITTED")
