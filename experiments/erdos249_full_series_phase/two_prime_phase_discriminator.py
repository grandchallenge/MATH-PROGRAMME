"""ERDOS-249 WP09-G: rational hostile comparator and 2x3 Cook cocycle signature.

This file contains exact rational/integer source assertions and bounded
floating diagnostic observations. The theorem and their distinction are in
TWO_PRIME_COOK_PHASE_DISCRIMINATOR_009G.md.

NEITHER a real trigonometric smoke test NOR this source promotes the
open Cook 10% criterion, totient irrationality, or MATHCERT.
"""
from __future__ import annotations

from fractions import Fraction
from math import cos, pi, sin

from experiments.erdos249_full_series_phase.fourier_probe import totients
from experiments.erdos249_full_series_phase.full_window_prime_projection import (
    cook_minimal_depth,
    cook_numerators_rolling,
)
from experiments.erdos249_full_series_phase.conditional_cook_phase import (
    centered_representative,
)


def _positive(x: int, name: str) -> None:
    if type(x) is not int or x < 1:
        raise ValueError(f"{name} must be a positive ordinary integer")


def adversarial_rational_comparator(n: int) -> int:
    """ALL coefficients even, in [0,n]; full binary series exactly one.

    Odd n: n-1.
    Even n=2k: 2*b_k, with base-4 digits b_1=1 and subsequently
    (b_2,b_3,b_4,b_5,...)=(0,1,3,0,1,3,...).
    """
    _positive(n, "n")
    if n % 2:
        return n-1
    k = n//2
    return 2*(1 if k == 1 else {0: 1, 1: 3, 2: 0}[k % 3])


def exact_comparator_series() -> dict[str, Fraction]:
    """Geometrically evaluate TWO infinite subseries, as exact fractions."""
    # sum_{odd n>=1} (n-1)/2^n = 4/9.
    odd = Fraction(1, 4) / (1-Fraction(1, 4))**2
    # sum b_k/4^k = 1/4 + (1/64+3/256)/(1-1/64)=5/18.
    base4 = Fraction(1,4)+(Fraction(1,64)+Fraction(3,256))/(1-Fraction(1,64))
    even = 2*base4
    if odd != Fraction(4, 9) or even != Fraction(5, 9):
        raise AssertionError("comparator's exact geometric sums drifted")
    if odd + even != 1:
        raise AssertionError("hostile comparator must have binary sum exactly one")
    return {"odd": odd, "even": even, "total": odd + even}


def two_prime_certificate(X: int, L: int | None = None
                          ) -> dict[str, object]:
    """Exact integer finite-X eligibility for a genuine 2x3 phase signature.

    If eligible, proven for actual Euler totient:
        delta_full >= X^2/32
        delta_source >= X^2/64
        Im(sum cocycle on n=0 mod6 - sum on n=2 mod6)
          >= pi*X^2/(64*Q).
    The final bound has an explicit pi factor; the value returned as a
    Fraction is only its coefficient, NOT a trigonometric computation.
    """
    _positive(X, "X")
    if L is None:
        L = cook_minimal_depth(X, 1) + 1
    _positive(L, "L")
    h = 1
    s = L+1
    Q = 1 << L
    E = 3+(3*X).bit_length()
    source_gate = Q >= 16*(2*X+h+L+2)
    # s+1 <=X/8; check by integer cross-multiplication, no rounding.
    eligible = (X >= 1024*E and 8*(s+1) <= X and
                Q >= 64*X and source_gate)
    return {
        "X": X, "h": h, "L": L, "s": s, "Q": Q,
        "E": E,
        "cook_minimum_depth": cook_minimal_depth(X, 1),
        "size_gate_passed": source_gate,
        "required_min_X": 1024*E,
        "eligible": eligible,
        "full_source_two_prime_contrast_lower":
            Fraction(X*X,32) if eligible else None,
        "truncated_source_two_prime_contrast_lower":
            Fraction(X*X,64) if eligible else None,
        "imag_cocycle_contrast_lower_coefficient_of_pi":
            Fraction(X*X,64*Q) if eligible else None,
        "comparator_source_contrast_absolute_upper":
            8*X if eligible else None,
        "comparator_imag_cocycle_contrast_absolute_upper":
            3 if eligible else None,
        "cook_tenth_saving": "OPEN",
        "irrationality": "OPEN",
        "mathcert": "NOT_SUBMITTED",
    }


