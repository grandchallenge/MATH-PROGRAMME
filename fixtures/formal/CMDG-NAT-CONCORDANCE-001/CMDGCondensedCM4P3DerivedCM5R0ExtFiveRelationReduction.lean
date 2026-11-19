import CMDGCondensedCM4P3DerivedCM5R0ExtFourGenuineSolidVanishing
import CMDGCondensedCM4P3DerivedCM5R0GlobalFourthRelationEpi
import CMDGCondensedCM4P3DerivedCM5R0ExtFourFourthRelationCriterion
import Mathlib.Algebra.Homology.DerivedCategory.Ext.ExactSequences

/-!
# CMDG CM5: structural exact degree-five obstruction, not vanishing

The genuine Čech short exact sequences and the *already checked*
Ext¹..Ext⁴ free-solid vanishings yield three dimension shifts
Ext¹(N_T,G_S) → Ext²(M_T,G_S) → Ext³(L_T,G_S) →
Ext⁴(K_T,G_S), followed by the Stonean kernel shift
Ext⁴(K_T,G_S) → Ext⁵(F_T,G_S).
The source and coefficient object are the actual protected ones.

Prove a short exact sequence involving the FIFTH relation, its
extension criterion, and exact equivalence with Ext⁵ vanishing.
This does NOT assert Ext⁵ vanishes.
-/

noncomputable section
universe u
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0

noncomputable abbrev stoneanCechFifthRelationKernel
    (T : Profinite.{u}) : Ambient :=
  kernel (stoneanCechFifthToFourthRelation T)

noncomputable abbrev stoneanCechFifthRelationShortComplex
    (T : Profinite.{u}) : ShortComplex Ambient :=
  ShortComplex.mk
    (kernel.ι (stoneanCechFifthToFourthRelation T))
    (stoneanCechFifthToFourthRelation T)
    (kernel.condition (stoneanCechFifthToFourthRelation T))

theorem stoneanCechFifthRelationShortExact (T : Profinite.{u}) :
    (stoneanCechFifthRelationShortComplex T).ShortExact := by
  letI : Epi (stoneanCechFifthToFourthRelation T) :=
    stoneanCechFifthToFourthRelation_epi_unconditional T
  exact {exact := ShortComplex.exact_kernel _}

noncomputable def fourthRelationExtFiveConnecting (T S : Profinite.{u}) :
    Abelian.Ext (stoneanCechFourthRelationKernel T) (underivedObject S) 1 →+
    Abelian.Ext (stoneanCechThirdRelationKernel T) (underivedObject S) 2 :=
  ((stoneanCechFourthRelationShortExact T).extClass).precomp
    (underivedObject S) (by decide : 1 + 1 = 2)

theorem fourthRelationExtFiveConnecting_surjective (T S : Profinite.{u}) :
    Function.Surjective (fourthRelationExtFiveConnecting T S) := by
  intro e
  have hz : (Abelian.Ext.mk₀ (stoneanCechFourthToThirdRelation T)).comp
      e (zero_add 2) = 0 := by
    exact freeSolid_extTwo_vanishes_unconditional
      (stoneanPresentationCechQuadruples T) S _
  obtain ⟨x, hx⟩ :=
    Abelian.Ext.contravariant_sequence_exact₃
      (stoneanCechFourthRelationShortExact T) (underivedObject S)
      e hz (by decide : 1 + 1 = 2)
  exact ⟨x, hx⟩

theorem fourthRelationExtFiveConnecting_injective (T S : Profinite.{u}) :
    Function.Injective (fourthRelationExtFiveConnecting T S) := by
  intro x y hxy
  have hzero : fourthRelationExtFiveConnecting T S (x - y) = 0 := by
    rw [map_sub, hxy, sub_self]
  have hcomp :
      (stoneanCechFourthRelationShortExact T).extClass.comp (x - y)
        (by decide : 1 + 1 = 2) = 0 := hzero
  obtain ⟨z, hz⟩ :=
    Abelian.Ext.contravariant_sequence_exact₁
      (stoneanCechFourthRelationShortExact T) (underivedObject S)
      (x - y) (by decide : 1 + 1 = 2) hcomp
  have hz0 : z = 0 :=
    freeProfinite_extOne_genuineSolid_vanishes
      (stoneanPresentationCechQuadruples T) S z
  rw [hz0] at hz
  have hsub : x - y = 0 := by simpa using hz.symm
  exact sub_eq_zero.mp hsub

