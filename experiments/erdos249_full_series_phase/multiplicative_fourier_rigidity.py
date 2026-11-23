"""Erdos #249 WP09-J: positive-density multiplicative Fourier separation.

A theorem about a NEW arithmetic bilinear/multiplicative-defect character,
not Cook's ORIGINAL overlapping full-totient phase. It proves an effective
positive-density Fourier distinction between true phi and EVERY nontrivial
bounded even-parity two-unit shadow. In particular it applies to WP09-I's
EXACT dyadic-rational shadow.

The asymptotic math is in MULTIPLICATIVE_FOURIER_RIGIDITY_009J.md.
This source checks finite integers and offers explicitly NONCERTIFYING
floating cosine diagnostics. It never claims Cook 10% or irrationality.
"""
from __future__ import annotations

from fractions import Fraction
from math import cos, pi

from experiments.erdos249_full_series_phase.fourier_probe import totients
from experiments.erdos249_full_series_phase.full_window_prime_projection import (
    cook_minimal_depth,
)
from experiments.erdos249_full_series_phase.two_unit_parity_shadow import (
    two_unit_target,
    certified_binary_prefix,
)


def _positive(x: int, name: str) -> None:
    if type(x) is not int or x < 1:
        raise ValueError(f"{name} must be a positive ordinary integer")


def first_modified_twounit_8() -> dict[str, object]:
    """Exact FOUR-totient certificate: WP09-I K=8 first correction at n=21.

    delta_8 = sum_{n>24} phi(n)/2^n.
    2^20 * sum_{25<=n<=28} phi(n)/2^n = 1.
    2^20 * sum_{n>28} n/2^n = 30/256 = 15/128.
    Thus 1 <= 2^13*x_8 <= 143/128 <2, x_8=2^7 delta_8.
    Floor bits b_1..b_12 are zero and b_13 is one;
    phi(21)=12, a_8(21)=10.
    """
    phi = totients(28)
    terms = tuple(phi[n] for n in range(25, 29))
    if terms != (20, 12, 18, 12):
        raise AssertionError("actual totient source at 25..28 changed")
    lower = Fraction(sum(phi[n] << (28-n) for n in range(25, 29)), 1 << 8)
    upper = lower + Fraction(30, 1 << 8)
    if not (lower == 1 and upper == Fraction(143, 128) and upper < 2):
        raise AssertionError("exact first-modified digit tail bound invalid")
    p = certified_binary_prefix(8, 13)
    if p["digits"] != (0,) * 12 + (1,):
        raise AssertionError("independent exact binary-prefix oracle disagrees")
    if phi[21] != 12:
        raise AssertionError("phi21 expected 12")
    return {
        "K": 8, "last_dyadic_prefix_index": 24,
        "first_modified_index": 21,
        "phi_first_modified": phi[21],
        "shadow_first_modified": phi[21]-2,
        "scaled_tail_lower": lower,
        "scaled_tail_upper": upper,
        "first_13_binary_digits": p["digits"],
        "gamma_8": two_unit_target(8)["gamma"],
        "entire_shadow_dyadic_rational": "PROVED_IN_WP09_I",
        "true_phi_irrationality": "OPEN",
    }


def fourier_rigidity_certificate(n: int, P: int) -> dict[str, object]:
    """Exact integer gate and symbolic rational Fourier lower bounds.

    Universal hypotheses on an integer coefficient sequence b:
      0 <= b(j) <= j; b(j)-phi(j) is even;
      |b(j)-phi(j)| <= 2 for every j >= 1;
      b(n) != phi(n), n >= 3.
    At n, this forces |eta(n)|=2.

    R={m in [P,2P): m == 1 mod n}; Q=2^L,
    L is the *least* Cook-admissible h=1 depth for X=nP.

    For at least P/(5n) elements m of R, phi(m)>=m/3.
    Their multiplicative defects have |Delta| in [m/2,3m],
    and chord 1-cos(2*pi*Delta/Q)>=1/(4608*n^2).
    Therefore sum_R (1-cos(...))>=P/(23040*n^3),
    and the normalized real Fourier gap >=1/(24000*n^2).

    These are theorems from the manuscript, not sampled in this function.
    """
    _positive(n, "n")
    _positive(P, "P")
    if n < 3:
        raise ValueError("nontrivial parity-compatible perturbation requires n>=3")
    X=n*P
    L=cook_minimal_depth(X, 1)
    Q=1<<L
    E=3+(2*P).bit_length()
    gate=(P>=32*n*E and P>=32*(n+3) and
          L+2<=X and Q>=16*(2*X+L+3) and
          Q<96*X)
    return {
        "n":n,"P":P,"X":X,"L":L,"Q":Q,
        "E":E,
        "P_min_crt":32*n*E,
        "P_min_defect":32*(n+3),
        "legal_cook_size":Q>=16*(2*X+L+3),
        "eligible":gate,
        "source_progression_count_lower":Fraction(P,n)-1 if gate else None,
        "good_phi_ratio_min":Fraction(1,3) if gate else None,
        "good_multipliers_count_lower":Fraction(P,5*n) if gate else None,
        "pointwise_defect_abs_lower_fraction_of_m":Fraction(1,2) if gate else None,
        "pointwise_defect_abs_upper_fraction_of_m":Fraction(3) if gate else None,
        "pointwise_fourier_real_gap_lower":
            Fraction(1,4608*n*n) if gate else None,
        "full_progression_real_gap_lower":
            Fraction(P,23040*n**3) if gate else None,
        "normalized_progression_real_gap_lower":
            Fraction(1,24000*n*n) if gate else None,
        "original_Cook_full_phase_bound": "OPEN",
        "source_locked_weighted_prime_cofactor_correlation": "OPEN",
        "erdos_249_irrationality": "OPEN",
        "mathcert": "NOT_SUBMITTED",
    }


