import Mathlib.Tactic.Ring
import Mathlib.Tactic.NormNum

/-! Polynomial receipts for the exact B3 cubic-shadow moments and multiscale
    variance decomposition. These are not kernel formalizations of the
    universal B3 set injection or the infinite density problem. -/

namespace GCLErdos41.CrossScaleMoments

theorem first_shadow_moment (n s : ℚ) :
    n*(n+1)*s - (n*(n+1)/2)*s - (n-1)*s
       = ((n*n-n+2)/2)*s := by ring

theorem second_shadow_moment (n s q : ℚ) :
    n*((n+2)*q+s^2)+(n*(n+1)/2)*q-2*(n+1)*s^2-(n-1)*q
       = ((3*n*n+3*n+2)/2)*q-(n+2)*s^2 := by ring

theorem central_variance_multiplier (n : ℚ) :
    2*n*(n+2)+(n*n-n+2)=3*n*n+3*n+2 := by ring

theorem weighted_two_block_decomposition
    (f g u v r s : ℚ) :
    (f+g)*(f*(u^2+r)+g*(v^2+s))-(f*u+g*v)^2
       = (f+g)*(f*r+g*s)+f*g*(u-v)^2 := by ring

theorem cubic_shadow_shift (a b c h : ℤ) :
    (a+h)+(b+h)-(c+h) = (a+b-c)+h := by ring

theorem failed_zero_sum_anchor :
    (1+5-2*2 : ℤ) = 2+2-2*1 := by norm_num

theorem shadow_three_element_example :
    ((3^3-3^2+2*3 : ℕ)/2) = 12 := by norm_num

end GCLErdos41.CrossScaleMoments
