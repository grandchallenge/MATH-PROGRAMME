import CMDGCondensedCM4P3DerivedCM5R0ExtThreeSecondRelationReduction
import Mathlib.Algebra.Homology.DerivedCategory.Ext.ExactSequences

/-!
# CMDG CM5 — the genuine third Čech relation and exact Ext³ criterion

For arbitrary profinite T, take the actual Čech triple-to-second-relation
epimorphism F_Q→L_T, protected in CM5 by global categorical exactness.
Its kernel M_T defines the genuine short exact sequence
0→M_T→F_Q→L_T→0, with no surrogate finite relation or formal quotient.

The protected Ext¹(F_Q,G_S)=0 and the actual derived-category long
exact sequence give Ext¹(L_T,G_S)=0 if and only if every map M_T→G_S
extends along M_T↪F_Q. Combined with the separately proved double
dimension-shift equivalence, this identifies the exact Ext³ obstruction
for the genuine free condensed module and actual free-solid target.

This proves a short exact sequence and equivalence of vanishing
conditions. It does NOT prove the extension condition, Ext³ vanishing,
higher derived solidity, or the Liquid-Tensor capstone.
-/

noncomputable section
universe u
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0

noncomputable abbrev stoneanCechThirdRelationKernel
    (T : Profinite.{u}) : Ambient :=
  kernel (stoneanCechTripleToSecondRelation T)

noncomputable abbrev stoneanCechThirdRelationShortComplex
    (T : Profinite.{u}) : ShortComplex Ambient :=
  ShortComplex.mk
    (kernel.ι (stoneanCechTripleToSecondRelation T))
    (stoneanCechTripleToSecondRelation T)
    (kernel.condition (stoneanCechTripleToSecondRelation T))

theorem stoneanCechThirdRelationShortExact (T : Profinite.{u}) :
    (stoneanCechThirdRelationShortComplex T).ShortExact := by
  letI : Epi (stoneanCechTripleToSecondRelation T) :=
    stoneanCechTripleToSecondRelation_epi_unconditional T
  exact {exact := ShortComplex.exact_kernel _}

private abbrev ThirdGS (S : Profinite.{u}) : Ambient :=
  (Condensed.profiniteSolid CMDG.CondensedCM4P2D.R.{u}).obj S

theorem thirdRelation_extOne_vanishes_iff_hom_extends
    (T S : Profinite.{u}) :
    (∀ e : Abelian.Ext (stoneanCechSecondRelationKernel T)
      (ThirdGS S) 1, e = 0) ↔
    (∀ f : stoneanCechThirdRelationKernel T ⟶ ThirdGS S,
      ∃ g : ((Condensed.profiniteFree Coeff).obj
        (stoneanPresentationCechTriples T)) ⟶ ThirdGS S,
        kernel.ι (stoneanCechTripleToSecondRelation T) ≫ g = f) := by
  let hS := stoneanCechThirdRelationShortExact T
  constructor
  · intro h f
    have hzero :
        hS.extClass.comp (Abelian.Ext.mk₀ f)
          (by decide : 1 + 0 = 1) = 0 := h _
    obtain ⟨y, hy⟩ :=
      Abelian.Ext.contravariant_sequence_exact₁
        hS (ThirdGS S) (Abelian.Ext.mk₀ f)
        (by decide : 1 + 0 = 1) hzero
    refine ⟨Abelian.Ext.homEquiv₀ y, ?_⟩
    apply (Abelian.Ext.mk₀_bijective _ _).1
    calc
      Abelian.Ext.mk₀
          (kernel.ι (stoneanCechTripleToSecondRelation T) ≫
            Abelian.Ext.homEquiv₀ y) =
        (Abelian.Ext.mk₀ (kernel.ι (stoneanCechTripleToSecondRelation T))).comp
          (Abelian.Ext.mk₀ (Abelian.Ext.homEquiv₀ y))
          (zero_add 0) :=
          (Abelian.Ext.mk₀_comp_mk₀ _ _).symm
      _ = (Abelian.Ext.mk₀
            (kernel.ι (stoneanCechTripleToSecondRelation T))).comp
              y (zero_add 0) := by
          rw [Abelian.Ext.mk₀_homEquiv₀_apply]
      _ = Abelian.Ext.mk₀ f := hy
  · intro h e
    have hFree :
        ∀ x : Abelian.Ext
          ((Condensed.profiniteFree Coeff).obj
            (stoneanPresentationCechTriples T)) (ThirdGS S) 1, x = 0 :=
      freeProfinite_extOne_genuineSolid_vanishes
        (stoneanPresentationCechTriples T) S
    have hzero :
        (Abelian.Ext.mk₀ (stoneanCechTripleToSecondRelation T)).comp
          e (zero_add 1) = 0 := hFree _
    obtain ⟨x, hx⟩ :=
      Abelian.Ext.contravariant_sequence_exact₃
        hS (ThirdGS S) e hzero (by decide : 1 + 0 = 1)
    obtain ⟨g, hg⟩ := h (Abelian.Ext.homEquiv₀ x)
    have hmk :
        (Abelian.Ext.mk₀
          (kernel.ι (stoneanCechTripleToSecondRelation T))).comp
            (Abelian.Ext.mk₀ g) (zero_add 0) = x := by
      simpa only [Abelian.Ext.mk₀_comp_mk₀,
        Abelian.Ext.mk₀_homEquiv₀_apply] using
          congrArg Abelian.Ext.mk₀ hg
    have hconn : hS.extClass.comp x (by decide : 1 + 0 = 1) = 0 := by
      rw [← hmk]
      exact hS.extClass_comp_assoc (Abelian.Ext.mk₀ g)
    exact hx.symm.trans hconn

theorem freeSolid_extThree_vanishes_iff_thirdRelation_hom_extends
    (T S : Profinite.{u}) :
    (∀ e : Abelian.Ext ((Condensed.profiniteFree Coeff).obj T)
      (ThirdGS S) 3, e = 0) ↔
    (∀ f : stoneanCechThirdRelationKernel T ⟶ ThirdGS S,
      ∃ g : ((Condensed.profiniteFree Coeff).obj
        (stoneanPresentationCechTriples T)) ⟶ ThirdGS S,
        kernel.ι (stoneanCechTripleToSecondRelation T) ≫ g = f) := by
  exact (freeSolid_extThree_vanishes_iff_secondRelation_extOne_vanishes
    T S).trans (thirdRelation_extOne_vanishes_iff_hom_extends T S)

#print axioms stoneanCechThirdRelationShortExact
#print axioms thirdRelation_extOne_vanishes_iff_hom_extends
#print axioms freeSolid_extThree_vanishes_iff_thirdRelation_hom_extends
end CMDG.CondensedCM5R0
