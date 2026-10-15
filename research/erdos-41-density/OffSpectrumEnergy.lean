import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring

/-! Algebraic receipts for the fourth-order B3 off-spectrum energy bound.
    The universal selector law and Cauchy-Schwarz proof remain in the
    written mathematical note OFF_SPECTRUM_FOURTH_MOMENT.md. -/
namespace GCLErdos41.OffSpectrum

theorem pair_count_lower (n : ℚ) (hn : 0 ≤ n) :
    n*n/2 ≤ n*(n+1)/2 := by nlinarith

theorem pair_count_upper (n : ℚ) (hn : 1 ≤ n) :
    n*(n+1)/2 ≤ n*n := by nlinarith

theorem known_difference_energy_polynomial (n : ℚ) :
    n*n*n*(n-1) = n^3*(n-1) := by ring

theorem modeled_critical_energy (n : ℚ) (hn : 320 ≤ n) :
    n^5 / 160 ≤ n^5 / 80 - 2 * n^4 := by
  have hpow : 0 ≤ n^4 := pow_nonneg (by linarith) _
  have h := mul_nonneg hpow (show 0 ≤ n-320 by linarith)
  nlinarith [h]

end GCLErdos41.OffSpectrum
