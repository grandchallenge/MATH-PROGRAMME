"""ERDOS-249 WP09-L: original Cook cofactor two-copy transfer with rational roots.

PROVED: exact cofactor-group second-moment sufficiency for source-locked
14X/25 weighted correlation; nonalignment and sharp adversarial obstruction.
Finite ORIGINAL-EULER-TOTIENT cases use only integer arithmetic and exact
rational Taylor/Archimedes/Machin bounds on every 2^L-th root of unity.
No floating-point trigonometric function participates in certification.
Finite s=8/12/26 runs, including h=1..8 at canonical s=26, do NOT
certify the cofinal all-h source theorem or irrationality.
"""
from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from functools import lru_cache
from math import factorial, isqrt

from experiments.erdos249_full_series_phase.fourier_probe import totients
from experiments.erdos249_full_series_phase.full_window_prime_projection import (
    cook_minimal_depth, cook_numerator_direct,
)

SCALE=10**15
COMPONENT_UNITS_ERROR=32


def _positive(x: int,name: str) -> None:
    if type(x) is not int or x < 1:
        raise ValueError(f"{name} must be a positive ordinary integer")


def _arctan_interval(q: int, terms: int=50) -> tuple[Fraction,Fraction]:
    """Alternating arctan series, exact geometric-tail sign enclosure."""
    _positive(q,"q")
    if q<=1:
        raise ValueError("arctan Machin denominator must exceed 1")
    acc=sum((Fraction((-1)**j,(2*j+1)*q**(2*j+1))
             for j in range(terms)), Fraction())
    nxt=Fraction((-1)**terms,(2*terms+1)*q**(2*terms+1))
    return (acc+min(nxt,0),acc+max(nxt,0))


@lru_cache(maxsize=1)
def pi_fixed_floor() -> dict[str,object]:
    """Certify floor(10^15*pi) exactly by Machin's identity."""
    a,b=_arctan_interval(5)
    c,d=_arctan_interval(239)
    lower=16*a-4*d
    upper=16*b-4*c
    lo=(lower*SCALE).__floor__()
    hi=(upper*SCALE).__floor__()
    if lo!=hi or not (Fraction(3)<lower<=upper<Fraction(22,7)):
        raise AssertionError("exact Machin pi interval did not certify integer")
    return {
        "pi_floor":lo,
        "pi_scaled_integer":lo,
        "pi_interval_width":upper-lower,
        "pi_lower":lower,"pi_upper":upper,
        "component_units_error":COMPONENT_UNITS_ERROR,
        "fixed_scale":SCALE,
    }


def _rounding_error_units(order:int,odd:bool) -> int:
    """Inductively bound integer-division recurrence rounding (ceil)."""
    e=0
    total=0
    for j in range(1,order+1):
        den=(2*j)*(2*j+1) if odd else (2*j-1)*(2*j)
        e=(10*e+den-1)//den+1
        total+=e
    return total


