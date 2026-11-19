import CMDGCondensedCM4P3DerivedCM5R0ExtThreeGenuineSolidVanishing
import CMDGCondensedCM4P3DerivedCM5R0GSHigherExtShift
import Mathlib.Algebra.Homology.DerivedCategory.Ext.ExactSequences

/-!
# CM5 degree four: actual third-relation obstruction (not vanishing)

Three honest connecting maps identify Ext⁴(F_T,G_S) with
Ext¹(M_T,G_S), where M_T is the genuine third Čech relation
kernel of F_{P(T)^3_T}→L_T. No higher cohomological acyclicity,
fifth Čech epi or Ext⁴ vanishing is assumed.
-/

noncomputable section
universe u
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0

private abbrev FourGS (S : Profinite.{u}) : Ambient := underivedObject S

noncomputable def thirdRelationExtConnecting (T S : Profinite.{u}) :
    Abelian.Ext (stoneanCechThirdRelationKernel T) (FourGS S) 1 →+
    Abelian.Ext (stoneanCechSecondRelationKernel T) (FourGS S) 2 :=
  ((stoneanCechThirdRelationShortExact T).extClass).precomp
    (FourGS S) (by decide : 1 + 1 = 2)

theorem thirdRelationExtConnecting_surjective (T S : Profinite.{u}) :
    Function.Surjective (thirdRelationExtConnecting T S) := by
  intro e
  have hz : (Abelian.Ext.mk₀ (stoneanCechTripleToSecondRelation T)).comp
      e (zero_add 2) = 0 := by
    exact freeSolid_extTwo_vanishes_unconditional
      (stoneanPresentationCechTriples T) S _
  obtain ⟨x, hx⟩ :=
    Abelian.Ext.contravariant_sequence_exact₃
      (stoneanCechThirdRelationShortExact T) (FourGS S)
      e hz (by decide : 1 + 1 = 2)
  exact ⟨x, hx⟩

theorem thirdRelationExtConnecting_injective (T S : Profinite.{u}) :
    Function.Injective (thirdRelationExtConnecting T S) := by
  intro x y hxy
  have hzero : thirdRelationExtConnecting T S (x - y) = 0 := by
    rw [map_sub, hxy, sub_self]
  have hcomp :
      (stoneanCechThirdRelationShortExact T).extClass.comp (x - y)
        (by decide : 1 + 1 = 2) = 0 := hzero
  obtain ⟨z, hz⟩ :=
    Abelian.Ext.contravariant_sequence_exact₁
      (stoneanCechThirdRelationShortExact T) (FourGS S)
      (x - y) (by decide : 1 + 1 = 2) hcomp
  have hz0 : z = 0 :=
    freeProfinite_extOne_genuineSolid_vanishes
      (stoneanPresentationCechTriples T) S z
  rw [hz0] at hz
  have hsub : x - y = 0 := by simpa using hz.symm
  exact sub_eq_zero.mp hsub

noncomputable def thirdRelationExtAddEquiv (T S : Profinite.{u}) :
    Abelian.Ext (stoneanCechThirdRelationKernel T) (FourGS S) 1 ≃+
    Abelian.Ext (stoneanCechSecondRelationKernel T) (FourGS S) 2 :=
  AddEquiv.ofBijective (thirdRelationExtConnecting T S)
    ⟨thirdRelationExtConnecting_injective T S,
      thirdRelationExtConnecting_surjective T S⟩

noncomputable def secondRelationHigherConnecting (T S : Profinite.{u}) :
    Abelian.Ext (stoneanCechSecondRelationKernel T) (FourGS S) 2 →+
    Abelian.Ext (stoneanPresentationKernel T) (FourGS S) 3 :=
  ((stoneanCechSecondRelationShortExact T).extClass).precomp
    (FourGS S) (by decide : 1 + 2 = 3)

theorem secondRelationHigherConnecting_surjective (T S : Profinite.{u}) :
    Function.Surjective (secondRelationHigherConnecting T S) := by
  intro e
  have hz : (Abelian.Ext.mk₀ (stoneanCechRelationToKernel T)).comp
      e (zero_add 3) = 0 := by
    exact freeSolid_extThree_vanishes_unconditional
      (stoneanPresentationCechPairs T) S _
  obtain ⟨x, hx⟩ :=
    Abelian.Ext.contravariant_sequence_exact₃
      (stoneanCechSecondRelationShortExact T) (FourGS S)
      e hz (by decide : 1 + 2 = 3)
  exact ⟨x, hx⟩

theorem secondRelationHigherConnecting_injective (T S : Profinite.{u}) :
    Function.Injective (secondRelationHigherConnecting T S) := by
  intro x y hxy
  have hzero : secondRelationHigherConnecting T S (x - y) = 0 := by
    rw [map_sub, hxy, sub_self]
  have hcomp :
      (stoneanCechSecondRelationShortExact T).extClass.comp (x - y)
        (by decide : 1 + 2 = 3) = 0 := hzero
  obtain ⟨z, hz⟩ :=
    Abelian.Ext.contravariant_sequence_exact₁
      (stoneanCechSecondRelationShortExact T) (FourGS S)
      (x - y) (by decide : 1 + 2 = 3) hcomp
  have hz0 : z = 0 :=
    freeSolid_extTwo_vanishes_unconditional
      (stoneanPresentationCechPairs T) S z
  rw [hz0] at hz
  have hsub : x - y = 0 := by simpa using hz.symm
  exact sub_eq_zero.mp hsub

noncomputable def secondRelationHigherExtAddEquiv (T S : Profinite.{u}) :
    Abelian.Ext (stoneanCechSecondRelationKernel T) (FourGS S) 2 ≃+
    Abelian.Ext (stoneanPresentationKernel T) (FourGS S) 3 :=
  AddEquiv.ofBijective (secondRelationHigherConnecting T S)
    ⟨secondRelationHigherConnecting_injective T S,
      secondRelationHigherConnecting_surjective T S⟩

/-- An actual categorical additive equivalence, NOT an assertion of
unconditional degree-four vanishing. -/
noncomputable def thirdRelationExtOneToFreeExtFourAddEquiv
    (T S : Profinite.{u}) :
    Abelian.Ext (stoneanCechThirdRelationKernel T) (FourGS S) 1 ≃+
    Abelian.Ext ((Condensed.profiniteFree Coeff).obj T)
      (FourGS S) 4 :=
  ((thirdRelationExtAddEquiv T S).trans
    (secondRelationHigherExtAddEquiv T S)).trans
      (stoneanKernelHigherExtAddEquiv T (FourGS S) 2)

theorem freeSolid_extFour_vanishes_iff_thirdRelation_extOne_vanishes
    (T S : Profinite.{u}) :
    (∀ e : Abelian.Ext ((Condensed.profiniteFree Coeff).obj T)
       (FourGS S) 4, e = 0) ↔
    (∀ e : Abelian.Ext (stoneanCechThirdRelationKernel T)
       (FourGS S) 1, e = 0) := by
  let e := thirdRelationExtOneToFreeExtFourAddEquiv T S
  constructor
  · intro h x
    apply e.injective
    calc
      e x = 0 := h _
      _ = e 0 := (map_zero e).symm
  · intro h x
    obtain ⟨y, rfl⟩ := e.surjective x
    rw [h y]
    exact map_zero e

#print axioms thirdRelationExtOneToFreeExtFourAddEquiv
#print axioms freeSolid_extFour_vanishes_iff_thirdRelation_extOne_vanishes
end CMDG.CondensedCM5R0
