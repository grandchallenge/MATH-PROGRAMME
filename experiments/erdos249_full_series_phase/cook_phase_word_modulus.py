"""ERDOS-249 WP09-K: genuine Cook-phase word and quantitative modulus separation.

A *long*, completely exact word in the ORIGINAL complete h=1 Cook
phases equals the high-frequency character of coprime multiplicative
defect differences. An effective two-subinterval divisor-ratio argument
gives a positive Fourier MODULUS deficit for EVERY nontrivial parity-
preserving two-unit perturbation of the true Euler totient.

It does NOT prove the original Cook one-point 10%-saving, any weighted
cofactor estimate, or irrationality of the binary totient series.
"""
from __future__ import annotations

from fractions import Fraction
from math import cos, gcd, lcm, pi, sin

from experiments.erdos249_full_series_phase.fourier_probe import totients
from experiments.erdos249_full_series_phase.full_window_prime_projection import (
    cook_minimal_depth, cook_numerator_direct,
)
from experiments.erdos249_full_series_phase.multiplicative_fourier_rigidity import (
    first_modified_twounit_8,
)


def _positive(x: int, name: str) -> None:
    if type(x) is not int or x < 1:
        raise ValueError(f"{name} must be a positive ordinary integer")


def cook_word_modulus_certificate(n: int, P: int) -> dict[str, object]:
    """All-perturbation, effective *modulus* saving, exactly rationals.

    The real Fourier gap in WP09-J does not imply a modulus gap.
    Here two positive-density, ordered multiplier ranges enforce a
    phase separation of at least 1/(72*n) in complex chord distance,
    hence a normalized modulus gap of at least 1/(165888000*n*n).

    This character transfers to a LONG original Cook-phase word.
    NEVER infer cancellation of individual E_N from that long word.
    """
    _positive(n, "n")
    _positive(P, "P")
    if n < 3:
        raise ValueError("n>=3 is needed for a nontrivial parity-preserving correction")
    q = lcm(n, 2)
    E = 3 + (2*P).bit_length()
    X = n*P
    L = cook_minimal_depth(X, 1)
    Q = 1 << L
    permitted = (
        P % 10 == 0
        and P >= 1000*q*E
        and P >= 100*(n+1)
        and P >= L+3
        and L+2 <= X
        and Q >= 16*(2*X+L+3)
        and 32*X < Q < 96*X
    )
    return {
        "n":n,"P":P,"q":q,"E":E,"X":X,"L":L,"Q":Q,
        "gate_P_divisible_by_ten":P%10==0,
        "gate_P_min_CRT":1000*q*E,
        "gate_P_min_defect":100*(n+1),
        "legal_h1_Cook_modulus":Q>=16*(2*X+L+3),
        "eligible":permitted,
        "low_range":"[P,11P/10) intersect {m=1 mod q}",
        "high_range":"[19P/10,2P) intersect {m=1 mod q; phi(m)/m>=7/10}",
        "low_count_lower":Fraction(P,20*q) if permitted else None,
        "high_count_lower":Fraction(P,50*q) if permitted else None,
        "low_fraction_of_all_R_lower":Fraction(1,80) if permitted else None,
        "high_fraction_of_all_R_lower":Fraction(1,200) if permitted else None,
        "signed_high_minus_low_defect_lower":Fraction(P,3) if permitted else None,
        "unwrapped_phase_separation_lower":Fraction(1,288*n) if permitted else None,
        "unit_circle_chord_separation_lower":Fraction(1,72*n) if permitted else None,
        "normalized_modulus_squared_gap_lower":
            Fraction(1,82944000*n*n) if permitted else None,
        "normalized_modulus_gap_lower":
            Fraction(1,165888000*n*n) if permitted else None,
        "actual_phi_word":"IDENTICALLY_ONE",
        "WP09I_rational_shadow_first_witness":
            (21 if n==21 else None),
        "original_Cook_single_phase_tenth_saving":"OPEN",
        "Cook_weighted_prime_cofactor_estimate":"OPEN",
        "erdos249_irrationality":"OPEN",
        "mathcert":"NOT_SUBMITTED",
    }


