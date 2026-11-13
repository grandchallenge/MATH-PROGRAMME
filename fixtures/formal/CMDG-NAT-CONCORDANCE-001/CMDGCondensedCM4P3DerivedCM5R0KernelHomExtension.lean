import CMDGCondensedCM4P3DerivedCM5R0KernelExtOneObstruction
import Mathlib.Algebra.Homology.DerivedCategory.Ext.ExactSequences

/-!
# CM5: exact concrete Hom extension criterion for arbitrary profinite tests

For every profinite T and every target A in the actual universe-lifted
condensed-module category, Ext¹(F_T,A) vanishes precisely if every
condensed-module morphism from the *actual Stonean presentation kernel*
K_T to A extends along K_T → F_{P(T)}.

This fully discharges the category-theoretic Ext⁰ ≃ Hom bridge.
It does NOT prove the extension property for A = ZLift or G_S, nor
any derived solidity or infinite-profinite Ext¹ vanishing.
-/

noncomputable section

universe u

open CategoryTheory Limits

namespace CMDG.CondensedCM5R0

/-- Concrete, necessary and sufficient condition for degree-one Ext
vanishing from an arbitrary free profinite condensed module. -/
theorem freeProfinite_extOne_vanishes_iff_kernel_hom_extends
    (T : Profinite.{u}) (A : Ambient) :
    (∀ e : Abelian.Ext ((Condensed.profiniteFree Coeff).obj T) A 1, e = 0) ↔
      (∀ f : stoneanPresentationKernel T ⟶ A,
        ∃ g : ((Condensed.profiniteFree Coeff).obj
          (Stonean.toProfinite.obj T.presentation)) ⟶ A,
          kernel.ι (freeStoneanPresentationMap T) ≫ g = f) := by
  rw [freeProfinite_extOne_vanishes_iff_kernel_extZero_lifts]
  constructor
  · intro h f
    obtain ⟨y, hy⟩ := h (Abelian.Ext.mk₀ f)
    refine ⟨Abelian.Ext.homEquiv₀ y, ?_⟩
    apply (Abelian.Ext.mk₀_bijective _ _).1
    simpa only [Abelian.Ext.mk₀_comp_mk₀,
      Abelian.Ext.mk₀_homEquiv₀_apply] using hy
  · intro h x
    obtain ⟨g, hg⟩ := h (Abelian.Ext.homEquiv₀ x)
    refine ⟨Abelian.Ext.mk₀ g, ?_⟩
    simpa only [Abelian.Ext.mk₀_comp_mk₀,
      Abelian.Ext.mk₀_homEquiv₀_apply] using
        congrArg Abelian.Ext.mk₀ hg

#print axioms freeProfinite_extOne_vanishes_iff_kernel_hom_extends

end CMDG.CondensedCM5R0
