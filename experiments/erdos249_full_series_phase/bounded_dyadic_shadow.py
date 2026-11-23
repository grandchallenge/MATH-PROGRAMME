"""Erdos #249 WP09-H: bounded dyadic-rational shadow and cocycle-scale no-go.

A constructive exact coefficient oracle is supplied for finite prefixes.
The all-n construction is given by a base-four floor expansion of the
positive arithmetic tail; the proof is in BOUNDED_DYADIC_SHADOW_009H.md.

This is a theorem about INSUFFICIENCY of normalized prime/cocycle evidence.
It neither asserts that the true binary totient series is rational nor
proves irrationality or Cook's tenth-saving.
"""
from __future__ import annotations

from fractions import Fraction
from math import cos, pi

from experiments.erdos249_full_series_phase.fourier_probe import totients
from experiments.erdos249_full_series_phase.full_window_prime_projection import (
    cook_minimal_depth, cook_numerator_direct,
)
from experiments.erdos249_full_series_phase.conditional_cook_phase import (
    centered_representative,
)
from experiments.erdos249_full_series_phase.two_prime_phase_discriminator import (
    two_prime_certificate,
)


def _positive(x: int, name: str) -> None:
    if type(x) is not int or x < 1:
        raise ValueError(f"{name} must be a positive ordinary integer")


def dyadic_target(K: int) -> dict[str, object]:
    """EXACT explicit dyadic target beta_K for the real totient series.

    beta_K = sum_(n<=3K) phi(n)/2^n + (3K+2)/2^(3K).
    delta = beta_K-alpha >0, and 0<delta/(2*4**(-K))<1 at K>=6.
    The value alpha/delta is not evaluated or claimed rational.
    """
    _positive(K, "K")
    if K < 6:
        raise ValueError("K>=6 is required for source-positive digit capacity")
    M = 3*K
    phi = totients(M)
    numerator = sum(phi[n] << (M-n) for n in range(1,M+1)) + M+2
    target = Fraction(numerator, 1 << M)
    capacity = Fraction(2, 4**K)
    delta_upper = Fraction(M+2, 1<<M)
    if not delta_upper < capacity:
        raise AssertionError("tail increment exceeds available even-digit capacity")
    return {
        "K": K, "M": M, "dyadic_target": target,
        "dyadic_denominator": 1<<M,
        "increasing_even_digit_capacity": capacity,
        "positive_delta_upper": delta_upper,
        "shadow_uniform_coefficient_gap_upper": 6,
        "real_series_value_of_true_totient": "UNDETERMINED",
        "Cook_tenth_saving_for_true_totient": "OPEN",
        "mathcert": "NOT_SUBMITTED",
    }


def certified_base4_prefix(
    K: int, J: int, margin_bits: int = 48, max_expansions: int = 4,
) -> dict[str, object]:
    """Certify floor(4^J*x) by an exact interval, no unknown-alpha oracle.

    x = 2^(2K-1) sum_(n>3K) (n-phi(n))/2^n in (0,1).
    First J digits are certified iff both integer interval endpoints
    have the same floor; ambiguity is explicitly rejected.

    The arithmetic tail bound is sum_(n>T)n/2^n=(T+2)/2^T.
    If x lies exactly on a base-four boundary, the finite oracle may
    remain ambiguous even though the mathematical base-four floor
    expansion is always well-defined.
    """
    c = dyadic_target(K)
    _positive(J,"J")
    _positive(margin_bits,"margin_bits")
    _positive(max_expansions,"max_expansions")
    M = c["M"]
    for extra in range(max_expansions):
        T = max(M+1, 2*J+2*K+margin_bits+32*extra)
        phi = totients(T)
        numerator = sum((n-phi[n]) << (T-n) for n in range(M+1, T+1))
        shift = T-(2*J+2*K-1)
        if shift < 1:
            raise AssertionError("positive certified interval shift missing")
        lo = numerator >> shift
        hi = (numerator+T+2) >> shift
        if lo == hi:
            if not (0 <= lo < (1 << (2*J))):
                raise AssertionError("dyadic shadow's base-four digits out of range")
            digits = tuple((lo >> (2*(J-j))) & 3 for j in range(1,J+1))
            if sum(d << (2*(J-j)) for j,d in enumerate(digits,start=1))!=lo:
                raise AssertionError("base-four floor reconstruction failed")
            return {
                "K":K,"J":J,"T":T,
                "base4_integer_prefix":lo,
                "digits":digits,
                "tail_scaled_interval_upper_numerator":numerator+T+2,
                "tail_scaled_interval_lower_numerator":numerator,
                "tail_interval_denominator":1 << shift,
                "exact_prefix_certified":True,
            }
    raise ValueError("arithmetic-tail interval crosses a base-four digit boundary")


