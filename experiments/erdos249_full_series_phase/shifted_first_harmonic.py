"""Erdos #249 WP09-A: exact signed shift contrasts and Cook-harmonic witnesses.

Scientific proofs of the all-X statements are in SHIFTED_FIRST_HARMONIC_009A.md.
This computes finite exact integer certificates and hostile rational controls.
A finite computation cannot certify the conjectured 10-percent cancellation.
"""
from fractions import Fraction
from math import gcd, isqrt

from experiments.erdos249_full_series_phase.overlog_phase_separation import (
    totients, centered
)


def _is_prime(n: int) -> bool:
    return n >= 2 and all(n % k for k in range(2, isqrt(n) + 1))


def shift_modulus(
    h: int, *, max_product: int = 1_000_000
) -> tuple[int, Fraction, tuple[int, ...]]:
    """Find a modest fixed M coprime h with eta_M <=29/50.

    This evaluator limits M for memory/sieve practicality. Mathematical
    existence for *every* fixed h is proven by Euler's prime-harmonic
    divergence in the manuscript and is not subject to this code cap.
    """
    if h < 1 or max_product < 2:
        raise ValueError("positive shift and product cap>=2 required")
    M, eta, ps = 1, Fraction(1), []
    p = 2
    while eta > Fraction(29, 50):
        if _is_prime(p) and gcd(p, h) == 1:
            if M * p > max_product:
                raise ValueError("exact evaluator product cap exceeded")
            M *= p
            eta *= Fraction(p - 1, p)
            ps.append(p)
        p += 1
    if M < 2 or gcd(M, h) != 1 or eta > Fraction(29, 50):
        raise AssertionError("fixed CRT witness construction failed")
    return M, eta, tuple(ps)


def cook_minimal_depth(X: int, h: int) -> int:
    """Least L>=1 with 2^L >= 16(2X+h+L+2)."""
    if X < 64 or h < 1:
        raise ValueError("X>=64 and h>=1 required")
    L = 1
    while (1 << L) < 16 * (2 * X + h + L + 2):
        L += 1
    return L


def signed_shift_numerators(
    X: int, h: int, L: int, phi: list[int]
) -> tuple[int, ...]:
    """All Cook D_(h,N,L) for X<=N<=2X, with exact rolling recurrence."""
    if X < 1 or h < 1 or L < 1 or 2*X + L + h >= len(phi):
        raise ValueError("invalid shifted-phase source or indices")
    Q = 1 << L
    D = sum(
        (phi[X+h+j] - phi[X+j]) << (L-j)
        for j in range(1,L+1)
    )
    out = [D]
    for N in range(X,2*X):
        D = (
            2 * D
            - Q * (phi[N+h+1] - phi[N+1])
            + (phi[N+h+L+1] - phi[N+L+1])
        )
        out.append(D)
    return tuple(out)


def direct_shift_numerator(N:int,h:int,L:int,phi:list[int])->int:
    if N<1 or h<1 or L<1 or N+h+L>=len(phi):
        raise ValueError("invalid direct shifted phase")
    return sum(
        (phi[N+h+j]-phi[N+j]) << (L-j)
        for j in range(1,L+1)
    )


def signed_shift_receipt(X: int, h: int) -> dict[str, object]:
    """Finite exact signed contrast and phase implication, no float phases.

    Applies the effective local implication whenever X>=58h and
    h+L+1<=X, with M_h the first small-prime witness.
    """
    L = cook_minimal_depth(X,h)
    Q = 1 << L
    if X < 58*h or h+L+1>X:
        raise ValueError("X must meet explicit signed-contrast endpoint bounds")
    M, eta, ps = shift_modulus(h)
    phi = totients(2*X+L+h+1)
    D = signed_shift_numerators(X,h,L,phi)
    residues = tuple(centered(d,Q) for d in D)
    lower, upper = X+L+1, 2*X+L-1

    minus = tuple(
        n for n in range(lower,upper+1)
        if n%M == (-h)%M and 5*phi[n] >= 3*n
    )
    plus = tuple(
        n for n in range(lower,upper+1)
        if n%M==0 and 5*phi[n+h] >=3*(n+h)
    )
    if set(minus).intersection(plus):
        raise AssertionError("signed CRT classes overlap")
    strong = {
        N for N in range(X,2*X)
        if 300 * abs(residues[N-X]) >= X
    }
    for n in minus+plus:
        delta = phi[n+h]-phi[n]
        if n in minus and 100*delta > -X:
            raise AssertionError("negative shifted totient contrast missing")
        if n in plus and 50*delta < X:
            raise AssertionError("positive shifted totient contrast missing")
        N = n-L-1
        if N not in strong and N+1 not in strong:
            raise AssertionError("adjacent Cook-phase implication failed")
        z = residues[N-X+1]-2*residues[N-X]
        if (z-delta)%Q!=0:
            raise AssertionError("exact shifted numerator recurrence failure")
    if len(strong)*2 < len(minus)+len(plus):
        raise AssertionError("two-to-one starting-position count falsified")
    if Q <= 96*X:
        fixed_fraction = {
            N for N in range(X,2*X)
            if 28800 * abs(residues[N-X]) >= Q
        }
        if not strong.issubset(fixed_fraction):
            raise AssertionError("fixed fractional gap comparison failed")
    else:
        fixed_fraction = set()
    return {
        "X":X,"h":h,"L":L,"Q":Q,"M":M,
        "CRT_primes":ps,"eta_M":str(eta),
        "negative_endpoints":minus,
        "positive_endpoints":plus,
        "strong_gap_starts":len(strong),
        "fixed_fraction_gap_starts":len(fixed_fraction),
        "two_to_one_lower_bound":(len(minus)+len(plus)+1)//2,
        "required_fractional_gap": "1/28800 if Q<=96X",
        "analytic_asymptotic": "NOT_ATTESTED_BY_FINITE_TEST",
        "cook_required_10_percent_saving": "OPEN",
        "original_totient_irrationality":"OPEN",
    }


def rational_shift_control(n: int, h: int, modulus: int) -> int:
    """Fixed quasi-linear periodic rational control with both signed shifts."""
    if n<0 or h<1 or modulus<3 or gcd(h,modulus)!=1:
        raise ValueError("nonnegative n, positive h and coprime modulus>=3")
    r=n%modulus
    if r==(-h)%modulus or r==h%modulus:
        return n
    if r==0:
        return 0
    return n//2


def rational_shift_control_sum(h: int, modulus: int) -> Fraction:
    """Closed exact FULL sum of rational shifted-contrast control."""
    if h<1 or modulus<3 or gcd(h,modulus)!=1 or modulus>64:
        raise ValueError("positive shift, coprime 3<=modulus<=64 required")
    T=2*modulus
    x=Fraction(1,1<<T)
    total=Fraction(0)
    for r in range(1,T+1):
        cls=r%modulus
        if cls==(-h)%modulus or cls==h%modulus:
            A=Fraction(r)
            B=Fraction(T)
        elif cls==0:
            A=B=Fraction(0)
        else:
            A=Fraction(r//2)
            B=Fraction(T//2)
        total+=Fraction(1,1<<r)*(A/(1-x)+B*x/(1-x)**2)
    return total
