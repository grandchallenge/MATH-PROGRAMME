"""WP09-I: SHARP <=2 parity-preserving dyadic rational shadow of true phi.

Exact analytic theorem: for each K>=6 there is a_K with integer
0 <= phi(n)-a_K(n) <=2 at all n, same parity and 0<=a_K(n)<=n,
equal phi through K, and full binary sum equal to the EXPLICIT
dyadic rational gamma_K=sum_(n<=3K)phi(n)/2^n. All late legal Cook
phases lie within 1/16 of integers despite inherited WP09-G 2x3
imaginary cocycle signature. Mathematical proof:
TWO_UNIT_PARITY_SHADOW_009I.md. No claim about true-alpha irrationality.
"""
from __future__ import annotations

from fractions import Fraction

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


def _positive(x:int,name:str)->None:
    if type(x) is not int or x<1:
        raise ValueError(f"{name} must be a positive ordinary integer")


def two_unit_target(K:int)->dict[str,object]:
    """Exact lower dyadic rational gamma and capacity for correction bits."""
    _positive(K,"K")
    if K<6:
        raise ValueError("parity-preserving two-unit theorem requires K>=6")
    M=3*K
    phi=totients(M)
    gamma=Fraction(sum(phi[n]<<(M-n) for n in range(1,M+1)),1<<M)
    capacity=Fraction(2,1<<K)
    tail_upper=Fraction(M+2,1<<M)
    if not 0<tail_upper<capacity:
        raise AssertionError("binary signed tail cannot fit correction budget")
    return {
        "K":K,"M":M,"gamma":gamma,"dyadic_denominator":1<<M,
        "correction_capacity":capacity,
        "positive_true_totient_tail_upper":tail_upper,
        "sup_coefficient_distance":2,
        "parity_preserved_from_n":3,
        "odd_prime_coefficients_preserved_exactly":False,
        "original_totient_binary_series_status":"OPEN",
    }


def certified_binary_prefix(
    K:int,J:int,margin_bits:int=48,max_expansions:int=4
)->dict[str,object]:
    """Certify floor(2^J x) by EXACT totient partial sums and tail intervals.

    x = 2^(K-1)*sum_(n>3K)phi(n)/2^n, and x is in (0,1).
    For T>=3K+1, set A_T=sum_(3K<n<=T)phi(n)*2^(T-n).
    Then 2^J*x is in [A_T/2^q,(A_T+T+2)/2^q],
    q=T-(J+K-1). If both floors agree, the first J digits
    are proved, even without knowing rationality of the true series.
    """
    c=two_unit_target(K)
    for name,v in (("J",J),("margin_bits",margin_bits),
                   ("max_expansions",max_expansions)):
        _positive(v,name)
    for t in range(max_expansions):
        T=max(c["M"]+1,J+K+margin_bits+32*t)
        phi=totients(T)
        A=sum(phi[n]<<(T-n) for n in range(c["M"]+1,T+1))
        shift=T-(J+K-1)
        if shift<1:
            raise AssertionError("binary prefix denominator must be integral")
        lo=A>>shift
        hi=(A+T+2)>>shift
        if lo==hi:
            if not 0<=lo<(1<<J):
                raise AssertionError("positive totient tail binary digits escaped unit")
            digits=tuple((lo>>(J-j))&1 for j in range(1,J+1))
            if sum(d<<(J-j) for j,d in enumerate(digits,start=1))!=lo:
                raise AssertionError("certified binary digits failed reconstruction")
            return {
                "K":K,"J":J,"T":T,
                "binary_integer_prefix":lo,"digits":digits,
                "exact_interval_denominator":1<<shift,
                "exact_interval_lower_numerator":A,
                "exact_interval_upper_numerator":A+T+2,
                "certified":True,
            }
    raise ValueError("finite arithmetic interval straddles a binary digit boundary")


def two_unit_coefficients(limit:int,K:int=8,
                          max_limit:int=12000)->dict[str,object]:
    """Exact finite coefficients; infinite definition is by floor digits."""
    _positive(limit,"limit")
    _positive(max_limit,"max_limit")
    c=two_unit_target(K)
    if limit>max_limit:
        raise ValueError("two-unit source smoke budget exceeded")
    phi=totients(max(limit,c["M"]))
    values=list(phi[:limit+1])
    J=max(0,limit-K)
    digits=certified_binary_prefix(K,J) if J else None
    if J:
        for j,b in enumerate(digits["digits"],start=1):
            values[K+j]-=2*b
    for n in range(1,limit+1):
        if not (0<=phi[n]-values[n]<=2 and 0<=values[n]<=n):
            raise AssertionError("bounded signed shadow source envelope failed")
        if n>=3 and (phi[n]-values[n])%2:
            raise AssertionError("shadow parity preservation failed")
        if n<=K and values[n]!=phi[n]:
            raise AssertionError("shadow's arbitrary finite exact prefix changed")
    return {
        "K":K,"limit":limit,"J":J,
        "gamma":c["gamma"],
        "coefficients":tuple(values),
        "true_totients":tuple(phi[:limit+1]),
        "digit_certificate":digits,
        "exact_max_gap":2,
    }


