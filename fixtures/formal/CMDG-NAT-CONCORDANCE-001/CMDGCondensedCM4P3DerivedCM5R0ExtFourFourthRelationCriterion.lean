import CMDGCondensedCM4P3DerivedCM5R0ExtFourRelationReduction
import CMDGCondensedCM4P3DerivedCM5R0GlobalThirdRelationEpi
import Mathlib.Algebra.Homology.DerivedCategory.Ext.ExactSequences

/-!
# CM5 Ext⁴: exact next kernel and extension criterion

The genuine global epimorphism
  F_{P(T)^4_T} → M_T
has kernel N_T. The degree-four obstruction is precisely
extension of every N_T → G_S over F_{P(T)^4_T}.
No Ext⁴ vanishing, fifth-order Čech exactness or scalar H⁴
potential is claimed here.
-/

noncomputable section
universe u
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0

noncomputable abbrev stoneanCechFourthRelationKernel
    (T : Profinite.{u}) : Ambient :=
  kernel (stoneanCechFourthToThirdRelation T)

noncomputable abbrev stoneanCechFourthRelationShortComplex
    (T : Profinite.{u}) : ShortComplex Ambient :=
  ShortComplex.mk
    (kernel.ι (stoneanCechFourthToThirdRelation T))
    (stoneanCechFourthToThirdRelation T)
    (kernel.condition (stoneanCechFourthToThirdRelation T))

theorem stoneanCechFourthRelationShortExact (T : Profinite.{u}) :
    (stoneanCechFourthRelationShortComplex T).ShortExact := by
  letI : Epi (stoneanCechFourthToThirdRelation T) :=
    stoneanCechFourthToThirdRelation_epi_unconditional T
  exact {exact := ShortComplex.exact_kernel _}

/-- Ext¹(M_T,G_S)=0 if and only if all actual fourth-relation Hom
maps extend across the genuine kernel inclusion. -/
theorem fourthRelation_extOne_vanishes_iff_hom_extends
    (T S : Profinite.{u}) :
    (∀ e : Abelian.Ext (stoneanCechThirdRelationKernel T)
      (underivedObject S) 1, e = 0) ↔
    (∀ f : stoneanCechFourthRelationKernel T ⟶ underivedObject S,
      ∃ g : ((Condensed.profiniteFree Coeff).obj
        (stoneanPresentationCechQuadruples T)) ⟶ underivedObject S,
        kernel.ι (stoneanCechFourthToThirdRelation T) ≫ g = f) := by
  let hS := stoneanCechFourthRelationShortExact T
  constructor
  · intro h f
    have hzero :
        hS.extClass.comp (Abelian.Ext.mk₀ f)
          (by decide : 1 + 0 = 1) = 0 := h _
    obtain ⟨y, hy⟩ :=
      Abelian.Ext.contravariant_sequence_exact₁
        hS (underivedObject S) (Abelian.Ext.mk₀ f)
        (by decide : 1 + 0 = 1) hzero
    refine ⟨Abelian.Ext.homEquiv₀ y, ?_⟩
    apply (Abelian.Ext.mk₀_bijective _ _).1
    calc
      Abelian.Ext.mk₀
          (kernel.ι (stoneanCechFourthToThirdRelation T) ≫
            Abelian.Ext.homEquiv₀ y) =
        (Abelian.Ext.mk₀ (kernel.ι (stoneanCechFourthToThirdRelation T))).comp
          (Abelian.Ext.mk₀ (Abelian.Ext.homEquiv₀ y))
          (zero_add 0) :=
          (Abelian.Ext.mk₀_comp_mk₀ _ _).symm
      _ = (Abelian.Ext.mk₀
            (kernel.ι (stoneanCechFourthToThirdRelation T))).comp
              y (zero_add 0) := by
          rw [Abelian.Ext.mk₀_homEquiv₀_apply]
      _ = Abelian.Ext.mk₀ f := hy
  · intro h e
    have hFree :
        ∀ x : Abelian.Ext
          ((Condensed.profiniteFree Coeff).obj
            (stoneanPresentationCechQuadruples T))
          (underivedObject S) 1, x = 0 :=
      freeProfinite_extOne_genuineSolid_vanishes
        (stoneanPresentationCechQuadruples T) S
    have hzero :
        (Abelian.Ext.mk₀ (stoneanCechFourthToThirdRelation T)).comp
          e (zero_add 1) = 0 := hFree _
    obtain ⟨x, hx⟩ :=
      Abelian.Ext.contravariant_sequence_exact₃
        hS (underivedObject S) e hzero
        (by decide : 1 + 0 = 1)
    obtain ⟨g, hg⟩ := h (Abelian.Ext.homEquiv₀ x)
    have hmk :
        (Abelian.Ext.mk₀
          (kernel.ι (stoneanCechFourthToThirdRelation T))).comp
            (Abelian.Ext.mk₀ g) (zero_add 0) = x := by
      simpa only [Abelian.Ext.mk₀_comp_mk₀,
        Abelian.Ext.mk₀_homEquiv₀_apply] using
          congrArg Abelian.Ext.mk₀ hg
    have hconn : hS.extClass.comp x (by decide : 1 + 0 = 1) = 0 := by
      rw [← hmk]
      exact hS.extClass_comp_assoc (Abelian.Ext.mk₀ g)
    exact hx.symm.trans hconn

/-- The precise unrestricted Ext⁴ obligation; this is a genuine
fourth-relation Hom extension criterion, with no hidden assumption
that the required lift always exists. -/
theorem freeSolid_extFour_vanishes_iff_fourthRelation_hom_extends
    (T S : Profinite.{u}) :
    (∀ e : Abelian.Ext ((Condensed.profiniteFree Coeff).obj T)
      (underivedObject S) 4, e = 0) ↔
    (∀ f : stoneanCechFourthRelationKernel T ⟶ underivedObject S,
      ∃ g : ((Condensed.profiniteFree Coeff).obj
        (stoneanPresentationCechQuadruples T)) ⟶ underivedObject S,
        kernel.ι (stoneanCechFourthToThirdRelation T) ≫ g = f) := by
  exact (freeSolid_extFour_vanishes_iff_thirdRelation_extOne_vanishes
    T S).trans (fourthRelation_extOne_vanishes_iff_hom_extends T S)

#print axioms stoneanCechFourthRelationShortExact
#print axioms fourthRelation_extOne_vanishes_iff_hom_extends
#print axioms freeSolid_extFour_vanishes_iff_fourthRelation_hom_extends
end CMDG.CondensedCM5R0
