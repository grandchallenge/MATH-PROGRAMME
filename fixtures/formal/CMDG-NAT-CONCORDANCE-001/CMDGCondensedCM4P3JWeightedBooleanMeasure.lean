import CMDGCondensedCM4P3GFiniteBooleanMeasureCone
import CMDGCondensedCM4P3GFiniteBooleanCoefficientPushforward

/-!
# CMDG CM4-P3-J — weighted Boolean measure family and canonical limit lift

The protected Boolean-measure construction is upgraded from the unweighted Nöbeling pairing to
an arbitrary integer weight vector. This is the exact family required by the protected weighted
finite-coordinate-dependence theorem.

This file constructs only the weighted finite stages, their refinement compatibility, and the
canonical global lift through the protected finite-quotient limit. It does not assert mapping-out
injectivity, coefficient-object solidity, or P3 completion.
-/

namespace CMDG.CondensedCM4P3J.WeightedBooleanMeasure

universe u

open CategoryTheory Limits Opposite
open scoped BigOperators

open CMDG.CondensedCM4P3G.BooleanCube
open CMDG.CondensedCM4P3G.BasisSeparation
open CMDG.CondensedCM4P3G.BasisBooleanPairingR
open CMDG.CondensedCM4P3G.FreeSections
open CMDG.CondensedCM4P3G.FiniteBooleanMeasure
open CMDG.CondensedCM4P3G.KernelWeightedLocalConstancy
open CMDG.CondensedCM4P3G.FiniteBooleanCoefficientPushforward
open CMDG.CondensedCM4P2E.RightKanReconstruction

abbrev R := CMDG.CondensedCM4P3G.R.{u}

attribute [local instance] FintypeCat.fintype

noncomputable local instance weightedDiscreteQuotientFintype
    (X : Profinite.{u}) (j : DiscreteQuotient X) : Fintype j :=
  Fintype.ofFinite j

noncomputable local instance weightedDiscreteQuotientDecidableEq
    (X : Profinite.{u}) (j : DiscreteQuotient X) : DecidableEq j :=
  Classical.decEq j

/-- One weighted Boolean coefficient at a finite quotient point. -/
noncomputable def weightedFiniteBooleanCoefficient
    (X : Profinite.{u}) (a : IntegralBasisIndex X → ℤ)
    (j : DiscreteQuotient X) (q : (FiniteQuotientObject X j).obj) :
    LocallyConstant (basisBooleanCube X) R.{u} := by
  change LocallyConstant (IntegralBasisIndex X → Bool) R.{u}
  exact
    (weightedBasisBooleanPairingR X a :
      LocallyConstant X R.{u} →ₗ[R.{u}]
        LocallyConstant (IntegralBasisIndex X → Bool) R.{u})
      (finiteDeltaPullbackR X j q)

/-- The weighted coefficient family on one finite quotient. -/
noncomputable def weightedFiniteBooleanCoefficientFamily
    (X : Profinite.{u}) (a : IntegralBasisIndex X → ℤ)
    (j : DiscreteQuotient X) :
    (CMDG.CondensedCM4P2E.FiniteTransport.finiteCoefficientFamilyPresheaf
      (FiniteQuotientObject X j)).obj
      (op ((profiniteToCompHaus).obj (basisBooleanCube X))) := by
  exact fun q => weightedFiniteBooleanCoefficient X a j q

/-- Transport the weighted coefficient family to the actual finite measure presheaf. -/
noncomputable def weightedFiniteBooleanMeasureSection
    (X : Profinite.{u}) (a : IntegralBasisIndex X → ℤ)
    (j : DiscreteQuotient X) :
    (CMDG.CondensedCM4P2D.measurePresheafObj (X.diagram.obj j)).obj
      (op ((profiniteToCompHaus).obj (basisBooleanCube X))) := by
  let Q := FiniteQuotientObject X j
  let S := op ((profiniteToCompHaus).obj (basisBooleanCube X))
  let c := weightedFiniteBooleanCoefficientFamily X a j
  let d :=
    (ConcreteCategory.hom
      ((CMDG.CondensedCM4P2E.FiniteDualTransport.finiteFamilyInternalHomIso Q).inv.app S)) c
  exact
    (ConcreteCategory.hom
      ((CMDG.CondensedCM4P2E.FiniteDualTransport.finiteMeasurePresheafFamilyIso Q).inv.app S)) d

