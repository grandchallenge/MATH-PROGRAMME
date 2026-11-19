import CMDGCondensedCM4P3DerivedCM5R0ExtTwoGenuineSolidVanishing
import CMDGCondensedCM4P3DerivedCM5R0GSHigherExtShift
import CMDGCondensedCM4P3DerivedCM5R0GSCechSecondRelation

/-!
# CMDG CM5 — exact degree-three obstruction via double dimension shifting

For arbitrary profinite T,S in the true universe-correct category of
condensed modules, let F_T be the genuine free condensed module and
G_S the actual protected free-solid target. Let K_T be the Stonean
presentation kernel and L_T the genuine second Čech relation kernel.

The proven short exact sequence 0→L_T→F_R→K_T→0 and unconditional
Ext¹(F_R,G_S)=Ext²(F_R,G_S)=0 give an additive equivalence
Ext¹(L_T,G_S) ≃+ Ext²(K_T,G_S). Compose this with the already protected
Stonean projective-cover dimension shift
Ext²(K_T,G_S) ≃+ Ext³(F_T,G_S).

This constructs the actual additive equivalence, and proves exact
vanishing equivalence Ext³(F_T,G_S)=0 ↔ Ext¹(L_T,G_S)=0.
It does NOT claim either side vanishes, nor any higher derived
solidification or Liquid-Tensor theorem. The next substantive obligation
is to prove extension for the second relation L_T, i.e. establish
Ext¹(L_T,G_S)=0 by an independent third Čech relation construction
or equivalent exact source-locked proof.
-/

noncomputable section
universe u
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0

private abbrev GenuineGS (S : Profinite.{u}) : Ambient :=
  (Condensed.profiniteSolid CMDG.CondensedCM4P2D.R.{u}).obj S

noncomputable def secondRelationExtConnecting (T S : Profinite.{u}) :
    Abelian.Ext (stoneanCechSecondRelationKernel T) (GenuineGS S) 1 →+
    Abelian.Ext (stoneanPresentationKernel T) (GenuineGS S) 2 :=
  ((stoneanCechSecondRelationShortExact T).extClass).precomp (GenuineGS S)
    (by decide : 1 + 1 = 2)

theorem secondRelationExtConnecting_surjective (T S : Profinite.{u}) :
    Function.Surjective (secondRelationExtConnecting T S) := by
  intro e
  have hz : (Abelian.Ext.mk₀ (stoneanCechRelationToKernel T)).comp
      e (zero_add 2) = 0 := by
    exact freeSolid_extTwo_vanishes_unconditional
      (stoneanPresentationCechPairs T) S _
  obtain ⟨x, hx⟩ :=
    Abelian.Ext.contravariant_sequence_exact₃
      (stoneanCechSecondRelationShortExact T) (GenuineGS S)
      e hz (by decide : 1 + 1 = 2)
  exact ⟨x, hx⟩

theorem secondRelationExtConnecting_injective (T S : Profinite.{u}) :
    Function.Injective (secondRelationExtConnecting T S) := by
  intro x y hxy
  have hzero : secondRelationExtConnecting T S (x - y) = 0 := by
    rw [map_sub, hxy, sub_self]
  have hcomp :
      (stoneanCechSecondRelationShortExact T).extClass.comp (x - y)
        (by decide : 1 + 1 = 2) = 0 := hzero
  obtain ⟨z, hz⟩ :=
    Abelian.Ext.contravariant_sequence_exact₁
      (stoneanCechSecondRelationShortExact T) (GenuineGS S)
      (x - y) (by decide : 1 + 1 = 2) hcomp
  have hz0 : z = 0 :=
    freeProfinite_extOne_genuineSolid_vanishes
      (stoneanPresentationCechPairs T) S z
  rw [hz0] at hz
  have hsub : x - y = 0 := by simpa using hz.symm
  exact sub_eq_zero.mp hsub

noncomputable def secondRelationExtAddEquiv (T S : Profinite.{u}) :
    Abelian.Ext (stoneanCechSecondRelationKernel T) (GenuineGS S) 1 ≃+
    Abelian.Ext (stoneanPresentationKernel T) (GenuineGS S) 2 :=
  AddEquiv.ofBijective
    (secondRelationExtConnecting T S)
    ⟨secondRelationExtConnecting_injective T S,
      secondRelationExtConnecting_surjective T S⟩

/-- The concrete canonical double dimension shift is an additive
 equivalence on the genuine condensed module Ext groups. -/
noncomputable def secondRelationExtOneToFreeExtThreeAddEquiv
    (T S : Profinite.{u}) :
    Abelian.Ext (stoneanCechSecondRelationKernel T) (GenuineGS S) 1 ≃+
    Abelian.Ext ((Condensed.profiniteFree Coeff).obj T)
      (GenuineGS S) 3 :=
  (secondRelationExtAddEquiv T S).trans
    (stoneanKernelHigherExtAddEquiv T (GenuineGS S) 1)

theorem freeSolid_extThree_vanishes_iff_secondRelation_extOne_vanishes
    (T S : Profinite.{u}) :
    (∀ e : Abelian.Ext
      ((Condensed.profiniteFree Coeff).obj T) (GenuineGS S) 3, e = 0) ↔
    (∀ e : Abelian.Ext
      (stoneanCechSecondRelationKernel T) (GenuineGS S) 1, e = 0) := by
  have h1 := freeSolid_extHigher_vanishes_iff_stoneanKernel_extLower_vanishes
    T S 1
  constructor
  · intro h e
    have hkernel : ∀ x : Abelian.Ext (stoneanPresentationKernel T)
      (GenuineGS S) 2, x = 0 := h1.mp (by simpa using h)
    apply secondRelationExtConnecting_injective T S
    calc
      secondRelationExtConnecting T S e = 0 := hkernel _
      _ = secondRelationExtConnecting T S 0 := (map_zero _).symm
  · intro h e
    apply h1.mpr
    intro x
    obtain ⟨a, rfl⟩ := secondRelationExtConnecting_surjective T S x
    rw [h a]
    exact map_zero _

#print axioms secondRelationExtOneToFreeExtThreeAddEquiv
#print axioms secondRelationExtConnecting_surjective
#print axioms secondRelationExtConnecting_injective
#print axioms freeSolid_extThree_vanishes_iff_secondRelation_extOne_vanishes
end CMDG.CondensedCM5R0
