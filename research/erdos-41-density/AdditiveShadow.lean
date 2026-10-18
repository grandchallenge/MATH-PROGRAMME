import Mathlib.Tactic.Ring
import Mathlib.Tactic.NormNum

/-! Polynomial, first/second-moment, and counterfixture certificates for
Erdős #41 additive-shadow methods. The universal M3 set-injection arguments
and the distinct-integer moment inequality are given as written proofs in
ADDITIVE_SHADOW_MOMENTS.md, not asserted to be Lean formalizations here. -/
namespace GCLErdos41.AdditiveShadow

theorem shadow_count_polynomial (n : ℤ) :
    2*n+n*n*(n-1) = n^3-n^2+2*n := by ring

theorem nontrivial_representation_count (n : ℤ) :
    n*n*(n+1)-2*n*n = n*n*(n-1) := by ring

theorem convolution_moment_identity
    (q r sP qP sY qY : ℤ) :
    (q*r)*(r*qP+q*qY+2*sP*sY)-(r*sP+q*sY)^2 =
      r^2*(q*qP-sP^2)+q^2*(r*qY-sY^2) := by ring

theorem separate_moment_witness_first :
    12*(6*9399-237^2)-6^2*(6^2-1) = (1440 : ℤ) := by norm_num

theorem separate_moment_witness_second :
    12*(6*11899-267^2)-6^2*(6^2-1) = (0 : ℤ) := by norm_num

theorem cross_pattern_moment_obstruction :
    12*(12*21298-504^2)-12^2*(12^2-1) = (-1872 : ℤ) := by norm_num

theorem cross_pattern_actual_collision :
    13+13+17 = (10+16+17 : ℕ) := by norm_num

theorem contiguous_eight_shadow_impossible :
    (8^3-8^2+2*8 : ℕ) > 6*7+2 := by norm_num

end GCLErdos41.AdditiveShadow
