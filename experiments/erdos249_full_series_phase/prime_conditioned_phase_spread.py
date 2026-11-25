"""WP09-N: finite exact original phase and terminal prime-pair certificates."""
from fractions import Fraction
from math import gcd

from experiments.erdos249_full_series_phase.cofactor_two_copy_transfer import (
    COMPONENT_UNITS_ERROR, SCALE, _largest_prime_factors, root_of_unity_fixed,
)
from experiments.erdos249_full_series_phase.fourier_probe import totients
from experiments.erdos249_full_series_phase.full_window_prime_projection import (
    cook_minimal_depth, cook_numerator_direct,
)


def phase_variance_interval(residues, L):
    """Exact rational enclosure of 1 minus squared complex phase mean."""
    if type(L) is not int or L < 1 or not residues:
        raise ValueError("invalid phase family")
    roots = [root_of_unity_fixed(r, L) for r in residues]
    n = len(roots)
    re = sum(a for a, _ in roots)
    im = sum(b for _, b in roots)
    estimate = 1 - Fraction(re*re + im*im, n*n*SCALE*SCALE)
    error = Fraction(8*COMPONENT_UNITS_ERROR, SCALE)
    return max(Fraction(), estimate-error), min(Fraction(1), estimate+error)


def rational_variance(values):
    if not values or any(type(v) is not int for v in values):
        raise ValueError("expected nonempty integer family")
    n = len(values)
    return Fraction(sum(v*v for v in values), n) - Fraction(sum(values), n)**2


def certified_prime_conditioned_spread(X, h, M, max_X=20000):
    """Finite Cook-legal minimal-depth specimen; M may be a small modulus.

    No asymptotic PNT claim is inferred from this finite test. The strong
    CRT ratio 1/100 in the cofinal proof need not hold for the specimen.
    """
    if (any(type(v) is not int or v < 1 for v in (X,h,M,max_X))
            or X > max_X or h > X or M < 2 or gcd(h,M) != 1):
        raise ValueError("invalid finite source scope")
    L = cook_minimal_depth(X,h)
    Q = 1 << L
    phi = totients(2*X+h+L+4)
    lpf = _largest_prime_factors(2*X+L)
    A, B, R, dp, primes = [], [], [], [], []
    D = cook_numerator_direct(phi,X,h,L)
    for N in range(X,2*X-1):
        p = N+L+1
        delta = phi[p+h]-phi[p]
        Dnext = 2*D-Q*(phi[N+h+1]-phi[N+1])+delta
        if N in (X,X+X//2,2*X-2):
            if (D != cook_numerator_direct(phi,N,h,L)
                    or Dnext != cook_numerator_direct(phi,N+1,h,L)):
                raise AssertionError("original full Cook direct oracle mismatch")
        if lpf[p] == p and (p+h)%M == 0:
            if (Dnext-2*D-delta)%Q or phi[p] != p-1:
                raise AssertionError("terminal prime cocycle mismatch")
            primes.append(p)
            A.append(D%Q)
            B.append(Dnext%Q)
            R.append(delta%Q)
            dp.append(delta)
        D = Dnext
    if len(primes) < 2:
        raise ValueError("fewer than two selected primes")
    va,vb,vr = (phase_variance_interval(v,L) for v in (A,B,R))
    dvar = rational_variance(dp)
    max_upper = max(va[1],vb[1])
    if vr[0] > 9*max_upper:
        raise AssertionError("phase pair L2 transfer contradicted")
    central = 8*(max(dp)-min(dp)) <= Q
    chord_lower = 36*dvar/Q**2 if central else Fraction()
    if chord_lower > vr[1]:
        raise AssertionError("terminal chord estimate contradicted")
    return dict(X=X,h=h,M=M,L=L,Q=Q,prime_count=len(primes),
                prime_variance=rational_variance(primes),delta_variance=dvar,
                A=va,B=vb,R=vr,central=central,chord_lower=chord_lower,
                max_variance_lower=max(va[0],vb[0],vr[0]/9,chord_lower/9),
                cofinal_irrationality="OPEN")