def shadow_coefficients(limit: int, K: int, max_limit: int = 12000
                        ) -> dict[str, object]:
    """Compute an exactly certified finite prefix of the dyadic rational shadow.

    The constructed infinite a_K agrees with phi up to 2K and at all odd
    indices; on even index n=2(K+j), add 2*d_j, d_j the j-th digit of x.
    """
    _positive(limit,"limit")
    c=dyadic_target(K)
    _positive(max_limit,"max_limit")
    if limit > max_limit:
        raise ValueError("finite exact shadow prefix exceeds smoke-test cap")
    phi = totients(max(limit,c["M"]))
    a=list(phi[:limit+1])
    J=max(0,limit//2-K)
    prefix=certified_base4_prefix(K,J) if J else None
    if J:
        digits=prefix["digits"]
        for j,d in enumerate(digits,start=1):
            n=2*(K+j)
            if n <= limit:
                a[n]+=2*d
    for n in range(1,limit+1):
        if not (0<=a[n]<=n and 0<=a[n]-phi[n]<=6):
            raise AssertionError("actual totient shadow coefficient envelope drifted")
        if n>=3 and a[n]%2:
            raise AssertionError("actual totient shadow parity drifted")
        if n<=2*K and a[n]!=phi[n]:
            raise AssertionError("shadow must agree on arbitrarily long prefix")
        if n%2 and a[n]!=phi[n]:
            raise AssertionError("shadow must preserve all odd coefficients exactly")
    return {
        "K":K,"limit":limit,"J":J,"target":c["dyadic_target"],
        "coefficients":tuple(a),"original_totients":tuple(phi[:limit+1]),
        "prefix":prefix,
        "bounded_difference_verified":True,
    }


def shadow_cook_replay(X:int, h:int, K:int=8, L:int|None=None,
                       max_X:int=2000) -> dict[str, object]:
    """Exact finite original Cook phases of an actual-phi bounded shadow.

    An integer-tail argument, NOT finite cosines, proves that for
    ALL sufficiently late Cook-admissible blocks, every phase is >0.9.
    """
    _positive(X,"X")
    _positive(h,"h")
    if L is None:
        L=cook_minimal_depth(X,h)
    _positive(L,"L")
    Q=1<<L
    target=dyadic_target(K)
    if X < target["M"] or Q <16*(2*X+h+L+2):
        raise ValueError("the dyadic tail and Cook source gates are both required")
    if X > max_X:
        raise ValueError("bounded exact replay budget exceeded")
    last=2*X+h+L+2
    values=shadow_coefficients(last,K,max_limit=2*max_X+h+L+4)
    a,phi=values["coefficients"],values["original_totients"]
    d=lambda n:a[n+h]-a[n]
    original_d=lambda n:phi[n+h]-phi[n]
    D=cook_numerator_direct(a,X,h,L)
    centered_energy=0
    actual_oracle_count=0
    for i in range(X):
        N=X+i
        r=centered_representative(D,Q)
        centered_energy+=r*r
        if abs(r)>N+h+L+2 or 16*abs(r)>=Q:
            raise AssertionError("dyadic denominator failed Cook integer-tail bound")
        if abs(d(N+L+1)-original_d(N+L+1))>6:
            raise AssertionError("six-unit source perturbation budget exceeded")
        if i in (0,X//2,X-1):
            if D!=cook_numerator_direct(a,N,h,L):
                raise AssertionError("true full shadow Cook rolling/direct disagreement")
            actual_oracle_count+=1
        if i < X-1:
            nxt=2*D-Q*d(N+1)+d(N+L+1)
            if (nxt-2*D-d(N+L+1))%Q:
                raise AssertionError("exact full phase cocycle mismatch")
            D=nxt
    nmax=last
    prefix_mass=sum((a[n] << (nmax-n) for n in range(1,nmax+1)),0)
    beta=target["dyadic_target"]
    lower=Fraction(prefix_mass,1<<nmax)
    upper=lower+Fraction(nmax+2,1<<nmax)
    if not (lower <= beta <= upper):
        raise AssertionError("explicit exact dyadic target outside coefficient envelope")
    return {
        "X":X,"h":h,"K":K,"L":L,"Q":Q,"M":target["M"],
        "dyadic_target":beta,
        "max_shadow_coefficient_delta":6,
        "direct_oracle_points":actual_oracle_count,
        "centered_phase_integer_energy":centered_energy,
        "every_full_Cook_phase_within_1_over_16":True,
        "every_Cook_real_part_strictly_above_9_over_10":True,
        "binary_series_exact_target":"DYADIC_RATIONAL_BY_PROOF",
        "source_scope":"actual phi plus certified <=6 even-index perturbations",
        "Cook_tenth_saving_for_original_totient":"OPEN",
    }


def multistep_stability_certificate(
    X:int,K:int=8,L:int|None=None,step:int=1,
) -> dict[str, object]:
    """Pure exact rational stability bound for k-step complete cocycles.

    Each original/genuine shadow k-step Cook cocycle differs by at most
    12*pi*(2^k-1)/Q in complex modulus. Returned coefficient is
    the exact rational multiplier OF pi, not a floating certification.
    For an arbitrary selection of at most X indices, the sum differs by
    <= 12*pi*X*(2^k-1)/Q.
    """
    _positive(X,"X")
    dyadic_target(K)
    if L is None:
        L=cook_minimal_depth(X,1)+1
    _positive(L,"L")
    _positive(step,"step")
    Q=1<<L
    if X<3*K or 16*(2*X+L+3)>Q:
        raise ValueError("source dyadic tail and Cook admissibility required")
    return {
        "X":X,"K":K,"L":L,"Q":Q,"k":step,
        "single_cocycle_distance_coefficient_of_pi":
            Fraction(12*((1<<step)-1),Q),
        "at_most_X_cocycle_sum_distance_coefficient_of_pi":
            Fraction(12*X*((1<<step)-1),Q),
        "normalized_mean_distance_coefficient_of_pi":
            Fraction(12*((1<<step)-1),Q),
        "real_original_Cook_harmonic_transfer":"NOT_JUSTIFIED",
    }


def two_prime_shadow_certificate(X:int,K:int=8,
                                 L:int|None=None) -> dict[str,object]:
    """The *rational* shadow reproduces WP09-G actual 2x3 Fourier signal.

    Under WP09-G eligibility, with U_phi>=pi*X^2/(64Q),
    U_shadow>=pi*X*(X-768)/(64Q)>=pi*X^2/(128Q).
    At L=L_1(X)+1 and sufficiently large X, Q<256X and
    hence U_shadow >=pi*X/32768, although all its original Cook
    real phases >cos(pi/8)>0.9.
    """
    dyadic_target(K)
    c=two_prime_certificate(X,L)
    if not c["eligible"] or X<3*K or X<1536:
        raise ValueError("actual totient 2x3 source and shadow tail gates missing")
    Q=c["Q"]
    return {
        "X":X,"K":K,"L":c["L"],"Q":Q,
        "true_phi_source_imag_contrast_lower_coefficient_of_pi":
            Fraction(X*X,64*Q),
        "shadow_vs_true_imag_difference_upper_coefficient_of_pi":
            Fraction(12*X,Q),
        "rational_shadow_imag_contrast_lower_coefficient_of_pi":
            Fraction(X*X,128*Q),
        "cofinal_linear_shadow_gap_coefficient_of_pi":
            Fraction(X,32768) if (c["L"] == c["cook_minimum_depth"]+1 and Q < 256*X) else None,
        "rational_shadow_original_phase_everywhere_above_9_over_10":True,
        "original_totient_10_percent_saving":"OPEN",
    }
