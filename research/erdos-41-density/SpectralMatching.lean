import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith

/-! Arithmetic certificates associated with the finite B3 spectral-matching
    theorem. The multiset-support matching proof is given in the research
    manuscript, not yet fully encoded as a Lean finite-set injection. -/
namespace GCLErdos41.SpectralMatching

theorem off_spectrum_first_mass (n : ℚ) :
    (n*(n+1)/2)^2-(n*(n+1)/2)-n^2*(n-1) =
      n*(n-1)*(n^2-n+2)/4 := by ring

theorem total_nonzero_mass (n q_ext : ℚ) :
    (n*(n+1)/2)^2-(n*(n+1)/2)+(n*(n+1)/2)*q_ext =
      (n*(n+1)/2)*((n*(n+1)/2)-1+q_ext) := by ring

theorem pointwise_quadratic_budget (n s : ℚ)
    (hn : 0 ≤ n) (hs : 0 ≤ s) (hle : s ≤ n) :
    s^2 ≤ n*s := by nlinarith [mul_nonneg hs (sub_nonneg.mpr hle)]

theorem hostile_spectrum_cap_failure :
    (1 : ℕ) + 3 > 3 := by norm_num

end GCLErdos41.SpectralMatching
