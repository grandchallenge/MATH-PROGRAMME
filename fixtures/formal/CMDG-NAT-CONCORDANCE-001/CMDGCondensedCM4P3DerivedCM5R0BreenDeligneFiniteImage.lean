import Mathlib.RingTheory.Noetherian.Basic
import Mathlib.RingTheory.Finiteness.Finsupp
import Mathlib.LinearAlgebra.Isomorphisms
import Mathlib.RingTheory.Int.Basic

/-! Finite generation of an image controlled by a finite quotient and
a finite previous filtration stage. -/
noncomputable section
namespace CMDG.CondensedCM5R0.BreenDeligneFiniteImage

variable {R : Type} [CommRing R] [IsNoetherianRing R]
variable {M N H : Type} [AddCommGroup M] [AddCommGroup N] [AddCommGroup H]
  [Module R M] [Module R N] [Module R H]

theorem finite_image_of_control (f : M →ₗ[R] H) (g : M →ₗ[R] N)
    (P : Submodule R H) (hP : P.FG) [Module.Finite R N]
    (h : ∀ x, g x=0 → f x ∈ P) : (LinearMap.range f).FG := by
  have hk : LinearMap.ker g ≤ LinearMap.ker (P.mkQ.comp f) := by
    intro x hx
    rw [LinearMap.mem_ker,LinearMap.comp_apply]
    change Submodule.Quotient.mk (f x) = 0
    rw [Submodule.Quotient.mk_eq_zero]
    exact h x hx
  let d := (LinearMap.ker g).liftQ (P.mkQ.comp f) hk
  letI : Module.Finite R (LinearMap.range g) := Module.Finite.of_fg
    (Submodule.FG.of_le Module.Finite.fg_top le_top)
  letI : Module.Finite R (M ⧸ LinearMap.ker g) :=
    Module.Finite.equiv g.quotKerEquivRange.symm
  apply Submodule.fg_of_fg_map_of_fg_inf_ker P.mkQ
  · rw [← LinearMap.range_comp,← Submodule.range_liftQ (LinearMap.ker g) (P.mkQ.comp f) hk]
    exact Submodule.FG.of_finite
  · rw [Submodule.ker_mkQ]
    exact hP.of_le inf_le_right

#print axioms finite_image_of_control
end CMDG.CondensedCM5R0.BreenDeligneFiniteImage
