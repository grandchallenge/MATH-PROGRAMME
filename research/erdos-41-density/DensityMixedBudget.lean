import Mathlib.Tactic.Ring

/-!
Algebraic certificates for the density-dependent B3 mixed-representation
budget. The universal B3 injection, matching theorem, and infinite-density
hypothesis are proved/discussed in DENSITY_FORCED_MIXED_BUDGET.md and are
NOT claimed as end-to-end formal Lean theorems here.
-/
namespace GCLErdos41.DensityMixedBudget

theorem exact_mixed_representation_count (x y : ℚ) :
    (x+y)*((x+y)*((x+y)+1)/2) - x*(x*(x+1)/2) -
      y*(y*(y+1)/2) = x*y*(3*(x+y)/2+1) := by ring

theorem exact_mixed_support_weight (x y : ℚ) :
    (x+y)*((x+y)^2-1) - x*(x^2-1) - y*(y^2-1) =
      3*x*y*(x+y) := by ring

theorem separated_block_count_constants (c : ℚ) :
    (3/2)*(c^3/36)*(c/2)*(c/2) = c^5/96 := by ring

theorem separated_block_weight_constants (c : ℚ) :
    3*(c^3/36)*(c/2)*(c/2) = c^5/48 := by ring

theorem separated_block_lag_constants (c : ℚ) :
    3*(c^3/36)*(c/2) = c^4/24 := by ring

end GCLErdos41.DensityMixedBudget
