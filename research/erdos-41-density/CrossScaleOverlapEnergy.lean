import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith

/-!
Finite rational algebraic certificates for the B3 cross-family centered-lag
overlap research audit. The complete set-valued correlation identity,
B3 pair-sum injectivity and infinite density consequences are WRITTEN
proofs, not claimed as Lean formalizations.
-/
namespace GCLErdos41.CrossScaleOverlap

theorem partition_pair_count_two (x y : ℚ) :
    ((x+y)*(x+y+1)/2)
    -x*(x+1)/2-y*(y+1)/2 = x*y := by ring

theorem partition_pair_count_three (x y z : ℚ) :
    ((x+y+z)*(x+y+z+1)/2)
    -x*(x+1)/2-y*(y+1)/2-z*(z+1)/2
      = x*y+x*z+y*z := by ring

theorem two_family_second_moment
    (f g : ℚ) : (f+g)^2-f^2-g^2=2*f*g := by ring

theorem three_family_second_moment
    (f g h : ℚ) :
    (f+g+h)^2-(f^2+g^2+h^2)
      =2*(f*g+f*h+g*h) := by ring

theorem cross_pair_deficit_nonnegative
    (x y : ℚ) (hx : 0 ≤ x) (hy : 0 ≤ y) :
    x*(x+1)/2+y*(y+1)/2 ≤
      (x+y)*(x+y+1)/2 := by
  nlinarith [mul_nonneg hx hy]

theorem collision_pressure_algebra
    (energy overlap : ℚ) :
    (energy+2*overlap)-energy=2*overlap := by ring

end GCLErdos41.CrossScaleOverlap
