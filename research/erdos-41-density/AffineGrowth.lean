import Init
import Lean.Elab.Tactic.Omega

namespace GCLErdos41.DensityTransfer

def CubicGrowthUnbounded (a : Nat → Nat) : Prop :=
  ∀ C N : Nat, ∃ k : Nat, N ≤ k ∧ C * (k + 1)^3 ≤ a k

theorem cubic_growth_affine_iff (a : Nat → Nat) :
    CubicGrowthUnbounded (fun k => 4 * a k + 1) ↔ CubicGrowthUnbounded a := by
  constructor
  · intro hb C N
    obtain ⟨k, hk, h⟩ := hb (4*C+1) N
    refine ⟨k, hk, ?_⟩
    have hp : 1 ≤ (k+1)^3 := by
      have h1 : 1 ≤ k+1 := by omega
      exact Nat.one_le_pow 3 _ h1
    have heq : (4*C+1) * ((k+1)^3) =
        4 * (C * ((k+1)^3)) + ((k+1)^3) := by
      simp [Nat.add_mul, Nat.mul_assoc]
    change (4*C+1) * ((k+1)^3) ≤ 4 * a k + 1 at h
    rw [heq] at h
    omega
  · intro ha C N
    obtain ⟨k, hk, h⟩ := ha C N
    refine ⟨k, hk, ?_⟩
    change C * ((k+1)^3) ≤ 4 * a k + 1
    omega

end GCLErdos41.DensityTransfer
