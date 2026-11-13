import CMDGCondensedCM4P3DerivedCM5R0StoneanKernelDimension
import Mathlib.Algebra.Homology.DerivedCategory.Ext.ExactSequences

/-!
# CM5: every arbitrary-profinite Ext¹ class comes from the Stonean kernel

For every profinite T, and any actual condensed ZLift-module target A,
the projective Stonean presentation

  0 → K_T → F_{P(T)} → F_T → 0

has a surjective connecting map
  Ext⁰(K_T,A) → Ext¹(F_T,A).

This is unconditional. It is the precise degree-one obstruction:
Ext¹ vanishes exactly when that connecting map is zero. No
assertion that the connecting map is zero is made here.

No finiteness hypothesis on T, and no projectivity hypothesis on
K_T or injectivity hypothesis on A.
-/

noncomputable section

universe u

open CategoryTheory Limits

namespace CMDG.CondensedCM5R0

/-- The connecting homomorphism from the actual kernel's Ext⁰
to the free profinite object's Ext¹. -/
noncomputable def stoneanKernelExtOneObstruction
    (T : Profinite.{u}) (A : Ambient) :
    Abelian.Ext (stoneanPresentationKernel T) A 0 →
      Abelian.Ext ((Condensed.profiniteFree Coeff).obj T) A 1 :=
  fun x => (stoneanPresentationShortExact T).extClass.comp x (by decide)

/-- Every condensed Ext¹ class on arbitrary profinite T is represented
by the canonical Stonean presentation's degree-zero kernel obstruction.
The proof is the long exact Ext sequence and genuine projectivity of
the Stonean source, not a claim that the obstruction vanishes. -/
theorem stoneanKernelExtOneObstruction_surjective
    (T : Profinite.{u}) (A : Ambient) :
    Function.Surjective (stoneanKernelExtOneObstruction T A) := by
  intro e
  letI : Projective
      ((Condensed.profiniteFree Coeff).obj
        (Stonean.toProfinite.obj T.presentation)) :=
    freeStoneanPresentation_source_projective T
  have hzero :
      (Abelian.Ext.mk₀ (freeStoneanPresentationMap T)).comp e (zero_add 1) = 0 := by
    exact Abelian.Ext.eq_zero_of_projective _
  obtain ⟨x, hx⟩ := Abelian.Ext.contravariant_sequence_exact₃
    (stoneanPresentationShortExact T) A e hzero (by decide : 1 + 0 = 1)
  exact ⟨x, hx⟩

/-- **Exact criterion**, not assumed vanishing: Ext¹ from F_T into A
vanishes if and only if every kernel connecting obstruction maps to zero. -/
theorem freeProfinite_extOne_vanishes_iff_kernel_obstruction_zero
    (T : Profinite.{u}) (A : Ambient) :
    (∀ e : Abelian.Ext ((Condensed.profiniteFree Coeff).obj T) A 1, e = 0) ↔
      (∀ x : Abelian.Ext (stoneanPresentationKernel T) A 0,
        stoneanKernelExtOneObstruction T A x = 0) := by
  constructor
  · intro h x
    exact h _
  · intro h e
    obtain ⟨x, rfl⟩ := stoneanKernelExtOneObstruction_surjective T A e
    exact h x

#print axioms stoneanKernelExtOneObstruction_surjective
#print axioms freeProfinite_extOne_vanishes_iff_kernel_obstruction_zero

end CMDG.CondensedCM5R0
