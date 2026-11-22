"""WP09-F: genuine fixed-prime conditional modulo-one Cook phase bounds.

Exact integer source/verification for CONDITIONAL_COOK_PHASE_009F.md.
Conclusions apply only after explicit arithmetic, depth and support gates.
The analytic chord inequality in the manuscript converts exact centered-
residue energy into a real exponential-sum bound; numerical cosine is not
used as a proof. Original Erdős #249 and 10% first harmonic remain OPEN.
"""
from __future__ import annotations

from fractions import Fraction
from math import isqrt

from experiments.erdos249_full_series_phase.fourier_probe import totients
from experiments.erdos249_full_series_phase.full_window_prime_projection import (
    cook_minimal_depth,
    cook_numerator_direct,
    cook_numerators_rolling,
    fixed_separating_prime,
)


def _positive(x: int, name: str) -> None:
    if type(x) is not int or x < 1:
        raise ValueError(f"{name} must be a positive integer")


def _prime_nondivisor(p: int, h: int) -> None:
    if (type(p) is not int or p < 2 or h % p == 0 or
            any(p % d == 0 for d in range(2, isqrt(p) + 1))):
        raise ValueError("p must be a prime not dividing h")


def centered_representative(D: int, Q: int) -> int:
    """Centered least-absolute integer mod the even Q=2^L."""
    if type(D) is not int or type(Q) is not int or Q < 2 or Q % 2:
        raise ValueError("integer D and positive even Q required")
    return (D + Q // 2) % Q - Q // 2


def conditional_certificate(
    X: int, h: int, L: int | None = None, p: int | None = None
) -> dict[str, object]:
    """Exact applicability and rigorous *analytic* lower-bound constants.

    For each r_+=-(L+1), r_- =-(L+1)-h modulo p, if eligible:
      |S_r| - Re sum_{S_r} E_(N+1) conjugate(E_N)^2
       >= X**3/(4*p**3*Q**2),
      |T_r| - Re sum_{T_r} E_N >= X**3/(20*p**3*Q**2).
    A class a in {r,r+1} has conditional average deficit >=
    X**2/(80*p**2*Q**2). This "exists" is not identified beforehand.

    Absolute fraction savings at source-locked *least* Cook depth apply
    only when L>h, H<=X, and 32X < Q <96X.
    """
    _positive(X, "X")
    _positive(h, "h")
    if L is None:
        L = cook_minimal_depth(X, h)
    _positive(L, "L")
    if p is None:
        p = fixed_separating_prime(h)
    _prime_nondivisor(p, h)
    Q = 1 << L
    s = L + 1
    H = s + h
    E = 3 + (3*X).bit_length()
    min_X = 40*p*p*max(E, h+4)
    is_cook_depth = L >= h and Q >= 16*(2*X+h+L+2)
    eligible = H <= X and X >= min_X and is_cook_depth
    least_depth = L == cook_minimal_depth(X, h)
    absolute_eligible = eligible and least_depth and L > h and Q < 96*X
    return {
        "X": X, "h": h, "L": L, "s": s, "p": p, "Q": Q,
        "H": H, "E": E, "min_X": min_X,
        "prime_positive_class": (-s) % p,
        "prime_negative_class": (-s-h) % p,
        "distinct_prime_classes": ((-s) % p != (-s-h) % p),
        "cook_depth_admissible": is_cook_depth,
        "least_cook_depth": least_depth,
        "eligible": eligible,
        "least_depth_absolute_eligible": absolute_eligible,
        "signed_full_first_moment_magnitude_lower":
            Fraction(X*X, 2*p*p) if eligible else None,
        "signed_truncated_first_moment_magnitude_lower":
            Fraction(X*X, 4*p*p) if eligible else None,
        "source_square_energy_lower":
            Fraction(X**3, 32*p**3) if eligible else None,
        "cocycle_real_deficit_lower":
            Fraction(X**3, 4*p**3*Q**2) if eligible else None,
        "pair_original_cook_real_deficit_lower":
            Fraction(X**3, 20*p**3*Q**2) if eligible else None,
        "exists_single_original_class_average_gap_lower":
            Fraction(X*X, 80*p*p*Q*Q) if eligible else None,
        "least_depth_cocycle_relative_gap":
            Fraction(1, 73728*p*p) if absolute_eligible else None,
        "least_depth_pair_block_deficit":
            Fraction(X, 184320*p**3) if absolute_eligible else None,
        "least_depth_exists_class_relative_gap":
            Fraction(1, 737280*p*p) if absolute_eligible else None,
        "cook_full_global_tenth_saving_proved": False,
        "original_irrationality": "OPEN",
        "mathcert": "NOT_SUBMITTED",
    }


def source_integer_delta(phi: list[int], N: int, h: int, s: int) -> int:
    return phi[N+s+h] - phi[N+s]


def exact_conditional_replay(
    X: int, h: int, L: int | None = None, p: int | None = None,
    max_X: int = 100_000,
) -> dict[str, object]:
    """Independent integer hostile check of the actual modular Cook source.

    Checks BOTH signed arithmetic progression lower bounds, both source
    squared-energy bounds, exact D recurrence modulo Q and exact centered
    phase L2 operator inequality. No floating or cos in assertions.
    """
    cert = conditional_certificate(X, h, L, p)
    if type(max_X) is not int or max_X < 1 or X > max_X:
        raise ValueError("finite replay exceeds declared smoke-test cap")
    if not cert["eligible"]:
        raise ValueError("explicit arithmetic or Cook depth theorem gate failed")
    s, Q, p, L = cert["s"], cert["Q"], cert["p"], cert["L"]
    phi = totients(2*X+s+h+2)
    Ds = cook_numerators_rolling(phi, X, h, L)
    if len(Ds) != X:
        raise AssertionError("actual complete Cook numerator length mismatch")
    for i in (0, X//2, X-1):
        if Ds[i] != cook_numerator_direct(phi, X+i, h, L):
            raise AssertionError("direct original Cook numerator mismatch")
    centered = tuple(centered_representative(D, Q) for D in Ds)
    delta = tuple(source_integer_delta(phi, X+i, h, s)
                  for i in range(X))
    for i in range(X-1):
        if (Ds[i+1] - 2*Ds[i] - delta[i]) % Q != 0:
            raise AssertionError("exact full Cook cocycle failed")
        if 2*abs(delta[i]) >= Q:
            raise AssertionError("local shifted difference escaped half modulus")
    reports: list[dict[str, object]] = []
    for label, r in (("positive", cert["prime_positive_class"]),
                     ("negative", cert["prime_negative_class"])):
        full = [i for i in range(X) if (X+i) % p == r]
        source = [i for i in range(X-1) if (X+i) % p == r]
        pair_classes = {r, (r+1) % p}
        pair = [i for i in range(X) if (X+i) % p in pair_classes]
        total_full = sum(delta[i] for i in full)
        total_source = sum(delta[i] for i in source)
        d2 = sum(delta[i]**2 for i in source)
        centered2 = sum(centered[i]**2 for i in pair)
        sign = 1 if label == "positive" else -1
        if 2*p*p*sign*total_full < X*X:
            raise AssertionError("fixed-prime weighted source mean violation")
        if 4*p*p*sign*total_source < X*X:
            raise AssertionError("endpoint-truncated source mean violation")
        if 32*p**3*d2 < X**3:
            raise AssertionError("conditional actual squared-energy violation")
        if 5*centered2 < d2:
            raise AssertionError("centered modulo-one transfer operator failed")
        if 160*p**3*centered2 < X**3:
            raise AssertionError("rigorous modulo-one cosine lower envelope failed")
        # Weighted Cauchy–Schwarz, endpoint class and single class size.
        if len(source)*d2 < total_source**2:
            raise AssertionError("exact restricted Cauchy Schwarz failed")
        if len(full) > 2*X//p + 1 or len(pair) > X:
            raise AssertionError("invalid arithmetic progression count")
        reports.append({
            "sign": label, "source_class": r,
            "neighbor_class": (r+1) % p,
            "full_signed_delta_sum": total_full,
            "source_signed_delta_sum": total_source,
            "source_count": len(source),
            "pair_count": len(pair),
            "source_delta_squared": d2,
            "pair_centered_residue_squared": centered2,
            "exact_cocycle_and_phase_transfer_pass": True,
        })
    return {
        **cert,
        "direct_cook_oracle_checked_at": (X, X+X//2, 2*X-1),
        "reports": tuple(reports),
        "phase_representatives_all_centered": True,
        "exact_integer_replay": "PASS",
    }
