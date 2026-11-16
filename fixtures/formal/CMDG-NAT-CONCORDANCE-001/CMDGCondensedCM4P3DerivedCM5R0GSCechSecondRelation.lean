import CMDGCondensedCM4P3DerivedCM5R0GSHigherExtShift
import CMDGCondensedCM4P3DerivedCM5R0CechRelationEpi
import Mathlib.Algebra.Homology.DerivedCategory.Ext.ExactSequences

/-!
# CMDG CM5: the actual second Čech relation obstruction to Ext²

For profinite T, the protected Stonean cover gives K_T = ker(F_P → F_T)
and the actual Čech relation epimorphism F_R → K_T, where
R = P(T) ×_T P(T). Denote its kernel by L_T. We prove the true short
exact sequence 0 → L_T → F_R → K_T → 0.

For genuine G_S, protected CM5 proves Ext¹(F_R,G_S)=0 without a
finiteness restriction on R. The contravariant long exact Ext
sequence therefore shows Ext¹(K_T,G_S)=0 iff every morphism
L_T → G_S extends across L_T → F_R.

Composing with protected dimension-shifting, this is equivalent to
Ext²(F_T,G_S)=0, but NO extension theorem is asserted. Thus the
unfinished mathematical obligation becomes a concrete second Čech
relation extension problem in the actual category CondensedMod.

This file does not assert Ext² vanishing or derived solidity.
-/

noncomputable section

universe u

open CategoryTheory Limits

namespace CMDG.CondensedCM5R0

private abbrev GS (S : Profinite.{u}) : Ambient :=
  (Condensed.profiniteSolid CMDG.CondensedCM4P2D.R.{u}).obj S

/-- The actual second relation object, not a formal placeholder. -/
noncomputable abbrev stoneanCechSecondRelationKernel
    (T : Profinite.{u}) : Ambient :=
  kernel (stoneanCechRelationToKernel T)

/-- The precise kernel-complex of the genuine Čech relation
epimorphism from the free profinite module on the pair fiber product. -/
noncomputable abbrev stoneanCechSecondRelationShortComplex
    (T : Profinite.{u}) : ShortComplex Ambient :=
  ShortComplex.mk
    (kernel.ι (stoneanCechRelationToKernel T))
    (stoneanCechRelationToKernel T)
    (kernel.condition (stoneanCechRelationToKernel T))

/-- Effective descent proves that the second relation complex is
actually short exact, even for infinite profinite test objects. -/
theorem stoneanCechSecondRelationShortExact (T : Profinite.{u}) :
    (stoneanCechSecondRelationShortComplex T).ShortExact := by
  letI : Epi (stoneanCechRelationToKernel T) :=
    stoneanCechRelationToKernel_epi T
  exact { exact := ShortComplex.exact_kernel _ }

/-- Degree-one vanishing out of the actual Stonean presentation kernel
is exactly the extension property for second Čech relation maps into
the genuine free-solid coefficient target.