def cook_oriented_word_residue(
    coeff, u: int, v: int, L: int
) -> int:
    """Exact exponent modulo 2^L of a word of *original* Cook phases.

    If E_N=exp(2pi*i D_{1,N,L}/Q) is the original FULL Cook phase and
    C_N=E_(N+1)*conj(E_N)^2, the oriented product
       prod_(j=u)^(v-1) C_(j-L-1)
    equals exp(2pi*i (b(v)-b(u))/Q).

    When u>v, define the product as the inverse of the reversed range.
    The function performs actual FULL numerator rolling, with three
    independent direct-oracle checks; no proxy bare source difference.
    """
    _positive(u,"u")
    _positive(v,"v")
    _positive(L,"L")
    if min(u,v) < L+2:
        raise ValueError("the original phase indices must be >=1")
    if u == v:
        return 0
    lo,hi=min(u,v),max(u,v)
    N=lo-L-1
    Q=1<<L
    D=cook_numerator_direct(coeff,N,1,L)
    phase_word=0
    checks=(lo,lo+(hi-lo)//2,hi-1)
    for t in range(lo,hi):
        source_start=(coeff(N+2)-coeff(N+1))
        source_terminal=(coeff(N+L+2)-coeff(N+L+1))
        D_next=2*D-Q*source_start+source_terminal
        step=(D_next-2*D)%Q
        if step!=(coeff(t+1)-coeff(t))%Q:
            raise AssertionError("true full-Cook step cocycle failed")
        if t in checks and D_next!=cook_numerator_direct(coeff,N+1,1,L):
            raise AssertionError("original full Cook rolling/direct mismatch")
        phase_word+=step
        D=D_next
        N+=1
    result=(phase_word if u<v else -phase_word)%Q
    if result!=(coeff(v)-coeff(u))%Q:
        raise AssertionError("oriented original phase word telescope failed")
    return result


def anchored_multiplicative_cook_word(
    coeff, n: int, m: int, m0: int, L: int
) -> dict[str, object]:
    """Exact original-phase word = twisted multiplicative-defect character.

    W_b(n;m,m0) =
      T_b(n*m0,n*m) / [T_b(m0,m)]^b(n)
      = exp(2pi*i (Delta_b(n,m)-Delta_b(n,m0))/Q).

    T uses only the full-length Cook E_N via E_(N+1)/E_N**2,
    which the verified integer engine exactly reconstructs.
    """
    for k,x in (("n",n),("m",m),("m0",m0),("L",L)):
        _positive(x,k)
    if n<3 or gcd(n,m)!=1 or gcd(n,m0)!=1:
        raise ValueError("n>=3 and both multipliers coprime to n required")
    if min(m,m0)<L+2:
        raise ValueError("Cook original phase indices must remain positive")
    Q=1<<L
    large=cook_oriented_word_residue(coeff,n*m0,n*m,L)
    small=cook_oriented_word_residue(coeff,m0,m,L)
    word=(large-coeff(n)*small)%Q
    d_m=coeff(n*m)-coeff(n)*coeff(m)
    d_0=coeff(n*m0)-coeff(n)*coeff(m0)
    direct=(d_m-d_0)%Q
    if word!=direct:
        raise AssertionError("genuine complete Cook word/defect exact identity failed")
    return {
        "n":n,"m":m,"m0":m0,"L":L,"Q":Q,
        "long_word_residue":large,
        "short_word_residue":small,
        "anchored_full_Cook_word_residue":word,
        "direct_defect_difference_residue":direct,
        "exact_word_equals_defect_difference":True,
        "uses_genuine_full_Cook_numerators":True,
        "word_can_span_O_nP_original_Cook_phases":True,
        "does_not_prove_original_first_harmonic_cancellation":True,
    }


def finite_two_range_replay(
    n: int, P: int, *, max_P: int = 1_300_000
) -> dict[str, object]:
    """Exact integer CRT/divisor-ratio replay on real phi.

    The analyzer does not evaluate the enormous-index canonical rational
    shadow correction bits. Uniform mathematics covers ALL admissible
    corrections. Optional float diagnostics use only a one-flip comparator
    and cannot certify the theorem.
    """
    c=cook_word_modulus_certificate(n,P)
    if not c["eligible"]:
        raise ValueError("the effective positive-density or legal Cook gates fail")
    _positive(max_P,"max_P")
    if P>max_P:
        raise ValueError("source finite-sieve budget exceeded")
    q=c["q"]
    phi=totients(2*P)
    a=[m for m in range(P,P+P//10) if m%q==1]
    b=[m for m in range(2*P-P//10,2*P) if m%q==1 and 10*phi[m]>=7*m]
    if 20*q*len(a)<P or 50*q*len(b)<P:
        raise AssertionError("true high/low CRT positive-density lemma failed")
    if not a or not b:
        raise AssertionError("nonempty positive-density source sets required")
    # This bounds ALL admissible eta, not a particular correction bit choice.
    max_low=max(2*phi[m]+2*(n+1) for m in a)
    min_high=min(2*phi[m]-2*(n+1) for m in b)
    if 3*(min_high-max_low)<P:
        raise AssertionError("uniform signed two-range defect gap failed")
    if 2*(max(2*phi[m]+2*(n+1) for m in b+a))>=c["Q"]:
        raise AssertionError("source defect separation may wrap modulo Q")
    # An illustrative one-flip (not dyadic-rational) source has
    # Delta=+2phi(m) if b(n)=phi(n)-2, and -2phi(m) for +2.
    # Exact integer worst-case gap is authoritative. Float means diagnostic.
    R=(m for m in range(P,2*P) if m%n==1)
    ct,re,im=0,0.0,0.0
    for m in R:
        angle=2*pi*(2*phi[m])/c["Q"]
        re+=cos(angle)
        im+=sin(angle)
        ct+=1
    modulus=(re*re+im*im)**0.5/ct
    if modulus>1.000001 or modulus<0:
        raise AssertionError("one-flip numerical diagnostic outside probability range")
    return {
        **c,
        "actual_low_count":len(a),
        "actual_high_ratio_good_count":len(b),
        "exact_low_high_gap_lower":min_high-max_low,
        "all_adversarial_two_unit_defects_controlled":True,
        "one_flip_nonrational_normalized_modulus_DIAGNOSTIC":modulus,
        "one_flip_is_dyadic_rational":False,
        "actual_shadow_huge_index_bits_evaluated":False,
    }