noncomputable def fourthRelationExtFiveAddEquiv (T S : Profinite.{u}) :
    Abelian.Ext (stoneanCechFourthRelationKernel T) (underivedObject S) 1 ≃+
    Abelian.Ext (stoneanCechThirdRelationKernel T) (underivedObject S) 2 :=
  AddEquiv.ofBijective (fourthRelationExtFiveConnecting T S)
    ⟨fourthRelationExtFiveConnecting_injective T S,
      fourthRelationExtFiveConnecting_surjective T S⟩

noncomputable def thirdRelationExtFiveConnecting (T S : Profinite.{u}) :
    Abelian.Ext (stoneanCechThirdRelationKernel T) (underivedObject S) 2 →+
    Abelian.Ext (stoneanCechSecondRelationKernel T) (underivedObject S) 3 :=
  ((stoneanCechThirdRelationShortExact T).extClass).precomp
    (underivedObject S) (by decide : 1 + 2 = 3)

theorem thirdRelationExtFiveConnecting_surjective (T S : Profinite.{u}) :
    Function.Surjective (thirdRelationExtFiveConnecting T S) := by
  intro e
  have hz : (Abelian.Ext.mk₀ (stoneanCechTripleToSecondRelation T)).comp
      e (zero_add 3) = 0 := by
    exact freeSolid_extThree_vanishes_unconditional
      (stoneanPresentationCechTriples T) S _
  obtain ⟨x, hx⟩ :=
    Abelian.Ext.contravariant_sequence_exact₃
      (stoneanCechThirdRelationShortExact T) (underivedObject S)
      e hz (by decide : 1 + 2 = 3)
  exact ⟨x, hx⟩

theorem thirdRelationExtFiveConnecting_injective (T S : Profinite.{u}) :
    Function.Injective (thirdRelationExtFiveConnecting T S) := by
  intro x y hxy
  have hzero : thirdRelationExtFiveConnecting T S (x - y) = 0 := by
    rw [map_sub, hxy, sub_self]
  have hcomp :
      (stoneanCechThirdRelationShortExact T).extClass.comp (x - y)
        (by decide : 1 + 2 = 3) = 0 := hzero
  obtain ⟨z, hz⟩ :=
    Abelian.Ext.contravariant_sequence_exact₁
      (stoneanCechThirdRelationShortExact T) (underivedObject S)
      (x - y) (by decide : 1 + 2 = 3) hcomp
  have hz0 : z = 0 :=
    freeSolid_extTwo_vanishes_unconditional
      (stoneanPresentationCechTriples T) S z
  rw [hz0] at hz
  have hsub : x - y = 0 := by simpa using hz.symm
  exact sub_eq_zero.mp hsub

noncomputable def thirdRelationExtFiveAddEquiv (T S : Profinite.{u}) :
    Abelian.Ext (stoneanCechThirdRelationKernel T) (underivedObject S) 2 ≃+
    Abelian.Ext (stoneanCechSecondRelationKernel T) (underivedObject S) 3 :=
  AddEquiv.ofBijective (thirdRelationExtFiveConnecting T S)
    ⟨thirdRelationExtFiveConnecting_injective T S,
      thirdRelationExtFiveConnecting_surjective T S⟩

noncomputable def secondRelationExtFiveConnecting (T S : Profinite.{u}) :
    Abelian.Ext (stoneanCechSecondRelationKernel T) (underivedObject S) 3 →+
    Abelian.Ext (stoneanPresentationKernel T) (underivedObject S) 4 :=
  ((stoneanCechSecondRelationShortExact T).extClass).precomp
    (underivedObject S) (by decide : 1 + 3 = 4)