The proof uses the *already established* Ext¹(F_R,G_S)=0;
it does not falsely assume that F_R or K_T is projective.
-/
theorem stoneanKernel_extOne_vanishes_iff_secondRelation_hom_extends
    (T S : Profinite.{u}) :
    (∀ e : Abelian.Ext (stoneanPresentationKernel T) (GS S) 1, e = 0) ↔
      (∀ f : stoneanCechSecondRelationKernel T ⟶ GS S,
        ∃ g : ((Condensed.profiniteFree Coeff).obj
            (stoneanPresentationCechPairs T)) ⟶ GS S,
          kernel.ι (stoneanCechRelationToKernel T) ≫ g = f) := by
  let hS := stoneanCechSecondRelationShortExact T
  constructor
  · intro h f
    have hzero :
        hS.extClass.comp (Abelian.Ext.mk₀ f)
          (by decide : 1 + 0 = 1) = 0 := h _
    obtain ⟨y, hy⟩ :=
      Abelian.Ext.contravariant_sequence_exact₁
        hS (GS S) (Abelian.Ext.mk₀ f)
        (by decide : 1 + 0 = 1) hzero
    refine ⟨Abelian.Ext.homEquiv₀ y, ?_⟩
    apply (Abelian.Ext.mk₀_bijective _ _).1
    calc
      Abelian.Ext.mk₀
          (kernel.ι (stoneanCechRelationToKernel T) ≫
            Abelian.Ext.homEquiv₀ y) =
        (Abelian.Ext.mk₀ (kernel.ι (stoneanCechRelationToKernel T))).comp
          (Abelian.Ext.mk₀ (Abelian.Ext.homEquiv₀ y))
          (zero_add 0) :=
          (Abelian.Ext.mk₀_comp_mk₀ _ _).symm
      _ = (Abelian.Ext.mk₀
            (kernel.ι (stoneanCechRelationToKernel T))).comp
              y (zero_add 0) := by
          rw [Abelian.Ext.mk₀_homEquiv₀_apply]
      _ = Abelian.Ext.mk₀ f := hy
  · intro h e
    have hFree :
        ∀ x : Abelian.Ext
          ((Condensed.profiniteFree Coeff).obj
            (stoneanPresentationCechPairs T)) (GS S) 1, x = 0 :=
      freeProfinite_extOne_genuineSolid_vanishes
        (stoneanPresentationCechPairs T) S
    have hzero :
        (Abelian.Ext.mk₀ (stoneanCechRelationToKernel T)).comp
          e (zero_add 1) = 0 := hFree _
    obtain ⟨x, hx⟩ :=
      Abelian.Ext.contravariant_sequence_exact₃
        hS (GS S) e hzero (by decide : 1 + 0 = 1)
    obtain ⟨g, hg⟩ := h (Abelian.Ext.homEquiv₀ x)
    have hmk :
        (Abelian.Ext.mk₀
          (kernel.ι (stoneanCechRelationToKernel T))).comp
            (Abelian.Ext.mk₀ g) (zero_add 0) = x := by
      simpa only [Abelian.Ext.mk₀_comp_mk₀,
        Abelian.Ext.mk₀_homEquiv₀_apply] using
          congrArg Abelian.Ext.mk₀ hg
    have hconn : hS.extClass.comp x (by decide : 1 + 0 = 1) = 0 := by
      rw [← hmk]
      exact hS.extClass_comp_assoc (Abelian.Ext.mk₀ g)
    exact hx.symm.trans hconn

/-- The first unproved higher-Ext vanishing is equivalent to a
specific extension property on actual second Čech relations. -/
theorem freeSolid_extTwo_vanishes_iff_secondRelation_hom_extends
    (T S : Profinite.{u}) :
    (∀ e : Abelian.Ext ((Condensed.profiniteFree Coeff).obj T)
      (GS S) 2, e = 0) ↔
      (∀ f : stoneanCechSecondRelationKernel T ⟶ GS S,
        ∃ g : ((Condensed.profiniteFree Coeff).obj
            (stoneanPresentationCechPairs T)) ⟶ GS S,
          kernel.ι (stoneanCechRelationToKernel T) ≫ g = f) := by
  exact (freeSolid_extTwo_vanishes_iff_stoneanKernel_extOne_vanishes
    T S).trans
    (stoneanKernel_extOne_vanishes_iff_secondRelation_hom_extends T S)

#check stoneanCechSecondRelationKernel
#check stoneanCechSecondRelationShortExact
#check stoneanKernel_extOne_vanishes_iff_secondRelation_hom_extends
#check freeSolid_extTwo_vanishes_iff_secondRelation_hom_extends

#print axioms stoneanCechSecondRelationShortExact
#print axioms stoneanKernel_extOne_vanishes_iff_secondRelation_hom_extends
#print axioms freeSolid_extTwo_vanishes_iff_secondRelation_hom_extends

end CMDG.CondensedCM5R0