def source_delta(func, n: int) -> int:
    return func(n+1) - func(n)


def _classes(X: int, s: int, *, truncated: bool
             ) -> tuple[list[int], list[int]]:
    """Take terminal-index 0 and 2 (mod 6), map back to source N."""
    last = 2*X-1 if truncated else 2*X
    return (
        [N for N in range(X, last) if (N+s) % 6 == 0],
        [N for N in range(X, last) if (N+s) % 6 == 2],
    )


def actual_two_prime_replay(
    X: int, L: int | None = None, max_X: int = 150_000
) -> dict[str, object]:
    """Actual phi exact integer contrast; all-phase diagnostic optional.

    Full integer Cook D_N is computed using existing source-exact rolling
    recurrence. The analytic sine Taylor bound is established in the
    associated manuscript; calculated sine is merely an observation.
    """
    c = two_prime_certificate(X, L)
    if not c["eligible"]:
        raise ValueError("exact two-prime source/depth eligibility fails")
    if type(max_X) is not int or max_X < 1 or X > max_X:
        raise ValueError("finite host computation exceeds declared budget")
    s, Q, L = c["s"], c["Q"], c["L"]
    phi = totients(2*X+s+3)
    D = cook_numerators_rolling(phi, X, 1, L)
    cls0, cls2 = _classes(X, s, truncated=False)
    S0, S2 = _classes(X, s, truncated=True)
    f = phi.__getitem__
    full0 = sum(source_delta(f, N+s) for N in cls0)
    full2 = sum(source_delta(f, N+s) for N in cls2)
    src0 = sum(source_delta(f, N+s) for N in S0)
    src2 = sum(source_delta(f, N+s) for N in S2)
    full, trunc = full0-full2, src0-src2
    if 32*full < X*X:
        raise AssertionError("actual 2x3 full totient progression theorem fails")
    if 64*trunc < X*X:
        raise AssertionError("actual 2x3 source totient progression theorem fails")
    for N in S0+S2:
        i = N-X
        if (D[i+1]-2*D[i]-source_delta(f,N+s)) % Q:
            raise AssertionError("actual Cook modular cocycle mismatch")
    # Noncertifying evaluation, comparing to the *proved symbolic* lower.
    U = sum(sin(2*pi*source_delta(f,N+s)/Q) for N in S0)
    U -= sum(sin(2*pi*source_delta(f,N+s)/Q) for N in S2)
    if U < pi*float(c["imag_cocycle_contrast_lower_coefficient_of_pi"])-1e-8:
        raise AssertionError("finite observation disagrees with analytic bound")
    return {
        **c, "source_class_0_count": len(S0), "source_class_2_count": len(S2),
        "full_source_delta_0": full0, "full_source_delta_2": full2,
        "full_source_contrast": full, "truncated_source_contrast": trunc,
        "imag_cocycle_contrast_diagnostic": U,
        "actual_cook_exact_modular_recurrence": "PASS",
        "finite_integer_two_prime_contrast": "PASS",
    }