theorem secondRelationExtFiveConnecting_surjective (T S : Profinite.{u}) :
    Function.Surjective (secondRelationExtFiveConnecting T S) := by
  intro e
  have hz : (Abelian.Ext.mk₀ (stoneanCechRelationToKernel T)).comp
      e (zero_add 4) = 0 := by
    exact freeSolid_extFour_vanishes_unconditional
      (stoneanPresentationCechPairs T) S _
  obtain ⟨x, hx⟩ :=
    Abelian.Ext.contravariant_sequence_exact₃
      (stoneanCechSecondRelationShortExact T) (underivedObject S)
      e hz (by decide : 1 + 3 = 4)
  exact ⟨x, hx⟩

theorem secondRelationExtFiveConnecting_injective (T S : Profinite.{u}) :
    Function.Injective (secondRelationExtFiveConnecting T S) := by
  intro x y hxy
  have hzero : secondRelationExtFiveConnecting T S (x - y) = 0 := by
    rw [map_sub, hxy, sub_self]
  have hcomp :
      (stoneanCechSecondRelationShortExact T).extClass.comp (x - y)
        (by decide : 1 + 3 = 4) = 0 := hzero
  obtain ⟨z, hz⟩ :=
    Abelian.Ext.contravariant_sequence_exact₁
      (stoneanCechSecondRelationShortExact T) (underivedObject S)
      (x - y) (by decide : 1 + 3 = 4) hcomp
  have hz0 : z = 0 :=
    freeSolid_extThree_vanishes_unconditional
      (stoneanPresentationCechPairs T) S z
  rw [hz0] at hz
  have hsub : x - y = 0 := by simpa using hz.symm
  exact sub_eq_zero.mp hsub

noncomputable def secondRelationExtFiveAddEquiv (T S : Profinite.{u}) :
    Abelian.Ext (stoneanCechSecondRelationKernel T) (underivedObject S) 3 ≃+
    Abelian.Ext (stoneanPresentationKernel T) (underivedObject S) 4 :=
  AddEquiv.ofBijective (secondRelationExtFiveConnecting T S)
    ⟨secondRelationExtFiveConnecting_injective T S,
      secondRelationExtFiveConnecting_surjective T S⟩


/-- Exact four-stage additive equivalence: genuine Ext¹ of the
fourth Čech relation is genuine Ext⁵ of the original free module. -/
noncomputable def fourthRelationExtOneToFreeExtFiveAddEquiv
    (T S : Profinite.{u}) :
    Abelian.Ext (stoneanCechFourthRelationKernel T)
      (underivedObject S) 1 ≃+
    Abelian.Ext ((Condensed.profiniteFree Coeff).obj T)
      (underivedObject S) 5 :=
  (((fourthRelationExtFiveAddEquiv T S).trans
    (thirdRelationExtFiveAddEquiv T S)).trans
      (secondRelationExtFiveAddEquiv T S)).trans
        (stoneanKernelHigherExtAddEquiv T (underivedObject S) 3)

/-- Ext⁵(F_T,G_S)=0 iff Ext¹(N_T,G_S)=0, where N_T is the
genuine fourth Čech relation. No vanishing is asserted here. -/
theorem freeSolid_extFive_vanishes_iff_fourthRelation_extOne_vanishes
    (T S : Profinite.{u}) :
    (∀ e : Abelian.Ext ((Condensed.profiniteFree Coeff).obj T)
      (underivedObject S) 5, e = 0) ↔
    (∀ e : Abelian.Ext (stoneanCechFourthRelationKernel T)
      (underivedObject S) 1, e = 0) := by
  let equiv := fourthRelationExtOneToFreeExtFiveAddEquiv T S
  constructor
  · intro h x
    apply equiv.injective
    calc
      equiv x = 0 := h _
      _ = equiv 0 := (map_zero equiv).symm
  · intro h x
    obtain ⟨y, rfl⟩ := equiv.surjective x
    rw [h y]
    exact map_zero equiv