/-- Linearity of the weighted pairing transports the protected finite-delta refinement identity. -/
theorem weightedBasisBooleanPairingR_fiber_sum
    (X : Profinite.{u}) (a : IntegralBasisIndex X → ℤ)
    {j k : DiscreteQuotient X} (f : j ⟶ k) (q : k) :
    (∑ p : j,
      if finiteQuotientTransition X f p = q then
        weightedBasisBooleanPairingR X a (finiteDeltaPullbackR X j p)
      else 0) =
      weightedBasisBooleanPairingR X a (finiteDeltaPullbackR X k q) := by
  calc
    (∑ p : j,
      if finiteQuotientTransition X f p = q then
        weightedBasisBooleanPairingR X a (finiteDeltaPullbackR X j p)
      else 0) =
        weightedBasisBooleanPairingR X a
          (∑ p : j,
            if finiteQuotientTransition X f p = q then
              finiteDeltaPullbackR X j p
            else 0) := by
              rw [map_sum]
              apply Finset.sum_congr rfl
              intro p _
              by_cases hpq : finiteQuotientTransition X f p = q
              · rw [if_pos hpq, if_pos hpq]
              · rw [if_neg hpq, if_neg hpq, map_zero]
    _ = weightedBasisBooleanPairingR X a (finiteDeltaPullbackR X k q) := by
      rw [finiteDeltaPullbackR_fiber_sum X f q]

/-- The weighted Boolean coefficient family obeys the same quotient-refinement law. -/
theorem weightedFiniteBooleanCoefficient_fiber_sum
    (X : Profinite.{u}) (a : IntegralBasisIndex X → ℤ)
    {j k : DiscreteQuotient X} (f : j ⟶ k) (q : k) :
    (∑ p : j,
      if finiteQuotientTransition X f p = q then
        weightedFiniteBooleanCoefficient X a j p
      else 0) =
      weightedFiniteBooleanCoefficient X a k q := by
  change
    (∑ p : j,
      if finiteQuotientTransition X f p = q then
        weightedBasisBooleanPairingR X a (finiteDeltaPullbackR X j p)
      else 0) =
      weightedBasisBooleanPairingR X a (finiteDeltaPullbackR X k q)
  exact weightedBasisBooleanPairingR_fiber_sum X a f q

/-- Canonical finite coefficient-family pushforward carries the weighted family to the next
quotient. -/
theorem weightedFiniteBooleanCoefficientFamily_pushforward
    (X : Profinite.{u}) (a : IntegralBasisIndex X → ℤ)
    {j k : DiscreteQuotient X} (f : j ⟶ k) :
    (ConcreteCategory.hom
      ((CMDG.CondensedCM4P2E.FiniteDualTransport.finiteCoefficientFamilyPushforwardMap
        (X.fintypeDiagram.map f)).app
        (op ((profiniteToCompHaus).obj (basisBooleanCube X)))))
      (weightedFiniteBooleanCoefficientFamily X a j) =
      weightedFiniteBooleanCoefficientFamily X a k := by
  classical
  rw [finiteCoefficientFamilyPushforwardMap_eq_fiberPushforward
    (X.fintypeDiagram.map f)]
  funext q
  change
    (∑ p : j,
      if (ConcreteCategory.hom (X.fintypeDiagram.map f)) p = q then
        weightedFiniteBooleanCoefficient X a j p
      else 0) =
      weightedFiniteBooleanCoefficient X a k q
  calc
    (∑ p : j,
      if (ConcreteCategory.hom (X.fintypeDiagram.map f)) p = q then
        weightedFiniteBooleanCoefficient X a j p
      else 0) =
        ∑ p : j,
          if finiteQuotientTransition X f p = q then
            weightedFiniteBooleanCoefficient X a j p
          else 0 := by
            apply Finset.sum_congr rfl
            intro p _
            rw [fintypeDiagram_map_eq_finiteQuotientTransition X f p]
            rfl
    _ = weightedFiniteBooleanCoefficient X a k q :=
      weightedFiniteBooleanCoefficient_fiber_sum X a f q

