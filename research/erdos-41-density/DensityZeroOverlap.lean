import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith

/-!
Arithmetic receipts for density-conditioned separated B3 block selection.
These do NOT encode or assert existence of an infinite B3 set of positive
critical lower density. Full geometric/pigeonhole proof is in
DENSITY_LOCALIZED_ZERO_OVERLAP.md.
-/
namespace GCLErdos41.DensityZeroOverlap

theorem shell_density_margin (c : ℚ) :
    c - 3*(c/6) = c/2 := by ring

theorem support_product_lower_coefficient (c : ℚ) :
    (c/2)*(c/4) = c^2/8 := by ring

theorem fixed_k_support_coefficient (c : ℚ) :
    (c/2)*(c/2) = c^2/4 := by ring

theorem gap_minus_diameter_positive
    (g delta : ℚ) (h : delta < g) :
    0 < 2*g-2*delta := by linarith

theorem pair_sum_lag_interval_separation
    (minHi maxLo maxY minY : ℚ)
    (h : maxY-minY < minHi-maxLo) :
    2*maxLo-2*minY < 2*minHi-2*maxY := by linarith

end GCLErdos41.DensityZeroOverlap
