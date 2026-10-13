import Mathlib.Algebra.Order.Ring.Unbundled.Rat
import Mathlib.Tactic

namespace GCLErdos41.ShellHardy

/-- The convexity inequality used in the discrete cubic Hardy bound. -/
theorem cube_two (x y : ℝ) (hx : 0 ≤ x) (hy : 0 ≤ y) :
    (x+y)^3 ≤ 4*(x^3+y^3) := by
  have h : 0 ≤ (x+y) * (x-y)^2 :=
    mul_nonneg (add_nonneg hx hy) (sq_nonneg _)
  nlinarith [h]

end GCLErdos41.ShellHardy
