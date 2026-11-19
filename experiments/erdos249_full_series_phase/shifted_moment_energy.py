"""ERDOS249 WP09-B: exact second moment and Cook phase-energy checks.

The all-X analytic theorem is in SHIFTED_MOMENT_ENERGY_009B.md.
Finite exact rational CRT or integer arithmetic tests supplement but
do not substitute for the infinite correlation proof.

No originality, MATHCERT, or irrationality certification claimed.
"""
from fractions import Fraction
from math import isqrt, prod

from experiments.erdos249_full_series_phase.overlog_phase_separation import (
    centered, totients
)
from experiments.erdos249_full_series_phase.shifted_first_harmonic import (
    _is_prime, cook_minimal_depth, rational_shift_control,
    signed_shift_numerators,
)


def prime_list(cutoff: int) -> tuple[int, ...]:
    if cutoff < 2:
        raise ValueError("cutoff must be >=2")
    flags = bytearray(b"\x01") * (cutoff + 1)
    flags[0:2] = b"\x00\x00"
    for p in range(2, isqrt(cutoff) + 1):
        if flags[p]:
            flags[p*p:cutoff+1:p] = (
                b"\x00" * (((cutoff-p*p)//p)+1)
            )
    return tuple(n for n in range(2, cutoff + 1) if flags[n])


def _check_primes(ps: tuple[int, ...]) -> tuple[int, ...]:
    if not ps or tuple(sorted(set(ps))) != ps:
        raise ValueError("nonempty ordered distinct prime support required")
    if any(not _is_prime(p) for p in ps):
        raise ValueError("all support members must be prime")
    return ps


def finite_euler_moments(h: int, ps: tuple[int, ...]
                        ) -> dict[str, Fraction]:
    """Exact CRT Euler factors for finite prime support."""
    if h < 1:
        raise ValueError("positive h required")
    _check_primes(ps)
    A, B, Bstar = Fraction(1), Fraction(1), Fraction(1)
    for p in ps:
        a = Fraction(1)-Fraction(2,p*p)+Fraction(1,p**3)
        b = a if h % p == 0 else Fraction(1)-Fraction(2,p*p)
        bstar = Fraction(1)-Fraction(2,p*p)
        A *= a
        B *= b
        Bstar *= bstar
    return {
        "A_f_squared": A,
        "B_shifted_correlation": B,
        "V_squared_difference": 2*(A-B),
        "Bstar_baseline": Bstar,
    }


def exact_finite_crt_period(h: int, ps: tuple[int, ...],
                            max_period: int = 5_000
                            ) -> dict[str, Fraction]:
    """Independently average f_P(n) and f_P(n+h) over full period.

    The finite CRT result is algebraic, with no asymptotic inference.
    """
    if h < 1:
        raise ValueError("positive h required")
    _check_primes(ps)
    M=prod(ps)
    if max_period < 1 or M > max_period:
        raise ValueError("finite CRT period exceeds resource cap")

    def f(n: int) -> Fraction:
        val=Fraction(1)
        for p in ps:
            if n % p == 0:
                val *= Fraction(p-1,p)
        return val

    A=sum((f(n)**2 for n in range(1,M+1)),Fraction())/M
    B=sum((f(n)*f(n+h) for n in range(1,M+1)),Fraction())/M
    V=sum(((f(n+h)-f(n))**2 for n in range(1,M+1)),
          Fraction())/M
    expected=finite_euler_moments(h,ps)
    if (A != expected["A_f_squared"] or
        B != expected["B_shifted_correlation"] or
        V != expected["V_squared_difference"]):
        raise AssertionError("independent finite CRT Euler identity failed")
    return {
        "A_exact_period": A, "B_exact_period": B,
        "V_exact_period": V, "period": Fraction(M),
    }


def first_omitted_prime(h: int) -> int:
    """Find the first prime not dividing a fixed h."""
    if h < 1:
        raise ValueError("positive shift required")
    p=2
    while h % p == 0 or not _is_prime(p):
        p += 1
    return p


def euler_moment_bounds(h: int, cutoff: int = 127
                        ) -> dict[str, object]:
    """Rigorous rational bounds on infinite Euler-product V_h.

    Each omitted product factor is in [1-2/p^2,1].
    For cutoff B, omitted prime-factor deficit is <=2/B.
    """
    if h < 1 or cutoff < 3 or cutoff > 4096:
        raise ValueError("positive h, 3<=cutoff<=4096 required")
    ps=prime_list(cutoff)
    data=finite_euler_moments(h,ps)
    A=data["A_f_squared"]
    B=data["B_shifted_correlation"]
    tail=Fraction(2,cutoff)
    lower=max(Fraction(),2*(A*(1-tail)-B))
    upper=2*(A-B*(1-tail))
    p=first_omitted_prime(h)
    structural_lower=Fraction(1,9*p**3)
    if not upper > structural_lower:
        raise AssertionError("Euler envelope contradicts fixed-prime lower")
    return {
        "h":h, "cutoff":cutoff, "prime_count":len(ps),
        "lower_V_from_tail":lower,
        "upper_V_from_tail":upper,
        "unconditional_strict_V_lower":structural_lower,
        "first_prime_not_dividing_shift":p,
        "rigorous_harmonic_saving_lower":Fraction(1,22500*p**3),
        "proof_scope":"NORMALIZED_TWO_POINT_CORRELATION_ONLY",
    }


def exact_phase_energy(X: int, h: int,
                       coefficients: list[int] | None = None
                       ) -> dict[str, object]:
    """Finite exact Cook phase-energy transference certificate.

    Checks Σd² <=9Σr² for the exact modulo-Q shifted window.
    The analytic 1-cos inequality (not numerically approximated)
    converts it to a lower bound on the real harmonic deficit.
    """
    if X < 64 or h < 1:
        raise ValueError("X>=64 and positive shift required")
    L=cook_minimal_depth(X,h)
    Q=1<<L
    limit=2*X+L+h+1
    if coefficients is None:
        a=totients(limit)
        kind="ACTUAL_EULER_TOTIENT"
    else:
        a=coefficients
        kind="EXPLICIT_INTEGER_COMPARATOR"
    if len(a)<=2*X+L+h or any(
        (not isinstance(a[n],int) or a[n]<0 or a[n]>n)
        for n in range(1,2*X+L+h+1)
    ):
        raise ValueError("coefficient source must cover indices and be 0..n integers")
    Ds=signed_shift_numerators(X,h,L,a)
    residues=tuple(centered(D,Q) for D in Ds[:-1])
    diffs=tuple(
        a[n+h]-a[n]
        for n in range(X+L+1,2*X+L)
    )
    if len(diffs)!=X-1 or len(residues)!=X:
        raise AssertionError("window endpoints incorrect")
    if any(2*abs(d)>=Q for d in diffs):
        raise ValueError("local shifted differences exceed half modulus")
    residual_energy=sum(r*r for r in residues)
    arithmetic_energy=sum(d*d for d in diffs)
    if arithmetic_energy > 9*residual_energy:
        raise AssertionError("phase-energy operator inequality falsified")
    for i,d in enumerate(diffs):
        if (residues[i+1]-2*residues[i]-d)%Q:
            raise AssertionError("exact shifted residue recurrence failed")
    guarantee=Fraction(8*arithmetic_energy,9*Q*Q)
    return {
        "X":X,"h":h,"L":L,"Q":Q,"source":kind,
        "arithmetic_squared_energy":arithmetic_energy,
        "centered_residual_squared_energy":residual_energy,
        "rigorous_harmonic_deficit_lower":guarantee,
        "deficit_lower_per_index":guarantee/X,
        "single_step_Cook_ten_percent":"NOT_CERTIFIED",
        "original_irrationality":"OPEN",
    }


def rational_hostile_phase_energy(X: int, h: int, modulus: int
                                  ) -> dict[str,object]:
    """An exact complete-rational-series control with shifted energy."""
    if h < 1 or modulus < 3:
        raise ValueError("positive h, modulus>=3 required")
    L=cook_minimal_depth(X,h)
    limit=2*X+L+h+1
    a=[rational_shift_control(n,h,modulus)
       for n in range(limit+1)]
    return exact_phase_energy(X,h,coefficients=a)