def rational_hostile_replay(X: int, L: int | None = None,
                            max_X: int = 150_000
                            ) -> dict[str, object]:
    """True rational comparator: all WP09-F h=1,p=2 source signs hold,
    yet EVERY real Cook phase > 9/10 on the source-admissible block.

    The latter is certified analytically via exact alpha=1 and an
    integer centered-residue/tail bound, NOT by floating cosine.
    """
    _positive(X, "X")
    if L is None:
        L = cook_minimal_depth(X, 1)
    _positive(L, "L")
    if X < 32 or L+2 > X or (1<<L) < 16*(2*X+L+3):
        raise ValueError("hostile source test requires Cook admissibility")
    if X > max_X:
        raise ValueError("comparator smoke exceeds declared budget")
    exact_comparator_series()
    Q=1<<L
    s=L+1
    a=adversarial_rational_comparator
    # Verify the exact WP09-F real signed source bounds, not a mere mean.
    out=[]
    for parity,sign in ((0,1),(1,-1)):
        full=[N for N in range(X,2*X) if (N+s)%2==parity]
        src=[N for N in range(X,2*X-1) if (N+s)%2==parity]
        b_full=sum(source_delta(a,N+s) for N in full)
        b_src=sum(source_delta(a,N+s) for N in src)
        energy=sum(source_delta(a,N+s)**2 for N in src)
        if 8*sign*b_full<X*X or 16*sign*b_src<X*X or 256*energy<X**3:
            raise AssertionError("hostile comparator fails WP09-F source bounds")
        out.append({"terminal_parity":parity, "sign":sign,
                    "full_source_signed_sum":b_full,
                    "truncated_source_signed_sum":b_src,
                    "source_square_energy":energy})
    Ds = tuple(
        sum((1<<(L-j))*source_delta(a,N+j) for j in range(1,L+1))
        for N in range(X,2*X)
    )
    for i,D in enumerate(Ds):
        N=X+i
        r=centered_representative(D,Q)
        # Because the INFINITE shifted signed dyadic sum is integral,
        # |r|<=sum_{j>L}(N+j+1)/2^j * Q = N+L+3.
        if abs(r) > N+L+3:
            raise AssertionError("binary rational series integer-tail obstruction fails")
        if 16*abs(r)>=Q:
            raise AssertionError("Cook admissibility must keep every phase < 1/16")
        if i+1<len(Ds) and (Ds[i+1]-2*D-source_delta(a,N+L+1))%Q:
            raise AssertionError("hostile complete Cook cocycle mismatch")
    real_average = sum(cos(2*pi*centered_representative(D,Q)/Q)
                       for D in Ds)/X
    if real_average <= .9:
        raise AssertionError("rational comparator must refute 10% saving")
    return {
        "X":X,"h":1,"L":L,"Q":Q,"binary_sum_exact":Fraction(1),
        "source_signed":tuple(out),
        "every_phase_within_one_sixteenth":"PROVED_EXACT_INTEGER_TAIL",
        "universal_real_lower": "cos(pi/8)>9/10",
        "observed_real_average_diagnostic":real_average,
        "cook_tenth_saving_for_comparator":"FAILS_AT_EVERY_ADMISSIBLE_BLOCK",
    }


def two_prime_hostile_comparison(X: int, L: int | None = None
                                 ) -> dict[str, object]:
    """At 2x3, true totient has Omega(X) imaginary cocycle contrast,
    but the rational parity mimic has uniformly |contrast| < 3.
    """
    v=actual_two_prime_replay(X,L)
    Q,s=v["Q"],v["s"]
    a=adversarial_rational_comparator
    C0,C2=_classes(X,s,truncated=False)
    S0,S2=_classes(X,s,truncated=True)
    comp_full=sum(source_delta(a,N+s) for N in C0)-sum(
        source_delta(a,N+s) for N in C2)
    if abs(comp_full)>8*X:
        raise AssertionError("comparator source classes not uniformly close")
    U=sum(sin(2*pi*source_delta(a,N+s)/Q) for N in S0)-sum(
        sin(2*pi*source_delta(a,N+s)/Q) for N in S2)
    if abs(U)>=3:
        raise AssertionError("comparator bounded 2x3 Fourier contrast fails")
    return {**v, "comparator_full_source_contrast":comp_full,
            "comparator_imag_cocycle_contrast_diagnostic":U,
            "comparator_imag_cocycle_universal_abs_bound":3}
