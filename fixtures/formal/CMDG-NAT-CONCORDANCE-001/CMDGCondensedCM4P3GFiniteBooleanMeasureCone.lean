import CMDGCondensedCM4P3GFiniteBooleanMeasureHom
import CMDGCondensedCM4P2EE2

/-!
# CMDG CM4-P3-I finite Boolean measure cone and canonical limit lift

The protected P3-H family of finite Boolean measure morphisms is packaged as a cone over the
finite-quotient measure diagram. The protected P2-E limit certificate then supplies the canonical
lift into the measure object on the original profinite set.

This fixture stops at the finite-quotient cone and its canonical limit lift. It does not assert a
structured-arrow cone, a pointwise or ordinary right-Kan theorem, mapping-out injectivity,
coefficient-object solidity, or global CMDG completeness.
-/

namespace CMDG.CondensedCM4P3I.FiniteBooleanMeasureCone

universe u

open CategoryTheory Limits Opposite

open CMDG.CondensedCM4P3G.BooleanCube
open CMDG.CondensedCM4P3G.FiniteBooleanMeasureHom
open CMDG.CondensedCM4P2E.RightKanReconstruction

abbrev R := CMDG.CondensedCM4P3G.R.{u}

/-- The protected P3-H finite Boolean measure family, packaged as a cone over the finite-quotient
measure diagram. -/
noncomputable def finiteBooleanMeasureCone (X : Profinite.{u}) :
    Cone (X.diagram ⋙ CMDG.CondensedCM4P2D.measureFunctor) where
  pt := (Condensed.profiniteFree R).obj (basisBooleanCube X)
  π :=
    { app := fun j => finiteBooleanMeasureHom X j
      naturality := by
        intro j k f
        simpa [Functor.comp_map] using
          (finiteBooleanMeasureHom_pushforward X f).symm }

@[simp]
theorem finiteBooleanMeasureCone_π_app
    (X : Profinite.{u}) (j : DiscreteQuotient X) :
    (finiteBooleanMeasureCone X).π.app j = finiteBooleanMeasureHom X j := by
  rfl

/-- The canonical lift of the finite Boolean measure cone through the protected P2-E finite-quotient
limit. -/
noncomputable def finiteBooleanMeasureLimitLift (X : Profinite.{u}) :
    (Condensed.profiniteFree R).obj (basisBooleanCube X) ⟶
      CMDG.CondensedCM4P2D.measureFunctor.obj X :=
  (measureFunctorMapConeIsLimit X).lift (finiteBooleanMeasureCone X)

/-- The canonical lift recovers the protected P3-H finite Boolean measure morphism at every finite
quotient. -/
theorem finiteBooleanMeasureLimitLift_fac
    (X : Profinite.{u}) (j : DiscreteQuotient X) :
    finiteBooleanMeasureLimitLift X ≫
        (CMDG.CondensedCM4P2D.measureFunctor.mapCone X.asLimitCone).π.app j =
      finiteBooleanMeasureHom X j := by
  dsimp only [finiteBooleanMeasureLimitLift]
  rw [← finiteBooleanMeasureCone_π_app X j]
  exact (measureFunctorMapConeIsLimit X).fac (finiteBooleanMeasureCone X) j

#check finiteBooleanMeasureCone
#print axioms finiteBooleanMeasureCone
#check finiteBooleanMeasureLimitLift
#print axioms finiteBooleanMeasureLimitLift
#check finiteBooleanMeasureLimitLift_fac
#print axioms finiteBooleanMeasureLimitLift_fac

end CMDG.CondensedCM4P3I.FiniteBooleanMeasureCone