theorem fifthRelation_extOne_vanishes_iff_hom_extends
    (T S : Profinite.{u}) :
    (∀ e : Abelian.Ext (stoneanCechFourthRelationKernel T)
      (underivedObject S) 1, e = 0) ↔
    (∀ f : stoneanCechFifthRelationKernel T ⟶ underivedObject S,
      ∃ g : ((Condensed.profiniteFree Coeff).obj
        (stoneanCechExplicitQuintupleProfinite T)) ⟶ underivedObject S,
        kernel.ι (stoneanCechFifthToFourthRelation T) ≫ g = f) := by
  let hS := stoneanCechFifthRelationShortExact T
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
          (kernel.ι (stoneanCechFifthToFourthRelation T) ≫
            Abelian.Ext.homEquiv₀ y) =
        (Abelian.Ext.mk₀ (kernel.ι (stoneanCechFifthToFourthRelation T))).comp
          (Abelian.Ext.mk₀ (Abelian.Ext.homEquiv₀ y))
          (zero_add 0) :=
          (Abelian.Ext.mk₀_comp_mk₀ _ _).symm
      _ = (Abelian.Ext.mk₀
            (kernel.ι (stoneanCechFifthToFourthRelation T))).comp
              y (zero_add 0) := by
          rw [Abelian.Ext.mk₀_homEquiv₀_apply]
      _ = Abelian.Ext.mk₀ f := hy
  · intro h e
    have hFree :
        ∀ x : Abelian.Ext
          ((Condensed.profiniteFree Coeff).obj
            (stoneanCechExplicitQuintupleProfinite T))
          (underivedObject S) 1, x = 0 :=
      freeProfinite_extOne_genuineSolid_vanishes
        (stoneanCechExplicitQuintupleProfinite T) S
    have hzero :
        (Abelian.Ext.mk₀ (stoneanCechFifthToFourthRelation T)).comp
          e (zero_add 1) = 0 := hFree _
    obtain ⟨x, hx⟩ :=
      Abelian.Ext.contravariant_sequence_exact₃
        hS (underivedObject S) e hzero
        (by decide : 1 + 0 = 1)
    obtain ⟨g, hg⟩ := h (Abelian.Ext.homEquiv₀ x)
    have hmk :
        (Abelian.Ext.mk₀
          (kernel.ι (stoneanCechFifthToFourthRelation T))).comp
            (Abelian.Ext.mk₀ g) (zero_add 0) = x := by
      simpa only [Abelian.Ext.mk₀_comp_mk₀,
        Abelian.Ext.mk₀_homEquiv₀_apply] using
          congrArg Abelian.Ext.mk₀ hg
    have hconn : hS.extClass.comp x (by decide : 1 + 0 = 1) = 0 := by
      rw [← hmk]
      exact hS.extClass_comp_assoc (Abelian.Ext.mk₀ g)
    exact hx.symm.trans hconn

/-- The genuine degree-five obstruction: extend ALL morphisms
from the actual fifth-relation kernel across its inclusion in
the fifth free condensed Čech term. -/
theorem freeSolid_extFive_vanishes_iff_fifthRelation_hom_extends
    (T S : Profinite.{u}) :
    (∀ e : Abelian.Ext ((Condensed.profiniteFree Coeff).obj T)
      (underivedObject S) 5, e = 0) ↔
    (∀ f : stoneanCechFifthRelationKernel T ⟶ underivedObject S,
      ∃ g : ((Condensed.profiniteFree Coeff).obj
        (stoneanCechExplicitQuintupleProfinite T)) ⟶
        underivedObject S,
        kernel.ι (stoneanCechFifthToFourthRelation T) ≫ g = f) := by
  exact (freeSolid_extFive_vanishes_iff_fourthRelation_extOne_vanishes
    T S).trans (fifthRelation_extOne_vanishes_iff_hom_extends T S)

#print axioms fourthRelationExtOneToFreeExtFiveAddEquiv
#print axioms freeSolid_extFive_vanishes_iff_fifthRelation_hom_extends
end CMDG.CondensedCM5R0