@lru_cache(maxsize=32768)
def _root_of_unity_fixed_cached(r:int,L:int) -> tuple[int,int]:
    """Certified cos/sin of e(2pi*i*r/2^L) as fixed-scale integers.

    Each true component differs from output/SCALE by <32/SCALE:
    - pi integer interval from exact alternating Machin formula;
    - angle quantization error <2/SCALE since |2r/Q|<=1;
    - 13-term Maclaurin exact integer Horner recurrence with
      rounding error <=25/SCALE per component;
    - tail errors <= (22/7)^28/28! and (22/7)^29/29!,
      each <1/SCALE. These are checked using exact rational comparisons.
    """
    _positive(L,"L")
    if type(r) is not int:
        raise ValueError("residue must be an ordinary integer")
    Q=1<<L
    v=r%Q
    if 2*v>Q:
        v-=Q
    p=pi_fixed_floor()["pi_floor"]
    x=(2*v*p)//Q
    if abs(x)*7>22*SCALE:
        raise AssertionError("exact root angle escaped Taylor interval")
    N=13
    if _rounding_error_units(N,False)>25 or _rounding_error_units(N,True)>25:
        raise AssertionError("Taylor fixed-point division error grew")
    if Fraction(22,7)**28 / factorial(28)>=Fraction(1,SCALE):
        raise AssertionError("cos remainder exceeds one fixed-point unit")
    if Fraction(22,7)**29 / factorial(29)>=Fraction(1,SCALE):
        raise AssertionError("sin remainder exceeds one fixed-point unit")
    tc=SCALE
    ts=x
    re=SCALE
    im=x
    sq=x*x
    for j in range(1,N+1):
        tc=-(tc*sq//(SCALE*SCALE*(2*j-1)*(2*j)))
        ts=-(ts*sq//(SCALE*SCALE*(2*j)*(2*j+1)))
        re+=tc
        im+=ts
    if not(-2*SCALE<=re<=2*SCALE and -2*SCALE<=im<=2*SCALE):
        raise AssertionError("fixed rational trigonometric evaluation escaped range")
    return re,im


def root_of_unity_fixed(r:int,L:int) -> tuple[int,int]:
    """Validate ordinary integer identity BEFORE cached Fourier lookup.

    Python equality makes False and 0 equal cache keys; a public cached
    function could otherwise bypass the type gate on a cache hit.
    """
    _positive(L,"L")
    if type(r) is not int:
        raise ValueError("residue must be an ordinary integer")
    return _root_of_unity_fixed_cached(r,L)


def _largest_prime_factors(limit:int) -> list[int]:
    lpf=[0]*(limit+1)
    for p in range(2,limit+1):
        if lpf[p]==0:
            for k in range(p,limit+1,p):
                lpf[k]=p
    return lpf


def _energy_from_group_sums(groups:dict[int,dict[str,int]],
                            prefix:str)->Fraction:
    return sum((Fraction(g[prefix+"_re"]**2+g[prefix+"_im"]**2,
                         g["n"]*SCALE*SCALE)
                for g in groups.values()),Fraction())


def _upper_group_absolute_z(groups:dict[int,dict[str,int]],G:int)->Fraction:
    return (sum((Fraction(isqrt(g["Z_re"]**2+g["Z_im"]**2)+1,SCALE)
                for g in groups.values()),Fraction())
            +Fraction(2*G*COMPONENT_UNITS_ERROR,SCALE))


def certified_actual_cofactor_transfer(
    X:int,h:int=1,s:int=8,eta_num:int=1,eta_den:int=1000,
    max_X:int=20000
)->dict[str,object]:
    """Finite rigorous all-integer TRUE-phi first-term and two-copy gate.

    This computes original full Cook D by exact rolling recurrence and
    the source's true largest-prime/cofactor groups. All root-of-unity
    evaluations have proven per-component rational enclosure. Returned
    certificates remain finite and never assert a cofinal conclusion.
    """
    for k,x in (("X",X),("h",h),("s",s),("eta_num",eta_num),
                ("eta_den",eta_den),("max_X",max_X)):
        _positive(x,k)
    if eta_num>=eta_den or X>max_X:
        raise ValueError("cofactor source parameter/budget gate failed")
    L=max(h+s,cook_minimal_depth(X,h))
    Q=1<<L
    t=L-s+1
    if not (h<t<=L and Q>=16*(2*X+h+L+2)):
        raise AssertionError("Cook source isolated-index size gate failed")
    phi=totients(2*X+h+L+4)
    lpf=_largest_prime_factors(2*X+t)
    sqrt=isqrt(X)
    max_m=sqrt//2
    D=cook_numerator_direct(phi,X,h,L)
    groups=defaultdict(lambda:{"n":0,"E_re":0,"E_im":0,
                               "Z_re":0,"Z_im":0,
                               "W_re":0,"W_im":0})
    sum_all_e_re=0
    sum_all_e_im=0
    sum_good_e_re=0
    third_re=third_im=0
    fourth_re=fourth_im=0
    count_A=0
    good=0
    checks=0
    for i in range(X):
        N=X+i
        if i in (0,X//2,X-1):
            if D!=cook_numerator_direct(phi,N,h,L):
                raise AssertionError("source exact full Cook rolling/direct mismatch")
            checks+=1
        e_re,e_im=root_of_unity_fixed(D%Q,L)
        sum_all_e_re+=e_re
        sum_all_e_im+=e_im
        k=N+t
        p=lpf[k]
        if p and p>2*sqrt and k//p<=max_m:
            count_A+=1
            m=k//p
            if phi[m]*eta_den>=eta_num*m:
                good+=1
                Z=(( (1<<h)-1)*phi[m]*(p-1)*(1<<(s-1)))%Q
                z_re,z_im=root_of_unity_fixed(Z,L)
                w_re,w_im=root_of_unity_fixed((D-Z)%Q,L)
                g=groups[m]
                g["n"]+=1
                g["E_re"]+=e_re
                g["E_im"]+=e_im
                g["Z_re"]+=z_re
                g["Z_im"]+=z_im
                g["W_re"]+=w_re
                g["W_im"]+=w_im
                sum_good_e_re+=e_re
            else:
                third_re+=e_re
                third_im+=e_im
        else:
            fourth_re+=e_re
            fourth_im+=e_im
        if i<X-1:
            D=(2*D
               -Q*(phi[N+h+1]-phi[N+1])
               +(phi[N+h+L+1]-phi[N+L+1]))
    if good!=sum(g["n"] for g in groups.values()) or good>count_A:
        raise AssertionError("source cofactor grouping/cardinality drift")
    C_E=_energy_from_group_sums(groups,"E")
    C_Z=_energy_from_group_sums(groups,"Z")
    C_W=_energy_from_group_sums(groups,"W")
    eps=Fraction(COMPONENT_UNITS_ERROR,SCALE)
    ce_error=8*good*eps
    C_E_hi=C_E+ce_error
    C_E_lo=max(Fraction(),C_E-ce_error)
    C_Z_hi=C_Z+ce_error
    C_Z_lo=max(Fraction(),C_Z-ce_error)
    C_W_hi=C_W+ce_error
    C_W_lo=max(Fraction(),C_W-ce_error)
    Z1_floor=sum((Fraction(isqrt(g["Z_re"]**2+g["Z_im"]**2),SCALE)
                  for g in groups.values()),Fraction())
    Z1_lo=max(Fraction(),Z1_floor-2*good*eps)
    Z1_hi=_upper_group_absolute_z(groups,good)
    B_re=sum((Fraction(g["W_re"]*g["Z_re"]-g["W_im"]*g["Z_im"],
                       g["n"]*SCALE*SCALE)
              for g in groups.values()),Fraction())
    B_im=sum((Fraction(g["W_re"]*g["Z_im"]+g["W_im"]*g["Z_re"],
                       g["n"]*SCALE*SCALE)
              for g in groups.values()),Fraction())
    S_approx=Fraction(sum_good_e_re,SCALE)-B_re
    def complex_mag_rational_upper(x:Fraction,y:Fraction)->Fraction:
        mag2=x*x+y*y
        if not mag2:
            return Fraction()
        k=mag2.numerator*SCALE*SCALE//mag2.denominator
        return Fraction(isqrt(k)+1,SCALE)
    def root_sum_modulus_upper(re:int,im:int,count:int)->Fraction:
        if count==0:
            return Fraction()
        return (Fraction(isqrt(re*re+im*im)+1,SCALE)
                +2*count*eps)
    second_mag_hi=(complex_mag_rational_upper(B_re,B_im)
                   +8*good*eps)
    third_mag_hi=root_sum_modulus_upper(third_re,third_im,count_A-good)
    fourth_mag_hi=root_sum_modulus_upper(fourth_re,fourth_im,X-count_A)
    all_four_pass=(
        S_approx+10*good*eps<=Fraction(14*X,25)
        and second_mag_hi<=Fraction(X,100)
        and third_mag_hi<=Fraction(X,100)
        and fourth_mag_hi<=Fraction(8*X,25))
    S_error=10*good*eps
    S_low,S_hi=S_approx-S_error,S_approx+S_error
    original_E_re_lower=Fraction(sum_all_e_re,SCALE)-X*eps
    original_E_re_upper=Fraction(sum_all_e_re,SCALE)+X*eps
    allowed=Fraction(14*X,25)
    gap_budget=allowed-Z1_hi
    criterion= bool(gap_budget>0 and good*C_E_hi<=gap_budget**2)
    Cauchy_bound_fails=bool(
        (good-C_W_hi)*(good-C_Z_hi)>allowed**2)
    if not (Fraction(0)<=C_E_lo<=C_E_hi<=good+ce_error):
        raise AssertionError("cofactor conditional energy invalid")
    return {
        "X":X,"h":h,"s":s,"eta_num":eta_num,"eta_den":eta_den,
        "L":L,"Q":Q,"t":t,"source_A_count":count_A,
        "source_G_count":good,"group_count":len(groups),
        "source_A_not_G_count":count_A-good,
        "source_outside_A_count":X-count_A,
        "three_direct_full_Cook_numerator_oracles":checks,
        "original_full_Cook_real_first_harmonic_lower":original_E_re_lower,
        "original_full_Cook_real_first_harmonic_upper":original_E_re_upper,
        "original_full_Cook_9X_over_10_FINITE":
            original_E_re_upper<=Fraction(9*X,10),
        "cofactor_good_E_two_copy_energy_upper":C_E_hi,
        "cofactor_good_E_two_copy_energy_lower":C_E_lo,
        "cofactor_good_Z_two_copy_energy_lower":C_Z_lo,
        "cofactor_good_W_two_copy_energy_lower":C_W_lo,
        "source_z_group_absolute_mean_lower":Z1_lo,
        "source_z_group_absolute_mean_upper":Z1_hi,
        "original_first_weighted_Cook_sum_real_lower":S_low,
        "original_first_weighted_Cook_sum_real_upper":S_hi,
        "first_weighted_Cook_14X_over_25_FINITE":S_hi<=allowed,
        "Cook_second_weighted_group_modulus_upper":second_mag_hi,
        "Cook_third_excluded_good_modulus_upper":third_mag_hi,
        "Cook_fourth_outside_A_modulus_upper":fourth_mag_hi,
        "source_locked_four_bounds_FINITE":all_four_pass,
        "Cook_second_1X_over_100_FINITE":second_mag_hi<=Fraction(X,100),
        "Cook_third_1X_over_100_FINITE":third_mag_hi<=Fraction(X,100),
        "Cook_fourth_8X_over_25_FINITE":fourth_mag_hi<=Fraction(8*X,25),
        "two_copy_sufficient_criterion_FINITE":criterion,
        "generic_WZ_Cauchy_certificate_INSUFFICIENT":Cauchy_bound_fails,
        "adversarial_w_conjugate_z_Vz_lower":good-C_Z_hi,
        "adversarial_w_conjugate_z_Vz_upper":good-C_Z_lo,
        "adversarial_w_conjugate_z_violates_14X_over_25":
            good-C_Z_hi>allowed,
        "finite_source_s_not_26":s!=26,
        "cofinal_source_14X_over_25":"OPEN",
        "original_Erdos249_irrationality":"OPEN",
        "MATHCERT":"NOT_SUBMITTED",
        "root_error_per_real_imag_component":eps,
        "pi_integer_certificate":pi_fixed_floor()["pi_floor"],
        "method":"EXACT_INTEGER_RATIONAL_INTERVAL_NOT_FLOATING_DIAGNOSTIC"
    }