def universal_defect_interval(n: int, m: int, phi_m: int) -> tuple[int, int]:
    """Exact envelope for EVERY admissible two-unit parity correction.

    Delta=b(n*m)-b(n)*b(m)
         =eta(n*m)-eta(n)*phi(m)-b(n)*eta(m).
    At modified n, |eta(n)|=2; |eta(any)|<=2; 0<=b(n)<=n.
    Therefore 2*phi(m)-2*(n+1) <= |Delta| <= 2*phi(m)+2*(n+1)
    whenever the lower bound is positive. The signs of eta are arbitrary.
    """
    for name, v in (("n",n),("m",m),("phi_m",phi_m)):
        _positive(v,name)
    if n < 3 or phi_m>m:
        raise ValueError("defect envelope source arguments invalid")
    return (2*phi_m-2*(n+1), 2*phi_m+2*(n+1))


def finite_fourier_rigidity_replay(
    n:int=21, P:int=20000, *, max_P:int=150000
) -> dict[str, object]:
    """Independent finite totient sieve and exact-integer hostile bound check.

    Demonstrate universal defect envelope WITHOUT evaluating huge-index
    shadow digit eta(n*m). A deliberately one-flip comparator b agrees
    with phi except b(n)=phi(n)-2; it has Delta=2*phi(m) on R for m>>n.
    This one-flip comparison is NOT asserted to have rational series.
    """
    c=fourier_rigidity_certificate(n,P)
    if not c["eligible"]:
        raise ValueError("effective Fourier density/size gates fail")
    _positive(max_P,"max_P")
    if P>max_P:
        raise ValueError("bounded sieve budget exceeded")
    if n==21:
        first_modified_twounit_8()
    phi=totients(2*P)
    R=[m for m in range(P,2*P) if m % n==1]
    good=[m for m in R if 3*phi[m]>=m]
    count=len(R)
    if count* n < P-n:
        raise AssertionError("progression count floor identity failed")
    if 5*n*len(good)<P:
        raise AssertionError("effective positive-density source lemma failed")
    for m in good:
        lower,upper=universal_defect_interval(n,m,phi[m])
        if lower*2<m or upper>3*m:
            raise AssertionError("two-unit universal defect failed high-bit bounds")
        if upper*2>c["Q"]:
            raise AssertionError("defect phase is not inside short unit-circle arc")
        if 192*n*lower<c["Q"]:
            raise AssertionError("universal defect arc lower bound failed")
    # For deliberately one-flip b(n)=phi(n)-2, other coefficients unchanged,
    # the multiplicative defect at nm equals +2*phi(m). Sum cosines is
    # finite DIAGNOSTIC ONLY, unrelated to analytic all-P proof.
    diagnostic_gap=sum(1-cos(2*pi*(2*phi[m])/c["Q"]) for m in R)
    if diagnostic_gap < float(c["full_progression_real_gap_lower"])-1e-9:
        raise AssertionError("one-flip finite diagnostic contradicts theorem")
    return {
        **c,
        "actual_progression_count":count,
        "actual_good_multipliers_count":len(good),
        "all_good_exact_defect_envelopes":"PASS",
        "one_flip_comparator_defect_delta":"2*phi(m)",
        "one_flip_diagnostic_real_sum_gap":diagnostic_gap,
        "one_flip_diagnostic_normalized_gap":diagnostic_gap/count,
        "actual_phi_multiplicativity_defect":"ZERO_FOR_ALL_COPRIME",
        "bound_holds_for_WP09I_dyadic_rational_shadow":
            (n==21),
        "direct_WP09I_huge_index_digits_evaluated":False,
    }
