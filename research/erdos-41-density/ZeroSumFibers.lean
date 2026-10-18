import Mathlib.Tactic.Ring
import Lean.Elab.Tactic.Omega

/-!
Arithmetic certificates for the explicit infinitely many B3 blocks with a
shared nonzero zero-sum fiber. These declarations do NOT formalize the
universal B3 uniqueness argument; see ZERO_SUM_FIBER_AUDIT.md.
-/
namespace GCLErdos41.ZeroSumFibers

theorem centered_lag_one (T k : ℤ) :
    T + (T + 2*k + 1) - 2*(T+k) = 1 := by ring

theorem digit_comparison
    (x0 x1 x2 y0 y1 y2 : ℤ)
    (hc : x0+x1+x2 = y0+y1+y2)
    (hw : x1+2*x2 = y1+2*y2) :
    x0-y0 = x2-y2 ∧ x1-y1 = -2*(x2-y2) := by
  constructor <;> omega

theorem fiber_mass_polynomial (n : ℚ) :
    n * (n * (n+1) / 2 - 1) = n*(n-1)*(n+2)/2 := by ring

theorem weighted_mass_polynomial (n : ℚ) :
    2*(n*n*(n-1)/2)+n*(n-1) = n*(n*n-1) := by ring

theorem base16_no_digit_carry :
    (3 : ℕ) < 16 ∧ (6 : ℕ) < 16 := by decide

end GCLErdos41.ZeroSumFibers
