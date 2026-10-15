import Mathlib.Tactic.Ring

/-!
Polynomial certificates for exact mixed B3 centered-lag moments and
positive/negative extreme-type weights. Universal finite-set B3 matching
and the hypothetical infinite-density consequences are written mathematics
in MIXED_LAG_BALLISTIC_DISPERSION.md, not end-to-end Lean theorems here.
-/
namespace GCLErdos41.MixedBallistic

theorem full_vs_monochromatic_weight (x y : ℚ) :
    (x+y)^3-x^3-y^3 = 3*x*y*(x+y) := by ring

theorem exact_mixed_second_moment_polynomial
    (x y vx vy delta : ℚ) :
    (x+y)^2*(x*vx+y*vy)+(x+y)*x*y*delta^2
      -x^3*vx-y^3*vy =
      x*y*((2*x+y)*vx+(x+2*y)*vy+(x+y)*delta^2) := by ring

theorem mixed_second_normalization (x y z : ℚ) :
    6*x*y*z = 3*x*y*(2*z) := by ring

theorem extreme_type_one_third_mass (x y : ℚ) :
    x^2*y+x*y^2 = (3*x*y*(x+y))/3 := by ring

theorem density_each_tail_constant (c : ℚ) :
    (c^3/36)*(c/2) = c^4/72 := by ring

theorem density_both_tails_constant (c : ℚ) :
    2*(c^4/72) = c^4/36 := by ring

end GCLErdos41.MixedBallistic
