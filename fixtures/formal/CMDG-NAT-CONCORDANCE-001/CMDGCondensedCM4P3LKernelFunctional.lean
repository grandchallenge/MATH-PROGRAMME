import CMDGCondensedCM4P3KKernelFiniteDependence

/-!
# CMDG CM4-P3-L — global weighted kernel-functional bridge

This successor starts the passage from the protected finite weighted Boolean measure algebra to
an additive global weighted family.  The present boundary is deliberately narrow: transport
weight additivity through the free/section equivalence and then through the protected profinite
measure limit.  No mapping-out injectivity, coefficient-object solidity, or P3 completion is
asserted here.
-/

namespace CMDG.CondensedCM4P3L.KernelFunctional

universe u

open CategoryTheory Limits Opposite

open CMDG.CondensedCM4P3G
open CMDG.CondensedCM4P3G.BasisSeparation
open CMDG.CondensedCM4P3G.BooleanCube
open CMDG.CondensedCM4P3G.FreeSections
open CMDG.CondensedCM4P3J.WeightedBooleanMeasure
open CMDG.CondensedCM4P3K.KernelFiniteDependence
open CMDG.CondensedCM4P2E.RightKanReconstruction

abbrev R := CMDG.CondensedCM4P3G.R.{u}

/-- The generic free/section equivalence preserves addition in the morphism variable. -/
theorem freeHomSectionsEquiv_add
    (T : Profinite.{u}) (A : CondensedMod.{u} R)
    (f g : (Condensed.profiniteFree R).obj T ⟶ A) :
    (show A.obj.obj (op ((profiniteToCompHaus).obj T)) from
      freeHomSectionsEquiv T A (f + g)) =
      (show A.obj.obj (op ((profiniteToCompHaus).obj T)) from
        freeHomSectionsEquiv T A f) +
        (show A.obj.obj (op ((profiniteToCompHaus).obj T)) from
          freeHomSectionsEquiv T A g) := by
  rfl

/-- The finite weighted measure morphism is additive in its external weight vector. -/
theorem weightedFiniteBooleanMeasureHom_add
    (X : Profinite.{u})
    (a b : IntegralBasisIndex X → ℤ)
    (j : DiscreteQuotient X) :
    weightedFiniteBooleanMeasureHom X (a + b) j =
      weightedFiniteBooleanMeasureHom X a j +
        weightedFiniteBooleanMeasureHom X b j := by
  let T := basisBooleanCube X
  let A := CMDG.CondensedCM4P2D.measureFunctor.obj (X.diagram.obj j)
  have hab :
      freeHomSectionsEquiv T A (weightedFiniteBooleanMeasureHom X (a + b) j) =
        weightedFiniteBooleanMeasureSection X (a + b) j := by
    exact Equiv.apply_symm_apply _ _
  have ha :
      freeHomSectionsEquiv T A (weightedFiniteBooleanMeasureHom X a j) =
        weightedFiniteBooleanMeasureSection X a j := by
    exact Equiv.apply_symm_apply _ _
  have hb :
      freeHomSectionsEquiv T A (weightedFiniteBooleanMeasureHom X b j) =
        weightedFiniteBooleanMeasureSection X b j := by
    exact Equiv.apply_symm_apply _ _
  have hsections := weightedFiniteBooleanMeasureSection_add X a b j
  have hsum := freeHomSectionsEquiv_add T A
    (weightedFiniteBooleanMeasureHom X a j)
    (weightedFiniteBooleanMeasureHom X b j)
  apply (freeHomSectionsEquiv T A).injective
  exact
    hab.trans
      (hsections.trans
        ((congrArg₂ (· + ·) ha hb).symm.trans hsum.symm))

/-- The canonical global weighted Boolean measure family is additive in the weight vector. -/
theorem weightedFiniteBooleanMeasureLimitLift_add
    (X : Profinite.{u})
    (a b : IntegralBasisIndex X → ℤ) :
    weightedFiniteBooleanMeasureLimitLift X (a + b) =
      weightedFiniteBooleanMeasureLimitLift X a +
        weightedFiniteBooleanMeasureLimitLift X b := by
  apply (measureFunctorMapConeIsLimit X).hom_ext
  intro j
  have hab := weightedFiniteBooleanMeasureLimitLift_fac X (a + b) j
  have ha := weightedFiniteBooleanMeasureLimitLift_fac X a j
  have hb := weightedFiniteBooleanMeasureLimitLift_fac X b j
  have hsum := weightedFiniteBooleanMeasureHom_add X a b j
  have hcomp :
      (weightedFiniteBooleanMeasureLimitLift X a +
          weightedFiniteBooleanMeasureLimitLift X b) ≫
          (CMDG.CondensedCM4P2D.measureFunctor.mapCone X.asLimitCone).π.app j =
        (weightedFiniteBooleanMeasureLimitLift X a ≫
          (CMDG.CondensedCM4P2D.measureFunctor.mapCone X.asLimitCone).π.app j) +
        (weightedFiniteBooleanMeasureLimitLift X b ≫
          (CMDG.CondensedCM4P2D.measureFunctor.mapCone X.asLimitCone).π.app j) := by
    exact Preadditive.add_comp _ _ _ _ _ _
  exact
    hab.trans
      (hsum.trans
        ((congrArg₂ (· + ·) ha.symm hb.symm).trans hcomp.symm))

#check freeHomSectionsEquiv_add
#check weightedFiniteBooleanMeasureHom_add
#check weightedFiniteBooleanMeasureLimitLift_add

#print axioms freeHomSectionsEquiv_add
#print axioms weightedFiniteBooleanMeasureHom_add
#print axioms weightedFiniteBooleanMeasureLimitLift_add

end CMDG.CondensedCM4P3L.KernelFunctional