/-- The weighted finite measure section is compatible with quotient refinement. -/
theorem weightedFiniteBooleanMeasureSection_pushforward
    (X : Profinite.{u}) (a : IntegralBasisIndex X → ℤ)
    {j k : DiscreteQuotient X} (f : j ⟶ k) :
    (ConcreteCategory.hom
      ((CMDG.CondensedCM4P2E.FiniteDualTransport.finiteMeasurePresheafMap
        (X.fintypeDiagram.map f)).app
        (op ((profiniteToCompHaus).obj (basisBooleanCube X)))))
      (weightedFiniteBooleanMeasureSection X a j) =
      weightedFiniteBooleanMeasureSection X a k := by
  let S := op ((profiniteToCompHaus).obj (basisBooleanCube X))
  let g := X.fintypeDiagram.map f
  let Tj :=
    (CMDG.CondensedCM4P2E.FiniteDualTransport.finiteFamilyInternalHomIso
      (X.fintypeDiagram.obj j)).inv ≫
      (CMDG.CondensedCM4P2E.FiniteDualTransport.finiteMeasurePresheafFamilyIso
        (X.fintypeDiagram.obj j)).inv
  let Tk :=
    (CMDG.CondensedCM4P2E.FiniteDualTransport.finiteFamilyInternalHomIso
      (X.fintypeDiagram.obj k)).inv ≫
      (CMDG.CondensedCM4P2E.FiniteDualTransport.finiteMeasurePresheafFamilyIso
        (X.fintypeDiagram.obj k)).inv
  have hcomp := finiteCoefficientToMeasure_pushforward g
  have hcomp' :
      CMDG.CondensedCM4P2E.FiniteDualTransport.finiteCoefficientFamilyPushforwardMap g ≫ Tk =
        Tj ≫ CMDG.CondensedCM4P2E.FiniteDualTransport.finiteMeasurePresheafMap g := by
    calc
      CMDG.CondensedCM4P2E.FiniteDualTransport.finiteCoefficientFamilyPushforwardMap g ≫ Tk =
          (CMDG.CondensedCM4P2E.FiniteDualTransport.finiteCoefficientFamilyPushforwardMap g ≫
            (CMDG.CondensedCM4P2E.FiniteDualTransport.finiteFamilyInternalHomIso
              (X.fintypeDiagram.obj k)).inv) ≫
            (CMDG.CondensedCM4P2E.FiniteDualTransport.finiteMeasurePresheafFamilyIso
              (X.fintypeDiagram.obj k)).inv := by
                dsimp [Tk]
                exact (Category.assoc _ _ _).symm
      _ =
          ((CMDG.CondensedCM4P2E.FiniteDualTransport.finiteFamilyInternalHomIso
              (X.fintypeDiagram.obj j)).inv ≫
            (CMDG.CondensedCM4P2E.FiniteDualTransport.finiteMeasurePresheafFamilyIso
              (X.fintypeDiagram.obj j)).inv) ≫
            CMDG.CondensedCM4P2E.FiniteDualTransport.finiteMeasurePresheafMap g := hcomp
      _ = Tj ≫ CMDG.CondensedCM4P2E.FiniteDualTransport.finiteMeasurePresheafMap g := by
            rfl
  have hcompS := congrArg (fun η => η.app S) hcomp'
  simp only [NatTrans.comp_app] at hcompS
  have hpoint := ConcreteCategory.congr_hom hcompS
    (weightedFiniteBooleanCoefficientFamily X a j)
  simp only [ConcreteCategory.comp_apply] at hpoint
  have hCoeff' :
      (ConcreteCategory.hom
        ((CMDG.CondensedCM4P2E.FiniteDualTransport.finiteCoefficientFamilyPushforwardMap
          g).app S))
        (weightedFiniteBooleanCoefficientFamily X a j) =
      weightedFiniteBooleanCoefficientFamily X a k := by
    simpa [S, g] using weightedFiniteBooleanCoefficientFamily_pushforward X a f
  rw [hCoeff'] at hpoint
  have hSectionJ :
      (ConcreteCategory.hom (Tj.app S))
          (weightedFiniteBooleanCoefficientFamily X a j) =
        weightedFiniteBooleanMeasureSection X a j := by
    rfl
  have hSectionK :
      (ConcreteCategory.hom (Tk.app S))
          (weightedFiniteBooleanCoefficientFamily X a k) =
        weightedFiniteBooleanMeasureSection X a k := by
    rfl
  rw [hSectionK, hSectionJ] at hpoint
  simpa [S, g] using hpoint.symm

/-- Package a weighted finite measure section as a morphism from the Boolean parameter cube. -/
noncomputable def weightedFiniteBooleanMeasureHom
    (X : Profinite.{u}) (a : IntegralBasisIndex X → ℤ)
    (j : DiscreteQuotient X) :
    (Condensed.profiniteFree R).obj (basisBooleanCube X) ⟶
      CMDG.CondensedCM4P2D.measureFunctor.obj (X.diagram.obj j) :=
  (freeHomSectionsEquiv
      (basisBooleanCube X)
      (CMDG.CondensedCM4P2D.measureFunctor.obj (X.diagram.obj j))).symm
    (weightedFiniteBooleanMeasureSection X a j)

/-- Weighted finite measure morphisms commute with quotient refinement. -/
theorem weightedFiniteBooleanMeasureHom_pushforward
    (X : Profinite.{u}) (a : IntegralBasisIndex X → ℤ)
    {j k : DiscreteQuotient X} (f : j ⟶ k) :
    weightedFiniteBooleanMeasureHom X a j ≫
        CMDG.CondensedCM4P2D.measureFunctor.map (X.diagram.map f) =
      weightedFiniteBooleanMeasureHom X a k := by
  let T := basisBooleanCube X
  let S := op ((profiniteToCompHaus).obj T)
  have hpost :
      ∀ {A B : CondensedMod.{u} R}
        (g : (Condensed.profiniteFree R).obj T ⟶ A)
        (h : A ⟶ B),
        freeHomSectionsEquiv T B (g ≫ h) =
          (ConcreteCategory.hom (((Condensed.forget R).map h).hom.app S))
            (freeHomSectionsEquiv T A g) := by
    intro A B g h
    change
      (coherentTopology CompHaus.{u}).uliftYonedaEquiv
        ((Condensed.freeForgetAdjunction R).homEquiv
          ((profiniteToCondensed).obj T) B (g ≫ h)) = _
    rw [Adjunction.homEquiv_naturality_right]
    rfl
  have hj :
      freeHomSectionsEquiv T
          (CMDG.CondensedCM4P2D.measureFunctor.obj (X.diagram.obj j))
          (weightedFiniteBooleanMeasureHom X a j) =
        weightedFiniteBooleanMeasureSection X a j := by
    exact Equiv.apply_symm_apply _ _
  have hk :
      freeHomSectionsEquiv T
          (CMDG.CondensedCM4P2D.measureFunctor.obj (X.diagram.obj k))
          (weightedFiniteBooleanMeasureHom X a k) =
        weightedFiniteBooleanMeasureSection X a k := by
    exact Equiv.apply_symm_apply _ _
  apply
    (freeHomSectionsEquiv T
      (CMDG.CondensedCM4P2D.measureFunctor.obj (X.diagram.obj k))).injective
  rw [hpost
      (g := weightedFiniteBooleanMeasureHom X a j)
      (h := CMDG.CondensedCM4P2D.measureFunctor.map (X.diagram.map f)),
    hj, hk]
  have hforget :
      (ConcreteCategory.hom
        (((Condensed.forget R).map
          (CMDG.CondensedCM4P2D.measureFunctor.map (X.diagram.map f))).hom.app S))
        (weightedFiniteBooleanMeasureSection X a j) =
      (ConcreteCategory.hom
        ((CMDG.CondensedCM4P2D.measureFunctor.map (X.diagram.map f)).hom.app S))
        (weightedFiniteBooleanMeasureSection X a j) := by
    rfl
  rw [hforget]
  exact weightedFiniteBooleanMeasureSection_pushforward X a f

/-- The weighted finite-stage family as one compatible cone. -/
noncomputable def weightedFiniteBooleanMeasureCone
    (X : Profinite.{u}) (a : IntegralBasisIndex X → ℤ) :
    Cone (X.diagram ⋙ CMDG.CondensedCM4P2D.measureFunctor) where
  pt := (Condensed.profiniteFree R).obj (basisBooleanCube X)
  π :=
    { app := fun j => weightedFiniteBooleanMeasureHom X a j
      naturality := by
        intro j k f
        simpa [Functor.comp_map] using
          (weightedFiniteBooleanMeasureHom_pushforward X a f) }

/-- The canonical global weighted Boolean measure family. -/
noncomputable def weightedFiniteBooleanMeasureLimitLift
    (X : Profinite.{u}) (a : IntegralBasisIndex X → ℤ) :
    (Condensed.profiniteFree R).obj (basisBooleanCube X) ⟶
      CMDG.CondensedCM4P2D.measureFunctor.obj X :=
  (measureFunctorMapConeIsLimit X).lift (weightedFiniteBooleanMeasureCone X a)

/-- The global weighted family recovers every finite-stage weighted family. -/
theorem weightedFiniteBooleanMeasureLimitLift_fac
    (X : Profinite.{u}) (a : IntegralBasisIndex X → ℤ)
    (j : DiscreteQuotient X) :
    weightedFiniteBooleanMeasureLimitLift X a ≫
        (CMDG.CondensedCM4P2D.measureFunctor.mapCone X.asLimitCone).π.app j =
      weightedFiniteBooleanMeasureHom X a j := by
  simpa [weightedFiniteBooleanMeasureLimitLift] using
    (measureFunctorMapConeIsLimit X).fac (weightedFiniteBooleanMeasureCone X a) j

#check weightedFiniteBooleanCoefficient
#check weightedFiniteBooleanMeasureSection
#check weightedFiniteBooleanCoefficient_fiber_sum
#check weightedFiniteBooleanCoefficientFamily_pushforward
#check weightedFiniteBooleanMeasureSection_pushforward
#check weightedFiniteBooleanMeasureHom
#check weightedFiniteBooleanMeasureHom_pushforward
#check weightedFiniteBooleanMeasureCone
#check weightedFiniteBooleanMeasureLimitLift
#check weightedFiniteBooleanMeasureLimitLift_fac

#print axioms weightedFiniteBooleanCoefficient_fiber_sum
#print axioms weightedFiniteBooleanCoefficientFamily_pushforward
#print axioms weightedFiniteBooleanMeasureSection_pushforward
#print axioms weightedFiniteBooleanMeasureHom_pushforward
#print axioms weightedFiniteBooleanMeasureLimitLift_fac

end CMDG.CondensedCM4P3J.WeightedBooleanMeasure
