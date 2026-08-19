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
  apply (freeHomSectionsEquiv T A).injective
  rw [freeHomSectionsEquiv_add]
  change
    weightedFiniteBooleanMeasureSection X (a + b) j =
      weightedFiniteBooleanMeasureSection X a j +
        weightedFiniteBooleanMeasureSection X b j
  exact weightedFiniteBooleanMeasureSection_add X a b j

/-- The canonical global weighted Boolean measure family is additive in the weight vector. -/
theorem weightedFiniteBooleanMeasureLimitLift_add
    (X : Profinite.{u})
    (a b : IntegralBasisIndex X → ℤ) :
    weightedFiniteBooleanMeasureLimitLift X (a + b) =
      weightedFiniteBooleanMeasureLimitLift X a +
        weightedFiniteBooleanMeasureLimitLift X b := by
  apply (measureFunctorMapConeIsLimit X).hom_ext
  intro j
  rw [Preadditive.add_comp,
    weightedFiniteBooleanMeasureLimitLift_fac X (a + b) j,
    weightedFiniteBooleanMeasureLimitLift_fac X a j,
    weightedFiniteBooleanMeasureLimitLift_fac X b j,
    weightedFiniteBooleanMeasureHom_add X a b j]

#check freeHomSectionsEquiv_add
#check weightedFiniteBooleanMeasureHom_add
#check weightedFiniteBooleanMeasureLimitLift_add

#print axioms freeHomSectionsEquiv_add
#print axioms weightedFiniteBooleanMeasureHom_add
#print axioms weightedFiniteBooleanMeasureLimitLift_add

end CMDG.CondensedCM4P3L.KernelFunctional