def two_unit_cook_replay(
    X:int,h:int=1,K:int=8,L:int|None=None,max_X:int=2000
)->dict[str,object]:
    """All actual-length shadow Cook D, exact integer tail and direct oracle."""
    _positive(X,"X")
    _positive(h,"h")
    if L is None:
        L=cook_minimal_depth(X,h)
    _positive(L,"L")
    c=two_unit_target(K)
    Q=1<<L
    if X<c["M"] or L<h or Q<16*(2*X+h+L+2):
        raise ValueError("shadow integer tail or original Cook size ineligible")
    if X>max_X:
        raise ValueError("bounded actual Cook replay limit exceeded")
    last=2*X+h+L+2
    s=two_unit_coefficients(last,K,max_limit=2*max_X+h+L+4)
    a,phi=s["coefficients"],s["true_totients"]
    Da=cook_numerator_direct(a,X,h,L)
    checked=0
    rmax=0
    for i in range(X):
        N=X+i
        r=centered_representative(Da,Q)
        rmax=max(rmax,abs(r))
        if abs(r)>N+h+L+2 or 16*abs(r)>=Q:
            raise AssertionError("true dyadic binary shadow Cook residue escaped")
        if abs((a[N+L+1+h]-a[N+L+1])
               -(phi[N+L+1+h]-phi[N+L+1]))>2:
            raise AssertionError("two-unit true source transfer violated")
        if i in (0,X//2,X-1):
            if Da!=cook_numerator_direct(a,N,h,L):
                raise AssertionError("full shadow rolling vs direct source mismatch")
            checked+=1
        if i<X-1:
            Da=2*Da-Q*(a[N+1+h]-a[N+1])+(a[N+L+1+h]-a[N+L+1])
    nmax=last
    prefix=Fraction(sum(a[n]<<(nmax-n) for n in range(1,nmax+1)),1<<nmax)
    if not prefix<=c["gamma"]<=prefix+Fraction(nmax+2,1<<nmax):
        raise AssertionError("exact lower rational target outside coefficient envelope")
    return {
        "X":X,"h":h,"K":K,"L":L,"Q":Q,
        "exact_rational_target":c["gamma"],
        "actual_length_direct_oracle_points":checked,
        "largest_centered_residue":rmax,
        "every_real_original_cook_phase_strictly_gt_0_9":True,
        "coefficient_distance_verified_max":2,
        "true_totient_Cook_tenth_saving":"OPEN",
    }


def two_unit_phase_stability(X:int,K:int=8,L:int|None=None,
                             step:int=1)->dict[str,object]:
    """Mathematically proven exact coefficients OF pi for phase stability."""
    _positive(X,"X")
    two_unit_target(K)
    _positive(step,"step")
    if L is None:
        L=cook_minimal_depth(X,1)+1
    _positive(L,"L")
    Q=1<<L
    if X<3*K or Q<16*(2*X+L+3):
        raise ValueError("source admissibility or rational denominator gate fails")
    return {
        "X":X,"K":K,"L":L,"Q":Q,"k":step,
        "one_step_source_difference_abs_max":2,
        "single_k_step_phase_distance_coefficient_of_pi":
            Fraction(4*((1<<step)-1),Q),
        "at_most_X_weighted_sum_difference_coefficient_of_pi":
            Fraction(4*X*((1<<step)-1),Q),
        "original_tenth_saving_transfer":"NO",
    }


def two_unit_two_prime_certificate(X:int,K:int=8,
                                   L:int|None=None)->dict[str,object]:
    """A dyadic rational inherits the same order-X WP09-G U signature.

    U_shadow >= U_phi -4*pi*X/Q
             >= pi*X*(X-256)/(64Q)
             >= pi*X^2/(128Q) for X>=512.
    """
    two_unit_target(K)
    c=two_prime_certificate(X,L)
    if not c["eligible"] or X<3*K or X<512:
        raise ValueError("WP09-G actual source or shadow integer-tail gate fails")
    Q=c["Q"]
    return {
        "X":X,"K":K,"L":c["L"],"Q":Q,
        "actual_phi_U_lower_coefficient_of_pi":Fraction(X*X,64*Q),
        "two_unit_shadow_U_error_upper_coefficient_of_pi":Fraction(4*X,Q),
        "shadow_U_lower_coefficient_of_pi":
            Fraction(X*(X-256),64*Q),
        "half_strength_shadow_U_lower_coefficient_of_pi":
            Fraction(X*X,128*Q),
        "cofinal_shadow_U_lower_coefficient_of_pi":
            Fraction(X,32768)
            if (c["L"]==c["cook_minimum_depth"]+1 and Q<256*X)
            else None,
        "rational_shadow_all_late_original_real_phases_gt_0_9":True,
        "original_totient_tenth_saving":"OPEN",
    }
